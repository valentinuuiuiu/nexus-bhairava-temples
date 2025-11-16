"""
Jira MCP Server for NewZyon Project (The Vikarma Team)
FastMCP implementation for PAI/KAN architecture
Author: Built with Claude for ionutbaltag3@gmail.com
"""

from fastmcp import FastMCP
import os
from typing import Optional, Dict, Any
import httpx

# Initialize FastMCP server
mcp = FastMCP("Jira MCP - NewZyon")

# Jira Configuration
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://your-domain.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "ionutbaltag3@gmail.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")


class JiraClient:
    """Jira API client for MCP integration"""
    
    def __init__(self):
        self.base_url = JIRA_BASE_URL
        self.email = JIRA_EMAIL
        self.token = JIRA_API_TOKEN
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _get_auth(self):
        """Return basic auth tuple for Jira API"""
        return (self.email, self.token)
    
    async def api_call(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None):
        """Generic API call handler"""
        url = f"{self.base_url}/rest/api/3/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, auth=self._get_auth(), headers=self.headers)
            elif method == "POST":
                response = await client.post(url, auth=self._get_auth(), headers=self.headers, json=data)
            elif method == "PUT":
                response = await client.put(url, auth=self._get_auth(), headers=self.headers, json=data)
            
            response.raise_for_status()
            return response.json()


# Initialize Jira client
jira = JiraClient()


@mcp.tool()
async def search_jira_issues(jql: str, max_results: int = 50) -> str:
    """
    Search Jira issues using JQL (Jira Query Language)
    
    Args:
        jql: JQL query string (e.g., "project = NEWZYON AND status = 'In Progress'")
        max_results: Maximum number of results to return (default: 50)
    
    Returns:
        JSON string with search results
    """
    try:
        endpoint = f"search?jql={jql}&maxResults={max_results}"
        results = await jira.api_call(endpoint)
        
        # Format results for readability
        issues = []
        for issue in results.get("issues", []):
            issues.append({
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
                "assignee": issue["fields"]["assignee"]["displayName"] if issue["fields"].get("assignee") else "Unassigned",
                "priority": issue["fields"]["priority"]["name"] if issue["fields"].get("priority") else "None"
            })
        
        return f"Found {len(issues)} issues:\n" + "\n".join([
            f"• {i['key']}: {i['summary']} [{i['status']}] - {i['assignee']}"
            for i in issues
        ])
    
    except Exception as e:
        return f"Error searching Jira: {str(e)}"


@mcp.tool()
async def get_jira_issue(issue_key: str) -> str:
    """
    Get detailed information about a specific Jira issue
    
    Args:
        issue_key: The issue key (e.g., "NEWZYON-123")
    
    Returns:
        Detailed issue information
    """
    try:
        endpoint = f"issue/{issue_key}"
        issue = await jira.api_call(endpoint)
        
        return f"""
Issue: {issue['key']}
Summary: {issue['fields']['summary']}
Status: {issue['fields']['status']['name']}
Priority: {issue['fields']['priority']['name'] if issue['fields'].get('priority') else 'None'}
Assignee: {issue['fields']['assignee']['displayName'] if issue['fields'].get('assignee') else 'Unassigned'}
Reporter: {issue['fields']['reporter']['displayName']}
Created: {issue['fields']['created']}
Description: {issue['fields']['description']}
        """.strip()
    
    except Exception as e:
        return f"Error retrieving issue: {str(e)}"


@mcp.tool()
async def create_jira_issue(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Task",
    priority: Optional[str] = None
) -> str:
    """
    Create a new Jira issue
    
    Args:
        project_key: Project key (e.g., "NEWZYON")
        summary: Issue title/summary
        description: Detailed description
        issue_type: Type of issue (Task, Bug, Story, etc.)
        priority: Priority level (Highest, High, Medium, Low, Lowest)
    
    Returns:
        Created issue key
    """
    try:
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        if priority:
            data["fields"]["priority"] = {"name": priority}
        
        result = await jira.api_call("issue", method="POST", data=data)
        return f"Created issue: {result['key']}"
    
    except Exception as e:
        return f"Error creating issue: {str(e)}"


@mcp.tool()
async def add_jira_comment(issue_key: str, comment: str) -> str:
    """
    Add a comment to a Jira issue
    
    Args:
        issue_key: The issue key (e.g., "NEWZYON-123")
        comment: Comment text to add
    
    Returns:
        Confirmation message
    """
    try:
        data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ]
            }
        }
        
        await jira.api_call(f"issue/{issue_key}/comment", method="POST", data=data)
        return f"Comment added to {issue_key}"
    
    except Exception as e:
        return f"Error adding comment: {str(e)}"


@mcp.tool()
async def get_newzyon_sprint_status() -> str:
    """
    Get current sprint status for NewZyon project
    Specialized tool for The Vikarma Team
    
    Returns:
        Sprint status and metrics
    """
    try:
        # Search for issues in current sprint
        jql = "project = NEWZYON AND sprint in openSprints()"
        results = await jira.api_call(f"search?jql={jql}&maxResults=100")
        
        issues = results.get("issues", [])
        total = len(issues)
        by_status = {}
        
        for issue in issues:
            status = issue["fields"]["status"]["name"]
            by_status[status] = by_status.get(status, 0) + 1
        
        status_report = "\n".join([f"• {status}: {count}" for status, count in by_status.items()])
        
        return f"""
NewZyon Sprint Status (The Vikarma Team)
========================================
Total Issues: {total}

Breakdown by Status:
{status_report}
        """.strip()
    
    except Exception as e:
        return f"Error getting sprint status: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
