import streamlit as st
import _design_tokens as ds

st.set_page_config(
    page_title="Financial Modeling Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global design system (Section 4 of AGENT_BRIEF.md)
# DISABLED 2026-04-10: dark theme conflicts with light-theme model pages —
# breaks buttons / widgets. Re-enable after frontend migrates all pages.
# ds.inject()

# ─── Page-specific CSS (landing-only components) ─────────────────────────────
st.markdown("""
<style>
.model-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
  gap:18px;
  margin:20px 0;
}
.model-card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:14px;
  padding:24px 22px;
  transition:all .2s ease;
  position:relative;
  overflow:hidden;
}
.model-card::before{
  content:"";
  position:absolute;top:0;left:0;right:0;height:2px;
  background:var(--accent);
  opacity:0;transition:opacity .2s ease;
}
.model-card:hover{
  border-color:var(--border-hi);
  transform:translateY(-3px);
  box-shadow:0 8px 30px rgba(0,0,0,.4);
}
.model-card:hover::before{opacity:1}
.model-card .mc-icon{font-size:2.4rem;margin-bottom:10px;display:block}
.model-card .mc-title{
  font-family:var(--font-display);
  font-size:1.05rem;
  font-weight:800;
  color:var(--text);
  margin-bottom:6px;
  letter-spacing:-0.01em;
}
.model-card .mc-sub{
  font-family:var(--font-body);
  font-size:.78rem;
  color:var(--muted);
  line-height:1.55;
  margin-bottom:14px;
}
.model-card .mc-tags{display:flex;flex-wrap:wrap;gap:6px}
.model-card .mc-tag{
  background:var(--surface-2);
  color:var(--accent);
  font-family:var(--font-display);
  font-size:.56rem;
  font-weight:700;
  padding:4px 9px;
  border-radius:10px;
  text-transform:uppercase;
  letter-spacing:.08em;
  border:1px solid var(--border);
}
.model-card .mc-badge{
  position:absolute;top:14px;right:14px;
  background:rgba(16,185,129,0.15);
  color:var(--green);
  font-family:var(--font-display);
  font-size:.56rem;
  font-weight:700;
  padding:3px 9px;
  border-radius:8px;
  text-transform:uppercase;
  letter-spacing:.08em;
  border:1px solid rgba(16,185,129,0.3);
}
.model-card .mc-badge-soon{
  background:rgba(245,158,11,0.15);
  color:var(--amber);
  border-color:rgba(245,158,11,0.3);
}
.hero-bar{
  background:linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border);
  border-radius:16px;
  padding:36px 40px;
  margin-bottom:24px;
  position:relative;
  overflow:hidden;
}
.hero-bar::before{
  content:"";
  position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg, var(--accent) 0%, var(--accent-2) 100%);
}
.hero-bar h1{
  font-family:var(--font-display) !important;
  font-size:1.8rem !important;
  font-weight:800;
  margin:0 0 6px 0;
  color:var(--text) !important;
  letter-spacing:-0.02em;
}
.hero-bar p{
  font-family:var(--font-body);
  font-size:.92rem;
  color:var(--muted) !important;
  margin:0;
  line-height:1.6;
  max-width:720px;
}
.platform-footer{
  text-align:center;
  padding:24px 0 12px 0;
  margin-top:40px;
  border-top:1px solid var(--border);
  color:var(--muted) !important;
  font-family:var(--font-body);
  font-size:.72rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Language toggle ─────────────────────────────────────────────────────────
_lc1, _lc2 = st.columns([8, 1])
with _lc2:
    _lang_sel = st.segmented_control("lang_home", ["PT", "EN"], default="PT",
                                      key="home_lang", label_visibility="collapsed")
lang = _lang_sel or "PT"

# ─── Hero ────────────────────────────────────────────────────────────────────
if lang == "PT":
    _hero_title = "Plataforma de Modelagem Financeira"
    _hero_sub = ("Selecione o tipo de modelo que deseja construir. "
                 "Cada modelo possui premissas, calculos e demonstracoes especificas "
                 "para o seu caso de uso.")
    _select_label = "Selecione um modelo para comecar"
else:
    _hero_title = "Financial Modeling Platform"
    _hero_sub = ("Select the type of model you want to build. "
                 "Each model has specific assumptions, calculations and statements "
                 "tailored to your use case.")
    _select_label = "Select a model to get started"

st.markdown(f"""
<div class="hero-bar">
    <h1>{_hero_title}</h1>
    <p>{_hero_sub}</p>
</div>
""", unsafe_allow_html=True)

# ─── Model definitions ──────────────────────────────────────────────────────
MODELS = [
    {
        "key": "business_case", "icon": "📋",
        "title": {"PT": "Business Case", "EN": "Business Case"},
        "sub": {
            "PT": "Analise de viabilidade para novos projetos, expansoes ou investimentos. "
                  "Fluxo de caixa operacional, financiamento por divida, DRE/DFC/BP anuais, "
                  "sensibilidade e Monte Carlo.",
            "EN": "Viability analysis for new projects, expansions or investments. "
                  "Operational cash flow, debt financing, annual statements, "
                  "sensitivity analysis and Monte Carlo.",
        },
        "tags": ["NPV", "IRR", "Payback", "DRE", "WACC", "Monte Carlo"],
        "badge": {"PT": "Disponivel", "EN": "Available"}, "ready": True,
        "page": "pages/01_Business_Case.py",
    },
    {
        "key": "ma", "icon": "🤝",
        "title": {"PT": "M&A — Fusoes e Aquisicoes", "EN": "M&A — Mergers & Acquisitions"},
        "sub": {
            "PT": "Avaliacao de targets, sinergias de receita e custo, analise de "
                  "acrecao/diluicao, purchase price allocation e pro-forma consolidado.",
            "EN": "Target valuation, revenue & cost synergies, accretion/dilution analysis, "
                  "purchase price allocation and consolidated pro-forma.",
        },
        "tags": ["EV/EBITDA", "Sinergias", "Acrecao/Diluicao", "PPA", "Pro-forma"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/02_MA.py",
    },
    {
        "key": "project_finance", "icon": "🏗️",
        "title": {"PT": "Project Finance", "EN": "Project Finance"},
        "sub": {
            "PT": "Modelagem de projetos de infraestrutura com fase de construcao, "
                  "debt sizing baseado em DSCR, waterfall de caixa e retornos.",
            "EN": "Infrastructure project modeling with construction phase, "
                  "DSCR-based debt sizing, cash waterfall and returns.",
        },
        "tags": ["DSCR", "LLCR", "Waterfall", "IDC", "Debt Sizing"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/03_Project_Finance.py",
    },
    {
        "key": "valuation_dcf", "icon": "📊",
        "title": {"PT": "Valuation DCF", "EN": "Valuation DCF"},
        "sub": {
            "PT": "Avaliacao de empresas por fluxo de caixa descontado. CAPM, WACC, "
                  "valor terminal por Gordon Growth ou multiplo de saida.",
            "EN": "Company valuation via discounted cash flow. CAPM, WACC, "
                  "terminal value via Gordon Growth or exit multiple.",
        },
        "tags": ["CAPM", "WACC", "Terminal Value", "FCFF", "FCFE"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/04_Valuation_DCF.py",
    },
    {
        "key": "lbo", "icon": "💼",
        "title": {"PT": "LBO — Leveraged Buyout", "EN": "LBO — Leveraged Buyout"},
        "sub": {
            "PT": "Modelagem de aquisicoes alavancadas: Sources & Uses, debt schedule "
                  "multi-tranche, IRR/MOIC, value creation bridge e exit waterfall.",
            "EN": "Leveraged buyout modeling: Sources & Uses, multi-tranche debt schedule, "
                  "IRR/MOIC, value creation bridge and exit waterfall.",
        },
        "tags": ["Sources & Uses", "TLA/TLB", "MOIC", "IRR", "Exit Multiple", "PIK"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/05_LBO.py",
    },
    {
        "key": "startup", "icon": "🚀",
        "title": {"PT": "Startup — Cap Table", "EN": "Startup — Cap Table"},
        "sub": {
            "PT": "Cap table, diluicao por rodada, unit economics (CAC/LTV/Churn), "
                  "runway e projecao de MRR/ARR.",
            "EN": "Cap table, round-by-round dilution, unit economics (CAC/LTV/Churn), "
                  "runway and MRR/ARR projection.",
        },
        "tags": ["Cap Table", "MRR/ARR", "CAC/LTV", "Runway"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/06_Startup.py",
    },
    {
        "key": "hedging", "icon": "🛡️",
        "title": {"PT": "Hedging Strategies", "EN": "Hedging Strategies"},
        "sub": {
            "PT": "Forwards, futuros, IRS, cross-currency swaps, total return swaps. "
                  "Pricing institucional baseado em ISDA, CME, e bancos de investimento.",
            "EN": "Forwards, futures, IRS, cross-currency swaps, total return swaps. "
                  "Institutional pricing based on ISDA, CME, and investment bank standards.",
        },
        "tags": ["FX Forward", "IRS", "CCS", "TRS", "Futures", "DV01"],
        "badge": {"PT": "Novo", "EN": "New"}, "ready": True,
        "page": "pages/07_Hedging_Strategies.py",
    },
]

# ─── Render cards (clickable via Streamlit page URLs) ───────────────────────
st.markdown(f"### {_select_label}")

# Map each model to its Streamlit-served URL (numeric prefix stripped by Streamlit)
_PAGE_URLS = {
    "business_case":   "/Business_Case",
    "ma":              "/MA",
    "project_finance": "/Project_Finance",
    "valuation_dcf":   "/Valuation_DCF",
    "lbo":             "/LBO",
    "startup":         "/Startup",
    "hedging":         "/Hedging_Strategies",
}

_cards_html = '<div class="model-grid">'
for m in MODELS:
    tags_html = "".join(f'<span class="mc-tag">{t}</span>' for t in m["tags"])
    badge_cls = "mc-badge" if m["key"] == "business_case" else "mc-badge mc-badge-soon"
    href = _PAGE_URLS.get(m["key"], "#")
    _cards_html += f"""
    <a href="{href}" target="_self" style="text-decoration:none;color:inherit;display:block">
      <div class="model-card">
          <span class="{badge_cls}">{m['badge'][lang]}</span>
          <div class="mc-icon">{m['icon']}</div>
          <div class="mc-title">{m['title'][lang]}</div>
          <div class="mc-sub">{m['sub'][lang]}</div>
          <div class="mc-tags">{tags_html}</div>
      </div>
    </a>"""
_cards_html += '</div>'
st.markdown(_cards_html, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="platform-footer">
    Financial Modeling Platform v3.2 — Powered by Streamlit + Plotly<br>
    Business Case · M&A · Project Finance · Valuation DCF · Startup · Hedging · LBO
</div>
""", unsafe_allow_html=True)
