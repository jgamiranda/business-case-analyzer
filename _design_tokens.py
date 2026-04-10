# ─────────────────────────────────────────────────────────────────────────────
# _design_tokens.py — Single source of truth for design system
# Per AGENT_BRIEF.md Section 4 — DO NOT improvise colours or fonts.
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st


# ─── Colour Tokens (exact values from Section 4.1) ───────────────────────────
TOKENS = {
    # Core
    "bg":        "#0d0f14",
    "surface":   "#141720",
    "surface_2": "#1c2030",
    "border":    "rgba(255,255,255,0.08)",
    "border_hi": "rgba(255,255,255,0.18)",
    "text":      "#e8eaf0",
    "muted":     "#6b7280",
    # Brand
    "accent":    "#3b82f6",
    "accent_2":  "#06b6d4",
    # Semantic
    "green":     "#10b981",
    "amber":     "#f59e0b",
    "red":       "#ef4444",
    "purple":    "#8b5cf6",
    # Module / entity colours
    "col_spv":       "#3b82f6",
    "col_sponsor":   "#8b5cf6",
    "col_lender":    "#10b981",
    "col_offtaker":  "#f59e0b",
    "col_epc":       "#ef4444",
    "col_om":        "#06b6d4",
    "col_govt":      "#f97316",
    "col_insurance": "#ec4899",
    "col_dsra":      "#14b8a6",
    "col_mla":       "#a78bfa",
    "col_dfi":       "#34d399",
    "col_custom":    "#94a3b8",
}


# ─── Status thresholds (Section 4.3) ─────────────────────────────────────────
def status_for(metric: str, value):
    """Return 'green' | 'amber' | 'red' | 'neutral' for a metric value.

    metric: one of 'irr', 'moic', 'dscr', 'debt_ebitda', 'icr', 'llcr'
    """
    if value is None:
        return "neutral"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "neutral"
    rules = {
        "irr":         lambda v: "green" if v > 25  else "amber" if v >= 20  else "red",
        "moic":        lambda v: "green" if v > 2.5 else "amber" if v >= 2.0 else "red",
        "dscr":        lambda v: "green" if v > 1.3 else "amber" if v >= 1.1 else "red",
        "debt_ebitda": lambda v: "green" if v < 4   else "amber" if v <= 6   else "red",
        "icr":         lambda v: "green" if v > 3   else "amber" if v >= 2   else "red",
        "llcr":        lambda v: "green" if v > 1.3 else "amber" if v >= 1.1 else "red",
    }
    fn = rules.get(metric)
    return fn(v) if fn else "neutral"


def status_color(status: str) -> str:
    """Map status name to hex colour."""
    return {
        "green":   TOKENS["green"],
        "amber":   TOKENS["amber"],
        "red":     TOKENS["red"],
        "neutral": TOKENS["accent"],
    }.get(status, TOKENS["accent"])


# ─── CSS — Single block to inject in every page ──────────────────────────────
DESIGN_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0d0f14;
  --surface: #141720;
  --surface-2: #1c2030;
  --border: rgba(255,255,255,0.08);
  --border-hi: rgba(255,255,255,0.18);
  --text: #e8eaf0;
  --muted: #6b7280;
  --accent: #3b82f6;
  --accent-2: #06b6d4;
  --green: #10b981;
  --amber: #f59e0b;
  --red: #ef4444;
  --purple: #8b5cf6;
  --font-display: 'Syne', sans-serif;
  --font-mono: 'DM Mono', monospace;
  --font-body: 'Syne', sans-serif;
}

/* ── Global background & text ────────────────────────────────────────────── */
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{
  background: var(--bg) !important;
}
[data-testid="stHeader"]{background: rgba(13,15,20,0.8) !important; backdrop-filter: blur(8px)}
.main .block-container{padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px}
body, .stApp, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li, label, span, div {
  font-family: var(--font-body) !important;
  color: var(--text) !important;
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display) !important;
  color: var(--text) !important;
  font-weight: 700 !important;
  letter-spacing: -0.01em;
}
h1{font-size: 1.6rem !important}
h2{font-size: 1.25rem !important}
h3{font-size: 1.05rem !important}
[data-testid="stCaption"], [data-testid="stCaption"] p {
  color: var(--muted) !important;
  font-size: 0.78rem !important;
  font-family: var(--font-body) !important;
}

