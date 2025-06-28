from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from typing import Dict, List, Any, TypedDict, Annotated
from dataclasses import dataclass
import json
import asyncio
from datetime import datetime
import re
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

from proximaai.prebuilt.prompt_templates import PromptTemplates
from proximaai.tools.tool_registry import ToolRegistry
from proximaai.tools.agent_builder import AgentBuilder

# Pydantic models for structured output
class AgentPlan(BaseModel):
    step: int = Field(description="Step number in the execution plan")
    task: str = Field(description="Description of the task to be performed")
    agent_type: str = Field(description="Type of agent needed for this task")
    agent_description: str = Field(description="What this agent will do")
    tools_needed: List[str] = Field(description="List of tool names needed for this agent", default_factory=list)
    system_prompt: str = Field(description="Specialized system prompt for this agent", default="")

class ReasoningPlan(BaseModel):
    reasoning: str = Field(description="Detailed reasoning about what needs to be done")
    plan: List[AgentPlan] = Field(description="List of steps in the execution plan")

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

# State definition for the orchestrator
class OrchestratorState(TypedDict):
    messages: List[Dict[str, Any]]
    reasoning: str
    plan: List[Dict[str, Any]]
    created_agents: List[Dict[str, Any]]
    agent_results: Dict[str, Any]
    final_response: str
    current_step: str

