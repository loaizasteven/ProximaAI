from optparse import Option
from pydantic import BaseModel
from typing import Any, Union, Optional, List
import json

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
            response = await self._method_wrapper(data=data, timeout=timeout)
            
            if response:   
                self.mcp_server_token = response.headers.get("mcp-session-id")
                self.headers['mcp-session-id'] = self.mcp_server_token or ""

    async def _method_wrapper(self, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = None):
        if self.client:
                response = await self.client.post(
                    url=self.mcp_server_url, 
                    headers=self.headers, 
                    json=data, 
                    follow_redirects=True,
                    timeout=timeout
                    )
                
                if response.status_code == status.HTTP_200_OK:
                    return response
                else:
                    response.raise_for_status()
        else:
            raise ConnectionError("MCP client not started")

    async def notification_initialization(self, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = None) -> dict:
            if not data:
                data = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
                }
            
            _ = await self._method_wrapper(data=data, timeout=timeout)
            
            return {"status": "ok"}
    
    @staticmethod
    def parse_sse_json(response_text: str) -> dict[Any, Any]:
        """
        Extracts and parses all JSON objects from 'data:' lines in an SSE-formatted response.

        Args:
            response_text (str): The raw text from the HTTP response.

        Returns:
            List[Any]: A list of parsed JSON objects.
        """
        results = []
        for line in response_text.splitlines():
            if line.startswith('data:'):
                json_str = line[len('data:'):].strip()
                try:
                    results.append(json.loads(json_str))
                except json.JSONDecodeError:
                    # Optionally, log or print the error and continue
                    pass
        return results[0]

    async def tool_list(self, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = None) -> list:
            if not data:
                data = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
            
            response = await self._method_wrapper(data=data, timeout=timeout)
            if response:
                formatted_response = self.parse_sse_json(response.text)
                tools = await self.tool_list_parse(value=formatted_response)
                return tools
            else:
                return []

    async def tool_list_parse(self, value:dict)-> list:
        #TODO Add class method for tools - structure output
        return value["result"]["tools"]

    async def tool_call(self, params: Optional[dict] = None, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = 60.0) -> Any:
        if not data:
            data = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": params 
            }
        
        response = await self._method_wrapper(data=data, timeout=timeout)
        if response:
            formatted_response = self.parse_sse_json(response.text)
            return formatted_response['result']
        else:
            return []

    async def invoke(self, params: Optional[dict] = None, data: Optional[dict[str, Any]] = None, timeout: Optional[Union[int, float]] = 60.0) -> Any:
        """Invoke the MCP protocol lifecycle to run desired tool"""
        await self.initialize()
        _ = await self.notification_initialization()
        result = await self.tool_call(params=params, data=data, timeout=timeout)

        return result
 