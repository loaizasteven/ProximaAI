"""
AgentBuilder Tool - Dynamically creates agents at runtime based on reasoning plans.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.tools import BaseTool
import json
import uuid
from proximaai.utils.logger import get_logger

logger = get_logger("agent_builder")


@dataclass
class AgentSpec:
    """Specification for creating a new agent."""
    name: str
    description: str
    system_prompt: str
    tools: List[str]  # List of tool names to attach
    model: str = "anthropic:claude-3-7-sonnet-latest"
    temperature: float = 0.0


class AgentBuilder(BaseTool):
    """Tool for dynamically creating agents at runtime."""
    
    def __init__(self, tool_registry: Dict[str, BaseTool]):
        super().__init__(
            name="agent_builder",
            description="""
            Creates specialized agents at runtime based on reasoning plans.
            Use this when you need to create a new agent for a specific task.
            
            Input should be a JSON string with:
            - name: Agent name
            - description: What this agent does
            - system_prompt: The system prompt for the agent
            - tools: List of tool names to attach
            - model: Model to use (optional, defaults to claude-3-7-sonnet)
            - temperature: Temperature setting (optional, defaults to 0.0)
            """
        )
        # Store instance variables in a way that doesn't conflict with Pydantic
        self._tool_registry = tool_registry
        self._created_agents: Dict[str, Any] = {}
        logger.info("AgentBuilder initialized", available_tools=len(tool_registry))
    
    @property
    def tool_registry(self) -> Dict[str, BaseTool]:
        """Get the tool registry."""
        return self._tool_registry
    
    @property
    def created_agents(self) -> Dict[str, Any]:
        """Get the created agents dictionary."""
        return self._created_agents
    
    def _run(self, agent_spec_json: str) -> str:
        """Create a new agent based on the specification."""
        try:
            logger.debug("Creating new agent", spec_json=agent_spec_json)
            spec_data = json.loads(agent_spec_json)
            spec = AgentSpec(**spec_data)
            
            logger.info("Agent specification parsed", 
                       agent_name=spec.name, 
                       requested_tools=spec.tools,
                       model=spec.model)
            
            # Get the specified tools from registry
            agent_tools = []
            missing_tools = []
            for tool_name in spec.tools:
                if tool_name in self._tool_registry:
                    agent_tools.append(self._tool_registry[tool_name])
                else:
                    missing_tools.append(tool_name)
            
            if missing_tools:
                logger.error("Missing tools in registry", missing_tools=missing_tools)
                return f"Error: Tools not found in registry: {', '.join(missing_tools)}"
            
            logger.debug("Tools retrieved successfully", tool_count=len(agent_tools))
            
            # Initialize the model
            model = init_chat_model(spec.model, temperature=spec.temperature)
            logger.debug("Model initialized", model=spec.model, temperature=spec.temperature)
            
            # Create the agent
            agent = create_react_agent(
                model=model,
                tools=agent_tools,
                prompt=spec.system_prompt
            )
            
            # Store the created agent
            agent_id = f"{spec.name}_{uuid.uuid4().hex[:8]}"
            self._created_agents[agent_id] = {
                "agent": agent,
                "spec": spec,
                "tools": agent_tools
            }
            
            logger.info("Agent created successfully", 
                       agent_name=spec.name, 
                       agent_id=agent_id, 
                       tool_count=len(agent_tools))
            
            return f"Successfully created agent '{spec.name}' (ID: {agent_id}) with {len(agent_tools)} tools"
            
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON specification", error=str(e))
            return "Error: Invalid JSON specification"
        except Exception as e:
            logger.exception("Error creating agent", error=str(e))
            return f"Error creating agent: {str(e)}"
    
    def get_agent(self, agent_id: str) -> Optional[Any]:
        """Retrieve a created agent by ID."""
        agent = self._created_agents.get(agent_id)
        if agent:
            logger.debug("Agent retrieved", agent_id=agent_id)
        else:
            logger.warning("Agent not found", agent_id=agent_id)
        return agent
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all created agents."""
        agents = [
            {
                "id": agent_id,
                "name": data["spec"].name,
                "description": data["spec"].description,
                "tools": [tool.name for tool in data["tools"]]
            }
            for agent_id, data in self._created_agents.items()
        ]
        logger.info("Agents listed", agent_count=len(agents))
        return agents 