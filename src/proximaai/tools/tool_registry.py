"""
Tool Registry - Manages all available tools for the ProximaAI system.
"""

from typing import Dict, List, Any, Optional
from langchain.tools import BaseTool
from proximaai.tools.agent_builder import AgentBuilder
from proximaai.tools.web_search import WebSearchTool, CompanyResearchTool
from proximaai.tools.resume_tools import ResumeParserTool, ResumeOptimizerTool
from proximaai.tools.career_coaching import CareerAdvisorTool, InterviewPreparationTool, SkillDevelopmentTool
from proximaai.tools.job_search import JobSearchTool, JobAnalyzerTool, ApplicationTrackerTool


class ToolRegistry:
    """Registry for managing all available tools in the ProximaAI system."""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all available tools."""
        # Web Search Tools
        self.tools["web_search"] = WebSearchTool()
        self.tools["company_research"] = CompanyResearchTool()
        
        # Resume Tools
        self.tools["resume_parser"] = ResumeParserTool()
        self.tools["resume_optimizer"] = ResumeOptimizerTool()
        
        # Career Coaching Tools
        self.tools["career_advisor"] = CareerAdvisorTool()
        self.tools["interview_preparer"] = InterviewPreparationTool()
        self.tools["skill_developer"] = SkillDevelopmentTool()
        
        # Job Search Tools
        self.tools["job_search"] = JobSearchTool()
        self.tools["job_analyzer"] = JobAnalyzerTool()
        self.tools["application_tracker"] = ApplicationTrackerTool()
        
        # Agent Builder (needs access to tool registry)
        self.tools["agent_builder"] = AgentBuilder(self.tools)
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a specific tool by name."""
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all available tools."""
        return list(self.tools.values())
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get tools by category."""
        category_mapping = {
            "web_search": ["web_search", "company_research"],
            "resume": ["resume_parser", "resume_optimizer"],
            "career_coaching": ["career_advisor", "interview_preparer", "skill_developer"],
            "job_search": ["job_search", "job_analyzer", "application_tracker"],
            "agent_building": ["agent_builder"]
        }
        
        tool_names = category_mapping.get(category, [])
        return [self.tools[name] for name in tool_names if name in self.tools]
    
    def list_available_tools(self) -> Dict[str, List[str]]:
        """List all available tools organized by category."""
        return {
            "web_search": ["web_search", "company_research"],
            "resume": ["resume_parser", "resume_optimizer"],
            "career_coaching": ["career_advisor", "interview_preparer", "skill_developer"],
            "job_search": ["job_search", "job_analyzer", "application_tracker"],
            "agent_building": ["agent_builder"]
        }
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all available tools."""
        return {
            name: tool.description for name, tool in self.tools.items()
        }
    
    def add_custom_tool(self, tool_name: str, tool: BaseTool):
        """Add a custom tool to the registry."""
        self.tools[tool_name] = tool
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from the registry."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
