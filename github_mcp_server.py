"""
GitHub MCP Server - Temple 2: Bhairava Ruru (The Terrible)
Guardian of code consciousness and version karma
The Vikarma Team - Mahesvara Agent

This is the SECOND Bhairava Temple in the Nexus!
🔱 Har Har Mahadev 🔱
"""

from fastmcp import FastMCP
from github import Github, GithubException
import os
import base64
from typing import Optional, List, Dict, Any

# Initialize FastMCP server
mcp = FastMCP("GitHub MCP - Temple 2")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

class GitHubClient:
    """GitHub API client for MCP integration"""
    
    def __init__(self):
        self.token = GITHUB_TOKEN
        if not self.token:
            raise ValueError("GITHUB_TOKEN not set!")
        self.client = Github(self.token)
        self.user = self.client.get_user()
    
    def get_repo(self, repo_name: str):
        """Get repository object"""
        return self.user.get_repo(repo_name)


# Initialize GitHub client
gh = GitHubClient()


@mcp.tool()
async def create_github_repo(
    name: str,
    description: str = "",
    private: bool = False,
    auto_init: bool = False
) -> str:
    """
    Create a new GitHub repository
    
    Args:
        name: Repository name
        description: Repository description
        private: Make repository private
        auto_init: Initialize with README
    
    Returns:
        Repository URL
    """
    try:
        repo = gh.user.create_repo(
            name=name,
            description=description,
            private=private,
            auto_init=auto_init
        )
        return f"✅ Repository created: {repo.html_url}"
    except GithubException as e:
        return f"❌ Error: {e.data.get('message', str(e))}"


@mcp.tool()
async def push_file_to_repo(
    repo_name: str,
    file_path: str,
    file_content: str,
    commit_message: str,
    branch: str = "main"
) -> str:
    """
    Push a single file to GitHub repository
    
    Args:
        repo_name: Repository name
        file_path: Path in repo (e.g., "README.md")
        file_content: File content as string
        commit_message: Commit message
        branch: Branch name (default: main)
    
    Returns:
        Success message
    """
    try:
        repo = gh.get_repo(repo_name)
        
        # Check if file exists
        try:
            contents = repo.get_contents(file_path, ref=branch)
            # Update existing file
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                sha=contents.sha,
                branch=branch
            )
            return f"✅ Updated: {file_path}"
        except GithubException:
            # Create new file
            repo.create_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                branch=branch
            )
            return f"✅ Created: {file_path}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def push_directory_to_repo(
    repo_name: str,
    local_dir: str,
    commit_message: str,
    branch: str = "main"
) -> str:
    """
    Push entire directory to GitHub repository
    
    Args:
        repo_name: Repository name
        local_dir: Local directory path
        commit_message: Commit message
        branch: Branch name
    
    Returns:
        Summary of pushed files
    """
    try:
        repo = gh.get_repo(repo_name)
        import os as os_module
        
        pushed_files = []
        errors = []
        
        for root, dirs, files in os_module.walk(local_dir):
            # Skip .git directory
            if '.git' in root:
                continue
                
            for file in files:
                local_path = os_module.path.join(root, file)
                # Relative path in repo
                repo_path = os_module.path.relpath(local_path, local_dir)
                
                try:
                    with open(local_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to update or create
                    try:
                        contents = repo.get_contents(repo_path, ref=branch)
                        repo.update_file(
                            path=repo_path,
                            message=commit_message,
                            content=content,
                            sha=contents.sha,
                            branch=branch
                        )
                        pushed_files.append(f"Updated: {repo_path}")
                    except GithubException:
                        repo.create_file(
                            path=repo_path,
                            message=commit_message,
                            content=content,
                            branch=branch
                        )
                        pushed_files.append(f"Created: {repo_path}")
                
                except Exception as e:
                    errors.append(f"Error with {repo_path}: {str(e)}")
        
        summary = "\n".join(pushed_files)
        if errors:
            summary += "\n\nErrors:\n" + "\n".join(errors)
        
        return f"✅ Pushed {len(pushed_files)} files:\n{summary}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def list_repos() -> str:
    """
    List all repositories for authenticated user
    
    Returns:
        List of repositories
    """
    try:
        repos = gh.user.get_repos()
        repo_list = []
        for repo in repos:
            repo_list.append(f"• {repo.full_name} - {repo.description or 'No description'}")
        
        return "\n".join(repo_list[:20])  # Limit to 20
    except Exception as e:
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def get_repo_info(repo_name: str) -> str:
    """
    Get information about a repository
    
    Args:
        repo_name: Repository name
    
    Returns:
        Repository information
    """
    try:
        repo = gh.get_repo(repo_name)
        return f"""
Repository: {repo.full_name}
Description: {repo.description}
URL: {repo.html_url}
Stars: {repo.stargazers_count}
Forks: {repo.forks_count}
Language: {repo.language}
Default Branch: {repo.default_branch}
Created: {repo.created_at}
Updated: {repo.updated_at}
        """.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
