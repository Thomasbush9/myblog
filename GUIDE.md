# Guide to Writing and Publishing Articles

This guide explains how to write articles, add them to your blog, and publish them.

## **Article Structure**

Articles are organized in a hierarchical structure:

```
blog/
├── research/                      # Research articles section
│   ├── post-name/                # Each post has its own directory
│   │   ├── index.qmd             # The article content (or .md)
│   │   └── images/               # Images for this post
│   │       ├── diagram1.png
│   │       └── chart2.png
│   └── another-post/
│       └── index.qmd
├── books/                        # Book reviews section
│   └── book-review-name/
│       └── index.qmd
└── about.qmd                     # About page
```

## **Creating a New Article**

### **Step 1: Create Post Directory**

For a research article:
```bash
mkdir -p research/my-article-name
```

For a book review:
```bash
mkdir -p books/my-book-review
```

### **Step 2: Create index.qmd**

Create `index.qmd` in your post directory with the following structure:

```yaml
---
title: "Your Article Title"
date: 2025-01-15                      # YYYY-MM-DD format
categories: [research, category1, category2]  # Tags for filtering
description: "Brief description"       # Optional: shows in listings
image: images/cover-image.png          # Optional: cover image
---

## Introduction

Your article content here. Use markdown formatting.

### Headers

Use # for H1, ## for H2, ### for H3, etc.

**Bold text** with double asterisks
*Italic text* with single asterisks

### Code Blocks

```python
def hello():
    print("Hello, world!")
```

### Links

[Link text](https://example.com)

### Images

Place images in the `images/` subdirectory and reference them like:

```markdown
![Image description](images/diagram.png)
```

For the cover image (shown in listings), use the `image:` field in the frontmatter.
```

### **Step 3: Add Images (Optional)**

If your article has images:

```bash
mkdir research/my-article-name/images
# Copy your images to this directory
cp ~/path/to/image.png research/my-article-name/images/
```

Reference images in your article:
```markdown
![Architecture diagram](images/architecture.png){width=80%}
```

## **Categories and Tags**

Categories are used for filtering on section pages. Use relevant tags like:

- `research` - always include for research posts
- `attention`, `transformers`, `nlp` - topic-specific
- `ml-basics`, `tutorial` - educational content
- `deep-learning`, `pytorch`, `tensorflow` - technology-specific
- `books` - always include for book reviews
- Plus any custom tags relevant to your content

Examples:
```yaml
categories: [research, attention, deep-learning]
categories: [books, ai, neuroscience]
categories: [research, ml-basics, tutorial]
```

## **Building the Site**

After creating or editing articles, rebuild the site:

```bash
# Build the site
python3 build_simple.py

# Start local server to preview
cd _site
python3 -m http.server 8000

# Open http://localhost:8000 in your browser
```

## **Publishing to GitHub Pages**

### **Method 1: Manual Upload**

1. Build the site:
   ```bash
   python3 build_simple.py
   ```

2. Push the `_site/` directory to GitHub:
   ```bash
   git add _site/
   git commit -m "Update website"
   git push origin main
   ```

3. Enable GitHub Pages:
   - Go to repository Settings > Pages
   - Set source to "Deploy from a branch"
   - Set branch to `main` and folder to `/ (root)`
   - Save

### **Method 2: Automated with GitHub Actions**

Create `.github/workflows/publish.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Build site
      run: |
        python3 build_simple.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_site
```

## **Article Templates**

### **Research Article Template**

```yaml
---
title: "Your Research Article Title"
date: 2025-01-15
categories: [research, your-topic, sub-topic]
description: "Brief summary of what this article covers"
image: images/cover-image.png
---

## Introduction

Explain what you're going to discuss and why it matters.

## Background

Provide context and prerequisite knowledge.

## Main Content

Your detailed analysis, explanation, or tutorial.

## Code Examples (if applicable)

```python
# Your code here
def example():
    pass
```

## Conclusion

Summarize key points and next steps.

## References

- [Link to paper/resource](https://example.com)
- [Another resource](https://example.org)
```

### **Book Review Template**

```yaml
---
title: "Book Title by Author"
date: 2025-01-15
categories: [books, genre, topic]
description: "My review and key takeaways from this book"
image: images/book-cover.jpg
---

## Overview

Title, author, publication year, and brief synopsis.

## Key Themes

Main ideas explored in the book.

## What I Learned

Personal takeaways and insights.

## Who Should Read This

Target audience and recommendations.

## Rating

⭐⭐⭐⭐☆ (4/5) - Brief justification
```

## **Common Issues and Solutions**

### **Images not showing**
- Ensure images are in the `images/` subdirectory
- Check the path in your markdown: `![alt](images/filename.png)`
- Verify the image file exists
- Rebuild the site: `python3 build_simple.py`

### **Categories not appearing**
- Include `categories:` in the YAML frontmatter
- Use brackets: `categories: [cat1, cat2]` not `categories: cat1, cat2`
- Ensure proper YAML indentation

### **Build errors**
- Check Python version: `python3 --version` (needs 3.6+)
- Verify file encoding is UTF-8
- Check for proper YAML frontmatter format with `---` delimiters

### **Post not showing in listings**
- Ensure it's in a section directory (research/ or books/)
- Check that it's in a subdirectory with `index.qmd`
- Verify the frontmatter has a `title:` field
- Make sure it's not a section index (not named "Research" or "Books")

## **Tips for Good Articles**

1. **Write clear titles**: Make it obvious what the article is about
2. **Use descriptive categories**: Tags help readers find related content
3. **Add a cover image**: Makes listings more visually appealing
4. **Include a description**: Helps readers decide if they want to read
5. **Use headers**: Break up content with H2, H3 for readability
6. **Show code examples**: Working code makes tutorials more useful
7. **Link to resources**: Cite papers, documentation, and related work
8. **Use images wisely**: Diagrams and screenshots clarify complex ideas

## **File Formats**

Supported file extensions:
- `.qmd` - Quarto markdown (recommended, same as .md for our generator)
- `.md` - Standard markdown (also works)

Both are processed the same way by the build script.

## **Directory Structure Reminder**

```
myblog/
├── build_simple.py         # Site generator
├── styles_simple.css       # Theme styling
├── about.qmd               # About page
├── profile.jpg             # Profile image
├── cv/
│   └── ThomasBush_CV.pdf
├── research/               # Research posts
│   ├── post-1/
│   │   ├── index.qmd
│   │   └── images/
│   └── post-2/
│       └── index.qmd
└── books/                  # Book reviews
    └── book-1/
        └── index.qmd
```

## **Quick Reference**

### **Commands**
```bash
# Build site
python3 build_simple.py

# Preview locally
cd _site && python3 -m http.server 8000

# Create new research post
mkdir -p research/my-post/images
touch research/my-post/index.qmd

# Create new book review
mkdir -p books/my-review
touch books/my-review/index.qmd
```

### **Frontmatter Fields**
```yaml
---
title: title: "Your Title"           # Required
date: 2025-01-15              # Required: YYYY-MM-DD
categories: [tag1, tag2]      # Required for filtering
description: "..."            # Optional: shown in listings
image: images/cover.png        # Optional: cover image
---
```

Happy writing!
