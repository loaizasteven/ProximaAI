from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import Connection
from typing import Union
import os
import json
import asyncio
from pathlib import Path

mcp_tools_path = Path(__file__).parents[3] / "src" / "proximaai" / "mcp" / "ppl-ai-mcp.json"

async def get_mcp_tools_from_json(json_file: Union[str, os.PathLike]):
    """Async version of JSON file reading to avoid blocking operations."""
    def _read_json_file():
        with open(json_file, "r") as f:
            return json.load(f)
    
    # Use asyncio.to_thread to move the blocking operation to a separate thread
    return await asyncio.to_thread(_read_json_file)


async def get_mcp_tools(mcp_tools: Union[list[Union[str, os.PathLike]], dict[str, Connection]] = [mcp_tools_path]):
    mcp_config = {}
    if isinstance(mcp_tools, list):
        for file in mcp_tools:
            # Load the JSON file and extract the mcpServers configuration
            # file_config = await get_mcp_tools_from_json(file)
            # if "mcpServers" in file_config:
            mcp_config.update({"perplexity-ask": {
            "command": "npx",
        "args": [
            "-y",
            "server-perplexity-ask"
        ],
        "env": {
          "PERPLEXITY_API_KEY": f"{os.getenv('PERPLEXITY_API_KEY')}"
        },
        "transport": "stdio"
      }})
            # else:
                # If no mcpServers key, assume the file contains server configs directly
                # mcp_config.update(file_config)
    elif isinstance(mcp_tools, dict):
        mcp_config = mcp_tools
    else:
        raise ValueError("mcp_tools must be a list of files or dict")
    
    client = MultiServerMCPClient(
        mcp_config
    )
    tools = await client.get_tools()

    return tools
