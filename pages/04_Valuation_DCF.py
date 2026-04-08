"""
04_Valuation_DCF.py — Streamlit page: DCF Valuation Model
Self-contained, bilingual PT/EN, blue theme (#1a56db).
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Valuation DCF", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "title": "Modelo de Valuation — DCF",
    "dark_mode": "Modo Escuro",
    # Tabs
    "tab_company": "  Empresa  ",
    "tab_proj": "  Projecoes  ",
    "tab_wacc": "  WACC  ",
    "tab_tv": "  Valor Terminal  ",
    "tab_val": "  Valuation  ",
    "tab_sens": "  Sensibilidade  ",
    # Company
    "company_name": "Nome da empresa",
    "company_name_ph": "Ex: Petrobras",
    "sector": "Setor",
    "current_revenue": "Receita atual (R$ MM)",
    "ebitda_margin": "Margem EBITDA atual (%)",
    "net_income": "Lucro liquido (R$ MM)",
    "shares_out": "Acoes em circulacao (MM)",
    "share_price": "Preco atual da acao (R$)",
    "company_info": "Preencha os dados basicos da empresa para alimentar o modelo DCF.",
    # Projections
    "proj_years": "Anos de projecao",
    "rev_growth": "Crescimento de receita (%) — Ano {y}",
    "ebitda_margin_y": "Margem EBITDA (%) — Ano {y}",
    "capex_pct": "CapEx como % da receita",
    "da_pct": "D&A como % da receita",
    "nwc_pct": "Variacao de Capital de Giro como % da receita",
    "tax_rate": "Aliquota de imposto (%)",
    "proj_info": "Defina as premissas de projecao para o horizonte selecionado.",
    "sec_rev_growth": "Crescimento de Receita",
    "sec_margins": "Margens e Custos",
    # WACC
    "risk_free": "Taxa livre de risco (%)",
    "erp": "Premio de risco de mercado (%)",
    "beta": "Beta",
    "cost_debt": "Custo da divida pre-tax (%)",
    "tax_wacc": "Aliquota de imposto (%)",
    "de_ratio": "Relacao D/E",
    "calc_wacc": "WACC Calculado",
    "cost_equity": "Custo do Equity (Ke)",
    "cost_debt_at": "Custo da Divida pos-tax (Kd)",
    "weight_e": "Peso do Equity",
    "weight_d": "Peso da Divida",
    "wacc_info": "Calculo do WACC via CAPM. Ajuste os parametros abaixo.",
    # Terminal Value
    "tv_method": "Metodo de valor terminal",
    "gordon": "Gordon Growth (Perpetuidade)",
    "exit_mult": "Multiplo de Saida (EV/EBITDA)",
    "perp_growth": "Taxa de crescimento na perpetuidade (%)",
    "exit_multiple": "Multiplo EV/EBITDA de saida",
    "tv_info": "Selecione o metodo e as premissas para o valor terminal.",
    # Valuation
    "val_title": "Resultado do Valuation",
    "year": "Ano",
    "revenue": "Receita",
    "ebitda": "EBITDA",
    "da": "(-) D&A",
    "ebit": "EBIT",
    "taxes": "(-) Impostos",
    "nopat": "NOPAT",
    "plus_da": "(+) D&A",
    "minus_capex": "(-) CapEx",
    "minus_nwc": "(-) Var. Capital de Giro",
    "fcff": "FCFF",
    "pv_fcff": "VP do FCFF",
    "sum_pv_fcf": "Soma VP dos FCFs",
    "pv_tv": "VP do Valor Terminal",
    "enterprise_value": "Enterprise Value (EV)",
    "net_debt": "(-) Divida Liquida",
    "equity_value": "Equity Value",
    "shares": "Acoes em circulacao (MM)",
    "price_per_share": "Valor por acao",
    "current_price": "Preco atual",
    "upside": "Upside / Downside",
    "tv_pct_ev": "% do EV vindo do Valor Terminal",
    "bridge_title": "Bridge: EV para Equity Value",
    "enter_net_debt": "Divida liquida (R$ MM)",
    "val_info": "Calculo completo do FCFF, valor presente e ponte para valor por acao.",
    # Sensitivity
    "sens_title": "Analise de Sensibilidade",
    "sens_wacc_label": "Faixa de WACC (%)",
    "sens_growth_label": "Faixa de crescimento perpetuo (%)",
    "sens_exit_label": "Faixa de multiplo de saida (x)",
    "sens_info": "Tabela bidimensional e grafico football field.",
    "football_title": "Football Field — Faixa de Valor por Acao",
    "implied_price": "Preco Implicito por Acao (R$)",
    "current_price_line": "Preco Atual",
    "scenario": "Cenario",
},
"EN": {
    "title": "Valuation Model — DCF",
    "dark_mode": "Dark Mode",
    "tab_company": "  Company  ",
    "tab_proj": "  Projections  ",
    "tab_wacc": "  WACC  ",
    "tab_tv": "  Terminal Value  ",
    "tab_val": "  Valuation  ",
    "tab_sens": "  Sensitivity  ",
    "company_name": "Company name",
    "company_name_ph": "E.g.: Apple Inc.",
    "sector": "Sector",
    "current_revenue": "Current revenue ($ MM)",
    "ebitda_margin": "Current EBITDA margin (%)",
    "net_income": "Net income ($ MM)",
    "shares_out": "Shares outstanding (MM)",
    "share_price": "Current share price ($)",
    "company_info": "Fill in the company basics to feed the DCF model.",
    "proj_years": "Projection years",
    "rev_growth": "Revenue growth (%) — Year {y}",
    "ebitda_margin_y": "EBITDA margin (%) — Year {y}",
    "capex_pct": "CapEx as % of revenue",
    "da_pct": "D&A as % of revenue",
    "nwc_pct": "Change in NWC as % of revenue",
    "tax_rate": "Tax rate (%)",
    "proj_info": "Set projection assumptions for the selected horizon.",
    "sec_rev_growth": "Revenue Growth",
    "sec_margins": "Margins & Costs",
    "risk_free": "Risk-free rate (%)",
    "erp": "Equity risk premium (%)",
    "beta": "Beta",
    "cost_debt": "Pre-tax cost of debt (%)",
    "tax_wacc": "Tax rate (%)",
    "de_ratio": "D/E ratio",
    "calc_wacc": "Calculated WACC",
    "cost_equity": "Cost of Equity (Ke)",
    "cost_debt_at": "After-tax Cost of Debt (Kd)",
    "weight_e": "Equity Weight",
    "weight_d": "Debt Weight",
    "wacc_info": "WACC calculation via CAPM. Adjust the parameters below.",
    "tv_method": "Terminal value method",
    "gordon": "Gordon Growth (Perpetuity)",
    "exit_mult": "Exit Multiple (EV/EBITDA)",
    "perp_growth": "Perpetuity growth rate (%)",
    "exit_multiple": "Exit EV/EBITDA multiple",
    "tv_info": "Select the method and assumptions for terminal value.",
    "val_title": "Valuation Result",
    "year": "Year",
    "revenue": "Revenue",
    "ebitda": "EBITDA",
    "da": "(-) D&A",
    "ebit": "EBIT",
    "taxes": "(-) Taxes",
    "nopat": "NOPAT",
    "plus_da": "(+) D&A",
    "minus_capex": "(-) CapEx",
    "minus_nwc": "(-) Change in NWC",
    "fcff": "FCFF",
    "pv_fcff": "PV of FCFF",
    "sum_pv_fcf": "Sum of PV of FCFs",
    "pv_tv": "PV of Terminal Value",
    "enterprise_value": "Enterprise Value (EV)",
    "net_debt": "(-) Net Debt",
    "equity_value": "Equity Value",
    "shares": "Shares outstanding (MM)",
    "price_per_share": "Price per share",
    "current_price": "Current price",
    "upside": "Upside / Downside",
    "tv_pct_ev": "% of EV from Terminal Value",
    "bridge_title": "Bridge: EV to Equity Value",
    "enter_net_debt": "Net debt ($ MM)",
    "val_info": "Full FCFF calculation, present value, and bridge to per-share value.",
    "sens_title": "Sensitivity Analysis",
    "sens_wacc_label": "WACC range (%)",
    "sens_growth_label": "Perpetuity growth range (%)",
    "sens_exit_label": "Exit multiple range (x)",
    "sens_info": "Two-dimensional table and football field chart.",
    "football_title": "Football Field — Price per Share Range",
    "implied_price": "Implied Price per Share ($)",
    "current_price_line": "Current Price",
    "scenario": "Scenario",
},
}

SECTORS_PT = ["Tecnologia", "Financeiro", "Saude", "Energia", "Varejo",
              "Industria", "Telecomunicacoes", "Materiais Basicos", "Outro"]
SECTORS_EN = ["Technology", "Financials", "Healthcare", "Energy", "Retail",
              "Industrials", "Telecom", "Basic Materials", "Other"]

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Blue theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"]{display:none}
.stTabs [data-baseweb="tab-list"]{gap:5px}
.stTabs [data-baseweb="tab"]{background:#dbeafe;border-radius:6px 6px 0 0;color:#1a56db;
    font-weight:600;padding:8px 18px;border:1px solid #bfdbfe;border-bottom:none;transition:all .2s ease}
.stTabs [data-baseweb="tab"]:hover{background:#1a56db;color:white;transform:translateY(-1px)}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:white !important;border-color:#1a56db !important}
[data-testid="stExpander"] details summary{background:#1a56db !important;border-radius:6px !important;
    padding:10px 16px !important;transition:background .2s ease}
[data-testid="stExpander"] details summary:hover{background:#1e429f !important}
[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary span{color:white !important;font-weight:600 !important}
[data-testid="stExpander"] details summary svg{fill:white !important;stroke:white !important}
[data-testid="stExpander"] details{border:1px solid #1a56db !important;border-radius:6px !important}
.metric-card{background:linear-gradient(135deg,#f0f7ff 0%,#dbeafe 100%);border:1px solid #bfdbfe;
    border-radius:10px;padding:16px 18px;text-align:center;transition:all .2s ease}
.metric-card:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(26,86,219,.14)}
.metric-card .mc-label{font-size:.72rem;color:#6b7280;font-weight:700;text-transform:uppercase;
    letter-spacing:.04em;margin-bottom:4px}
.metric-card .mc-value{font-size:1.5rem;font-weight:800;color:#1a56db;margin:2px 0}
.metric-card .mc-delta{font-size:.78rem;font-weight:600;margin-top:2px}
.mc-pos{color:#16a34a}.mc-neg{color:#dc2626}
.metric-card-green{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-color:#a3d9a5}
.metric-card-green .mc-value{color:#16a34a}
.metric-card-red{background:linear-gradient(135deg,#f8d7da 0%,#f5c6cb 100%);border-color:#f1aeb5}
.metric-card-red .mc-value{color:#dc2626}
.unit-bar{background:linear-gradient(90deg,#1a56db 0%,#1e429f 100%);border-radius:8px;
    padding:10px 20px;margin-bottom:6px}
.unit-label{color:white;font-weight:700;font-size:.95rem}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER + LANGUAGE + DARK MODE
# ─────────────────────────────────────────────────────────────────────────────
if "dark_mode_dcf" not in st.session_state:
    st.session_state["dark_mode_dcf"] = False

_hc_title, _hc_lang, _hc_dark = st.columns([6, 1, 1])

with _hc_lang:
    st.write("")
    lang_sel = st.segmented_control("lang_dcf", ["PT", "EN"], default="PT",
                                    key="lang_dcf", label_visibility="collapsed")
lang = lang_sel or "PT"

def T(k):
    return _L.get(lang, _L["PT"]).get(k, _L["PT"].get(k, k))

with _hc_dark:
    st.write("")
    dark_mode = st.toggle(T("dark_mode"), key="dark_mode_dcf")

_hc_title.title(T("title"))

if dark_mode:
    st.markdown("""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#0f172a !important}
