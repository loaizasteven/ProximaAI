from pydantic import BaseModel
from typing import Any, Union, Optional

import httpx
import proximaai
from fastapi import status
from importlib.metadata import version


class MCPCommunication(BaseModel):
    mcp_server_url:str
    client: Optional[httpx.AsyncClient] = None
    timeout: Union[int, float] = 60.0
    headers: dict[str,str]= {
       "Accept": "application/json, text/event-stream",
       "content-type": "application/json",
       "Connection": "keep-alive"
        }
    mcp_server_token:Optional[str] = None 
    model_config= {"arbitrary_types_allowed": True}

    def model_post_init(self, context: Any, /) -> None:
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return super().model_post_init(context)
    
    async def initialize(self, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = None):
        if not data:
            data = {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {
                        "sampling": {}, 
                        "roots": {
                            "listChanged": "false"
                            }
                    },
                    "clientInfo": {
                        "name": f"{proximaai.__name__}", 
                        "version": f"{version(proximaai.__name__)}"
                        }
                },
                "id": "initialize-1"
            }
            if self.client:
                response = await self.client.post(
                    url=self.mcp_server_url, 
                    headers=self.headers, 
                    json=data, 
                    follow_redirects=True,
                    timeout=timeout
                    )
                
                if response.status_code == status.HTTP_200_OK:
                    self.mcp_server_token = response.headers.get("mcp-session-id")
                    self.headers['mcp-session-id'] = self.mcp_server_token or ""
                else:
                    response.raise_for_status()
            else:
                raise ConnectionError("MCP client not started")
