# Publishing Your Blog to GitHub Pages

This guide explains how to publish your blog with **automatic HTTPS** for free.

## 🌐 HTTPS - Yes, It's Automatic!

**Good news**: GitHub Pages provides HTTPS automatically for all sites:
- ✅ Free SSL certificate
- ✅ Automatic setup (no manual configuration)
- ✅ Automatic renewal
- ✅ Secure by default
- ✅ Works with custom domains too

You don't need to do anything special for HTTPS - it's enabled automatically when you activate GitHub Pages.

## 📋 Prerequisites

1. **Git repository initialized**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **GitHub repository created**
   - Go to github.com and create a new repository
   - Name it (e.g., `myblog`)

3. **Site built**
   ```bash
   python3 build_simple.py
   ```

## 🚀 Quick Publish (Recommended)

Use the automated script:

```bash
chmod +x publish_https.sh
./publish_https.sh
```

The script will:
1. Build your site
2. Commit changes
3. Push to GitHub
4. Show you exactly where to enable GitHub Pages
5. Provide your HTTPS URL

## 📖 Manual Publishing Steps

If you prefer manual control:

### 1. Build the Site
```bash
python3 build_simple.py
```

### 2. Commit Your Changes
```bash
git add .
git commit -m "Publish updated site"
```

### 3. Push to GitHub
```bash
git push origin main  # or your branch name
```

### 4. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** > **Pages** (in the left sidebar)
3. Under "Build and deployment", select:
   - **Source**: "Deploy from a branch"
   - **Branch**: `main` (or your branch)
   - **Folder**: `/ (root)`
4. Click **Save**

### 5. Wait for Deployment

- Deployment takes 30-60 seconds
- You'll see a green checkmark when it's live
- GitHub sends you an email when it's ready

### 6. Access Your Site

Your site will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

For you specifically:
```
https://thomasbush9.github.io/myblog/
```

**Note**: HTTPS is automatic - no setup needed!

## 📂 What Gets Published

The `_site/` directory contains your complete website:
- `index.html` - Homepage
- `research.html` - Research articles
- `books.html` - Book reviews
- `about.html` - About page
- `styles.css` - Catppuccin theme
- `search.js` - Search functionality
- `profile.jpg` - Profile image
- `cv/` - CV download
- `[section]_[slug]_images/` - Post images

## 🔄 Updating Your Site

When you make changes:

```bash
# 1. Make your changes
# 2. Rebuild
python3 build_simple.py

# 3. Commit and push
./publish_https.sh

# 4. Wait 30-60 seconds for deployment
```

## 🌐 HTTPS Details

### How HTTPS Works on GitHub Pages

GitHub Pages uses Let's Encrypt to provide free SSL certificates:
- **Issuance**: Automatic when you enable Pages
- **Renewal**: Automatic (no manual intervention)
- **Validation**: Domain verification via GitHub
- **Security**: TLS 1.2+ enforced

### Verifying HTTPS

1. Visit your site URL
2. Look for the padlock icon 🔒 in the browser
3. Click it to see certificate details
4. Should show: "Connection is secure" and GitHub as issuer

### Troubleshooting HTTPS

**If you don't see HTTPS:**
1. Check that GitHub Pages is enabled in settings
2. Ensure you're using the `username.github.io` domain or a properly configured custom domain
3. Wait a few minutes - first setup can take 5-10 minutes
4. Clear browser cache

## 🎯 Common Issues

### "Site not found" after enabling Pages
- **Solution**: Wait 5-10 minutes for first deployment
- **Check**: View deployment status in repository Actions tab

### Images not loading after publish
- **Cause**: Image paths in markdown need to be relative
- **Fix**: Use `images/filename.png` not absolute paths
- **Rebuild**: Run `python3 build_simple.py` again

### Changes not appearing
- **Cause**: Browser cache
- **Fix**: Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)

### Build errors on GitHub
- **Cause**: Missing files or incorrect paths
- **Fix**: Ensure _site is gitignored and rebuild locally first

## 📊 Publishing Best Practices

1. **Always build before publishing**
   ```bash
   python3 build_simple.py
   ```

2. **Test locally first**
   ```bash
   cd _site && python3 -m http.server 8000
   # Open http://localhost:8000 to check
   ```

3. **Optimize images if needed**
   ```bash
   ./optimize_images.sh
   ```

4. **Commit after each publish**
   - Makes rollbacks easy
   - Tracks your publishing history
   - Shows site evolution over time

## 🔗 Your Site URLs

### Default URLs
- **Repository**: https://github.com/Thomasbush9/myblog
- **Site**: https://thomasbush9.github.io/myblog/
- **Settings**: https://github.com/Thomasbush9/myblog/settings/pages

### After Publishing
Your site will be available at the HTTPS URL within 60 seconds of pushing.

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Custom Domains with HTTPS](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)

## 🚀 Next Steps

1. Run: `./publish_https.sh`
2. Follow the prompts
3. Enable GitHub Pages in settings
4. Wait 60 seconds
5. Visit your live HTTPS site!

**Your site is secure by default - enjoy free HTTPS!** 🔒
