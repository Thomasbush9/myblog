#!/bin/bash
# Publish site to GitHub Pages

echo "🚀 Publishing Blog to GitHub Pages"
echo "===================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "✗ Not in a git repository. Initialize with: git init"
    exit 1
fi

# Check if _site exists
if [ ! -d "_site" ]; then
    echo "✗ _site directory not found. Run: python3 build_simple.py"
    exit 1
fi

# Get current branch
current_branch=$(git branch --show-current)
echo "📍 Current branch: ${current_branch}"

# Get changes summary
uncommitted=$(git status --porcelain | wc -l)
if [ $uncommitted -gt 0 ]; then
    echo "${YELLOW}⚠️  You have uncommitted changes:${NC}"
    git status --short
    echo ""
    read -p "Add and commit these changes? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="Update site"
        fi
        git commit -m "$commit_msg"
    fi
fi

# Optimize images
read -p "Optimize images before publishing? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "optimize_images.sh" ]; then
        ./optimize_images.sh
    else
        echo "${YELLOW}⚠️  Image optimizer not found, skipping...${NC}"
    fi
fi

# Build site
echo ""
echo "🏗️  Building site..."
python3 build_simple.py
if [ $? -ne 0 ]; then
    echo "✗ Build failed"
    exit 1
fi
echo -e "${GREEN}✓ Site built successfully${NC}"

# Ask about pushing
echo ""
echo "Changes to be pushed:"
echo "  - _site/ (generated website)"
echo "  - Source files (markdown, images, etc.)"
echo ""
read -p "Push to GitHub? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. Site is built but not pushed."
    exit 0
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git add _site/
git add *.py *.md *.css *.sh

read -p "Enter commit message [Update site]: " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update site"
fi

git commit -m "$commit_msg"
git push origin "$current_branch"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pushed to GitHub successfully!${NC}"
else
    echo "✗ Push failed"
    exit 1
fi

# Check if GitHub Pages is enabled
echo ""
echo "📋 Next steps:"
echo "   1. Go to https://github.com/Thomasbush9/myblog/settings/pages"
echo "   2. Under 'Build and deployment', select 'Deploy from a branch'"
echo "   3. Choose branch: ${current_branch} and folder: / (root)"
echo "   4. Click Save and wait a few minutes"
echo "   5. Your site will be at: https://thomasbush9.github.io/myblog/"
echo ""
echo "To check status:"
echo "   git push origin ${current_branch}:gh-pages"

# Offer to open browser
read -p "Open browser to configure GitHub Pages? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "https://github.com/Thomasbush9/myblog/settings/pages"
fi

echo ""
echo -e "${GREEN}🎉 Publishing complete!${NC}"
