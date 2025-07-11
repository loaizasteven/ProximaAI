from pathlib import Path
import base64
import os
import io

from typing import Any, Union
from fastapi.responses import JSONResponse, Response
from fastapi import Request
from fastapi import status

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

@llama_parse_mcp.custom_route(
    path="/health",
    methods=["GET"],
    name="health-check",
    include_in_schema=True
)
async def health(request: Request)->Response:
    return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)

# --- Tool Registration using @mcp.tool Decorator ---
@llama_parse_mcp.tool(
    name="parse_document",
    description="Parse a document using LlamaParse."
)
async def parse_document(
    ctx: Context, 
    request: Union[os.PathLike, str, io.BytesIO, dict],
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
        if isinstance(request, (str, os.PathLike)):
            file_path = Path(request)  # Convert string paths to Path objects
            _type = file_path.suffix
            assert _type == ".pdf", f"FileTypeError: extension {_type} is not supported"
            file_like = await file_to_bytesio(file_path)
            file_name = str(file_path)  # Ensure file_name is a string
        elif isinstance(request, dict):
            # # Read json content
            # body = await request.json()
            file_data = request.get("file_data")
            if file_data is None:
                raise ValueError("Missing 'file_data' in request")
            # Extract information
            file_bytes = base64.b64decode(file_data)
            file_like = io.BytesIO(file_bytes)
            file_name = request.get("file_name", "uploaded_file.pdf")
        elif isinstance(request, io.BytesIO):
            file_like = request
            file_name = "default_resume.pdf"
        result = await llama_parse.aparse(file_like, extra_info={"file_name": file_name})
            
        if isinstance(result, JobResult):
            markdown = await result.aget_markdown_documents()
            text = [doc.text for doc in markdown]
            return text
        else:
            raise ValueError(f"Unexpected result type: {type(result)}")

    except Exception as e:
        await ctx.error(f"Error parsing document: {str(e)}")
        return f"An error occurred while processing the document. Please try again later."

# --- HTTP Streamable Server Startup ---
if __name__ == "__main__":
    # Start the MCP server with streamable HTTP transport
    llama_parse_mcp.run(transport="streamable-http")
