"""
Notion Addon for NewZyon/PAI-KAN Architecture
Temple 5 - Notion Guardian
Purpose: Knowledge Base & Notes — Sacred Mind Palace

The Vikarma Team | Om Namah Shivaya 🔱
"""
from typing import Dict, Any, Optional, List
import httpx
import os


class NotionAddon:
    """
    Notion integration addon for MCP server
    Temple 5 of the 64 Bhairava Guardian Temples
    Guardian Purpose: Knowledge Base, Notes, Databases
    """

    API_BASE = "https://api.notion.com/v1"
    NOTION_VERSION = "2022-06-28"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError(
                "Missing NOTION_TOKEN. "
                "Get your token from https://www.notion.so/my-integrations"
            )
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": self.NOTION_VERSION,
        }

    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generic Notion API request handler"""
        url = f"{self.API_BASE}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == "GET":
                r = await client.get(url, headers=self.headers, params=params or {})
            elif method == "POST":
                r = await client.post(url, headers=self.headers, json=data or {})
            elif method == "PATCH":
                r = await client.patch(url, headers=self.headers, json=data or {})
            elif method == "DELETE":
                r = await client.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            r.raise_for_status()
            return r.json()

    # ─── Search ───────────────────────────────────────────────────────────────

    async def search(
        self,
        query: str = "",
        filter_type: Optional[str] = None,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search pages and databases in Notion workspace"""
        payload: Dict[str, Any] = {"page_size": page_size}
        if query:
            payload["query"] = query
        if filter_type in ("page", "database"):
            payload["filter"] = {"value": filter_type, "property": "object"}
        return await self.request("search", "POST", data=payload)

    # ─── Pages ────────────────────────────────────────────────────────────────

    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get a Notion page by ID"""
        return await self.request(f"pages/{page_id}")

    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: Optional[str] = None,
        parent_type: str = "page_id",
    ) -> Dict[str, Any]:
        """
        Create a new Notion page

        Args:
            parent_id: ID of parent page or database
            title: Page title
            content: Optional text content for the page body
            parent_type: 'page_id' or 'database_id'
        """
        payload: Dict[str, Any] = {
            "parent": {parent_type: parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
        }
        if content:
            payload["children"] = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            ]
        return await self.request("pages", "POST", data=payload)

    async def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any],
        archived: bool = False,
    ) -> Dict[str, Any]:
        """Update a Notion page properties"""
        return await self.request(
            f"pages/{page_id}",
            "PATCH",
            data={"properties": properties, "archived": archived},
        )

    async def archive_page(self, page_id: str) -> Dict[str, Any]:
        """Archive (soft-delete) a Notion page"""
        return await self.request(
            f"pages/{page_id}", "PATCH", data={"archived": True}
        )

    # ─── Blocks ───────────────────────────────────────────────────────────────

    async def get_page_content(self, block_id: str) -> Dict[str, Any]:
        """Get all blocks (content) of a page"""
        return await self.request(f"blocks/{block_id}/children")

    async def append_content(
        self, block_id: str, text: str
    ) -> Dict[str, Any]:
        """Append a paragraph block to a page"""
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": text}}]
                    },
                }
            ]
        }
        return await self.request(
            f"blocks/{block_id}/children", "PATCH", data=payload
        )

    async def delete_block(self, block_id: str) -> Dict[str, Any]:
        """Delete a block"""
        return await self.request(f"blocks/{block_id}", "DELETE")

    # ─── Databases ────────────────────────────────────────────────────────────

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """Get a Notion database schema"""
        return await self.request(f"databases/{database_id}")

    async def query_database(
        self,
        database_id: str,
        filter_obj: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Query a Notion database with optional filters and sorting"""
        payload: Dict[str, Any] = {"page_size": page_size}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        return await self.request(
            f"databases/{database_id}/query", "POST", data=payload
        )

    async def create_database_entry(
        self,
        database_id: str,
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new entry (row) in a Notion database"""
        return await self.request(
            "pages",
            "POST",
            data={
                "parent": {"database_id": database_id},
                "properties": properties,
            },
        )

    # ─── Users ────────────────────────────────────────────────────────────────

    async def list_users(self) -> Dict[str, Any]:
        """List all users in the Notion workspace"""
        return await self.request("users")

    async def get_bot_user(self) -> Dict[str, Any]:
        """Get the bot user info (verify connection)"""
        return await self.request("users/me")

    # ─── Comments ────────────────────────────────────────────────────────────

    async def get_comments(self, block_id: str) -> Dict[str, Any]:
        """Get comments on a page or block"""
        return await self.request("comments", params={"block_id": block_id})

    async def add_comment(
        self, page_id: str, text: str
    ) -> Dict[str, Any]:
        """Add a comment to a page"""
        return await self.request(
            "comments",
            "POST",
            data={
                "parent": {"page_id": page_id},
                "rich_text": [{"text": {"content": text}}],
            },
        )
