"""
Core Markdown → PDF conversion engine.

Pipeline:  Markdown  →  HTML (markdown-it-py)  →  PDF (Playwright / Chromium)

Features supported:
  • GitHub Flavored Markdown (tables, strikethrough, autolinks, task-lists)
  • Fenced code blocks with Pygments syntax highlighting
  • Footnotes
  • Math equations  ($...$  and  $$...$$)  via KaTeX
  • Mermaid diagrams rendered via mermaid.js
  • GitHub-style alerts  (> [!NOTE], > [!TIP], etc.)
  • Front-matter stripping
  • Images (remote URLs)
"""

from __future__ import annotations

import html as html_module
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin

from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from styles import get_full_css

# ────────────────────────────────────────────────────────────────────────────
#  Alert SVG icons (matching GitHub exactly)
# ────────────────────────────────────────────────────────────────────────────
ALERT_ICONS = {
    "NOTE": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
    "TIP": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>',
    "IMPORTANT": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
    "WARNING": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
    "CAUTION": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><path d="M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a.749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11.53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5.38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
}

ALERT_LABELS = {
    "NOTE": "Note",
    "TIP": "Tip",
    "IMPORTANT": "Important",
    "WARNING": "Warning",
    "CAUTION": "Caution",
}


# ────────────────────────────────────────────────────────────────────────────
#  Syntax highlighting callback for markdown-it-py
# ────────────────────────────────────────────────────────────────────────────
def _highlight_code(code: str, lang: str, _attrs: str) -> str:
    """Return highlighted HTML for a fenced code block.

    For ``mermaid`` blocks we return an empty string so that the custom
    fence renderer can wrap them in ``<div class="mermaid">``.
    """
    if lang and lang.strip().lower() == "mermaid":
        return ""  # handled by custom fence renderer

    if lang:
        try:
            lexer = get_lexer_by_name(lang.strip(), stripall=True)
        except ClassNotFound:
            return ""  # fall back to default escaping
    else:
        return ""

    formatter = HtmlFormatter(nowrap=True)
    return pygments_highlight(code, lexer, formatter)


# ────────────────────────────────────────────────────────────────────────────
#  Custom fence renderer – handles mermaid and syntax-highlighted blocks
# ────────────────────────────────────────────────────────────────────────────
def _fence_renderer(self, tokens, idx, options, env):
    """Override the default fence renderer to support mermaid blocks and
    preserve Pygments output."""
    token = tokens[idx]
    info = token.info.strip() if token.info else ""
    lang = info.split()[0] if info else ""
    lang_lower = lang.lower()

    # Mermaid diagrams
    if lang_lower == "mermaid":
        return f'<div class="mermaid">{html_module.escape(token.content)}</div>\n'

    # Attempt syntax highlighting
    highlighted = ""
    if options.get("highlight"):
        highlighted = options["highlight"](token.content, lang, "")

    if highlighted:
        lang_class = f' class="language-{html_module.escape(lang)} highlight"' if lang else ' class="highlight"'
        return f"<pre{lang_class}><code>{highlighted}</code></pre>\n"

    # Default: escape and wrap
    escaped = html_module.escape(token.content)
    lang_attr = f' class="language-{html_module.escape(lang)}"' if lang else ""
    return f"<pre><code{lang_attr}>{escaped}</code></pre>\n"


# ────────────────────────────────────────────────────────────────────────────
#  GitHub-style alerts post-processing
# ────────────────────────────────────────────────────────────────────────────
_ALERT_RE = re.compile(
    r"<blockquote>\s*<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]",
    re.IGNORECASE,
)


