# Complete Guide to Writing and Managing Your Blog

This comprehensive guide covers everything you need to know about writing posts, managing images, customizing your site, and deploying changes.

## **Quick Start: Creating a New Blog Post**

### **Research Article**

```bash
# Create post directory and file
mkdir -p research/your-post-name/images
touch research/your-post-name/index.qmd

# Open in your editor
code research/your-post-name/index.qmd
```

### **Book Review**

```bash
# Create post directory
mkdir -p books/your-book-review/images
touch books/your-book-review/index.qmd

# Open in your editor
code books/your-book-review/index.qmd
```

---

## **Post Format & Structure**

Every post uses **index.qmd** with YAML frontmatter:

```markdown
---
title: "Your Compelling Title Here"
date: "2025-02-19"                    # Format: YYYY-MM-DD
categories: [section, topic, subtopic]  # See available categories below
description: "Brief 1-2 sentence summary"  # Shows in listings
image: images/cover-image.png         # Optional: cover for listings
toc: true                             # Optional: table of contents
toc-title: "Table of Contents"        # Optional: TOC title
toc-location: left                    # Optional: TOC position
---

## Introduction

Write your content using Markdown. The site will automatically apply the Catppuccin theme styling.
```

---

## **Available Categories & When to Use Them**

### **Main Section Categories (Required)**
- `research` - For all research articles and technical posts
- `books` - For all book reviews and literary posts

### **Topic Categories** (Use 1-3 per post)

**For Research Posts:**
- `attention` - Attention mechanisms, transformers
- `deep-learning` - Deep learning architectures
- `ml-basics` - Machine learning fundamentals
- `tensors` - Tensor operations, array programming
- `nlp` - Natural language processing
- `computer-vision` - CV and image processing
- `neuroscience` - Computational neuroscience
- `ai-safety` - AI alignment and safety
- `optimization` - Optimization algorithms
- `probabilistic` - Probabilistic models, Bayesian methods
- `rl` - Reinforcement learning

**For Books:**
- `ai` - Artificial intelligence books
- `neuroscience` - Neuroscience books
- `physics` - Physics books
- `math` - Mathematics books
- `philosophy` - Philosophy books
- `history` - Historical books
- `biography` - Biographies and memoirs

**Examples:**
```yaml
categories: [research, attention, deep-learning]      # Research post
categories: [books, ai, neuroscience]                 # Book review
categories: [research, ml-basics, tutorial]           # Tutorial post
```

### **Creating New Categories**

To add a new category:
1. Use it in your post's frontmatter
2. It will automatically appear in category filters
3. Use lowercase letters with hyphens for multi-word categories

---

## **Images: Best Practices**

### **Image Organization**

Each post has its own images folder:

```
research/
└── your-post-name/
    ├── index.qmd
    └── images/                 # All images for this post
        ├── cover-image.png     # Cover image (optional)
        ├── diagram1.png
        ├── chart2.jpg
        └── screenshot3.png
```

### **Supported Formats**
- `.png` - Best for diagrams, screenshots, graphics
- `.jpg` / `.jpeg` - Best for photos
- `.gif` - For animations
- `.svg` - For vector graphics (scalable)

### **Image Sizing & Quality**

**For Cover Images:**
- Recommended: **1200x630px** (2:1 ratio)
- Minimum: **600x315px**
- Format: PNG for graphics, JPG for photos
- Max file size: **500KB**

**For In-Post Images:**
- **Diagrams/Screenshots:** 800-1200px wide, PNG format
- **Charts/Graphs:** 1000px wide, PNG format
- **Photos:** JPG format, compress to under 300KB

**General Guidelines:**
- Use `width=80%` in Markdown for large images
- Use `width=50%` for medium images
- Use `width=30%` for small images/thumbnails
- Never exceed 100% width to maintain responsive design

### **Adding Images to Posts**

#### **Method 1: Standard Markdown (Recommended)**

