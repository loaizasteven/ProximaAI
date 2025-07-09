import os
import io

from typing import Any, Union, List
from mcp.server.fastmcp import FastMCP, Context
from llama_cloud_services import LlamaParse
from llama_cloud_services.parse.types import JobResult
import aiofiles

# --- MCP Server Setup ---
llama_parse_mcp = FastMCP("llama-parse-server")

async def file_to_bytesio(file_path):
    """Read a file into a BytesIO object asynchronously."""
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
    return io.BytesIO(content)

# --- Tool Registration using @mcp.tool Decorator ---
@llama_parse_mcp.tool(
    name="parse_document",
    description="Parse a document using LlamaParse."
)
async def parse_document(
    ctx: Context, 
    file_path: str,
    project_id: Union[str, None] = os.getenv("LLAMA_CLOUD_PROJECT_ID"),
    org_id: Union[str, None] = os.getenv("LLAMA_CLOUD_ORG_ID")
    ) -> Any:
    """
    Parse a document using a configured LlamaParse agent.
    """
    ctx = llama_parse_mcp.get_context()
    try:
        # Instantiate the LlamaParse agent
        llama_parse = LlamaParse(organization_id=org_id, project_id=project_id)

        # Non-blocking file read
        file_like = await file_to_bytesio(file_path)
        result = await llama_parse.aparse(file_like, extra_info={"file_name": file_path.split("/")[-1]})

        if isinstance(result, JobResult):
            markdown = await result.aget_markdown_documents()
            text = [doc.text for doc in markdown]
            return text
        else:
            raise ValueError(f"Unexpected result type: {type(result)}")
        return 

    except Exception as e:
        await ctx.error(f"Error parsing document: {str(e)}")
        return f"Error parsing document: {str(e)}"

# --- HTTP Streamable Server Startup ---
if __name__ == "__main__":
    # Start the MCP server with streamable HTTP transport
    llama_parse_mcp.run(transport="streamable-http")