def _process_github_alerts(html_body: str) -> str:
    """Convert ``> [!NOTE]`` style blockquotes into GitHub-styled alert boxes."""
    def _replace(match):
        alert_type = match.group(1).upper()
        icon = ALERT_ICONS.get(alert_type, "")
        label = ALERT_LABELS.get(alert_type, alert_type.title())
        return (
            f'<div class="markdown-alert markdown-alert-{alert_type.lower()}">'
            f'<p class="markdown-alert-title">{icon} {label}</p>'
            f"<p>"
        )
    result = _ALERT_RE.sub(_replace, html_body)
    # Close the div where we opened it (replace the corresponding </blockquote>)
    # We do a more targeted replacement: for each alert div we opened, the next
    # </blockquote> should become </div>
    parts = result.split('<div class="markdown-alert')
    if len(parts) <= 1:
        return result

    final = parts[0]
    for part in parts[1:]:
        part_with_div = '<div class="markdown-alert' + part
        # Replace only the FIRST </blockquote> within this chunk
        part_with_div = part_with_div.replace("</blockquote>", "</div>", 1)
        final += part_with_div
    return final


# ────────────────────────────────────────────────────────────────────────────
#  Math rendering post-processing
# ────────────────────────────────────────────────────────────────────────────
def _process_math(html_body: str) -> str:
    """Wrap math tokens from dollarmath plugin so KaTeX can pick them up."""
    # dollarmath emits:
    #   <span class="math inline">...</span>
    #   <div class="math display">...</div>
    # We need them as raw LaTeX for KaTeX auto-render, but dollarmath
    # already does HTML escaping. Let's unescape the math content.
    def _unescape_math(m):
        tag = m.group(1)  # span or div
        cls = m.group(2)  # inline or display
        content = m.group(3)
        # unescape HTML entities back to raw LaTeX
        content = (
            content
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
        )
        if cls == "inline":
            return f'<span class="math math-inline">${content}$</span>'
        else:
            return f'<div class="math math-display">$${content}$$</div>'

    html_body = re.sub(
        r'<(span|div) class="math (inline|display|block)">(.*?)</\1>',
        _unescape_math,
        html_body,
        flags=re.DOTALL,
    )
    return html_body


# ────────────────────────────────────────────────────────────────────────────
#  Build the markdown-it parser
# ────────────────────────────────────────────────────────────────────────────
def create_parser() -> MarkdownIt:
    """Create a fully-configured GFM-like markdown parser."""
    md = MarkdownIt(
        "gfm-like",
        {"highlight": _highlight_code, "html": True, "linkify": True, "typographer": True},
    )

    # Plugins
    footnote_plugin(md)
    front_matter_plugin(md)
    tasklists_plugin(md)
    dollarmath_plugin(md, double_inline=True)

    # Override fence renderer
    md.add_render_rule("fence", _fence_renderer)

    return md


# ────────────────────────────────────────────────────────────────────────────
#  Markdown → full HTML document
# ────────────────────────────────────────────────────────────────────────────
def md_to_html(
    md_content: str,
    page_size: str = "A4",
    margin_top: str = "20mm",
    margin_bottom: str = "20mm",
    margin_left: str = "25mm",
    margin_right: str = "25mm",
    font_scale: float = 1.0,
) -> str:
    """Convert raw Markdown text into a complete, self-contained HTML
    document styled to look like a GitHub readme."""
    parser = create_parser()
    html_body = parser.render(md_content)

    # Post-processing
    html_body = _process_github_alerts(html_body)
    html_body = _process_math(html_body)

    css = get_full_css(page_size, margin_top, margin_bottom, margin_left, margin_right, font_scale)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Markdown Document</title>

  <!-- KaTeX for math rendering -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>

  <!-- Mermaid for diagram rendering -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 0; background: #ffffff; }}
    .markdown-body {{ max-width: none; padding: 2rem 0; }}
    
    #loading-overlay {{
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(255, 255, 255, 0.9); z-index: 9999;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      font-family: 'Inter', sans-serif; color: #4a5568; transition: opacity 0.3s;
    }}
    .spinner {{
      width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top: 4px solid #667eea;
      border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem;
    }}
    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}

    {css}
  </style>
