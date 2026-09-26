"""
F.R.I.D.A.Y. Hive Mind Network Gateway.
Allows the main engine to execute commands and transfer files across remote nodes.
"""

import httpx
from typing import Dict, Any, List
from friday_engine.logger import logger

class HiveMindGateway:
    def __init__(self, nexus: Any):
        self.nexus = nexus
        self.client = httpx.AsyncClient(timeout=60.0)

    async def list_active_nodes(self) -> Dict[str, Any]:
        """List all computers currently connected to the F.R.I.D.A.Y. Hive Mind."""
        if not hasattr(self.nexus, 'active_nodes'):
            return {"error": "Webhook Nexus is not managing active nodes."}
        return {"nodes": self.nexus.active_nodes}

    def _get_node_url(self, node_name: str) -> str:
        nodes = getattr(self.nexus, 'active_nodes', {})
        if node_name not in nodes:
            raise ValueError(f"Node '{node_name}' is not registered.")
        node_info = nodes[node_name]
        return f"http://{node_info['ip']}:{node_info['port']}"

    async def execute_on_node(self, node_name: str, command: str) -> Dict[str, Any]:
        """Run a terminal command on a remote computer and get the result."""
        try:
            url = f"{self._get_node_url(node_name)}/execute"
            response = await self.client.post(url, json={"command": command})
            return response.json()
        except Exception as e:
            logger.error(f"Failed to execute on node {node_name}: {e}")
            return {"error": str(e)}

    async def read_file_from_node(self, node_name: str, remote_filepath: str) -> str:
        """Read the text contents of a file on a remote computer."""
        try:
            url = f"{self._get_node_url(node_name)}/fs/read"
            response = await self.client.get(url, params={"filepath": remote_filepath})
            if response.status_code == 200:
                return response.json().get("content", "")
            return f"Error: HTTP {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {e}"

    async def write_file_to_node(self, node_name: str, remote_filepath: str, content: str) -> str:
        """Create or overwrite a file on a remote computer."""
        try:
            url = f"{self._get_node_url(node_name)}/fs/write"
            response = await self.client.post(url, json={"filepath": remote_filepath, "content": content})
            if response.status_code == 200:
                return "File written successfully."
            return f"Error: HTTP {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {e}"
