#!/usr/bin/env python3
"""
Markdown to HTML Blog Post Converter for perceptron.ai
Converts Markdown files to styled HTML blog posts matching your site theme.

Usage:
    python3 convert_blog.py input.md output.html
"""

import sys
import re
from pathlib import Path

# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | perceptron.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- MathJax for LaTeX -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #000000;
            --secondary: #1a1a1a;
            --accent: #00d9ff;
            --bg: #0a0a0a;
            --border: #2a2a2a;
            --text-light: #b0b0b0;
            --text-white: #ffffff;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            color: var(--primary);
            background: var(--bg);
            line-height: 1.6;
        }}

        nav {{
            position: sticky;
            top: 0;
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            z-index: 100;
            backdrop-filter: blur(10px);
            background: rgba(10, 10, 10, 0.95);
        }}

        .nav-container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .nav-logo {{
            font-size: 1.3rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            text-decoration: none;
            color: var(--text-white);
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}

        .nav-links a {{
            text-decoration: none;
            color: var(--text-light);
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s;
            position: relative;
        }}

        .nav-links a:hover {{
            color: var(--accent);
        }}

        .nav-links a::after {{
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.2s;
        }}

        .nav-links a:hover::after {{
            width: 100%;
        }}

        .back-link {{
            display: inline-block;
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 2rem;
            transition: color 0.2s;
        }}

        .back-link:hover {{
            color: var(--text-white);
        }}

        .back-link::before {{
            content: '← ';
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .blog-header {{
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid var(--accent);
        }}

        .blog-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-white);
            line-height: 1.2;
        }}

        .blog-meta {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            color: var(--text-light);
            font-size: 0.95rem;
        }}

        .blog-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .tag {{
            background: var(--secondary);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--text-light);
            border: 1px solid var(--border);
        }}

        .blog-content {{
            color: var(--text-white);
            line-height: 1.9;
        }}

        .blog-content h1 {{
            font-size: 2rem;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
            font-weight: 700;
        }}

        .blog-content h2 {{
            font-size: 1.8rem;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
            font-weight: 700;
        }}

        .blog-content h3 {{
            font-size: 1.4rem;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
            color: var(--text-white);
            font-weight: 700;
        }}

        .blog-content h4 {{
            font-size: 1.1rem;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            color: var(--text-white);
            font-weight: 600;
        }}

        .blog-content p {{
            margin-bottom: 1.5rem;
            color: var(--text-light);
            font-size: 1rem;
        }}

        .blog-content ul, .blog-content ol {{
            margin-left: 2rem;
            margin-bottom: 1.5rem;
            color: var(--text-light);
        }}

        .blog-content li {{
            margin-bottom: 0.8rem;
            line-height: 1.8;
        }}

        .blog-content strong {{
            color: var(--text-white);
            font-weight: 600;
        }}

        .blog-content em {{
            font-style: italic;
            color: var(--accent);
        }}

        .blog-content a {{
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid var(--accent);
            transition: all 0.2s;
        }}

        .blog-content a:hover {{
            color: var(--text-white);
            border-color: var(--text-white);
        }}

        .blog-content blockquote {{
            border-left: 3px solid var(--accent);
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            color: var(--text-light);
            font-style: italic;
        }}

        .blog-content code {{
            background: var(--secondary);
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            color: var(--accent);
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }}

        .blog-content pre {{
            background: var(--secondary);
            padding: 1rem;
            border-left: 3px solid var(--accent);
            margin: 1.5rem 0;
            border-radius: 4px;
            color: var(--text-light);
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            line-height: 1.4;
        }}

        .blog-content pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}

        .blog-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}

        .blog-content th {{
            background: var(--secondary);
            color: var(--text-white);
            padding: 0.8rem;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid var(--accent);
        }}

        .blog-content td {{
            padding: 0.8rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-light);
        }}

        /* MathJax styling */
        .MathJax {{
            color: var(--accent) !important;
        }}

        footer {{
            background: var(--primary);
            color: var(--text-white);
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            border-top: 1px solid var(--border);
        }}

        .footer-links {{
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}

        .footer-links a {{
            color: var(--text-white);
            text-decoration: none;
            transition: color 0.2s;
        }}

        .footer-links a:hover {{
            color: var(--accent);
        }}

        .footer-text {{
            font-size: 0.9rem;
            color: var(--text-light);
        }}

        @media (max-width: 600px) {{
            .blog-title {{
                font-size: 2rem;
            }}

            .blog-content h2 {{
                font-size: 1.4rem;
            }}

            .nav-links {{
                gap: 1rem;
                font-size: 0.85rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <a href="../index.html" class="nav-logo">perceptron.ai</a>
            <ul class="nav-links">
                <li><a href="../index.html#home">Home</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../index.html#projects">Projects</a></li>
                <li><a href="../index.html#cv">CV</a></li>
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">
        <a href="../index.html#blog" class="back-link">Back to Blog</a>

        <article class="blog-header">
            <h1 class="blog-title">{title}</h1>
            <div class="blog-meta">
                <span>📅 {date}</span>
                <div class="blog-tags">
                    {tags}
                </div>
            </div>
        </article>

        <article class="blog-content">
            {content}
        </article>
    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-links">
            <a href="https://twitter.com" target="_blank">Twitter</a>
            <a href="https://github.com" target="_blank">GitHub</a>
            <a href="https://linkedin.com" target="_blank">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
        </div>
        <p class="footer-text">© 2026 perceptron.ai. Building in public.</p>
    </footer>
</body>
</html>
'''

def parse_markdown_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter = {}
    for line in parts[1].split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip().strip('"\'')
            
            if key == 'tags':
                # Parse list format
                value = [tag.strip().strip('[]"\'') for tag in value.split(',')]
            
            frontmatter[key] = value
    
    return frontmatter, parts[2]

def markdown_to_html(md_content):
    """Convert markdown to HTML."""
    html = md_content
    
    # FIRST: Protect math blocks with placeholders
    math_blocks = {}
    math_counter = [0]
    
    def save_display_math(match):
        key = f"__DISPLAY_MATH_{math_counter[0]}__"
        math_blocks[key] = f"$${ match.group(1) }$$"
        math_counter[0] += 1
        return key
    
    def save_inline_math(match):
        key = f"__INLINE_MATH_{math_counter[0]}__"
        math_blocks[key] = f"${ match.group(1) }$"
        math_counter[0] += 1
        return key
    
    # Protect display math $$ ... $$
    html = re.sub(r'\$\$(.*?)\$\$', save_display_math, html, flags=re.DOTALL)
    
    # Protect inline math $ ... $
    html = re.sub(r'(?<!\$)\$([^\$\n]+?)\$(?!\$)', save_inline_math, html)
    
    # Code blocks (must be before inline code)
    html = re.sub(r'```([^\n]*)\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    
    # Headings
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Lists (unordered)
    html = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    html = re.sub(r'</li>\n<li>', r'</li><li>', html)
    
    # Lists (ordered)
    html = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Blockquotes
    html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Paragraphs
    paragraphs = html.split('\n\n')
    processed = []
    for para in paragraphs:
        if para.strip() and not any(tag in para for tag in ['<h', '<ul', '<blockquote', '<pre', '<div', '<li']):
            para = f'<p>{para}</p>'
        processed.append(para)
    html = '\n'.join(processed)
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # FINALLY: Restore math blocks
    for key, value in math_blocks.items():
        if '__DISPLAY_MATH_' in key:
            html = html.replace(key, f'<div class="math-display">{value}</div>')
        else:
            html = html.replace(key, value)
    
    return html

def generate_tags_html(tags):
    """Generate HTML for tags."""
    if isinstance(tags, str):
        tags = [tags]
    return '\n'.join(f'<span class="tag">{tag}</span>' for tag in tags)

def convert_markdown_to_html(input_file, output_file):
    """Convert markdown blog post to HTML."""
    
    # Read markdown file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Parse frontmatter
    frontmatter, body = parse_markdown_frontmatter(md_content)
    
    # Convert markdown to HTML
    html_content = markdown_to_html(body.strip())
    
    # Prepare template variables
    title = frontmatter.get('title', 'Blog Post')
    date = frontmatter.get('date', 'Unknown Date')
    tags = frontmatter.get('tags', [])
    tags_html = generate_tags_html(tags)
    
    # Generate final HTML
    final_html = HTML_TEMPLATE.format(
        title=title,
        date=date,
        tags=tags_html,
        content=html_content
    )
    
    # Write output with UTF-8 encoding (force UTF-8 on Windows)
    import io
    with io.open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✓ Converted: {input_file} → {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 convert_blog.py input.md output.html")
        print("\nExample:")
        print("  python3 convert_blog.py post.md ../blog/post.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    convert_markdown_to_html(input_file, output_file)