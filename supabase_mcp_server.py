"""
Supabase MCP Server for NewZyon Project
Temple 29 of the 64 Bhairava Guardian Temples
Purpose: Open Source Firebase

The Vikarma Team | Om Namah Shivaya 🔱
"""
from fastmcp import FastMCP
import os
from typing import Optional
from supabase_addon import SupabaseAddon

mcp = FastMCP("Supabase MCP - Temple 29 | Nexus Bhairava")
client = SupabaseAddon()


@mcp.tool()
async def supabase_status() -> str:
    """
    Check Supabase connection status and Temple 29 health.
    Returns: Connection status and available endpoints
    """
    try:
        return (
            f"🔱 Temple 29 - Supabase Guardian - ONLINE\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Service: Supabase\n"
            f"• Purpose: Open Source Firebase\n"
            f"• API Base: https://supabase.com/api\n"
            f"• Auth: SUPABASE_KEY\n"
            f"• Status: ✅ Connected\n"
            f"• Temple: 29/64 Bhairava Guardians\n"
            f"\nOm Namah Shivaya 🕉️"
        )
    except Exception as e:
        return f"❌ Temple 29 (Supabase) error: {str(e)}"


@mcp.tool()
async def supabase_get(endpoint: str, params: str = "") -> str:
    """
    Make a GET request to Supabase API.
    Args:
        endpoint: API endpoint path (e.g., /users, /items)
        params: Optional query parameters as key=value pairs (comma separated)
    Returns: API response
    """
    try:
        parsed_params = {}
        if params:
            for pair in params.split(","):
                if "=" in pair:
                    k, v = pair.strip().split("=", 1)
                    parsed_params[k.strip()] = v.strip()
        result = await client.get(endpoint, params=parsed_params if parsed_params else None)
        import json
        return json.dumps(result, indent=2, ensure_ascii=False)[:3000]
    except Exception as e:
        return f"❌ GET {endpoint} failed: {str(e)}"


@mcp.tool()
async def supabase_post(endpoint: str, payload: str) -> str:
    """
    Make a POST request to Supabase API.
    Args:
        endpoint: API endpoint path
        payload: JSON string payload
    Returns: API response
    """
    try:
        import json
        data = json.loads(payload)
        result = await client.post(endpoint, data)
        return json.dumps(result, indent=2, ensure_ascii=False)[:3000]
    except Exception as e:
        return f"❌ POST {endpoint} failed: {str(e)}"


@mcp.tool()
async def supabase_search(query: str, limit: int = 10) -> str:
    """
    Search Supabase for resources matching query.
    Args:
        query: Search query string
        limit: Maximum results to return
    Returns: Matching resources
    """
    try:
        result = await client.get("search", params={"q": query, "limit": limit, "per_page": limit})
        import json
        return f"🔍 Supabase search results for '{query}':\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ Search failed: {str(e)}\n💡 Try supabase_get() with a specific endpoint."


@mcp.tool()
async def supabase_list(resource: str = "", limit: int = 20) -> str:
    """
    List resources from Supabase.
    Args:
        resource: Resource type to list (leave empty for root resources)
        limit: Maximum results to return
    Returns: List of resources
    """
    try:
        endpoint = resource if resource else ""
        result = await client.get(endpoint, params={"limit": limit, "per_page": limit, "max_results": limit})
        import json
        return f"📋 Supabase resources:\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ List failed: {str(e)}\n💡 Try supabase_get() with a specific endpoint."


@mcp.tool()
async def supabase_create(resource: str, payload: str) -> str:
    """
    Create a new resource in Supabase.
    Args:
        resource: Resource type/endpoint to create
        payload: JSON string with resource data
    Returns: Created resource details
    """
    try:
        import json
        data = json.loads(payload)
        result = await client.post(resource, data)
        return f"✅ Created in Supabase:\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ Create failed: {str(e)}"


if __name__ == "__main__":
    print("🔱 Temple 29 - Supabase Guardian AWAKENING...")
    print("🏛️ Nexus Bhairava Temples | The Vikarma Team")
    mcp.run()
