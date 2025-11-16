# QUICK REFERENCE - Jira MCP for NewZyon
**The Vikarma Team - PAI/KAN Architecture**

## 📦 What We Built Together

1. **jira_mcp_server.py** - Main FastMCP server with 5 tools
2. **addon.py** - Reusable Jira API wrapper (copy for other services!)
3. **requirements.txt** - Python dependencies
4. **.env.example** - Configuration template
5. **setup.sh** - Automated setup script
6. **README.md** - Complete documentation

## 🚀 Quick Start (3 Steps)

```bash
# 1. Download all files to your NewZyon project folder
cd ~/NewZyon/mcp_servers/jira

# 2. Run setup script
bash setup.sh

# 3. Start the server
python jira_mcp_server.py
```

## 🔑 Getting Your API Token

1. Visit: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it: "NewZyon MCP"
4. Copy token to `.env` file

## 🛠️ Available Tools for Claude Sonnet 4

Once connected, your architect friend can:

```
1. search_jira_issues(jql, max_results=50)
   Example: "project = NEWZYON AND status = Open"

2. get_jira_issue(issue_key)
   Example: "NEWZYON-123"

3. create_jira_issue(project, summary, description, type, priority)
   Example: Create tasks automatically

4. add_jira_comment(issue_key, comment)
   Example: Update issues with progress

5. get_newzyon_sprint_status()
   Custom tool for The Vikarma Team!
```

## 🔄 The Addon Pattern (Your Architecture)

```python
# addon.py structure - REUSE THIS!
class JiraAddon:
    async def request(...)     # HTTP layer
    async def search_issues()  # Domain logic
    async def create_issue()   # Domain logic
    # ... more methods

# Copy this pattern for:
# - slack_addon.py
# - github_addon.py  
# - confluence_addon.py
# - [any API you want!]
```

## 🎯 Integration with Your Tools

### With acli:
```bash
# acli for admin tasks
acli jira getServerInfo

# MCP for AI automation
# Let Claude handle the logic!
```

### With Rovo:
- Use MCP to feed Rovo with Jira context
- Let Claude orchestrate both systems
- Build custom workflows

## 💡 PAI/KAN Architecture

```
PAI (Your AI System)
  └── KAN (Knowledge Augmented Network)
      ├── Jira MCP ✓ (project knowledge)
      ├── Slack MCP (team knowledge)
      ├── GitHub MCP (code knowledge)
      └── [more sources...]
```

Each addon.py = One knowledge source!

## 🤖 Connecting to Claude Sonnet 4

**Option 1: Claude Desktop** (Easiest)
Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jira-newzyon": {
      "command": "python3",
      "args": ["/full/path/to/jira_mcp_server.py"],
      "env": {
        "JIRA_BASE_URL": "https://team.atlassian.net",
        "JIRA_EMAIL": "ionutbaltag3@gmail.com",
        "JIRA_API_TOKEN": "your_token"
      }
    }
  }
}
```

**Option 2: Direct Integration**
Import the MCP server directly in your PAI code.

## 📧 Your Setup

- Email: ionutbaltag3@gmail.com
- Team: The Vikarma Team
- Project: NewZyon
- Goal: Build PAI as KAN
- Architect: Claude Sonnet 4 (your loyal friend!)
- Infrastructure Helper: Claude Sonnet 4.5 (me!)

## 🔥 Pro Tips

1. **Keep it modular**: Each addon.py = separate concern
2. **Environment vars**: Never hardcode credentials
3. **Test individually**: Run `python addon.py` to test connection
4. **Version control**: Git ignore `.env` file!
5. **Port management**: Each MCP can run on different port

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Auth failed" | Check API token and email |
| "Connection timeout" | Verify JIRA_BASE_URL format |
| "Can't import addon" | Check file location/PYTHONPATH |

## 🎓 What Makes This Special

Unlike pre-built MCPs, this gives you:
- ✅ Full API control
- ✅ Custom tools for NewZyon
- ✅ Reusable pattern (addon.py)
- ✅ No vendor lock-in
- ✅ Works with FREE APIs

As you said: *"Open a port in any app making it MCP server and connect with the addon"*

That's exactly what we built! 🎯

## 📚 Learning Resources

- FastMCP Docs: https://github.com/jlowin/fastmcp
- Jira API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- MCP Protocol: https://modelcontextprotocol.io/

## 🤝 We're Partners!

You mentioned we work together, not just me helping you. That's the spirit!

You bring:
- Vision (PAI/KAN architecture)
- Domain knowledge (NewZyon project)
- Strategic direction

I bring:
- Code generation
- Best practices
- Documentation

Together = Unstoppable! 💪

---

**Next Move**: Run `bash setup.sh` and let's get this connected to your architect (Sonnet 4)! 🚀

**Questions?** Just ask - we're in this together, partner! 🤝
