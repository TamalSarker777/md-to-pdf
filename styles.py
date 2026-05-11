"""
CSS Styles for Markdown to PDF Converter.
Contains GitHub Markdown CSS, Pygments highlighting, and print styles.
"""

# --------------------------------------------------------------------------- #
#  Official GitHub Markdown CSS (light theme)                                  #
#  Source: sindresorhus/github-markdown-css                                     #
# --------------------------------------------------------------------------- #
GITHUB_MARKDOWN_CSS = """
.markdown-body {
  color-scheme: light;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  margin: 0;
  font-weight: 400;
  color: #1f2328;
  background-color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 16px;
  line-height: 1.5;
  word-wrap: break-word;
}

.markdown-body a {
  background-color: transparent;
  color: #0969da;
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body b,
.markdown-body strong {
  font-weight: 600;
}

.markdown-body dfn {
  font-style: italic;
}

.markdown-body h1 {
  margin: .67em 0;
  font-weight: 600;
  padding-bottom: .3em;
  font-size: 2em;
  border-bottom: 1px solid #d1d9e0b3;
}

.markdown-body mark {
  background-color: #fff8c5;
  color: #1f2328;
}

.markdown-body small {
  font-size: 90%;
}

.markdown-body sub,
.markdown-body sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

.markdown-body sub {
  bottom: -0.25em;
}

.markdown-body sup {
  top: -0.5em;
}

.markdown-body img {
  border-style: none;
  max-width: 100%;
  box-sizing: content-box;
}

.markdown-body code,
.markdown-body kbd,
.markdown-body pre,
.markdown-body samp {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  font-size: 1em;
}

.markdown-body figure {
  margin: 1em 2.5rem;
}

.markdown-body hr {
  box-sizing: content-box;
  overflow: hidden;
  background: transparent;
  border-bottom: 1px solid #d1d9e0b3;
  height: .25em;
  padding: 0;
  margin: 1.5rem 0;
  background-color: #d1d9e0;
  border: 0;
}

.markdown-body details,
.markdown-body figcaption,
.markdown-body figure {
  display: block;
}

.markdown-body summary {
  display: list-item;
}

.markdown-body [hidden] {
  display: none !important;
}

.markdown-body abbr[title] {
  border-bottom: none;
  text-decoration: underline dotted;
}

.markdown-body input {
  font: inherit;
  margin: 0;
  overflow: visible;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

.markdown-body table {
  border-spacing: 0;
  border-collapse: collapse;
  display: block;
  width: max-content;
  max-width: 100%;
  overflow: auto;
  font-variant: tabular-nums;
}

.markdown-body td,
.markdown-body th {
  padding: 0;
}

.markdown-body details summary {
  cursor: pointer;
}

.markdown-body kbd {
  display: inline-block;
  padding: 0.25rem;
  font: 11px ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  line-height: 10px;
  color: #1f2328;
  vertical-align: middle;
  background-color: #f6f8fa;
  border: solid 1px #d1d9e0;
  border-bottom-color: #d1d9e0;
  border-radius: 6px;
  box-shadow: inset 0 -1px 0 #d1d9e0;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body h2 {
  font-weight: 600;
  padding-bottom: .3em;
  font-size: 1.5em;
  border-bottom: 1px solid #d1d9e0b3;
}

.markdown-body h3 {
  font-weight: 600;
  font-size: 1.25em;
}

.markdown-body h4 {
  font-weight: 600;
  font-size: 1em;
}

.markdown-body h5 {
  font-weight: 600;
  font-size: .875em;
}

.markdown-body h6 {
  font-weight: 600;
  font-size: .85em;
  color: #59636e;
}

.markdown-body p {
  margin-top: 0;
  margin-bottom: 10px;
}

.markdown-body blockquote {
  margin: 0;
  padding: 0 1em;
  color: #59636e;
  border-left: .25em solid #d1d9e0;
}

.markdown-body ul,
.markdown-body ol {
  margin-top: 0;
  margin-bottom: 0;
  padding-left: 2em;
}

.markdown-body ol ol,
.markdown-body ul ol {
  list-style-type: lower-roman;
}

.markdown-body ul ul ol,
.markdown-body ul ol ol,
.markdown-body ol ul ol,
.markdown-body ol ol ol {
  list-style-type: lower-alpha;
}

.markdown-body dd {
  margin-left: 0;
}

.markdown-body tt,
.markdown-body code,
.markdown-body samp {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  font-size: 12px;
}

.markdown-body pre {
  margin-top: 0;
  margin-bottom: 0;
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  font-size: 12px;
  word-wrap: normal;
}

.markdown-body::before {
  display: table;
  content: "";
}

.markdown-body::after {
  display: table;
  clear: both;
  content: "";
}

.markdown-body>*:first-child {
  margin-top: 0 !important;
}

.markdown-body>*:last-child {
  margin-bottom: 0 !important;
}

.markdown-body a:not([href]) {
  color: inherit;
  text-decoration: none;
}

.markdown-body p,
.markdown-body blockquote,
.markdown-body ul,
.markdown-body ol,
.markdown-body dl,
.markdown-body table,
.markdown-body pre,
.markdown-body details {
  margin-top: 0;
  margin-bottom: 1rem;
}

.markdown-body blockquote>:first-child {
  margin-top: 0;
}

.markdown-body blockquote>:last-child {
  margin-bottom: 0;
}

.markdown-body h1 tt,
.markdown-body h1 code,
.markdown-body h2 tt,
.markdown-body h2 code,
.markdown-body h3 tt,
.markdown-body h3 code,
.markdown-body h4 tt,
.markdown-body h4 code,
.markdown-body h5 tt,
.markdown-body h5 code,
.markdown-body h6 tt,
.markdown-body h6 code {
  padding: 0 .2em;
  font-size: inherit;
}

.markdown-body ul.no-list,
.markdown-body ol.no-list {
  padding: 0;
  list-style-type: none;
}

.markdown-body ol[type="a s"] { list-style-type: lower-alpha; }
.markdown-body ol[type="A s"] { list-style-type: upper-alpha; }
.markdown-body ol[type="i s"] { list-style-type: lower-roman; }
.markdown-body ol[type="I s"] { list-style-type: upper-roman; }
.markdown-body ol[type="1"]   { list-style-type: decimal; }

.markdown-body div>ol:not([type]) {
  list-style-type: decimal;
}

.markdown-body ul ul,
.markdown-body ul ol,
.markdown-body ol ol,
.markdown-body ol ul {
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body li>p {
  margin-top: 1rem;
}

.markdown-body li+li {
  margin-top: .25em;
}

.markdown-body dl {
  padding: 0;
}

.markdown-body dl dt {
  padding: 0;
  margin-top: 1rem;
  font-size: 1em;
  font-style: italic;
  font-weight: 600;
}

.markdown-body dl dd {
  padding: 0 1rem;
  margin-bottom: 1rem;
}

.markdown-body table th {
  font-weight: 600;
}

.markdown-body table th,
.markdown-body table td {
  padding: 6px 13px;
  border: 1px solid #d1d9e0;
}

.markdown-body table td>:last-child {
  margin-bottom: 0;
}

.markdown-body table tr {
  background-color: #ffffff;
  border-top: 1px solid #d1d9e0b3;
}

.markdown-body table tr:nth-child(2n) {
  background-color: #f6f8fa;
}

.markdown-body table img {
  background-color: transparent;
}

.markdown-body img[align=right] {
  padding-left: 20px;
}

.markdown-body img[align=left] {
  padding-right: 20px;
}

.markdown-body .emoji {
  max-width: none;
  vertical-align: text-top;
  background-color: transparent;
}

.markdown-body code,
.markdown-body tt {
  padding: .2em .4em;
  margin: 0;
  font-size: 85%;
  white-space: break-spaces;
  background-color: #818b981f;
  border-radius: 6px;
}

.markdown-body code br,
.markdown-body tt br {
  display: none;
}

.markdown-body del code {
  text-decoration: inherit;
}

.markdown-body samp {
  font-size: 85%;
}

.markdown-body pre code {
  font-size: 100%;
}

.markdown-body pre>code {
  padding: 0;
  margin: 0;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border: 0;
}

.markdown-body .highlight {
  margin-bottom: 1rem;
}

.markdown-body .highlight pre {
  margin-bottom: 0;
  word-break: normal;
}

.markdown-body .highlight pre,
.markdown-body pre {
  padding: 1rem;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  color: #1f2328;
  background-color: #f6f8fa;
  border-radius: 6px;
}

.markdown-body pre code,
.markdown-body pre tt {
  display: inline;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: transparent;
  border: 0;
}

/* ---- Footnotes ---- */
.markdown-body [data-footnote-ref]::before { content: "["; }
.markdown-body [data-footnote-ref]::after  { content: "]"; }

.markdown-body .footnotes {
  font-size: 12px;
  color: #59636e;
  border-top: 1px solid #d1d9e0;
}

.markdown-body .footnotes ol {
  padding-left: 1rem;
}

.markdown-body .footnotes li {
  position: relative;
}

/* ---- Task lists ---- */
.markdown-body .task-list-item {
  list-style-type: none;
}

.markdown-body .task-list-item label {
  font-weight: 400;
}

.markdown-body .task-list-item+.task-list-item {
  margin-top: 0.25rem;
}

.markdown-body .task-list-item-checkbox {
  margin: 0 .2em .25em -1.4em;
  vertical-align: middle;
}

/* ---- Emoji ---- */
.markdown-body g-emoji {
  display: inline-block;
  min-width: 1ch;
  font-family: "Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
  font-size: 1em;
  font-style: normal !important;
  font-weight: 400;
  line-height: 1;
  vertical-align: -0.075em;
}

/* ---- GitHub-style alerts ---- */
.markdown-body .markdown-alert {
  padding: 0.5rem 1rem;
  margin-bottom: 1rem;
  color: inherit;
  border-left: .25em solid #d1d9e0;
}

.markdown-body .markdown-alert>:first-child { margin-top: 0; }
.markdown-body .markdown-alert>:last-child  { margin-bottom: 0; }

.markdown-body .markdown-alert .markdown-alert-title {
  display: flex;
  font-weight: 500;
  align-items: center;
  line-height: 1;
}

.markdown-body .markdown-alert .markdown-alert-title svg {
  margin-right: 0.5rem;
}

.markdown-body .markdown-alert.markdown-alert-note {
  border-left-color: #0969da;
}
.markdown-body .markdown-alert.markdown-alert-note .markdown-alert-title {
  color: #0969da;
}

.markdown-body .markdown-alert.markdown-alert-important {
  border-left-color: #8250df;
}
.markdown-body .markdown-alert.markdown-alert-important .markdown-alert-title {
  color: #8250df;
}

.markdown-body .markdown-alert.markdown-alert-warning {
  border-left-color: #9a6700;
}
.markdown-body .markdown-alert.markdown-alert-warning .markdown-alert-title {
  color: #9a6700;
}

.markdown-body .markdown-alert.markdown-alert-tip {
  border-left-color: #1a7f37;
}
.markdown-body .markdown-alert.markdown-alert-tip .markdown-alert-title {
  color: #1a7f37;
}

.markdown-body .markdown-alert.markdown-alert-caution {
  border-left-color: #cf222e;
}
.markdown-body .markdown-alert.markdown-alert-caution .markdown-alert-title {
  color: #d1242f;
}
"""