def create_orchestrator_agent():
    """Create the main orchestrator agent with reasoning and planning capabilities."""
    
    def analyze_request(state: OrchestratorState) -> OrchestratorState:
        """Analyze the user request and create a reasoning plan."""
        messages = state["messages"]
        user_message = messages[-1]["content"] if messages else ""
        
        # Create reasoning prompt
        reasoning_prompt = f"""
        You are the lead orchestrator for the VELOA multi-agent system. Analyze the user request and create a reasoning plan.

        USER REQUEST: {user_message}

        Create a detailed reasoning plan with:
        1. Reasoning about what the user wants
        2. A step-by-step execution plan with specialized agents
        3. Each step must include: step number, task description, agent type, agent description, tools needed, and system prompt

        Be concise but complete. Ensure all required fields are provided.
        """
        
        # Get reasoning from the model with structured output
        structured_model = model.with_structured_output(ReasoningPlan)
        reasoning_data = structured_model.invoke(reasoning_prompt)
        
        try:
            # With structured output, we get the Pydantic model directly
            if not isinstance(reasoning_data, ReasoningPlan):
                raise Exception("Expected ReasoningPlan but got different type")
        except Exception as e:
            print(f"[ERROR] Failed to get structured output: {e}")
            print("Raw response:")
            print(reasoning_data)
            raise
        
        print("\n" + "="*80)
        print("🧠 ORCHESTRATOR REASONING")
        print("="*80)
        print(reasoning_data.reasoning)
        print("\n📋 EXECUTION PLAN:")
        for step in reasoning_data.plan:
            print(f"  Step {step.step}: {step.task}")
            print(f"    Agent: {step.agent_type}")
            print(f"    Tools: {', '.join(step.tools_needed)}")
        print("="*80)
        
        return {
            **state,
            "reasoning": reasoning_data.reasoning,
            "plan": [step.model_dump() for step in reasoning_data.plan],
            "current_step": "reasoning_complete"
        }
    
    def create_specialized_agents(state: OrchestratorState) -> OrchestratorState:
        """Create specialized agents based on the plan."""
        plan = state["plan"]
        created_agents = []
        
        print("\n🔧 CREATING SPECIALIZED AGENTS")
        print("="*80)
        
        # Get available tool names
        available_tools = [tool.name for tool in tools]
        print(f"Available tools: {', '.join(available_tools)}")
        
        for step in plan:
            agent_spec = {
                "name": step["agent_type"],
                "description": step["agent_description"],
                "system_prompt": step["system_prompt"],
                "tools": step["tools_needed"],
                "model": "anthropic:claude-3-7-sonnet-latest",
                "temperature": 0.0
            }
            
            # Filter tools to only use available ones
            available_tool_names = [tool for tool in step["tools_needed"] if tool in available_tools]
            if not available_tool_names:
                # Use default tools if none of the requested tools are available
                available_tool_names = ["web_search", "resume_optimizer"]
            
            agent_spec["tools"] = available_tool_names
            
            # Create the agent using the agent builder
            result = agent_builder._run(json.dumps(agent_spec))
            print(f"  Created {step['agent_type']}: {result}")
            
            # Extract agent ID properly
            agent_id = None
            if "ID: " in result:
                id_part = result.split("ID: ")[-1]
                # Extract just the ID part (before the closing parenthesis)
                agent_id = id_part.split(")")[0] if ")" in id_part else id_part.split()[0]
            
            created_agents.append({
                "step": step["step"],
                "agent_spec": agent_spec,
                "agent_id": agent_id
            })
        
        print("="*80)
        
        return {
            **state,
            "created_agents": created_agents,
            "current_step": "agents_created"
        }
    
    def execute_agent_tasks(state: OrchestratorState) -> OrchestratorState:
        """Execute tasks with the created agents in parallel."""
        created_agents = state["created_agents"]
        user_message = state["messages"][-1]["content"] if state["messages"] else ""
        agent_results = {}
        
        print("\n🚀 EXECUTING AGENT TASKS")
        print("="*80)
        print(f"Number of agents to execute: {len(created_agents)}")
        
        # Execute each agent's task
        for agent_info in created_agents:
            agent_id = agent_info["agent_id"]
            print(f"Processing agent ID: {agent_id}")
            
            if agent_id and agent_id in agent_builder.created_agents:
                agent = agent_builder.created_agents[agent_id]["agent"]
                agent_spec = agent_info["agent_spec"]
                
                print(f"  Executing {agent_spec['name']}...")
                print(f"    Tools: {agent_spec['tools']}")
                
                # Create task-specific prompt
                task_prompt = f"""
                {agent_spec['system_prompt']}
                
                USER REQUEST: {user_message}
                
                Please execute your specialized task and provide a detailed response.
                """
                
                print(f"    Task prompt length: {len(task_prompt)} characters")
                
                # Execute the agent
                try:
                    print("    Invoking agent...")
                    response = agent.invoke({
                        "messages": [{"role": "user", "content": task_prompt}]
                    })
                    
                    print(f"    Agent response type: {type(response)}")
                    print(f"    Agent response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
                    
                    # Extract the response
                    messages = response.get('messages', [])
                    print(f"    Number of messages: {len(messages)}")
                    
                    agent_response = ""
                    for i, message in enumerate(reversed(messages)):
                        print(f"    Message {i}: type={type(message)}, has_content={hasattr(message, 'content')}")
                        if hasattr(message, 'content') and isinstance(message.content, str):
                            agent_response = message.content
                            print(f"    Found response: {len(agent_response)} characters")
                            break
                    
                    if not agent_response:
                        agent_response = "No response content found"
                        print("    ⚠️ No response content found")
                    
                    agent_results[agent_spec['name']] = {
                        "response": agent_response,
                        "status": "completed"
                    }
                    
                    print(f"    ✅ {agent_spec['name']} completed")
                    
                except Exception as e:
                    print(f"    ❌ Exception: {str(e)}")
                    agent_results[agent_spec['name']] = {
                        "response": f"Error: {str(e)}",
                        "status": "failed"
                    }
                    print(f"    ❌ {agent_spec['name']} failed: {str(e)}")
            else:
                print(f"  ⚠️ Agent ID {agent_id} not found in created agents")
                agent_results[f"agent_{agent_id}"] = {
                    "response": "Agent not found",
                    "status": "failed"
                }
        
        print(f"Total agent results: {len(agent_results)}")
        print("="*80)
        
        return {
            **state,
            "agent_results": agent_results,
            "current_step": "tasks_completed"
        }
    
    def synthesize_final_response(state: OrchestratorState) -> OrchestratorState:
        """Synthesize responses from all agents into a final response."""
        agent_results = state["agent_results"]
        user_message = state["messages"][-1]["content"] if state["messages"] else ""
        reasoning = state["reasoning"]
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        You are the lead orchestrator synthesizing responses from multiple specialized agents.

        ORIGINAL USER REQUEST:
        {user_message}

        ORCHESTRATOR REASONING:
        {reasoning}

        AGENT RESPONSES:
        {json.dumps(agent_results, indent=2)}

        Your task is to synthesize all the agent responses into a comprehensive, well-structured final response that:
        1. Addresses the user's original request completely
        2. Integrates insights from all specialized agents
        3. Provides actionable recommendations
        4. Maintains a professional and helpful tone

        Provide your final synthesized response:
        """
        
        # Get final response from the model
        response = model.invoke(synthesis_prompt)
        final_response = response.content if hasattr(response, 'content') and isinstance(response.content, str) else str(response)
        
        print("\n" + "="*80)
        print("🤖 FINAL SYNTHESIZED RESPONSE")
        print("="*80)
        print(final_response)
        print("="*80)
        
        return {
            **state,
            "final_response": final_response,
            "current_step": "complete"
        }
    
    # Create the workflow graph
    workflow = StateGraph(OrchestratorState)
    
    # Add nodes
    workflow.add_node("analyze_request", analyze_request)
    workflow.add_node("create_agents", create_specialized_agents)
    workflow.add_node("execute_tasks", execute_agent_tasks)
    workflow.add_node("synthesize_response", synthesize_final_response)
    
    # Add edges
    workflow.add_edge(START, "analyze_request")
    workflow.add_edge("analyze_request", "create_agents")
    workflow.add_edge("create_agents", "execute_tasks")
    workflow.add_edge("execute_tasks", "synthesize_response")
    workflow.add_edge("synthesize_response", END)
    
    return workflow.compile()

# Create the orchestrator
orchestrator = create_orchestrator_agent()

def format_response(response):
    """Format the orchestrator response for better readability."""
    print("\n" + "="*80)
    print("🎯 ORCHESTRATOR SUMMARY")
    print("="*80)
    
    if "final_response" in response:
        print("✅ Task completed successfully!")
        print(f"📊 Agents created: {len(response.get('created_agents', []))}")
        print(f"📈 Tasks executed: {len(response.get('agent_results', {}))}")
    else:
        print("❌ Task did not complete successfully")
        print(f"Current step: {response.get('current_step', 'unknown')}")
    
    print("="*80)

if __name__ == "__main__":
    conversation = {
        "messages": [
            {"role": "user", "content": """
            I want to apply for a job at Google. I have a resume that I need to optimize for the job and understand if I meet all qualifications.

            Google's job description is:
               ML Engineer with 3+ years of experience in machine learning and deep learning.

            My Resume is:
               Education:
                  Bachelor of Science in Computer Science
                  Master of Science in Machine Learning

               Experience:
                  - 3+ years of experience in machine learning and deep learning
                  - 2+ years of experience in software development
            """}
        ],
        "reasoning": "",
        "plan": [],
        "created_agents": [],
        "agent_results": {},
        "final_response": "",
        "current_step": "start"
    }
    
    print("🚀 Starting ProximaAI Multi-Agent Orchestrator...")
    print("📝 User Request: Resume analysis and job application optimization")
    print("-" * 50)
    
    response = orchestrator.invoke(conversation)
    format_response(response)