from ast import Or
from langchain.chat_models import init_chat_model
from langgraph.types import Send
from langgraph.graph import StateGraph, END, START

import json
import asyncio
import uuid
import time
import os

from typing import Any
from typing_extensions import TypedDict
from proximaai.utils.structured_output import ReasoningPlan, OrchestratorStateMultiAgent, AgentSpec, WebSearchResults

from langchain_core.load.load import loads
from langchain.load.dump import dumps

# Create alias for compatibility
OrchestratorState = OrchestratorStateMultiAgent

# Tools
from proximaai.prebuilt.prompt_templates import PromptTemplates
from proximaai.tools.tool_registry import ToolRegistry
from proximaai.tools.agent_builder import AgentBuilder
from proximaai.utils.logger import setup_logging

# Agents
from proximaai.agents.websearch_agent import create_websearch_agent
from proximaai.agents.resume_parsing_agent import ResumeParsingAgent

# LongTerm Memory & Cache
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy


# Setup logging
logger = setup_logging(level="INFO")

# Initialize the model
model = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0,
    max_tokens=4000
)

# Get all available tools from the registry
tool_registry = ToolRegistry()
tools = tool_registry.get_all_tools()

# Add agent builder to tools
agent_builder = AgentBuilder({tool.name: tool for tool in tools})
tools.append(agent_builder)