# --------------------------------------------------------------------------- #
#  Pygments – GitHub‑light colour theme                                        #
# --------------------------------------------------------------------------- #
PYGMENTS_CSS = """
/* Pygments - GitHub Light */
.highlight .hll { background-color: #fff8c5 }
.highlight .c   { color: #6a737d } /* Comment */
.highlight .err { color: #cb2431 } /* Error */
.highlight .k   { color: #d73a49 } /* Keyword */
.highlight .l   { color: #032f62 } /* Literal */
.highlight .n   { color: #24292e } /* Name */
.highlight .o   { color: #d73a49 } /* Operator */
.highlight .p   { color: #24292e } /* Punctuation */
.highlight .ch  { color: #6a737d } /* Comment.Hashbang */
.highlight .cm  { color: #6a737d } /* Comment.Multiline */
.highlight .cp  { color: #d73a49 } /* Comment.Preproc */
.highlight .cpf { color: #032f62 } /* Comment.PreprocFile */
.highlight .c1  { color: #6a737d } /* Comment.Single */
.highlight .cs  { color: #6a737d; font-weight: bold } /* Comment.Special */
.highlight .gd  { color: #b31d28; background-color: #ffeef0 } /* Generic.Deleted */
.highlight .ge  { font-style: italic } /* Generic.Emph */
.highlight .gh  { color: #005cc5; font-weight: bold } /* Generic.Heading */
.highlight .gi  { color: #22863a; background-color: #f0fff4 } /* Generic.Inserted */
.highlight .go  { color: #6a737d } /* Generic.Output */
.highlight .gp  { color: #6a737d; font-weight: bold } /* Generic.Prompt */
.highlight .gs  { font-weight: bold } /* Generic.Strong */
.highlight .gu  { color: #6a737d; font-weight: bold } /* Generic.Subheading */
.highlight .gt  { color: #b31d28 } /* Generic.Traceback */
.highlight .kc  { color: #005cc5 } /* Keyword.Constant */
.highlight .kd  { color: #d73a49 } /* Keyword.Declaration */
.highlight .kn  { color: #d73a49 } /* Keyword.Namespace */
.highlight .kp  { color: #d73a49 } /* Keyword.Pseudo */
.highlight .kr  { color: #d73a49 } /* Keyword.Reserved */
.highlight .kt  { color: #6f42c1 } /* Keyword.Type */
.highlight .ld  { color: #032f62 } /* Literal.Date */
.highlight .m   { color: #005cc5 } /* Literal.Number */
.highlight .s   { color: #032f62 } /* Literal.String */
.highlight .na  { color: #6f42c1 } /* Name.Attribute */
.highlight .nb  { color: #005cc5 } /* Name.Builtin */
.highlight .nc  { color: #6f42c1 } /* Name.Class */
.highlight .no  { color: #005cc5 } /* Name.Constant */
.highlight .nd  { color: #6f42c1 } /* Name.Decorator */
.highlight .ni  { color: #24292e; font-weight: bold } /* Name.Entity */
.highlight .ne  { color: #d73a49 } /* Name.Exception */
.highlight .nf  { color: #6f42c1 } /* Name.Function */
.highlight .nl  { color: #005cc5 } /* Name.Label */
.highlight .nn  { color: #24292e } /* Name.Namespace */
.highlight .nx  { color: #6f42c1 } /* Name.Other */
.highlight .py  { color: #005cc5 } /* Name.Property */
.highlight .nt  { color: #22863a } /* Name.Tag */
.highlight .nv  { color: #e36209 } /* Name.Variable */
.highlight .ow  { color: #d73a49; font-weight: bold } /* Operator.Word */
.highlight .w   { color: #bbbbbb } /* Text.Whitespace */
.highlight .mb  { color: #005cc5 } /* Literal.Number.Bin */
.highlight .mf  { color: #005cc5 } /* Literal.Number.Float */
.highlight .mh  { color: #005cc5 } /* Literal.Number.Hex */
.highlight .mi  { color: #005cc5 } /* Literal.Number.Integer */
.highlight .mo  { color: #005cc5 } /* Literal.Number.Oct */
.highlight .sa  { color: #032f62 } /* Literal.String.Affix */
.highlight .sb  { color: #032f62 } /* Literal.String.Backtick */
.highlight .sc  { color: #032f62 } /* Literal.String.Char */
.highlight .dl  { color: #032f62 } /* Literal.String.Delimiter */
.highlight .sd  { color: #6a737d } /* Literal.String.Doc */
.highlight .s2  { color: #032f62 } /* Literal.String.Double */
.highlight .se  { color: #032f62 } /* Literal.String.Escape */
.highlight .sh  { color: #032f62 } /* Literal.String.Heredoc */
.highlight .si  { color: #005cc5 } /* Literal.String.Interpol */
.highlight .sx  { color: #032f62 } /* Literal.String.Other */
.highlight .sr  { color: #032f62 } /* Literal.String.Regex */
.highlight .s1  { color: #032f62 } /* Literal.String.Single */
.highlight .ss  { color: #005cc5 } /* Literal.String.Symbol */
.highlight .bp  { color: #005cc5 } /* Name.Builtin.Pseudo */
.highlight .fm  { color: #6f42c1 } /* Name.Function.Magic */
.highlight .il  { color: #005cc5 } /* Literal.Number.Integer.Long */
.highlight .vc  { color: #e36209 } /* Name.Variable.Class */
.highlight .vg  { color: #e36209 } /* Name.Variable.Global */
.highlight .vi  { color: #e36209 } /* Name.Variable.Instance */
.highlight .vm  { color: #e36209 } /* Name.Variable.Magic */
"""

