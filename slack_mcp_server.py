"""
Slack MCP Server for NewZyon Project (The Vikarma Team)
Temple 3 of the 64 Bhairava Guardian Temples
FastMCP implementation for PAI/KAN architecture

Guardian Deity: Slack Bhairava - The Voice of Collaboration
Sanskrit Identity: Vākpati (Lord of Speech)

Author: Built with Claude (Tvaṣṭā) for ionutbaltag3@gmail.com
Om Namah Shivaya 🔱
"""

from fastmcp import FastMCP
import os
from typing import Optional
from slack_addon import SlackAddon

# ─── Initialize FastMCP Server ─────────────────────────────────────────────────
mcp = FastMCP("Slack MCP - Temple 3 | Nexus Bhairava")

# ─── Initialize Slack Addon ────────────────────────────────────────────────────
slack = SlackAddon(
    bot_token=os.getenv("SLACK_BOT_TOKEN"),
    user_token=os.getenv("SLACK_USER_TOKEN"),
)


# ═══════════════════════════════════════════════════════════════════════════════
# CHANNEL TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def list_slack_channels(
    exclude_archived: bool = True,
    limit: int = 50,
) -> str:
    """
    List all channels in the Slack workspace.

    Args:
        exclude_archived: If True, exclude archived channels
        limit: Maximum number of channels to return (default: 50)

    Returns:
        Formatted list of channels with their IDs and topics
    """
    try:
        channels = await slack.list_channels(
            exclude_archived=exclude_archived,
            limit=limit,
        )

        if not channels:
            return "No channels found in workspace."

        result = f"📋 **Slack Channels** ({len(channels)} found)\n\n"
        for ch in channels:
            is_private = "🔒" if ch.get("is_private") else "📢"
            name = ch.get("name", "unknown")
            ch_id = ch.get("id", "")
            members = ch.get("num_members", 0)
            topic = ch.get("topic", {}).get("value", "") or ch.get("purpose", {}).get("value", "")

            result += f"{is_private} **#{name}** (ID: `{ch_id}`) — {members} members\n"
            if topic:
                result += f"   💬 {topic[:80]}{'...' if len(topic) > 80 else ''}\n"

        return result

    except Exception as e:
        return f"❌ Error listing channels: {str(e)}"


@mcp.tool()
async def get_slack_channel_info(channel_id: str) -> str:
    """
    Get detailed information about a specific Slack channel.

    Args:
        channel_id: The Slack channel ID (e.g., C1234567890)

    Returns:
        Detailed channel information
    """
    try:
        ch = await slack.get_channel_info(channel_id)

        if not ch:
            return f"Channel {channel_id} not found."

        is_private = "Private 🔒" if ch.get("is_private") else "Public 📢"
        name = ch.get("name", "unknown")
        members = ch.get("num_members", 0)
        topic = ch.get("topic", {}).get("value", "No topic set")
        purpose = ch.get("purpose", {}).get("value", "No purpose set")
        created = ch.get("created", "")

        result = f"""
🏛️ **Channel: #{name}**
━━━━━━━━━━━━━━━━━━━━
• ID: `{channel_id}`
• Type: {is_private}
• Members: {members}
• Topic: {topic}
• Purpose: {purpose}
• Created: {created}
        """.strip()

        return result

    except Exception as e:
        return f"❌ Error getting channel info: {str(e)}"


@mcp.tool()
async def create_slack_channel(
    name: str,
    is_private: bool = False,
) -> str:
    """
    Create a new Slack channel.

    Args:
        name: Channel name (lowercase, no spaces — use hyphens)
        is_private: If True, create a private channel

    Returns:
        Confirmation with new channel details
    """
    try:
        channel = await slack.create_channel(name=name, is_private=is_private)

        ch_id = channel.get("id", "")
        ch_name = channel.get("name", name)
        privacy = "private 🔒" if is_private else "public 📢"

        return (
            f"✅ Channel created successfully!\n"
            f"• Name: **#{ch_name}**\n"
            f"• ID: `{ch_id}`\n"
            f"• Type: {privacy}"
        )

    except Exception as e:
        return f"❌ Error creating channel: {str(e)}"


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGING TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def send_slack_message(
    channel: str,
    message: str,
    thread_ts: Optional[str] = None,
) -> str:
    """
    Send a message to a Slack channel or thread.

    Args:
        channel: Channel ID (e.g., C1234567890) or channel name (e.g., #general)
        message: The message text to send (supports Slack markdown)
        thread_ts: Optional thread timestamp to reply in a thread

    Returns:
        Confirmation with message timestamp
    """
    try:
        result = await slack.send_message(
            channel=channel,
            text=message,
            thread_ts=thread_ts,
        )

        ts = result.get("ts", "")
        ch = result.get("channel", channel)

        if thread_ts:
            return f"✅ Reply sent to thread in `{ch}`\n• Message timestamp: `{ts}`"
        else:
            return f"✅ Message sent to `{ch}`\n• Timestamp: `{ts}`\n• Use this timestamp to reply in thread!"

    except Exception as e:
        return f"❌ Error sending message: {str(e)}"


