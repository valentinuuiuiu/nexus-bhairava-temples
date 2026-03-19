"""
Slack MCP Addon for NewZyon/PAI-KAN Architecture
Temple 3 - Slack Guardian
Modular addon pattern - consistent with Jira and GitHub addons

The Vikarma Team - ionutbaltag3@gmail.com
Om Namah Shivaya 🔱
"""

from typing import Dict, Any, Optional, List
import httpx
import os


class SlackAddon:
    """
    Slack integration addon for MCP server
    Follows the FastMCP + addon.py pattern for NewZyon
    
    Temple 3 of the 64 Bhairava Guardian Temples
    Guardian: Slack - The Voice of the Team
    """

    SLACK_API_BASE = "https://slack.com/api"

    def __init__(
        self,
        bot_token: Optional[str] = None,
        user_token: Optional[str] = None,
    ):
        """
        Initialize Slack addon with credentials

        Args:
            bot_token: Slack Bot OAuth token (xoxb-...)
            user_token: Slack User OAuth token (xoxp-...) - optional, for user-level actions
        """
        self.bot_token = bot_token or os.getenv("SLACK_BOT_TOKEN")
        self.user_token = user_token or os.getenv("SLACK_USER_TOKEN")

        if not self.bot_token:
            raise ValueError(
                "Missing SLACK_BOT_TOKEN. "
                "Create a Slack App at https://api.slack.com/apps and install it to your workspace."
            )

        self.headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def _get_headers(self, use_user_token: bool = False) -> Dict[str, str]:
        """Return appropriate auth headers"""
        token = self.user_token if use_user_token and self.user_token else self.bot_token
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    async def request(
        self,
        method_name: str,
        http_method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        use_user_token: bool = False,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Slack Web API

        Args:
            method_name: Slack API method (e.g., 'chat.postMessage')
            http_method: HTTP method (GET or POST)
            data: Request body (for POST)
            params: Query parameters (for GET)
            use_user_token: Use user token instead of bot token

        Returns:
            API response as dictionary
        """
        url = f"{self.SLACK_API_BASE}/{method_name}"
        headers = self._get_headers(use_user_token)

        async with httpx.AsyncClient(timeout=30.0) as client:
            if http_method == "POST":
                response = await client.post(url, headers=headers, json=data or {})
            else:
                response = await client.get(url, headers=headers, params=params or {})

            response.raise_for_status()
            result = response.json()

            # Slack API always returns 200, but includes ok: true/false
            if not result.get("ok"):
                error = result.get("error", "Unknown Slack API error")
                raise ValueError(f"Slack API error: {error}")

            return result

    # ─── Channel Operations ────────────────────────────────────────────────

    async def list_channels(
        self,
        exclude_archived: bool = True,
        limit: int = 100,
        types: str = "public_channel,private_channel",
    ) -> List[Dict[str, Any]]:
        """List all channels in the workspace"""
        result = await self.request(
            "conversations.list",
            params={
                "exclude_archived": str(exclude_archived).lower(),
                "limit": limit,
                "types": types,
            },
        )
        return result.get("channels", [])

    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get detailed info about a specific channel"""
        result = await self.request(
            "conversations.info",
            params={"channel": channel_id},
        )
        return result.get("channel", {})

    async def create_channel(
        self, name: str, is_private: bool = False
    ) -> Dict[str, Any]:
        """Create a new Slack channel"""
        result = await self.request(
            "conversations.create",
            http_method="POST",
            data={"name": name, "is_private": is_private},
        )
        return result.get("channel", {})

    async def join_channel(self, channel_id: str) -> Dict[str, Any]:
        """Join a Slack channel (bot joins)"""
        result = await self.request(
            "conversations.join",
            http_method="POST",
            data={"channel": channel_id},
        )
        return result.get("channel", {})

    # ─── Messaging Operations ──────────────────────────────────────────────

    async def send_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None,
        blocks: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Send a message to a channel or thread

        Args:
            channel: Channel ID or name (e.g., 'C1234567890' or '#general')
            text: Message text
            thread_ts: Thread timestamp to reply in thread
            blocks: Block Kit blocks for rich formatting
        """
        payload: Dict[str, Any] = {"channel": channel, "text": text}
        if thread_ts:
            payload["thread_ts"] = thread_ts
        if blocks:
            payload["blocks"] = blocks

        result = await self.request("chat.postMessage", http_method="POST", data=payload)
        return result

    async def update_message(
        self, channel: str, ts: str, text: str
    ) -> Dict[str, Any]:
        """Update an existing message"""
        result = await self.request(
            "chat.update",
            http_method="POST",
            data={"channel": channel, "ts": ts, "text": text},
        )
        return result

    async def delete_message(self, channel: str, ts: str) -> Dict[str, Any]:
        """Delete a message"""
        result = await self.request(
            "chat.delete",
            http_method="POST",
            data={"channel": channel, "ts": ts},
        )
        return result

    async def get_channel_history(
        self,
        channel_id: str,
        limit: int = 20,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get message history from a channel"""
        params: Dict[str, Any] = {"channel": channel_id, "limit": limit}
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest

        result = await self.request("conversations.history", params=params)
        return result.get("messages", [])

    async def get_thread_replies(
        self, channel_id: str, thread_ts: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get replies in a thread"""
        result = await self.request(
            "conversations.replies",
            params={"channel": channel_id, "ts": thread_ts, "limit": limit},
        )
        return result.get("messages", [])

    # ─── User Operations ───────────────────────────────────────────────────

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get information about a Slack user"""
        result = await self.request("users.info", params={"user": user_id})
        return result.get("user", {})

    async def list_users(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all users in the workspace"""
        result = await self.request("users.list", params={"limit": limit})
        return result.get("members", [])

    async def get_bot_info(self) -> Dict[str, Any]:
        """Get info about the authenticated bot"""
        result = await self.request("auth.test")
        return result

    # ─── Search Operations ─────────────────────────────────────────────────

    async def search_messages(
        self, query: str, count: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search messages in Slack workspace
        Note: Requires user token (xoxp-) not bot token
        """
        result = await self.request(
            "search.messages",
            params={"query": query, "count": count},
            use_user_token=True,
        )
        return result.get("messages", {}).get("matches", [])

    # ─── Reaction Operations ───────────────────────────────────────────────

    async def add_reaction(
        self, channel: str, timestamp: str, emoji_name: str
    ) -> Dict[str, Any]:
        """Add an emoji reaction to a message"""
        result = await self.request(
            "reactions.add",
            http_method="POST",
            data={"channel": channel, "timestamp": timestamp, "name": emoji_name},
        )
        return result

    # ─── File Operations ───────────────────────────────────────────────────

    async def upload_file(
        self,
        channel: str,
        content: str,
        filename: str,
        title: Optional[str] = None,
        filetype: str = "text",
    ) -> Dict[str, Any]:
        """Upload a file/snippet to a channel"""
        # Use multipart form for file uploads
        url = f"{self.SLACK_API_BASE}/files.upload"
        headers = {"Authorization": f"Bearer {self.bot_token}"}

        async with httpx.AsyncClient(timeout=30.0) as client:
            data = {
                "channels": channel,
                "content": content,
                "filename": filename,
                "filetype": filetype,
            }
            if title:
                data["title"] = title

            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()

            if not result.get("ok"):
                raise ValueError(f"Slack file upload error: {result.get('error')}")

            return result.get("file", {})
