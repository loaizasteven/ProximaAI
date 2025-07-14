from langchain_mcp_adapters.sessions import StreamableHttpConnection
from datetime import timedelta
import os

from urllib.parse import urljoin

server_base_url = os.getenv("LANGGRAPH_MCP_BASE_URL", "")

# MCP Server Defintions
mcp_servers = dict(
    llamaParseServer=StreamableHttpConnection(
        transport="streamable_http",
        url=urljoin(server_base_url, "/parse_document/mcp"),
        headers={
            "Content-Type":"application/json"
        },
        timeout=timedelta(seconds=30),
        sse_read_timeout=timedelta(seconds=30),
        terminate_on_close=False,
        session_kwargs=None,
        httpx_client_factory=None
    )
)