p,h1,h2,h3,h4,label,li{color:#e2e8f0 !important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#e2e8f0 !important}
[data-testid="stCaption"] p,.stCaption p{color:#94a3b8 !important}
[data-testid="stExpander"] details{background:#1e293b !important;border-color:#334155 !important}
</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DCF_DEFAULTS = {
    "dcf_company_name": "",
    "dcf_sector": 0,
    "dcf_revenue": 1000.0,
    "dcf_ebitda_margin": 25.0,
    "dcf_net_income": 100.0,
    "dcf_shares": 500.0,
    "dcf_share_price": 20.0,
    "dcf_proj_years": 5,
    "dcf_capex_pct": 5.0,
    "dcf_da_pct": 4.0,
    "dcf_nwc_pct": 1.0,
    "dcf_tax_rate": 34.0,
    "dcf_risk_free": 5.0,
    "dcf_erp": 6.0,
    "dcf_beta": 1.0,
    "dcf_cost_debt": 8.0,
    "dcf_tax_wacc": 34.0,
    "dcf_de_ratio": 0.5,
    "dcf_tv_method": 0,
    "dcf_perp_growth": 3.0,
    "dcf_exit_multiple": 8.0,
    "dcf_net_debt": 200.0,
}

for k, v in _DCF_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Per-year growth/margin defaults
for y in range(1, 11):
    gk = f"dcf_rev_growth_{y}"
    mk = f"dcf_ebitda_margin_{y}"
    if gk not in st.session_state:
        st.session_state[gk] = 10.0 if y <= 3 else 7.0 if y <= 5 else 4.0
    if mk not in st.session_state:
        st.session_state[mk] = 25.0

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: metric card
# ─────────────────────────────────────────────────────────────────────────────
def _mc(label, value, delta=None, color=None):
    cls = "metric-card"
    if color == "green":
        cls = "metric-card metric-card-green"
    elif color == "red":
        cls = "metric-card metric-card-red"
    delta_html = ""
    if delta is not None:
        d_cls = "mc-pos" if delta >= 0 else "mc-neg"
        d_sign = "+" if delta >= 0 else ""
        delta_html = f'<div class="mc-delta {d_cls}">{d_sign}{delta:.1f}%</div>'
    return f"""<div class="{cls}">
<div class="mc-label">{label}</div>
<div class="mc-value">{value}</div>
{delta_html}</div>"""

def fmt_mm(v):
    """Format value in MM with 1 decimal."""
    if abs(v) >= 1_000:
        return f"{v:,.0f}"
    return f"{v:,.1f}"

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    T("tab_company"), T("tab_proj"), T("tab_wacc"),
    T("tab_tv"), T("tab_val"), T("tab_sens"),
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — COMPANY
# ═════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.info(T("company_info"))
    sectors = SECTORS_EN if lang == "EN" else SECTORS_PT

    c1, c2 = st.columns(2)
    with c1:
        st.text_input(T("company_name"), placeholder=T("company_name_ph"),
                      key="dcf_company_name")
        st.selectbox(T("sector"), sectors, key="dcf_sector")
        st.number_input(T("current_revenue"), min_value=0.0, step=10.0,
                        format="%.1f", key="dcf_revenue")
        st.number_input(T("ebitda_margin"), min_value=0.0, max_value=100.0,
                        step=0.5, format="%.1f", key="dcf_ebitda_margin")
    with c2:
        st.number_input(T("net_income"), step=10.0, format="%.1f",
                        key="dcf_net_income")
        st.number_input(T("shares_out"), min_value=0.1, step=10.0,
                        format="%.1f", key="dcf_shares")
        st.number_input(T("share_price"), min_value=0.01, step=0.5,
                        format="%.2f", key="dcf_share_price")

    # Summary metrics
    rev = st.session_state["dcf_revenue"]
    marg = st.session_state["dcf_ebitda_margin"]
    ebitda_now = rev * marg / 100
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.markdown(_mc(T("current_revenue"), f"{fmt_mm(rev)}"), unsafe_allow_html=True)
    m2.markdown(_mc("EBITDA", f"{fmt_mm(ebitda_now)}"), unsafe_allow_html=True)
    ev_ebitda = (st.session_state["dcf_share_price"] * st.session_state["dcf_shares"]
                 + st.session_state.get("dcf_net_debt", 0)) / ebitda_now if ebitda_now else 0
    m3.markdown(_mc("EV/EBITDA", f"{ev_ebitda:.1f}x"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — PROJECTIONS
# ═════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.info(T("proj_info"))
    n_years = st.slider(T("proj_years"), 3, 10, key="dcf_proj_years")

    st.subheader(T("sec_rev_growth"))
    cols_g = st.columns(min(n_years, 5))
    for y in range(1, n_years + 1):
        with cols_g[(y - 1) % min(n_years, 5)]:
            st.number_input(
                T("rev_growth").format(y=y),
                min_value=-50.0, max_value=200.0, step=0.5, format="%.1f",
                key=f"dcf_rev_growth_{y}",
            )

    st.subheader(T("sec_margins"))
    cols_m = st.columns(min(n_years, 5))
    for y in range(1, n_years + 1):
        with cols_m[(y - 1) % min(n_years, 5)]:
            st.number_input(
                T("ebitda_margin_y").format(y=y),
                min_value=0.0, max_value=100.0, step=0.5, format="%.1f",
                key=f"dcf_ebitda_margin_{y}",
            )

    st.markdown("---")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.number_input(T("capex_pct"), 0.0, 50.0, step=0.5, format="%.1f",
                        key="dcf_capex_pct")
    with p2:
        st.number_input(T("da_pct"), 0.0, 50.0, step=0.5, format="%.1f",
                        key="dcf_da_pct")
    with p3:
        st.number_input(T("nwc_pct"), -20.0, 20.0, step=0.5, format="%.1f",
                        key="dcf_nwc_pct")
    with p4:
        st.number_input(T("tax_rate"), 0.0, 60.0, step=0.5, format="%.1f",
                        key="dcf_tax_rate")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — WACC
# ═════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.info(T("wacc_info"))

    w1, w2 = st.columns(2)
    with w1:
        st.number_input(T("risk_free"), 0.0, 30.0, step=0.1, format="%.2f",
                        key="dcf_risk_free")
        st.number_input(T("erp"), 0.0, 30.0, step=0.1, format="%.2f",
                        key="dcf_erp")
        st.number_input(T("beta"), 0.0, 5.0, step=0.05, format="%.2f",
                        key="dcf_beta")
    with w2:
        st.number_input(T("cost_debt"), 0.0, 50.0, step=0.1, format="%.2f",
                        key="dcf_cost_debt")
        st.number_input(T("tax_wacc"), 0.0, 60.0, step=0.5, format="%.1f",
                        key="dcf_tax_wacc")
        st.number_input(T("de_ratio"), 0.0, 10.0, step=0.05, format="%.2f",
                        key="dcf_de_ratio")

    # ── WACC Calculation ──
    rf = st.session_state["dcf_risk_free"] / 100
    erp = st.session_state["dcf_erp"] / 100
    beta = st.session_state["dcf_beta"]
    kd_pre = st.session_state["dcf_cost_debt"] / 100
    tax_w = st.session_state["dcf_tax_wacc"] / 100
    de = st.session_state["dcf_de_ratio"]

    ke = rf + beta * erp
    kd_post = kd_pre * (1 - tax_w)
    we = 1 / (1 + de)
    wd = de / (1 + de)
    wacc = we * ke + wd * kd_post

    st.markdown("---")
    st.subheader(T("calc_wacc"))
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(_mc(T("cost_equity"), f"{ke*100:.2f}%"), unsafe_allow_html=True)
    c2.markdown(_mc(T("cost_debt_at"), f"{kd_post*100:.2f}%"), unsafe_allow_html=True)
    c3.markdown(_mc(T("weight_e"), f"{we*100:.1f}%"), unsafe_allow_html=True)
    c4.markdown(_mc(T("weight_d"), f"{wd*100:.1f}%"), unsafe_allow_html=True)
    c5.markdown(_mc("WACC", f"{wacc*100:.2f}%"), unsafe_allow_html=True)

    st.latex(r"K_e = R_f + \beta \times ERP = "
             f"{rf*100:.2f}\\% + {beta:.2f} \\times {erp*100:.2f}\\% = {ke*100:.2f}\\%")
    st.latex(r"WACC = w_e \cdot K_e + w_d \cdot K_d(1-t) = "
             f"{we:.3f} \\times {ke*100:.2f}\\% + {wd:.3f} \\times {kd_post*100:.2f}\\% = {wacc*100:.2f}\\%")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — TERMINAL VALUE
# ═════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.info(T("tv_info"))

    tv_options = [T("gordon"), T("exit_mult")]
    tv_method = st.radio(T("tv_method"), tv_options, horizontal=True,
                         key="dcf_tv_method_radio")
    is_gordon = tv_method == tv_options[0]

    if is_gordon:
        st.number_input(T("perp_growth"), 0.0, 15.0, step=0.1, format="%.2f",
                        key="dcf_perp_growth")
    else:
        st.number_input(T("exit_multiple"), 1.0, 50.0, step=0.5, format="%.1f",
                        key="dcf_exit_multiple")

# ═════════════════════════════════════════════════════════════════════════════
# CORE DCF CALCULATION (shared by Valuation + Sensitivity tabs)
# ═════════════════════════════════════════════════════════════════════════════
def _run_dcf(wacc_override=None, g_override=None, exit_mult_override=None):
    """Return dict with full DCF outputs."""
    n = st.session_state["dcf_proj_years"]
    base_rev = st.session_state["dcf_revenue"]
    capex_pct = st.session_state["dcf_capex_pct"] / 100
    da_pct = st.session_state["dcf_da_pct"] / 100
    nwc_pct = st.session_state["dcf_nwc_pct"] / 100
    tax = st.session_state["dcf_tax_rate"] / 100
    _wacc = wacc_override if wacc_override is not None else wacc

    rows = {
        "revenue": [], "ebitda": [], "da": [], "ebit": [], "taxes": [],
        "nopat": [], "plus_da": [], "capex": [], "nwc": [], "fcff": [],
        "pv_fcff": [],
    }

    rev_prev = base_rev
    for y in range(1, n + 1):
        g = st.session_state.get(f"dcf_rev_growth_{y}", 5.0) / 100
        m = st.session_state.get(f"dcf_ebitda_margin_{y}", 25.0) / 100
        rev = rev_prev * (1 + g)
        ebitda = rev * m
        da = rev * da_pct
        ebit = ebitda - da
        taxes_val = max(ebit * tax, 0)
        nopat = ebit - taxes_val
        capex = rev * capex_pct
        nwc_val = rev * nwc_pct
        fcff = nopat + da - capex - nwc_val
        pv = fcff / ((1 + _wacc) ** y)

        rows["revenue"].append(rev)
        rows["ebitda"].append(ebitda)
        rows["da"].append(da)
        rows["ebit"].append(ebit)
        rows["taxes"].append(taxes_val)
        rows["nopat"].append(nopat)
        rows["plus_da"].append(da)
        rows["capex"].append(capex)
        rows["nwc"].append(nwc_val)
        rows["fcff"].append(fcff)
        rows["pv_fcff"].append(pv)

        rev_prev = rev

    sum_pv_fcf = sum(rows["pv_fcff"])

    # Terminal value
    last_fcff = rows["fcff"][-1]
    last_ebitda = rows["ebitda"][-1]

    # Determine method from radio (use session state for radio)
    use_gordon = (st.session_state.get("dcf_tv_method_radio", T("gordon")) == tv_options[0]
                  if exit_mult_override is None and g_override is None else
                  g_override is not None)

    if use_gordon or g_override is not None:
        g_tv = (g_override if g_override is not None
                else st.session_state["dcf_perp_growth"] / 100)
        if _wacc <= g_tv:
            tv = last_fcff * 50  # cap to avoid infinity
        else:
            tv = last_fcff * (1 + g_tv) / (_wacc - g_tv)
    else:
        em = exit_mult_override if exit_mult_override is not None else st.session_state["dcf_exit_multiple"]
        tv = last_ebitda * em

    pv_tv = tv / ((1 + _wacc) ** n)
    ev = sum_pv_fcf + pv_tv
    net_debt_val = st.session_state.get("dcf_net_debt", 0)
    equity = ev - net_debt_val
    shares = st.session_state["dcf_shares"]
    price = equity / shares if shares > 0 else 0
    current = st.session_state["dcf_share_price"]
    upside_pct = ((price / current) - 1) * 100 if current > 0 else 0

    return {
        "rows": rows, "n": n, "sum_pv_fcf": sum_pv_fcf, "tv": tv,
        "pv_tv": pv_tv, "ev": ev, "net_debt": net_debt_val,
        "equity": equity, "price": price, "upside": upside_pct,
        "tv_pct": (pv_tv / ev * 100) if ev != 0 else 0,
        "wacc_used": _wacc,
    }

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — VALUATION
# ═════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.info(T("val_info"))

    st.number_input(T("enter_net_debt"), step=10.0, format="%.1f",
                    key="dcf_net_debt")

    res = _run_dcf()

    # ── FCFF projection table ──
    st.subheader(T("val_title"))
    year_labels = [f"{T('year')} {y}" for y in range(1, res["n"] + 1)]
    tbl = pd.DataFrame({
        T("year"): year_labels,
        T("revenue"): [fmt_mm(v) for v in res["rows"]["revenue"]],
        T("ebitda"): [fmt_mm(v) for v in res["rows"]["ebitda"]],
        T("da"): [fmt_mm(v) for v in res["rows"]["da"]],
        T("ebit"): [fmt_mm(v) for v in res["rows"]["ebit"]],
        T("taxes"): [fmt_mm(v) for v in res["rows"]["taxes"]],
        T("nopat"): [fmt_mm(v) for v in res["rows"]["nopat"]],
        T("plus_da"): [fmt_mm(v) for v in res["rows"]["plus_da"]],
        T("minus_capex"): [fmt_mm(v) for v in res["rows"]["capex"]],
        T("minus_nwc"): [fmt_mm(v) for v in res["rows"]["nwc"]],
        T("fcff"): [fmt_mm(v) for v in res["rows"]["fcff"]],
        T("pv_fcff"): [fmt_mm(v) for v in res["rows"]["pv_fcff"]],
    })
    st.dataframe(tbl, use_container_width=True, hide_index=True)

    # ── Bridge ──
    st.subheader(T("bridge_title"))
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    b1.markdown(_mc(T("sum_pv_fcf"), fmt_mm(res["sum_pv_fcf"])), unsafe_allow_html=True)
    b2.markdown(_mc(T("pv_tv"), fmt_mm(res["pv_tv"])), unsafe_allow_html=True)
    b3.markdown(_mc(T("enterprise_value"), fmt_mm(res["ev"])), unsafe_allow_html=True)
    b4.markdown(_mc(T("net_debt"), fmt_mm(res["net_debt"])), unsafe_allow_html=True)
    b5.markdown(_mc(T("equity_value"), fmt_mm(res["equity"])), unsafe_allow_html=True)
    b6.markdown(_mc(T("tv_pct_ev"), f"{res['tv_pct']:.1f}%"), unsafe_allow_html=True)

    # ── Per share result ──
    st.markdown("---")
    v1, v2, v3 = st.columns(3)
    color = "green" if res["upside"] >= 0 else "red"
    v1.markdown(_mc(T("price_per_share"), f"{res['price']:.2f}", color=color),
                unsafe_allow_html=True)
    v2.markdown(_mc(T("current_price"), f"{st.session_state['dcf_share_price']:.2f}"),
                unsafe_allow_html=True)
    v3.markdown(_mc(T("upside"), f"{res['upside']:+.1f}%", delta=res["upside"],
                    color=color), unsafe_allow_html=True)

    # ── Waterfall chart ──
    waterfall_labels = [T("sum_pv_fcf"), T("pv_tv"), T("enterprise_value"),
                        T("net_debt"), T("equity_value")]
    waterfall_values = [res["sum_pv_fcf"], res["pv_tv"], res["ev"],
                        -res["net_debt"], res["equity"]]
    waterfall_measures = ["relative", "relative", "total", "relative", "total"]

    fig_w = go.Figure(go.Waterfall(
        x=waterfall_labels,
        y=waterfall_values,
        measure=waterfall_measures,
        textposition="outside",
        text=[fmt_mm(v) for v in waterfall_values],
        connector={"line": {"color": "#1a56db", "width": 1.5}},
        increasing={"marker": {"color": "#1a56db"}},
        decreasing={"marker": {"color": "#dc2626"}},
        totals={"marker": {"color": "#1e429f"}},
    ))
    fig_w.update_layout(
        title=T("bridge_title"),
        showlegend=False,
        height=420,
        margin=dict(t=50, b=40),
        yaxis_title="R$ MM" if lang == "PT" else "$ MM",
    )
    st.plotly_chart(fig_w, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 6 — SENSITIVITY
# ═════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.info(T("sens_info"))

    # Determine if Gordon or Exit method
    tv_radio_val = st.session_state.get("dcf_tv_method_radio", tv_options[0])
    is_gordon_sens = tv_radio_val == tv_options[0]

    s1, s2 = st.columns(2)
    with s1:
        wacc_min, wacc_max = st.slider(
            T("sens_wacc_label"), 3.0, 25.0, (wacc * 100 - 2.0, wacc * 100 + 2.0),
            step=0.5, format="%.1f%%")
    with s2:
        if is_gordon_sens:
            g_min, g_max = st.slider(
                T("sens_growth_label"), 0.0, 10.0,
                (max(0.0, st.session_state["dcf_perp_growth"] - 1.5),
                 st.session_state["dcf_perp_growth"] + 1.5),
                step=0.25, format="%.2f%%")
        else:
            em_min, em_max = st.slider(
                T("sens_exit_label"), 2.0, 30.0,
                (max(2.0, st.session_state["dcf_exit_multiple"] - 3.0),
                 st.session_state["dcf_exit_multiple"] + 3.0),
                step=0.5, format="%.1f")

    # Build sensitivity grid
    wacc_range = np.linspace(wacc_min / 100, wacc_max / 100, 7)
    if is_gordon_sens:
        second_range = np.linspace(g_min / 100, g_max / 100, 7)
    else:
        second_range = np.linspace(em_min, em_max, 7)

    price_grid = np.zeros((len(wacc_range), len(second_range)))
    for i, w in enumerate(wacc_range):
        for j, sv in enumerate(second_range):
            if is_gordon_sens:
                r = _run_dcf(wacc_override=w, g_override=sv)
            else:
                r = _run_dcf(wacc_override=w, exit_mult_override=sv)
            price_grid[i, j] = r["price"]

    # Format labels
    wacc_labels = [f"{w*100:.1f}%" for w in wacc_range]
    if is_gordon_sens:
        sec_labels = [f"{s*100:.2f}%" for s in second_range]
        sec_header = T("sens_growth_label")
    else:
        sec_labels = [f"{s:.1f}x" for s in second_range]
        sec_header = T("sens_exit_label")

    # Build DataFrame for display
    sens_df = pd.DataFrame(
        [[f"{price_grid[i,j]:.2f}" for j in range(len(second_range))]
         for i in range(len(wacc_range))],
        index=wacc_labels,
        columns=sec_labels,
    )
    sens_df.index.name = "WACC"

    st.subheader(T("sens_title"))
    st.markdown(f"**WACC** vs **{sec_header}** -- {T('implied_price')}")

    # Apply color styling
    def _color_cell(val):
        try:
            v = float(val)
        except (ValueError, TypeError):
            return ""
        curr = st.session_state["dcf_share_price"]
        if v >= curr * 1.15:
            return "background-color: #d4edda; color: #155724; font-weight: 700"
        elif v >= curr * 0.85:
            return "background-color: #fff3cd; color: #856404; font-weight: 600"
        else:
            return "background-color: #f8d7da; color: #721c24; font-weight: 700"

    styled = sens_df.style.map(_color_cell)
    st.dataframe(styled, use_container_width=True)

    # ── Football Field Chart ──
    st.subheader(T("football_title"))

    # Collect scenarios
    scenarios = []
    current_price = st.session_state["dcf_share_price"]

    # Base case
    base_res = _run_dcf()
    scenarios.append(("Base Case" if lang == "EN" else "Caso Base",
                      base_res["price"], base_res["price"]))

    # WACC range scenarios
    low_wacc_res = _run_dcf(wacc_override=wacc_range[0])
    high_wacc_res = _run_dcf(wacc_override=wacc_range[-1])
    lbl_wacc = "WACC Range" if lang == "EN" else "Faixa de WACC"
    scenarios.append((lbl_wacc, high_wacc_res["price"], low_wacc_res["price"]))

    # Second dimension range
    if is_gordon_sens:
        low_g_res = _run_dcf(g_override=second_range[0])
        high_g_res = _run_dcf(g_override=second_range[-1])
        lbl_g = "Growth Range" if lang == "EN" else "Faixa de Crescimento"
        scenarios.append((lbl_g, low_g_res["price"], high_g_res["price"]))
    else:
        low_em_res = _run_dcf(exit_mult_override=second_range[0])
        high_em_res = _run_dcf(exit_mult_override=second_range[-1])
        lbl_em = "Multiple Range" if lang == "EN" else "Faixa de Multiplo"
        scenarios.append((lbl_em, low_em_res["price"], high_em_res["price"]))

    # Combined best/worst
    prices_all = price_grid.flatten()
    lbl_comb = "Combined" if lang == "EN" else "Combinado"
    scenarios.append((lbl_comb, float(np.min(prices_all)), float(np.max(prices_all))))

    scenario_names = [s[0] for s in scenarios]
    low_vals = [min(s[1], s[2]) for s in scenarios]
    high_vals = [max(s[1], s[2]) for s in scenarios]
    mid_vals = [(s[1] + s[2]) / 2 for s in scenarios]

    fig_ff = go.Figure()

    # Horizontal bars
    for i, (name, lo, hi) in enumerate(zip(scenario_names, low_vals, high_vals)):
        fig_ff.add_trace(go.Bar(
            y=[name], x=[hi - lo], base=[lo],
            orientation="h",
            marker_color="#1a56db",
            opacity=0.7,
            text=f"{lo:.1f} - {hi:.1f}",
            textposition="inside",
            textfont=dict(color="white", size=12),
            showlegend=False,
            hovertemplate=f"<b>{name}</b><br>Low: {lo:.2f}<br>High: {hi:.2f}<extra></extra>",
        ))

    # Current price line
    fig_ff.add_vline(
        x=current_price,
        line_dash="dash",
        line_color="#dc2626",
        line_width=2,
        annotation_text=f"{T('current_price_line')}: {current_price:.2f}",
        annotation_position="top",
        annotation_font_color="#dc2626",
    )

    fig_ff.update_layout(
        title=T("football_title"),
        xaxis_title=T("implied_price"),
        yaxis_title=T("scenario"),
        height=350,
        margin=dict(l=20, r=20, t=60, b=40),
        bargap=0.3,
    )
    st.plotly_chart(fig_ff, use_container_width=True)

    # ── Heatmap ──
    fig_hm = go.Figure(data=go.Heatmap(
        z=price_grid,
        x=sec_labels,
        y=wacc_labels,
        colorscale=[
            [0, "#dc2626"],
            [0.35, "#fbbf24"],
            [0.5, "#fef3c7"],
            [0.65, "#86efac"],
            [1, "#16a34a"],
        ],
        text=[[f"{price_grid[i,j]:.1f}" for j in range(len(second_range))]
              for i in range(len(wacc_range))],
        texttemplate="%{text}",
        textfont={"size": 11},
        hovertemplate="WACC: %{y}<br>" + sec_header + ": %{x}<br>"
                      + T("implied_price") + ": %{z:.2f}<extra></extra>",
        colorbar=dict(title=T("implied_price")),
    ))
    fig_hm.update_layout(
        title=f"{T('sens_title')} — Heatmap",
        xaxis_title=sec_header,
        yaxis_title="WACC",
        height=450,
        margin=dict(t=50, b=40),
    )
    st.plotly_chart(fig_hm, use_container_width=True)
