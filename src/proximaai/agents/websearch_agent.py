from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from typing import Dict, Any, Union, Optional
import asyncio
import traceback
from proximaai.tools.perplexity_search import PerplexityWebSearchTool
from proximaai.utils.logger import get_logger

from proximaai.utils.structured_output import WebSearchResults

logger = get_logger("websearch_agent")

class WebSearchAgent:
    """A specialized agent for checking company about pages using Perplexity only."""
    
    def __init__(self, model_name: str = "anthropic:claude-3-7-sonnet-latest", temperature: float = 0.0):
        """Initialize the web search agent."""
        self.model = init_chat_model(model_name, temperature=temperature)
        self.agent = None
        logger.info("WebSearchAgent initialized", model=model_name)
    
    async def initialize(self):
        """Initialize Perplexity tool only."""
        self.agent = create_react_agent(
            model=self.model,
            tools=[PerplexityWebSearchTool()],
            prompt="You are a company research specialist. Your only task is to find and analyze company about pages."
        )
    
    async def check_company_about_page(self, company_name: str) -> WebSearchResults:
        """Check the about page of a specific company."""
        logger.info("Checking company about page", company_name=company_name)
        
        task_prompt = f"""
        Using the tools availeble to you find and analyze the about page for {company_name}.
        
        Search for: "{company_name} about us" or "{company_name} company about"
        
        Focus only on:
        1. Company mission and values
        
        Do not search for job postings, news, or other information. Only focus on the company's about page content. If the tool does not return relevant information, 
        you should return "No relevant information found".
        """
        
        if self.agent is None:
            return WebSearchResults(
                company=company_name,
                agent_response="Agent not initialized",
                tool_response="Tool not initialized",
                intermediate_steps=[]
            )
        
        response = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": task_prompt}]
        })

        try:
            messages = response.get('messages', [])
            agent_response = messages[-1].content[0]['text']
            tool_response = ""
            for message in reversed(messages):
                if hasattr(message, 'content') and isinstance(message.content, str):
                    print("her", message)
                    logger.info("Tool Called Response", Tool=message.name)
                    tool_response = message.content
                    break
            
            return WebSearchResults(
                company=company_name,
                agent_response=agent_response,
                tool_response=tool_response,
                intermediate_steps=messages
            )
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error("Error in websearch_agent", traceback=error_traceback)
            return WebSearchResults(
                company=company_name,
                agent_response=f"Traceback:\n{error_traceback}",
                tool_response="Error in websearch_agent",
                intermediate_steps=messages
            )

def create_websearch_agent(model_name: str = "anthropic:claude-3-7-sonnet-latest", temperature: float = 0.0) -> WebSearchAgent:
    """Factory function to create a web search agent."""
    return WebSearchAgent(model_name=model_name, temperature=temperature)
