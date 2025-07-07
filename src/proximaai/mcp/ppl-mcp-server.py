import os
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Literal

PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    raise RuntimeError("PERPLEXITY_API_KEY environment variable is required")

# Create an MCP server
mcp = FastMCP("Perplexity")

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class PerplexityAskInput(BaseModel):
    messages: List[Message]

@mcp.tool()
async def perplexity_ask(messages: List[Message]) -> str:
    """Engages in a conversation using the Perplexity Sonar API. Accepts an array of messages (each with a role and content) and returns a completion response from the Perplexity model."""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    }
    body = {
        "model": "sonar-pro",
        "messages": [m.model_dump() for m in messages],
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        if response.status_code != 200:
            raise RuntimeError(f"Perplexity API error: {response.text}")
        data = response.json()
    message_content = data["choices"][0]["message"]["content"]
    if "citations" in data and isinstance(data["citations"], list) and data["citations"]:
        message_content += "\n\nCitations:\n"
        for idx, citation in enumerate(data["citations"], 1):
            message_content += f"[{idx}] {citation}\n"
    return message_content 
    