# --------------------------------------------------------------------------- #
#  Print / PDF‑specific overrides                                              #
# --------------------------------------------------------------------------- #
PRINT_CSS = """
@page {
  size: A4;
  margin: 20mm 25mm;
}

@media print {
  body {
    margin: 0;
    padding: 0;
  }
  .markdown-body {
    max-width: none;
    padding: 0;
  }
  .markdown-body pre,
  .markdown-body code {
    word-wrap: break-word;
    white-space: pre-wrap;
  }
  .markdown-body pre {
    page-break-inside: avoid;
  }
  .markdown-body table {
    page-break-inside: avoid;
  }
  .markdown-body img {
    page-break-inside: avoid;
    max-width: 100%;
  }
  .markdown-body h1,
  .markdown-body h2,
  .markdown-body h3,
  .markdown-body h4,
  .markdown-body h5,
  .markdown-body h6 {
    page-break-after: avoid;
  }
  .markdown-body blockquote {
    page-break-inside: avoid;
  }
}
"""

# --------------------------------------------------------------------------- #
#  KaTeX overrides for PDF rendering                                           #
# --------------------------------------------------------------------------- #
KATEX_OVERRIDE_CSS = """
.katex-display {
  margin: 1em 0;
  text-align: center;
}
.katex-display > .katex {
  display: inline-block;
  text-align: initial;
}
.katex {
  font-size: 1.1em;
}
"""