async def create_orchestrator_agent():
    """Create the main orchestrator agent with reasoning and planning capabilities."""
    async with AsyncPostgresStore.from_conn_string(os.getenv("DB_URI", "")) as store:
        await store.setup()
        
        async def resume_parse(state: OrchestratorState) -> OrchestratorState:
            parse_agent = ResumeParsingAgent()
            file_input = state.get('file_input')
            if file_input:
                result = await parse_agent.invoke(**file_input)
                state['messages'].append({ "type": "agent", "content": result['content'][0]['text'] })
            else:
                state['messages'].append({ "type": "agent", "content": "Unable to Parse Resume" })

            state['file_input']['file_data'] = "MASKED"            
            return state

        def analyze_request(state: OrchestratorState) -> OrchestratorState:
            """Analyze the user request and create a reasoning plan."""
            start_time = time.time()
            logger.log_step("analyze_request", {"user_message_length": len(state["messages"][-1]["content"]) if state["messages"] else 0})
            
            messages = state["messages"]
            user_message = messages[-1]["content"] if messages else ""
            
            # Create reasoning prompt
            reasoning_prompt = PromptTemplates('LEAD_AGENT', user_message=user_message)
            
            # Get reasoning from the model with structured output
            structured_model = model.with_structured_output(ReasoningPlan)
            reasoning_data = structured_model.invoke(reasoning_prompt)
            
            try:
                # With structured output, we get the Pydantic model directly
                if not isinstance(reasoning_data, ReasoningPlan):
                    raise Exception("Expected ReasoningPlan but got different type")
            except Exception as e:
                logger.error("Failed to get structured output", error=str(e), raw_response=str(reasoning_data))
                raise
            
            logger.info("🧠 ORCHESTRATOR REASONING", reasoning=reasoning_data.reasoning)
            logger.info("📋 EXECUTION PLAN")
            for step in reasoning_data.plan:
                logger.info(f"  Step {step.step}: {step.task}", 
                        agent_type=step.agent_type, 
                        tools_needed=step.tools_needed)
            
            duration = time.time() - start_time
            logger.log_performance("analyze_request", duration, plan_steps=len(reasoning_data.plan))
            
            return {
                **state,
                "reasoning": reasoning_data.reasoning,
                "plan": [step.model_dump() for step in reasoning_data.plan],
                "current_step": "reasoning_complete"
            }
        
        async def websearch_research(state: OrchestratorState, config: RunnableConfig, *, store: BaseStore) -> OrchestratorState:
            """Perform web search research based on the user request."""
            # Cache monitoring
            request_id = str(uuid.uuid4())[:8]
            execution_time = time.strftime("%H:%M:%S")
            logger.info(f"🔄 WEBSEARCH NODE EXECUTION - Request ID: {request_id} | Time: {execution_time} | LangGraph Cache TTL: 1 second")
            
            async with AsyncPostgresStore.from_conn_string(os.getenv("DB_URI", "")) as store:
                company_name = "Geico"  # Default to Geico for now TODO: Make this dynamic
                # Set Up Store - Postgres
                await store.setup()
                namespace = (f"websearch_research", )

                # Check Persisted Cache Web Search Results
                cache_results = await store.aget(namespace=namespace, key=f"cache_results_{company_name}", refresh_ttl=False)
                if cache_results:
                    logger.info("🔍 WEB SEARCH RESEARCH CACHE HIT")
                    memory = loads(cache_results.value["data"])

                    return {
                        **state,
                        "websearch_results": WebSearchResults(
                            **memory
                        ),
                        "current_step": "websearch_complete_cache"
                    }
                    
                    
                # Run Web Search Research
                logger.log_step("websearch_research", {"user_message_length": len(state["messages"][-1]["content"]) if state["messages"] else 0})
                
                messages = state["messages"]
                user_message = messages[-1]["content"] if messages else ""
                reasoning = state.get("reasoning", "")
                
                # Create web search agent
                websearch_agent = create_websearch_agent()
                
                # Initialize the websearch agent
                await websearch_agent.initialize()
                
                try:
                    # Extract company name from user message (simple approach)
                    user_message_lower = user_message.lower()
                    
                    
                    # Execute company about page check
                    search_result = await websearch_agent.check_company_about_page(company_name)
                    
                    logger.info("🔍 WEB SEARCH RESEARCH COMPLETED")
                    logger.info("Push results to Database")
                    await store.aput(
                        namespace=namespace, 
                        key=f"cache_results_{company_name}", 
                        value={
                            "data": dumps(search_result, ensure_ascii=False)
                        },
                        ttl=10080 # 1 week
                    )
                    return {
                        **state,
                        "websearch_results": search_result,
                        "current_step": "websearch_complete"
                    }
                    
                except Exception as e:
                    logger.error("Web search research failed", error=str(e))
                    
                    return {
                        **state,
                        "websearch_results": WebSearchResults(
                            company=company_name,
                            agent_response="",
                            tool_response=f"Error performing web research: {str(e)}",
                            intermediate_steps={}
                        ),
                        "current_step": "websearch_failed"
                    }
        
        def create_specialized_agents(state: OrchestratorState) -> OrchestratorState:
            """Create specialized agents based on the plan."""
            start_time = time.time()
            logger.log_step("create_specialized_agents", {"plan_steps": len(state["plan"])})
            
            plan = state["plan"]
            created_agents = []
            
            logger.info("🔧 CREATING SPECIALIZED AGENTS")
            
            for step in plan:
                agent_spec = {
                    "name": step["agent_type"],
                    "description": step["agent_description"],
                    "system_prompt": step["system_prompt"],
                    "tools": step["tools_needed"],
                    "model": "anthropic:claude-3-7-sonnet-latest",
                    "temperature": 0.0
                }
                
                # Get available tool names
                available_tools = [tool.name for tool in tools]

                # Filter tools to only use available ones
                available_tool_names = [tool for tool in step["tools_needed"] if tool in available_tools]
                if not available_tool_names:
                    # Use default tools if none of the requested tools are available
                    available_tool_names = available_tools
                    logger.warning(f"No requested tools available for {step['agent_type']}, using defaults", 
                                requested_tools=step["tools_needed"], 
                                default_tools=available_tool_names)
                
                # Filter tools to only use available ones
                available_tool_names = [tool for tool in step["tools_needed"] if tool in available_tools]
                
                agent_spec["tools"] = available_tool_names
                
                # Create the agent using the agent builder
                result = agent_builder._run(json.dumps(agent_spec))
                logger.info(f"Created {step['agent_type']}", result=result)
                
                # Extract agent ID properly
                agent_id = None
                if "ID: " in result:
                    id_part = result.split("ID: ")[-1]
                    # Extract just the ID part (before the closing parenthesis)
                    agent_id = id_part.split(")")[0] if ")" in id_part else id_part.split()[0]
                
                        
                # Filter tools to only use available ones
                available_tool_names = [tool for tool in step["tools_needed"] if tool in available_tools]
                if not available_tool_names:
                    # Use default tools if none of the requested tools are available
                    available_tool_names = ["web_search", "resume_optimizer"]
                    logger.warning(f"No requested tools available for {step['agent_type']}, using defaults", 
                                requested_tools=step["tools_needed"], 
                                default_tools=available_tool_names)
                
                agent_spec["tools"] = available_tool_names
                
                # Create the agent using the agent builder
                result = agent_builder._run(json.dumps(agent_spec))
                logger.info(f"Created {step['agent_type']}", result=result)
                
                # Extract agent ID properly
                agent_id = None
                if "ID: " in result:
                    id_part = result.split("ID: ")[-1]
                    # Extract just the ID part (before the closing parenthesis)
                    agent_id = id_part.split(")")[0] if ")" in id_part else id_part.split()[0]
                
                created_agents.append({
                    "step": step["step"],
                    "agent_spec": agent_spec,
                    "agent_id": uuid.uuid4()
                })
                
            return {
                **state,
                "created_agents": created_agents,
                "current_step": "agents_created"
            }
        
        def define_agent_graph_nodes(state: OrchestratorState):
            created_agents = state["created_agents"]
            max_agents_to_run = state.get("max_agents_to_run", 2)  # Default to 2 agents if not specified
            return [Send("run_agent", {"state": state, "agent_spec": agent_info["agent_spec"], "agent_id": agent_info["agent_id"]}) for agent_info in created_agents[:max_agents_to_run]]

        def run_agent(state: AgentSpec) -> OrchestratorState:
            """Execute tasks with the created agents in parallel."""
            start_time = time.time()
            graph_state = state['state'] 
            agent_info = state['agent_spec']
            
            user_message = graph_state["messages"][-1]["content"] if graph_state["messages"] else ""
            agent_results = {}

            # Get available tool names
            available_tools = [tool.name for tool in tools]
            logger.info("Available tools", tools=available_tools)
            
            # Filter tools to only use available ones
            available_tool_names = [tool for tool in agent_info["tools"] if tool in available_tools]
            if not available_tool_names:
                # Use default tools if none of the requested tools are available
                available_tool_names = available_tools
                logger.warning(f"No requested tools available for {agent_info['name']}, using defaults", 
                                requested_tools=agent_info["tools"], 
                                default_tools=available_tool_names)
            
            agent_info["tools"] = available_tool_names
            
            # Create the agent using the agent builder
            result = agent_builder._run(json.dumps(agent_info))
            logger.info(f"Created {agent_info['name']}", result=result)
            logger.info(f"🚀 EXECUTING {state['agent_spec']['name']} AGENT TASKS")
            
            # Execute each agent's task
            agent_start_time = time.time()
            if "ID: " in result:
                id_part = result.split("ID: ")[-1]
                # Extract just the ID part (before the closing parenthesis)
                agent_id = id_part.split(")")[0] if ")" in id_part else id_part.split()[0]
            logger.info("Processing agent", agent_id=agent_id)
            
            if agent_id and agent_id in agent_builder.created_agents:
                agent = agent_builder.created_agents[agent_id]["agent"]
                agent_spec = agent_info
                
                logger.info(f"Executing {agent_spec['name']}", tools=agent_spec['tools'])
                
                # Create task-specific prompt
                task_prompt = f"""
                {agent_spec['system_prompt']}
                
                USER REQUEST: {user_message}
                
                Please execute your specialized task and provide a detailed response.
                """
                
                logger.debug("Task prompt created", prompt_length=len(task_prompt))
                
                # Execute the agent
                try:
                    logger.debug("Invoking agent")
                    response = agent.invoke({
                        "messages": [{"role": "user", "content": task_prompt}]
                    })
                    
                    logger.debug("Agent response received", 
                                response_type=type(response).__name__,
                                response_keys=list(response.keys()) if isinstance(response, dict) else "Not a dict")
                    
                    # Extract the response
                    messages = response.get('messages', [])
                    logger.debug("Processing messages", message_count=len(messages))
                    
                    agent_response = ""
                    for i, message in enumerate(reversed(messages)):
                        logger.debug(f"Processing message {i}", 
                                    message_type=type(message).__name__,
                                    has_content=hasattr(message, 'content'))
                        if hasattr(message, 'content') and isinstance(message.content, str):
                            agent_response = message.content
                            logger.debug("Found response", response_length=len(agent_response))
                            break
                    
                    if not agent_response:
                        agent_response = "No response content found"
                        logger.warning("No response content found")
                    
                    agent_results[agent_spec['name']] = {
                        "response": agent_response,
                        "status": "completed"
                    }
                    
                    agent_duration = time.time() - agent_start_time
                    logger.log_agent_execution(agent_spec['name'], "completed", agent_duration)
                    
                except Exception as e:
                    agent_duration = time.time() - agent_start_time
                    logger.exception(f"Agent execution failed: {agent_spec['name']}", 
                                    agent_name=agent_spec['name'], 
                                    error=str(e))
                    agent_results[agent_spec['name']] = {
                        "response": f"Error: {str(e)}",
                        "status": "failed"
                    }
                    logger.log_agent_execution(agent_spec['name'], "failed", agent_duration)
            else:
                logger.warning("Agent not found in created agents", agent_id=agent_id)
                agent_results[f"agent_{agent_id}"] = {
                    "response": "Agent not found",
                    "status": "failed"
                }
            
            duration = time.time() - start_time
            logger.log_performance("execute_agent_tasks", duration, 
                                total_results=len(agent_results),
                                successful_results=len([r for r in agent_results.values() if r["status"] == "completed"]))

            return {
                **graph_state,
                "agent_results": agent_results,
                "current_step": "tasks_completed",
                "websearch_results": graph_state.get("websearch_results", {}),
                "user_id": graph_state.get("user_id", None),
                "file_input": graph_state.get("file_input", None)
            }

        def synthesize_final_response(state: OrchestratorState) -> OrchestratorState:
            """Synthesize responses from all agents into a final response."""
            start_time = time.time()
            logger.log_step("synthesize_final_response", {"agent_results_count": len(state["agent_results"])})
            
            agent_results = state["agent_results"]
            websearch_results = state.get("websearch_results", {})
            user_message = state["messages"][-1]["content"] if state["messages"] else ""
            reasoning = state["reasoning"]
            
            # Create synthesis prompt
            synthesis_prompt = f"""
            You are the lead orchestrator synthesizing responses from multiple specialized agents.

            ORIGINAL USER REQUEST:
            {user_message}

            ORCHESTRATOR REASONING:
            {reasoning}

            WEB SEARCH RESEARCH:
            {json.dumps(websearch_results, indent=2)}

            AGENT RESPONSES:
            {json.dumps(agent_results, indent=2)}

            Your task is to synthesize all the agent responses and web search research into a comprehensive, well-structured final response that:
            1. Addresses the user's original request completely
            2. Integrates insights from web search research and all specialized agents
            3. Provides actionable recommendations based on current market information
            4. Maintains a professional and helpful tone

            Provide your final synthesized response:
            """
            
            # Get final response from the model
            response = model.invoke(synthesis_prompt)
            final_response = response.content if hasattr(response, 'content') and isinstance(response.content, str) else str(response)
            
            logger.info("🤖 FINAL SYNTHESIZED RESPONSE", response_length=len(final_response))
            
            duration = time.time() - start_time
            logger.log_performance("synthesize_final_response", duration, response_length=len(final_response))
            
            return {
                **state,
                "final_response": final_response,
                "current_step": "complete"
            }
        
        # Create the workflow graph
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        # workflow.add_node("analyze_request", analyze_request)
        # workflow.add_node("websearch_research", websearch_research, cache_policy=CachePolicy(ttl=5))
        # workflow.add_node("create_agents", create_specialized_agents)
        # workflow.add_node("run_agent", run_agent)
        # workflow.add_node("synthesize_response", synthesize_final_response)
        workflow.add_node("Resume_Parsing_Agent", resume_parse)
        
        # Add edges
        workflow.add_edge(START, "Resume_Parsing_Agent")
        # workflow.add_edge(START, "websearch_research")
        # workflow.add_edge("analyze_request", "websearch_research")
        # workflow.add_edge("analyze_request", "create_agents")
        # workflow.add_edge("websearch_research", "synthesize_response")

        #Dynamic Conditional Edges
        # workflow.add_conditional_edges("create_agents", define_agent_graph_nodes, ["run_agent"])
        # workflow.add_edge("run_agent", "synthesize_response")
        # workflow.add_edge("synthesize_response", END)
        
        return workflow.compile(
            store=store,
            cache=InMemoryCache()
        )


