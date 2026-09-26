"""
F.R.I.D.A.Y. Omniscient Retrieval Interface.
Bypasses standard search engine blockages by querying independent search and archival datasets.
"""

import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List, Dict, Any, Optional
from friday_engine.logger import logger

class OmniscientSearch:
    """
    Provides F.R.I.D.A.Y. with unfiltered access to the live web and historical archives.
    """
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_surface_web(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search the live web using DuckDuckGo (bypasses Google-specific tracking and blocks).
        """
        logger.info(f"[OmniscientSearch] Searching live web for: '{query}'")
        try:
            results = DDGS().text(query, max_results=max_results)
            return results if results else []
        except Exception as e:
            logger.error(f"[OmniscientSearch] Live search failed: {e}")
            return [{"error": str(e)}]

    async def get_historical_snapshots(self, url: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Query the Internet Archive (Wayback Machine) CDX API to find all historical snapshots of a deleted or modified URL.
        Use this to prove something existed on a website in the past.
        """
        logger.info(f"[OmniscientSearch] Querying historical snapshots for: {url}")
        api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&limit={limit}&fl=timestamp,original,statuscode,mimetype&collapse=timestamp:6"
        
        try:
            response = await self.client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if not data or len(data) < 2:
                    return [{"message": "No historical snapshots found."}]
                
                headers = data[0]
                snapshots = []
                for row in data[1:]:
                    snapshots.append({
                        "timestamp": row[0],
                        "url": row[1],
                        "status": row[2],
                        "mimetype": row[3],
                        "archive_link": f"http://web.archive.org/web/{row[0]}/{row[1]}"
                    })
                return snapshots
            else:
                return [{"error": f"HTTP {response.status_code}"}]
        except Exception as e:
            logger.error(f"[OmniscientSearch] Snapshot query failed: {e}")
            return [{"error": str(e)}]

    async def read_historical_page(self, url: str, timestamp: str) -> str:
        """
        Download and extract text from a specific historical snapshot of a webpage.
        Provide the original URL and the exact timestamp (e.g., '20220101123000') from get_historical_snapshots.
        """
        # The 'id_' modifier gets the raw HTML without the Wayback Machine injection toolbar
        archive_url = f"http://web.archive.org/web/{timestamp}id_/{url}"
        logger.info(f"[OmniscientSearch] Reading historical page: {archive_url}")
        
        try:
            response = await self.client.get(archive_url, follow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "header", "footer"]):
                    script.extract()
                
                text = soup.get_text(separator='\n', strip=True)
                
                # Compress excessive newlines
                import re
                text = re.sub(r'\n+', '\n', text)
                
                return text[:20000] # Return up to 20k characters to avoid context overflow
            else:
                return f"Error: Wayback Machine returned HTTP {response.status_code}"
        except Exception as e:
            logger.error(f"[OmniscientSearch] Read historical page failed: {e}")
            return f"Error reading page: {str(e)}"
