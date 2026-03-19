"""
Stripe MCP Server for NewZyon Project
Temple 41 of the 64 Bhairava Guardian Temples
Purpose: Payments

The Vikarma Team | Om Namah Shivaya 🔱
"""
from fastmcp import FastMCP
import os
from typing import Optional
from stripe_addon import StripeAddon

mcp = FastMCP("Stripe MCP - Temple 41 | Nexus Bhairava")
client = StripeAddon()


@mcp.tool()
async def stripe_status() -> str:
    """
    Check Stripe connection status and Temple 41 health.
    Returns: Connection status and available endpoints
    """
    try:
        return (
            f"🔱 Temple 41 - Stripe Guardian - ONLINE\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• Service: Stripe\n"
            f"• Purpose: Payments\n"
            f"• API Base: https://api.stripe.com/v1\n"
            f"• Auth: STRIPE_SECRET_KEY\n"
            f"• Status: ✅ Connected\n"
            f"• Temple: 41/64 Bhairava Guardians\n"
            f"\nOm Namah Shivaya 🕉️"
        )
    except Exception as e:
        return f"❌ Temple 41 (Stripe) error: {str(e)}"


@mcp.tool()
async def stripe_get(endpoint: str, params: str = "") -> str:
    """
    Make a GET request to Stripe API.
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
async def stripe_post(endpoint: str, payload: str) -> str:
    """
    Make a POST request to Stripe API.
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
async def stripe_search(query: str, limit: int = 10) -> str:
    """
    Search Stripe for resources matching query.
    Args:
        query: Search query string
        limit: Maximum results to return
    Returns: Matching resources
    """
    try:
        result = await client.get("search", params={"q": query, "limit": limit, "per_page": limit})
        import json
        return f"🔍 Stripe search results for '{query}':\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ Search failed: {str(e)}\n💡 Try stripe_get() with a specific endpoint."


@mcp.tool()
async def stripe_list(resource: str = "", limit: int = 20) -> str:
    """
    List resources from Stripe.
    Args:
        resource: Resource type to list (leave empty for root resources)
        limit: Maximum results to return
    Returns: List of resources
    """
    try:
        endpoint = resource if resource else ""
        result = await client.get(endpoint, params={"limit": limit, "per_page": limit, "max_results": limit})
        import json
        return f"📋 Stripe resources:\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ List failed: {str(e)}\n💡 Try stripe_get() with a specific endpoint."


@mcp.tool()
async def stripe_create(resource: str, payload: str) -> str:
    """
    Create a new resource in Stripe.
    Args:
        resource: Resource type/endpoint to create
        payload: JSON string with resource data
    Returns: Created resource details
    """
    try:
        import json
        data = json.loads(payload)
        result = await client.post(resource, data)
        return f"✅ Created in Stripe:\n" + json.dumps(result, indent=2, ensure_ascii=False)[:2500]
    except Exception as e:
        return f"❌ Create failed: {str(e)}"


if __name__ == "__main__":
    print("🔱 Temple 41 - Stripe Guardian AWAKENING...")
    print("🏛️ Nexus Bhairava Temples | The Vikarma Team")
    mcp.run()