/* ── Numbers always DM Mono ──────────────────────────────────────────────── */
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"],
.dm-mono,
input[type="number"],
[data-baseweb="input"] input,
[data-baseweb="select"] [data-testid="stSelectbox"] > div {
  font-family: var(--font-mono) !important;
}
[data-testid="stMetricValue"]{
  font-size: 1.65rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
}
[data-testid="stMetricLabel"]{
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted) !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
  gap: 4px;
  border-bottom: 1px solid var(--border);
  background: transparent;
}
.stTabs [data-baseweb="tab"]{
  background: transparent !important;
  color: var(--muted) !important;
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 10px 16px !important;
  border: none !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  transition: all .2s ease;
}
.stTabs [data-baseweb="tab"]:hover{
  color: var(--text) !important;
  border-bottom-color: var(--border-hi) !important;
}
.stTabs [aria-selected="true"]{
  color: var(--text) !important;
  border-bottom-color: var(--accent) !important;
  background: transparent !important;
}

/* ── Expanders ───────────────────────────────────────────────────────────── */
[data-testid="stExpander"] details{
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  margin-bottom: 8px;
}
[data-testid="stExpander"] details summary{
  background: var(--surface) !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  border: none !important;
}
[data-testid="stExpander"] details summary:hover{background: var(--surface-2) !important}
[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary span {
  color: var(--text) !important;
  font-family: var(--font-display) !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
}
[data-testid="stExpander"] details summary svg{fill: var(--text) !important; stroke: var(--text) !important}
[data-testid="stExpander"] details[open] summary{border-bottom: 1px solid var(--border) !important; border-radius: 12px 12px 0 0 !important}

/* ── Inputs ──────────────────────────────────────────────────────────────── */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] {
  background: var(--surface-2) !important;
  border-radius: 6px !important;
}
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: var(--surface-2) !important;
  color: var(--accent) !important;  /* Editable values are blue per Section 8 rule 2 */
  font-family: var(--font-mono) !important;
  font-size: 0.86rem !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
}
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 1px var(--accent) !important;
}
[data-baseweb="select"] > div {
  background: var(--surface-2) !important;
  color: var(--text) !important;
  font-family: var(--font-mono) !important;
  border: 1px solid var(--border) !important;
}
.stSlider [data-baseweb="slider"] > div > div > div{background: var(--accent) !important}
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"]{color: var(--muted) !important; font-family: var(--font-mono) !important}

/* Labels above inputs — micro spec */
.stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label, .stDateInput label, .stTextArea label {
  font-family: var(--font-display) !important;
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: 0.10em;
  color: var(--muted) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--surface-2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  font-family: var(--font-display) !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.04em;
  padding: 8px 16px !important;
  transition: all .15s ease;
}
.stButton > button:hover{
  background: var(--surface) !important;
  border-color: var(--border-hi) !important;
  transform: translateY(-1px);
}
.stButton > button[kind="primary"]{
  background: var(--accent) !important;
  border-color: var(--accent) !important;
  color: white !important;
}
.stButton > button[kind="primary"]:hover{
  background: #2563eb !important;
  border-color: #2563eb !important;
}

/* ── Metric Card (per Section 4.3 spec) ──────────────────────────────────── */
.ds-metric-card{
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 12px;
  padding: 16px 18px;
  height: 100%;
  transition: all .2s ease;
  position: relative;
  overflow: hidden;
}
.ds-metric-card:hover{
  border-color: var(--border-hi);
  transform: translateY(-1px);
}
.ds-metric-card.green{border-left-color: var(--green)}
.ds-metric-card.amber{border-left-color: var(--amber)}
.ds-metric-card.red{border-left-color: var(--red)}
.ds-metric-card.neutral{border-left-color: var(--accent)}
.ds-metric-card .ds-mc-label{
  font-family: var(--font-display);
  font-size: 0.56rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  margin-bottom: 6px;
}
.ds-metric-card .ds-mc-value{
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 4px;
}
.ds-metric-card.green .ds-mc-value{color: var(--green)}
.ds-metric-card.amber .ds-mc-value{color: var(--amber)}
.ds-metric-card.red .ds-mc-value{color: var(--red)}
.ds-metric-card .ds-mc-sub{
  font-family: var(--font-display);
  font-size: 0.68rem;
  color: var(--muted);
}

/* ── Tables / dataframes ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"],
[data-testid="stTable"]{
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
.df-styled, .sens-tbl{
  background: var(--surface) !important;
  border-radius: 12px !important;
  overflow: hidden;
  border: 1px solid var(--border);
}
.df-styled table, .sens-tbl table{
  background: transparent !important;
  font-family: var(--font-mono) !important;
}
.df-styled table thead th, .sens-tbl table thead th{
  background: var(--surface-2) !important;
  color: var(--text) !important;
  font-family: var(--font-display) !important;
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border: 1px solid var(--border) !important;
  padding: 10px 14px !important;
}
.df-styled table tbody th{
  background: var(--surface) !important;
  color: var(--text) !important;
  font-family: var(--font-display) !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  border: 1px solid var(--border) !important;
}
.df-styled table tbody td{
  background: var(--surface) !important;
  color: var(--text) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.82rem !important;
  border: 1px solid var(--border) !important;
}
.df-styled table tbody tr:hover td,
.df-styled table tbody tr:hover th{background: var(--surface-2) !important}

/* ── Alerts & verdict boxes (semantic) ───────────────────────────────────── */
[data-testid="stAlert"]{
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}
[data-testid="stAlert"] p, [data-testid="stAlert"] div{color: var(--text) !important}
[data-testid="stAlert"][data-baseweb="notification"] [kind="info"]{border-left: 3px solid var(--accent) !important}

