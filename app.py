import streamlit as st

st.set_page_config(
    page_title="Financial Modeling Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.model-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;margin:20px 0}
.model-card{background:white;border:2px solid #e5e7eb;border-radius:16px;padding:28px 24px;
    transition:all .2s ease;cursor:pointer;position:relative;overflow:hidden}
.model-card:hover{border-color:#1a56db;box-shadow:0 8px 30px rgba(26,86,219,.15);transform:translateY(-2px)}
.model-card .mc-icon{font-size:2.8rem;margin-bottom:12px}
.model-card .mc-title{font-size:1.3rem;font-weight:800;color:#1e3a8a;margin-bottom:6px}
.model-card .mc-sub{font-size:.88rem;color:#6b7280;line-height:1.5;margin-bottom:14px}
.model-card .mc-tags{display:flex;flex-wrap:wrap;gap:6px}
.model-card .mc-tag{background:#dbeafe;color:#1e3a8a;font-size:.72rem;font-weight:700;
    padding:3px 10px;border-radius:12px;text-transform:uppercase;letter-spacing:.03em}
.model-card .mc-badge{position:absolute;top:16px;right:16px;background:#16a34a;color:white;
    font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:12px;text-transform:uppercase}
.model-card .mc-badge-soon{background:#f97316}
.hero-bar{background:linear-gradient(135deg,#1e3a8a 0%,#1a56db 100%);border-radius:16px;
    padding:40px 44px;margin-bottom:30px;color:white}
.hero-bar h1{font-size:2.2rem;font-weight:800;margin:0 0 8px 0;color:white !important}
.hero-bar p{font-size:1rem;color:#bfdbfe;margin:0;line-height:1.6}
.platform-footer{text-align:center;padding:30px 0 10px 0;margin-top:50px;
    border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.78rem}
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
        "page": "pages/05_Startup.py",
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
        "page": "pages/06_Hedging.py",
    },
]

# ─── Render cards ────────────────────────────────────────────────────────────
st.markdown(f"### {_select_label}")

_cards_html = '<div class="model-grid">'
for m in MODELS:
    tags_html = "".join(f'<span class="mc-tag">{t}</span>' for t in m["tags"])
    badge_cls = "mc-badge" if m["key"] == "business_case" else "mc-badge mc-badge-soon"
    _cards_html += f"""
    <div class="model-card">
        <span class="{badge_cls}">{m['badge'][lang]}</span>
        <div class="mc-icon">{m['icon']}</div>
        <div class="mc-title">{m['title'][lang]}</div>
        <div class="mc-sub">{m['sub'][lang]}</div>
        <div class="mc-tags">{tags_html}</div>
    </div>"""
_cards_html += '</div>'
st.markdown(_cards_html, unsafe_allow_html=True)

# Navigation buttons
st.markdown("---")
cols = st.columns(len(MODELS))
for i, (col, m) in enumerate(zip(cols, MODELS)):
    with col:
        _btn_label = f"{m['icon']}  {m['title'][lang]}"
        if st.button(_btn_label, use_container_width=True,
                     type="primary" if m["key"] == "business_case" else "secondary"):
            st.switch_page(m["page"])

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="platform-footer">
    Financial Modeling Platform v3.0 — Powered by Streamlit + Plotly<br>
    Business Case · M&A · Project Finance · Valuation DCF · Startup
</div>
""", unsafe_allow_html=True)
