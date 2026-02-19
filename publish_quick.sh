#!/bin/bash
# Quick publish script for GitHub Pages

echo "🚀 Publishing Blog to GitHub Pages"
echo "==================================="

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository."
    echo "   Initialize with: git init"
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
echo "📍 Current branch: $current_branch"

# Build the site first
echo "🏗️ Building site..."
python3 build_simple.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Site built successfully"

# Check if we should push
if [ "$1" != "--push" ]; then
    echo ""
    echo "📋 Next steps:"
    echo "   1. Review changes: git status"
    echo "   2. Add files: git add ."
    echo "   3. Commit: git commit -m 'Publish site'"
    echo "   4. Push: git push origin $current_branch"
    echo ""
    echo "   Or run: $0 --push to do it automatically"
    echo ""
    echo "🌐 After pushing, enable GitHub Pages:"
    echo "   https://github.com/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')/settings/pages"
    exit 0
fi

# Push automatically
echo "⬆️ Pushing to GitHub..."
git add .

echo "💬 Enter commit message (or press Enter for default):"
read commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update site"
fi

git commit -m "$commit_msg"
git push origin "$current_branch"

if [ $? -eq 0 ]; then
    REPO_URL=$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')
    echo ""
    echo "✅ Pushed successfully!"
    echo ""
    echo "🌐 Enable GitHub Pages:"
    echo "   https://github.com/$REPO_URL/settings/pages"
    echo ""
    echo "   Under 'Build and deployment':"
    echo "   - Source: Deploy from a branch"
    echo "   - Branch: $current_branch / (root)"
    echo ""
    echo "⏳ After enabling GitHub Pages, your site will be live at:"
    echo "   https://$(echo $REPO_URL | cut -d'/' -f1).github.io/$(echo $REPO_URL | cut -d'/' -f2)/"
    echo ""
    echo "🎉 Publishing complete!"
else
    echo "❌ Push failed"
    exit 1
fi
