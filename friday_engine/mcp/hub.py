"""
F.R.I.D.A.Y. Model Context Protocol (MCP) Hub.
Allows F.R.I.D.A.Y. to act as an MCP Client and connect to external MCP Servers 
(e.g., Anthropic Claude, Google Antigravity, local specialized servers).
"""

import asyncio
import json
import subprocess
from typing import Any, Dict, List, Optional
from friday_engine.logger import logger
from friday_engine.tool_forge.registry import ToolRegistry


class StdioMCPServer:
    """Manages a single stdio-based MCP Server connection."""
    
    def __init__(self, name: str, command: str, args: List[str]):
        self.name = name
        self.command = command
        self.args = args
        self.process: Optional[asyncio.subprocess.Process] = None
        self._request_id = 0
        self._pending_requests: Dict[int, asyncio.Future] = {}
        self.tools: List[Dict[str, Any]] = []

    async def connect(self):
        """Spawns the MCP server process and starts the listener loop."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                self.command,
                *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"MCP Server '{self.name}' connected successfully via stdio.")
            asyncio.create_task(self._listen())
            
            # Request tools from the server
            await self._refresh_tools()
        except Exception as e:
            logger.error(f"Failed to connect to MCP Server '{self.name}': {e}")

    async def _listen(self):
        """Listen to stdout for JSON-RPC messages from the server."""
        if not self.process or not self.process.stdout:
            return

        while True:
            line = await self.process.stdout.readline()
            if not line:
                logger.warning(f"MCP Server '{self.name}' disconnected.")
                break
                
            try:
                data = json.loads(line.decode('utf-8').strip())
                self._handle_message(data)
            except json.JSONDecodeError:
                # Might be normal stdout logging from the server
                continue
            except Exception as e:
                logger.error(f"Error handling MCP message from '{self.name}': {e}")
                
        # Reject all pending requests if the server disconnects
        for req_id, future in self._pending_requests.items():
            if not future.done():
                future.set_exception(RuntimeError(f"MCP Server '{self.name}' disconnected unexpectedly."))
        self._pending_requests.clear()

    def _handle_message(self, data: Dict[str, Any]):
        """Route incoming JSON-RPC responses to the appropriate future."""
        if "id" in data and data["id"] in self._pending_requests:
            future = self._pending_requests.pop(data["id"])
            if "error" in data:
                future.set_exception(Exception(data["error"]))
            else:
                future.set_result(data.get("result"))

    async def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a JSON-RPC request to the MCP server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError(f"MCP Server '{self.name}' is not running.")
            
        self._request_id += 1
        req_id = self._request_id
        
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {}
        }
        
        future = asyncio.get_running_loop().create_future()
        self._pending_requests[req_id] = future
        
        message = json.dumps(payload) + "\n"
        self.process.stdin.write(message.encode('utf-8'))
        await self.process.stdin.drain()
        
        return await future

    async def _refresh_tools(self):
        """Fetch available tools from the server."""
        try:
            # Wrap the tool request in a timeout so bad servers don't hang the boot
            result = await asyncio.wait_for(self._send_request("tools/list"), timeout=10.0)
            self.tools = result.get("tools", [])
            logger.info(f"MCP Server '{self.name}' exposed {len(self.tools)} tools.")
        except asyncio.TimeoutError:
            logger.warning(f"MCP Server '{self.name}' timed out while listing tools.")
        except Exception as e:
            logger.error(f"Failed to list tools for '{self.name}': {e}")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool on the MCP server."""
        logger.info(f"Calling MCP tool '{tool_name}' on server '{self.name}'")
        result = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if result.get("isError"):
            raise RuntimeError(f"MCP Tool Error: {result.get('content')}")
            
        return result.get("content", [])

    async def shutdown(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()


class MCPHub:
    """
    Central hub managing multiple MCP server connections and registering
    their tools into F.R.I.D.A.Y.'s local ToolRegistry.
    """
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.servers: Dict[str, StdioMCPServer] = {}

    def load_config(self, config_path: str):
        """Load MCP servers from a JSON config (e.g. claude_desktop_config.json structure)."""
        import os
        if not os.path.exists(config_path):
            return
            
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            servers_config = data.get("mcpServers", {})
            for name, cfg in servers_config.items():
                self.add_server(name, cfg.get("command"), cfg.get("args", []))
        except Exception as e:
            logger.error(f"Failed to load MCP config from {config_path}: {e}")

    def add_server(self, name: str, command: str, args: List[str]):
        """Register a new MCP server configuration."""
        self.servers[name] = StdioMCPServer(name, command, args)

    async def connect_all(self):
        """Connect to all registered MCP servers and inject their tools (in parallel)."""
        async def _connect_and_inject(server: StdioMCPServer):
            await server.connect()
            self._inject_server_tools(server)

        tasks = [_connect_and_inject(server) for server in self.servers.values()]
        if tasks:
            await asyncio.gather(*tasks)

    def _inject_server_tools(self, server: StdioMCPServer):
        """Wrap MCP server tools and register them into Friday's ToolRegistry."""
        for tool_def in server.tools:
            tool_name = f"mcp_{server.name}_{tool_def['name']}"
            
            # Create a dynamic async wrapper for the tool
            async def mcp_tool_wrapper(**kwargs):
                return await server.call_tool(tool_def['name'], kwargs)
                
            # Assign the docstring for the LLM
            mcp_tool_wrapper.__doc__ = tool_def.get("description", f"MCP Tool: {tool_name}")
            
            # Register it globally so Friday can use it!
            self.registry.register(tool_name, mcp_tool_wrapper)
            logger.info(f"Injected MCP tool into F.R.I.D.A.Y.: {tool_name}")

    async def shutdown(self):
        for server in self.servers.values():
            await server.shutdown()
