"""
Salesforce Addon for NewZyon/PAI-KAN Architecture
Temple 49 - Salesforce Guardian
Purpose: CRM
The Vikarma Team | Om Namah Shivaya 🔱
"""
from typing import Dict, Any, Optional, List
import httpx
import os


class SalesforceAddon:
    """
    Salesforce integration addon for MCP server
    Temple 49 of the 64 Bhairava Guardian Temples
    Guardian Purpose: CRM
    """

    API_BASE = "https://login.salesforce.com/services/data"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("SF_ACCESS_TOKEN")
        if not self.token and "SF_ACCESS_TOKEN" != "NO_AUTH_REQUIRED":
            raise ValueError(
                f"Missing SF_ACCESS_TOKEN. "
                f"Get your token from the Salesforce developer portal."
            )
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        if "SF_ACCESS_TOKEN" == "NO_AUTH_REQUIRED":
            return {"Content-Type": "application/json"}
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generic API request handler"""
        url = f"{self.API_BASE}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == "GET":
                r = await client.get(url, headers=self.headers, params=params or {})
            elif method == "POST":
                r = await client.post(url, headers=self.headers, json=data or {})
            elif method == "PUT":
                r = await client.put(url, headers=self.headers, json=data or {})
            elif method == "DELETE":
                r = await client.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return {"text": r.text, "status": r.status_code}

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return await self.request(endpoint, "GET", params=params)

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.request(endpoint, "POST", data=data)

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.request(endpoint, "PUT", data=data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        return await self.request(endpoint, "DELETE")
