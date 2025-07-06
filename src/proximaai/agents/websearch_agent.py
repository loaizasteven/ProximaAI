from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from typing import Dict, Any, Union, Optional
import asyncio
from proximaai.mcp.langchain_mcp_transform import get_mcp_tools
from proximaai.utils.logger import get_logger

from langchain_core.language_models import (
    BaseChatModel,
    LanguageModelInput,
    LanguageModelLike,
)

logger = get_logger("websearch_agent")


class WebSearchAgent:
    """A specialized agent for checking company about pages using MCP tools."""
    
    def __init__(self, model_name: str = "anthropic:claude-3-7-sonnet-latest", temperature: float = 0.0):
        """Initialize the web search agent."""
        self.model = init_chat_model(model_name, temperature=temperature)
        self.agent = None
        logger.info("WebSearchAgent initialized", model=model_name)
    
    async def initialize(self):
        """Initialize MCP tools."""
        mcp_tools = await get_mcp_tools()
        self.agent = create_react_agent(
            model=self.model,
            tools=mcp_tools,
            prompt="You are a company research specialist. Your only task is to find and analyze company about pages."
        )
    
    async def check_company_about_page(self, company_name: str) -> Dict[str, Any]:
        """Check the about page of a specific company."""
        logger.info("Checking company about page", company_name=company_name)
        
        task_prompt = f"""
        Find and analyze the about page for {company_name}.
        
        Search for: "{company_name} about us" or "{company_name} company about"
        
        Focus only on:
        1. Company mission and values
        2. Company history and background
        3. Company culture and work environment
        4. Key company information from their official about page
        
        Do not search for job postings, news, or other information. Only focus on the company's about page content.
        """
        
        if self.agent is None:
            return {
                "company": company_name,
                "response": "Agent not initialized",
                "status": "failed",
                "agent_type": "company_about_page"
            }
        
        response = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": task_prompt}]
        })
        
        messages = response.get('messages', [])
        agent_response = ""
        for message in reversed(messages):
            if hasattr(message, 'content') and isinstance(message.content, str):
                agent_response = message.content
                break
        
        return {
            "company": company_name,
            "response": agent_response,
            "status": "completed",
            "agent_type": "company_about_page"
        }


def create_websearch_agent(model_name: str = "anthropic:claude-3-7-sonnet-latest", temperature: float = 0.0) -> WebSearchAgent:
    """Factory function to create a web search agent."""
    return WebSearchAgent(model_name=model_name, temperature=temperature)
