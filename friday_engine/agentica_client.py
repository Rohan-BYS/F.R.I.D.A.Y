"""
Top-level re-export for Agentica Client to satisfy friday_engine/agentica_client.py interface.
"""

from friday_engine.agentica.client import AgenticaClient, AgenticaError

__all__ = ["AgenticaClient", "AgenticaError"]
