"""
Notion MCP Server for NewZyon Project
Temple 5 of the 64 Bhairava Guardian Temples
Purpose: Knowledge Base & Sacred Mind Palace

Guardian: Unmatta Bhairava — Lord of the Mind
Sanskrit: Unmatta (The Frenzied One who sees all knowledge)

The Vikarma Team | Om Namah Shivaya 🔱
"""
from fastmcp import FastMCP
import os
import json
from typing import Optional
from notion_addon import NotionAddon

mcp = FastMCP("Notion MCP - Temple 5 | Nexus Bhairava")
notion = NotionAddon()


# ─── SEARCH ───────────────────────────────────────────────────────────────────

@mcp.tool()
async def notion_search(query: str, filter_type: str = "", limit: int = 20) -> str:
    """
    Search pages and databases in your Notion workspace.

    Args:
        query: Search query string
        filter_type: Filter by 'page' or 'database' (leave empty for all)
        limit: Max results to return (default 20)

    Returns:
        List of matching pages/databases with titles and IDs
    """
    try:
        ft = filter_type if filter_type in ("page", "database") else None
        result = await notion.search(query=query, filter_type=ft, page_size=limit)
        results = result.get("results", [])

        if not results:
            return f"No results found for '{query}'"

        output = f"🔍 **Notion Search** — '{query}' ({len(results)} results)\n\n"
        for item in results:
            obj_type = item.get("object", "unknown")
            item_id = item.get("id", "")

            if obj_type == "page":
                props = item.get("properties", {})
                title_prop = props.get("title") or props.get("Name") or {}
                title_list = title_prop.get("title", []) if isinstance(title_prop, dict) else []
                title = "".join([t.get("plain_text", "") for t in title_list]) or "Untitled"
                url = item.get("url", "")
                output += f"📄 **{title}**\n   ID: `{item_id}`\n   🔗 {url}\n\n"

            elif obj_type == "database":
                title_list = item.get("title", [])
                title = "".join([t.get("plain_text", "") for t in title_list]) or "Untitled DB"
                url = item.get("url", "")
                output += f"🗄️ **{title}** (Database)\n   ID: `{item_id}`\n   🔗 {url}\n\n"

        return output
    except Exception as e:
        return f"❌ Search failed: {str(e)}"


# ─── PAGES ────────────────────────────────────────────────────────────────────

@mcp.tool()
async def notion_get_page(page_id: str) -> str:
    """
    Get details of a Notion page by its ID.

    Args:
        page_id: The Notion page ID (e.g., abc123def456...)

    Returns:
        Page title, properties, and metadata
    """
    try:
        page = await notion.get_page(page_id)
        props = page.get("properties", {})

        title = "Untitled"
        for prop in props.values():
            if isinstance(prop, dict) and prop.get("type") == "title":
                title_list = prop.get("title", [])
                title = "".join([t.get("plain_text", "") for t in title_list])
                break

        url = page.get("url", "")
        created = page.get("created_time", "")[:10]
        edited = page.get("last_edited_time", "")[:10]
        archived = page.get("archived", False)

        output = f"""📄 **{title}**
━━━━━━━━━━━━━━━━━━━━━
• ID: `{page_id}`
• URL: {url}
• Created: {created}
• Last edited: {edited}
• Archived: {'Yes ⚠️' if archived else 'No ✅'}
• Properties: {len(props)} fields
        """.strip()

        return output
    except Exception as e:
        return f"❌ Failed to get page: {str(e)}"


@mcp.tool()
async def notion_get_page_content(page_id: str) -> str:
    """
    Get the full text content of a Notion page.

    Args:
        page_id: The Notion page ID

    Returns:
        Full page content as readable text
    """
    try:
        result = await notion.get_page_content(page_id)
        blocks = result.get("results", [])

        if not blocks:
            return f"Page `{page_id}` has no content."

        output = f"📖 **Page Content** ({len(blocks)} blocks)\n\n"

        for block in blocks:
            btype = block.get("type", "")
            bdata = block.get(btype, {})
            rich_text = bdata.get("rich_text", [])
            text = "".join([t.get("plain_text", "") for t in rich_text])

            if btype == "heading_1":
                output += f"# {text}\n"
            elif btype == "heading_2":
                output += f"## {text}\n"
            elif btype == "heading_3":
                output += f"### {text}\n"
            elif btype == "paragraph":
                output += f"{text}\n"
            elif btype == "bulleted_list_item":
                output += f"• {text}\n"
            elif btype == "numbered_list_item":
                output += f"1. {text}\n"
            elif btype == "to_do":
                checked = bdata.get("checked", False)
                output += f"{'☑' if checked else '☐'} {text}\n"
            elif btype == "quote":
                output += f"> {text}\n"
            elif btype == "code":
                lang = bdata.get("language", "")
                output += f"```{lang}\n{text}\n```\n"
            elif btype == "divider":
                output += "---\n"
            else:
                if text:
                    output += f"{text}\n"

        return output[:4000]
    except Exception as e:
        return f"❌ Failed to get content: {str(e)}"