def format_response(response):
    """Format the orchestrator response for better readability."""
    logger.info("🎯 ORCHESTRATOR SUMMARY")
    
    if "final_response" in response:
        logger.info("✅ Task completed successfully!", 
                   agents_created=len(response.get('created_agents', [])),
                   tasks_executed=len(response.get('agent_results', {})))
    else:
        logger.error("❌ Task did not complete successfully", 
                    current_step=response.get('current_step', 'unknown'))

if __name__ == "__main__":
    async def main():
        conversation = {
            "messages": [
                {"role": "user", "content": "I want to apply for a job at Meta. I have a resume that I need to optimize for the job and understand if I meet all qualifications.\nGoogle's job description is:ML Engineer with 3+ years of experience in machine learning and deep learning.\n My Resume is:Education:Bachelor of Science in Computer Science Experience:3+ years of experience in machine learning and deep learning"}
            ],
            "reasoning": "",
            "plan": [],
            "created_agents": [],
            "agent_results": {},
            "final_response": "",
            "current_step": "start",
            "user_id": "test1a"
        }
        
        logger.info("🚀 Starting ProximaAI Multi-Agent Orchestrator...")
        
        orchestrator = await create_orchestrator_agent()
        
        # Use streaming to see cache metadata
        logger.info("🔄 Streaming execution with cache monitoring...")
        first_response = await orchestrator.ainvoke(conversation)
        logger.info(f"📊 First response completed")
        
        # Wait for LangGraph cache to expire (TTL=N second)
        logger.info("⏳ Waiting for LangGraph cache to expire (TTL=N second)...")
        await asyncio.sleep(2)  # Wait 2 seconds (longer than TTL=N)
        
        logger.info("🔄 Second call after cache expiration...")
        second_response = await orchestrator.ainvoke(conversation)
        logger.info(f"📊 Second response completed")
        
        # Test streaming to see cache metadata
        logger.info("🔄 Testing streaming for cache metadata...")
        async for chunk in orchestrator.astream(conversation, stream_mode='updates'):
            if '__metadata__' in chunk:
                logger.info(f"🎯 Cache metadata found: {chunk['__metadata__']}")
        
        format_response(second_response)
    
    asyncio.run(main())
    