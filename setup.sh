#!/bin/bash
# Quick Start Script for Jira MCP Server
# NewZyon / The Vikarma Team

echo "🚀 Jira MCP Server Setup - The Vikarma Team"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Create virtual environment
echo "📦 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "🔑 IMPORTANT: Edit .env file with your Jira credentials:"
    echo "   - JIRA_BASE_URL (your Jira instance)"
    echo "   - JIRA_EMAIL (ionutbaltag3@gmail.com or your team email)"
    echo "   - JIRA_API_TOKEN (get from https://id.atlassian.com/manage-profile/security/api-tokens)"
    echo ""
    echo "Run this script again after configuring .env"
    exit 0
fi

# Test connection
echo ""
echo "🔍 Testing Jira connection..."
python3 addon.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. Start the MCP server: python jira_mcp_server.py"
    echo "   2. Configure Claude Desktop (see README.md)"
    echo "   3. Start building PAI/KAN! 🚀"
    echo ""
    echo "💡 Tip: Keep this terminal open and run the server"
else
    echo ""
    echo "❌ Connection test failed. Please check your .env configuration."
    exit 1
fi
