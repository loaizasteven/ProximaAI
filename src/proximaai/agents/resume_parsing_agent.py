from httpx import request
from pydantic import BaseModel, model_validator
from typing import Union, Optional
from urllib.parse import urljoin
import json
import io
import os

from fastapi import status
import httpx

from proximaai.mcp import server


class ResumeParsingAgent(BaseModel):
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
        project_id: Union[str, None] = os.getenv("LLAMA_CLOUD_PROJECT_ID"),
        org_id: Union[str, None] = os.getenv("LLAMA_CLOUD_ORG_ID")
    ):
        # Make a call to MCP Server Health
        health_check = await self.mcp_server_health()
        assert health_check.status_code == 200

        return health_check.text
