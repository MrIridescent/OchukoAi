"""
Model Context Protocol (MCP) Server Integration
Enables Ochuko AI to expose capabilities via MCP
Implements JSON-RPC 2.0 protocol for tool/resource access
Author: David Akpoviroro Oke (MrIridescent)
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import sys
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)


class MCPMessageType(Enum):
    """MCP message types (JSON-RPC 2.0)"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MCPResource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mimeType: str = "application/json"
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MCPRequest:
    """MCP JSON-RPC Request"""
    jsonrpc: str = "2.0"
    method: str = None
    params: Dict[str, Any] = None
    id: Any = None
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class MCPResponse:
    """MCP JSON-RPC Response"""
    jsonrpc: str = "2.0"
    result: Any = None
    error: Optional[Dict] = None
    id: Any = None
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class MCPServer:
    """
    Model Context Protocol Server Implementation
    Exposes Ochuko AI capabilities to MCP clients (Claude, etc.)
    """
    
    def __init__(self, server_name: str = "UniversalAI", version: str = "4.0.0"):
        self.server_name = server_name
        self.version = version
        self.tools: Dict[str, Callable] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.prompts: Dict[str, Dict] = {}
        self.request_handlers: Dict[str, Callable] = {}
        self._setup_rpc_handlers()
        
    def _setup_rpc_handlers(self):
        """Setup JSON-RPC 2.0 method handlers"""
        self.request_handlers = {
            "initialize": self.handle_initialize,
            "tools/list": self.handle_tools_list,
            "tools/call": self.handle_tools_call,
            "resources/list": self.handle_resources_list,
            "resources/read": self.handle_resources_read,
            "prompts/list": self.handle_prompts_list,
            "prompts/get": self.handle_prompts_get,
            "completion/complete": self.handle_completion,
        }
    
    def register_tool(self, name: str, func: Callable, description: str, 
                     input_schema: Dict[str, Any]):
        """Register a tool/function that MCP clients can call"""
        self.tools[name] = {
            "function": func,
            "description": description,
            "inputSchema": input_schema
        }
        logger.info(f"Registered MCP tool: {name}")
    
    def register_resource(self, uri: str, resource: MCPResource):
        """Register a resource that MCP clients can access"""
        self.resources[uri] = resource
        logger.info(f"Registered MCP resource: {uri}")
    
    def register_prompt(self, name: str, description: str, arguments: List[Dict]):
        """Register a prompt template"""
        self.prompts[name] = {
            "description": description,
            "arguments": arguments
        }
        logger.info(f"Registered MCP prompt: {name}")
    
    async def handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": self.server_name,
                "version": self.version
            }
        }
    
    async def handle_tools_list(self, params: Dict) -> Dict:
        """List available tools"""
        tools_list = []
        for name, tool_info in self.tools.items():
            tools_list.append({
                "name": name,
                "description": tool_info["description"],
                "inputSchema": tool_info["inputSchema"]
            })
        return {"tools": tools_list}
    
    async def handle_tools_call(self, params: Dict) -> Dict:
        """Execute a tool"""
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "code": "TOOL_NOT_FOUND"
            }
        
        try:
            tool_func = self.tools[tool_name]["function"]
            result = await tool_func(**tool_args) if asyncio.iscoroutinefunction(tool_func) else tool_func(**tool_args)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result) if not isinstance(result, str) else result
                    }
                ]
            }
        except Exception as e:
            return {
                "error": str(e),
                "code": "TOOL_EXECUTION_ERROR"
            }
    
    async def handle_resources_list(self, params: Dict) -> Dict:
        """List available resources"""
        resources_list = []
        for uri, resource in self.resources.items():
            resources_list.append(resource.to_dict())
        return {"resources": resources_list}
    
    async def handle_resources_read(self, params: Dict) -> Dict:
        """Read a resource"""
        uri = params.get("uri")
        if uri not in self.resources:
            return {"error": f"Resource '{uri}' not found"}
        resource = self.resources[uri]
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": resource.mimeType,
                    "text": json.dumps({"name": resource.name, "description": resource.description})
                }
            ]
        }
    
    async def handle_prompts_list(self, params: Dict) -> Dict:
        """List available prompts"""
        prompts_list = []
        for name, prompt_info in self.prompts.items():
            prompts_list.append({
                "name": name,
                "description": prompt_info["description"],
                "arguments": prompt_info["arguments"]
            })
        return {"prompts": prompts_list}
    
    async def handle_prompts_get(self, params: Dict) -> Dict:
        """Get a prompt template"""
        name = params.get("name")
        if name not in self.prompts:
            return {"error": f"Prompt '{name}' not found"}
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Using prompt: {name}\nArguments: {json.dumps(params.get('arguments', {}))}"
                }
            ]
        }
    
    async def handle_completion(self, params: Dict) -> Dict:
        """Handle completion request"""
        partial = params.get("partial", "")
        return {
            "completion": partial,
            "partial": True
        }
    
    async def process_message(self, message: str) -> str:
        """Process incoming JSON-RPC message"""
        try:
            data = json.loads(message)
            method = data.get("method")
            params = data.get("params", {})
            msg_id = data.get("id")
            
            if method not in self.request_handlers:
                response = MCPResponse(
                    error={"code": -32601, "message": f"Method not found: {method}"},
                    id=msg_id
                )
                return json.dumps(response.to_dict())
            
            handler = self.request_handlers[method]
            result = await handler(params) if asyncio.iscoroutinefunction(handler) else handler(params)
            
            response = MCPResponse(result=result, id=msg_id)
            return json.dumps(response.to_dict())
            
        except json.JSONDecodeError as e:
            response = MCPResponse(
                error={"code": -32700, "message": f"Parse error: {str(e)}"}
            )
            return json.dumps(response.to_dict())
        except Exception as e:
            response = MCPResponse(
                error={"code": -32603, "message": f"Internal error: {str(e)}"}
            )
            return json.dumps(response.to_dict())
    
    async def run_stdio_server(self):
        """Run MCP server over stdin/stdout (for local integration)"""
        logger.info(f"Starting MCP Server ({self.server_name}) on stdio")
        
        loop = asyncio.get_event_loop()
        
        async def read_input():
            """Read JSON-RPC messages from stdin"""
            while True:
                try:
                    line = await loop.run_in_executor(None, sys.stdin.readline)
                    if not line:
                        break
                    line = line.strip()
                    if line:
                        response = await self.process_message(line)
                        print(response, flush=True)
                except Exception as e:
                    logger.error(f"Error reading input: {e}")
                    break
        
        await read_input()
    
    async def run_http_server(self, host: str = "0.0.0.0", port: int = 8001):
        """Run MCP server over HTTP (for remote integration)"""
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
        import uvicorn
        
        app = FastAPI(title=self.server_name)
        
        @app.post("/mcp")
        async def mcp_handler(request: Request):
            """Handle MCP JSON-RPC requests"""
            body = await request.json()
            message = json.dumps(body)
            response_str = await self.process_message(message)
            return JSONResponse(json.loads(response_str))
        
        logger.info(f"Starting MCP HTTP Server on {host}:{port}")
        await uvicorn.run(app, host=host, port=port)


