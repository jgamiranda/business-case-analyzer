# ─────────────────────────────────────────────────────────────────────────────
# 03_Project_Finance.py — Streamlit page: Project Finance Model
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BILINGUAL LABELS (PT / EN)
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "page_title": "Project Finance",
    "page_sub": "Modelo de financiamento de projetos com estrutura de divida e cascata de caixa",
    "tab_project": "  Projeto  ", "tab_construction": "  Construcao  ",
    "tab_operations": "  Operacao  ", "tab_debt": "  Dimensionamento de Divida  ",
    "tab_waterfall": "  Cascata de Caixa  ", "tab_results": "  Resultados  ",
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
    "debt_title": "Dimensionamento de Divida Senior",
    "debt_target_dscr": "DSCR alvo (x)",
    "debt_tenor": "Tenor da divida (anos)",
    "debt_grace": "Periodo de carencia (anos)",
    "debt_rate": "Taxa de juros (% a.a.)",
    "debt_amort_type": "Tipo de amortizacao",
    "debt_max_capacity": "Capacidade maxima de divida",
    "debt_leverage": "Alavancagem (Divida / CapEx total)",
    "debt_equity_needed": "Equity necessario",
    "debt_schedule": "Cronograma de Servico da Divida",
    # Waterfall tab
    "wf_title": "Cascata de Fluxo de Caixa",
    "wf_revenue": "Receita Bruta",
    "wf_opex": "(-) OpEx",
    "wf_taxes": "(-) Impostos",
    "wf_senior_debt": "(-) Servico Divida Senior",
    "wf_reserve": "(-) Reservas",
    "wf_equity_dist": "= Distribuicao ao Equity",
    "wf_reserve_months": "Reserva em meses de servico de divida",
    "wf_chart_title": "Cascata Anual de Caixa",
    # Results tab
    "res_title": "Metricas de Retorno e Risco",
    "res_project_irr": "TIR do Projeto",
    "res_equity_irr": "TIR do Equity",
    "res_min_dscr": "DSCR Minimo",
    "res_avg_dscr": "DSCR Medio",
    "res_llcr": "LLCR",
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
},
"EN": {
    "page_title": "Project Finance",
    "page_sub": "Project financing model with debt structuring and cash flow waterfall",
    "tab_project": "  Project  ", "tab_construction": "  Construction  ",
    "tab_operations": "  Operations  ", "tab_debt": "  Debt Sizing  ",
    "tab_waterfall": "  Cash Waterfall  ", "tab_results": "  Results  ",
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
    "debt_title": "Senior Debt Sizing",
    "debt_target_dscr": "Target DSCR (x)",
    "debt_tenor": "Debt tenor (years)",
    "debt_grace": "Grace period (years)",
    "debt_rate": "Interest rate (% p.a.)",
    "debt_amort_type": "Amortization type",
    "debt_max_capacity": "Maximum debt capacity",
    "debt_leverage": "Leverage (Debt / Total CapEx)",
    "debt_equity_needed": "Equity needed",
    "debt_schedule": "Debt Service Schedule",
    # Waterfall tab
    "wf_title": "Cash Flow Waterfall",
    "wf_revenue": "Gross Revenue",
    "wf_opex": "(-) OpEx",
    "wf_taxes": "(-) Taxes",
    "wf_senior_debt": "(-) Senior Debt Service",
    "wf_reserve": "(-) Reserves",
    "wf_equity_dist": "= Equity Distribution",
    "wf_reserve_months": "Reserve in months of debt service",
    "wf_chart_title": "Annual Cash Waterfall",
    # Results tab
    "res_title": "Return & Risk Metrics",
    "res_project_irr": "Project IRR",
    "res_equity_irr": "Equity IRR",
    "res_min_dscr": "Minimum DSCR",
    "res_avg_dscr": "Average DSCR",
    "res_llcr": "LLCR",
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
},
}

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTOR + HEADER
# ─────────────────────────────────────────────────────────────────────────────
_hdr_col, _lang_col = st.columns([8, 1])
with _lang_col:
    st.write("")
    _lang_sel = st.segmented_control("pf_lang", ["PT", "EN"], default="PT",
                                     key="pf_lang", label_visibility="collapsed")
lang = _lang_sel or "PT"
L = _L[lang]
def T(k): return L.get(k, _L["PT"].get(k, k))