</head>
<body>
  <div id="loading-overlay">
    <div class="spinner"></div>
    <div style="font-weight: 600;">Rendering Document...</div>
  </div>

  <article class="markdown-body">
    {html_body}
  </article>

  <script>
    mermaid.initialize({{ startOnLoad: false, theme: 'default' }});

    document.addEventListener("DOMContentLoaded", async function() {{
      // 1. Math
      if (typeof renderMathInElement !== 'undefined') {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{ left: "$$", right: "$$", display: true }},
            {{ left: "$", right: "$", display: false }}
          ],
          throwOnError: false
        }});
      }}
      
      // 2. Mermaid
      try {{
        await mermaid.run({{ querySelector: '.mermaid' }});
      }} catch (e) {{
        console.error(e);
      }}

      // 3. Mark rendering as complete for Playwright
      const flag = document.createElement("div");
      flag.id = "render-complete";
      flag.style.display = "none";
      document.body.appendChild(flag);

      // 4. Hide loading overlay
      const overlay = document.getElementById("loading-overlay");
      overlay.style.opacity = "0";
      setTimeout(() => overlay.style.display = "none", 300);
    }});
  </script>
</body>
</html>"""
    return full_html


# ────────────────────────────────────────────────────────────────────────────
#  HTML → PDF via Playwright (headless Chromium)
# ────────────────────────────────────────────────────────────────────────────
def ensure_playwright_browsers():
    """Install Chromium for Playwright if it isn't already available."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
    except Exception:
        print("📦 Installing Chromium browser for Playwright…")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
        )


def html_to_pdf(
    html_content: str,
    page_size: str = "A4",
    margin_top: str = "20mm",
    margin_bottom: str = "20mm",
    margin_left: str = "25mm",
    margin_right: str = "25mm",
    display_header_footer: bool = False,
    header_template: str = "",
    footer_template: str = "",
) -> bytes:
    """Render the HTML document to PDF using headless Chromium."""
    import asyncio
    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        except Exception:
            pass

    from playwright.sync_api import sync_playwright

    # Write HTML to a temporary file for reliable loading
    tmp_html = Path(tempfile.mktemp(suffix=".html"))
    tmp_html.write_text(html_content, encoding="utf-8")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to file URL – more reliable than set_content for
            # pages that load external resources (KaTeX CSS/JS, Mermaid JS).
            page.goto(
                tmp_html.as_uri(),
                wait_until="domcontentloaded",
                timeout=60000,
            )

            # Wait deterministically for math and diagrams to finish rendering
            page.wait_for_selector("#render-complete", state="attached", timeout=60000)

            pdf_options = {
                "format": page_size,
                "margin": {
                    "top": margin_top,
                    "bottom": margin_bottom,
                    "left": margin_left,
                    "right": margin_right,
                },
                "print_background": True,
                "prefer_css_page_size": True,
            }

            if display_header_footer:
                pdf_options["display_header_footer"] = True
                # Default footer with page numbers
                if not footer_template:
                    footer_template = """
                    <div style="font-size:9px; width:100%; text-align:center; color:#888;">
                        <span class="pageNumber"></span> / <span class="totalPages"></span>
                    </div>
                    """
                pdf_options["header_template"] = header_template or "<span></span>"
                pdf_options["footer_template"] = footer_template

            pdf_bytes = page.pdf(**pdf_options)
            browser.close()
            return pdf_bytes
    finally:
        # Clean up the temporary HTML file
        try:
            tmp_html.unlink()
        except OSError:
            pass


# ────────────────────────────────────────────────────────────────────────────
#  High-level API
# ────────────────────────────────────────────────────────────────────────────
def convert(
    md_content: str,
    page_size: str = "A4",
    margin_top: str = "20mm",
    margin_bottom: str = "20mm",
    margin_left: str = "25mm",
    margin_right: str = "25mm",
    display_header_footer: bool = False,
    header_template: str = "",
    footer_template: str = "",
    font_scale: float = 1.0,
) -> bytes:
    """Convert Markdown text to a PDF byte string.

    Returns
    -------
    bytes
        The raw PDF file content.
    """
    html = md_to_html(
        md_content,
        page_size=page_size,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        font_scale=font_scale,
    )
    return html_to_pdf(
        html,
        page_size=page_size,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        display_header_footer=display_header_footer,
        header_template=header_template,
        footer_template=footer_template,
    )