.veredicto-verde{background: rgba(16,185,129,0.10) !important; border-left: 3px solid var(--green) !important; border-radius: 12px; padding: 18px 22px}
.veredicto-amarelo{background: rgba(245,158,11,0.10) !important; border-left: 3px solid var(--amber) !important; border-radius: 12px; padding: 18px 22px}
.veredicto-vermelho{background: rgba(239,68,68,0.10) !important; border-left: 3px solid var(--red) !important; border-radius: 12px; padding: 18px 22px}
.veredicto-titulo{font-family: var(--font-display); font-size: 1.35rem; font-weight: 800; margin-bottom: 6px}
.veredicto-verde .veredicto-titulo{color: var(--green) !important}
.veredicto-amarelo .veredicto-titulo{color: var(--amber) !important}
.veredicto-vermelho .veredicto-titulo{color: var(--red) !important}

.alerta-ok{background: rgba(16,185,129,0.10) !important; color: var(--green) !important; border-left: 3px solid var(--green); padding: 8px 14px; border-radius: 6px; margin: 4px 0; display: block; font-family: var(--font-body); font-size: 0.82rem}
.alerta-warn{background: rgba(245,158,11,0.10) !important; color: var(--amber) !important; border-left: 3px solid var(--amber); padding: 8px 14px; border-radius: 6px; margin: 4px 0; display: block; font-family: var(--font-body); font-size: 0.82rem}
.alerta-bad{background: rgba(239,68,68,0.10) !important; color: var(--red) !important; border-left: 3px solid var(--red); padding: 8px 14px; border-radius: 6px; margin: 4px 0; display: block; font-family: var(--font-body); font-size: 0.82rem}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"]{
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] *{color: var(--text) !important; font-family: var(--font-body) !important}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3{
  font-family: var(--font-display) !important;
}

/* ── Macro / dashboard cards (legacy fallback) ───────────────────────────── */
.macro-card{
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 14px 16px !important;
  text-align: center;
  transition: all .2s ease;
}
.macro-card:hover{transform: translateY(-2px); border-color: var(--border-hi)}
.macro-label{font-family: var(--font-display); font-size: 0.62rem; color: var(--muted) !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em}
.macro-value{font-family: var(--font-mono); font-size: 1.45rem; font-weight: 700; color: var(--accent) !important; margin: 4px 0}
.macro-date{font-family: var(--font-mono); font-size: 0.62rem; color: var(--muted) !important}

/* Section headers / dividers */
hr{border-color: var(--border) !important}
.linha-hdr{
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--muted) !important;
  font-size: 0.62rem;
  margin: 14px 0 4px 0;
  border-left: 2px solid var(--accent);
  padding-left: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Unit bar */
.unit-bar{
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px;
  padding: 10px 18px;
  margin-bottom: 8px;
}
.unit-label{
  font-family: var(--font-display);
  color: var(--text) !important;
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
}

/* Sidebar metric cards */
.sb-metric{
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: 10px 12px;
  margin: 6px 0;
  text-align: center;
}
.sb-metric .sb-val{font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: var(--accent) !important}
.sb-metric .sb-lbl{font-family: var(--font-display); font-size: 0.56rem; color: var(--muted) !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em}

/* Footer */
.app-footer{
  text-align: center;
  padding: 24px 0 12px 0;
  margin-top: 40px;
  border-top: 1px solid var(--border);
  color: var(--muted) !important;
  font-family: var(--font-body);
  font-size: 0.72rem;
}

/* Hide the old collapsed-sidebar control */
[data-testid="collapsedControl"]{display: none}
</style>
"""


def inject():
    """Call this at the top of every page to apply the design system."""
    st.markdown(DESIGN_CSS, unsafe_allow_html=True)


def metric_card(label: str, value: str, status: str = "neutral", sub: str = "") -> str:
    """Return HTML for a metric card per Section 4.3 spec.

    status: 'green' | 'amber' | 'red' | 'neutral'
    """
    sub_html = f'<div class="ds-mc-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="ds-metric-card {status}">'
        f'<div class="ds-mc-label">{label}</div>'
        f'<div class="ds-mc-value">{value}</div>'
        f'{sub_html}'
        f'</div>'
    )