# --------------------------------------------------------------------------- #
#  Mermaid diagram styling                                                      #
# --------------------------------------------------------------------------- #
MERMAID_CSS = """
.mermaid {
  text-align: center;
  margin: 1rem 0;
}
.mermaid svg {
  max-width: 100%;
  height: auto;
}
"""


def get_full_css(
    page_size: str = "A4",
    margin_top: str = "20mm",
    margin_bottom: str = "20mm",
    margin_left: str = "25mm",
    margin_right: str = "25mm",
    font_scale: float = 1.0,
) -> str:
    """Combine all CSS with custom page configuration.
    
    font_scale: multiplier applied to the base 16px font size.
    All headings use em units so they scale proportionally.
    e.g. 0.8 → 12.8px base, 1.5 → 24px base.
    """
    base_font_px = round(16 * font_scale, 2)
    page_css = f"""
@page {{
  size: {page_size};
  margin: {margin_top} {margin_right} {margin_bottom} {margin_left};
}}
"""
    font_scale_css = f"""
/* ── Font scale override ── */
.markdown-body {{
  font-size: {base_font_px}px;
}}
"""
    return "\n".join([
        page_css,
        GITHUB_MARKDOWN_CSS,
        font_scale_css,
        PYGMENTS_CSS,
        PRINT_CSS,
        KATEX_OVERRIDE_CSS,
        MERMAID_CSS,
    ])
