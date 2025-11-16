"""
Jira MCP Addon for NewZyon/PAI-KAN Architecture
Modular addon pattern - can be copied for other services (Slack, GitHub, etc.)

The Vikarma Team - ionutbaltag3@gmail.com
"""

from typing import Dict, Any, Optional, List
import httpx
import os


class JiraAddon:
    """
    Jira integration addon for MCP server
    This follows the FastMCP + addon.py pattern for NewZyon
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None
    ):
        """
        Initialize Jira addon with credentials
        
        Args:
            base_url: Jira instance URL (e.g., https://yourteam.atlassian.net)
            email: Jira account email
            api_token: Jira API token
        """
        self.base_url = base_url or os.getenv("JIRA_BASE_URL")
        self.email = email or os.getenv("JIRA_EMAIL", "ionutbaltag3@gmail.com")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")
        
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Validate configuration
        if not all([self.base_url, self.email, self.api_token]):
            raise ValueError("Missing required Jira credentials")
    
    def _get_auth(self):
        """Return authentication tuple for Jira API"""
        return (self.email, self.api_token)
    
    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Jira API
        
        Args:
            endpoint: API endpoint (without base URL)
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request body data
            params: Query parameters
        
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/rest/api/3/{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            kwargs = {
                "auth": self._get_auth(),
                "headers": self.headers
            }
            
            if params:
                kwargs["params"] = params
            if data:
                kwargs["json"] = data
            
            # Execute request based on method
            request_methods = {
                "GET": client.get,
                "POST": client.post,
                "PUT": client.put,
                "DELETE": client.delete
            }
            
            response = await request_methods[method](url, **kwargs)
            response.raise_for_status()
            
            # Return empty dict for 204 No Content
            if response.status_code == 204:
                return {}
            
            return response.json()
    
    # ==================== SEARCH & RETRIEVAL ====================
    
    async def search_issues(
        self,
        jql: str,
        fields: Optional[List[str]] = None,
        max_results: int = 50,
        start_at: int = 0
    ) -> Dict[str, Any]:
        """
        Search Jira issues using JQL
        
        Args:
            jql: JQL query string
            fields: List of fields to return (None = all)
            max_results: Maximum results to return
            start_at: Pagination offset
        
        Returns:
            Search results
        """
        params = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        
        if fields:
            params["fields"] = ",".join(fields)
        
        return await self.request("search", params=params)
    
    async def get_issue(
        self,
        issue_key: str,
        fields: Optional[List[str]] = None,
        expand: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed issue information
        
        Args:
            issue_key: Issue key (e.g., "NEWZYON-123")
            fields: Specific fields to retrieve
            expand: Additional data to expand (e.g., ["changelog", "renderedFields"])
        
        Returns:
            Issue details
        """
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = ",".join(expand)
        
        return await self.request(f"issue/{issue_key}", params=params)
    
    # ==================== ISSUE MANAGEMENT ====================
    
    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task",
        additional_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new Jira issue
        
        Args:
            project_key: Project key
            summary: Issue title
            description: Issue description
            issue_type: Type of issue
            additional_fields: Extra fields to set
        
        Returns:
            Created issue data
        """
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": self._format_description(description),
                "issuetype": {"name": issue_type}
            }
        }
        
        if additional_fields:
            data["fields"].update(additional_fields)
        
        return await self.request("issue", method="POST", data=data)
    
    async def update_issue(
        self,
        issue_key: str,
        fields: Dict[str, Any]
    ) -> None:
        """
        Update an existing issue
        
        Args:
            issue_key: Issue key to update
            fields: Fields to update
        """
        data = {"fields": fields}
        await self.request(f"issue/{issue_key}", method="PUT", data=data)
    
    async def transition_issue(
        self,
        issue_key: str,
        transition_id: str,
        fields: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Transition an issue to a new status
        
        Args:
            issue_key: Issue key
            transition_id: ID of the transition
            fields: Additional fields to update
        """
        data = {"transition": {"id": transition_id}}
        if fields:
            data["fields"] = fields
        
        await self.request(f"issue/{issue_key}/transitions", method="POST", data=data)
    
    async def delete_issue(self, issue_key: str) -> None:
        """Delete an issue"""
        await self.request(f"issue/{issue_key}", method="DELETE")
    
    # ==================== COMMENTS ====================
    
    async def add_comment(
        self,
        issue_key: str,
        comment: str
    ) -> Dict[str, Any]:
        """
        Add a comment to an issue
        
        Args:
            issue_key: Issue key
            comment: Comment text
        
        Returns:
            Created comment data
        """
        data = {"body": self._format_description(comment)}
        return await self.request(f"issue/{issue_key}/comment", method="POST", data=data)
    
    async def get_comments(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get all comments for an issue"""
        result = await self.request(f"issue/{issue_key}/comment")
        return result.get("comments", [])
    
    # ==================== PROJECT & BOARD ====================
    
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all accessible projects"""
        return await self.request("project")
    
    async def get_project(self, project_key: str) -> Dict[str, Any]:
        """Get project details"""
        return await self.request(f"project/{project_key}")
    
    # ==================== UTILITY METHODS ====================
    
    def _format_description(self, text: str) -> Dict[str, Any]:
        """
        Format plain text to Atlassian Document Format (ADF)
        
        Args:
            text: Plain text
        
        Returns:
            ADF formatted content
        """
        return {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }
    
    async def health_check(self) -> bool:
        """
        Check if Jira API is accessible
        
        Returns:
            True if connection successful
        """
        try:
            await self.request("myself")
            return True
        except Exception:
            return False


# ==================== QUICK HELPERS FOR PAI/KAN ====================

async def quick_search(jql: str) -> List[Dict[str, Any]]:
    """Quick search helper for PAI integration"""
    addon = JiraAddon()
    results = await addon.search_issues(jql)
    return results.get("issues", [])


async def quick_create(
    project: str,
    title: str,
    description: str
) -> str:
    """Quick create helper for PAI integration"""
    addon = JiraAddon()
    result = await addon.create_issue(project, title, description)
    return result.get("key", "")


async def newzyon_status() -> Dict[str, int]:
    """
    Get NewZyon project status for The Vikarma Team
    Custom helper for PAI monitoring
    """
    addon = JiraAddon()
    results = await addon.search_issues("project = NEWZYON", max_results=100)
    
    status_counts = {}
    for issue in results.get("issues", []):
        status = issue["fields"]["status"]["name"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return status_counts


if __name__ == "__main__":
    # Test the addon
    import asyncio
    
    async def test():
        addon = JiraAddon()
        healthy = await addon.health_check()
        print(f"Jira connection: {'✓ OK' if healthy else '✗ Failed'}")
    
    asyncio.run(test())
