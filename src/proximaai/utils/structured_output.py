from pydantic import BaseModel, Field
from typing import List, Dict, Any, TypedDict


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

# State definition for the orchestrator
class OrchestratorState(TypedDict):
    messages: List[Dict[str, Any]]
    reasoning: str
    plan: List[Dict[str, Any]]
    created_agents: List[Dict[str, Any]]
    agent_results: Dict[str, Any]
    final_response: str
    current_step: str
