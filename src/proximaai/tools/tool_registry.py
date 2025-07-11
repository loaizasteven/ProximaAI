"""
Tool Registry - Manages all available tools for the ProximaAI system.
"""

from typing import Dict, List, Optional
from langchain.tools import BaseTool
from collections.abc import Mapping
from langchain_mcp_adapters.sessions import Connection

# Tools and MCP
from proximaai.tools.agent_builder import AgentBuilder
from langchain_mcp_adapters.client import MultiServerMCPClient
from proximaai.tools.perplexity_search import PerplexityWebSearchTool
from proximaai.mcp.server_connections import mcp_servers

# Other imports
from proximaai.utils.logger import get_logger

logger = get_logger("tool_registry")


class ToolRegistry:
    """Registry for managing all available tools in the ProximaAI system."""
    
    def __init__(self, tools:Dict[str, BaseTool]={}):
        self.tools = tools

        logger.info("Initializing ToolRegistry")
        self._initialize_tools()
        logger.info("ToolRegistry initialized", total_tools=len(self.tools))
    
    @classmethod
    async def async_init(cls, tools={}):
        "Lazy/Deferred Tool Registration must be called after server is running. Fetch registry during tool binding on node"
        instances = cls(tools)
        async def get_mcp_tools(
            mcp_connections: Mapping[str, Connection] = mcp_servers #Covariate type checking for subclasses
        ):
            logger.info("Fetching MCP Tools")
            client = MultiServerMCPClient(dict(mcp_connections))
            mcp_tools = await client.get_tools()
            for tool in mcp_tools:
                instances.tools[tool.name] = tool
                
        await get_mcp_tools()
        logger.info("ToolRegistry with MCP", total_tools=len(instances.tools))
        return instances

    def _initialize_tools(self):
        """Initialize all available tools."""
        logger.debug("Initializing tools")
        
        # Web Search Tools
        self.tools["perplexity_research"] = PerplexityWebSearchTool()
        logger.debug("Web search tools initialized")
        
        # Agent Builder (needs access to tool registry)
        self.tools["agent_builder"] = AgentBuilder(self.tools)
        logger.debug("Agent builder initialized")
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a specific tool by name."""
        tool = self.tools.get(tool_name)
        if tool:
            logger.debug("Tool retrieved", tool_name=tool_name)
        else:
            logger.warning("Tool not found", tool_name=tool_name)
        return tool
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all available tools."""
        tools_list = list(self.tools.values())
        logger.debug("All tools retrieved", tool_count=len(tools_list))
        return tools_list
    
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
        categories = {
            "web_search": ["web_search", "company_research"],
            "resume": ["resume_parser", "resume_optimizer"],
            "career_coaching": ["career_advisor", "interview_preparer", "skill_developer"],
            "job_search": ["job_search", "job_analyzer", "application_tracker"],
            "agent_management": ["agent_builder"]
        }
        
        # Filter to only include tools that actually exist
        available_categories = {}
        for category, tool_names in categories.items():
            available_tools = [name for name in tool_names if name in self.tools]
            if available_tools:
                available_categories[category] = available_tools
        
        logger.debug("Available tools listed by category", categories=available_categories)
        return available_categories
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all available tools."""
        descriptions = {}
        for name, tool in self.tools.items():
            descriptions[name] = tool.description
        
        logger.debug("Tool descriptions retrieved", tool_count=len(descriptions))
        return descriptions
    
    def add_custom_tool(self, tool_name: str, tool: BaseTool):
        """Add a custom tool to the registry."""
        self.tools[tool_name] = tool
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from the registry."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