@mcp.tool()
async def notion_create_page(
    parent_id: str,
    title: str,
    content: str = "",
    parent_type: str = "page_id",
) -> str:
    """
    Create a new Notion page.

    Args:
        parent_id: ID of the parent page or database
        title: Title of the new page
        content: Optional text content for the page body
        parent_type: 'page_id' (default) or 'database_id'

    Returns:
        Confirmation with new page ID and URL
    """
    try:
        page = await notion.create_page(
            parent_id=parent_id,
            title=title,
            content=content,
            parent_type=parent_type,
        )
        page_id = page.get("id", "")
        url = page.get("url", "")
        return (
            f"✅ Page created!\n"
            f"• Title: **{title}**\n"
            f"• ID: `{page_id}`\n"
            f"• URL: {url}"
        )
    except Exception as e:
        return f"❌ Failed to create page: {str(e)}"


@mcp.tool()
async def notion_append_content(page_id: str, text: str) -> str:
    """
    Append text content to an existing Notion page.

    Args:
        page_id: The page ID to append content to
        text: Text content to append

    Returns:
        Confirmation of content added
    """
    try:
        await notion.append_content(page_id, text)
        return f"✅ Content appended to page `{page_id}`"
    except Exception as e:
        return f"❌ Failed to append content: {str(e)}"


@mcp.tool()
async def notion_archive_page(page_id: str) -> str:
    """
    Archive (soft-delete) a Notion page.

    Args:
        page_id: The page ID to archive

    Returns:
        Confirmation of archiving
    """
    try:
        await notion.archive_page(page_id)
        return f"✅ Page `{page_id}` archived successfully."
    except Exception as e:
        return f"❌ Failed to archive page: {str(e)}"


# ─── DATABASES ────────────────────────────────────────────────────────────────

@mcp.tool()
async def notion_get_database(database_id: str) -> str:
    """
    Get schema and details of a Notion database.

    Args:
        database_id: The Notion database ID

    Returns:
        Database title, properties schema, and metadata
    """
    try:
        db = await notion.get_database(database_id)
        title_list = db.get("title", [])
        title = "".join([t.get("plain_text", "") for t in title_list]) or "Untitled"
        props = db.get("properties", {})
        url = db.get("url", "")

        output = f"🗄️ **Database: {title}**\n━━━━━━━━━━━━━━━━━━\n"
        output += f"• ID: `{database_id}`\n• URL: {url}\n\n"
        output += f"**Properties ({len(props)}):**\n"
        for name, prop in props.items():
            ptype = prop.get("type", "unknown")
            output += f"  • {name} ({ptype})\n"

        return output
    except Exception as e:
        return f"❌ Failed to get database: {str(e)}"


@mcp.tool()
async def notion_query_database(
    database_id: str,
    limit: int = 20,
) -> str:
    """
    Query all entries in a Notion database.

    Args:
        database_id: The Notion database ID
        limit: Max entries to return (default 20)

    Returns:
        List of database entries with their properties
    """
    try:
        result = await notion.query_database(database_id, page_size=limit)
        entries = result.get("results", [])

        if not entries:
            return f"Database `{database_id}` has no entries."

        output = f"📊 **Database Entries** ({len(entries)} found)\n\n"

        for entry in entries:
            props = entry.get("properties", {})
            entry_id = entry.get("id", "")
            url = entry.get("url", "")

            title = "Untitled"
            for prop in props.values():
                if isinstance(prop, dict) and prop.get("type") == "title":
                    title_list = prop.get("title", [])
                    title = "".join([t.get("plain_text", "") for t in title_list])
                    break

            output += f"• **{title}**\n  ID: `{entry_id}` | {url}\n"

        return output
    except Exception as e:
        return f"❌ Failed to query database: {str(e)}"


# ─── COMMENTS ────────────────────────────────────────────────────────────────

@mcp.tool()
async def notion_add_comment(page_id: str, comment: str) -> str:
    """
    Add a comment to a Notion page.

    Args:
        page_id: The page ID to comment on
        comment: Comment text

    Returns:
        Confirmation of comment added
    """
    try:
        await notion.add_comment(page_id, comment)
        return f"✅ Comment added to page `{page_id}`"
    except Exception as e:
        return f"❌ Failed to add comment: {str(e)}"


# ─── STATUS ───────────────────────────────────────────────────────────────────

@mcp.tool()
async def notion_status() -> str:
    """
    Check Notion connection and Temple 5 health.

    Returns:
        Connection status and bot user info
    """
    try:
        bot = await notion.get_bot_user()
        name = bot.get("name", "Unknown")
        bot_id = bot.get("id", "")
        bot_type = bot.get("type", "")

        return (
            f"🔱 Temple 5 - Notion Guardian - ONLINE\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Bot Name: {name}\n"
            f"• Bot ID: `{bot_id}`\n"
            f"• Type: {bot_type}\n"
            f"• Purpose: Knowledge Base & Sacred Mind Palace\n"
            f"• Guardian: Unmatta Bhairava\n"
            f"• Temple: 5/64 Bhairava Guardians\n"
            f"\nOm Namah Shivaya 🕉️"
        )
    except Exception as e:
        return f"❌ Temple 5 (Notion) error: {str(e)}"


if __name__ == "__main__":
    print("🔱 Temple 5 - Notion Guardian AWAKENING...")
    print("🏛️ Nexus Bhairava Temples | The Vikarma Team")
    mcp.run()
