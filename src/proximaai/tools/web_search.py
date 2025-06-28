"""
Web Search Tool - Performs internet searches for job-related information.
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
import requests
import json
from urllib.parse import quote_plus
import time


class WebSearchTool(BaseTool):
    """Tool for performing web searches."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="web_search",
            description="""
            Performs web searches to find current information about companies, job markets, 
            industry trends, and career-related topics.
            
            Input should be a search query string.
            Returns relevant search results with URLs and snippets.
            """
        )
        # Store api_key in a way that doesn't conflict with Pydantic
        self._api_key = api_key
        # For now, we'll use a simple approach. In production, you'd want to use
        # a proper search API like Google Custom Search, SerpAPI, or similar
    
    @property
    def api_key(self) -> Optional[str]:
        """Get the API key."""
        return self._api_key
    
    def _run(self, query: str) -> str:
        """Perform a web search."""
        try:
            # This is a placeholder implementation
            # In production, you'd integrate with a real search API
            search_results = self._perform_search(query)
            return json.dumps(search_results, indent=2)
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform the actual search (placeholder implementation)."""
        # This is a mock implementation
        # In production, replace with actual search API calls
        
        # Simulate search results
        mock_results = [
            {
                "title": f"Search results for: {query}",
                "url": f"https://example.com/search?q={quote_plus(query)}",
                "snippet": f"Relevant information about {query} from various sources.",
                "source": "web_search"
            },
            {
                "title": f"Latest news about {query}",
                "url": f"https://news.example.com/search?q={quote_plus(query)}",
                "snippet": f"Recent developments and news related to {query}.",
                "source": "news_search"
            }
        ]
        
        return mock_results


class CompanyResearchTool(BaseTool):
    """Tool for researching specific companies."""
    
    def __init__(self):
        super().__init__(
            name="company_research",
            description="""
            Researches specific companies to find information about their culture, 
            recent news, financial performance, and job opportunities.
            
            Input should be a company name.
            Returns comprehensive company information.
            """
        )
    
    def _run(self, company_name: str) -> str:
        """Research a specific company."""
        try:
            # Perform multiple searches for comprehensive company info
            searches = [
                f"{company_name} company culture",
                f"{company_name} recent news",
                f"{company_name} job opportunities",
                f"{company_name} financial performance"
            ]
            
            results = {}
            for search in searches:
                results[search] = self._perform_search(search)
            
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error researching company: {str(e)}"
    
    def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform search (placeholder implementation)."""
        # Mock implementation - replace with actual search API
        return [
            {
                "title": f"Results for: {query}",
                "url": f"https://example.com/search?q={quote_plus(query)}",
                "snippet": f"Information about {query}",
                "source": "company_research"
            }
        ]
