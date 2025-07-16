import os
import httpx
from langchain.tools import BaseTool
import json
from typing import Optional

class PerplexityWebSearchTool(BaseTool):
    """Tool for performing web searches using the Perplexity API."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="perplexity_web_search",
            description="""
            Uses the Perplexity API to perform a web search and return a conversational answer.
            Input should be a search query string.
            """
        )
        self._api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")

    def _run(self, query: str) -> str:
        if not self._api_key:
            return "Error: PERPLEXITY_API_KEY is not set."
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        body = {
            "model": "sonar-pro",
            "messages": [
                {"role": "user", "content": query}
            ],
        }
        try:
            with httpx.Client() as client:
                response = client.post(url, headers=headers, json=body, timeout=30)
                response.raise_for_status()
                data = response.json()
            message_content = data["choices"][0]["message"]["content"]
            if "citations" in data and isinstance(data["citations"], list) and data["citations"]:
                message_content += "\n\nCitations:\n"
                for idx, citation in enumerate(data["citations"], 1):
                    message_content += f"[{idx}] {citation}\n"
            return message_content
        except Exception as e:
            return f"Error calling Perplexity API: {str(e)}"
