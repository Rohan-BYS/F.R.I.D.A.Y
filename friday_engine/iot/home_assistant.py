"""
F.R.I.D.A.Y. IoT & Smart Home Nerve Center.
Integrates with local Home Assistant REST API to control physical devices.
"""

import os
from typing import Any, Dict, List, Optional
from friday_engine.logger import logger

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


class HomeAssistantNerveCenter:
    """
    Connects F.R.I.D.A.Y. to the physical world via Home Assistant.
    """
    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        self.url = url or os.getenv("HASS_URL", "http://homeassistant.local:8123")
        self.token = token or os.getenv("HASS_TOKEN", "")
        self.enabled = HTTPX_AVAILABLE and bool(self.token)
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def check_connection(self) -> bool:
        if not self.enabled: return False
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{self.url}/api/", headers=self.headers, timeout=5.0)
                return res.status_code == 200
        except Exception:
            return False

    async def get_states(self) -> List[Dict[str, Any]]:
        """Fetch all device states from the smart home."""
        if not self.enabled: return []
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{self.url}/api/states", headers=self.headers, timeout=10.0)
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            logger.error(f"Home Assistant GET failed: {e}")
        return []

    async def call_service(self, domain: str, service: str, entity_id: str, **service_data) -> bool:
        """
        Command a physical device (e.g. domain="light", service="turn_on", entity_id="light.living_room")
        """
        if not self.enabled: return False
        
        payload = {"entity_id": entity_id}
        payload.update(service_data)
        
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"{self.url}/api/services/{domain}/{service}", 
                    headers=self.headers, 
                    json=payload,
                    timeout=10.0
                )
                logger.info(f"Home Assistant Command: {domain}.{service} on {entity_id} -> HTTP {res.status_code}")
                return res.status_code == 200
        except Exception as e:
            logger.error(f"Home Assistant POST failed: {e}")
            return False
