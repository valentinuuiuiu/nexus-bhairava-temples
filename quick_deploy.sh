#!/bin/bash
# Quick Deploy to Hetzner VPS - The Vikarma Team
# Atlassian Space: 31/ATLAS.atlassian.net

echo "🚀 NewZyon Jira MCP - Quick VPS Deploy"
echo "======================================"
echo ""

# Get details
read -p "VPS IP/hostname: " VPS_HOST
read -p "SSH user [root]: " VPS_USER
VPS_USER=${VPS_USER:-root}
read -p "GitHub username: " GITHUB_USER

echo ""
echo "📡 Deploying to $VPS_USER@$VPS_HOST..."
echo ""

# One-liner deployment
ssh $VPS_USER@$VPS_HOST << EOF
set -e
echo "🔧 Setting up environment..."
mkdir -p ~/newzyon && cd ~/newzyon

echo "📥 Cloning repository..."
git clone https://github.com/$GITHUB_USER/newzyon-jira-mcp.git 2>/dev/null || (cd newzyon-jira-mcp && git pull)

echo "📦 Installing dependencies..."
cd newzyon-jira-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Location: ~/newzyon/newzyon-jira-mcp/"
echo ""
echo "🔑 Next steps:"
echo "   1. Configure .env file:"
echo "      cd ~/newzyon/newzyon-jira-mcp"
echo "      cp .env.example .env"
echo "      nano .env  # Add your Jira API token"
echo ""
echo "   2. Run the server:"
echo "      source venv/bin/activate"
echo "      python jira_mcp_server.py"
echo ""
echo "🌐 Shivanath-Gurunatha Network active! 🙏"
EOF

echo ""
echo "🎉 Done! SSH in and configure your .env file."
echo ""
echo "Quick SSH: ssh $VPS_USER@$VPS_HOST"
echo ""
echo "💪 The Vikarma Team - Building the future!"
