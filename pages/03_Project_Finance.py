# ─────────────────────────────────────────────────────────────────────────────
# 03_Project_Finance.py — Streamlit page: Project Finance Model (Enhanced)
# ─────────────────────────────────────────────────────────────────────────────
import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Project Finance", layout="wide")

import sys, os as _os
_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _root not in sys.path: sys.path.insert(0, _root)
import _design_tokens as ds
ds.inject()

# ─────────────────────────────────────────────────────────────────────────────
# BLUE THEME CSS (#1a56db)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"]{display:none}
.stTabs [data-baseweb="tab-list"]{gap:5px}
.stTabs [data-baseweb="tab"]{background:#dbeafe;border-radius:6px 6px 0 0;color:#1a56db;font-weight:600;padding:8px 18px;border:1px solid #bfdbfe;border-bottom:none;transition:all .2s ease}
.stTabs [data-baseweb="tab"]:hover{background:#1a56db;color:white;transform:translateY(-1px)}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:white !important;border-color:#1a56db !important}
[data-testid="stExpander"] details summary{background:#1a56db !important;border-radius:6px !important;padding:10px 16px !important}
[data-testid="stExpander"] details summary p,[data-testid="stExpander"] details summary span{color:white !important;font-weight:600 !important}
[data-testid="stExpander"] details summary svg{fill:white !important;stroke:white !important}
[data-testid="stExpander"] details{border:1px solid #1a56db !important;border-radius:6px !important}
.pf-header{background:linear-gradient(135deg,#1a56db 0%,#1e3a8a 100%);color:white;padding:18px 28px;border-radius:12px;margin-bottom:18px}
.pf-header h1{color:white !important;margin:0;font-size:1.8rem}
.pf-header p{color:#bfdbfe !important;margin:4px 0 0 0;font-size:.9rem}
.metric-card{background:linear-gradient(135deg,#f0f7ff 0%,#dbeafe 100%);border:1px solid #bfdbfe;border-radius:10px;padding:16px 18px;text-align:center;transition:all .2s ease}
.metric-card:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(26,86,219,.14)}
.metric-card .mc-label{font-size:.72rem;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.metric-card .mc-value{font-size:1.4rem;font-weight:800;color:#1a56db;margin:2px 0}
.metric-card-green{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-color:#a3d9a5}
.metric-card-green .mc-value{color:#16a34a}
.metric-card-red{background:linear-gradient(135deg,#f8d7da 0%,#f5c6cb 100%);border-color:#f1aeb5}
.metric-card-red .mc-value{color:#dc2626}
.metric-card-amber{background:linear-gradient(135deg,#fff3cd 0%,#ffeeba 100%);border-color:#ffc107}
.metric-card-amber .mc-value{color:#d97706}
.wf-row{display:flex;align-items:center;gap:8px;margin:4px 0}
.wf-bar{height:28px;border-radius:4px;display:flex;align-items:center;padding:0 10px;font-size:.78rem;font-weight:600;color:white}
.lockup-pass{background:#d4edda;border:1px solid #a3d9a5;border-radius:6px;padding:8px 14px;color:#155724;font-weight:600;margin:4px 0}
.lockup-fail{background:#f8d7da;border:1px solid #f1aeb5;border-radius:6px;padding:8px 14px;color:#721c24;font-weight:600;margin:4px 0}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BILINGUAL LABELS (PT / EN)
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "page_title": "Project Finance",
    "page_sub": "Modelo de financiamento de projetos com estrutura de divida e cascata de caixa",
    "tab_project": "  \U0001f3d7 Projeto  ", "tab_construction": "  \U0001f528 Construcao  ",
    "tab_operations": "  \u2699 Operacao  ", "tab_debt": "  \U0001f4b0 Dimensionamento de Divida  ",
    "tab_waterfall": "  \U0001f30a Cascata de Caixa  ", "tab_results": "  \U0001f3af Resultados  ",
    "tab_sensitivity": "  \U0001f4ca Sensibilidade  ",
    # Project tab
    "proj_name": "Nome do Projeto", "proj_name_ph": "Ex: Usina Solar Alfa",
    "proj_sector": "Setor", "proj_sectors": ["Energia", "Infraestrutura", "Saneamento", "Telecomunicacoes", "Transporte", "Mineracao", "Outro"],
    "proj_constr_months": "Periodo de construcao (meses)",
    "proj_ops_months": "Periodo de operacao (meses)",
    "proj_total_capex": "CapEx total (R$ MM)",
    "proj_currency": "Moeda", "proj_discount": "Taxa de desconto (% a.a.)",
    "proj_tax_rate": "Aliquota IR/CSLL (%)",
    "proj_summary": "Resumo do Projeto",
    # Construction tab
    "constr_title": "Cronograma de Desembolso de CapEx",
    "constr_distr": "Distribuicao do CapEx",
    "constr_uniform": "Uniforme", "constr_front_loaded": "Concentrado no inicio",
    "constr_back_loaded": "Concentrado no final", "constr_custom": "Personalizado",
    "constr_schedule": "Cronograma de Desembolso",
    "constr_quarter": "Trimestre", "constr_amount": "Valor (R$ MM)", "constr_pct": "% do Total",
    "constr_idc": "Juros Durante a Construcao (IDC)",
    "constr_idc_rate": "Taxa de juros p/ IDC (% a.a.)",
    "constr_idc_total": "IDC total estimado",
    "constr_total_invested": "Total investido (CapEx + IDC)",
    "constr_contingency": "Contingencia de construcao (%)",
    "constr_contingency_val": "Valor da contingencia",
    "constr_cost_overrun": "Reserva p/ estouro de custo (%)",
    "constr_cost_overrun_val": "Reserva estouro custo",
    "constr_total_with_contingency": "Total c/ contingencia + IDC",
    # Operations tab
    "ops_title": "Premissas Operacionais",
    "ops_revenue_y1": "Receita no Ano 1 (R$ MM)",
    "ops_rev_growth": "Crescimento de receita (% a.a.)",
    "ops_opex_y1": "OpEx no Ano 1 (R$ MM)",
    "ops_opex_growth": "Crescimento OpEx (% a.a.)",
    "ops_maint_capex": "Manutencao CapEx anual (% da receita)",
    "ops_ramp_up": "Ramp-up: % receita no Ano 1",
    "ops_depreciation": "Depreciacao",
    "ops_depr_life": "Vida util do ativo (anos)",
    "ops_projection": "Projecao Operacional",
    # Debt tab
    "debt_title": "Dimensionamento de Divida",
    "debt_senior_title": "Divida Senior",
    "debt_mezz_title": "Divida Mezzanine",
    "debt_sub_title": "Divida Subordinada",
    "debt_target_dscr": "DSCR alvo (x)",
    "debt_tenor": "Tenor da divida (anos)",
    "debt_grace": "Periodo de carencia (anos)",
    "debt_rate": "Taxa de juros (% a.a.)",
    "debt_amort_type": "Tipo de amortizacao",
    "debt_max_capacity": "Capacidade maxima de divida",
    "debt_leverage": "Alavancagem (Divida / CapEx total)",
    "debt_equity_needed": "Equity necessario",
    "debt_schedule": "Cronograma de Servico da Divida",
    "debt_sculpted": "Sculpted",
    "debt_enable_mezz": "Habilitar Mezzanine",
    "debt_enable_sub": "Habilitar Subordinada",
    "debt_mezz_amount": "Montante Mezzanine (R$ MM)",
    "debt_mezz_rate": "Taxa Mezzanine (% a.a.)",
    "debt_mezz_tenor": "Tenor Mezzanine (anos)",
    "debt_sub_amount": "Montante Subordinada (R$ MM)",
    "debt_sub_rate": "Taxa Subordinada (% a.a.)",
    "debt_sub_tenor": "Tenor Subordinada (anos)",
    "debt_max_gearing": "Gearing maximo (%)",
    "debt_compare_title": "Comparacao de Amortizacao",
    "debt_sculpted_label": "Perfil sculpted: principal dimensionado p/ DSCR alvo",
    "debt_total_all_tranches": "Divida total (todas tranches)",
    # Waterfall tab
    "wf_title": "Cascata de Fluxo de Caixa",
    "wf_revenue": "Receita Bruta",
    "wf_opex": "(-) OpEx",
    "wf_taxes": "(-) Impostos",
    "wf_cfads": "= CFADS",
    "wf_senior_debt": "(-) Servico Divida Senior",
    "wf_dsra": "(-) Aporte/Liberacao DSRA",
    "wf_mezz_debt": "(-) Servico Divida Mezzanine",
    "wf_sub_debt": "(-) Servico Divida Subordinada",
    "wf_cash_available": "= Caixa Disponivel p/ Distribuicao",
    "wf_lockup_test": "Teste de Lock-up",
    "wf_cash_sweep": "(-) Cash Sweep",
    "wf_equity_dist": "= Distribuicao ao Equity",
    "wf_reserve": "(-) Reservas",
    "wf_reserve_months": "DSRA em meses de servico de divida",
    "wf_mra_pct": "MRA (% da receita)",
    "wf_lockup_dscr": "DSCR Lock-up (distribuicoes bloqueadas abaixo)",
    "wf_default_dscr": "DSCR Default (cash trap abaixo)",
    "wf_sweep_pct": "Cash Sweep (% do excedente)",
    "wf_chart_title": "Cascata Anual de Caixa",
    # Results tab
    "res_title": "Metricas de Retorno e Risco",
    "res_project_irr": "TIR do Projeto",
    "res_equity_irr": "TIR do Equity",
    "res_min_dscr": "DSCR Minimo",
    "res_avg_dscr": "DSCR Medio",
    "res_max_dscr": "DSCR Maximo",
    "res_llcr": "LLCR",
    "res_plcr": "PLCR",
    "res_debt_capacity": "Capacidade de Divida (R$ MM)",
    "res_payback": "Payback do Equity (anos)",
    "res_npv": "VPL do Projeto (R$ MM)",
    "res_equity_npv": "VPL do Equity (R$ MM)",
    "res_dscr_profile": "Perfil de DSCR ao Longo do Tempo",
    "res_dscr_warning": "DSCR abaixo do alvo em {n} periodo(s)",
    "res_cashflow_chart": "Fluxo de Caixa do Projeto",
    "res_summary_table": "Tabela Resumo Anual",
    "year": "Ano", "revenue": "Receita", "opex": "OpEx", "ebitda": "EBITDA",
    "debt_service": "Serv. Divida", "cfads": "CFADS", "dscr": "DSCR",
    "equity_cf": "FC Equity", "cumul_equity": "FC Equity Acum.",
    # Sensitivity tab
    "sens_title": "Analise de Sensibilidade e Cenarios",
    "sens_revenue_vol": "Sensibilidade de Volume de Receita",
    "sens_cost_overrun": "Estouro de Custo de Construcao",
    "sens_interest_rate": "Sensibilidade de Taxa de Juros",
    "sens_combined": "Cenario Combinado Adverso",
    "sens_prob_weighted": "Retornos Ponderados por Probabilidade",
    "sens_scenario": "Cenario",
    "sens_base": "Caso Base",
    "sens_downside": "Cenario Adverso",
    "sens_upside": "Cenario Otimista",
    "sens_probability": "Probabilidade (%)",
    "sens_wtd_irr": "TIR Ponderada",
    "sens_revenue_delta": "Variacao de Receita (%)",
    "sens_cost_delta": "Estouro de Custo (%)",
    "sens_rate_delta": "Variacao de Taxa (p.p.)",
    "sens_tornado_title": "Grafico Tornado — Impacto na TIR do Equity",
    "sens_heatmap_title": "Mapa de Calor — TIR Equity (Receita x Taxa de Juros)",
},
"EN": {
    "page_title": "Project Finance",
    "page_sub": "Project financing model with debt structuring and cash flow waterfall",
    "tab_project": "  \U0001f3d7 Project  ", "tab_construction": "  \U0001f528 Construction  ",
    "tab_operations": "  \u2699 Operations  ", "tab_debt": "  \U0001f4b0 Debt Sizing  ",
    "tab_waterfall": "  \U0001f30a Cash Waterfall  ", "tab_results": "  \U0001f3af Results  ",
    "tab_sensitivity": "  \U0001f4ca Sensitivity  ",
    # Project tab
    "proj_name": "Project Name", "proj_name_ph": "e.g. Solar Plant Alpha",
    "proj_sector": "Sector", "proj_sectors": ["Energy", "Infrastructure", "Sanitation", "Telecom", "Transport", "Mining", "Other"],
    "proj_constr_months": "Construction period (months)",
    "proj_ops_months": "Operations period (months)",
    "proj_total_capex": "Total CapEx (R$ MM)",
    "proj_currency": "Currency", "proj_discount": "Discount rate (% p.a.)",
    "proj_tax_rate": "Tax rate — IR/CSLL (%)",
    "proj_summary": "Project Summary",
    # Construction tab
    "constr_title": "CapEx Disbursement Schedule",
    "constr_distr": "CapEx Distribution",
    "constr_uniform": "Uniform", "constr_front_loaded": "Front-loaded",
    "constr_back_loaded": "Back-loaded", "constr_custom": "Custom",
    "constr_schedule": "Disbursement Schedule",
    "constr_quarter": "Quarter", "constr_amount": "Amount (R$ MM)", "constr_pct": "% of Total",
    "constr_idc": "Interest During Construction (IDC)",
    "constr_idc_rate": "IDC interest rate (% p.a.)",
    "constr_idc_total": "Total estimated IDC",
    "constr_total_invested": "Total invested (CapEx + IDC)",
    "constr_contingency": "Construction contingency (%)",
    "constr_contingency_val": "Contingency value",
    "constr_cost_overrun": "Cost overrun reserve (%)",
    "constr_cost_overrun_val": "Cost overrun reserve",
    "constr_total_with_contingency": "Total w/ contingency + IDC",
    # Operations tab
    "ops_title": "Operating Assumptions",
    "ops_revenue_y1": "Year 1 Revenue (R$ MM)",
    "ops_rev_growth": "Revenue growth (% p.a.)",
    "ops_opex_y1": "Year 1 OpEx (R$ MM)",
    "ops_opex_growth": "OpEx growth (% p.a.)",
    "ops_maint_capex": "Maintenance CapEx (% of revenue)",
    "ops_ramp_up": "Ramp-up: % revenue in Year 1",
    "ops_depreciation": "Depreciation",
    "ops_depr_life": "Asset useful life (years)",
    "ops_projection": "Operating Projection",
    # Debt tab
    "debt_title": "Debt Sizing",
    "debt_senior_title": "Senior Debt",
    "debt_mezz_title": "Mezzanine Debt",
    "debt_sub_title": "Subordinated Debt",
    "debt_target_dscr": "Target DSCR (x)",
    "debt_tenor": "Debt tenor (years)",
    "debt_grace": "Grace period (years)",
    "debt_rate": "Interest rate (% p.a.)",
    "debt_amort_type": "Amortization type",
    "debt_max_capacity": "Maximum debt capacity",
    "debt_leverage": "Leverage (Debt / Total CapEx)",
    "debt_equity_needed": "Equity needed",
    "debt_schedule": "Debt Service Schedule",
    "debt_sculpted": "Sculpted",
    "debt_enable_mezz": "Enable Mezzanine",
    "debt_enable_sub": "Enable Subordinated",
    "debt_mezz_amount": "Mezzanine amount (R$ MM)",
    "debt_mezz_rate": "Mezzanine rate (% p.a.)",
    "debt_mezz_tenor": "Mezzanine tenor (years)",
    "debt_sub_amount": "Subordinated amount (R$ MM)",
    "debt_sub_rate": "Subordinated rate (% p.a.)",
    "debt_sub_tenor": "Subordinated tenor (years)",
    "debt_max_gearing": "Maximum gearing (%)",
    "debt_compare_title": "Amortization Comparison",
    "debt_sculpted_label": "Sculpted profile: principal sized to maintain target DSCR",
    "debt_total_all_tranches": "Total debt (all tranches)",
    # Waterfall tab
    "wf_title": "Cash Flow Waterfall",
    "wf_revenue": "Gross Revenue",
    "wf_opex": "(-) OpEx",
    "wf_taxes": "(-) Taxes",
    "wf_cfads": "= CFADS",
    "wf_senior_debt": "(-) Senior Debt Service",
    "wf_dsra": "(-) DSRA Funding/Release",
    "wf_mezz_debt": "(-) Mezzanine Debt Service",
    "wf_sub_debt": "(-) Subordinated Debt Service",
    "wf_cash_available": "= Cash Available for Distribution",
    "wf_lockup_test": "Lock-up Test",
    "wf_cash_sweep": "(-) Cash Sweep",
    "wf_equity_dist": "= Equity Distribution",
    "wf_reserve": "(-) Reserves",
    "wf_reserve_months": "DSRA in months of debt service",
    "wf_mra_pct": "MRA (% of revenue)",
    "wf_lockup_dscr": "Lock-up DSCR (distributions blocked below)",
    "wf_default_dscr": "Default DSCR (cash trap below)",
    "wf_sweep_pct": "Cash Sweep (% of excess)",
    "wf_chart_title": "Annual Cash Waterfall",
    # Results tab
    "res_title": "Return & Risk Metrics",
    "res_project_irr": "Project IRR",
    "res_equity_irr": "Equity IRR",
    "res_min_dscr": "Minimum DSCR",
    "res_avg_dscr": "Average DSCR",
    "res_max_dscr": "Maximum DSCR",
    "res_llcr": "LLCR",
    "res_plcr": "PLCR",
    "res_debt_capacity": "Debt Capacity (R$ MM)",
    "res_payback": "Equity Payback (years)",
    "res_npv": "Project NPV (R$ MM)",
    "res_equity_npv": "Equity NPV (R$ MM)",
    "res_dscr_profile": "DSCR Profile Over Time",
    "res_dscr_warning": "DSCR below target in {n} period(s)",
    "res_cashflow_chart": "Project Cash Flows",
    "res_summary_table": "Annual Summary Table",
    "year": "Year", "revenue": "Revenue", "opex": "OpEx", "ebitda": "EBITDA",
    "debt_service": "Debt Service", "cfads": "CFADS", "dscr": "DSCR",
    "equity_cf": "Equity CF", "cumul_equity": "Cumul. Equity CF",
    # Sensitivity tab
    "sens_title": "Sensitivity Analysis & Scenarios",
    "sens_revenue_vol": "Revenue Volume Sensitivity",
    "sens_cost_overrun": "Construction Cost Overrun",
    "sens_interest_rate": "Interest Rate Sensitivity",
    "sens_combined": "Combined Downside Scenario",
    "sens_prob_weighted": "Probability-Weighted Returns",
    "sens_scenario": "Scenario",
    "sens_base": "Base Case",
    "sens_downside": "Downside Scenario",
    "sens_upside": "Upside Scenario",
    "sens_probability": "Probability (%)",
    "sens_wtd_irr": "Weighted IRR",
    "sens_revenue_delta": "Revenue Variation (%)",
    "sens_cost_delta": "Cost Overrun (%)",
    "sens_rate_delta": "Rate Variation (p.p.)",
    "sens_tornado_title": "Tornado Chart — Equity IRR Impact",
    "sens_heatmap_title": "Heat Map — Equity IRR (Revenue x Interest Rate)",
},
}

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTOR + HEADER
# ─────────────────────────────────────────────────────────────────────────────
_hdr_col, _lang_col, _dark_col = st.columns([8, 1, 1])
with _lang_col:
    st.write("")
    _lang_sel = st.segmented_control("pf_lang", ["PT", "EN"], default="PT",
                                     key="pf_lang", label_visibility="collapsed")
with _dark_col:
    st.write("")
    dark_mode = st.toggle("\U0001f319", key="pf_dark_mode")
lang = _lang_sel or "PT"
L = _L[lang]
def T(k): return L.get(k, _L["PT"].get(k, k))

with _hdr_col:
    st.markdown(f"""<div class="pf-header">
        <h1>{T("page_title")}</h1>
        <p>{T("page_sub")}</p>
    </div>""", unsafe_allow_html=True)

if dark_mode:
    st.markdown("""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#0f172a !important}
p,h1,h2,h3,h4,label,li{color:#e2e8f0 !important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#e2e8f0 !important}
[data-testid="stCaption"] p{color:#94a3b8 !important}
[data-testid="stExpander"] details{background:#1e293b !important;border-color:#334155 !important}
.stTabs [data-baseweb="tab"]{background:#1e293b !important;color:#93c5fd !important;border-color:#334155 !important}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:#fff !important}
[data-testid="stAlert"]{background:#1e293b !important;border-color:#334155 !important}
[data-testid="stAlert"] p{color:#e2e8f0 !important}
[data-testid="stMetricValue"],[data-testid="stMetricLabel"]{color:#e2e8f0 !important}
[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,[data-baseweb="select"] div{background:#1e293b !important;color:#e2e8f0 !important}
.metric-card{background:linear-gradient(135deg,#1e293b,#1e3a5f) !important;border-color:#334155 !important}
.metric-card .mc-label{color:#94a3b8 !important}.metric-card .mc-value{color:#60a5fa !important}
.metric-card-green{background:linear-gradient(135deg,#064e3b,#065f46) !important;border-color:#10b981 !important}
.metric-card-green .mc-value{color:#6ee7b7 !important}
.metric-card-red{background:linear-gradient(135deg,#7f1d1d,#991b1b) !important;border-color:#ef4444 !important}
.metric-card-red .mc-value{color:#fca5a5 !important}
hr{border-color:#334155 !important}
</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "pf_name": "", "pf_sector_idx": 0,
    "pf_constr_months": 24, "pf_ops_months": 240, "pf_total_capex": 500.0,
    "pf_discount": 12.0, "pf_tax_rate": 34.0,
    "pf_capex_dist": "Uniforme", "pf_idc_rate": 10.0,
    "pf_contingency_pct": 10.0, "pf_cost_overrun_pct": 5.0,
    "pf_rev_y1": 120.0, "pf_rev_growth": 3.0,
    "pf_opex_y1": 40.0, "pf_opex_growth": 2.5,
    "pf_maint_capex_pct": 2.0, "pf_ramp_up_pct": 70.0,
    "pf_depr_life": 20,
    "pf_target_dscr": 1.30, "pf_debt_tenor": 15, "pf_grace": 2,
    "pf_debt_rate": 10.0, "pf_amort_type": "SAC",
    "pf_reserve_months": 6,
    "pf_enable_mezz": False, "pf_mezz_amount": 50.0,
    "pf_mezz_rate": 14.0, "pf_mezz_tenor": 10,
    "pf_enable_sub": False, "pf_sub_amount": 30.0,
    "pf_sub_rate": 18.0, "pf_sub_tenor": 8,
    "pf_max_gearing": 80.0,
    "pf_lockup_dscr": 1.15, "pf_default_dscr": 1.05,
    "pf_sweep_pct": 50.0, "pf_mra_pct": 1.0,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: metric card HTML
# ─────────────────────────────────────────────────────────────────────────────
def mc(label, value, extra_class=""):
    cls = f"metric-card {extra_class}".strip()
    return f'<div class="{cls}"><div class="mc-label">{label}</div><div class="mc-value">{value}</div></div>'

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: safe IRR via numpy
# ─────────────────────────────────────────────────────────────────────────────
def safe_irr(cashflows):
    """Compute IRR using numpy polynomial roots. Returns None on failure."""
    cf = np.array(cashflows, dtype=float)
    if len(cf) < 2 or np.all(cf == 0):
        return None
    signs = np.sign(cf[cf != 0])
    if len(signs) < 2 or np.all(signs == signs[0]):
        return None
    try:
        coeffs = cf[::-1]
        roots = np.roots(coeffs)
        real_roots = []
        for r in roots:
            if np.isreal(r) and r.real > 0:
                real_roots.append(r.real)
        if not real_roots:
            return None
        irrs = [1.0 / x - 1.0 for x in real_roots]
        valid = [i for i in irrs if -0.5 < i < 10.0]
        if not valid:
            return None
        return min(valid, key=abs) if len(valid) > 1 else valid[0]
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: build debt schedule for a single tranche
# ─────────────────────────────────────────────────────────────────────────────
def build_tranche_schedule(debt_amount, debt_rate, tenor, grace, amort_type,
                           ops_years, cfads, target_dscr):
    """Build amortization schedule for a debt tranche. Returns dict of arrays."""
    repayment_start = grace
    repayment_years = tenor - grace
    if repayment_years <= 0:
        repayment_years = max(tenor, 1)
        repayment_start = 0
    n = repayment_years

    annual_principal = np.zeros(ops_years)
    annual_interest = np.zeros(ops_years)
    annual_ds = np.zeros(ops_years)
    outstanding = np.zeros(ops_years + 1)
    outstanding[0] = debt_amount

    if amort_type == "SAC":
        pp = debt_amount / n if n > 0 else 0
        for i in range(ops_years):
            if i < repayment_start:
                annual_interest[i] = outstanding[i] * debt_rate
                annual_ds[i] = annual_interest[i]
                outstanding[i + 1] = outstanding[i]
            elif i < repayment_start + n:
                annual_interest[i] = outstanding[i] * debt_rate
                annual_principal[i] = pp
                annual_ds[i] = annual_principal[i] + annual_interest[i]
                outstanding[i + 1] = outstanding[i] - pp
            else:
                outstanding[i + 1] = max(outstanding[i], 0)

    elif amort_type == "Price":
        if n > 0 and debt_rate > 0:
            pmt = debt_amount * debt_rate / (1 - (1 + debt_rate) ** (-n))
        elif n > 0:
            pmt = debt_amount / n
        else:
            pmt = 0
        for i in range(ops_years):
            if i < repayment_start:
                annual_interest[i] = outstanding[i] * debt_rate
                annual_ds[i] = annual_interest[i]
                outstanding[i + 1] = outstanding[i]
            elif i < repayment_start + n:
                annual_interest[i] = outstanding[i] * debt_rate
                annual_principal[i] = min(pmt - annual_interest[i], outstanding[i])
                annual_ds[i] = pmt
                outstanding[i + 1] = outstanding[i] - annual_principal[i]
            else:
                outstanding[i + 1] = max(outstanding[i], 0)

    elif amort_type == "Bullet":
        for i in range(ops_years):
            if i < tenor and i < ops_years:
                annual_interest[i] = outstanding[i] * debt_rate
                if i == tenor - 1:
                    annual_principal[i] = outstanding[i]
                    annual_ds[i] = annual_interest[i] + annual_principal[i]
                    outstanding[i + 1] = 0
                else:
                    annual_ds[i] = annual_interest[i]
                    outstanding[i + 1] = outstanding[i]
            else:
                outstanding[i + 1] = max(outstanding[i], 0)

    else:  # Sculpted
        # Principal sized each period so that DSCR = target_dscr
        # DS_t = CFADS_t / target_dscr; principal_t = DS_t - interest_t
        for i in range(ops_years):
            if i < repayment_start:
                annual_interest[i] = outstanding[i] * debt_rate
                annual_ds[i] = annual_interest[i]
                outstanding[i + 1] = outstanding[i]
            elif i < repayment_start + n and outstanding[i] > 1e-6:
                annual_interest[i] = outstanding[i] * debt_rate
                max_ds = cfads[i] / target_dscr if target_dscr > 0 else 0
                princ = max(min(max_ds - annual_interest[i], outstanding[i]), 0)
                annual_principal[i] = princ
                annual_ds[i] = annual_interest[i] + annual_principal[i]
                outstanding[i + 1] = outstanding[i] - princ
            else:
                outstanding[i + 1] = max(outstanding[i], 0)

    return {
        "principal": annual_principal,
        "interest": annual_interest,
        "ds": annual_ds,
        "outstanding": outstanding,
        "repayment_start": repayment_start,
        "repayment_years": repayment_years,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: size senior debt capacity
# ─────────────────────────────────────────────────────────────────────────────
def size_senior_debt(cfads, target_dscr, debt_rate, tenor, grace, amort_type,
                     ops_years, max_debt_cap):
    """Determine maximum senior debt capacity given CFADS and constraints."""
    repayment_start = grace
    repayment_years = tenor - grace
    if repayment_years <= 0:
        repayment_years = max(tenor, 1)
        repayment_start = 0
    n = repayment_years

    max_ds_per_year = np.zeros(ops_years)
    for i in range(ops_years):
        if cfads[i] > 0:
            max_ds_per_year[i] = cfads[i] / target_dscr

    debt_capacity = 0.0

    if amort_type == "SAC":
        if n > 0:
            candidates = []
            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years)):
                t_in_repay = yr_idx - repayment_start
                factor = 1.0 / n + debt_rate * (1.0 - t_in_repay / n)
                if factor > 0 and max_ds_per_year[yr_idx] > 0:
                    candidates.append(max_ds_per_year[yr_idx] / factor)
            debt_capacity = min(candidates) if candidates else 0.0

    elif amort_type == "Price":
        if n > 0 and debt_rate > 0:
            annuity_factor = debt_rate / (1 - (1 + debt_rate) ** (-n))
            ds_available = [max_ds_per_year[yr_idx]
                            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years))]
            max_annual_ds = min(ds_available) if ds_available else 0
            debt_capacity = max_annual_ds / annuity_factor if annuity_factor > 0 else 0
        elif n > 0:
            ds_available = [max_ds_per_year[yr_idx]
                            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years))]
            max_annual_ds = min(ds_available) if ds_available else 0
            debt_capacity = max_annual_ds * n

    elif amort_type == "Bullet":
        if tenor > 0:
            candidates = []
            for yr_idx in range(min(tenor, ops_years)):
                factor = (debt_rate + 1.0) if yr_idx == tenor - 1 else debt_rate
                if factor > 0 and max_ds_per_year[yr_idx] > 0:
                    candidates.append(max_ds_per_year[yr_idx] / factor)
            debt_capacity = min(candidates) if candidates else 0

    else:  # Sculpted — use NPV of max DS capacity
        # Sculpted: each year DS = CFADS / target_dscr
        # Debt = NPV of all principal payments; iterate
        # Simpler approach: debt = sum of (CFADS_t / target_dscr - outstanding * rate) over repayment
        # Use iterative convergence
        debt_est = 0
        for iteration in range(50):
            sched = build_tranche_schedule(debt_est, debt_rate, tenor, grace,
                                           "Sculpted", ops_years, cfads, target_dscr)
            total_princ = sched["principal"].sum()
            if abs(total_princ - debt_est) < 0.01:
                break
            debt_est = total_princ
        debt_capacity = debt_est

    debt_capacity = min(max(debt_capacity, 0), max_debt_cap)
    return debt_capacity


# ─────────────────────────────────────────────────────────────────────────────
# CORE MODEL CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────
def build_model(override=None):
    """Build the full project finance model. override dict patches session_state values."""
    ov = override or {}
    def S(k):
        return ov[k] if k in ov else st.session_state[k]

    constr_m = S("pf_constr_months")
    ops_m = S("pf_ops_months")
    total_capex = S("pf_total_capex")
    disc = S("pf_discount") / 100.0
    tax = S("pf_tax_rate") / 100.0
    idc_rate = S("pf_idc_rate") / 100.0
    rev_y1 = S("pf_rev_y1")
    rev_g = S("pf_rev_growth") / 100.0
    opex_y1 = S("pf_opex_y1")
    opex_g = S("pf_opex_growth") / 100.0
    maint_pct = S("pf_maint_capex_pct") / 100.0
    ramp_pct = S("pf_ramp_up_pct") / 100.0
    depr_life = max(S("pf_depr_life"), 1)
    target_dscr = S("pf_target_dscr")
    debt_tenor = S("pf_debt_tenor")
    grace = S("pf_grace")
    debt_rate = S("pf_debt_rate") / 100.0
    amort_type = S("pf_amort_type")
    reserve_months = S("pf_reserve_months")
    contingency_pct = S("pf_contingency_pct") / 100.0
    cost_overrun_pct = S("pf_cost_overrun_pct") / 100.0
    max_gearing = S("pf_max_gearing") / 100.0
    lockup_dscr = S("pf_lockup_dscr")
    default_dscr = S("pf_default_dscr")
    sweep_pct = S("pf_sweep_pct") / 100.0
    mra_pct = S("pf_mra_pct") / 100.0

    enable_mezz = S("pf_enable_mezz")
    mezz_amount = S("pf_mezz_amount") if enable_mezz else 0.0
    mezz_rate = S("pf_mezz_rate") / 100.0
    mezz_tenor = S("pf_mezz_tenor")
    enable_sub = S("pf_enable_sub")
    sub_amount = S("pf_sub_amount") if enable_sub else 0.0
    sub_rate = S("pf_sub_rate") / 100.0
    sub_tenor = S("pf_sub_tenor")

    constr_q = max(math.ceil(constr_m / 3), 1)
    ops_years = max(math.ceil(ops_m / 12), 1)

    # ── Construction phase: quarterly CapEx schedule ──
    dist_type = S("pf_capex_dist") if "pf_capex_dist" in ov else st.session_state.get("pf_capex_dist", "Uniforme")
    if dist_type in ("Uniforme", "Uniform"):
        capex_schedule = np.ones(constr_q) / constr_q * total_capex
    elif dist_type in ("Concentrado no inicio", "Front-loaded"):
        weights = np.linspace(2, 0.5, constr_q)
        capex_schedule = weights / weights.sum() * total_capex
    elif dist_type in ("Concentrado no final", "Back-loaded"):
        weights = np.linspace(0.5, 2, constr_q)
        capex_schedule = weights / weights.sum() * total_capex
    else:
        custom_key = "pf_custom_capex"
        if custom_key in st.session_state and len(st.session_state[custom_key]) == constr_q:
            raw = np.array(st.session_state[custom_key], dtype=float)
            s = raw.sum()
            capex_schedule = raw / s * total_capex if s > 0 else np.ones(constr_q) / constr_q * total_capex
        else:
            capex_schedule = np.ones(constr_q) / constr_q * total_capex

    # Construction contingency
    contingency_val = total_capex * contingency_pct
    cost_overrun_val = total_capex * cost_overrun_pct

    # IDC: compound interest on cumulative disbursements (quarterly)
    quarterly_rate = (1 + idc_rate) ** 0.25 - 1
    idc_total = 0.0
    cumul = 0.0
    idc_by_q = []
    for q in range(constr_q):
        cumul += capex_schedule[q]
        idc_q = cumul * quarterly_rate
        idc_total += idc_q
        idc_by_q.append(idc_q)

    total_invested = total_capex + idc_total
    total_with_contingency = total_invested + contingency_val + cost_overrun_val

    # Drawdown schedule: CapEx + IDC capitalized per quarter
    drawdown_schedule = capex_schedule.copy()
    for q in range(constr_q):
        drawdown_schedule[q] += idc_by_q[q]

    # ── Operations phase: annual projections ──
    years = list(range(1, ops_years + 1))
    revenue = np.zeros(ops_years)
    opex = np.zeros(ops_years)
    maint_capex = np.zeros(ops_years)
    depreciation = np.full(ops_years, total_invested / depr_life)
    for i in range(ops_years):
        if i >= depr_life:
            depreciation[i] = 0.0

    for i in range(ops_years):
        base_rev = rev_y1 * ((1 + rev_g) ** i)
        if i == 0:
            revenue[i] = base_rev * ramp_pct
        else:
            revenue[i] = base_rev
        opex[i] = opex_y1 * ((1 + opex_g) ** i)
        maint_capex[i] = revenue[i] * maint_pct

    ebitda = revenue - opex - maint_capex
    ebit = ebitda - depreciation
    taxes_on_ebit = np.maximum(ebit * tax, 0)
    cfads = ebitda - taxes_on_ebit

    # ── Senior debt sizing ──
    max_debt_from_gearing = total_with_contingency * max_gearing
    senior_capacity = size_senior_debt(cfads, target_dscr, debt_rate, debt_tenor,
                                       grace, amort_type, ops_years,
                                       min(total_with_contingency, max_debt_from_gearing))

    # Ensure total debt (senior + mezz + sub) does not exceed gearing cap
    total_junior = mezz_amount + sub_amount
    if senior_capacity + total_junior > max_debt_from_gearing:
        senior_capacity = max(max_debt_from_gearing - total_junior, 0)
    debt_capacity = senior_capacity

    # Build senior schedule
    senior_sched = build_tranche_schedule(debt_capacity, debt_rate, debt_tenor,
                                          grace, amort_type, ops_years, cfads, target_dscr)

    # Build mezzanine schedule (SAC, no grace)
    mezz_sched = build_tranche_schedule(mezz_amount, mezz_rate, mezz_tenor, 0,
                                        "SAC", ops_years, cfads, target_dscr) if enable_mezz else None

    # Build subordinated schedule (SAC, no grace)
    sub_sched = build_tranche_schedule(sub_amount, sub_rate, sub_tenor, 0,
                                       "SAC", ops_years, cfads, target_dscr) if enable_sub else None

    total_debt = debt_capacity + mezz_amount + sub_amount
    equity_invested = total_with_contingency - total_debt
    if equity_invested < 0:
        equity_invested = 0

    # ── Aggregate debt service ──
    annual_principal = senior_sched["principal"].copy()
    annual_interest = senior_sched["interest"].copy()
    annual_ds = senior_sched["ds"].copy()
    outstanding = senior_sched["outstanding"].copy()

    mezz_ds = np.zeros(ops_years)
    sub_ds = np.zeros(ops_years)
    mezz_outstanding = np.zeros(ops_years + 1)
    sub_outstanding = np.zeros(ops_years + 1)
    if mezz_sched:
        mezz_ds = mezz_sched["ds"]
        mezz_outstanding = mezz_sched["outstanding"]
    if sub_sched:
        sub_ds = sub_sched["ds"]
        sub_outstanding = sub_sched["outstanding"]

    # ── DSCR profile (senior only for covenant purposes) ──
    dscr = np.zeros(ops_years)
    for i in range(ops_years):
        if annual_ds[i] > 0:
            dscr[i] = cfads[i] / annual_ds[i]

    # ── LLCR: NPV(CFADS during loan life) / debt outstanding at t=0 ──
    repayment_start = senior_sched["repayment_start"]
    repayment_years = senior_sched["repayment_years"]
    debt_life_end = repayment_start + repayment_years if amort_type != "Bullet" else debt_tenor
    npv_cfads_ll = 0
    for i in range(min(debt_life_end, ops_years)):
        npv_cfads_ll += cfads[i] / ((1 + disc) ** (i + 1))
    llcr = npv_cfads_ll / debt_capacity if debt_capacity > 0 else 0

    # ── PLCR: NPV(CFADS over entire project life) / debt outstanding at t=0 ──
    npv_cfads_pl = 0
    for i in range(ops_years):
        npv_cfads_pl += cfads[i] / ((1 + disc) ** (i + 1))
    plcr = npv_cfads_pl / debt_capacity if debt_capacity > 0 else 0

    # ── Cash Flow Waterfall with reserve accounts, lock-up, cash sweep ──
    dsra_target = np.zeros(ops_years)
    dsra_contribution = np.zeros(ops_years)
    dsra_balance = np.zeros(ops_years + 1)
    mra_contribution = np.zeros(ops_years)
    mra_balance = np.zeros(ops_years + 1)
    cash_sweep_amt = np.zeros(ops_years)
    equity_distribution = np.zeros(ops_years)
    lockup_pass = np.ones(ops_years, dtype=bool)
    default_triggered = np.zeros(ops_years, dtype=bool)
    cash_available = np.zeros(ops_years)

    for i in range(ops_years):
        # Step 1: CFADS already computed
        # Step 2: Senior debt service
        cf_after_senior = cfads[i] - annual_ds[i]

        # Step 3: DSRA funding/release
        next_ds = annual_ds[i + 1] if i + 1 < ops_years else annual_ds[i]
        dsra_target[i] = (reserve_months / 12.0) * next_ds
        dsra_needed = max(dsra_target[i] - dsra_balance[i], 0)
        dsra_contribution[i] = min(dsra_needed, max(cf_after_senior, 0))
        dsra_balance[i + 1] = dsra_balance[i] + dsra_contribution[i]
        cf_after_dsra = cf_after_senior - dsra_contribution[i]

        # Step 4: Mezzanine debt service
        cf_after_mezz = cf_after_dsra - mezz_ds[i]

        # Step 5: Subordinated debt service
        cf_after_sub = cf_after_mezz - sub_ds[i]

        # Step 6: MRA (Maintenance Reserve Account)
        mra_need = revenue[i] * mra_pct
        mra_actual = min(mra_need, max(cf_after_sub, 0))
        mra_contribution[i] = mra_actual
        mra_balance[i + 1] = mra_balance[i] + mra_actual

        cash_available[i] = cf_after_sub - mra_actual

        # Step 7: Lock-up test
        current_dscr = dscr[i] if annual_ds[i] > 0 else 99.0
        if current_dscr < lockup_dscr:
            lockup_pass[i] = False
        if current_dscr < default_dscr:
            default_triggered[i] = True

        # Step 8: Cash sweep (if default triggered, 100% sweep; else normal %)
        if default_triggered[i]:
            # Cash trap — all excess goes to accelerated repayment
            sweep = max(cash_available[i], 0)
            cash_sweep_amt[i] = sweep
            equity_distribution[i] = 0
        elif not lockup_pass[i]:
            # Lock-up: no distributions, but partial sweep
            sweep = max(cash_available[i] * sweep_pct, 0)
            cash_sweep_amt[i] = sweep
            equity_distribution[i] = 0
        else:
            # Normal: sweep portion, distribute rest
            sweep = max(cash_available[i] * sweep_pct, 0) if cash_available[i] > 0 else 0
            cash_sweep_amt[i] = sweep
            equity_distribution[i] = max(cash_available[i] - sweep, 0)

    # ── Build comparison schedules (SAC vs Price vs Sculpted) for debt tab ──
    compare_sac = build_tranche_schedule(debt_capacity, debt_rate, debt_tenor,
                                         grace, "SAC", ops_years, cfads, target_dscr)
    compare_price = build_tranche_schedule(debt_capacity, debt_rate, debt_tenor,
                                           grace, "Price", ops_years, cfads, target_dscr)
    compare_bullet = build_tranche_schedule(debt_capacity, debt_rate, debt_tenor,
                                            grace, "Bullet", ops_years, cfads, target_dscr)
    compare_sculpted = build_tranche_schedule(debt_capacity, debt_rate, debt_tenor,
                                              grace, "Sculpted", ops_years, cfads, target_dscr)

    # ── Project IRR ──
    constr_years = max(math.ceil(constr_m / 12), 1)
    project_cf = []
    capex_annual = np.zeros(constr_years)
    months_per_q = 3
    for q in range(constr_q):
        yr = min(int(q * months_per_q / 12), constr_years - 1)
        capex_annual[yr] += capex_schedule[q]
    capex_annual[-1] += idc_total

    for i in range(constr_years):
        project_cf.append(-capex_annual[i])
    for i in range(ops_years):
        project_cf.append(cfads[i])

    project_irr = safe_irr(project_cf)

    # ── Equity IRR ──
    equity_cf_list = []
    for i in range(constr_years):
        eq_share = capex_annual[i] / total_capex * equity_invested if total_capex > 0 else 0
        if i == constr_years - 1:
            eq_share += idc_total * (equity_invested / total_with_contingency) if total_with_contingency > 0 else 0
        equity_cf_list.append(-eq_share)
    for i in range(ops_years):
        equity_cf_list.append(equity_distribution[i])

    equity_irr = safe_irr(equity_cf_list)

    # ── NPV ──
    project_npv = sum(cf / (1 + disc) ** t for t, cf in enumerate(project_cf))
    equity_npv = sum(cf / (1 + disc) ** t for t, cf in enumerate(equity_cf_list))

    # ── Payback ──
    cum = 0
    payback = None
    for i, cf in enumerate(equity_cf_list):
        cum += cf
        if cum >= 0 and payback is None:
            payback = i

    equity_cumul = np.cumsum(equity_cf_list)

    return {
        "years": years, "ops_years": ops_years, "constr_q": constr_q,
        "constr_years": constr_years,
        "capex_schedule": capex_schedule, "capex_annual": capex_annual,
        "drawdown_schedule": drawdown_schedule,
        "idc_by_q": idc_by_q, "idc_total": idc_total,
        "total_invested": total_invested,
        "contingency_val": contingency_val, "cost_overrun_val": cost_overrun_val,
        "total_with_contingency": total_with_contingency,
        "revenue": revenue, "opex": opex, "maint_capex": maint_capex,
        "ebitda": ebitda, "depreciation": depreciation,
        "ebit": ebit, "taxes_on_ebit": taxes_on_ebit, "cfads": cfads,
        "debt_capacity": debt_capacity, "total_debt": total_debt,
        "equity_invested": equity_invested,
        "outstanding": outstanding,
        "annual_principal": annual_principal, "annual_interest": annual_interest,
        "annual_ds": annual_ds, "dscr": dscr, "llcr": llcr, "plcr": plcr,
        "mezz_ds": mezz_ds, "mezz_outstanding": mezz_outstanding,
        "sub_ds": sub_ds, "sub_outstanding": sub_outstanding,
        "mezz_sched": mezz_sched, "sub_sched": sub_sched,
        "dsra_contribution": dsra_contribution, "dsra_balance": dsra_balance,
        "dsra_target": dsra_target,
        "mra_contribution": mra_contribution, "mra_balance": mra_balance,
        "cash_sweep_amt": cash_sweep_amt,
        "cash_available": cash_available,
        "lockup_pass": lockup_pass, "default_triggered": default_triggered,
        "equity_distribution": equity_distribution,
        "project_cf": project_cf, "equity_cf_list": equity_cf_list,
        "project_irr": project_irr, "equity_irr": equity_irr,
        "project_npv": project_npv, "equity_npv": equity_npv,
        "payback": payback, "equity_cumul": equity_cumul,
        "target_dscr": target_dscr,
        "repayment_start": repayment_start,
        "repayment_years": repayment_years,
        "compare_sac": compare_sac, "compare_price": compare_price,
        "compare_bullet": compare_bullet, "compare_sculpted": compare_sculpted,
        "senior_sched": senior_sched,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    T("tab_project"), T("tab_construction"), T("tab_operations"),
    T("tab_debt"), T("tab_waterfall"), T("tab_results"), T("tab_sensitivity"),
    "\U0001f578  SPE Diagram", "\U0001f4dc  Contract Minutes",
])

# =====================  TAB 1: PROJECT  =====================================
with tabs[0]:
    st.subheader(T("proj_summary"))
    c1, c2 = st.columns(2)
    with c1:
        st.text_input(T("proj_name"), placeholder=T("proj_name_ph"), key="pf_name")
        st.selectbox(T("proj_sector"), T("proj_sectors"), key="pf_sector_idx")
        st.number_input(T("proj_constr_months"), min_value=1, max_value=120,
                        step=1, key="pf_constr_months")
        st.number_input(T("proj_ops_months"), min_value=12, max_value=600,
                        step=12, key="pf_ops_months")
    with c2:
        st.number_input(T("proj_total_capex"), min_value=1.0, step=10.0,
                        format="%.1f", key="pf_total_capex")
        st.number_input(T("proj_discount"), min_value=0.0, max_value=50.0,
                        step=0.5, format="%.2f", key="pf_discount")
        st.number_input(T("proj_tax_rate"), min_value=0.0, max_value=60.0,
                        step=1.0, format="%.1f", key="pf_tax_rate")

    st.divider()
    m = build_model()
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(mc(T("proj_total_capex"), f"R$ {st.session_state['pf_total_capex']:.1f} MM"), unsafe_allow_html=True)
    sc2.markdown(mc(T("proj_constr_months"), f"{st.session_state['pf_constr_months']} m"), unsafe_allow_html=True)
    sc3.markdown(mc(T("proj_ops_months"), f"{st.session_state['pf_ops_months']} m"), unsafe_allow_html=True)
    sc4.markdown(mc(T("proj_discount"), f"{st.session_state['pf_discount']:.1f}%"), unsafe_allow_html=True)

# =====================  TAB 2: CONSTRUCTION  ================================
with tabs[1]:
    st.subheader(T("constr_title"))
    c1, c2 = st.columns([1, 2])
    with c1:
        dist_options_pt = ["Uniforme", "Concentrado no inicio", "Concentrado no final", "Personalizado"]
        dist_options_en = ["Uniform", "Front-loaded", "Back-loaded", "Custom"]
        dist_options = dist_options_en if lang == "EN" else dist_options_pt
        dist_val = st.radio(T("constr_distr"), dist_options, key="pf_capex_dist_radio",
                            horizontal=False)
        mapping = dict(zip(dist_options_en, dist_options_pt))
        if lang == "EN":
            st.session_state["pf_capex_dist"] = mapping.get(dist_val, dist_val)
        else:
            st.session_state["pf_capex_dist"] = dist_val

        st.divider()
        st.number_input(T("constr_idc_rate"), min_value=0.0, max_value=30.0,
                        step=0.5, format="%.2f", key="pf_idc_rate")
        st.number_input(T("constr_contingency"), min_value=0.0, max_value=30.0,
                        step=1.0, format="%.1f", key="pf_contingency_pct")
        st.number_input(T("constr_cost_overrun"), min_value=0.0, max_value=30.0,
                        step=1.0, format="%.1f", key="pf_cost_overrun_pct")

    m = build_model()
    with c2:
        constr_q = m["constr_q"]
        schedule_data = {
            T("constr_quarter"): [f"Q{i+1}" for i in range(constr_q)],
            T("constr_amount"): [f"{v:.2f}" for v in m["capex_schedule"]],
            T("constr_pct"): [f"{v/st.session_state['pf_total_capex']*100:.1f}%" for v in m["capex_schedule"]],
            "IDC": [f"{v:.2f}" for v in m["idc_by_q"]],
            "Drawdown": [f"{v:.2f}" for v in m["drawdown_schedule"]],
        }
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

        if st.session_state.get("pf_capex_dist") in ("Personalizado", "Custom"):
            st.caption("Ajuste os pesos por trimestre:" if lang == "PT" else "Adjust weights per quarter:")
            custom_vals = []
            cols = st.columns(min(constr_q, 8))
            for i in range(constr_q):
                with cols[i % len(cols)]:
                    v = st.number_input(f"Q{i+1}", min_value=0.0, value=1.0, step=0.1,
                                        key=f"pf_cq_{i}", format="%.1f")
                    custom_vals.append(v)
            st.session_state["pf_custom_capex"] = custom_vals

        fig_capex = go.Figure()
        fig_capex.add_trace(go.Bar(
            x=[f"Q{i+1}" for i in range(constr_q)],
            y=m["capex_schedule"],
            marker_color="#1a56db",
            name="CapEx"
        ))
        fig_capex.add_trace(go.Bar(
            x=[f"Q{i+1}" for i in range(constr_q)],
            y=m["idc_by_q"],
            marker_color="#93c5fd",
            name="IDC"
        ))
        fig_capex.update_layout(
            barmode="stack", height=340,
            title=T("constr_schedule"),
            xaxis_title=T("constr_quarter"),
            yaxis_title="R$ MM",
            template="plotly_white",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_capex, use_container_width=True)

    st.divider()
    ic1, ic2, ic3, ic4, ic5 = st.columns(5)
    ic1.markdown(mc(T("constr_idc_total"), f"R$ {m['idc_total']:.2f} MM"), unsafe_allow_html=True)
    ic2.markdown(mc(T("constr_total_invested"), f"R$ {m['total_invested']:.2f} MM"), unsafe_allow_html=True)
    ic3.markdown(mc(T("constr_contingency_val"), f"R$ {m['contingency_val']:.2f} MM"), unsafe_allow_html=True)
    ic4.markdown(mc(T("constr_cost_overrun_val"), f"R$ {m['cost_overrun_val']:.2f} MM"), unsafe_allow_html=True)
    ic5.markdown(mc(T("constr_total_with_contingency"), f"R$ {m['total_with_contingency']:.2f} MM", "metric-card-amber"), unsafe_allow_html=True)

# =====================  TAB 3: OPERATIONS  ==================================
with tabs[2]:
    st.subheader(T("ops_title"))
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(T("ops_revenue_y1"), min_value=0.1, step=5.0,
                        format="%.1f", key="pf_rev_y1")
        st.number_input(T("ops_rev_growth"), min_value=-20.0, max_value=50.0,
                        step=0.5, format="%.2f", key="pf_rev_growth")
        st.number_input(T("ops_ramp_up"), min_value=10.0, max_value=100.0,
                        step=5.0, format="%.0f", key="pf_ramp_up_pct")
    with c2:
        st.number_input(T("ops_opex_y1"), min_value=0.0, step=5.0,
                        format="%.1f", key="pf_opex_y1")
        st.number_input(T("ops_opex_growth"), min_value=-10.0, max_value=30.0,
                        step=0.5, format="%.2f", key="pf_opex_growth")
        st.number_input(T("ops_maint_capex"), min_value=0.0, max_value=20.0,
                        step=0.5, format="%.1f", key="pf_maint_capex_pct")
    st.number_input(T("ops_depr_life"), min_value=1, max_value=50,
                    step=1, key="pf_depr_life")

    m = build_model()
    st.divider()
    st.subheader(T("ops_projection"))

    df_ops = pd.DataFrame({
        T("year"): m["years"],
        T("revenue"): [f"{v:.2f}" for v in m["revenue"]],
        T("opex"): [f"{v:.2f}" for v in m["opex"]],
        "EBITDA": [f"{v:.2f}" for v in m["ebitda"]],
        "EBITDA %": [f"{v/max(r,0.01)*100:.1f}%" for v, r in zip(m["ebitda"], m["revenue"])],
        T("cfads"): [f"{v:.2f}" for v in m["cfads"]],
    })
    st.dataframe(df_ops, use_container_width=True, hide_index=True, height=min(400, 35 * len(m["years"]) + 40))

    fig_ops = go.Figure()
    fig_ops.add_trace(go.Bar(x=m["years"], y=m["revenue"], name=T("revenue"),
                             marker_color="#1a56db"))
    fig_ops.add_trace(go.Bar(x=m["years"], y=-m["opex"], name=T("opex"),
                             marker_color="#ef4444"))
    fig_ops.add_trace(go.Scatter(x=m["years"], y=m["ebitda"], name="EBITDA",
                                 line=dict(color="#16a34a", width=3), mode="lines+markers"))
    fig_ops.update_layout(
        barmode="relative", height=380,
        title=T("ops_projection"),
        xaxis_title=T("year"), yaxis_title="R$ MM",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_ops, use_container_width=True)

# =====================  TAB 4: DEBT SIZING  =================================
with tabs[3]:
    st.subheader(T("debt_title"))

    # Senior debt inputs
    with st.expander(T("debt_senior_title"), expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(T("debt_target_dscr"), min_value=1.0, max_value=3.0,
                            step=0.05, format="%.2f", key="pf_target_dscr")
            st.number_input(T("debt_tenor"), min_value=1, max_value=30,
                            step=1, key="pf_debt_tenor")
            st.number_input(T("debt_grace"), min_value=0, max_value=10,
                            step=1, key="pf_grace")
        with c2:
            st.number_input(T("debt_rate"), min_value=0.0, max_value=30.0,
                            step=0.5, format="%.2f", key="pf_debt_rate")
            st.selectbox(T("debt_amort_type"), ["SAC", "Price", "Bullet", "Sculpted"],
                         key="pf_amort_type")
            st.number_input(T("debt_max_gearing"), min_value=10.0, max_value=100.0,
                            step=5.0, format="%.0f", key="pf_max_gearing")

    # Mezzanine
    with st.expander(T("debt_mezz_title"), expanded=False):
        st.toggle(T("debt_enable_mezz"), key="pf_enable_mezz")
        if st.session_state["pf_enable_mezz"]:
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.number_input(T("debt_mezz_amount"), min_value=0.0, step=5.0,
                                format="%.1f", key="pf_mezz_amount")
            with mc2:
                st.number_input(T("debt_mezz_rate"), min_value=0.0, max_value=40.0,
                                step=0.5, format="%.2f", key="pf_mezz_rate")
            with mc3:
                st.number_input(T("debt_mezz_tenor"), min_value=1, max_value=20,
                                step=1, key="pf_mezz_tenor")

    # Subordinated
    with st.expander(T("debt_sub_title"), expanded=False):
        st.toggle(T("debt_enable_sub"), key="pf_enable_sub")
        if st.session_state["pf_enable_sub"]:
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.number_input(T("debt_sub_amount"), min_value=0.0, step=5.0,
                                format="%.1f", key="pf_sub_amount")
            with sc2:
                st.number_input(T("debt_sub_rate"), min_value=0.0, max_value=50.0,
                                step=0.5, format="%.2f", key="pf_sub_rate")
            with sc3:
                st.number_input(T("debt_sub_tenor"), min_value=1, max_value=15,
                                step=1, key="pf_sub_tenor")

    m = build_model()
    st.divider()

    # Key metrics
    dc1, dc2, dc3, dc4, dc5 = st.columns(5)
    dc1.markdown(mc(T("debt_max_capacity"), f"R$ {m['debt_capacity']:.2f} MM",
                    "metric-card-green" if m['debt_capacity'] > 0 else ""), unsafe_allow_html=True)
    leverage = m['total_debt'] / max(m['total_with_contingency'], 0.01) * 100
    dc2.markdown(mc(T("debt_leverage"), f"{leverage:.1f}%",
                    "metric-card-green" if leverage <= 80 else "metric-card-amber"), unsafe_allow_html=True)
    dc3.markdown(mc(T("debt_equity_needed"), f"R$ {m['equity_invested']:.2f} MM"), unsafe_allow_html=True)
    de_ratio = m['total_debt'] / max(m['equity_invested'], 0.01)
    dc4.markdown(mc("Debt / Equity", f"{de_ratio:.2f}x"), unsafe_allow_html=True)
    dc5.markdown(mc(T("debt_total_all_tranches"), f"R$ {m['total_debt']:.2f} MM", "metric-card-amber"), unsafe_allow_html=True)

    # Debt schedule table
    st.subheader(T("debt_schedule"))
    ops_y = m["ops_years"]
    debt_table_data = {
        T("year"): m["years"],
        "Senior Out.": [f"{m['outstanding'][i]:.2f}" for i in range(ops_y)],
        "Sr. Principal": [f"{m['annual_principal'][i]:.2f}" for i in range(ops_y)],
        "Sr. " + ("Juros" if lang == "PT" else "Interest"): [f"{m['annual_interest'][i]:.2f}" for i in range(ops_y)],
        "Sr. DS": [f"{m['annual_ds'][i]:.2f}" for i in range(ops_y)],
    }
    if st.session_state["pf_enable_mezz"]:
        debt_table_data["Mezz DS"] = [f"{m['mezz_ds'][i]:.2f}" for i in range(ops_y)]
        debt_table_data["Mezz Out."] = [f"{m['mezz_outstanding'][i]:.2f}" for i in range(ops_y)]
    if st.session_state["pf_enable_sub"]:
        debt_table_data["Sub DS"] = [f"{m['sub_ds'][i]:.2f}" for i in range(ops_y)]
        debt_table_data["Sub Out."] = [f"{m['sub_outstanding'][i]:.2f}" for i in range(ops_y)]
    debt_table_data[T("cfads")] = [f"{m['cfads'][i]:.2f}" for i in range(ops_y)]
    debt_table_data[T("dscr")] = [f"{m['dscr'][i]:.2f}x" if m['annual_ds'][i] > 0 else "n/a" for i in range(ops_y)]

    st.dataframe(pd.DataFrame(debt_table_data), use_container_width=True, hide_index=True,
                 height=min(400, 35 * ops_y + 40))

    # Debt service chart
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Bar(x=m["years"], y=m["annual_principal"],
                              name="Sr. Principal", marker_color="#1a56db"))
    fig_debt.add_trace(go.Bar(x=m["years"], y=m["annual_interest"],
                              name="Sr. " + ("Juros" if lang == "PT" else "Interest"),
                              marker_color="#93c5fd"))
    if st.session_state["pf_enable_mezz"]:
        fig_debt.add_trace(go.Bar(x=m["years"], y=m["mezz_ds"],
                                  name="Mezz DS", marker_color="#f59e0b"))
    if st.session_state["pf_enable_sub"]:
        fig_debt.add_trace(go.Bar(x=m["years"], y=m["sub_ds"],
                                  name="Sub DS", marker_color="#ef4444"))
    fig_debt.add_trace(go.Scatter(x=m["years"], y=m["cfads"], name="CFADS",
                                  line=dict(color="#16a34a", width=2, dash="dot"),
                                  mode="lines+markers"))
    fig_debt.update_layout(
        barmode="stack", height=380,
        title=T("debt_schedule"),
        xaxis_title=T("year"), yaxis_title="R$ MM",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_debt, use_container_width=True)

    # ── Amortization comparison chart ──
    with st.expander(T("debt_compare_title"), expanded=False):
        fig_cmp = go.Figure()
        for label, sched, color in [
            ("SAC", m["compare_sac"], "#1a56db"),
            ("Price", m["compare_price"], "#16a34a"),
            ("Bullet", m["compare_bullet"], "#ef4444"),
            ("Sculpted", m["compare_sculpted"], "#f59e0b"),
        ]:
            fig_cmp.add_trace(go.Scatter(
                x=m["years"], y=sched["ds"][:ops_y],
                name=label, mode="lines+markers",
                line=dict(color=color, width=2),
            ))
        fig_cmp.add_trace(go.Scatter(x=m["years"], y=m["cfads"], name="CFADS",
                                     line=dict(color="#9ca3af", width=2, dash="dot"),
                                     mode="lines"))
        fig_cmp.update_layout(
            height=380,
            title=T("debt_compare_title"),
            xaxis_title=T("year"), yaxis_title="R$ MM",
            template="plotly_white",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_cmp, use_container_width=True)
        if amort_type == "Sculpted":
            st.info(T("debt_sculpted_label"))

# =====================  TAB 5: WATERFALL  ===================================
with tabs[4]:
    st.subheader(T("wf_title"))
    wc1, wc2, wc3, wc4 = st.columns(4)
    with wc1:
        st.number_input(T("wf_reserve_months"), min_value=0, max_value=24,
                        step=1, key="pf_reserve_months")
    with wc2:
        st.number_input(T("wf_mra_pct"), min_value=0.0, max_value=10.0,
                        step=0.5, format="%.1f", key="pf_mra_pct")
    with wc3:
        st.number_input(T("wf_lockup_dscr"), min_value=1.0, max_value=2.0,
                        step=0.05, format="%.2f", key="pf_lockup_dscr")
    with wc4:
        st.number_input(T("wf_default_dscr"), min_value=0.8, max_value=1.5,
                        step=0.05, format="%.2f", key="pf_default_dscr")

    st.number_input(T("wf_sweep_pct"), min_value=0.0, max_value=100.0,
                    step=5.0, format="%.0f", key="pf_sweep_pct")

    m = build_model()
    ops_y = m["ops_years"]

    # Annual waterfall chart
    fig_wf = go.Figure()
    fig_wf.add_trace(go.Bar(x=m["years"], y=m["revenue"], name=T("wf_revenue"),
                            marker_color="#1a56db"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["opex"], name=T("wf_opex"),
                            marker_color="#ef4444"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["taxes_on_ebit"], name=T("wf_taxes"),
                            marker_color="#f97316"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["annual_ds"], name=T("wf_senior_debt"),
                            marker_color="#6366f1"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["dsra_contribution"],
                            name=T("wf_dsra"), marker_color="#a78bfa"))
    if st.session_state["pf_enable_mezz"]:
        fig_wf.add_trace(go.Bar(x=m["years"], y=-m["mezz_ds"],
                                name=T("wf_mezz_debt"), marker_color="#f59e0b"))
    if st.session_state["pf_enable_sub"]:
        fig_wf.add_trace(go.Bar(x=m["years"], y=-m["sub_ds"],
                                name=T("wf_sub_debt"), marker_color="#dc2626"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["cash_sweep_amt"],
                            name=T("wf_cash_sweep"), marker_color="#64748b"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=m["equity_distribution"],
                            name=T("wf_equity_dist"), marker_color="#16a34a"))
    fig_wf.update_layout(
        barmode="relative", height=420,
        title=T("wf_chart_title"),
        xaxis_title=T("year"), yaxis_title="R$ MM",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # Lock-up / Default indicators
    n_lockup_fail = int(np.sum(~m["lockup_pass"]))
    n_default = int(np.sum(m["default_triggered"]))
    if n_default > 0:
        st.markdown(f'<div class="lockup-fail">{"CASH TRAP acionado em" if lang == "PT" else "CASH TRAP triggered in"} {n_default} {"periodo(s)" if lang == "PT" else "period(s)"} (DSCR < {st.session_state["pf_default_dscr"]:.2f}x)</div>', unsafe_allow_html=True)
    if n_lockup_fail > 0:
        st.markdown(f'<div class="lockup-fail">{"Lock-up acionado em" if lang == "PT" else "Lock-up triggered in"} {n_lockup_fail} {"periodo(s)" if lang == "PT" else "period(s)"} (DSCR < {st.session_state["pf_lockup_dscr"]:.2f}x)</div>', unsafe_allow_html=True)
    elif n_lockup_fail == 0 and n_default == 0:
        st.markdown(f'<div class="lockup-pass">{"Todos os testes de covenant passaram" if lang == "PT" else "All covenant tests passed"}</div>', unsafe_allow_html=True)

    # Waterfall detail table
    with st.expander(T("res_summary_table"), expanded=False):
        wf_table = {
            T("year"): m["years"],
            T("wf_revenue"): [f"{v:.2f}" for v in m["revenue"]],
            T("wf_opex"): [f"({v:.2f})" for v in m["opex"]],
            T("wf_taxes"): [f"({v:.2f})" for v in m["taxes_on_ebit"]],
            T("wf_cfads"): [f"{v:.2f}" for v in m["cfads"]],
            T("wf_senior_debt"): [f"({v:.2f})" for v in m["annual_ds"]],
            T("wf_dsra"): [f"({v:.2f})" for v in m["dsra_contribution"]],
        }
        if st.session_state["pf_enable_mezz"]:
            wf_table[T("wf_mezz_debt")] = [f"({v:.2f})" for v in m["mezz_ds"]]
        if st.session_state["pf_enable_sub"]:
            wf_table[T("wf_sub_debt")] = [f"({v:.2f})" for v in m["sub_ds"]]
        wf_table[T("wf_cash_sweep")] = [f"({v:.2f})" for v in m["cash_sweep_amt"]]
        wf_table[T("wf_lockup_test")] = ["PASS" if m["lockup_pass"][i] else "FAIL" for i in range(ops_y)]
        wf_table[T("wf_equity_dist")] = [f"{v:.2f}" for v in m["equity_distribution"]]
        st.dataframe(pd.DataFrame(wf_table), use_container_width=True, hide_index=True)

    # Reserve account balances chart
    with st.expander("DSRA / MRA Balances", expanded=False):
        fig_res = go.Figure()
        fig_res.add_trace(go.Scatter(
            x=m["years"], y=[m["dsra_balance"][i+1] for i in range(ops_y)],
            name="DSRA", fill="tozeroy", line=dict(color="#6366f1"),
        ))
        fig_res.add_trace(go.Scatter(
            x=m["years"], y=[m["mra_balance"][i+1] for i in range(ops_y)],
            name="MRA", fill="tozeroy", line=dict(color="#a78bfa"),
        ))
        fig_res.add_trace(go.Scatter(
            x=m["years"], y=m["dsra_target"],
            name="DSRA Target", line=dict(color="#ef4444", dash="dash"),
        ))
        fig_res.update_layout(
            height=320, title="Reserve Account Balances",
            xaxis_title=T("year"), yaxis_title="R$ MM",
            template="plotly_white", font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_res, use_container_width=True)

    # Single-year waterfall
    st.divider()
    sel_year = st.select_slider(
        T("year"), options=m["years"], value=m["years"][min(2, len(m["years"]) - 1)],
        key="pf_wf_year"
    )
    idx = sel_year - 1
    if 0 <= idx < ops_y:
        items = [
            (T("wf_revenue"), m["revenue"][idx], "#1a56db"),
            (T("wf_opex"), -m["opex"][idx], "#ef4444"),
            (T("wf_taxes"), -m["taxes_on_ebit"][idx], "#f97316"),
            (T("wf_senior_debt"), -m["annual_ds"][idx], "#6366f1"),
            (T("wf_dsra"), -m["dsra_contribution"][idx], "#a78bfa"),
        ]
        if st.session_state["pf_enable_mezz"]:
            items.append((T("wf_mezz_debt"), -m["mezz_ds"][idx], "#f59e0b"))
        if st.session_state["pf_enable_sub"]:
            items.append((T("wf_sub_debt"), -m["sub_ds"][idx], "#dc2626"))
        items.append((T("wf_cash_sweep"), -m["cash_sweep_amt"][idx], "#64748b"))
        items.append((T("wf_equity_dist"), m["equity_distribution"][idx], "#16a34a"))

        fig_single = go.Figure(go.Waterfall(
            x=[it[0] for it in items],
            y=[it[1] for it in items],
            connector=dict(line=dict(color="#1a56db", width=1)),
            increasing=dict(marker_color="#1a56db"),
            decreasing=dict(marker_color="#ef4444"),
            totals=dict(marker_color="#16a34a"),
            textposition="outside",
            text=[f"{it[1]:.1f}" for it in items],
        ))
        yr_label = f"{'Ano' if lang == 'PT' else 'Year'} {sel_year}"
        lockup_status = "PASS" if m["lockup_pass"][idx] else "FAIL"
        fig_single.update_layout(
            height=400,
            title=f"{T('wf_chart_title')} -- {yr_label} (Lock-up: {lockup_status})",
            yaxis_title="R$ MM",
            template="plotly_white",
            font=dict(family="Inter, sans-serif"),
            showlegend=False,
        )
        st.plotly_chart(fig_single, use_container_width=True)

# =====================  TAB 6: RESULTS  =====================================
with tabs[5]:
    m = build_model()
    st.subheader(T("res_title"))
    ops_y = m["ops_years"]

    # Key Metrics row 1
    r1, r2, r3 = st.columns(3)
    pirr_str = f"{m['project_irr']*100:.2f}%" if m['project_irr'] is not None else "n/a"
    eirr_str = f"{m['equity_irr']*100:.2f}%" if m['equity_irr'] is not None else "n/a"
    pirr_cls = "metric-card-green" if m['project_irr'] and m['project_irr'] > st.session_state['pf_discount']/100 else "metric-card-red"
    eirr_cls = "metric-card-green" if m['equity_irr'] and m['equity_irr'] > st.session_state['pf_discount']/100 else "metric-card-red"
    r1.markdown(mc(T("res_project_irr"), pirr_str, pirr_cls), unsafe_allow_html=True)
    r2.markdown(mc(T("res_equity_irr"), eirr_str, eirr_cls), unsafe_allow_html=True)
    npv_cls = "metric-card-green" if m['project_npv'] > 0 else "metric-card-red"
    r3.markdown(mc(T("res_npv"), f"R$ {m['project_npv']:.2f} MM", npv_cls), unsafe_allow_html=True)

    # Key Metrics row 2 — DSCR min/avg/max
    r4, r5, r6, r7 = st.columns(4)
    dscr_active = m["dscr"][m["annual_ds"] > 0]
    min_dscr = dscr_active.min() if len(dscr_active) > 0 else 0
    avg_dscr = dscr_active.mean() if len(dscr_active) > 0 else 0
    max_dscr = dscr_active.max() if len(dscr_active) > 0 else 0
    dscr_cls = "metric-card-green" if min_dscr >= m["target_dscr"] else "metric-card-red"
    r4.markdown(mc(T("res_min_dscr"), f"{min_dscr:.2f}x", dscr_cls), unsafe_allow_html=True)
    r5.markdown(mc(T("res_avg_dscr"), f"{avg_dscr:.2f}x"), unsafe_allow_html=True)
    r6.markdown(mc(T("res_max_dscr"), f"{max_dscr:.2f}x"), unsafe_allow_html=True)
    r7.markdown(mc(T("res_llcr"), f"{m['llcr']:.2f}x",
                   "metric-card-green" if m['llcr'] >= 1.2 else "metric-card-amber"), unsafe_allow_html=True)

    # Key Metrics row 3
    r8, r9, r10, r11 = st.columns(4)
    r8.markdown(mc(T("res_plcr"), f"{m['plcr']:.2f}x",
                   "metric-card-green" if m['plcr'] >= 1.5 else "metric-card-amber"), unsafe_allow_html=True)
    r9.markdown(mc(T("res_debt_capacity"), f"R$ {m['debt_capacity']:.2f} MM"), unsafe_allow_html=True)
    payback_str = f"{m['payback']}" if m['payback'] is not None else "n/a"
    r10.markdown(mc(T("res_payback"), payback_str), unsafe_allow_html=True)
    r11.markdown(mc(T("res_equity_npv"), f"R$ {m['equity_npv']:.2f} MM",
                   "metric-card-green" if m['equity_npv'] > 0 else "metric-card-red"), unsafe_allow_html=True)

    # DSCR Warning
    n_below = int(np.sum((dscr_active < m["target_dscr"]) & (dscr_active > 0)))
    if n_below > 0:
        st.warning(T("res_dscr_warning").format(n=n_below))

    st.divider()

    # DSCR Profile Chart
    st.subheader(T("res_dscr_profile"))
    fig_dscr = go.Figure()
    dscr_display = [d if d > 0 else None for d in m["dscr"]]
    fig_dscr.add_trace(go.Bar(
        x=m["years"], y=dscr_display, name="DSCR",
        marker_color=["#16a34a" if (d and d >= m['target_dscr']) else "#ef4444"
                       for d in dscr_display],
    ))
    fig_dscr.add_hline(y=m["target_dscr"], line_dash="dash", line_color="#1a56db",
                       annotation_text=f"Target: {m['target_dscr']:.2f}x")
    fig_dscr.add_hline(y=st.session_state["pf_lockup_dscr"], line_dash="dot",
                       line_color="#f59e0b",
                       annotation_text=f"Lock-up: {st.session_state['pf_lockup_dscr']:.2f}x")
    fig_dscr.add_hline(y=st.session_state["pf_default_dscr"], line_dash="dot",
                       line_color="#ef4444",
                       annotation_text=f"Default: {st.session_state['pf_default_dscr']:.2f}x")
    fig_dscr.add_hline(y=1.0, line_dash="dot", line_color="#9ca3af",
                       annotation_text="1.00x")
    fig_dscr.update_layout(
        height=350,
        title=T("res_dscr_profile"),
        xaxis_title=T("year"), yaxis_title="DSCR (x)",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
    )
    st.plotly_chart(fig_dscr, use_container_width=True)

    # Cash Flow Chart
    st.subheader(T("res_cashflow_chart"))
    all_years_label = list(range(-m["constr_years"] + 1, 1)) + list(m["years"])
    fig_cf = make_subplots(specs=[[{"secondary_y": True}]])
    fig_cf.add_trace(go.Bar(
        x=all_years_label, y=m["project_cf"],
        name="Project CF", marker_color=["#ef4444" if v < 0 else "#1a56db" for v in m["project_cf"]],
    ), secondary_y=False)
    fig_cf.add_trace(go.Scatter(
        x=all_years_label, y=list(m["equity_cumul"]),
        name=T("cumul_equity"), line=dict(color="#16a34a", width=3),
        mode="lines+markers",
    ), secondary_y=True)
    fig_cf.update_layout(
        height=400,
        title=T("res_cashflow_chart"),
        xaxis_title=T("year"), template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    fig_cf.update_yaxes(title_text="R$ MM", secondary_y=False)
    fig_cf.update_yaxes(title_text=T("cumul_equity"), secondary_y=True)
    st.plotly_chart(fig_cf, use_container_width=True)

    # Summary Table
    st.subheader(T("res_summary_table"))
    df_summary = pd.DataFrame({
        T("year"): m["years"],
        T("revenue"): [f"{v:.2f}" for v in m["revenue"]],
        T("opex"): [f"{v:.2f}" for v in m["opex"]],
        T("ebitda"): [f"{v:.2f}" for v in m["ebitda"]],
        T("cfads"): [f"{v:.2f}" for v in m["cfads"]],
        T("debt_service"): [f"{v:.2f}" for v in m["annual_ds"]],
        T("dscr"): [f"{v:.2f}x" if m["annual_ds"][i] > 0 else "n/a"
                    for i, v in enumerate(m["dscr"])],
        T("equity_cf"): [f"{v:.2f}" for v in m["equity_distribution"]],
    })
    st.dataframe(df_summary, use_container_width=True, hide_index=True,
                 height=min(500, 35 * ops_y + 40))

# =====================  TAB 7: SENSITIVITY  =================================
with tabs[6]:
    m_base = build_model()
    st.subheader(T("sens_title"))

    # ── Tornado Chart: key sensitivities ──
    st.subheader(T("sens_tornado_title"))

    def run_sensitivity(param_key, delta_pct, base_val=None):
        """Run model with a % change on a parameter, return equity IRR."""
        if base_val is None:
            base_val = st.session_state[param_key]
        new_val = base_val * (1 + delta_pct / 100.0)
        ov = {param_key: new_val}
        m_s = build_model(override=ov)
        return m_s["equity_irr"]

    def run_rate_sensitivity(delta_pp):
        """Run model with absolute change in interest rate (percentage points)."""
        base_rate = st.session_state["pf_debt_rate"]
        ov = {"pf_debt_rate": base_rate + delta_pp}
        m_s = build_model(override=ov)
        return m_s["equity_irr"]

    base_eirr = m_base["equity_irr"]
    base_eirr_val = base_eirr if base_eirr is not None else 0

    # Revenue sensitivity
    rev_down_irr = run_sensitivity("pf_rev_y1", -20)
    rev_up_irr = run_sensitivity("pf_rev_y1", 20)
    # Cost overrun
    cost_up_irr = run_sensitivity("pf_total_capex", 10)
    cost_up30_irr = run_sensitivity("pf_total_capex", 30)
    # Interest rate
    rate_up_irr = run_rate_sensitivity(2.0)
    rate_down_irr = run_rate_sensitivity(-2.0)
    # OpEx
    opex_up_irr = run_sensitivity("pf_opex_y1", 20)
    opex_down_irr = run_sensitivity("pf_opex_y1", -20)

    def irr_val(x):
        return (x if x is not None else 0) * 100

    categories = [
        T("sens_revenue_vol") + " (+/-20%)",
        "CapEx (+10%/+30%)",
        T("sens_interest_rate") + " (+/-2pp)",
        "OpEx (+/-20%)",
    ]
    low_vals = [
        irr_val(rev_down_irr) - irr_val(base_eirr),
        irr_val(cost_up_irr) - irr_val(base_eirr),
        irr_val(rate_up_irr) - irr_val(base_eirr),
        irr_val(opex_up_irr) - irr_val(base_eirr),
    ]
    high_vals = [
        irr_val(rev_up_irr) - irr_val(base_eirr),
        irr_val(cost_up30_irr) - irr_val(base_eirr),
        irr_val(rate_down_irr) - irr_val(base_eirr),
        irr_val(opex_down_irr) - irr_val(base_eirr),
    ]

    fig_tornado = go.Figure()
    fig_tornado.add_trace(go.Bar(
        y=categories, x=low_vals,
        orientation="h", name="Downside" if lang == "EN" else "Adverso",
        marker_color="#ef4444",
    ))
    fig_tornado.add_trace(go.Bar(
        y=categories, x=high_vals,
        orientation="h", name="Upside" if lang == "EN" else "Favoravel",
        marker_color="#16a34a",
    ))
    fig_tornado.add_vline(x=0, line_color="#1a56db", line_width=2)
    fig_tornado.update_layout(
        barmode="overlay", height=350,
        title=f"{T('sens_tornado_title')} ({T('sens_base')}: {irr_val(base_eirr):.1f}%)",
        xaxis_title="Delta IRR (p.p.)",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_tornado, use_container_width=True)

    st.divider()

    # ── Heat Map: Revenue x Interest Rate ──
    st.subheader(T("sens_heatmap_title"))
    rev_deltas = [-20, -10, -5, 0, 5, 10, 20]
    rate_deltas = [-3, -2, -1, 0, 1, 2, 3]
    heatmap_data = np.zeros((len(rate_deltas), len(rev_deltas)))

    for ri, rd in enumerate(rate_deltas):
        for ci, rvd in enumerate(rev_deltas):
            base_rev = st.session_state["pf_rev_y1"]
            base_rate = st.session_state["pf_debt_rate"]
            ov = {
                "pf_rev_y1": base_rev * (1 + rvd / 100.0),
                "pf_debt_rate": base_rate + rd,
            }
            m_s = build_model(override=ov)
            val = m_s["equity_irr"]
            heatmap_data[ri, ci] = val * 100 if val is not None else 0

    fig_hm = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=[f"{d:+d}%" for d in rev_deltas],
        y=[f"{d:+d}pp" for d in rate_deltas],
        text=[[f"{v:.1f}%" for v in row] for row in heatmap_data],
        texttemplate="%{text}",
        colorscale="RdYlGn",
        colorbar=dict(title="Equity IRR %"),
    ))
    fig_hm.update_layout(
        height=400,
        title=T("sens_heatmap_title"),
        xaxis_title=T("sens_revenue_delta"),
        yaxis_title=T("sens_rate_delta"),
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    st.divider()

    # ── Combined downside scenario ──
    st.subheader(T("sens_combined"))
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        comb_rev = st.slider(T("sens_revenue_delta"), min_value=-30, max_value=0,
                             value=-15, step=5, key="pf_sens_comb_rev")
    with cc2:
        comb_cost = st.slider(T("sens_cost_delta"), min_value=0, max_value=40,
                              value=15, step=5, key="pf_sens_comb_cost")
    with cc3:
        comb_rate = st.slider(T("sens_rate_delta"), min_value=0.0, max_value=5.0,
                              value=2.0, step=0.5, key="pf_sens_comb_rate")

    ov_combined = {
        "pf_rev_y1": st.session_state["pf_rev_y1"] * (1 + comb_rev / 100.0),
        "pf_total_capex": st.session_state["pf_total_capex"] * (1 + comb_cost / 100.0),
        "pf_debt_rate": st.session_state["pf_debt_rate"] + comb_rate,
    }
    m_comb = build_model(override=ov_combined)

    cc4, cc5, cc6, cc7 = st.columns(4)
    comb_eirr = m_comb["equity_irr"]
    comb_eirr_str = f"{comb_eirr*100:.2f}%" if comb_eirr is not None else "n/a"
    comb_cls = "metric-card-green" if comb_eirr and comb_eirr > st.session_state["pf_discount"]/100 else "metric-card-red"
    cc4.markdown(mc(T("res_equity_irr") + " (Combined)", comb_eirr_str, comb_cls), unsafe_allow_html=True)

    comb_dscr_active = m_comb["dscr"][m_comb["annual_ds"] > 0]
    comb_min_dscr = comb_dscr_active.min() if len(comb_dscr_active) > 0 else 0
    comb_dscr_cls = "metric-card-green" if comb_min_dscr >= m_comb["target_dscr"] else "metric-card-red"
    cc5.markdown(mc(T("res_min_dscr"), f"{comb_min_dscr:.2f}x", comb_dscr_cls), unsafe_allow_html=True)

    comb_npv_cls = "metric-card-green" if m_comb["equity_npv"] > 0 else "metric-card-red"
    cc6.markdown(mc(T("res_equity_npv"), f"R$ {m_comb['equity_npv']:.2f} MM", comb_npv_cls), unsafe_allow_html=True)
    cc7.markdown(mc(T("res_debt_capacity"), f"R$ {m_comb['debt_capacity']:.2f} MM"), unsafe_allow_html=True)

    st.divider()

    # ── Probability-Weighted Returns ──
    st.subheader(T("sens_prob_weighted"))

    pw1, pw2, pw3 = st.columns(3)
    with pw1:
        st.markdown(f"**{T('sens_upside')}**")
        prob_up = st.number_input(T("sens_probability"), min_value=0.0, max_value=100.0,
                                  value=25.0, step=5.0, key="pf_prob_up", format="%.0f")
    with pw2:
        st.markdown(f"**{T('sens_base')}**")
        prob_base = st.number_input(T("sens_probability"), min_value=0.0, max_value=100.0,
                                    value=50.0, step=5.0, key="pf_prob_base", format="%.0f")
    with pw3:
        st.markdown(f"**{T('sens_downside')}**")
        prob_down = st.number_input(T("sens_probability"), min_value=0.0, max_value=100.0,
                                    value=25.0, step=5.0, key="pf_prob_down", format="%.0f")

    # Upside: +10% rev, -5% cost
    m_up = build_model(override={
        "pf_rev_y1": st.session_state["pf_rev_y1"] * 1.10,
        "pf_total_capex": st.session_state["pf_total_capex"] * 0.95,
    })
    # Downside: combined scenario values
    m_down = m_comb

    up_eirr = m_up["equity_irr"] if m_up["equity_irr"] is not None else 0
    base_eirr_v = m_base["equity_irr"] if m_base["equity_irr"] is not None else 0
    down_eirr = m_down["equity_irr"] if m_down["equity_irr"] is not None else 0

    total_prob = prob_up + prob_base + prob_down
    if total_prob > 0:
        wtd_irr = (prob_up * up_eirr + prob_base * base_eirr_v + prob_down * down_eirr) / total_prob
    else:
        wtd_irr = 0

    sc_data = {
        T("sens_scenario"): [T("sens_upside"), T("sens_base"), T("sens_downside"), T("sens_wtd_irr")],
        T("sens_probability"): [f"{prob_up:.0f}%", f"{prob_base:.0f}%", f"{prob_down:.0f}%", "100%"],
        T("res_equity_irr"): [
            f"{up_eirr*100:.2f}%", f"{base_eirr_v*100:.2f}%",
            f"{down_eirr*100:.2f}%", f"{wtd_irr*100:.2f}%",
        ],
        T("res_min_dscr"): [
            f"{m_up['dscr'][m_up['annual_ds']>0].min():.2f}x" if np.any(m_up['annual_ds']>0) else "n/a",
            f"{min_dscr:.2f}x",
            f"{comb_min_dscr:.2f}x",
            "--",
        ],
        T("res_npv"): [
            f"R$ {m_up['project_npv']:.2f} MM",
            f"R$ {m_base['project_npv']:.2f} MM",
            f"R$ {m_down['project_npv']:.2f} MM",
            "--",
        ],
    }
    st.dataframe(pd.DataFrame(sc_data), use_container_width=True, hide_index=True)

    # Scenario comparison chart
    fig_sc = go.Figure()
    scenarios = [T("sens_upside"), T("sens_base"), T("sens_downside")]
    irr_vals = [up_eirr * 100, base_eirr_v * 100, down_eirr * 100]
    colors = ["#16a34a", "#1a56db", "#ef4444"]
    fig_sc.add_trace(go.Bar(
        x=scenarios, y=irr_vals,
        marker_color=colors,
        text=[f"{v:.1f}%" for v in irr_vals],
        textposition="outside",
    ))
    fig_sc.add_hline(y=wtd_irr * 100, line_dash="dash", line_color="#f59e0b",
                     annotation_text=f"{T('sens_wtd_irr')}: {wtd_irr*100:.1f}%")
    fig_sc.add_hline(y=st.session_state["pf_discount"], line_dash="dot",
                     line_color="#9ca3af",
                     annotation_text=f"Hurdle: {st.session_state['pf_discount']:.1f}%")
    fig_sc.update_layout(
        height=380,
        title=T("sens_prob_weighted"),
        yaxis_title="Equity IRR (%)",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# =====================  TAB 8: SPE DIAGRAM  =================================
# Per agent_reference.md Section 18a — interactive structure builder
ENTITY_TYPES = {
    "spv":       {"label": "SPV / Project Co.",  "icon": "\U0001f3d7", "color": "#3b82f6"},
    "sponsor":   {"label": "Sponsor (Equity)",   "icon": "\U0001f3e6", "color": "#8b5cf6"},
    "lender":    {"label": "Senior Lender",      "icon": "\U0001f4b0", "color": "#10b981"},
    "mla":       {"label": "MLA / Arranger",     "icon": "\U0001f4cb", "color": "#a78bfa"},
    "dfi":       {"label": "DFI / MDB / IFC",    "icon": "\U0001f30d", "color": "#34d399"},
    "offtaker":  {"label": "Offtaker / PPA",     "icon": "\u26a1",     "color": "#f59e0b"},
    "epc":       {"label": "EPC Contractor",     "icon": "\U0001f527", "color": "#ef4444"},
    "om":        {"label": "O&M Operator",       "icon": "\u2699",     "color": "#06b6d4"},
    "govt":      {"label": "Govt / PPP",         "icon": "\U0001f3db", "color": "#f97316"},
    "insurance": {"label": "Insurance Co.",      "icon": "\U0001f6e1", "color": "#ec4899"},
    "dsra":      {"label": "DSRA / Reserve",     "icon": "\U0001f512", "color": "#14b8a6"},
    "custom":    {"label": "Custom Entity",      "icon": "\U0001f4e6", "color": "#94a3b8"},
}

FLOW_TYPES = {
    "equity":   {"label": "Equity Contribution",  "color": "#8b5cf6", "dash": "solid"},
    "debt":     {"label": "Debt / Loan",          "color": "#10b981", "dash": "solid"},
    "revenue":  {"label": "Revenue / Offtake",    "color": "#f59e0b", "dash": "solid"},
    "payment":  {"label": "Fee / Service Payment","color": "#f59e0b", "dash": "dash"},
    "service":  {"label": "Service / Operational","color": "#06b6d4", "dash": "dash"},
    "security": {"label": "Security / Charge",    "color": "#f87171", "dash": "dot"},
    "custom":   {"label": "Custom Flow",          "color": "#94a3b8", "dash": "dashdot"},
}

# Pre-built templates
SPE_TEMPLATES = {
    "PPP": {
        "nodes": [
            {"id": "n1", "type": "spv",      "name": "Project Co.",   "sub": "SPV",            "x": 400, "y": 300},
            {"id": "n2", "type": "sponsor",  "name": "Sponsor A",     "sub": "Equity 50%",     "x": 100, "y": 100},
            {"id": "n3", "type": "sponsor",  "name": "Sponsor B",     "sub": "Equity 50%",     "x": 250, "y": 100},
            {"id": "n4", "type": "lender",   "name": "Senior Lender", "sub": "Bank Syndicate", "x": 100, "y": 500},
            {"id": "n5", "type": "mla",      "name": "MLA",           "sub": "Arranger",       "x": 250, "y": 500},
            {"id": "n6", "type": "govt",     "name": "Government",    "sub": "Concession",     "x": 700, "y": 100},
            {"id": "n7", "type": "offtaker", "name": "Offtaker",      "sub": "Long-term PPA",  "x": 700, "y": 300},
            {"id": "n8", "type": "epc",      "name": "EPC Co.",       "sub": "Construction",   "x": 700, "y": 500},
            {"id": "n9", "type": "om",       "name": "O&M Operator",  "sub": "Operations",     "x": 550, "y": 600},
        ],
        "edges": [
            {"id": "e1", "from": "n2", "to": "n1", "flow": "equity",  "label": "Equity"},
            {"id": "e2", "from": "n3", "to": "n1", "flow": "equity",  "label": "Equity"},
            {"id": "e3", "from": "n4", "to": "n1", "flow": "debt",    "label": "Senior Loan"},
            {"id": "e4", "from": "n5", "to": "n1", "flow": "debt",    "label": "Co-arranger"},
            {"id": "e5", "from": "n1", "to": "n6", "flow": "service", "label": "Concession"},
            {"id": "e6", "from": "n1", "to": "n7", "flow": "revenue", "label": "Tariff"},
            {"id": "e7", "from": "n1", "to": "n8", "flow": "payment", "label": "EPC Fee"},
            {"id": "e8", "from": "n1", "to": "n9", "flow": "payment", "label": "O&M Fee"},
        ],
    },
    "Renewable Energy": {
        "nodes": [
            {"id": "n1", "type": "spv",      "name": "Solar SPV",      "sub": "Project Co.",      "x": 400, "y": 300},
            {"id": "n2", "type": "sponsor",  "name": "PE Sponsor",     "sub": "Equity 30%",       "x": 100, "y": 150},
            {"id": "n3", "type": "dfi",      "name": "IFC",            "sub": "DFI Lender",       "x": 100, "y": 350},
            {"id": "n4", "type": "lender",   "name": "Commercial Bank","sub": "Senior Lender",    "x": 100, "y": 500},
            {"id": "n5", "type": "offtaker", "name": "Grid Offtaker",  "sub": "20yr PPA",         "x": 700, "y": 200},
            {"id": "n6", "type": "epc",      "name": "EPC Solar",      "sub": "Turnkey",          "x": 700, "y": 400},
            {"id": "n7", "type": "om",       "name": "O&M Provider",   "sub": "5yr contract",     "x": 700, "y": 550},
            {"id": "n8", "type": "dsra",     "name": "Account Bank",   "sub": "DSRA 6 months",    "x": 400, "y": 600},
        ],
        "edges": [
            {"id": "e1", "from": "n2", "to": "n1", "flow": "equity",  "label": "Equity"},
            {"id": "e2", "from": "n3", "to": "n1", "flow": "debt",    "label": "DFI Tranche"},
            {"id": "e3", "from": "n4", "to": "n1", "flow": "debt",    "label": "Senior Debt"},
            {"id": "e4", "from": "n1", "to": "n5", "flow": "revenue", "label": "Energy Sales"},
            {"id": "e5", "from": "n1", "to": "n6", "flow": "payment", "label": "EPC Payment"},
            {"id": "e6", "from": "n1", "to": "n7", "flow": "payment", "label": "O&M Fee"},
            {"id": "e7", "from": "n1", "to": "n8", "flow": "service", "label": "Reserve"},
        ],
    },
    "Mining": {
        "nodes": [
            {"id": "n1", "type": "spv",      "name": "MiningCo SPV",   "sub": "Project Co.",      "x": 400, "y": 300},
            {"id": "n2", "type": "sponsor",  "name": "Mining Co.",     "sub": "Sponsor",          "x": 100, "y": 200},
            {"id": "n3", "type": "dfi",      "name": "ECA",            "sub": "Export Credit",    "x": 100, "y": 400},
            {"id": "n4", "type": "lender",   "name": "Bank Syndicate", "sub": "Senior Lenders",   "x": 250, "y": 500},
            {"id": "n5", "type": "offtaker", "name": "Commodity Buyer","sub": "Offtake",          "x": 700, "y": 200},
            {"id": "n6", "type": "epc",      "name": "Mine EPC",       "sub": "Construction",     "x": 700, "y": 400},
            {"id": "n7", "type": "govt",     "name": "Host Govt",      "sub": "Mining Licence",   "x": 700, "y": 100},
        ],
        "edges": [
            {"id": "e1", "from": "n2", "to": "n1", "flow": "equity",  "label": "Equity"},
            {"id": "e2", "from": "n3", "to": "n1", "flow": "debt",    "label": "ECA Loan"},
            {"id": "e3", "from": "n4", "to": "n1", "flow": "debt",    "label": "Senior Debt"},
            {"id": "e4", "from": "n1", "to": "n5", "flow": "revenue", "label": "Offtake"},
            {"id": "e5", "from": "n1", "to": "n6", "flow": "payment", "label": "EPC"},
            {"id": "e6", "from": "n7", "to": "n1", "flow": "service", "label": "Concession"},
        ],
    },
    "LNG": {
        "nodes": [
            {"id": "n1", "type": "spv",      "name": "LNG Plant Co.",   "sub": "SPV",             "x": 400, "y": 300},
            {"id": "n2", "type": "sponsor",  "name": "Upstream Co.",    "sub": "Sponsor",         "x": 100, "y": 200},
            {"id": "n3", "type": "lender",   "name": "Bank Syndicate",  "sub": "Senior Lenders",  "x": 100, "y": 400},
            {"id": "n4", "type": "offtaker", "name": "LNG Buyer",       "sub": "20yr SPA",        "x": 700, "y": 200},
            {"id": "n5", "type": "epc",      "name": "EPC Contractor",  "sub": "Plant Build",     "x": 700, "y": 400},
            {"id": "n6", "type": "om",       "name": "Shipping Co.",    "sub": "Marine Logistics","x": 550, "y": 550},
        ],
        "edges": [
            {"id": "e1", "from": "n2", "to": "n1", "flow": "equity",  "label": "Equity"},
            {"id": "e2", "from": "n3", "to": "n1", "flow": "debt",    "label": "Senior Debt"},
            {"id": "e3", "from": "n1", "to": "n4", "flow": "revenue", "label": "LNG Sales"},
            {"id": "e4", "from": "n1", "to": "n5", "flow": "payment", "label": "EPC Payment"},
            {"id": "e5", "from": "n1", "to": "n6", "flow": "payment", "label": "Shipping Fee"},
        ],
    },
}

# Initialize diagram state
if "pf_diagram" not in st.session_state:
    st.session_state["pf_diagram"] = {
        "project_name": "", "currency": "USD", "total_ev": 100.0, "closing_date": "",
        "nodes": [], "edges": [],
    }

with tabs[7]:
    st.markdown("### \U0001f578 SPE Diagram Builder")
    st.caption("Build the project finance legal/flow structure visually. Choose a template or build from scratch. Feeds the Contract Minutes generator.")
    st.divider()

    diag = st.session_state["pf_diagram"]

    # ── Top toolbar ──────────────────────────────────────────────────────────
    tb_a, tb_b, tb_c, tb_d = st.columns([2, 2, 2, 1.5])
    with tb_a:
        _tpl = st.selectbox("Pre-built Template",
                            ["(none)"] + list(SPE_TEMPLATES.keys()),
                            key="spe_tpl_sel")
    with tb_b:
        if st.button("Load template", use_container_width=True):
            if _tpl != "(none)":
                tpl = SPE_TEMPLATES[_tpl]
                diag["nodes"] = [dict(n) for n in tpl["nodes"]]
                diag["edges"] = [dict(e) for e in tpl["edges"]]
                diag["project_name"] = _tpl + " Project"
                st.success(f"Loaded {_tpl} template")
                st.rerun()
    with tb_c:
        if st.button("Clear diagram", use_container_width=True):
            diag["nodes"] = []
            diag["edges"] = []
            st.rerun()
    with tb_d:
        st.metric("Nodes", len(diag["nodes"]), label_visibility="visible")

    # ── Project metadata ─────────────────────────────────────────────────────
    with st.expander("Project Metadata", expanded=False):
        m1, m2, m3, m4 = st.columns(4)
        diag["project_name"] = m1.text_input("Project name", value=diag.get("project_name", ""), key="spe_proj_name")
        diag["currency"]     = m2.selectbox("Currency", ["USD","EUR","GBP","BRL"],
                                            index=["USD","EUR","GBP","BRL"].index(diag.get("currency","USD")),
                                            key="spe_currency")
        diag["total_ev"]     = m3.number_input("Total EV ($M)", value=float(diag.get("total_ev", 100.0)), step=10.0, key="spe_total_ev")
        diag["closing_date"] = m4.text_input("Closing date", value=diag.get("closing_date", ""), placeholder="YYYY-MM-DD", key="spe_closing")

    # ── Diagram visualisation (Plotly) ───────────────────────────────────────
    st.markdown("#### Diagram")
    if diag["nodes"]:
        fig_spe = go.Figure()
        node_lookup = {n["id"]: n for n in diag["nodes"]}

        # Edges first (so nodes overlay them)
        for e in diag["edges"]:
            src = node_lookup.get(e["from"]); tgt = node_lookup.get(e["to"])
            if not src or not tgt: continue
            ft = FLOW_TYPES.get(e["flow"], FLOW_TYPES["custom"])
            fig_spe.add_trace(go.Scatter(
                x=[src["x"], tgt["x"]], y=[src["y"], tgt["y"]],
                mode="lines",
                line=dict(color=ft["color"], width=2.2,
                          dash="solid" if ft["dash"] == "solid" else "dash"),
                hoverinfo="text",
                hovertext=f"{e.get('label','')} ({ft['label']})",
                showlegend=False,
            ))
            # Arrow head
            fig_spe.add_annotation(
                x=tgt["x"], y=tgt["y"], ax=src["x"], ay=src["y"],
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1.4, arrowwidth=2,
                arrowcolor=ft["color"], opacity=0.85,
            )
            # Edge label (mid-point)
            mx, my = (src["x"] + tgt["x"]) / 2, (src["y"] + tgt["y"]) / 2
            fig_spe.add_annotation(
                x=mx, y=my, text=f"<b>{e.get('label','')}</b>",
                showarrow=False, font=dict(color=ft["color"], size=10, family="DM Mono"),
                bgcolor="rgba(13,15,20,0.85)", borderpad=2,
            )

        # Nodes
        node_x = [n["x"] for n in diag["nodes"]]
        node_y = [n["y"] for n in diag["nodes"]]
        node_colors = [ENTITY_TYPES.get(n["type"], ENTITY_TYPES["custom"])["color"] for n in diag["nodes"]]
        node_text = [
            f"{ENTITY_TYPES.get(n['type'], ENTITY_TYPES['custom'])['icon']} <b>{n['name']}</b><br>"
            f"<span style='font-size:9px'>{n.get('sub','')}</span>"
            for n in diag["nodes"]
        ]
        fig_spe.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            marker=dict(size=64, color=node_colors, line=dict(color="rgba(255,255,255,0.4)", width=2),
                         symbol="square"),
            text=node_text,
            textposition="middle center",
            textfont=dict(color="white", size=10, family="Syne"),
            hovertext=[f"{n['name']} ({ENTITY_TYPES.get(n['type'], {}).get('label', n['type'])})" for n in diag["nodes"]],
            hoverinfo="text",
            showlegend=False,
        ))

        fig_spe.update_layout(
            height=620,
            paper_bgcolor="rgba(13,15,20,0)",
            plot_bgcolor="rgba(13,15,20,0)",
            xaxis=dict(visible=False, range=[0, 850]),
            yaxis=dict(visible=False, range=[700, 0]),  # invert y so top of canvas = top of screen
            margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_spe, use_container_width=True)
    else:
        st.info("No diagram yet. Load a template above or add nodes manually below.")

    # ── Entity & Edge editors ────────────────────────────────────────────────
    edit_a, edit_b = st.columns(2)

    with edit_a:
        st.markdown("##### Add Entity")
        new_type = st.selectbox("Type", list(ENTITY_TYPES.keys()),
                                format_func=lambda k: f"{ENTITY_TYPES[k]['icon']}  {ENTITY_TYPES[k]['label']}",
                                key="spe_new_type")
        new_name = st.text_input("Name", placeholder="e.g. Solar SPV Ltd", key="spe_new_name")
        new_sub  = st.text_input("Sub-label", placeholder="e.g. Project Company", key="spe_new_sub")
        nx_a, nx_b = st.columns(2)
        new_x = nx_a.number_input("X", value=400, step=20, key="spe_new_x")
        new_y = nx_b.number_input("Y", value=300, step=20, key="spe_new_y")
        if st.button("\u2795 Add entity", type="primary", use_container_width=True):
            new_id = f"n{len(diag['nodes']) + 1}_{new_type}"
            diag["nodes"].append({
                "id": new_id, "type": new_type,
                "name": new_name or ENTITY_TYPES[new_type]["label"],
                "sub": new_sub, "x": new_x, "y": new_y,
            })
            st.rerun()

        if diag["nodes"]:
            st.markdown("##### Remove Entity")
            rm_id = st.selectbox("Pick entity",
                                 [n["id"] for n in diag["nodes"]],
                                 format_func=lambda i: next(f"{n['name']} ({n['type']})" for n in diag["nodes"] if n["id"] == i),
                                 key="spe_rm_node")
            if st.button("\U0001f5d1 Delete entity", use_container_width=True):
                diag["nodes"] = [n for n in diag["nodes"] if n["id"] != rm_id]
                diag["edges"] = [e for e in diag["edges"] if e["from"] != rm_id and e["to"] != rm_id]
                st.rerun()

    with edit_b:
        st.markdown("##### Add Connection")
        if len(diag["nodes"]) < 2:
            st.caption("Add at least 2 entities to create connections.")
        else:
            ids = [n["id"] for n in diag["nodes"]]
            id_label = lambda i: next(f"{n['name']}" for n in diag["nodes"] if n["id"] == i)
            new_from = st.selectbox("From", ids, format_func=id_label, key="spe_new_from")
            new_to   = st.selectbox("To", ids, format_func=id_label, key="spe_new_to",
                                    index=min(1, len(ids) - 1))
            new_flow = st.selectbox("Flow type", list(FLOW_TYPES.keys()),
                                    format_func=lambda k: FLOW_TYPES[k]["label"],
                                    key="spe_new_flow")
            new_label = st.text_input("Label", placeholder="e.g. Senior Loan", key="spe_new_lbl")
            new_amt   = st.text_input("Amount (optional)", placeholder="e.g. $315M", key="spe_new_amt")
            if st.button("\u2795 Add connection", type="primary", use_container_width=True, key="spe_add_edge"):
                if new_from != new_to:
                    diag["edges"].append({
                        "id": f"e{len(diag['edges']) + 1}",
                        "from": new_from, "to": new_to,
                        "flow": new_flow, "label": new_label or FLOW_TYPES[new_flow]["label"],
                        "amount": new_amt,
                    })
                    st.rerun()
                else:
                    st.warning("Source and target must differ.")

        if diag["edges"]:
            st.markdown("##### Remove Connection")
            rm_eid = st.selectbox("Pick connection",
                                  [e["id"] for e in diag["edges"]],
                                  format_func=lambda i: next(
                                      f"{id_label(e['from'])} \u2192 {id_label(e['to'])} ({e['flow']})"
                                      for e in diag["edges"] if e["id"] == i),
                                  key="spe_rm_edge")
            if st.button("\U0001f5d1 Delete connection", use_container_width=True, key="spe_del_edge"):
                diag["edges"] = [e for e in diag["edges"] if e["id"] != rm_eid]
                st.rerun()

    # ── Legend ───────────────────────────────────────────────────────────────
    with st.expander("Legend — Entity & Flow Types", expanded=False):
        leg_a, leg_b = st.columns(2)
        with leg_a:
            st.markdown("**Entity types**")
            for k, v in ENTITY_TYPES.items():
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0">'
                    f'<span style="width:14px;height:14px;background:{v["color"]};border-radius:3px;display:inline-block"></span>'
                    f'<span style="font-family:Syne;font-size:.78rem">{v["icon"]} {v["label"]}</span></div>',
                    unsafe_allow_html=True)
        with leg_b:
            st.markdown("**Flow types**")
            for k, v in FLOW_TYPES.items():
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0">'
                    f'<span style="width:24px;height:0;border-top:2px {v["dash"] if v["dash"] != "solid" else "solid"} {v["color"]};display:inline-block"></span>'
                    f'<span style="font-family:Syne;font-size:.78rem">{v["label"]}</span></div>',
                    unsafe_allow_html=True)

# =====================  TAB 9: CONTRACT MINUTES  ============================
with tabs[8]:
    st.markdown("### \U0001f4dc Contract Minutes")
    st.caption("Auto-drafted contract documents based on your SPE diagram and PF assumptions. Placeholders [\u25cf] are highlighted in amber.")

    diag = st.session_state.get("pf_diagram", {"nodes": [], "edges": []})

    if not diag["nodes"]:
        st.info("Build a diagram in the **SPE Diagram** tab first.")
    else:
        # ── Classify diagram ─────────────────────────────────────────────────
        counts = {}
        for n in diag["nodes"]:
            counts[n["type"]] = counts.get(n["type"], 0) + 1
        flags = {
            "num_lenders":   counts.get("lender", 0) + counts.get("mla", 0) + counts.get("dfi", 0),
            "num_sponsors":  counts.get("sponsor", 0),
            "has_spv":       counts.get("spv", 0) > 0,
            "has_dfi":       counts.get("dfi", 0) > 0,
            "has_govt":      counts.get("govt", 0) > 0,
            "has_epc":       counts.get("epc", 0) > 0,
            "has_om":        counts.get("om", 0) > 0,
            "has_offtaker":  counts.get("offtaker", 0) > 0,
            "has_dsra":      counts.get("dsra", 0) > 0,
            "has_insurance": counts.get("insurance", 0) > 0,
        }

        # ── Select documents per Section 18d ─────────────────────────────────
        docs = []
        if flags["has_spv"] and flags["num_lenders"] > 0:
            docs.append("Facility Agreement")
        if flags["num_lenders"] >= 2 or flags["has_dfi"]:
            docs.append("Common Terms Agreement")
        if flags["num_lenders"] >= 2:
            docs.append("Intercreditor Agreement")
        if flags["has_epc"]:      docs.append("Direct Agreement \u2014 EPC Contractor")
        if flags["has_om"]:       docs.append("Direct Agreement \u2014 O&M Operator")
        if flags["has_offtaker"]: docs.append("Direct Agreement \u2014 Offtaker / PPA")
        if flags["has_govt"]:     docs.append("Direct Agreement \u2014 Concession / PPP")
        docs.append("Security Trust Deed")
        docs.append("Accounts Agreement")

        # Diagnostic info
        info_col1, info_col2, info_col3 = st.columns(3)
        info_col1.metric("Documents to generate", len(docs))
        info_col2.metric("Lenders", flags["num_lenders"])
        info_col3.metric("Sponsors", flags["num_sponsors"])

        if not docs:
            st.warning("Diagram has no SPV + Lender combination — no contracts can be generated.")
        else:
            # ── Sidebar: doc list + main: rendered clauses ──────────────────
            doc_col, clause_col = st.columns([1, 3])
            with doc_col:
                st.markdown("##### Generated Documents")
                doc_sel = st.radio("Documents", docs, key="cm_doc_sel", label_visibility="collapsed")

            with clause_col:
                # ── Extract parties ──────────────────────────────────────────
                spv      = next((n for n in diag["nodes"] if n["type"] == "spv"), None)
                sponsors = [n for n in diag["nodes"] if n["type"] == "sponsor"]
                lenders  = [n for n in diag["nodes"] if n["type"] in ("lender", "mla", "dfi")]
                dsra_node = next((n for n in diag["nodes"] if n["type"] == "dsra"), None)

                # ── Pull assumptions from session state ──────────────────────
                total_ev = float(diag.get("total_ev", 100.0))
                debt_pct = 0.70  # default
                debt_amt = total_ev * debt_pct
                eq_amt   = total_ev * (1 - debt_pct)
                currency = diag.get("currency", "USD")

                vars_ = {
                    "{{BORROWER_NAME}}":   spv["name"] if spv else "[\u25cf PROJECT CO.]",
                    "{{SPONSOR_NAMES}}":   " and ".join(s["name"] for s in sponsors) or "[\u25cf SPONSORS]",
                    "{{LENDER_NAMES}}":    ", ".join(l["name"] for l in lenders) or "[\u25cf LENDERS]",
                    "{{CURRENCY}}":        currency,
                    "{{FACILITY_AMOUNT}}": f"{debt_amt:,.0f}M",
                    "{{EQUITY_AMOUNT}}":   f"{eq_amt:,.0f}M",
                    "{{TOTAL_EV}}":        f"{total_ev:,.0f}M",
                    "{{DEBT_PCT}}":        f"{debt_pct*100:.0f}",
                    "{{EQUITY_PCT}}":      f"{(1-debt_pct)*100:.0f}",
                    "{{TENOR}}":           "15",
                    "{{MARGIN}}":          "2.00",
                    "{{FLOATING_RATE_INDEX}}": "SOFR",
                    "{{DSCR_MINIMUM}}":    "1.20",
                    "{{LLCR_MINIMUM}}":    "1.15",
                    "{{GEARING_MAX}}":     f"{debt_pct*100:.0f}",
                    "{{DSRA_MONTHS}}":     "6",
                    "{{ACCOUNT_BANK}}":    dsra_node["name"] if dsra_node else "[\u25cf ACCOUNT BANK]",
                    "{{GOVERNING_LAW}}":   "English law",
                    "{{JURISDICTION_COURTS}}": "England and Wales",
                    "{{PROJECT_DESCRIPTION}}": diag.get("project_name", "[\u25cf PROJECT]"),
                    "{{CASH_SWEEP_PCT}}":  "100",
                    "{{DSCR_SCULPTING_TARGET}}": "1.25",
                    "{{REPAYMENT_COMMENCEMENT}}": "[\u25cf]",
                }

                # ── Document content templates ───────────────────────────────
                FACILITY_AGREEMENT = """
# FACILITY AGREEMENT

**Parties:**
- {{BORROWER_NAME}} (the **Borrower**)
- {{LENDER_NAMES}} (the **Lenders**)
- {{SPONSOR_NAMES}} (the **Sponsors**)

---

### Clause 1 — DEFINITIONS AND INTERPRETATION
'CFADS' means Cash Flow Available for Debt Service. 'COD' or 'Commercial Operation Date' means [\u25cf]. 'DSRA' means the Debt Service Reserve Account maintained with {{ACCOUNT_BANK}} in accordance with Clause 14. 'DSCR' means the Debt Service Coverage Ratio.

### Clause 2 — THE FACILITY
2.1 The Lenders make available to the Borrower a term loan facility in an aggregate amount of **{{CURRENCY}} {{FACILITY_AMOUNT}}** (the 'Facility').
2.2 The Facility is available for the sole purpose of financing the **{{PROJECT_DESCRIPTION}}** (the 'Project').
2.3 The total capital cost of the Project is approximately **{{CURRENCY}} {{TOTAL_EV}}**, financed as follows:
  (a) Equity of {{CURRENCY}} {{EQUITY_AMOUNT}} ({{EQUITY_PCT}}%) to be contributed by {{SPONSOR_NAMES}}; and
  (b) Senior Debt of {{CURRENCY}} {{FACILITY_AMOUNT}} ({{DEBT_PCT}}%) under this Facility.

### Clause 5 — REPAYMENT
5.1 The Borrower shall repay the Facility in accordance with the Repayment Schedule, sculpted to maintain a DSCR of not less than **{{DSCR_SCULPTING_TARGET}}x** in each period.
5.2 Repayment shall commence on the first Payment Date following {{REPAYMENT_COMMENCEMENT}}, being **{{TENOR}} years** from COD.
5.3 Cash Sweep: **{{CASH_SWEEP_PCT}}%** of Excess Cash Flow shall be applied in optional prepayment of the Facility.

### Clause 6 — INTEREST
6.1 The rate of interest is the aggregate of: (a) the Applicable Margin of **{{MARGIN}}%** per annum; and (b) **{{FLOATING_RATE_INDEX}}** for the relevant Interest Period.
6.3 During construction, interest shall be capitalised to the Facility (Interest During Construction, 'IDC').

### Clause 9 — FINANCIAL COVENANTS
9.1 The Borrower shall ensure that:
  (a) the DSCR for each period shall not be less than **{{DSCR_MINIMUM}}x**;
  (b) the LLCR shall not be less than **{{LLCR_MINIMUM}}x**;
  (c) the ratio of Total Senior Debt to Total Project Cost shall not exceed **{{GEARING_MAX}}%**;
  (d) the DSRA shall be funded to **{{DSRA_MONTHS}} months** of projected Debt Service.

### Clause 14 — RESERVE ACCOUNTS
14.1 The Borrower shall maintain the DSRA with **{{ACCOUNT_BANK}}**, funded to **{{DSRA_MONTHS}} months** of projected Debt Service.

### Clause 15 — GOVERNING LAW
15.1 This Agreement is governed by **{{GOVERNING_LAW}}**.
15.2 The courts of **{{JURISDICTION_COURTS}}** shall have non-exclusive jurisdiction.
"""

                CTA_TEMPLATE = """
# COMMON TERMS AGREEMENT

**Parties:** {{BORROWER_NAME}}, {{LENDER_NAMES}}

This Common Terms Agreement establishes uniform definitions, representations, covenants and events of default that apply to **all** Finance Documents entered into by the Borrower with the Finance Parties identified above.

### Common Definitions
All capitalized terms in any Finance Document shall have the meaning assigned in this Agreement.

### Common Representations & Warranties
The Borrower represents that it: (a) is duly incorporated; (b) has corporate power to enter into the Finance Documents; (c) holds all necessary authorisations; (d) is in compliance with all applicable laws.

### Common Covenants
The Borrower undertakes to comply with all covenants in Clause 9 of the Facility Agreement on a uniform basis.

### Common Events of Default
The events of default in Clause 13 of the Facility Agreement shall apply equally under all Finance Documents.
"""

                INTERCREDITOR_TEMPLATE = """
# INTERCREDITOR AGREEMENT

**Parties:** {{LENDER_NAMES}} (the **Senior Creditors**), {{BORROWER_NAME}}

### Ranking
Senior Debt ranks pari passu among the Senior Creditors. All Senior Creditors share rateably in the security package and proceeds of enforcement.

### Voting Rights
Decisions requiring Majority Lender approval require **66 2/3%** by commitment value. Unanimous decisions are required for: (a) extension of maturity; (b) reduction of margin; (c) release of security.

### Standstill Period
On occurrence of an Event of Default, no individual Lender may take enforcement action for **90 days**, during which Majority Lenders shall determine the collective response.
"""

                STD_TEMPLATE = """
# SECURITY TRUST DEED

**Parties:** {{BORROWER_NAME}}, **Security Trustee** (TBD), {{LENDER_NAMES}}

### Security Package
The Borrower hereby grants to the Security Trustee, for the benefit of the Finance Parties:
1. First-ranking fixed and floating charge over all present and future assets of the Borrower
2. Assignment by way of security of all rights under the Project Documents
3. Pledge over all shares in the Borrower held by **{{SPONSOR_NAMES}}**
4. Assignment of all Project Accounts (including the DSRA at {{ACCOUNT_BANK}})
5. Assignment of all insurance policies
"""

                ACCOUNTS_TEMPLATE = """
# ACCOUNTS AGREEMENT

**Parties:** {{BORROWER_NAME}}, {{ACCOUNT_BANK}} (the **Account Bank**), {{LENDER_NAMES}}

### Project Accounts
The Borrower shall maintain the following Project Accounts with the Account Bank:
1. **Proceeds Account** — receives all revenues
2. **Operating Account** — funds OpEx and capital expenditure
3. **Debt Service Account** — funds scheduled debt service
4. **Debt Service Reserve Account (DSRA)** — funded to {{DSRA_MONTHS}} months forward debt service
5. **Distribution Account** — funds equity distributions when permitted by Clause 12

### Cash Waterfall
Cash flows shall be applied in the following order:
1. Operating expenses
2. Maintenance CapEx
3. Tax payments
4. Senior Debt Service
5. DSRA top-up
6. MMRA top-up
7. Permitted Equity Distributions
"""

                DA_EPC_TEMPLATE = """
# DIRECT AGREEMENT — EPC CONTRACTOR

**Parties:** {{BORROWER_NAME}}, EPC Contractor (per diagram), {{LENDER_NAMES}}

The EPC Contractor acknowledges that the EPC Contract has been assigned by way of security to the Senior Lenders. On occurrence of an Event of Default by the Borrower, the Senior Lenders may **step-in** and assume the Borrower's rights and obligations under the EPC Contract.
"""
                DA_OM_TEMPLATE = """
# DIRECT AGREEMENT — O&M OPERATOR

**Parties:** {{BORROWER_NAME}}, O&M Operator (per diagram), {{LENDER_NAMES}}

The O&M Operator acknowledges the assignment by way of security and consents to step-in rights of the Senior Lenders.
"""
                DA_OFFTAKER_TEMPLATE = """
# DIRECT AGREEMENT — OFFTAKER

**Parties:** {{BORROWER_NAME}}, Offtaker (per diagram), {{LENDER_NAMES}}

The Offtaker acknowledges the assignment of revenues by way of security to the Senior Lenders and shall pay all amounts under the Offtake Agreement directly to the Proceeds Account at the Account Bank.
"""
                DA_GOVT_TEMPLATE = """
# DIRECT AGREEMENT — CONCESSION / PPP

**Parties:** {{BORROWER_NAME}}, Contracting Authority (per diagram), {{LENDER_NAMES}}

The Contracting Authority acknowledges the security granted under the Concession and consents to lender step-in rights.
"""

                DOC_TEMPLATES = {
                    "Facility Agreement": FACILITY_AGREEMENT,
                    "Common Terms Agreement": CTA_TEMPLATE,
                    "Intercreditor Agreement": INTERCREDITOR_TEMPLATE,
                    "Security Trust Deed": STD_TEMPLATE,
                    "Accounts Agreement": ACCOUNTS_TEMPLATE,
                    "Direct Agreement \u2014 EPC Contractor": DA_EPC_TEMPLATE,
                    "Direct Agreement \u2014 O&M Operator": DA_OM_TEMPLATE,
                    "Direct Agreement \u2014 Offtaker / PPA": DA_OFFTAKER_TEMPLATE,
                    "Direct Agreement \u2014 Concession / PPP": DA_GOVT_TEMPLATE,
                }

                template = DOC_TEMPLATES.get(doc_sel, "")
                # Populate variables
                rendered = template
                for k, v in vars_.items():
                    rendered = rendered.replace(k, str(v))

                # Highlight [●] placeholders in amber
                rendered_html = rendered.replace(
                    "[\u25cf]",
                    '<span style="background:rgba(245,158,11,0.20);color:#f59e0b;'
                    'padding:1px 6px;border-radius:4px;border:1px solid rgba(245,158,11,0.4);'
                    'font-family:DM Mono,monospace;font-size:.86em">[\u25cf]</span>'
                )
                # Wrap in styled container
                st.markdown(
                    f'<div style="background:var(--surface);border:1px solid var(--border);'
                    f'border-radius:12px;padding:24px 28px;font-family:Syne,sans-serif;'
                    f'line-height:1.7;color:var(--text);max-height:680px;overflow-y:auto">'
                    f'{rendered_html}</div>',
                    unsafe_allow_html=True,
                )

                # Toolbar
                st.divider()
                tb1, tb2 = st.columns([1, 4])
                with tb1:
                    st.download_button(
                        "\u2b07 Download (.md)",
                        data=rendered,
                        file_name=f"{doc_sel.lower().replace(' ', '_').replace('—', '').replace('/', '')}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div style="text-align:center;padding:20px 0 10px 0;margin-top:40px;
border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.75rem">
Project Finance Model &mdash; Built with Streamlit
</div>""", unsafe_allow_html=True)
