"""
Markdown → PDF Converter
========================
A Streamlit application that converts Markdown files into pixel-perfect,
GitHub-styled PDFs using headless Chromium rendering.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import base64
import subprocess
import sys
import time
from pathlib import Path

import streamlit as st

from converter import convert, md_to_html, ensure_playwright_browsers

# ── Auto-install Playwright Chromium (needed on cloud deployments) ────────────
@st.cache_resource(show_spinner="🌿 Setting up browser engine (first run only)…")
def _install_playwright():
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=False, capture_output=True
    )

_install_playwright()


# ──────────────────────────────────────────────────────────────────────────────
#  Page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MD → PDF Converter",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",   # sidebar hidden by default
)

# ──────────────────────────────────────────────────────────────────────────────
#  Light Green Theme CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  /* ── Global ──────────────────────────────────────────────────────────── */
  html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }
  .stApp {
    background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 40%, #ecfdf5 100%);
    min-height: 100vh;
  }

  /* ── Hide sidebar toggle (we moved settings inline) ─────────────────── */
  section[data-testid="stSidebar"] { display: none; }
  [data-testid="collapsedControl"]  { display: none; }

  /* ── Header ──────────────────────────────────────────────────────────── */
  .main-header {
    text-align: center;
    padding: 1.5rem 0 1rem;
  }
  .main-header h1 {
    background: linear-gradient(135deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    font-size: 2.6rem;
    margin-bottom: 0.2rem;
    letter-spacing: -0.03em;
  }
  .main-header p {
    color: #15803d;
    font-size: 1rem;
    font-weight: 400;
  }
  .main-header .leaf {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
    display: block;
    animation: float 3s ease-in-out infinite;
  }
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
  }

  /* ── Settings panel (expander) ───────────────────────────────────────── */
  .settings-panel {
    background: #ffffff;
    border: 1.5px solid #bbf7d0;
    border-radius: 18px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 16px rgba(16,185,129,0.07);
    margin-bottom: 1rem;
  }
  .settings-title {
    color: #059669;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  /* ── Streamlit expander styling ──────────────────────────────────────── */
  .streamlit-expanderHeader {
    background: #f0fdf4 !important;
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 14px !important;
    color: #166534 !important;
    font-weight: 600 !important;
    padding: 0.7rem 1rem !important;
  }
  .streamlit-expanderContent {
    background: #ffffff !important;
    border: 1.5px solid #bbf7d0 !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    padding: 1rem !important;
  }

  /* ── Tabs ────────────────────────────────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    background: #f0fdf4;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1.5px solid #bbf7d0;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #166534 !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
  }

  /* ── Upload area ─────────────────────────────────────────────────────── */
  .stFileUploader > div {
    border: 2px dashed rgba(16,185,129,0.5) !important;
    border-radius: 16px !important;
    background: rgba(16,185,129,0.04) !important;
    transition: all 0.3s ease;
  }
  .stFileUploader > div:hover {
    border-color: rgba(16,185,129,0.8) !important;
    background: rgba(16,185,129,0.08) !important;
  }

  /* ── Text area ───────────────────────────────────────────────────────── */
  .stTextArea textarea {
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    color: #1a2e1a !important;
    font-family: 'ui-monospace', 'SFMono-Regular', monospace !important;
    font-size: 0.875rem !important;
    transition: border-color 0.2s ease !important;
  }
  .stTextArea textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
  }

  /* ── Buttons ─────────────────────────────────────────────────────────── */
  .stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.35) !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(16,185,129,0.5) !important;
  }

  /* ── Stats badges ────────────────────────────────────────────────────── */
  .stat-badge {
    display: inline-block;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 0.35rem 0.85rem;
    color: #166534;
    font-size: 0.82rem;
    margin: 0.2rem;
    font-weight: 500;
  }
  .stat-badge strong { color: #059669; }

  /* ── Feature badges ──────────────────────────────────────────────────── */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 0.4rem;
    margin-top: 0.5rem;
  }
  .feature-tag {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 0.3rem 0.5rem;
    color: #166534;
    font-size: 0.75rem;
    text-align: center;
    font-weight: 500;
  }

  /* ── Success banner ──────────────────────────────────────────────────── */
  .success-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(52,211,153,0.12));
    border: 1.5px solid rgba(16,185,129,0.4);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: #166534;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  /* ── Green card ──────────────────────────────────────────────────────── */
  .green-card {
    background: #ffffff;
    border: 1.5px solid #bbf7d0;
    border-radius: 18px;
    padding: 1.75rem;
    box-shadow: 0 4px 20px rgba(16,185,129,0.08);
    margin-bottom: 1rem;
  }

  /* ── Inputs / selects ────────────────────────────────────────────────── */
  .stSelectbox [data-baseweb="select"] > div,
  .stTextInput > div > div > input {
    border-color: #bbf7d0 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #166534 !important;
  }
  .stCheckbox label span { color: #166534 !important; }
  hr { border-color: #bbf7d0 !important; }

  /* ── Mobile-friendly label colours ──────────────────────────────────── */
  label, .stMarkdown p { color: #166534; }

  /* ── Hide Streamlit branding ──────────────────────────────────────────── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Header
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <span class="leaf">🌿</span>
  <h1>Markdown → PDF</h1>
  <p>Convert <code>.md</code> files into pixel-perfect, GitHub-styled PDFs</p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ⚙️ Settings Panel (inline — works on mobile!)
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("⚙️ PDF Settings", expanded=False):
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        page_size = st.selectbox(
            "📐 Page Size",
            ["A4", "Letter", "Legal", "A3", "A5", "Tabloid"],
            index=0,
            help="Output PDF page size",
        )
        show_page_numbers = st.checkbox("Show page numbers", value=True)
        show_preview      = st.checkbox("Show HTML preview", value=True)

    with col2:
        st.markdown("**📏 Margins**")
        mc1, mc2 = st.columns(2)
        with mc1:
            margin_top    = st.text_input("Top",    value="20mm")
            margin_left   = st.text_input("Left",   value="25mm")
        with mc2:
            margin_bottom = st.text_input("Bottom", value="20mm")
            margin_right  = st.text_input("Right",  value="25mm")

    with col3:
        st.markdown("**🔤 Font Scale**")
        font_scale = st.slider(
            "Overall size",
            min_value=0.6, max_value=2.0, value=1.0, step=0.05,
            format="%.2fx",
            help="Scales all text proportionally. Headings stay bigger.",
        )
        st.caption(f"Base: **{round(16 * font_scale, 1)} px**")

        st.markdown("**🎨 Features**")
        features = [
            "📝 GFM","💻 Code","📊 Tables","✅ Tasks",
            "🧮 Math","📈 Mermaid","⚠️ Alerts","🔗 Links",
        ]
        feat_html = '<div class="feature-grid">' + "".join(
            f'<div class="feature-tag">{f}</div>' for f in features
        ) + '</div>'
        st.markdown(feat_html, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Input – Upload OR Paste (tabs)
# ──────────────────────────────────────────────────────────────────────────────
tab_upload, tab_paste = st.tabs(["📂 Upload File", "📋 Paste Markdown"])

md_content = None
file_stem  = "document"

with tab_upload:
    uploaded_file = st.file_uploader(
        "Drop your Markdown file here",
        type=["md", "markdown", "txt"],
        help="Supports .md, .markdown, and .txt files",
        key="file_upload",
    )
    if uploaded_file is not None:
        md_content = uploaded_file.read().decode("utf-8")
        file_stem  = Path(uploaded_file.name).stem

with tab_paste:
    pasted_text = st.text_area(
        "Paste your Markdown content here",
        height=300,
        placeholder="# Hello World\n\nPaste your **markdown** here and click Convert!\n\n- Item 1\n- Item 2",
        help="Paste any Markdown text directly — no file needed.",
        key="paste_input",
    )
    paste_filename = st.text_input(
        "Output filename (without extension)",
        value="document",
        key="paste_filename",
    )
    if pasted_text and pasted_text.strip():
        md_content = pasted_text
        file_stem  = paste_filename.strip() or "document"


# ──────────────────────────────────────────────────────────────────────────────
#  Main content
# ──────────────────────────────────────────────────────────────────────────────
if md_content:
    lines = md_content.count("\n") + 1
    words = len(md_content.split())
    chars = len(md_content)

    st.markdown(f"""
    <div style="text-align:center; margin:1rem 0;">
      <span class="stat-badge">📄 <strong>{file_stem}</strong></span>
      <span class="stat-badge">📏 <strong>{lines:,}</strong> lines</span>
      <span class="stat-badge">📝 <strong>{words:,}</strong> words</span>
      <span class="stat-badge">🔤 <strong>{chars:,}</strong> chars</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Preview ───────────────────────────────────────────────────────────
    if show_preview:
        with st.expander("📖 HTML Preview (GitHub-styled)", expanded=True):
            with st.spinner("⏳ Generating preview…"):
                html_preview = md_to_html(
                    md_content,
                    page_size=page_size,
                    margin_top=margin_top,
                    margin_bottom=margin_bottom,
                    margin_left=margin_left,
                    margin_right=margin_right,
                    font_scale=font_scale,
                )
            b64_html = base64.b64encode(html_preview.encode("utf-8")).decode("utf-8")
            st.markdown(
                f'<iframe src="data:text/html;base64,{b64_html}" '
                f'width="100%" height="680" '
                f'style="border:1.5px solid #bbf7d0; border-radius:14px; background:#fff;">'
                f'</iframe>',
                unsafe_allow_html=True,
            )

    # ── Convert button ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        convert_clicked = st.button("🚀 Convert to PDF", use_container_width=True, type="primary")

    if convert_clicked:
        for k in ("pdf_bytes", "pdf_name", "elapsed"):
            st.session_state.pop(k, None)

        with st.spinner("🔄 Rendering PDF with headless Chromium…"):
            start = time.time()
            try:
                pdf_bytes = convert(
                    md_content,
                    page_size=page_size,
                    margin_top=margin_top,
                    margin_bottom=margin_bottom,
                    margin_left=margin_left,
                    margin_right=margin_right,
                    display_header_footer=show_page_numbers,
                    font_scale=font_scale,
                )
                elapsed = time.time() - start
                st.session_state["pdf_bytes"] = pdf_bytes
                st.session_state["pdf_name"]  = f"{file_stem}.pdf"
                st.session_state["elapsed"]   = elapsed
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")
                st.exception(e)

    # ── Download ──────────────────────────────────────────────────────────
    if "pdf_bytes" in st.session_state:
        pdf_bytes = st.session_state["pdf_bytes"]
        pdf_name  = st.session_state["pdf_name"]
        elapsed   = st.session_state["elapsed"]
        size_kb   = len(pdf_bytes) / 1024

        st.markdown(f"""
        <div class="success-banner">
            ✅ PDF generated in <strong>{elapsed:.1f}s</strong>
            &nbsp;·&nbsp; Size: <strong>{size_kb:.1f} KB</strong>
        </div>
        """, unsafe_allow_html=True)

        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            st.markdown(f'''
                <a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_name}"
                   style="display:block; width:100%; text-align:center;
                          background:linear-gradient(135deg,#10b981,#059669);
                          color:white; text-decoration:none; padding:0.7rem 1.5rem;
                          border-radius:12px; font-weight:600; font-size:0.95rem;
                          box-shadow:0 4px 15px rgba(16,185,129,0.35);">
                   ⬇️ Download {pdf_name}
                </a>
            ''', unsafe_allow_html=True)

else:
    # ── Empty state ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="green-card" style="text-align:center; padding:2.5rem 2rem;">
      <div style="font-size:3rem; margin-bottom:0.6rem;">🌿</div>
      <h3 style="color:#166534; font-size:1.4rem; margin-bottom:0.6rem; font-weight:700;">
        Upload or paste your Markdown
      </h3>
      <p style="color:#4b7c59; max-width:520px; margin:0 auto; line-height:1.8; font-size:0.92rem;">
        Use the <strong>Upload File</strong> tab for a <code>.md</code> file,
        or <strong>Paste Markdown</strong> to type content directly.<br><br>
        Tap <strong>⚙️ PDF Settings</strong> above to adjust page size, margins, and font scale.
      </p>
    </div>
    """, unsafe_allow_html=True)
