from pydantic import BaseModel, Field
from typing import List, Dict, Any, Annotated, Optional
from typing_extensions import TypedDict
import operator

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


class ResumeParseStructure(TypedDict):
    file_data: str
    file_name: str

# State definition for the orchestrator
class OrchestratorState(TypedDict):
    messages: List[Dict[str, Any]]
    reasoning: str
    plan: List[Dict[str, Any]]
    created_agents: List[Dict[str, Any]]
    agent_results: Dict[str, Any]
    final_response: str
    current_step: str

def select_first(current_value, new_values):
    """
    Custom reducer that selects the first value from the list of new_values.
    """
    if new_values:
        # Assuming new_values is a list of updates, return the first one
        # Or, if it's a single value update, just return new_values
        return new_values
    else:
        return current_value

def merge_dictionaries(current_dict: Dict[str, Any], new_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Custom reducer to merge two dictionaries.
    Prioritizes values from the new_dict in case of key conflicts.
    """
    if current_dict is None:
        current_dict = {}  # Handle the initial case where current_dict is None
    if new_dict is None:
        new_dict = {}  # Handle the case where new_dict is None
    return {**current_dict, **new_dict}  # Use dictionary unpacking to merge


class WebSearchResults(TypedDict):
    company: str
    agent_response: str
    tool_response: str
    intermediate_steps: Dict[str, Any]

class OrchestratorStateMultiAgent(TypedDict):
    # https://langchain-ai.github.io/langgraph/troubleshooting/errors/INVALID_CONCURRENT_GRAPH_UPDATE/
    messages: Annotated[List[Dict[str, Any]], operator.add]
    file_input: Annotated[ResumeParseStructure, select_first]
    reasoning: Annotated[str, select_first]
    plan: Annotated[List[Dict[str, Any]], select_first]
    created_agents: Annotated[List[Dict[str, Any]], select_first]
    agent_results: Annotated[Dict[str, Any], merge_dictionaries]  # Use the custom reducer
    websearch_results: Annotated[WebSearchResults, select_first]  # Web search research results
    final_response: Annotated[str, select_first]
    current_step: Annotated[str, select_first]
    user_id: Annotated[Optional[str], select_first]
    tailored_resume_markdown: Annotated[Optional[str], select_first]
    formatted_resume_markdown: Annotated[Optional[str], select_first]
    resume_html: Annotated[Optional[str], select_first]
    tailor_reasoning: Annotated[Optional[Any], select_first]

class AgentSpec(TypedDict):
        state: OrchestratorState
        agent_spec: Any
        agent_id: Any

class MarkdownResponse(BaseModel):
    text: str = Field(..., description="Markdown code as text, that can be easily rendered")

class SectionChange(BaseModel):
    section: str = Field(description="The section of the resume that was changed (e.g., 'Experience', 'Education', etc.)")
    change: str = Field(description="A description of what was changed, added, or removed in this section.")
    justification: str = Field(description="The reasoning for this change, addition, or removal.")

class TailoredResumeWithReasoning(BaseModel):
    tailored_resume_markdown: str = Field(description="The tailored resume as a markdown string, preserving all original sections unless truly irrelevant.")
    reasoning: List[SectionChange] = Field(description="A list of section-by-section reasoning for each change, addition, or removal.")