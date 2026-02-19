# Fix for GitHub Pages Deployment

## Problem
Your `_site/` directory is in `.gitignore`, so GitHub Pages can't see your built site.

## Solution: GitHub Actions

We've set up GitHub Actions to automatically build and deploy your site.

## How It Works

1. **On every push to main**: GitHub Actions runs `build_simple.py`
2. **Builds your site**: Creates fresh `_site/` directory
3. **Deploys automatically**: Pushes to GitHub Pages
4. **HTTPS enabled**: Automatic SSL certificate

## Setup Steps

### 1. Commit the workflow
```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment"
git push origin main
```

### 2. Enable GitHub Pages (one-time)
1. Go to: https://github.com/Thomasbush9/myblog/settings/pages
2. Under "Build and deployment":
   - **Source**: "GitHub Actions"
3. Click **Save**

### 3. Wait 2-3 minutes
The workflow will run automatically and deploy your site.

### 4. Access your site
Your site will be at: https://thomasbush9.github.io/myblog/

## How to Publish Updates

Simply push to main:
```bash
# Make your changes
git add .
git commit -m "Update article"
git push origin main
```

GitHub Actions will automatically:
- Build the site
- Deploy to Pages
- Update HTTPS certificate if needed

## Monitoring Deployments

Check deployment status:
1. Go to Actions tab: https://github.com/Thomasbush9/myblog/actions
2. See "Build and Deploy to GitHub Pages" workflow
3. Green checkmark = deployed successfully

## Benefits

✅ Always see latest version
✅ No need to commit _site/
✅ Automatic HTTPS
✅ Clean repository
✅ Easy updates

## Troubleshooting

### Site not updating
1. Check Actions tab for build errors
2. Verify workflow ran successfully
3. Clear browser cache (Ctrl+Shift+R)
4. Wait 2-3 minutes for deployment

### Workflow failing
1. Check Python version in workflow (3.10)
2. Verify build_simple.py has no errors
3. Check Actions logs for specific errors

### Still showing old version
1. Go to Actions tab
2. Cancel any in-progress workflows
3. Re-run the latest workflow
4. Wait for completion