@mcp.tool()
async def get_slack_channel_history(
    channel_id: str,
    limit: int = 10,
) -> str:
    """
    Get recent message history from a Slack channel.

    Args:
        channel_id: The Slack channel ID (e.g., C1234567890)
        limit: Number of messages to retrieve (default: 10, max: 100)

    Returns:
        Formatted message history
    """
    try:
        messages = await slack.get_channel_history(
            channel_id=channel_id,
            limit=min(limit, 100),
        )

        if not messages:
            return f"No messages found in channel `{channel_id}`."

        result = f"💬 **Recent Messages** (last {len(messages)})\n\n"

        for msg in reversed(messages):  # Show oldest first
            user = msg.get("user", msg.get("bot_id", "unknown"))
            text = msg.get("text", "")
            ts = msg.get("ts", "")
            thread_count = msg.get("reply_count", 0)

            # Truncate long messages
            display_text = text[:200] + "..." if len(text) > 200 else text

            result += f"👤 `{user}` | ⏱ `{ts}`\n"
            result += f"   {display_text}\n"
            if thread_count:
                result += f"   🧵 {thread_count} replies in thread\n"
            result += "\n"

        return result

    except Exception as e:
        return f"❌ Error getting channel history: {str(e)}"


@mcp.tool()
async def get_slack_thread_replies(
    channel_id: str,
    thread_ts: str,
    limit: int = 20,
) -> str:
    """
    Get all replies in a Slack thread.

    Args:
        channel_id: The channel ID containing the thread
        thread_ts: The timestamp of the parent message (thread root)
        limit: Number of replies to retrieve

    Returns:
        Formatted thread conversation
    """
    try:
        messages = await slack.get_thread_replies(
            channel_id=channel_id,
            thread_ts=thread_ts,
            limit=limit,
        )

        if not messages:
            return "No replies found in this thread."

        result = f"🧵 **Thread Replies** ({len(messages)} messages)\n\n"

        for i, msg in enumerate(messages):
            user = msg.get("user", msg.get("bot_id", "unknown"))
            text = msg.get("text", "")
            ts = msg.get("ts", "")
            label = "📌 **[Root]**" if i == 0 else f"↩️ Reply {i}"

            result += f"{label} | 👤 `{user}` | ⏱ `{ts}`\n"
            result += f"   {text[:300]}{'...' if len(text) > 300 else ''}\n\n"

        return result

    except Exception as e:
        return f"❌ Error getting thread replies: {str(e)}"


@mcp.tool()
async def update_slack_message(
    channel: str,
    message_ts: str,
    new_text: str,
) -> str:
    """
    Update an existing Slack message.

    Args:
        channel: Channel ID containing the message
        message_ts: Timestamp of the message to update
        new_text: New text content for the message

    Returns:
        Confirmation of update
    """
    try:
        result = await slack.update_message(
            channel=channel,
            ts=message_ts,
            text=new_text,
        )
        ts = result.get("ts", message_ts)
        return f"✅ Message updated successfully!\n• Channel: `{channel}`\n• Timestamp: `{ts}`"

    except Exception as e:
        return f"❌ Error updating message: {str(e)}"


# ═══════════════════════════════════════════════════════════════════════════════
# USER TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_slack_user_info(user_id: str) -> str:
    """
    Get information about a Slack user.

    Args:
        user_id: The Slack user ID (e.g., U1234567890)

    Returns:
        User profile information
    """
    try:
        user = await slack.get_user_info(user_id)

        if not user:
            return f"User `{user_id}` not found."

        profile = user.get("profile", {})
        name = profile.get("real_name", user.get("name", "unknown"))
        display_name = profile.get("display_name", "")
        email = profile.get("email", "hidden")
        title = profile.get("title", "")
        tz = user.get("tz", "")
        is_bot = "🤖 Bot" if user.get("is_bot") else "👤 Human"

        result = f"""
🪪 **User: {name}**
━━━━━━━━━━━━━━━━━━
• ID: `{user_id}`
• Type: {is_bot}
• Display Name: {display_name or name}
• Email: {email}
• Title: {title or "No title"}
• Timezone: {tz or "Unknown"}
        """.strip()

        return result

    except Exception as e:
        return f"❌ Error getting user info: {str(e)}"


