from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import Connection
from typing import Union
import os
import json
import asyncio
from pathlib import Path

script_path = Path(__file__).parents[3] / "src" / "proximaai" / "mcp"

async def get_mcp_tools(
    mcp_tools: dict[str, dict] = {
        "perplexity-ask": {
            "command": "npx",
            "args": ["-y", "server-perplexity-ask"],
            "env": {
                "PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")
            },
            "transport": "stdio"
        }
    }
):
    if not isinstance(mcp_tools, dict):
        raise ValueError("mcp_tools must be a dict")
    client = MultiServerMCPClient(mcp_tools)
    return await client.get_tools()
