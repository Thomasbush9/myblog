#!/usr/bin/env python3
"""
Simple static site generator for the blog - no external dependencies
"""

import os
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path
from html import escape


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content with nested structure support"""
    frontmatter = {}
    body = content

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = match.group(2)

        lines = yaml_text.split("\n")
        i = 0
        stack = [
            {"data": frontmatter, "indent": -1}
        ]  # Stack to track nested structures

        while i < len(lines):
            line = lines[i].rstrip()
            i += 1

            if not line or ":" not in line:
                continue

            indent = len(line) - len(line.lstrip())
            line = line.strip()

            # Pop stack until we find the right parent
            while stack and stack[-1]["indent"] >= indent:
                stack.pop()

            current = stack[-1]["data"] if stack else frontmatter

            # Handle array items (start with -)
            if line.startswith("- "):
                item = line[2:].strip()

                # If current is a dict and we're in an array context, create object
                if isinstance(current, dict) and ":" in item:
                    obj = {}
                    k, v = item.split(":", 1)
                    obj[k.strip()] = v.strip(" '\"")

                    # Collect additional properties for this object
                    while i < len(lines) and lines[i].startswith(" " * (indent + 2)):
                        sub_line = lines[i].strip()
                        if ":" in sub_line:
                            sk, sv = sub_line.split(":", 1)
                            obj[sk.strip()] = sv.strip(" '\"")
                        i += 1

                    # Add to parent's array
                    parent_key = None
                    for key, val in current.items():
                        if isinstance(val, list):
                            parent_key = key
                            break

                    if parent_key:
                        current[parent_key].append(obj)
                continue

            # Regular key: value
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Handle arrays: [item1, item2]
            if value.startswith("[") and value.endswith("]"):
                items = [
                    item.strip().strip(" '\"")
                    for item in value[1:-1].split(",")
                    if item.strip()
                ]
                current[key] = items

            # Handle nested structure (next line is indented with array items)
            elif i < len(lines) and lines[i].strip().startswith("- "):
                # This is a parent key for nested array
                current[key] = []
                stack.append({"data": {key: current[key]}, "indent": indent})

            # Handle simple value
            else:
                # If value looks like it should be nested but isn't, create nested structure
                if (
                    not value
                    and i < len(lines)
                    and (len(lines[i]) - len(lines[i].lstrip())) > indent
                ):
                    current[key] = {}
                    stack.append({"data": current[key], "indent": indent})
                else:
                    current[key] = value.strip(" '\"")

    return frontmatter, body


def md_to_html(md_content):
    """Convert markdown to simple HTML"""
    html = md_content

    # Remove Quarto column syntax
    html = re.sub(r"^:::*\s*\{[^}]*\}\s*\n?", "", html, flags=re.MULTILINE)
    html = re.sub(r"^::\+\s*\{[^}]*\}\s*\n?", "", html, flags=re.MULTILINE)
    html = re.sub(r"^:+\s*\n", "", html, flags=re.MULTILINE)

    # Protect code blocks with placeholders before processing headers
    code_blocks = []

    def save_code_block(m):
        code_blocks.append(m.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

    html = re.sub(r"```\w*.*?```", save_code_block, html, flags=re.DOTALL)

    # Inline code - also protect
    inline_codes = []

    def save_inline_code(m):
        inline_codes.append(m.group(0))
        return f"__INLINE_CODE_{len(inline_codes) - 1}__"

    html = re.sub(r"`[^`]+`", save_inline_code, html)

    # Headers (h1-h6) - strip {#id} custom anchor syntax
    for i in range(6, 0, -1):
        pattern = "^" + "#" * i + r"\s+(.+)$"

        def make_header(level):
            def replacer(m):
                text = m.group(1)
                text = re.sub(r"\s*\{#[^}]+\}\s*$", "", text)
                return f"<h{level}>{text}</h{level}>"

            return replacer

        html = re.sub(pattern, make_header(i), html, flags=re.MULTILINE)

    # Restore inline code
    for i, code in enumerate(inline_codes):
        html = html.replace(f"__INLINE_CODE_{i}__", code)

    # Restore code blocks and convert to HTML
    for i, code in enumerate(code_blocks):
        if code.startswith("```") and len(code) > 3:
            lang_match = re.match(r"```(\w+)", code)
            if lang_match:
                lang = lang_match.group(1)
                content = code[3 + len(lang) : -3]
                code_html = (
                    f'<pre><code class="language-{lang}">{escape(content)}</code></pre>'
                )
            else:
                content = code[3:-3]
                code_html = f"<pre><code>{escape(content)}</code></pre>"
        else:
            content = code[3:-3] if code.startswith("```") else code
            code_html = f"<pre><code>{escape(content)}</code></pre>"
        html = html.replace(f"__CODE_BLOCK_{i}__", code_html)

    # Bold
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)

    # Italic
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # Images ![alt](url)
    html = re.sub(
        r"!\[([^\]]*)\]\(([^\)\s]+)\)(?!\{)",
        r'<img src="\2" alt="\1" class="img-fluid" loading="lazy">',
        html,
    )
    html = re.sub(
        r"!\[([^\]]*)\]\(([^\)\s]+)\)\{[^}]*width=(\d+)%[^}]*\}",
        r'<img src="\2" alt="\1" class="img-fluid" style="width: \3%;" loading="lazy">',
        html,
    )
    html = re.sub(
        r"!\[([^\]]*)\]\(([^\)\s]+)\)\{[^}]*\}",
        r'<img src="\2" alt="\1" class="img-fluid" loading="lazy">',
        html,
    )

    # Links [text](url)
    html = re.sub(r"\[([^\]]+)\]\(([^\)\s]+)\)", r'<a href="\2">\1</a>', html)

    # Line breaks and paragraphs
    paragraphs = re.split(r"\n\s*\n", html)
    result = []
    for p in paragraphs:
        if p.strip():
            if p.strip().startswith("<h") or p.strip().startswith("<pre>"):
                result.append(p)
            else:
                p = p.replace("\n", "<br>")
                result.append(f"<p>{p}</p>")
    html = "\n".join(result)

    return html


def copy_assets(base_dir, output_dir):
    """Copy CSS, JS, images, and CV"""
    output = Path(output_dir)
    base = Path(base_dir)

    css_src_simple = base / "styles_simple.css"
    css_src = base / "styles.css"
    css_dst = output / "styles.css"

    if css_src_simple.exists():
        shutil.copy2(css_src_simple, css_dst)
    elif css_src.exists():
        shutil.copy2(css_src, css_dst)

    profile_src = base / "profile.jpg"
    profile_dst = output / "profile.jpg"
    if profile_src.exists():
        shutil.copy2(profile_src, profile_dst)

    cv_src = base / "cv" / "ThomasBush_CV.pdf"
    cv_dst_dir = output / "cv"
    cv_dst_dir.mkdir(exist_ok=True)
    if cv_src.exists():
        shutil.copy2(cv_src, cv_dst_dir / "ThomasBush_CV.pdf")

    for section in ["research", "books"]:
        section_src = base / section
        if not section_src.exists():
            continue

        for post_dir in section_src.iterdir():
            if post_dir.is_dir() and (post_dir / "images").exists():
                img_src = post_dir / "images"
                img_dst = output / f"{section}_{post_dir.name}_images"
                img_dst.mkdir(parents=True, exist_ok=True)
                for img in img_src.iterdir():
                    if img.is_file():
                        shutil.copy2(img, img_dst / img.name)


def get_all_posts(base_dir):
    """Get all posts from research and books directories"""
    posts = []

    for section in ["research", "books"]:
        section_dir = Path(base_dir) / section
        if not section_dir.exists():
            continue

        for post_dir in section_dir.iterdir():
            if post_dir.is_dir():
                post_file = post_dir / "index.qmd"
                if post_file.exists():
                    with open(post_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        frontmatter, body = parse_frontmatter(content)

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

    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


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

    search_html = ""
    if page_type in ["home", "listing"]:
        search_html = """\n        <div class="search-box">\n          <input type="text" id="search-input" placeholder="Search posts..." />\n        </div>\n        """

    return f"""<!DOCTYPE html>\n<html lang="en" data-theme="dark">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{title}</title>\n    <link rel="stylesheet" href="styles.css">\n    <style>\n        .search-box {{\n            margin: 2rem 0;\n            text-align: center;\n        }}\n        .search-box input {{\n            padding: 0.75rem 1rem;\n            border: 1px solid #45475a;\n            background: #181825;\n            color: #cdd6f4;\n            border-radius: 6px;\n            font-family: inherit;\n            width: 100%;\n            max-width: 500px;\n            font-size: 1rem;\n        }}\n        .search-box input:focus {{\n            outline: none;\n            border-color: #89dceb;\n            box-shadow: 0 0 0 2px rgba(137, 220, 235, 0.2);\n        }}\n        .post-item {{\n            display: flex;\n            flex-direction: column;\n            margin-bottom: 2.5rem;\n            padding-bottom: 1.5rem;\n            border-bottom: 1px solid #313244;\n        }}\n        .post-item:last-child {{\n            border-bottom: none;\n        }}\n        .post-title {{\n            margin-bottom: 0.5rem;\n        }}\n        .post-title a {{\n            color: #89b4fa;\n            font-size: 1.5rem;\n            font-weight: 600;\n            text-decoration: none;\n        }}\n        .post-title a:hover {{\n            color: #94e2d5;\n            text-decoration: underline;\n        }}\n        .post-meta {{\n            color: #a6adc8;\n            font-size: 0.9rem;\n            margin-bottom: 0.75rem;\n        }}\n        .post-categories {{\n            margin-bottom: 0.5rem;\n        }}\n        .post-categories span {{\n            display: inline-block;\n            background: #45475a;\n            color: #bac2de;\n            padding: 0.25rem 0.5rem;\n            border-radius: 4px;\n            font-size: 0.8rem;\n            margin-right: 0.5rem;\n        }}\n        .post-description {{\n            color: #cdd6f4;\n            margin-top: 0.75rem;\n            line-height: 1.5;\n        }}\n        nav {{\n            background: #181825;\n            padding: 1rem 0;\n            margin-bottom: 2rem;\n            border-bottom: 1px solid #313244;\n        }}\n        nav ul {{\n            list-style: none;\n            display: flex;\n            gap: 2rem;\n            justify-content: center;\n            margin: 0;\n            padding: 0;\n        }}\n        nav a {{\n            color: #cdd6f4;\n            text-decoration: none;\n            font-weight: 500;\n            padding: 0.5rem 1rem;\n            border-radius: 4px;\n            transition: all 0.2s ease;\n        }}\n        nav a:hover {{\n            background: #313244;\n            color: #89dceb;\n        }}\n        .container {{\n            max-width: 900px;\n            margin: 0 auto;\n            padding: 0 1rem;\n        }}\n        .about-profile {{\n            text-align: center;\n            margin-bottom: 2rem;\n        }}\n        .about-profile img {{\n            border-radius: 50%;\n            width: 200px;\n            height: 200px;\n            object-fit: cover;\n            border: 3px solid #45475a;\n            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);\n        }}\n        .social-links {{\n            text-align: center;\n            margin-top: 2rem;\n        }}\n        .social-links a {{\n            display: inline-block;\n            margin: 0 1rem;\n            color: #89dceb;\n            text-decoration: none;\n            font-weight: 500;\n        }}\n        .social-links a:hover {{\n            color: #94e2d5;\n        }}\n        pre {{\n            background: #181825;\n            border: 1px solid #313244;\n            border-radius: 6px;\n            padding: 1rem;\n            overflow-x: auto;\n            margin-bottom: 1.5rem;\n        }}\n        code {{\n            background: #313244;\n            padding: 0.2rem 0.4rem;\n            border-radius: 3px;\n            font-family: \'JetBrains Mono\', monospace;\n            font-size: 0.9rem;\n            color: #a6e3a1;\n        }}\n        pre code {{\n            background: none;\n            padding: 0;\n            color: #cdd6f4;\n        }}\n        h1, h2, h3, h4, h5, h6 {{\n            color: #b4befe;\n            margin-top: 2rem;\n            margin-bottom: 1rem;\n            font-weight: 600;\n        }}\n        h1 {{ font-size: 2.2rem; }}\n        h2 {{ font-size: 1.8rem; }}\n        h3 {{ font-size: 1.5rem; }}\n        a {{\n            color: #89dceb;\n        }}\n        a:hover {{\n            color: #94e2d5;\n            text-decoration: underline;\n        }}\n        body {{\n            background: #1e1e2e;\n            color: #cdd6f4;\n            font-family: \'JetBrains Mono\', \'Monaco\', \'Consolas\', monospace;\n            line-height: 1.6;\n            margin: 0;\n            padding: 0;\n        }}\n        .hidden {{\n            display: none !important;\n        }}\n        .toc li {{
            margin: 0.25rem 0;
            line-height: 1.3;
        }}

        .toc ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .toc-title {{
            color: #89b4fa;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .toc {{
            background: #181825;
            border: 1px solid #313244;
            border-radius: 6px;
            padding: 0.75rem 1rem;
            max-width: 100%;
            overflow: hidden;
        }}

        .toc-container {{
            margin-bottom: 1.5rem;
            max-width: 100%;
            overflow-x: hidden;
        }}

        article h1 {{\n            color: #b4befe;\n            border-bottom: 2px solid #313244;\n            padding-bottom: 0.5rem;\n            margin-bottom: 1.5rem;\n        }}\n    </style>\n</head>\n<body>\n    <nav>\n        <div class="container">\n            <ul>\n                {nav_html}\n            </ul>\n        </div>\n    </nav>\n    \n    <div class="container">\n        {search_html}\n        <main>\n            {content}\n        </main>\n    </div>\n    \n    <script>
    MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']]
        }},
        svg: {{
            fontCache: 'global'
        }}
    }};
    </script>
    <script type="text/javascript" id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
    </script>
    <script src="search.js"></script>\n</body>\n</html>\n"""


def generate_post_page(post, output_dir):
    """Generate individual post page"""
    html_content = md_to_html(post["body"])

    html_content = re.sub(
        r'src="images/([^"]+)"',
        f'src="{post["section"]}_{post["slug"]}_images/\\1"',
        html_content,
    )

    cover_image_html = ""
    if "image" in post["frontmatter"]:
        img_path = post["frontmatter"]["image"]
        if img_path.startswith("images/"):
            img_path = f"{post['section']}_{post['slug']}_images/{img_path[7:]}"
        cover_image_html = (
            f'<div class="post-cover"><img src="{img_path}" alt="Cover image"></div>'
        )

    # Generate TOC if enabled
    toc_html = ""
    if post["frontmatter"].get("toc", False):
        headers = re.findall(r"<h([1-4])>([^<]+)</h\1>", html_content)
        headers = [
            (level, re.sub(r"\s*\{#[^}]+\}\s*$", "", text.strip()))
            for level, text in headers
        ]
        post_title = post["title"]
        headers = [h for h in headers if h[1].lower() != post_title.lower()]
        if headers:
            toc_title = post["frontmatter"].get("toc-title", "Table of Contents")
            toc_location = post["frontmatter"].get("toc-location", "right")
            toc_items = []
            for level, text in headers:
                anchor = re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))
                indent = max(0, int(level) - 2) * 1.25
                toc_items.append(
                    f'<li class="toc-level-{level}" style="margin-left: {indent}rem"><a href="#{anchor}">{text}</a></li>'
                )
            toc_html = f"""<aside class="toc-container" data-location="{toc_location}"><div class="toc"><h2 class="toc-title">{toc_title}</h2><ul>{"".join(toc_items)}</ul></div></aside>"""
            for level, text in headers:
                anchor = re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))
                html_content = re.sub(
                    rf"<h{level}>([^<]*){re.escape(text)}([^<]*)</h{level}>",
                    rf'<h{level} id="{anchor}">\1{text}\2</h{level}>',
                    html_content,
                    count=1,
                )
            toc_html = f"""<aside class="toc-container" data-location="{toc_location}"><div class="toc"><h2 class="toc-title">{toc_title}</h2><ul>{"".join(toc_items)}</ul></div></aside>"""
            # Add anchors to headers
            for level, text in headers:
                anchor = re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))
                html_content = re.sub(
                    rf"<h{level}>([^<]*){re.escape(text)}([^<]*)</h{level}>",
                    rf'<h{level} id="{anchor}">\1{text}\2</h{level}>',
                    html_content,
                    count=1,
                )

    cats_html = ", ".join(post["categories"]) if post["categories"] else ""
    cats_display = (
        f' | <span class="post-categories">{cats_html}</span>' if cats_html else ""
    )

    page_content = f"""
    <article>
        {toc_html}
        <h1>{post["title"]}</h1>
        <div class="post-meta">
            <time>{post["date"]}</time>
            {cats_display}
        </div>
        {cover_image_html}
        {html_content}
    </article>
    """

    html = generate_html_layout(
        f"{post['title']} - Thomas W. Bush", page_content, "post"
    )

    output_path = Path(output_dir) / f"{post['section']}_{post['slug']}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# Rest of functions to add...


def generate_listing(title, posts, output_path, page_type="listing"):
    """Generate a listing page"""
    header_html = ""
    if page_type == "home":
        header_html = """
        <div class="site-header">
            <h1 class="site-title">Thomas W. Bush</h1>
            <p class="site-description">Research, book reviews, and thoughts on machine learning, neuroscience, and software.</p>
        </div>
        """

    filter_html = ""
    if page_type != "home" and posts:
        categories = sorted(set(cat for post in posts for cat in post["categories"]))
        if categories:
            options = ['<option value="">All Categories</option>']
            for cat in categories:
                options.append(
                    f'<option value="{cat}">{cat.replace("-", " ").title()}</option>'
                )
            filter_html = f"""
            <div class="category-filter">
                <label for="category-select">Filter by category:</label>
                <select id="category-select">
                    {"".join(options)}
                </select>
            </div>
            """.strip()

    posts_html = ""
    for post in posts:
        post_url = f"{post['section']}_{post['slug']}.html"
        categories_html = "".join(
            [f"<span>{cat}</span>" for cat in post["categories"][:3]]
        )
        desc_attr = post["description"].lower() if post["description"] else ""
        cats_attr = " ".join(post["categories"])
        cover_html = ""
        if "image" in post["frontmatter"]:
            img_path = post["frontmatter"]["image"]
            if img_path.startswith("images/"):
                img_path = f"{post['section']}_{post['slug']}_images/{img_path[7:]}"
            cover_html = f'<div class="post-cover-small"><img src="{img_path}" alt="{post["title"]}" loading="lazy"></div>'

        posts_html += f"""
        <div class="post-item" data-categories="{cats_attr}" data-title="{post["title"].lower()}" data-description="{desc_attr}">
            {cover_html}
            <h2 class="post-title"><a href="{post_url}">{post["title"]}</a></h2>
            <div class="post-meta">
                <time>{post["date"]}</time>
            </div>
            {(f'<div class="post-categories">{categories_html}</div>') if categories_html else ""}
            {(f'<div class="post-description">{post["description"]}</div>') if post["description"] else ""}
        </div>
        """

    page_content = f"""
    {header_html}
    <h1>{title}</h1>
    {filter_html}
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
        page_content = """
        <article>
            <h1>About Me</h1>
            <div class="about-profile">
                <img src="profile.jpg" alt="Profile">
            </div>
            <p>Welcome to my blog.</p>
        </article>
        """
        html = generate_html_layout("About - Thomas W. Bush", page_content, "page")
        with open(Path(output_dir) / "about.html", "w", encoding="utf-8") as f:
            f.write(html)
        return

    with open(about_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)
    html_content = md_to_html(body)

    social_links_html = ""
    links = []
    icon_map = {
        "twitter": "🐦",
        "linkedin": "💼",
        "github": "🐙",
        "file": "📄",
        "envelope": "✉️",
    }

    # Get links from nested structure (prefer about.links)
    if "about" in frontmatter and isinstance(frontmatter["about"], dict):
        links = frontmatter["about"].get("links", [])
    elif "links" in frontmatter and isinstance(frontmatter["links"], list):
        links = frontmatter["links"]

    link_html = []
    for link in links:
        if isinstance(link, dict):
            icon = link.get("icon", "")
            text = link.get("text", "")
            href = link.get("href", "#")
            icon_char = icon_map.get(icon, "🔗")
            link_html.append(f'<a href="{href}" target="_blank">{icon_char} {text}</a>')

    if link_html:
        social_links_html = (
            '<div class="social-links">' + " ".join(link_html) + "</div>"
        )

    page_content = f"""
    <article>
        <h1>{frontmatter.get("title", "About")}</h1>
        <div class="about-profile">
            <img src="profile.jpg" alt="Profile">
        </div>
        {html_content}
        {social_links_html}
    </article>
    """

    html = generate_html_layout("About - Thomas W. Bush", page_content, "page")

    with open(Path(output_dir) / "about.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_site(base_dir, output_dir):
    """Build the entire site"""
    base = Path(base_dir)
    output = Path(output_dir)

    if output.exists():
        shutil.rmtree(output)
    output.mkdir()

    copy_assets(base_dir, output_dir)

    posts = get_all_posts(base_dir)

    research_posts = [p for p in posts if p["section"] == "research"]
    books_posts = [p for p in posts if p["section"] == "books"]

    for post in posts:
        generate_post_page(post, output_dir)

    generate_listing("Recent Posts", posts, output / "index.html", "home")
    generate_listing("Research", research_posts, output / "research.html", "listing")
    generate_listing("Books", books_posts, output / "books.html", "listing")

    generate_about_page(base_dir, output_dir)

    search_js = """// Simple client-side search
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const posts = document.querySelectorAll('.post-item');
    
    function filterPosts() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedCategory = categorySelect ? categorySelect.value.toLowerCase() : '';
        
        posts.forEach(post => {
            let show = true;
            
            if (query) {
                const title = post.getAttribute('data-title') || '';
                const description = post.getAttribute('data-description') || '';
                const categories = post.getAttribute('data-categories') || '';
                const match = title.includes(query) || 
                             description.includes(query) || 
                             categories.includes(query);
                if (!match) show = false;
            }
            
            if (selectedCategory && show) {
                const categories = post.getAttribute('data-categories') || '';
                if (!categories.includes(selectedCategory)) {
                    show = false;
                }
            }
            
            if (show) {
                post.classList.remove('hidden');
            } else {
                post.classList.add('hidden');
            }
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', filterPosts);
    }
    
    if (categorySelect) {
        categorySelect.addEventListener('change', filterPosts);
    }
});"""

    with open(output / "search.js", "w", encoding="utf-8") as f:
        f.write(search_js)

    print(f"Site built successfully! {len(posts)} posts generated.")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "_site")

    build_site(base_dir, output_dir)
