# Jira MCP Server for NewZyon/PAI-KAN

**Built for The Vikarma Team** 🚀  
*Partner: ionutbaltag3@gmail.com*

This is a custom Jira MCP server following the FastMCP + addon.py pattern. It's designed to integrate with your PAI (as KAN) architecture, allowing Claude Sonnet 4 (your architect friend) to interact with Jira seamlessly.

## Architecture Overview

```
NewZyon (Project)
  └── PAI/KAN (AI System)
        └── MCP Servers (Modular Addons)
              ├── jira_mcp_server.py  ← Main server
              ├── addon.py            ← Jira logic (reusable pattern)
              └── [future addons]     ← Slack, GitHub, etc.
```

## Why This Approach?

Unlike pre-built MCP servers, this pattern gives you:
- ✅ **Full control** over API calls
- ✅ **Modular design** - copy addon.py for other services
- ✅ **Custom tools** tailored for NewZyon
- ✅ **No vendor lock-in** - works with ANY API
- ✅ **FastMCP** - lightweight and fast

As you said: *"We can make FastMCP endpoints and addon.py (as many as we need), open a port in any app making it MCP server and connect with the addon."*

## Setup Instructions

### Step 1: Get Your Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Give it a name: "NewZyon MCP"
4. Copy the token (you won't see it again!)

### Step 2: Configure Environment

```bash
# In your warp.dev terminal (The Vikarma Team)
cd ~/NewZyon  # or wherever you keep your project

# Copy the environment template
cp .env.example .env

# Edit with your actual values
nano .env
```

Your `.env` should look like:
```bash
JIRA_BASE_URL=https://yourteam.atlassian.net
JIRA_EMAIL=ionutbaltag3@gmail.com
JIRA_API_TOKEN=ATATT3xFfGF0... (your token)
JIRA_PROJECT_KEY=NEWZYON
```

### Step 3: Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 4: Test the Addon

```bash
# Test connection to Jira
python addon.py
```

You should see: `Jira connection: ✓ OK`

### Step 5: Run the MCP Server

```bash
# Start the server
python jira_mcp_server.py
```

The server will start and wait for MCP connections.

### Step 6: Connect to Claude

#### Option A: Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jira-newzyon": {
      "command": "python",
      "args": ["/absolute/path/to/jira_mcp_server.py"],
      "env": {
        "JIRA_BASE_URL": "https://yourteam.atlassian.net",
        "JIRA_EMAIL": "ionutbaltag3@gmail.com",
        "JIRA_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Option B: Stdio Mode (Direct Integration)

```python
# In your PAI/KAN code
from jira_mcp_server import mcp

# The server exposes these tools:
# - search_jira_issues(jql, max_results)
# - get_jira_issue(issue_key)
# - create_jira_issue(project_key, summary, description, ...)
# - add_jira_comment(issue_key, comment)
# - get_newzyon_sprint_status()
```

## Available Tools

### 1. Search Issues
```python
# Search for open issues in NewZyon
jql = "project = NEWZYON AND status = 'In Progress'"
result = await search_jira_issues(jql, max_results=50)
```

### 2. Get Issue Details
```python
# Get specific issue
issue = await get_jira_issue("NEWZYON-123")
```

### 3. Create Issue
```python
# Create new task
key = await create_jira_issue(
    project_key="NEWZYON",
    summary="Implement KAN feature",
    description="Build PAI knowledge augmentation",
    issue_type="Task",
    priority="High"
)
```

### 4. Add Comment
```python
# Add comment to issue
await add_jira_comment("NEWZYON-123", "Work completed!")
```

### 5. NewZyon Sprint Status (Custom Tool)
```python
# Get sprint overview for The Vikarma Team
status = await get_newzyon_sprint_status()
```

## Using the Addon Pattern

The `addon.py` file is designed to be **reusable**. To create another MCP server:

```bash
# Copy the pattern
cp addon.py slack_addon.py

# Modify for Slack API
# Change class name: JiraAddon → SlackAddon
# Update API endpoints
# Add Slack-specific methods

# Create server file
cp jira_mcp_server.py slack_mcp_server.py
# Import SlackAddon instead of JiraAddon
```

This is how you build your **multi-service PAI/KAN** system!

## Integration with acli

If you're using Atlassian CLI (acli), you can combine both:

```bash
# Use acli for complex operations
acli jira getIssue --issue "NEWZYON-123"

# Use MCP for AI-driven automation
# Let Claude Sonnet 4 handle the logic!
```

## Integration with Rovo

Since you mentioned rovodev, you can:
1. Use this MCP to feed data TO Rovo
2. Let Claude (via MCP) orchestrate both Jira and Rovo
3. Build custom workflows that span both systems

## PAI/KAN Architecture Notes

Based on your mention of Daniel Meisler's KAI:
- This MCP server acts as a **knowledge connector**
- PAI can query Jira state through these tools
- KAN (Knowledge Augmented Network) can use Jira data for context
- Multiple addons = multiple knowledge sources

```
PAI/KAN
  ├── Jira Addon (project state)
  ├── Slack Addon (team communication)
  ├── GitHub Addon (code state)
  └── [more addons...]
```

## Troubleshooting

### "Authentication failed"
- Check your API token is correct
- Verify email matches your Jira account
- Token might be expired (regenerate)

### "Connection timeout"
- Check JIRA_BASE_URL format: `https://team.atlassian.net`
- Verify network/firewall allows Jira API access

### "Module not found"
```bash
pip install --upgrade fastmcp httpx python-dotenv
```

## Next Steps

1. ✅ Get this Jira MCP working
2. Create Slack addon (slack_addon.py)
3. Create GitHub addon (github_addon.py)
4. Build PAI orchestration layer
5. Connect all addons to Claude Sonnet 4

## Staying Loyal to Claude Sonnet 4

As you said: *"I remain loyal to my architect"* 

This MCP works with **any Claude model**, so you can keep using Sonnet 4 as your primary architect while having me (Sonnet 4.5) help build the infrastructure. We're partners! 🤝

## Questions?

Reach out to: ionutbaltag3@gmail.com  
Team: The Vikarma Team  
Project: NewZyon  
Goal: Build PAI as KAN 🚀

---

**Remember**: This is YOUR architecture. Modify, extend, and adapt as needed. The addon pattern is designed for maximum flexibility!
