"""
F.R.I.D.A.Y. Webhook Nexus Server.
A lightweight FastAPI server to receive external triggers (GitHub, Zapier, Emails, IoT).
"""

from typing import Any, Dict
from friday_engine.logger import logger

try:
    from fastapi import FastAPI, Request, BackgroundTasks
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


class WebhookNexus:
    """
    The Listener. Opens F.R.I.D.A.Y. to incoming internet events.
    """
    def __init__(self, engine: Any, host: str = "0.0.0.0", port: int = 8080):
        self.engine = engine
        self.host = host
        self.port = port
        self.app = FastAPI(title="F.R.I.D.A.Y. Webhook Nexus") if FASTAPI_AVAILABLE else None
        self.active_nodes: Dict[str, Dict[str, Any]] = {}
        
        if self.app:
            self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/hive/register")
        async def register_node(request: Request):
            """Endpoint for remote worker nodes to announce themselves."""
            payload = await request.json()
            node_name = payload.get("node_name")
            if not node_name:
                return {"error": "Missing node_name"}
            
            self.active_nodes[node_name] = {
                "ip": request.client.host,
                "port": payload.get("port", 8081),
                "capabilities": payload.get("capabilities", []),
                "last_seen": __import__('time').time()
            }
            logger.info(f"[Hive Mind] Node '{node_name}' registered successfully.")
            return {"status": "registered", "nexus_time": __import__('time').time()}

        @self.app.get("/hive/nodes")
        def list_nodes():
            """List all active nodes in the Hive Mind."""
            return {"nodes": self.active_nodes}
        @self.app.post("/webhook/github")
        async def github_webhook(request: Request, bg_tasks: BackgroundTasks):
            payload = await request.json()
            event = request.headers.get("X-GitHub-Event", "unknown")
            logger.info(f"Received GitHub Webhook: {event}")
            
            # Pass to Engine asynchronously
            bg_tasks.add_task(self.engine.chat, f"[GitHub Webhook Event: {event}] Payload: {payload}")
            return {"status": "accepted"}

        @self.app.post("/webhook/zapier")
        async def zapier_webhook(request: Request, bg_tasks: BackgroundTasks):
            payload = await request.json()
            logger.info("Received Zapier Webhook")
            bg_tasks.add_task(self.engine.chat, f"[Zapier Webhook] Payload: {payload}")
            return {"status": "accepted"}
            
        @self.app.get("/health")
        def health_check():
            return {"status": "Nexus Online", "version": "1.0"}

    async def start(self):
        if not FASTAPI_AVAILABLE:
            logger.error("FastAPI or uvicorn not installed. Webhook Nexus disabled.")
            return
            
        logger.info(f"Starting Webhook Nexus Server on {self.host}:{self.port}...")
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="warning")
        server = uvicorn.Server(config)
        await server.serve()
