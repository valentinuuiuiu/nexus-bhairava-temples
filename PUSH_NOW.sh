#!/bin/bash
# Sacred Push Script - The Vikarma Team
# Tryambakam → Mahesvara Flow

echo "🕉️ PUSHING THE NEXUS TO GITHUB 🕉️"
echo "=================================="
echo ""
echo "Repository Status:"
git log --oneline | head -7
echo ""
echo "Total commits: $(git rev-list --count HEAD)"
echo "Total files: $(git ls-files | wc -l)"
echo "Total lines: $(git ls-files | xargs cat | wc -l)"
echo ""
echo "🔱 READY TO PUSH 🔱"
echo ""

# Check if already has remote
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists"
    echo "Current remote:"
    git remote -v
    echo ""
    read -p "Remove and re-add? (y/n): " REMOVE
    if [ "$REMOVE" = "y" ]; then
        git remote remove origin
        echo "✓ Removed old remote"
    fi
fi

echo ""
echo "📝 Enter your GitHub details:"
read -p "GitHub username: " GH_USER
read -p "Repository name [nexus-bhairava-temples]: " REPO_NAME
REPO_NAME=${REPO_NAME:-nexus-bhairava-temples}

echo ""
echo "🔗 Adding remote..."
git remote add origin https://github.com/$GH_USER/$REPO_NAME.git

echo "🌿 Creating main branch..."
git branch -M main

echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! The Nexus is on GitHub!"
    echo ""
    echo "🌐 View at: https://github.com/$GH_USER/$REPO_NAME"
    echo ""
    echo "🔱 Har Har Mahadev 🔱"
    echo ""
    echo "Next steps:"
    echo "1. Deploy to Hetzner VPS: bash quick_deploy.sh"
    echo "2. Configure Jira credentials: cp .env.example .env"
    echo "3. Run Temple 1: python jira_mcp_server.py"
    echo "4. Build Temple 2: cp addon.py slack_addon.py"
    echo ""
    echo "🕉️ The substrate continues... 🕉️"
else
    echo ""
    echo "❌ Push failed. Possible reasons:"
    echo "   - Repository doesn't exist on GitHub yet"
    echo "   - Need to create it at: https://github.com/new"
    echo "   - Or use GitHub CLI: gh repo create $REPO_NAME --public --source=. --push"
    echo ""
    echo "🔥 Create the repo and run this script again!"
fi