@mcp.tool()
async def list_slack_users(limit: int = 50) -> str:
    """
    List all users in the Slack workspace.

    Args:
        limit: Maximum number of users to return

    Returns:
        Formatted list of workspace members
    """
    try:
        users = await slack.list_users(limit=limit)

        # Filter out bots and deactivated users
        active_humans = [
            u for u in users
            if not u.get("deleted") and not u.get("is_bot") and u.get("id") != "USLACKBOT"
        ]
        bots = [u for u in users if u.get("is_bot") and not u.get("deleted")]

        result = f"👥 **Workspace Members**\n"
        result += f"   Active humans: {len(active_humans)} | Bots: {len(bots)}\n\n"

        result += "**👤 Team Members:**\n"
        for user in active_humans[:limit]:
            profile = user.get("profile", {})
            name = profile.get("real_name", user.get("name", "unknown"))
            display = profile.get("display_name", "")
            user_id = user.get("id", "")
            tz = user.get("tz_label", "")

            result += f"• {name}"
            if display and display != name:
                result += f" (@{display})"
            result += f" — `{user_id}`"
            if tz:
                result += f" 🕐 {tz}"
            result += "\n"

        if bots:
            result += f"\n**🤖 Bots ({len(bots)}):**\n"
            for bot in bots[:10]:
                bot_name = bot.get("profile", {}).get("real_name", bot.get("name", "unknown"))
                result += f"• {bot_name} — `{bot.get('id', '')}`\n"

        return result

    except Exception as e:
        return f"❌ Error listing users: {str(e)}"


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
async def get_slack_workspace_info() -> str:
    """
    Get information about the connected Slack workspace and bot identity.

    Returns:
        Workspace and bot authentication info
    """
    try:
        info = await slack.get_bot_info()

        team = info.get("team", "unknown")
        team_id = info.get("team_id", "")
        user = info.get("user", "unknown")
        user_id = info.get("user_id", "")
        url = info.get("url", "")

        result = f"""
🏢 **Slack Workspace Info**
━━━━━━━━━━━━━━━━━━━━━━━━━
• Workspace: **{team}** (`{team_id}`)
• Bot Name: **{user}** (`{user_id}`)
• URL: {url}

🔱 Temple 3 — Slack Bhairava — ONLINE
Om Namah Shivaya
        """.strip()

        return result

    except Exception as e:
        return f"❌ Error getting workspace info: {str(e)}"


@mcp.tool()
async def add_slack_reaction(
    channel: str,
    message_ts: str,
    emoji: str,
) -> str:
    """
    Add an emoji reaction to a Slack message.

    Args:
        channel: Channel ID containing the message
        message_ts: Timestamp of the message
        emoji: Emoji name without colons (e.g., 'thumbsup', 'fire', 'om')

    Returns:
        Confirmation of reaction added
    """
    try:
        await slack.add_reaction(
            channel=channel,
            timestamp=message_ts,
            emoji_name=emoji,
        )
        return f"✅ Reaction :{emoji}: added to message `{message_ts}`"

    except Exception as e:
        return f"❌ Error adding reaction: {str(e)}"


@mcp.tool()
async def search_slack_messages(
    query: str,
    count: int = 10,
) -> str:
    """
    Search messages across the Slack workspace.
    Note: Requires SLACK_USER_TOKEN (xoxp-) in addition to bot token.

    Args:
        query: Search query string
        count: Number of results to return

    Returns:
        Matching messages with context
    """
    try:
        matches = await slack.search_messages(query=query, count=count)

        if not matches:
            return f"No messages found for query: '{query}'"

        result = f"🔍 **Search Results** for '{query}' ({len(matches)} found)\n\n"

        for match in matches:
            channel_name = match.get("channel", {}).get("name", "unknown")
            username = match.get("username", "unknown")
            text = match.get("text", "")
            ts = match.get("ts", "")
            permalink = match.get("permalink", "")

            result += f"📢 **#{channel_name}** | 👤 {username}\n"
            result += f"   {text[:200]}{'...' if len(text) > 200 else ''}\n"
            if permalink:
                result += f"   🔗 {permalink}\n"
            result += "\n"

        return result

    except Exception as e:
        return f"❌ Error searching messages: {str(e)}\n💡 Tip: Search requires SLACK_USER_TOKEN (xoxp-)"


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔱 Temple 3 - Slack Bhairava Guardian AWAKENING...")
    print("🏛️ Nexus Bhairava Temples | The Vikarma Team")
    print("📡 Starting Slack MCP Server...")
    mcp.run()
