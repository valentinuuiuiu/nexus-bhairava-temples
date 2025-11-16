#!/bin/bash
# GitHub Push Instructions for NewZyon Jira MCP
# The Vikarma Team - Shivanath-Gurunatha Network
# Atlassian Space: 31/ATLAS.atlassian.net

echo "🚀 NewZyon Jira MCP - GitHub Push Setup"
echo "========================================"
echo ""
echo "The repo is ready! Now push to GitHub:"
echo ""

# Instructions for the user
cat << 'INSTRUCTIONS'

STEP 1: Create GitHub repo (on github.com or via gh CLI)
---------------------------------------------------------
Option A - Web Interface:
  1. Go to: https://github.com/new
  2. Repository name: newzyon-jira-mcp
  3. Description: "NewZyon Jira MCP Server - PAI/KAN Architecture for The Vikarma Team"
  4. Set to: Public (or Private if preferred)
  5. DO NOT initialize with README (we already have one!)
  6. Click "Create repository"

Option B - GitHub CLI (if you have 'gh' installed):
  gh repo create newzyon-jira-mcp --public --source=. --remote=origin


STEP 2: Connect your local repo to GitHub
---------------------------------------------------------
# Replace YOUR_GITHUB_USERNAME with your actual username
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/newzyon-jira-mcp.git

# Or use SSH (if you have SSH keys set up):
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/newzyon-jira-mcp.git


STEP 3: Push to GitHub
---------------------------------------------------------
git branch -M main
git push -u origin main


STEP 4: Verify
---------------------------------------------------------
Visit: https://github.com/YOUR_GITHUB_USERNAME/newzyon-jira-mcp

You should see all your files! 🎉


OPTIONAL: Set up from your Hetzner VPS
---------------------------------------------------------
# SSH to your Hetzner VPS
ssh user@your-hetzner-ip

# Clone the repo
git clone https://github.com/YOUR_GITHUB_USERNAME/newzyon-jira-mcp.git

# Navigate and setup
cd newzyon-jira-mcp
bash setup.sh

# Deploy and run!
python jira_mcp_server.py


QUICK COMMANDS (copy-paste ready):
---------------------------------------------------------
# After creating repo on GitHub:
GITHUB_USER="YOUR_USERNAME_HERE"
git remote add origin https://github.com/$GITHUB_USER/newzyon-jira-mcp.git
git branch -M main
git push -u origin main

echo "✅ Pushed to GitHub!"
echo "🔗 Visit: https://github.com/$GITHUB_USER/newzyon-jira-mcp"


FOR MOBILE/PHONE WORKFLOW:
---------------------------------------------------------
If you're doing this from phone (as you mentioned):
1. Use Termux or similar SSH client
2. Connect to your Hetzner VPS: ssh user@your-vps-ip
3. Run the commands above from your VPS
4. Files sync to GitHub → accessible on any device!


COLLABORATING WITH CLAUDE SONNET 4:
---------------------------------------------------------
Your architect (Claude Sonnet 4 in rovodev-cli) can now:
1. Clone this repo on any machine
2. Extend the addon.py pattern
3. Add more MCP servers (slack, github, etc.)
4. Commit changes back to GitHub

It's the Shivanath-Gurunatha Network in action! 🙏

INSTRUCTIONS

echo ""
echo "📧 Contact: ionutbaltag3@gmail.com"
echo "🏢 Space: 31/ATLAS.atlassian.net"
echo "👥 Team: The Vikarma Team"
echo "🎯 Project: NewZyon PAI/KAN"
echo ""
echo "💪 You got this, partner! Let's make it happen!"