with _hdr_col:
    st.markdown(f"""<div class="pf-header">
        <h1>{T("page_title")}</h1>
        <p>{T("page_sub")}</p>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "pf_name": "", "pf_sector_idx": 0,
    "pf_constr_months": 24, "pf_ops_months": 240, "pf_total_capex": 500.0,
    "pf_discount": 12.0, "pf_tax_rate": 34.0,
    "pf_capex_dist": "Uniforme", "pf_idc_rate": 10.0,
    "pf_rev_y1": 120.0, "pf_rev_growth": 3.0,
    "pf_opex_y1": 40.0, "pf_opex_growth": 2.5,
    "pf_maint_capex_pct": 2.0, "pf_ramp_up_pct": 70.0,
    "pf_depr_life": 20,
    "pf_target_dscr": 1.30, "pf_debt_tenor": 15, "pf_grace": 2,
    "pf_debt_rate": 10.0, "pf_amort_type": "SAC",
    "pf_reserve_months": 6,
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
    # Need at least one sign change
    signs = np.sign(cf[cf != 0])
    if len(signs) < 2 or np.all(signs == signs[0]):
        return None
    try:
        # np.irr was removed; use polynomial approach
        # NPV = sum cf_t / (1+r)^t = 0  =>  sum cf_t * x^(n-t) = 0 where x=1/(1+r)
        n = len(cf) - 1
        coeffs = cf[::-1]  # reverse for polynomial: highest power first
        roots = np.roots(coeffs)
        # Filter real positive roots
        real_roots = []
        for r in roots:
            if np.isreal(r) and r.real > 0:
                real_roots.append(r.real)
        if not real_roots:
            return None
        # x = 1/(1+irr) => irr = 1/x - 1
        irrs = [1.0 / x - 1.0 for x in real_roots]
        # Pick IRR closest to 0 and reasonable
        valid = [i for i in irrs if -0.5 < i < 10.0]
        if not valid:
            return None
        return min(valid, key=abs) if len(valid) > 1 else valid[0]
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────────────────────
# CORE MODEL CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────
def build_model():
    """Build the full project finance model from session state. Returns dict."""
    constr_m = st.session_state["pf_constr_months"]
    ops_m = st.session_state["pf_ops_months"]
    total_capex = st.session_state["pf_total_capex"]
    disc = st.session_state["pf_discount"] / 100.0
    tax = st.session_state["pf_tax_rate"] / 100.0
    idc_rate = st.session_state["pf_idc_rate"] / 100.0
    rev_y1 = st.session_state["pf_rev_y1"]
    rev_g = st.session_state["pf_rev_growth"] / 100.0
    opex_y1 = st.session_state["pf_opex_y1"]
    opex_g = st.session_state["pf_opex_growth"] / 100.0
    maint_pct = st.session_state["pf_maint_capex_pct"] / 100.0
    ramp_pct = st.session_state["pf_ramp_up_pct"] / 100.0
    depr_life = max(st.session_state["pf_depr_life"], 1)
    target_dscr = st.session_state["pf_target_dscr"]
    debt_tenor = st.session_state["pf_debt_tenor"]
    grace = st.session_state["pf_grace"]
    debt_rate = st.session_state["pf_debt_rate"] / 100.0
    amort_type = st.session_state["pf_amort_type"]
    reserve_months = st.session_state["pf_reserve_months"]

    constr_q = max(math.ceil(constr_m / 3), 1)
    ops_years = max(math.ceil(ops_m / 12), 1)

    # ── Construction phase: quarterly CapEx schedule ──
    dist_type = st.session_state.get("pf_capex_dist", "Uniforme")
    if dist_type in ("Uniforme", "Uniform"):
        capex_schedule = np.ones(constr_q) / constr_q * total_capex
    elif dist_type in ("Concentrado no inicio", "Front-loaded"):
        weights = np.linspace(2, 0.5, constr_q)
        capex_schedule = weights / weights.sum() * total_capex
    elif dist_type in ("Concentrado no final", "Back-loaded"):
        weights = np.linspace(0.5, 2, constr_q)
        capex_schedule = weights / weights.sum() * total_capex
    else:
        # Custom — check session state for custom values
        custom_key = "pf_custom_capex"
        if custom_key in st.session_state and len(st.session_state[custom_key]) == constr_q:
            raw = np.array(st.session_state[custom_key], dtype=float)
            s = raw.sum()
            capex_schedule = raw / s * total_capex if s > 0 else np.ones(constr_q) / constr_q * total_capex
        else:
            capex_schedule = np.ones(constr_q) / constr_q * total_capex

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

    # ── Operations phase: annual projections ──
    years = list(range(1, ops_years + 1))
    revenue = np.zeros(ops_years)
    opex = np.zeros(ops_years)
    maint_capex = np.zeros(ops_years)
    depreciation = np.full(ops_years, total_invested / depr_life)
    # Cap depreciation at ops_years
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
    nopat = ebit - taxes_on_ebit
    # CFADS = EBITDA - Taxes (on EBIT) - Maintenance CapEx  (maint already in ebitda)
    cfads = ebitda - taxes_on_ebit  # maintenance capex already subtracted from ebitda

    # ── Debt sizing based on target DSCR ──
    # For each year in repayment period, max debt service = CFADS / target_DSCR
    repayment_start = grace  # years of grace from start of operations
    repayment_years = debt_tenor - grace
    if repayment_years <= 0:
        repayment_years = max(debt_tenor, 1)
        repayment_start = 0

    # Build debt service capacity per year
    max_ds_per_year = np.zeros(ops_years)
    for i in range(ops_years):
        if cfads[i] > 0:
            max_ds_per_year[i] = cfads[i] / target_dscr

    # Calculate max debt via iterative approach for SAC
    # For SAC: principal_payment = Debt / repayment_years (constant)
    # Total DS in year t = principal + interest on outstanding
    # We solve for max Debt such that DS_t <= max_ds_per_year[t] for all repayment years

    debt_capacity = 0.0
    annual_principal = np.zeros(ops_years)
    annual_interest = np.zeros(ops_years)
    annual_ds = np.zeros(ops_years)
    outstanding = np.zeros(ops_years + 1)

    if amort_type == "SAC":
        # SAC: equal principal, declining interest
        # Find max debt: constrained by each repayment year
        # DS_t = D/n + (D - (t-g)*D/n)*r = D*(1/n + r - (t-g)*r/n)
        # DS_t / D = 1/n + r*(1 - (t-g)/n)   for t in [g..g+n-1]
        # D <= max_ds_t / factor_t  for all t
        n = repayment_years
        if n > 0:
            candidates = []
            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years)):
                t_in_repay = yr_idx - repayment_start  # 0-indexed period in repayment
                factor = 1.0 / n + debt_rate * (1.0 - t_in_repay / n)
                if factor > 0 and max_ds_per_year[yr_idx] > 0:
                    candidates.append(max_ds_per_year[yr_idx] / factor)
            debt_capacity = min(candidates) if candidates else 0.0
        # Cap at total invested
        debt_capacity = min(debt_capacity, total_invested)
        debt_capacity = max(debt_capacity, 0.0)

        # Build schedule
        outstanding[0] = debt_capacity
        pp = debt_capacity / n if n > 0 else 0
        for i in range(ops_years):
            if i < repayment_start:
                # Grace period: interest only (or capitalized)
                annual_interest[i] = outstanding[i] * debt_rate
                annual_principal[i] = 0
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
        # Price (annuity): equal total payments
        n = repayment_years
        if n > 0 and debt_rate > 0:
            annuity_factor = debt_rate / (1 - (1 + debt_rate) ** (-n))
            # max DS = min of max_ds_per_year over repayment period
            ds_available = []
            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years)):
                ds_available.append(max_ds_per_year[yr_idx])
            max_annual_ds = min(ds_available) if ds_available else 0
            debt_capacity = max_annual_ds / annuity_factor if annuity_factor > 0 else 0
        elif n > 0:
            ds_available = []
            for yr_idx in range(repayment_start, min(repayment_start + n, ops_years)):
                ds_available.append(max_ds_per_year[yr_idx])
            max_annual_ds = min(ds_available) if ds_available else 0
            debt_capacity = max_annual_ds * n
        debt_capacity = min(max(debt_capacity, 0), total_invested)

        outstanding[0] = debt_capacity
        if n > 0 and debt_rate > 0:
            pmt = debt_capacity * debt_rate / (1 - (1 + debt_rate) ** (-n))
        elif n > 0:
            pmt = debt_capacity / n
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

    else:  # Bullet
        n = debt_tenor
        if n > 0:
            # Bullet: interest only, principal at maturity
            # DS during tenor = interest; final year = interest + principal
            # Need CFADS[last] / target_dscr >= D*r + D  =>  D <= CFADS[last] / (target_dscr*(1+r))
            candidates = []
            for yr_idx in range(min(n, ops_years)):
                if yr_idx == n - 1:
                    factor = debt_rate + 1.0
                else:
                    factor = debt_rate
                if factor > 0 and max_ds_per_year[yr_idx] > 0:
                    candidates.append(max_ds_per_year[yr_idx] / factor)
            debt_capacity = min(candidates) if candidates else 0
        debt_capacity = min(max(debt_capacity, 0), total_invested)

        outstanding[0] = debt_capacity
        for i in range(ops_years):
            if i < n and i < ops_years:
                annual_interest[i] = outstanding[i] * debt_rate
                if i == n - 1:
                    annual_principal[i] = outstanding[i]
                    annual_ds[i] = annual_interest[i] + annual_principal[i]
                    outstanding[i + 1] = 0
                else:
                    annual_ds[i] = annual_interest[i]
                    outstanding[i + 1] = outstanding[i]
            else:
                outstanding[i + 1] = max(outstanding[i], 0)

    # ── DSCR profile ──
    dscr = np.zeros(ops_years)
    for i in range(ops_years):
        if annual_ds[i] > 0:
            dscr[i] = cfads[i] / annual_ds[i]
        else:
            dscr[i] = 0  # no debt service

    # ── LLCR: Loan Life Coverage Ratio ──
    # LLCR = NPV(CFADS over remaining debt life) / Outstanding debt
    # Computed at year 0 (start of operations)
    debt_life_end = repayment_start + repayment_years if amort_type != "Bullet" else debt_tenor
    npv_cfads_debt = 0
    for i in range(min(debt_life_end, ops_years)):
        npv_cfads_debt += cfads[i] / ((1 + disc) ** (i + 1))
    llcr = npv_cfads_debt / debt_capacity if debt_capacity > 0 else 0

    # ── Waterfall ──
    # Reserve account: accumulate reserve_months worth of annual DS / 12
    reserve_target = np.zeros(ops_years)
    reserve_contribution = np.zeros(ops_years)
    reserve_balance = np.zeros(ops_years + 1)
    equity_distribution = np.zeros(ops_years)

    for i in range(ops_years):
        cf_after_ds = cfads[i] - annual_ds[i]
        # Reserve target = reserve_months / 12 * next year DS (or current if last)
        next_ds = annual_ds[i + 1] if i + 1 < ops_years else annual_ds[i]
        reserve_target[i] = (reserve_months / 12.0) * next_ds
        needed = max(reserve_target[i] - reserve_balance[i], 0)
        reserve_contribution[i] = min(needed, max(cf_after_ds, 0))
        reserve_balance[i + 1] = reserve_balance[i] + reserve_contribution[i]
        equity_distribution[i] = max(cf_after_ds - reserve_contribution[i], 0)

    # ── Project IRR: CapEx as negative, CFADS as positive ──
    # Construction: quarterly negative CFs → convert to annual
    constr_years = max(math.ceil(constr_m / 12), 1)
    project_cf = []
    # Spread CapEx across construction years
    capex_annual = np.zeros(constr_years)
    months_per_q = 3
    for q in range(constr_q):
        yr = min(int(q * months_per_q / 12), constr_years - 1)
        capex_annual[yr] += capex_schedule[q]
    # Add IDC to last construction year
    capex_annual[-1] += idc_total

    for i in range(constr_years):
        project_cf.append(-capex_annual[i])
    for i in range(ops_years):
        project_cf.append(cfads[i])

    project_irr = safe_irr(project_cf)

    # ── Equity IRR: equity investment as negative, distributions as positive ──
    equity_invested = total_invested - debt_capacity
    equity_cf_list = []
    # Spread equity across construction years proportionally
    for i in range(constr_years):
        eq_share = capex_annual[i] / total_capex * equity_invested if total_capex > 0 else 0
        if i == constr_years - 1:
            # Add IDC share to equity (IDC funded by debt draw; but equity portion)
            eq_share += idc_total * (equity_invested / total_invested) if total_invested > 0 else 0
        equity_cf_list.append(-eq_share)
    for i in range(ops_years):
        equity_cf_list.append(equity_distribution[i])

    equity_irr = safe_irr(equity_cf_list)

    # ── NPV ──
    project_npv = sum(cf / (1 + disc) ** t for t, cf in enumerate(project_cf))
    equity_npv = sum(cf / (1 + disc) ** t for t, cf in enumerate(equity_cf_list))

    # ── Payback ──
    cumul = 0
    payback = None
    for i, cf in enumerate(equity_cf_list):
        cumul += cf
        if cumul >= 0 and payback is None:
            payback = i  # years from start (includes construction)

    # ── Cumulative equity CF for chart ──
    equity_cumul = np.cumsum(equity_cf_list)

    return {
        "years": years, "ops_years": ops_years, "constr_q": constr_q,
        "constr_years": constr_years,
        "capex_schedule": capex_schedule, "capex_annual": capex_annual,
        "idc_by_q": idc_by_q, "idc_total": idc_total,
        "total_invested": total_invested,
        "revenue": revenue, "opex": opex, "maint_capex": maint_capex,
        "ebitda": ebitda, "depreciation": depreciation,
        "ebit": ebit, "taxes_on_ebit": taxes_on_ebit, "cfads": cfads,
        "debt_capacity": debt_capacity,
        "equity_invested": equity_invested,
        "outstanding": outstanding,
        "annual_principal": annual_principal, "annual_interest": annual_interest,
        "annual_ds": annual_ds, "dscr": dscr, "llcr": llcr,
        "reserve_contribution": reserve_contribution,
        "reserve_balance": reserve_balance,
        "equity_distribution": equity_distribution,
        "project_cf": project_cf, "equity_cf_list": equity_cf_list,
        "project_irr": project_irr, "equity_irr": equity_irr,
        "project_npv": project_npv, "equity_npv": equity_npv,
        "payback": payback, "equity_cumul": equity_cumul,
        "target_dscr": st.session_state["pf_target_dscr"],
        "repayment_start": repayment_start if amort_type != "Bullet" else 0,
        "repayment_years": repayment_years if amort_type != "Bullet" else debt_tenor,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    T("tab_project"), T("tab_construction"), T("tab_operations"),
    T("tab_debt"), T("tab_waterfall"), T("tab_results"),
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

    # Quick summary
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
        # Map back to internal key
        mapping = dict(zip(dist_options_en, dist_options_pt))
        if lang == "EN":
            st.session_state["pf_capex_dist"] = mapping.get(dist_val, dist_val)
        else:
            st.session_state["pf_capex_dist"] = dist_val

        st.divider()
        st.number_input(T("constr_idc_rate"), min_value=0.0, max_value=30.0,
                        step=0.5, format="%.2f", key="pf_idc_rate")

    m = build_model()
    with c2:
        # Show schedule
        constr_q = m["constr_q"]
        schedule_data = {
            T("constr_quarter"): [f"Q{i+1}" for i in range(constr_q)],
            T("constr_amount"): [f"{v:.2f}" for v in m["capex_schedule"]],
            T("constr_pct"): [f"{v/st.session_state['pf_total_capex']*100:.1f}%" for v in m["capex_schedule"]],
        }
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

        # Custom inputs
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

        # CapEx disbursement chart
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

    # IDC summary
    st.divider()
    ic1, ic2, ic3 = st.columns(3)
    ic1.markdown(mc(T("constr_idc_total"), f"R$ {m['idc_total']:.2f} MM"), unsafe_allow_html=True)
    ic2.markdown(mc(T("constr_total_invested"), f"R$ {m['total_invested']:.2f} MM"), unsafe_allow_html=True)
    ic3.markdown(mc("IDC / CapEx", f"{m['idc_total']/max(st.session_state['pf_total_capex'],0.01)*100:.1f}%"), unsafe_allow_html=True)

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

    # Projection table
    df_ops = pd.DataFrame({
        T("year"): m["years"],
        T("revenue"): [f"{v:.2f}" for v in m["revenue"]],
        T("opex"): [f"{v:.2f}" for v in m["opex"]],
        "EBITDA": [f"{v:.2f}" for v in m["ebitda"]],
        "EBITDA %": [f"{v/max(r,0.01)*100:.1f}%" for v, r in zip(m["ebitda"], m["revenue"])],
        T("cfads"): [f"{v:.2f}" for v in m["cfads"]],
    })
    st.dataframe(df_ops, use_container_width=True, hide_index=True, height=min(400, 35 * len(m["years"]) + 40))

    # Chart
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
        st.selectbox(T("debt_amort_type"), ["SAC", "Price", "Bullet"], key="pf_amort_type")

    m = build_model()
    st.divider()

    # Key metrics
    dc1, dc2, dc3, dc4 = st.columns(4)
    dc1.markdown(mc(T("debt_max_capacity"), f"R$ {m['debt_capacity']:.2f} MM", "metric-card-green" if m['debt_capacity'] > 0 else ""), unsafe_allow_html=True)
    leverage = m['debt_capacity'] / max(m['total_invested'], 0.01) * 100
    dc2.markdown(mc(T("debt_leverage"), f"{leverage:.1f}%",
                    "metric-card-green" if leverage <= 80 else "metric-card-amber"), unsafe_allow_html=True)
    dc3.markdown(mc(T("debt_equity_needed"), f"R$ {m['equity_invested']:.2f} MM"), unsafe_allow_html=True)
    dc4.markdown(mc("Debt / Equity", f"{m['debt_capacity']/max(m['equity_invested'],0.01):.2f}x"), unsafe_allow_html=True)

    # Debt schedule table
    st.subheader(T("debt_schedule"))
    ops_y = m["ops_years"]
    df_debt = pd.DataFrame({
        T("year"): m["years"],
        "Outstanding": [f"{m['outstanding'][i]:.2f}" for i in range(ops_y)],
        "Principal": [f"{m['annual_principal'][i]:.2f}" for i in range(ops_y)],
        ("Juros" if lang == "PT" else "Interest"): [f"{m['annual_interest'][i]:.2f}" for i in range(ops_y)],
        T("debt_service"): [f"{m['annual_ds'][i]:.2f}" for i in range(ops_y)],
        T("cfads"): [f"{m['cfads'][i]:.2f}" for i in range(ops_y)],
        T("dscr"): [f"{m['dscr'][i]:.2f}x" if m['annual_ds'][i] > 0 else "n/a" for i in range(ops_y)],
    })
    st.dataframe(df_debt, use_container_width=True, hide_index=True,
                 height=min(400, 35 * ops_y + 40))

    # Debt service chart
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Bar(x=m["years"], y=m["annual_principal"],
                              name="Principal", marker_color="#1a56db"))
    fig_debt.add_trace(go.Bar(x=m["years"], y=m["annual_interest"],
                              name=("Juros" if lang == "PT" else "Interest"),
                              marker_color="#93c5fd"))
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

# =====================  TAB 5: WATERFALL  ===================================
with tabs[4]:
    st.subheader(T("wf_title"))
    st.number_input(T("wf_reserve_months"), min_value=0, max_value=24,
                    step=1, key="pf_reserve_months")

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
    fig_wf.add_trace(go.Bar(x=m["years"], y=-m["reserve_contribution"],
                            name=T("wf_reserve"), marker_color="#a78bfa"))
    fig_wf.add_trace(go.Bar(x=m["years"], y=m["equity_distribution"],
                            name=T("wf_equity_dist"), marker_color="#16a34a"))
    fig_wf.update_layout(
        barmode="relative", height=420,
        title=T("wf_chart_title"),
        xaxis_title=T("year"), yaxis_title="R$ MM",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # Waterfall detail table
    with st.expander(T("res_summary_table"), expanded=False):
        df_wf = pd.DataFrame({
            T("year"): m["years"],
            T("wf_revenue"): [f"{v:.2f}" for v in m["revenue"]],
            T("wf_opex"): [f"({v:.2f})" for v in m["opex"]],
            T("wf_taxes"): [f"({v:.2f})" for v in m["taxes_on_ebit"]],
            T("wf_senior_debt"): [f"({v:.2f})" for v in m["annual_ds"]],
            T("wf_reserve"): [f"({v:.2f})" for v in m["reserve_contribution"]],
            T("wf_equity_dist"): [f"{v:.2f}" for v in m["equity_distribution"]],
        })
        st.dataframe(df_wf, use_container_width=True, hide_index=True)

    # Waterfall bars for a single selected year
    st.divider()
    sel_year = st.select_slider(
        T("year"), options=m["years"], value=m["years"][min(2, len(m["years"]) - 1)],
        key="pf_wf_year"
    )
    idx = sel_year - 1
    if 0 <= idx < ops_y:
        rev_v = m["revenue"][idx]
        items = [
            (T("wf_revenue"), rev_v, "#1a56db"),
            (T("wf_opex"), -m["opex"][idx], "#ef4444"),
            (T("wf_taxes"), -m["taxes_on_ebit"][idx], "#f97316"),
            (T("wf_senior_debt"), -m["annual_ds"][idx], "#6366f1"),
            (T("wf_reserve"), -m["reserve_contribution"][idx], "#a78bfa"),
            (T("wf_equity_dist"), m["equity_distribution"][idx], "#16a34a"),
        ]
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
        fig_single.update_layout(
            height=380,
            title=f"{T('wf_chart_title')} — {yr_label}",
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

    # ── Key Metrics ──
    r1, r2, r3 = st.columns(3)
    pirr_str = f"{m['project_irr']*100:.2f}%" if m['project_irr'] is not None else "n/a"
    eirr_str = f"{m['equity_irr']*100:.2f}%" if m['equity_irr'] is not None else "n/a"
    pirr_cls = "metric-card-green" if m['project_irr'] and m['project_irr'] > st.session_state['pf_discount']/100 else "metric-card-red"
    eirr_cls = "metric-card-green" if m['equity_irr'] and m['equity_irr'] > st.session_state['pf_discount']/100 else "metric-card-red"
    r1.markdown(mc(T("res_project_irr"), pirr_str, pirr_cls), unsafe_allow_html=True)
    r2.markdown(mc(T("res_equity_irr"), eirr_str, eirr_cls), unsafe_allow_html=True)
    npv_cls = "metric-card-green" if m['project_npv'] > 0 else "metric-card-red"
    r3.markdown(mc(T("res_npv"), f"R$ {m['project_npv']:.2f} MM", npv_cls), unsafe_allow_html=True)

    r4, r5, r6 = st.columns(3)
    dscr_active = m["dscr"][m["annual_ds"] > 0]
    min_dscr = dscr_active.min() if len(dscr_active) > 0 else 0
    avg_dscr = dscr_active.mean() if len(dscr_active) > 0 else 0
    dscr_cls = "metric-card-green" if min_dscr >= m["target_dscr"] else "metric-card-red"
    r4.markdown(mc(T("res_min_dscr"), f"{min_dscr:.2f}x", dscr_cls), unsafe_allow_html=True)
    r5.markdown(mc(T("res_avg_dscr"), f"{avg_dscr:.2f}x"), unsafe_allow_html=True)
    r6.markdown(mc(T("res_llcr"), f"{m['llcr']:.2f}x",
                   "metric-card-green" if m['llcr'] >= 1.2 else "metric-card-amber"), unsafe_allow_html=True)

    r7, r8, r9 = st.columns(3)
    r7.markdown(mc(T("res_debt_capacity"), f"R$ {m['debt_capacity']:.2f} MM"), unsafe_allow_html=True)
    payback_str = f"{m['payback']}" if m['payback'] is not None else "n/a"
    r8.markdown(mc(T("res_payback"), payback_str), unsafe_allow_html=True)
    r9.markdown(mc(T("res_equity_npv"), f"R$ {m['equity_npv']:.2f} MM",
                   "metric-card-green" if m['equity_npv'] > 0 else "metric-card-red"), unsafe_allow_html=True)

    # ── DSCR Warning ──
    n_below = int(np.sum((dscr_active < m["target_dscr"]) & (dscr_active > 0)))
    if n_below > 0:
        st.warning(T("res_dscr_warning").format(n=n_below))

    st.divider()

    # ── DSCR Profile Chart ──
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
    fig_dscr.add_hline(y=1.0, line_dash="dot", line_color="#ef4444",
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

    # ── Cash Flow Chart ──
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

    # ── Summary Table ──
    st.subheader(T("res_summary_table"))
    cumul_eq = list(np.cumsum(m["equity_cf_list"]))
    # Only operational years in table
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

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div style="text-align:center;padding:20px 0 10px 0;margin-top:40px;
border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.75rem">
Project Finance Model &mdash; Built with Streamlit
</div>""", unsafe_allow_html=True)