class MCPClientAdapter:
    """
    Adapter to connect to external MCP servers
    Used by Ochuko AI to consume external MCP resources
    """
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.tools_cache: Dict[str, Dict] = {}
        self.resources_cache: Dict[str, Dict] = {}
        
    async def initialize(self) -> Dict:
        """Initialize connection to MCP server"""
        request = MCPRequest(method="initialize", params={}, id=str(uuid4()))
        return await self._send_request(request)
    
    async def list_tools(self) -> List[Dict]:
        """List available tools from MCP server"""
        request = MCPRequest(method="tools/list", params={}, id=str(uuid4()))
        response = await self._send_request(request)
        self.tools_cache = {t["name"]: t for t in response.get("tools", [])}
        return response.get("tools", [])
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Call a tool on the MCP server"""
        request = MCPRequest(
            method="tools/call",
            params={"name": tool_name, "arguments": arguments},
            id=str(uuid4())
        )
        return await self._send_request(request)
    
    async def list_resources(self) -> List[Dict]:
        """List available resources from MCP server"""
        request = MCPRequest(method="resources/list", params={}, id=str(uuid4()))
        response = await self._send_request(request)
        self.resources_cache = {r["uri"]: r for r in response.get("resources", [])}
        return response.get("resources", [])
    
    async def read_resource(self, uri: str) -> Dict:
        """Read a resource from the MCP server"""
        request = MCPRequest(
            method="resources/read",
            params={"uri": uri},
            id=str(uuid4())
        )
        return await self._send_request(request)
    
    async def _send_request(self, request: MCPRequest) -> Dict:
        """Send JSON-RPC request to MCP server"""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.server_url}/mcp",
                    json=request.to_dict(),
                    timeout=30
                ) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"MCP request failed: {e}")
            return {"error": str(e)}