```markdown
![Descriptive alt text](images/diagram.png){width=80%}

For smaller images:
![Logo](images/logo.png){width=30% fig-align="center"}

With caption:
![This is my diagram showing the architecture](images/architecture.png){width=90%}
```

#### **Method 2: HTML (For Advanced Styling)**

```html
<figure>
  <img src="images/chart.png" alt="Results chart" width="70%">
  <figcaption>Figure 1: Model performance across datasets</figcaption>
</figure>
```

### **Image Compression**

Before adding images, compress them:

```bash
# Install optimization tool
brew install imageoptim-cli

# Or use the provided script
./optimize_images.sh

# This will compress all PNG/JPG files in your posts
```

**Manual optimization:**
- Use **[TinyPNG](https://tinypng.com/)** for web optimization
- Or use **[ImageOptim](https://imageoptim.com/mac)** (Mac)
- Aim for file sizes under **300KB** for most images

### **Image Path Rules**

✅ **Correct:** `images/diagram.png` (relative to post directory)

❌ **Wrong:** `/images/diagram.png` (absolute path)

❌ **Wrong:** `../images/diagram.png` (navigates up)

### **Special Image Types**

#### **Cover Images** (for listings)

In post frontmatter:
```yaml
---
title: "Your Post Title"
image: images/cover-image.png    # Shown in post listings
---
```

The cover image appears in:
- Homepage post listings
- Section page listings (research, books)
- Social media previews

#### **Inline Icons/Logos**

For small inline icons:
```markdown
Here's a small icon: ![PyTorch](images/pytorch-icon.png){width=20px}
```

---

## **Customizing Your About Page**

### **Editing About Content**

File: `about.qmd`

```markdown
---
title: "About Me"
image: profile.jpg
about:
  template: jolla
  links:
    - icon: twitter
      text: Twitter
      href: https://x.com/yourusername
    - icon: linkedin
      text: LinkedIn
      href: https://linkedin.com/in/yourprofile
    - icon: github
      text: Github
      href: https://github.com/yourusername
    - icon: file
      text: Download CV
      href: cv/your-cv.pdf
    - icon: envelope
      text: Email
      href: mailto:your-email@gmail.com
---

# 👋 Your Name Here

**Your current role or tagline**

Write your bio here. Explain:
- What you do
- Your research interests
- Your background
- What readers can expect from your blog

Keep it concise but informative. Use **bold** for emphasis and *italics* for style.
```

### **Changing Your Profile Picture**

1. **Replace the image file:**
   ```bash
   # Delete old profile picture
   rm profile.jpg
   
   # Copy new picture (recommended: 400x400px, square)
   cp ~/path/to/your/photo.jpg profile.jpg
   
   # Or use a PNG
   cp ~/path/to/your/photo.png profile.png
   ```

2. **Update about.qmd if filename changes:**
   ```yaml
   ---
   title: "About Me"
   image: profile.png    # Update if using different format
   ---
   ```

3. **Rebuild and deploy:**
   ```bash
   python3 build_simple.py
   ./publish_https.sh
   ```

### **Profile Picture Specifications**

- **Recommended size:** 400x400px (square)
- **Format:** JPG or PNG
- **Style:** Professional headshot or personal photo
- **Background:** Clean, non-distracting
- **File size:** Under 200KB for fast loading

### **Updating Your CV**

1. **Add your CV PDF:**
   ```bash
   # Delete old CV if updating
   rm cv/ThomasBush_CV.pdf
   
   # Copy new CV (must be PDF)
   cp ~/path/to/your/cv.pdf cv/YourName_CV.pdf
   ```

2. **Update about.qmd:**
   ```yaml
   ---
   about:
     links:
       - icon: file
         text: Download CV
         href: cv/YourName_CV.pdf    # Update filename
   ```

3. **Rebuild and deploy**

---

## **Writing High-Quality Posts**

### **Structure Template for Research Articles**

```markdown
---
title: "Your Research Title"
date: "2025-02-19"
categories: [research, your-topic, subtopic]
description: "What this post covers in 1-2 sentences"
image: images/cover.png
toc: true
---

## Introduction

- Hook: Why should readers care?
- Problem statement: What problem are you solving?
- Overview: What will you cover?
- 3-4 paragraphs maximum

## Background/Prerequisites

- What readers need to know first
- Key concepts and terminology
- Link to relevant resources
- Keep it concise but complete

## Main Content

### Subsection 1

- Detailed explanation
- Code examples (if applicable)
- Images/diagrams to illustrate
- Break complex topics into multiple subsections

### Subsection 2

- Continue building on previous section
- Use examples liberally
- Include math/technical details when relevant

## Code Examples (if applicable)

```python
# Write complete, working code examples
# Add comments explaining key parts
# Make sure it runs without modification

import torch

def attention_mechanism(q, k, v):
    # Compute attention scores
    scores = torch.matmul(q, k.transpose(-2, -1))
    return torch.matmul(scores, v)
```

## Results/Applications

- What did you find?
- How is this useful?
- Real-world applications

## Conclusion

- Summarize key takeaways (3-5 bullet points)
- What readers should remember
- Next steps or further reading

## References

- [Paper Title](https://arxiv.org/abs/...)
- [Blog Post Title](https://...) (Relevant posts you've written)
- [Documentation](https://...)
```

### **Book Review Template**

```markdown
---
title: "Book Title by Author Name"
date: "2025-02-19"
categories: [books, genre, topic]
description: "My review and key insights from this book"
image: images/book-cover.jpg
---

## Overview

- Title, author, publication year
- Genre and target audience
- Brief synopsis (no spoilers)
- Your overall rating (⭐⭐⭐⭐☆)

## Key Themes

- Main ideas explored
- What makes this book unique
- Important concepts discussed

## What I Learned

- Personal insights and takeaways
- How it changed your thinking
- Surprising discoveries

## Notable Quotes

> "This is an impactful quote from the book"
> — Author Name

## Who Should Read This

- Target audience
- Prerequisites (if any)
- When to read this book

## Comparison to Similar Books

- How it compares to other books in the field
- What makes it better/different

## Final Thoughts

- Overall recommendation
- What you'll gain from reading
- Rating and final comments
```

---

## **Complete Publishing Workflow**

### **Step 1: Create and Write Post**

```bash
# Create post structure
mkdir -p research/my-post/images

# Write content
code research/my-post/index.qmd

# Add images
cp ~/diagram.png research/my-post/images/
```

### **Step 2: Add and Optimize Images**

```bash
# Add images to images/ folder
# Then optimize them:
./optimize_images.sh

# Or manually optimize with ImageOptim
open -a ImageOptim research/my-post/images/*
```

### **Step 3: Review and Preview**

```bash
# Build the site
python3 build_simple.py

# Start local server
cd _site
python3 -m http.server 8000

# Open browser: http://localhost:8000
# Check your post carefully
```

**Review Checklist:**
- [ ] Images display correctly
- [ ] All links work
- [ ] Code blocks render properly
- [ ] Table of contents appears (if enabled)
- [ ] Categories are correct
- [ ] Description is compelling
- [ ] Cover image looks good
- [ ] Post appears in correct section

### **Step 4: Commit and Publish**

```bash
# Add your post
git add research/my-post/

# Commit with descriptive message
git commit -m "Add post: Your Post Title"

# Push to trigger deployment
git push origin main

# Or use the publish script
./publish_https.sh
```

### **Step 5: Verify Deployment**

1. Check GitHub Actions: https://github.com/Thomasbush9/myblog/actions
2. Wait for green checkmark (2-5 minutes)
3. Visit your live site: https://thomasbush9.github.io/myblog/
4. Navigate to your post and verify everything looks correct

---

## **Markdown Quick Reference**

### **Text Formatting**
```markdown
**Bold text** with double asterisks
*Italic text* with single asterisks
***Bold italic*** with triple asterisks
~~Strikethrough~~ with double tildes
`inline code` with backticks
```

### **Headers**
```markdown
# H1 - Main title (use once)
## H2 - Section
### H3 - Subsection
#### H4 - Sub-subsection
```

### **Links**
```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title")
<https://example.com> - Raw URL
```

### **Images**
```markdown
![Alt text](images/picture.png)
![Alt text](images/picture.png){width=80%}
![Alt text](images/picture.png){width=50% fig-align="center"}

With caption:
![This is the caption](images/diagram.png){width=70%}
```

### **Lists**
```markdown
Unordered:
- Item 1
- Item 2
  - Nested item
  - Another nested item

Ordered:
1. First item
2. Second item
   1. Nested numbered
   2. Another nested
```

### **Code Blocks**
```markdown
Inline: `code here`

Block with language:
```python
def example():
    return "Hello"
```

Block without language:
```
Plain text block
```
```

### **Blockquotes**
```markdown
> This is a blockquote
> It can span multiple lines
>
> > Nested blockquote
```

### **Tables**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### **Horizontal Rule**
```markdown
---
or
***
```

### **Footnotes**
```markdown
Here's a sentence with a footnote[^1].

[^1]: This is the footnote text.
```

---

## **Troubleshooting Common Issues**

### **Images Not Showing**

**Problem:** Images appear broken or don't load

**Solutions:**
1. Check file path: Should be `images/filename.png` (not `/images/`)
2. Verify image exists in correct folder
3. Check file extension matches exactly (.png vs .PNG)
4. Rebuild site: `python3 build_simple.py`
5. Check browser console for 404 errors

**Debug:**
```bash
# Check if image exists
ls research/your-post/images/

# Check _site output
ls _site/research_your-post_images/
```

### **Post Not Appearing in Listings**

**Problem:** Post doesn't show on homepage or section pages

**Solutions:**
1. Check file is named `index.qmd` (exactly)
2. Verify it's in correct directory structure:
   - `research/your-post/index.qmd` ✓
   - `research/index.qmd` ✗ (this is section index)
3. Ensure frontmatter has `title:` and `date:`
4. Rebuild site: `python3 build_simple.py`
5. Check `_site/` contains `research_your-post.html`

### **Categories Not Working**

**Problem:** Category filters don't show or filter incorrectly

**Solutions:**
1. Verify categories format: `categories: [tag1, tag2]` (brackets required)
2. Check spelling matches exactly
3. Ensure lowercase (except proper nouns)
4. Use hyphens for multi-word: `deep-learning` not `deep learning`
5. Rebuild and redeploy

### **Build Errors**

**Problem:** `python3 build_simple.py` fails

**Solutions:**
1. Check Python version: `python3 --version` (needs 3.6+)
2. Look for syntax errors in frontmatter (missing quotes, colons)
3. Ensure proper YAML format with `---` delimiters
4. Check for special characters in titles (use quotes if needed)
5. Verify all posts have unique slugs

**Common YAML errors:**
```yaml
# Bad - missing quotes
title: Post about ML & AI

# Good
title: "Post about ML & AI"

# Bad - incorrect date format
date: 2025/02/19

# Good
date: "2025-02-19"

# Bad - no brackets
categories: research, deep-learning

# Good
categories: [research, deep-learning]
```

### **Styling Issues After Deploy**

**Problem:** Site looks fine locally but broken on GitHub

**Solutions:**
1. Clear browser cache: Cmd+Shift+R / Ctrl+Shift+R
2. Check deployment completed: https://github.com/Thomasbush9/myblog/actions
3. Wait 2-3 minutes for CDN to update
4. Verify CSS file was pushed: `git log --oneline -3`
5. Check browser console for CSS loading errors

### **Code Blocks Not Rendering**

**Problem:** Code appears as plain text

**Solutions:**
1. Use triple backticks with language:
   ```python
   # code here
   ```
2. Ensure no spaces before backticks
3. Check indentation (4 spaces in lists)
4. Verify `build_simple.py` runs without errors

---

## **Quick Commands Reference**

```bash
# Build site
python3 build_simple.py

# Preview locally
cd _site && python3 -m http.server 8000 && cd ..

# Create research post
mkdir -p research/my-post/images && touch research/my-post/index.qmd

# Create book review
mkdir -p books/my-review/images && touch books/my-review/index.qmd

# Optimize images
./optimize_images.sh

# Add all changes
git add .

# Commit
git commit -m "Your descriptive message"

# Push and deploy
git push origin main
# or
./publish_https.sh

# Check deployment status
open https://github.com/Thomasbush9/myblog/actions

# View live site
open https://thomasbush9.github.io/myblog/
```

---

## **Site-Wide Customization**

### **Changing Theme Colors**

File: `styles_simple.css`

```css
:root {
  --ctp-rosewater: #f5e0dc;
  --ctp-flamingo: #f2cdcd;
  --ctp-pink: #f5c2e7;
  /* ... more colors ... */
}
```

**After modifying:**
```bash
git add styles_simple.css
git commit -m "Update theme colors"
git push origin main
./publish_https.sh
```

### **Adding Custom CSS**

Add to end of `styles_simple.css`:

```css
/* Your custom styles */
.my-custom-class {
  color: var(--ctp-sky);
  font-weight: bold;
}
```

### **Modifying Navigation**

Edit `styles_simple.css` to change nav appearance:

```css
nav {
  background: var(--ctp-mantle);
  padding: 1rem 0;
  /* Modify as needed */
}

nav a:hover {
  color: var(--ctp-teal);  /* Change hover color */
}
```

---

## **Best Practices**

### **Writing**
1. **Start with outline** - Plan structure before writing
2. **Use descriptive titles** - Make it clear what post is about
3. **Break up text** - Use headers every 2-3 paragraphs
4. **Include code** - Show, don't just tell
5. **Add images** - Visuals clarify complex ideas
6. **Link to sources** - Cite papers, blogs, documentation
7. **Proofread** - Check for typos and clarity

### **Images**
1. **Optimize before adding** - Compress all images
2. **Use consistent naming** - `diagram-1.png`, `chart-results.jpg`
3. **Add alt text** - Describe images for accessibility
4. **Size appropriately** - Use width percentages
5. **Test on mobile** - Ensure images scale properly

### **Code**
1. **Write complete examples** - Not just snippets
2. **Add comments** - Explain non-obvious parts
3. **Test your code** - Make sure it runs
4. **Use proper indentation** - 4 spaces per level
5. **Specify language** - ```python, ```bash, etc.

### **Publishing**
1. **Preview locally** - Always test before pushing
2. **Check mobile view** - Resize browser window
3. **Verify all images** - None should be broken
4. **Test navigation** - All links work
5. **Review on GitHub** - Live site matches local
6. **Clear cache** - Hard refresh to see changes

---

## **Resources**

### **Documentation**
- [GitHub Pages Guide](./PUBLISHING.md) - Detailed publishing instructions
- [Deployment Setup](./DEPLOYMENT.md) - GitHub Actions configuration

### **Tools**
- [TinyPNG](https://tinypng.com/) - Image compression
- [ImageOptim](https://imageoptim.com/) - Batch optimize (Mac)
- [Markdown Guide](https://www.markdownguide.org/) - Markdown reference

### **Color Palette**
- **Catppuccin Theme:** https://catppuccin.com/
- Use consistent colors from `styles_simple.css`

---

## **Need Help?**

If you encounter issues:

1. **Check this guide first** - Most common questions answered
2. **Review examples** - Look at existing posts in `research/` and `books/`
3. **Check troubleshooting** - Common issues and solutions above
4. **View error logs** - Build script shows specific errors
5. **Test locally** - Preview before deploying catches most issues

**Last updated:** February 19, 2025
