#!/usr/bin/env python3
"""
Simple static site generator for the blog
- Reads .qmd and .md files
- Converts markdown to HTML
- Generates listing pages
- Preserves Catppuccin styling
"""

import os
import re
import sys
import yaml
import shutil
from datetime import datetime
from pathlib import Path

# Try to import markdown, fallback to simple conversion if not available
try:
    import markdown

    MD = markdown.Markdown(extensions=["fenced_code", "codehilite", "tables", "meta"])
except ImportError:
    MD = None


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content"""
    frontmatter = {}
    body = content

    # Match --- yaml --- pattern
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
        except yaml.YAMLError:
            pass

    return frontmatter, body


def md_to_html(md_content):
    """Convert markdown to HTML"""
    if MD:
        return MD.reset().convert(md_content)
    else:
        # Simple fallback conversion
        # Basic formatting
        html = md_content
        html = re.sub(
            r"```([\w-]*)\n(.*?)\n```",
            r'<pre><code class="\1">\2</code></pre>',
            html,
            flags=re.DOTALL,
        )
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        html = re.sub(r"\n\n", r"</p><p>", html)
        html = re.sub(r"\n", r"<br>", html)
        html = f"<p>{html}</p>"
        return html


def get_all_posts(base_dir):
    """Get all posts from research and books directories"""
    posts = []

    for section in ["research", "books"]:
        section_dir = Path(base_dir) / section
        if not section_dir.exists():
            continue

        # Find all qmd files in subdirectories (not index.qmd)
        for post_dir in section_dir.iterdir():
            if post_dir.is_dir():
                post_file = post_dir / "index.qmd"
                if post_file.exists():
                    with open(post_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        frontmatter, body = parse_frontmatter(content)

                        # Skip if this is the section index
                        if frontmatter.get("title", "").lower() in [
                            section,
                            f"{section.capitalize()}",
                            "book reviews",
                        ]:
                            continue

                        posts.append(
                            {
                                "section": section,
                                "slug": post_dir.name,
                                "path": post_file,
                                "frontmatter": frontmatter,
                                "body": body,
                                "date": frontmatter.get("date", "2000-01-01"),
                                "title": frontmatter.get("title", post_dir.name),
                                "categories": frontmatter.get("categories", []),
                                "description": frontmatter.get("description", ""),
                            }
                        )

    # Sort by date descending
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def find_images(post_dir):
    """Find images in post directory"""
    images = []
    img_dir = post_dir / "images"

    if img_dir.exists():
        for img_file in img_dir.iterdir():
            if img_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
                images.append(img_file)

    return images


def copy_assets(base_dir, output_dir):
    """Copy CSS, JS, images, and CV"""
    output = Path(output_dir)
    base = Path(base_dir)

    # Copy CSS
    css_src = base / "styles.css"
    css_dst = output / "styles.css"
    if css_src.exists():
        shutil.copy2(css_src, css_dst)

    # Copy profile image
    profile_src = base / "profile.jpg"
    profile_dst = output / "profile.jpg"
    if profile_src.exists():
        shutil.copy2(profile_src, profile_dst)

    # Copy CV
    cv_src = base / "cv" / "ThomasBush_CV.pdf"
    cv_dst_dir = output / "cv"
    cv_dst_dir.mkdir(exist_ok=True)
    if cv_src.exists():
        shutil.copy2(cv_src, cv_dst_dir / "ThomasBush_CV.pdf")

    # Copy images from posts
    for section in ["research", "books"]:
        section_src = base / section
        if not section_src.exists():
            continue

        for post_dir in section_src.iterdir():
            if post_dir.is_dir() and (post_dir / "images").exists():
                img_src = post_dir / "images"
                img_dst = output / section / post_dir.name / "images"
                img_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(img_src, img_dst, dirs_exist_ok=True)


def generate_html_layout(title, content, page_type="post"):
    """Generate HTML page with Catppuccin styling"""

    nav_links = [
        ("index.html", "Home"),
        ("research.html", "Research"),
        ("books.html", "Books"),
        ("about.html", "About"),
    ]

    nav_html = "\n".join(
        [
            f'<li><a href="{href}" class="nav-link">{text}</a></li>'
            for href, text in nav_links
        ]
    )

    # Simple search box for posts
    search_html = ""
    if page_type in ["home", "listing"]:
        search_html = """
        <div class="search-box">
          <input type="text" id="search-input" placeholder="Search posts..." />
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/styles.css">
    <style>
        /* Simple search styling */
        .search-box {{
            margin: 2rem 0;
            text-align: center;
        }}
        .search-box input {{
            padding: 0.5rem 1rem;
            border: 1px solid var(--ctp-surface0);
            background: var(--ctp-mantle);
            color: var(--ctp-text);
            border-radius: 4px;
            font-family: inherit;
        }}
        .post-item {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--ctp-surface0);
        }}
        .post-title {{
            margin-bottom: 0.5rem;
        }}
        .post-meta {{
            color: var(--ctp-subtext0);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        .post-categories {{
            display: inline;
        }}
        .post-categories span {{
            display: inline-block;
            background: var(--ctp-surface0);
            color: var(--ctp-subtext1);
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
        }}
        .post-description {{
            color: var(--ctp-text);
            margin-top: 0.5rem;
        }}
        nav {{
            background: var(--ctp-mantle);
            padding: 1rem 0;
            margin-bottom: 2rem;
        }}
        nav ul {{
            list-style: none;
            display: flex;
            gap: 2rem;
            justify-content: center;
            margin: 0;
            padding: 0;
        }}
        nav a {{
            color: var(--ctp-text);
            text-decoration: none;
            font-weight: 500;
        }}
        nav a:hover {{
            color: var(--ctp-sky);
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        .about-profile {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .about-profile img {{
            border-radius: 50%;
            width: 200px;
            height: 200px;
            object-fit: cover;
        }}
        .social-links {{
            text-align: center;
            margin-top: 2rem;
        }}
        .social-links a {{
            display: inline-block;
            margin: 0 1rem;
            color: var(--ctp-sky);
            text-decoration: none;
        }}
        pre {{
            background: var(--ctp-mantle);
            border: 1px solid var(--ctp-surface0);
            border-radius: 4px;
            padding: 1rem;
            overflow-x: auto;
        }}
        code {{
            background: var(--ctp-surface0);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: var(--ctp-lavender);
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        a {{
            color: var(--ctp-sky);
        }}
        a:hover {{
            color: var(--ctp-teal);
        }}
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container">
            <ul>
                {nav_html}
            </ul>
        </div>
    </nav>
    
    <div class="container">
        {search_html}
        <main>
            {content}
        </main>
    </div>
    
    <script src="/search.js"></script>
</body>
</html>
"""


def generate_post_page(post, output_dir):
    """Generate individual post page"""
    html_content = md_to_html(post["body"])

    # Update image paths in content
    html_content = html_content.replace(
        "images/", f"/{post['section']}/{post['slug']}/images/"
    )

    page_title = f"{post['title']} - Thomas W. Bush"
    page_content = f"""
    <article>
        <h1>{post["title"]}</h1>
        <div class="post-meta">
            <time>{post["date"]}</time>
            {f' | <span class="post-categories">{", ".join(post["categories"])}</span>' if post["categories"] else ""}
        </div>
        {html_content}
    </article>
    """

    html = generate_html_layout(page_title, page_content, "post")

    # Write to output
    output_path = Path(output_dir) / f"{post['section']}_{post['slug']}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_listing(title, posts, output_path, page_type="listing"):
    """Generate a listing page"""
    posts_html = ""

    for post in posts:
        post_url = f"{post['section']}_{post['slug']}.html"
        categories_html = "".join(
            [f"<span>{cat}</span>" for cat in post["categories"][:3]]
        )  # Limit to 3

        desc_attr = post["description"].lower() if post["description"] else ""
        posts_html += (
            f'''
        <div class="post-item" data-categories="{" ".join(post["categories"])}" data-title="{post["title"].lower()}" data-description="{desc_attr}">
            <h2 class="post-title"><a href="{post_url}">{post["title"]}</a></h2>
            <div class="post-meta">
                <time>{post["date"]}</time>
            </div>
            '''
            + (
                f'<div class="post-categories">{categories_html}</div>'
                if categories_html
                else ""
            )
            + """
            """
            + (
                f'<div class="post-description">{post["description"]}</div>'
                if post["description"]
                else ""
            )
            + """
        </div>
        """
        )

    page_content = f"""
    <h1>{title}</h1>
    <div class="post-list">
        {posts_html}
    </div>
    """

    html = generate_html_layout(f"{title} - Thomas W. Bush", page_content, page_type)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_about_page(base_dir, output_dir):
    """Generate about page"""
    about_path = Path(base_dir) / "about.qmd"
    if not about_path.exists():
        return

    with open(about_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)
    html_content = md_to_html(body)

    page_content = f"""
    <article>
        <h1>{frontmatter.get("title", "About")}</h1>
        <div class="about-profile">
            <img src="/profile.jpg" alt="Profile">
        </div>
        {html_content}
    </article>
    """

    html = generate_html_layout(f"About - Thomas W. Bush", page_content, "page")

    with open(Path(output_dir) / "about.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_site(base_dir, output_dir):
    """Build the entire site"""
    base = Path(base_dir)
    output = Path(output_dir)

    # Clean and create output directory
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()

    # Copy assets
    copy_assets(base_dir, output_dir)

    # Get all posts
    posts = get_all_posts(base_dir)

    # Group posts by section
    research_posts = [p for p in posts if p["section"] == "research"]
    books_posts = [p for p in posts if p["section"] == "books"]

    # Generate individual post pages
    for post in posts:
        generate_post_page(post, output_dir)

    # Generate listing pages
    generate_listing("Recent Posts", posts, output / "index.html", "home")
    generate_listing("Research", research_posts, output / "research.html", "listing")
    generate_listing("Books", books_posts, output / "books.html", "listing")

    # Generate about page
    generate_about_page(base_dir, output_dir)

    # Generate search.js
    search_js = """
    // Simple client-side search
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;
        
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            const posts = document.querySelectorAll('.post-item');
            
            posts.forEach(post => {
                if (query === '') {
                    post.classList.remove('hidden');
                } else {
                    const title = post.getAttribute('data-title') || '';
                    const description = post.getAttribute('data-description') || '';
                    const categories = post.getAttribute('data-categories') || '';
                    
                    const match = title.includes(query) || 
                                 description.includes(query) || 
                                 categories.includes(query);
                    
                    if (match) {
                        post.classList.remove('hidden');
                    } else {
                        post.classList.add('hidden');
                    }
                }
            });
        });
    });
    """

    with open(output / "search.js", "w", encoding="utf-8") as f:
        f.write(search_js)

    print(f"Site built successfully! {len(posts)} posts generated.")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "_site")

    build_site(base_dir, output_dir)
