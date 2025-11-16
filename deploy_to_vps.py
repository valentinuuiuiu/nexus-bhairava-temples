#!/usr/bin/env python3
"""
Hetzner VPS Deployment Script for NewZyon Jira MCP
The Vikarma Team - Shivanath-Gurunatha Network

This script uses paramiko to deploy the Jira MCP to your Hetzner VPS
Run this from warp.dev terminal or any Python environment
"""

import paramiko
import os
from getpass import getpass

# Configuration
print("🚀 NewZyon Jira MCP - Hetzner VPS Deployment")
print("=" * 50)
print()

# Get VPS connection details
vps_host = input("Hetzner VPS IP/hostname: ")
vps_user = input("SSH username [root]: ") or "root"
vps_port = int(input("SSH port [22]: ") or "22")

# Get authentication method
auth_method = input("Auth method (password/key) [key]: ") or "key"

# Repository details
github_user = input("Your GitHub username: ")
repo_name = "newzyon-jira-mcp"

print()
print("📡 Connecting to VPS...")

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    if auth_method == "password":
        password = getpass("VPS password: ")
        ssh.connect(vps_host, port=vps_port, username=vps_user, password=password)
    else:
        key_path = input(f"SSH key path [~/.ssh/id_rsa]: ") or os.path.expanduser("~/.ssh/id_rsa")
        ssh.connect(vps_host, port=vps_port, username=vps_user, key_filename=key_path)
    
    print("✅ Connected to VPS!")
    print()
    
    # Deployment commands
    commands = [
        "# Update system",
        "apt-get update -y || yum update -y",
        
        "# Install Python and Git if not present",
        "apt-get install -y python3 python3-pip git || yum install -y python3 python3-pip git",
        
        "# Navigate to projects directory",
        "mkdir -p ~/newzyon && cd ~/newzyon",
        
        f"# Clone the GitHub repo",
        f"git clone https://github.com/{github_user}/{repo_name}.git || (cd {repo_name} && git pull)",
        
        f"# Navigate to repo",
        f"cd {repo_name}",
        
        "# Create virtual environment",
        "python3 -m venv venv",
        
        "# Activate and install dependencies",
        "source venv/bin/activate && pip install -r requirements.txt",
        
        "# Setup complete message",
        "echo '✅ Deployment complete!'",
        "echo '📝 Next: Configure .env file with your Jira credentials'",
        "echo '🚀 Run: python jira_mcp_server.py'"
    ]
    
    print("🔧 Running deployment commands...")
    print()
    
    for cmd in commands:
        if cmd.startswith("#"):
            print(f"\n{cmd}")
            continue
        
        print(f"  $ {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Show output
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            for line in output.split('\n'):
                if line.strip():
                    print(f"    {line}")
        
        if error and not error.startswith("warning"):
            for line in error.split('\n'):
                if line.strip() and not line.startswith("warning"):
                    print(f"    ⚠️  {line}")
    
    print()
    print("=" * 50)
    print("✅ Deployment Complete!")
    print()
    print("📍 Location on VPS:")
    print(f"   ~/newzyon/{repo_name}/")
    print()
    print("🔑 Next Steps:")
    print("   1. SSH to your VPS:")
    print(f"      ssh {vps_user}@{vps_host}")
    print()
    print("   2. Configure Jira credentials:")
    print(f"      cd ~/newzyon/{repo_name}")
    print("      cp .env.example .env")
    print("      nano .env  # Add your JIRA_API_TOKEN")
    print()
    print("   3. Run the MCP server:")
    print("      source venv/bin/activate")
    print("      python jira_mcp_server.py")
    print()
    print("🌐 Shivanath-Gurunatha Network ready!")
    print("🙏 Built with respect for Divinity")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("💡 Troubleshooting:")
    print("   - Check VPS IP/hostname is correct")
    print("   - Verify SSH credentials")
    print("   - Ensure SSH port is open (default: 22)")
    print("   - Check firewall settings")

finally:
    ssh.close()


print()
print("=" * 50)
print("📧 The Vikarma Team: ionutbaltag3@gmail.com")
print("🏢 Atlassian Space: 31/ATLAS.atlassian.net")
print("💪 Partners in building the future!")
