# 📄 Markdown → PDF Converter

A Streamlit-powered application that converts Markdown files into **pixel-perfect, GitHub-styled PDFs** using headless Chromium rendering.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **GitHub-accurate styling** | Uses the official GitHub Markdown CSS for pixel-perfect rendering |
| 💻 **Syntax highlighting** | Pygments-powered code highlighting with GitHub's color theme |
| 🧮 **Math equations** | Full KaTeX support for inline (`$...$`) and display (`$$...$$`) math |
| 📈 **Mermaid diagrams** | Flowcharts, sequence diagrams, and more rendered via Mermaid.js |
| ⚠️ **GitHub alerts** | `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, etc. with proper icons |
| ✅ **Task lists** | GitHub-style checkboxes |
| 📝 **Footnotes** | Standard footnote syntax |
| 📊 **Tables** | Full GFM table support with alternating row colors |
| 🔢 **Page numbers** | Optional page number footer |
| 📐 **Customizable layout** | Page size (A4/Letter/etc.) and margin controls |

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Chromium for Playwright

```bash
python -m playwright install chromium
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 📁 Project Structure

```
md-to-pdf/
├── app.py              # Streamlit web interface
├── converter.py         # Core Markdown → HTML → PDF engine
├── styles.py            # GitHub CSS, Pygments theme, print styles
├── requirements.txt     # Python dependencies
├── test_sample.md       # Comprehensive test/demo file
└── README.md            # This file
```

## 🔧 How It Works

```
Markdown File
     │
     ▼
┌─────────────┐    markdown-it-py + plugins
│  Parse MD   │    (GFM, footnotes, math, task-lists)
└──────┬──────┘
       │
       ▼
┌─────────────┐    Pygments syntax highlighting
│ Render HTML │    GitHub CSS styling
│             │    KaTeX / Mermaid JS injection
└──────┬──────┘
       │
       ▼
┌─────────────┐    Headless Chromium via Playwright
│ Generate    │    Chrome-quality rendering
│ PDF         │    Proper page breaks, backgrounds
└──────┬──────┘
       │
       ▼
   PDF File ✅
```

## 🛠️ Tech Stack

- **[markdown-it-py](https://github.com/executablebooks/markdown-it-py)** — Python port of markdown-it, the same parser used by many modern tools
- **[Pygments](https://pygments.org/)** — Syntax highlighting with GitHub's light theme
- **[Playwright](https://playwright.dev/python/)** — Headless Chromium for pixel-perfect PDF generation
- **[KaTeX](https://katex.org/)** — Fast math rendering (loaded via CDN)
- **[Mermaid](https://mermaid.js.org/)** — Diagram rendering (loaded via CDN)
- **[Streamlit](https://streamlit.io/)** — Web interface

## 📋 Python API Usage

You can also use the converter programmatically:

```python
from converter import convert

# Read your markdown
with open("document.md", encoding="utf-8") as f:
    md_content = f.read()

# Convert to PDF
pdf_bytes = convert(
    md_content,
    page_size="A4",
    margin_top="20mm",
    margin_bottom="20mm",
    margin_left="25mm",
    margin_right="25mm",
    display_header_footer=True,  # page numbers
)

# Save
with open("document.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## 📝 License

MIT
