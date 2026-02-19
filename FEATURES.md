# Site Features Summary

## ✅ All Features Implemented

### 1. **Images Working** ✓
- All 11 images in attention article display correctly
- Images stored in `section_slug_images/` directories
- Markdown image syntax `![alt](images/file.png)` works
- Cover images on post pages and thumbnails on listings

### 2. **Category Filtering** ✓
- Dropdown filter on Research and Books pages
- Automatically shows categories from your posts
- Real-time filtering without page reload
- Can filter by: attention, deep-learning, ml-basics, research, tensors
- Works together with search

**How to use:** Select a category from the dropdown to filter posts instantly.

### 3. **Subcategory/Tag Filtering** ✓
- Categories act as tags/filters
- Each post can have multiple categories
- Dropdown shows all unique categories for that section
- Categories display as styled pills below post titles

### 4. **Homepage Header** ✓
- Title: "Thomas W. Bush" prominently displayed
- Description: "Research, book reviews, and thoughts on machine learning, neuroscience, and software."
- Clean, centered design matching theme

### 5. **Social Links on About** ✓
- Twitter 🐦
- LinkedIn 💼
- GitHub 🐙
- Download CV 📄
- Email ✉️
- All open in new tabs

### 6. **Post Cover Images** ✓
- Thumbnails shown on homepage listings
- Full cover images on individual post pages
- Specified via `image:` field in frontmatter
- Images copied automatically during build

### 7. **Client-Side Search** ✓
- Live filtering on homepage and section pages
- Searches titles, descriptions, and categories
- Works together with category filters
- Instant results as you type

### 8. **Clean URLs** ✓
- Simple structure: `research_attention-einsum.html`
- No nested directories for posts
- Flat structure in `_site/` directory

### 9. **Dark Catppuccin TUI Theme** ✓
- Consistent dark theme throughout
- Removed light mode toggle for simplicity
- 395 lines of clean, organized CSS
- Beautiful syntax highlighting for code

### 10. **No External Dependencies** ✓
- Pure Python 3 (no pip install needed)
- Built-in markdown and YAML parsing
- No Quarto, Jekyll, or other SSGs needed
- Simple: `python3 build_simple.py`

## 📁 Site Structure

```
blog/
├── build_simple.py              # Site generator (no dependencies!)
├── styles_simple.css            # Dark Catppuccin theme
├── about.qmd                    # About page content
├── profile.jpg                  # Profile image
├── GUIDE.md                     # Complete writing guide
├── research/                    # Research articles
│   ├── attention-einsum/       # Example: Attention article
│   │   ├── index.qmd           # Article content
│   │   └── images/             # 11 images for this article
│   └── dissection-array/       # Example: Tensors article
├── books/                       # Book reviews (empty for now)
└── _site/                       # Generated site (gitignored)
    ├── index.html              # Homepage
    ├── research.html           # Research listings with filters
    ├── books.html              # Books listings
    ├── about.html              # About page
    ├── research_*.html         # Individual post pages
    ├── search.js               # Search & filter functionality
    ├── styles.css              # Copied theme
    └── cv/
        └── ThomasBush_CV.pdf   # CV download
```

## 📝 Writing New Articles

See **GUIDE.md** for complete instructions with examples!

Quick summary:
1. Create directory: `mkdir -p research/my-post/images`
2. Create `index.qmd` with frontmatter + content
3. Add images to `images/` subdirectory
4. Run: `python3 build_simple.py`
5. Preview: `cd _site && python3 -m http.server 8000`

## 🚀 Quick Commands

```bash
# Build the site
python3 build_simple.py

# Preview locally
cd _site && python3 -m http.server 8000

# Create new research post
mkdir -p research/my-post/images
touch research/my-post/index.qmd

# Create new book review
mkdir -p books/my-review
touch books/my-review/index.qmd

# Deploy to GitHub Pages
git add _site/ && git commit -m "Update" && git push origin main
```

## 🎯 Category Filtering Demo

The Research page now has a dropdown that shows:
- All Categories
- Attention
- Deep Learning
- Ml Basics
- Research
- Tensors

Selecting one instantly filters the posts!

## 💡 Tips

- **Articles not showing?** Check they're in subdirectories with `index.qmd`, not named "Research" or "Books"
- **Images not working?** Use `![alt](images/filename.png)` syntax, place files in `images/`
- **Categories not filtering?** Make sure `categories: [tag1, tag2]` is in frontmatter
- **Build errors?** Check Python 3.6+ and UTF-8 encoding

## 🎉 What's Improved

**vs Original Quarto site:**
- ✅ No external dependencies
- ✅ Simpler URL structure
- ✅ Dark mode only (cleaner)
- ✅ Category filtering added
- ✅ Better image handling
- ✅ Faster builds
- ✅ Easier to customize

**Current Status:** Ready to use and deploy!