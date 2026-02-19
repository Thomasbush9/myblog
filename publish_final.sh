#!/bin/bash
# Publishing script for GitHub Actions deployment

echo "🚀 Publishing with GitHub Actions"
echo "=================================="

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository."
    exit 1
fi

# Check if workflow exists
if [ ! -f ".github/workflows/deploy.yml" ]; then
    echo "❌ GitHub Actions workflow not found."
    echo "   Run this first:"
    echo "   git add .github/workflows/deploy.yml"
    echo "   git commit -m 'Add deployment workflow'"
    echo "   git push origin main"
    exit 1
fi

# Get current branch
current_branch=$(git branch --show-current)
echo "📍 Current branch: $current_branch"

# Status check
echo ""
echo "📋 Repository status:"
git status --short

# Build test
echo ""
echo "🏗️ Testing build locally..."
python3 build_simple.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed - fix errors before publishing"
    exit 1
fi

echo "✅ Build successful"

# Ask to commit
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    read -p "Commit and push changes? [y/N] " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        
        default_msg="Update site $(date '+%Y-%m-%d %H:%M')"
        read -p "Commit message [$default_msg]: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg=$default_msg
        fi
        
        git commit -m "$commit_msg"
        
        echo "⬆️ Pushing to GitHub..."
        git push origin "$current_branch"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Pushed successfully!"
            echo ""
            echo "🔄 GitHub Actions workflow will start automatically"
            echo "   Check status: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')/actions"
            echo ""
            echo "⏰ Wait 2-3 minutes for deployment..."
            echo ""
            echo "🌐 Your site will be at:"
            echo "   https://$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/' | tr '/' '.').github.io/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/' | cut -d'/' -f2)/"
            echo ""
            echo "🔒 HTTPS is automatic - no setup needed!"
        else
            echo "❌ Push failed"
            exit 1
        fi
    else
        echo "⚠️  Skipping push"
    fi
else
    echo "✓ No changes to commit"
fi

# Show monitoring info
echo ""
echo "📊 To monitor deployment:"
echo "   Watch workflow: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/')/actions"
echo ""
echo "🌐 When deployment completes (checkmark appears):"
echo "   Visit: https://$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/' | tr '/' '.').github.io/$(git remote get-url origin | sed 's/.*github.com[:\/]\(.*\)\.git/\1/' | cut -d'/' -f2)/"
echo ""
echo "ℹ️  First deployment takes 2-3 minutes"
echo "   Subsequent updates take 30-60 seconds"
