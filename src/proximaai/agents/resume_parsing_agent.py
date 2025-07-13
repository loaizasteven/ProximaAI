from pydantic import BaseModel, model_validator
from typing import Optional, Any
import json
import io
import os

from proximaai.mcp.mcp_client import MCPCommunication
from fastapi import status
from urllib.parse import urljoin
import httpx

class ResumeParsingAgent(BaseModel):
    tool_name: str = "parse_document"
    client: Optional[MCPCommunication] = None
    model_config= {"arbitrary_types_allowed": True}

    def model_post_init(self, context: Any, /) -> None:
        server_base_url = os.getenv("LANGGRAPH_MCP_BASE_URL", "")
        self.client = MCPCommunication(
            mcp_server_url=urljoin(server_base_url, self.tool_name + "/mcp")
        )
        return super().model_post_init(context)

    @model_validator(mode='before')
    @classmethod
    def api_key_validations(cls, values):
        if not os.getenv("LLAMA_CLOUD_API_KEY"):
         raise ValueError("LLAMA_CLOUD_API_KEY not set as environment variable in graph")

        return values
        
    async def mcp_server_health(self, subpath:str="/parse_document/health") -> httpx.Response:
        server_base_url = os.getenv("LANGGRAPH_MCP_BASE_URL", "")
        if not server_base_url:
            error_content = json.dumps({"detail": "LANGGRAPH_MCP_BASE_URL env not found"}).encode("utf-8")
            return httpx.Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_content,
                headers={"content-type": "application/json"}
            )
        try:
            async with httpx.AsyncClient() as client:
                result = await client.get(urljoin(base=server_base_url, url=subpath))
            return result
        except BaseException as e:
            error_content = json.dumps({"detail": "Server not running"}).encode("utf-8")
            return httpx.Response(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=error_content,
                headers={"content-type": "application/json"}
            )
            
    async def invoke(
        self,
        file: Optional[io.BytesIO],
        file_name: Optional[str],
    ) -> Any:
        # Make a call to MCP Server Health
        health_check = await self.mcp_server_health()
        assert health_check.status_code == 200, health_check.raise_for_status
        parameters = {
                    "name": "parse_document",
                    "arguments":{
                        "request": {
                            "file_data": file,
                            "file_name": file_name or "resume.pdf"
                        }
                    }
                }
        if self.client:
            result = await self.client.invoke(params=parameters, timeout=60.0)
        else:
            raise ConnectionError("MCP client is not open")

        return result
