#!/bin/bash
# Enhanced publish script with HTTPS support info

echo "🚀 Publishing Blog to GitHub Pages with HTTPS"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository."
    echo ""
    echo "To initialize:"
    echo "  1. git init"
    echo "  2. git add ."
    echo "  3. git commit -m 'Initial commit'"
    echo "  4. Create repo on GitHub"
    echo "  5. git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "  6. git push -u origin main"
    exit 1
fi

# Check if _site exists
if [ ! -d "_site" ]; then
    echo "❌ _site directory not found."
    echo "   Build first with: python3 build_simple.py"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo "🔍 Checking repository status..."

# Get current branch
current_branch=$(git branch --show-current)
echo "📍 Current branch: ${current_branch}"

# Get remote URL
remote_url=$(git remote get-url origin 2>/dev/null || echo "")
if [ -n "$remote_url" ]; then
    repo_name=$(echo "$remote_url" | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')
    echo "🌐 Repository: $repo_name"
else
    echo "⚠️  No remote repository configured"
fi

# Build the site
echo ""
echo "🏗️ Building site..."
python3 build_simple.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Site built successfully"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📋 Uncommitted changes found:"
    git status --short
    echo ""
    
    read -p "Add and commit these changes? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        
        # Get commit message
        default_msg="Update site $(date '+%Y-%m-%d %H:%M')"
        read -p "Commit message [$default_msg]: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg=$default_msg
        fi
        
        git commit -m "$commit_msg"
        echo "✅ Committed"
    else
        echo "⚠️  Skipping commit"
    fi
fi

# Push if we have commits
echo ""
if git log --oneline -1 > /dev/null 2>&1; then
    if [ -n "$remote_url" ]; then
        echo "⬆️ Pushing to GitHub..."
        git push origin "$current_branch"
        
        if [ $? -eq 0 ]; then
            echo "✅ Pushed successfully!"
            echo ""
            echo "${YELLOW}IMPORTANT: Enable GitHub Pages${NC}"
            echo ""
            echo "1. Go to: ${BLUE}https://github.com/$repo_name/settings/pages${NC}"
            echo "2. Under 'Build and deployment', select:"
            echo "   • Source: 'Deploy from a branch'"
            echo "   • Branch: '$current_branch'"
            echo "   • Folder: '/ (root)'"
            echo "3. Click 'Save'"
            echo ""
            echo "⏰ Wait 30-60 seconds for GitHub Pages to deploy..."
            echo ""
            echo "${GREEN}✨ YOUR SITE WILL BE LIVE AT:${NC}"
            echo "${BLUE}https://thomasbush9.github.io/myblog/${NC}"
            echo ""
            echo "${GREEN}🔒 WITH AUTOMATIC HTTPS!${NC}"
            echo ""
            echo "ℹ️  GitHub Pages automatically provides:" 
            echo "   • Free HTTPS certificate"
            echo "   • Automatic renewal"
            echo "   • Secure connection (no manual setup needed)"
        else
            echo "❌ Push failed"
            exit 1
        fi
    else
        echo "⚠️  No remote repository configured"
        echo "   Please configure remote and push manually"
    fi
else
    echo "⚠️  No commits to push"
fi

# Offer to open in browser
if [ -n "$(which open)" ]; then
    read -p "Open the Pages settings in browser? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "https://github.com/$repo_name/settings/pages"
    fi
fi

echo ""
echo "${GREEN}🎉 Publishing process complete!${NC}"
echo ""
echo "📖 After enabling GitHub Pages:"
echo "   • Your site will be live within 60 seconds"
echo "   • HTTPS is automatically enabled"
echo "   • No certificate management needed"
echo "   • Auto-renewal handled by GitHub"
echo ""
echo "📚 Documentation: https://docs.github.com/en/pages"
