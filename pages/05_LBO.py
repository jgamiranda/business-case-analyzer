# -*- coding: utf-8 -*-
"""
07_LBO.py — Institutional-Grade Leveraged Buyout (LBO) Model
=============================================================
Full LBO toolkit covering:
    1. Target Company
    2. Transaction (Sources & Uses)
    3. Operating Projections
    4. Debt Schedule
    5. Returns Analysis (MOIC, IRR, Value Creation Bridge)
    6. Sensitivity & Scenarios
    7. Three-Statement Integration (IS / CF / BS)

References:
- CFI LBO Modeling Course
- Wall Street Prep LBO Walkthrough
- Rosenbaum & Pearl, "Investment Banking" (Wiley)
- Pignataro, "Leveraged Buyouts" (Wiley)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="LBO Model",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# THEME / STYLING
# =============================================================================
PRIMARY = "#1a56db"
PRIMARY_DARK = "#1e40af"
PRIMARY_LIGHT = "#dbeafe"
ACCENT_GREEN = "#059669"
ACCENT_RED = "#dc2626"
ACCENT_AMBER = "#d97706"
ACCENT_PURPLE = "#7c3aed"
BG_SOFT = "#f8fafc"
BORDER = "#e2e8f0"
TEXT_DARK = "#0f172a"
TEXT_MUTED = "#64748b"

DEBT_COLORS = {
    "TLA": "#1a56db",
    "TLB": "#3b82f6",
    "Senior Notes": "#60a5fa",
    "Sub Notes": "#a78bfa",
    "Mezzanine": "#c084fc",
    "Sponsor Equity": "#059669",
    "Rollover": "#10b981",
}

CUSTOM_CSS = f"""
<style>
    .main-title {{
        font-size: 2.1rem;
        font-weight: 800;
        color: {PRIMARY};
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }}
    .subtitle {{
        font-size: 1.0rem;
        color: {TEXT_MUTED};
        margin-bottom: 1.4rem;
    }}
    .section-header {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {PRIMARY_DARK};
        border-left: 4px solid {PRIMARY};
        padding-left: 0.75rem;
        margin: 1.1rem 0 0.7rem 0;
    }}
    .sub-header {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin: 0.8rem 0 0.4rem 0;
    }}
    .metric-card {{
        background: linear-gradient(135deg, #ffffff 0%, {BG_SOFT} 100%);
        border: 1px solid {BORDER};
        border-left: 4px solid {PRIMARY};
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
    }}
    .metric-card-green {{
        border-left-color: {ACCENT_GREEN} !important;
    }}
    .metric-card-red {{
        border-left-color: {ACCENT_RED} !important;
    }}
    .metric-card-amber {{
        border-left-color: {ACCENT_AMBER} !important;
    }}
    .metric-card-purple {{
        border-left-color: {ACCENT_PURPLE} !important;
    }}
    .metric-label {{
        font-size: 0.78rem;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    .metric-value {{
        font-size: 1.45rem;
        font-weight: 800;
        color: {TEXT_DARK};
        margin-top: 0.2rem;
    }}
    .metric-delta-pos {{
        font-size: 0.82rem;
        color: {ACCENT_GREEN};
        font-weight: 600;
    }}
    .metric-delta-neg {{
        font-size: 0.82rem;
        color: {ACCENT_RED};
        font-weight: 600;
    }}
    .info-box {{
        background: {PRIMARY_LIGHT};
        border-left: 4px solid {PRIMARY};
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.7rem 0;
        font-size: 0.9rem;
        color: {TEXT_DARK};
    }}
    .warning-box {{
        background: #fef3c7;
        border-left: 4px solid {ACCENT_AMBER};
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.7rem 0;
        font-size: 0.9rem;
    }}
    .success-box {{
        background: #d1fae5;
        border-left: 4px solid {ACCENT_GREEN};
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.7rem 0;
        font-size: 0.9rem;
    }}
    .error-box {{
        background: #fee2e2;
        border-left: 4px solid {ACCENT_RED};
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 0.7rem 0;
        font-size: 0.9rem;
    }}
    .formula-box {{
        background: #f1f5f9;
        border: 1px dashed #94a3b8;
        border-radius: 6px;
        padding: 0.6rem 0.9rem;
        font-family: 'Courier New', monospace;
        font-size: 0.88rem;
        color: {TEXT_DARK};
        margin: 0.5rem 0;
    }}
    div[data-testid="stMetricValue"] {{
        color: {PRIMARY_DARK};
        font-weight: 700;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {BG_SOFT};
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {PRIMARY} !important;
        color: white !important;
    }}
    .dataframe tbody tr:nth-child(odd) {{
        background-color: {BG_SOFT};
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# BILINGUAL DICTIONARY
# =============================================================================
_L = {
    "en": {
        "title": "Leveraged Buyout (LBO) Model",
        "subtitle": "Institutional-grade LBO — Sources & Uses, Debt Schedule, Returns & Three-Statement",
        "language": "Language",
        # Tabs
        "tab_target": "1. Target",
        "tab_tx": "2. Transaction",
        "tab_ops": "3. Operating Projections",
        "tab_debt": "4. Debt Schedule",
        "tab_returns": "5. Returns",
        "tab_sens": "6. Sensitivity & Scenarios",
        "tab_3s": "7. Three-Statement",
        # Target
        "target_inputs": "Target Company Inputs",
        "company_name": "Company Name",
        "sector": "Sector",
        "revenue": "Current Revenue ($M)",
        "ebitda_margin": "EBITDA Margin (%)",
        "ebitda": "EBITDA ($M)",
        "net_income": "Net Income ($M)",
        "total_debt": "Total Debt ($M)",
        "cash": "Cash & Equivalents ($M)",
        "shares_out": "Shares Outstanding (M)",
        "share_price": "Current Share Price ($)",
        "proj_years": "Projection Years",
        "target_metrics": "Target Key Metrics",
        "implied_ev_ebitda": "Implied EV/EBITDA",
        "net_debt": "Net Debt",
        "equity_value": "Equity Value",
        "market_cap": "Market Cap",
        "target_edu": "LBO Target Screening",
        # Transaction
        "tx_inputs": "Transaction Assumptions",
        "entry_multiple": "Entry EV/EBITDA Multiple (x)",
        "tx_fees_pct": "Transaction Fees (% EV)",
        "fin_fees_pct": "Financing Fees (% New Debt)",
        "refi_debt": "Refinance Existing Debt",
        "min_cash": "Minimum Cash Requirement ($M)",
        "sources": "Sources of Funds",
        "uses": "Uses of Funds",
        "tla": "Term Loan A",
        "tlb": "Term Loan B",
        "sr_notes": "Senior Notes",
        "sub_notes": "Subordinated Notes / HY",
        "mezz": "Mezzanine / PIK",
        "sponsor_eq": "Sponsor Equity (plug)",
        "rollover_eq": "Management Rollover Equity ($M)",
        "pct_ev": "% of EV",
        "rate": "Rate (%)",
        "tenor": "Tenor (years)",
        "cash_rate": "Cash Rate (%)",
        "pik_rate": "PIK Rate (%)",
        "purchase_eq": "Purchase of Equity",
        "refi_exist": "Refinance Existing Debt",
        "tx_fees": "Transaction Fees",
        "fin_fees": "Financing Fees",
        "min_cash_use": "Minimum Cash",
        "total_sources": "Total Sources",
        "total_uses": "Total Uses",
        "balance_chk": "Balance Check",
        "balanced": "Balanced",
        "imbalanced": "Imbalanced",
        "total_leverage": "Total Leverage",
        "senior_leverage": "Senior Leverage",
        "sources_mix": "Sources Mix",
        "uses_breakdown": "Uses Breakdown",
        # Operating
        "ops_inputs": "Operating Assumptions",
        "rev_growth": "Revenue Growth (%)",
        "ebitda_mgn": "EBITDA Margin (%)",
        "da_pct": "D&A (% Revenue)",
        "capex_pct": "CapEx (% Revenue)",
        "wc_pct": "ΔWC (% ΔRevenue)",
        "tax_rate": "Tax Rate (%)",
        "int_income_rate": "Interest on Cash (%)",
        "ops_proj": "Operating Projections",
        "year": "Year",
        "ebit": "EBIT",
        "int_exp": "Interest Expense",
        "ebt": "EBT",
        "tax": "Tax",
        "ni": "Net Income",
        "fcf": "Free Cash Flow",
        "rev_ebitda_chart": "Revenue & EBITDA Projection",
        # Debt
        "debt_config": "Debt Schedule Configuration",
        "cash_sweep": "Cash Sweep (% FCF after mandatory)",
        "opt_prepay": "Optional Prepayments (% excess, per tranche)",
        "debt_table": "Consolidated Debt Schedule",
        "debt_chart": "Debt Balance Evolution",
        "leverage_chart": "Leverage Profile",
        "dscr": "DSCR",
        "int_cov": "Interest Coverage",
        "open_bal": "Opening Balance",
        "mand_amort": "Mandatory Amort",
        "sweep": "Cash Sweep",
        "close_bal": "Closing Balance",
        "pik_accrual": "PIK Accrual",
        # Returns
        "returns_inputs": "Returns Inputs",
        "exit_year": "Exit Year",
        "exit_multiple": "Exit EV/EBITDA Multiple (x)",
        "returns_metrics": "Returns Summary",
        "moic": "MOIC",
        "irr": "IRR",
        "sponsor_proceeds": "Sponsor Proceeds",
        "value_created": "Value Created",
        "exit_ev": "Exit EV",
        "exit_net_debt": "Exit Net Debt",
        "exit_equity": "Exit Equity Value",
        "sponsor_eq_inv": "Sponsor Equity Invested",
        "value_bridge": "Value Creation Bridge",
        "ebitda_growth": "EBITDA Growth",
        "mult_expansion": "Multiple Expansion",
        "debt_paydown": "Debt Paydown",
        "sens_table": "Sensitivity: Exit Multiple × Hold Period",
        "hold_period": "Hold Period (yrs)",
        # Sensitivity
        "sens_2d": "2D Sensitivities",
        "sens_entry_exit": "Entry × Exit Multiple → IRR",
        "sens_cagr_exit": "Revenue CAGR × Exit Multiple → IRR",
        "sens_lev_exit": "Leverage × Exit Multiple → IRR",
        "tornado": "Tornado Chart — IRR Drivers",
        "scenarios": "Scenarios (Bear / Base / Bull)",
        "bear": "Bear",
        "base": "Base",
        "bull": "Bull",
        "probability": "Probability (%)",
        "expected_irr": "Probability-Weighted IRR",
        "expected_moic": "Probability-Weighted MOIC",
        # Three-Statement
        "three_stmt": "Three-Statement Integration",
        "income_stmt": "Income Statement",
        "cf_stmt": "Cash Flow Statement",
        "bs_stmt": "Balance Sheet",
        "ppa_writeup": "PPA Write-Up (% of Purchase Premium)",
        "goodwill": "Goodwill",
        "bs_check": "Balance Sheet Check",
        "bs_pass": "Balance Sheet Balanced",
        "bs_fail": "Balance Sheet Imbalanced",
        "assets": "Total Assets",
        "liab_eq": "Total Liab. + Equity",
        "diff": "Difference",
    },
    "pt": {
        "title": "Modelo de Aquisição Alavancada (LBO)",
        "subtitle": "LBO institucional — Fontes & Usos, Dívida, Retornos e 3 Demonstrações",
        "language": "Idioma",
        # Tabs
        "tab_target": "1. Alvo",
        "tab_tx": "2. Transação",
        "tab_ops": "3. Projeções Operacionais",
        "tab_debt": "4. Cronograma de Dívida",
        "tab_returns": "5. Retornos",
        "tab_sens": "6. Sensibilidade & Cenários",
        "tab_3s": "7. Três Demonstrações",
        # Target
        "target_inputs": "Dados da Empresa Alvo",
        "company_name": "Nome da Empresa",
        "sector": "Setor",
        "revenue": "Receita Atual (R$ M)",
        "ebitda_margin": "Margem EBITDA (%)",
        "ebitda": "EBITDA (R$ M)",
        "net_income": "Lucro Líquido (R$ M)",
        "total_debt": "Dívida Total (R$ M)",
        "cash": "Caixa e Equivalentes (R$ M)",
        "shares_out": "Ações em Circulação (M)",
        "share_price": "Preço Atual da Ação (R$)",
        "proj_years": "Anos de Projeção",
        "target_metrics": "Métricas-Chave do Alvo",
        "implied_ev_ebitda": "EV/EBITDA Implícito",
        "net_debt": "Dívida Líquida",
        "equity_value": "Valor do Equity",
        "market_cap": "Market Cap",
        "target_edu": "Critérios de Seleção de Alvo LBO",
        # Transaction
        "tx_inputs": "Premissas da Transação",
        "entry_multiple": "Múltiplo EV/EBITDA de Entrada (x)",
        "tx_fees_pct": "Taxas de Transação (% EV)",
        "fin_fees_pct": "Taxas de Financiamento (% Nova Dívida)",
        "refi_debt": "Refinanciar Dívida Existente",
        "min_cash": "Caixa Mínimo Exigido (R$ M)",
        "sources": "Fontes de Recursos",
        "uses": "Usos de Recursos",
        "tla": "Term Loan A",
        "tlb": "Term Loan B",
        "sr_notes": "Notes Seniores",
        "sub_notes": "Notes Subordinadas / HY",
        "mezz": "Mezanino / PIK",
        "sponsor_eq": "Equity do Sponsor (plug)",
        "rollover_eq": "Rollover do Management (R$ M)",
        "pct_ev": "% do EV",
        "rate": "Taxa (%)",
        "tenor": "Prazo (anos)",
        "cash_rate": "Taxa Cash (%)",
        "pik_rate": "Taxa PIK (%)",
        "purchase_eq": "Compra do Equity",
        "refi_exist": "Refinanciamento Dívida",
        "tx_fees": "Taxas de Transação",
        "fin_fees": "Taxas de Financiamento",
        "min_cash_use": "Caixa Mínimo",
        "total_sources": "Total Fontes",
        "total_uses": "Total Usos",
        "balance_chk": "Verificação de Balanço",
        "balanced": "Equilibrado",
        "imbalanced": "Desequilibrado",
        "total_leverage": "Alavancagem Total",
        "senior_leverage": "Alavancagem Senior",
        "sources_mix": "Mix de Fontes",
        "uses_breakdown": "Abertura dos Usos",
        # Operating
        "ops_inputs": "Premissas Operacionais",
        "rev_growth": "Crescimento Receita (%)",
        "ebitda_mgn": "Margem EBITDA (%)",
        "da_pct": "D&A (% Receita)",
        "capex_pct": "CapEx (% Receita)",
        "wc_pct": "ΔCG (% ΔReceita)",
        "tax_rate": "Alíquota IR (%)",
        "int_income_rate": "Juros sobre Caixa (%)",
        "ops_proj": "Projeções Operacionais",
        "year": "Ano",
        "ebit": "EBIT",
        "int_exp": "Despesa Financeira",
        "ebt": "LAIR",
        "tax": "Imposto",
        "ni": "Lucro Líquido",
        "fcf": "Fluxo de Caixa Livre",
        "rev_ebitda_chart": "Projeção de Receita & EBITDA",
        # Debt
        "debt_config": "Configuração do Cronograma",
        "cash_sweep": "Cash Sweep (% FCF após mandatório)",
        "opt_prepay": "Pré-pagamentos Opcionais (% por tranche)",
        "debt_table": "Cronograma Consolidado",
        "debt_chart": "Evolução dos Saldos de Dívida",
        "leverage_chart": "Perfil de Alavancagem",
        "dscr": "DSCR",
        "int_cov": "Cobertura de Juros",
        "open_bal": "Saldo Inicial",
        "mand_amort": "Amort. Mandatória",
        "sweep": "Cash Sweep",
        "close_bal": "Saldo Final",
        "pik_accrual": "Acréscimo PIK",
        # Returns
        "returns_inputs": "Parâmetros de Saída",
        "exit_year": "Ano de Saída",
        "exit_multiple": "Múltiplo EV/EBITDA de Saída (x)",
        "returns_metrics": "Resumo de Retornos",
        "moic": "MOIC",
        "irr": "TIR",
        "sponsor_proceeds": "Recebíveis do Sponsor",
        "value_created": "Valor Criado",
        "exit_ev": "EV de Saída",
        "exit_net_debt": "Dívida Líquida na Saída",
        "exit_equity": "Equity de Saída",
        "sponsor_eq_inv": "Equity do Sponsor Investido",
        "value_bridge": "Ponte de Criação de Valor",
        "ebitda_growth": "Crescimento EBITDA",
        "mult_expansion": "Expansão de Múltiplo",
        "debt_paydown": "Amortização de Dívida",
        "sens_table": "Sensibilidade: Múltiplo × Período",
        "hold_period": "Período (anos)",
        # Sensitivity
        "sens_2d": "Sensibilidades 2D",
        "sens_entry_exit": "Múltiplo Entrada × Saída → TIR",
        "sens_cagr_exit": "CAGR Receita × Múltiplo Saída → TIR",
        "sens_lev_exit": "Alavancagem × Múltiplo Saída → TIR",
        "tornado": "Tornado — Drivers da TIR",
        "scenarios": "Cenários (Bear / Base / Bull)",
        "bear": "Bear",
        "base": "Base",
        "bull": "Bull",
        "probability": "Probabilidade (%)",
        "expected_irr": "TIR Ponderada",
        "expected_moic": "MOIC Ponderado",
        # Three-Statement
        "three_stmt": "Integração das 3 Demonstrações",
        "income_stmt": "DRE",
        "cf_stmt": "Fluxo de Caixa",
        "bs_stmt": "Balanço Patrimonial",
        "ppa_writeup": "PPA Write-Up (% do Premium)",
        "goodwill": "Ágio (Goodwill)",
        "bs_check": "Verificação do Balanço",
        "bs_pass": "Balanço Equilibrado",
        "bs_fail": "Balanço Desequilibrado",
        "assets": "Ativos Totais",
        "liab_eq": "Passivo + PL",
        "diff": "Diferença",
    },
}

# =============================================================================
# LANGUAGE HELPERS
# =============================================================================
if "lbo_lang" not in st.session_state:
    st.session_state["lbo_lang"] = "en"


def T(key: str) -> str:
    lang = st.session_state.get("lbo_lang", "en")
    return _L.get(lang, _L["en"]).get(key, key)


# =============================================================================
# UTILITIES
# =============================================================================
def fmt_money(x: float, ccy: str = "$", decimals: int = 1) -> str:
    """Macabacus convention: parentheses for negatives."""
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return f"{ccy}0.0"
        if x < 0:
            return f"({ccy}{abs(x):,.{decimals}f}M)"
        return f"{ccy}{x:,.{decimals}f}M"
    except Exception:
        return f"{ccy}0.0M"


def fmt_mult(x: float, decimals: int = 2) -> str:
    try:
        if x < 0:
            return f"({abs(x):,.{decimals}f}x)"
        return f"{x:,.{decimals}f}x"
    except Exception:
        return "0.00x"


def fmt_pct(x: float, decimals: int = 1) -> str:
    try:
        v = x * 100
        if v < 0:
            return f"({abs(v):,.{decimals}f}%)"
        return f"{v:,.{decimals}f}%"
    except Exception:
        return "0.0%"


def fmt_num(x: float, decimals: int = 2) -> str:
    try:
        if x < 0:
            return f"({abs(x):,.{decimals}f})"
        return f"{x:,.{decimals}f}"
    except Exception:
        return "0.00"


def metric_card(label: str, value: str, delta: str = "", delta_pos: bool = True, color: str = ""):
    delta_class = "metric-delta-pos" if delta_pos else "metric-delta-neg"
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    card_class = "metric-card"
    if color == "green":
        card_class += " metric-card-green"
    elif color == "red":
        card_class += " metric-card-red"
    elif color == "amber":
        card_class += " metric-card-amber"
    elif color == "purple":
        card_class += " metric-card-purple"
    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def sub_header(text: str):
    st.markdown(f'<div class="sub-header">{text}</div>', unsafe_allow_html=True)


def info_box(text: str):
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def warning_box(text: str):
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)


def success_box(text: str):
    st.markdown(f'<div class="success-box">{text}</div>', unsafe_allow_html=True)


def error_box(text: str):
    st.markdown(f'<div class="error-box">{text}</div>', unsafe_allow_html=True)


def formula_box(text: str):
    st.markdown(f'<div class="formula-box">{text}</div>', unsafe_allow_html=True)


# =============================================================================
# FINANCIAL HELPERS
# =============================================================================
def compute_irr(cashflows, guess: float = 0.15, max_iter: int = 200, tol: float = 1e-7):
    """
    Compute IRR via Newton's method with bisection fallback.
    cashflows: list where index 0 is t=0 (negative outflow) and subsequent are inflows.
    """
    cf = np.array(cashflows, dtype=float)
    if len(cf) < 2:
        return float("nan")
    if np.all(cf >= 0) or np.all(cf <= 0):
        return float("nan")

    def npv(rate):
        t = np.arange(len(cf))
        return np.sum(cf / (1 + rate) ** t)

    def dnpv(rate):
        t = np.arange(len(cf))
        return np.sum(-t * cf / (1 + rate) ** (t + 1))

    rate = guess
    for _ in range(max_iter):
        f = npv(rate)
        if abs(f) < tol:
            return rate
        fp = dnpv(rate)
        if fp == 0:
            break
        new_rate = rate - f / fp
        if new_rate <= -0.999:
            new_rate = (rate - 0.999) / 2
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate

    # Bisection fallback
    lo, hi = -0.99, 10.0
    f_lo = npv(lo)
    f_hi = npv(hi)
    if f_lo * f_hi > 0:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return (lo + hi) / 2


def moic(total_inflows, equity_invested):
    if equity_invested <= 0:
        return float("nan")
    return total_inflows / equity_invested


# =============================================================================
# SESSION STATE DEFAULTS
# =============================================================================
def _init_state():
    defaults = {
        # Target
        "lbo_company_name": "Acme Industries",
        "lbo_sector": "Industrials",
        "lbo_revenue": 800.0,
        "lbo_ebitda_margin": 20.0,
        "lbo_net_income": 60.0,
        "lbo_total_debt": 150.0,
        "lbo_cash": 50.0,
        "lbo_shares_out": 50.0,
        "lbo_share_price": 20.0,
        "lbo_proj_years": 5,
        # Transaction
        "lbo_entry_mult": 10.0,
        "lbo_tx_fees_pct": 2.0,
        "lbo_fin_fees_pct": 2.5,
        "lbo_refi_debt": True,
        "lbo_min_cash": 25.0,
        "lbo_tla_pct": 15.0,
        "lbo_tla_rate": 7.0,
        "lbo_tla_tenor": 6,
        "lbo_tlb_pct": 25.0,
        "lbo_tlb_rate": 8.5,
        "lbo_tlb_tenor": 7,
        "lbo_srn_pct": 10.0,
        "lbo_srn_rate": 9.0,
        "lbo_srn_tenor": 8,
        "lbo_subn_pct": 5.0,
        "lbo_subn_rate": 11.0,
        "lbo_subn_tenor": 8,
        "lbo_mezz_pct": 0.0,
        "lbo_mezz_cash_rate": 6.0,
        "lbo_mezz_pik_rate": 6.0,
        "lbo_mezz_tenor": 10,
        "lbo_rollover": 0.0,
        # Operating (base rates)
        "lbo_rev_growth": 6.0,
        "lbo_ebitda_mgn_proj": 21.0,
        "lbo_da_pct": 4.0,
        "lbo_capex_pct": 4.0,
        "lbo_wc_pct": 15.0,
        "lbo_tax_rate": 25.0,
        "lbo_int_income_rate": 2.0,
        # Debt
        "lbo_cash_sweep": 75.0,
        # Returns
        "lbo_exit_year": 5,
        "lbo_exit_mult": 10.0,
        # Three-Stmt
        "lbo_ppa_writeup": 20.0,
        # Scenarios
        "lbo_bear_prob": 25.0,
        "lbo_base_prob": 50.0,
        "lbo_bull_prob": 25.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()

# =============================================================================
# HEADER
# =============================================================================
col_title, col_lang, col_dark = st.columns([6, 1, 1])
with col_title:
    st.markdown(f'<div class="main-title">{T("title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{T("subtitle")}</div>', unsafe_allow_html=True)
with col_lang:
    st.write("")
    _lbo_lang_ui = "EN" if st.session_state.get("lbo_lang", "en") == "en" else "PT"
    _lbo_lang_sel = st.segmented_control(
        "lbo_lang_seg", ["PT", "EN"], default=_lbo_lang_ui,
        key="lbo_lang_seg", label_visibility="collapsed")
    _new_lang = ("en" if (_lbo_lang_sel or "EN") == "EN" else "pt")
    if _new_lang != st.session_state.get("lbo_lang", "en"):
        st.session_state["lbo_lang"] = _new_lang
        st.rerun()
with col_dark:
    st.write("")
    dark_mode = st.toggle("\U0001f319", key="lbo_dark_mode", help="Dark Mode")

if dark_mode:
    st.markdown("""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#0f172a !important}
p,h1,h2,h3,h4,label,li,span,div{color:#e2e8f0 !important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#e2e8f0 !important}
[data-testid="stCaption"] p,.stCaption p{color:#94a3b8 !important}
[data-testid="stExpander"] details{background:#1e293b !important;border-color:#334155 !important}
.stTabs [data-baseweb="tab"]{background:#1e293b !important;color:#93c5fd !important;border-color:#334155 !important}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:#fff !important}
[data-testid="stAlert"]{background:#1e293b !important;border-color:#334155 !important}
[data-testid="stMetricValue"],[data-testid="stMetricLabel"]{color:#e2e8f0 !important}
[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,[data-baseweb="select"] div{background:#1e293b !important;color:#e2e8f0 !important}
hr{border-color:#334155 !important}
.main-title,.subtitle{color:#e2e8f0 !important}
</style>""", unsafe_allow_html=True)


# =============================================================================
# CORE CALCULATION ENGINE
# =============================================================================
def build_transaction(inputs: dict) -> dict:
    """Build Sources & Uses."""
    ebitda = inputs["ebitda"]
    entry_mult = inputs["entry_mult"]
    ev = ebitda * entry_mult

    existing_debt = inputs["total_debt"]
    cash_on_bs = inputs["cash"]
    refi = inputs["refi_debt"]

    # Equity purchase price = EV - existing debt + cash (standard LBO)
    eq_purchase = ev - existing_debt + cash_on_bs

    tx_fees = ev * inputs["tx_fees_pct"] / 100.0

    # New debt raised (gross)
    tla = ev * inputs["tla_pct"] / 100.0
    tlb = ev * inputs["tlb_pct"] / 100.0
    srn = ev * inputs["srn_pct"] / 100.0
    subn = ev * inputs["subn_pct"] / 100.0
    mezz = ev * inputs["mezz_pct"] / 100.0
    new_debt_total = tla + tlb + srn + subn + mezz

    fin_fees = new_debt_total * inputs["fin_fees_pct"] / 100.0
    min_cash = inputs["min_cash"]
    refi_amt = existing_debt if refi else 0.0

    total_uses = eq_purchase + refi_amt + tx_fees + fin_fees + min_cash

    rollover = inputs["rollover"]

    # Sponsor equity = plug
    sponsor_eq = total_uses - (new_debt_total + rollover)
    sponsor_eq = max(sponsor_eq, 0.0)

    total_sources = new_debt_total + sponsor_eq + rollover

    total_debt_new = new_debt_total
    senior_debt = tla + tlb + srn
    total_lev = total_debt_new / ebitda if ebitda > 0 else 0.0
    senior_lev = senior_debt / ebitda if ebitda > 0 else 0.0

    return {
        "ev": ev,
        "eq_purchase": eq_purchase,
        "tx_fees": tx_fees,
        "fin_fees": fin_fees,
        "refi_amt": refi_amt,
        "min_cash": min_cash,
        "tla": tla,
        "tlb": tlb,
        "srn": srn,
        "subn": subn,
        "mezz": mezz,
        "new_debt_total": new_debt_total,
        "sponsor_eq": sponsor_eq,
        "rollover": rollover,
        "total_sources": total_sources,
        "total_uses": total_uses,
        "total_lev": total_lev,
        "senior_lev": senior_lev,
        "balance_diff": total_sources - total_uses,
    }


def project_operations(target: dict, tx: dict, ops: dict, years: int) -> pd.DataFrame:
    """Build operating projection table (excluding interest — that comes from debt schedule)."""
    rows = []
    prior_rev = target["revenue"]
    for y in range(1, years + 1):
        growth = ops["rev_growth"][y - 1] / 100.0
        margin = ops["ebitda_mgn"][y - 1] / 100.0
        da_pct = ops["da_pct"][y - 1] / 100.0
        capex_pct = ops["capex_pct"][y - 1] / 100.0
        wc_pct = ops["wc_pct"][y - 1] / 100.0

        rev = prior_rev * (1 + growth)
        ebitda = rev * margin
        da = rev * da_pct
        ebit = ebitda - da
        capex = rev * capex_pct
        delta_rev = rev - prior_rev
        delta_wc = delta_rev * wc_pct

        rows.append({
            "Year": y,
            "Revenue": rev,
            "Growth": growth,
            "EBITDA": ebitda,
            "Margin": margin,
            "D&A": da,
            "EBIT": ebit,
            "CapEx": capex,
            "ΔWC": delta_wc,
            "PriorRev": prior_rev,
        })
        prior_rev = rev
    return pd.DataFrame(rows)


def build_debt_schedule(tx: dict, ops_df: pd.DataFrame, tranche_inputs: dict,
                        ops: dict, target: dict, years: int, cash_sweep_pct: float) -> dict:
    """
    Iterative integrated debt schedule.
    Returns: debt_df (full schedule), interest_series, net_debt_series, cash_series
    """
    # Tranche opening balances
    balances = {
        "TLA": tx["tla"],
        "TLB": tx["tlb"],
        "Senior Notes": tx["srn"],
        "Sub Notes": tx["subn"],
        "Mezzanine": tx["mezz"],
    }

    # Rates
    rates = {
        "TLA": tranche_inputs["tla_rate"] / 100.0,
        "TLB": tranche_inputs["tlb_rate"] / 100.0,
        "Senior Notes": tranche_inputs["srn_rate"] / 100.0,
        "Sub Notes": tranche_inputs["subn_rate"] / 100.0,
        "Mezzanine": tranche_inputs["mezz_cash_rate"] / 100.0,
    }
    pik_rate = tranche_inputs["mezz_pik_rate"] / 100.0

    # Tenors
    tenors = {
        "TLA": tranche_inputs["tla_tenor"],
        "TLB": tranche_inputs["tlb_tenor"],
        "Senior Notes": tranche_inputs["srn_tenor"],
        "Sub Notes": tranche_inputs["subn_tenor"],
        "Mezzanine": tranche_inputs["mezz_tenor"],
    }

    # Amortization schedules:
    # TLA: straight-line over tenor
    # TLB: 1% per year + bullet at maturity
    # Notes, Mezz: bullet
    tla_annual_amort = balances["TLA"] / tenors["TLA"] if tenors["TLA"] > 0 else 0
    tlb_annual_amort = balances["TLB"] * 0.01

    # Initial cash = min cash requirement
    cash = tx["min_cash"]

    records = []
    int_series = []
    cash_series = []
    net_debt_series = []
    total_debt_series = []
    senior_debt_series = []
    fcf_series = []

    for idx, row in ops_df.iterrows():
        y = int(row["Year"])
        ebitda = row["EBITDA"]
        da = row["D&A"]
        ebit = row["EBIT"]
        capex = row["CapEx"]
        delta_wc = row["ΔWC"]

        open_bal = {k: v for k, v in balances.items()}
        total_open = sum(open_bal.values())

        # Interest expense on opening balances
        interest_cash = 0.0
        for k in ["TLA", "TLB", "Senior Notes", "Sub Notes", "Mezzanine"]:
            interest_cash += open_bal[k] * rates[k]
        mezz_pik = open_bal["Mezzanine"] * pik_rate

        # Interest income on opening cash
        int_income = cash * (ops["int_income_rate"] / 100.0)

        # Net interest expense (for IS/FCF)
        net_interest = interest_cash - int_income

        # Tax on EBT (EBT = EBIT - net_interest + PIK? PIK is non-cash but deductible)
        # Convention: PIK interest is tax-deductible but non-cash
        total_interest_for_tax = interest_cash + mezz_pik - int_income
        ebt = ebit - total_interest_for_tax
        tax = max(0.0, ebt) * (ops["tax_rate"][y - 1] / 100.0)
        ni = ebt - tax

        # FCF available for debt paydown = EBITDA - cash taxes - capex - ΔWC - cash interest + int income
        fcf_available = ebitda - tax - capex - delta_wc - interest_cash + int_income

        # --- Mandatory amortization ---
        mand_amort = {
            "TLA": min(tla_annual_amort, open_bal["TLA"]) if y <= tenors["TLA"] else 0.0,
            "TLB": min(tlb_annual_amort, open_bal["TLB"]) if y < tenors["TLB"] else open_bal["TLB"] if y == tenors["TLB"] else 0.0,
            "Senior Notes": open_bal["Senior Notes"] if y == tenors["Senior Notes"] else 0.0,
            "Sub Notes": open_bal["Sub Notes"] if y == tenors["Sub Notes"] else 0.0,
            "Mezzanine": 0.0,  # Bullet — paid at maturity but won't usually be in hold
        }
        # TLA final-year bullet
        if y == tenors["TLA"]:
            mand_amort["TLA"] = open_bal["TLA"]
        if y == tenors["Mezzanine"]:
            mand_amort["Mezzanine"] = open_bal["Mezzanine"]

        total_mand = sum(mand_amort.values())

        # FCF after mandatory
        fcf_after_mand = fcf_available - total_mand

        # --- Cash sweep ---
        # Sweep from excess FCF after maintaining min cash
        excess_cash_for_sweep = max(0.0, fcf_after_mand)  # only if positive
        sweep_total = excess_cash_for_sweep * (cash_sweep_pct / 100.0)

        # Sweep priority: TLA -> TLB -> Senior Notes -> Sub Notes (most LBOs sweep senior first)
        sweep_alloc = {"TLA": 0.0, "TLB": 0.0, "Senior Notes": 0.0, "Sub Notes": 0.0, "Mezzanine": 0.0}
        remaining_sweep = sweep_total
        for tranche in ["TLA", "TLB", "Senior Notes", "Sub Notes"]:
            avail_after_mand = max(0.0, open_bal[tranche] - mand_amort[tranche])
            use = min(remaining_sweep, avail_after_mand)
            sweep_alloc[tranche] = use
            remaining_sweep -= use
            if remaining_sweep <= 0:
                break

        total_sweep = sum(sweep_alloc.values())

        # --- Update balances ---
        new_balances = {}
        for k in open_bal:
            new_bal = open_bal[k] - mand_amort[k] - sweep_alloc.get(k, 0.0)
            if k == "Mezzanine":
                new_bal += mezz_pik  # PIK accrues
            new_balances[k] = max(0.0, new_bal)

        balances = new_balances
        total_close = sum(balances.values())

        # Cash evolution
        net_cash_change = fcf_after_mand - total_sweep
        cash = cash + net_cash_change
        if cash < tx["min_cash"]:
            # Shortfall — in reality would draw revolver; here just floor at min_cash
            cash = max(cash, 0.0)

        senior_close = balances["TLA"] + balances["TLB"] + balances["Senior Notes"]
        net_debt = total_close - cash

        records.append({
            "Year": y,
            "Open TLA": open_bal["TLA"],
            "Open TLB": open_bal["TLB"],
            "Open SrN": open_bal["Senior Notes"],
            "Open SubN": open_bal["Sub Notes"],
            "Open Mezz": open_bal["Mezzanine"],
            "Open Total": total_open,
            "Mand TLA": mand_amort["TLA"],
            "Mand TLB": mand_amort["TLB"],
            "Mand SrN": mand_amort["Senior Notes"],
            "Mand SubN": mand_amort["Sub Notes"],
            "Mand Mezz": mand_amort["Mezzanine"],
            "Sweep TLA": sweep_alloc["TLA"],
            "Sweep TLB": sweep_alloc["TLB"],
            "Sweep SrN": sweep_alloc["Senior Notes"],
            "Sweep SubN": sweep_alloc["Sub Notes"],
            "PIK Mezz": mezz_pik,
            "Close TLA": balances["TLA"],
            "Close TLB": balances["TLB"],
            "Close SrN": balances["Senior Notes"],
            "Close SubN": balances["Sub Notes"],
            "Close Mezz": balances["Mezzanine"],
            "Close Total": total_close,
            "Senior Close": senior_close,
            "Cash": cash,
            "Net Debt": net_debt,
            "Interest Cash": interest_cash,
            "Interest PIK": mezz_pik,
            "Interest Income": int_income,
            "Total Interest (Tax)": total_interest_for_tax,
            "EBT": ebt,
            "Tax": tax,
            "NI": ni,
            "FCF": fcf_available,
            "FCF after Mand": fcf_after_mand,
            "Total Sweep": total_sweep,
            "EBITDA": ebitda,
            "D&A": da,
            "EBIT": ebit,
            "CapEx": capex,
            "ΔWC": delta_wc,
        })

    debt_df = pd.DataFrame(records)
    return {
        "debt_df": debt_df,
    }


def compute_returns(debt_df: pd.DataFrame, tx: dict, target: dict, exit_year: int, exit_mult: float) -> dict:
    """Compute MOIC, IRR, value bridge."""
    if exit_year < 1 or exit_year > len(debt_df):
        return {}
    exit_row = debt_df.iloc[exit_year - 1]
    exit_ebitda = exit_row["EBITDA"]
    exit_ev = exit_ebitda * exit_mult
    exit_net_debt = exit_row["Net Debt"]
    exit_equity = exit_ev - exit_net_debt

    sponsor_eq_in = tx["sponsor_eq"]
    rollover = tx["rollover"]
    total_eq_in = sponsor_eq_in + rollover

    if total_eq_in > 0:
        sponsor_share = sponsor_eq_in / total_eq_in
    else:
        sponsor_share = 1.0

    sponsor_proceeds = max(0.0, exit_equity) * sponsor_share

    moic_val = moic(sponsor_proceeds, sponsor_eq_in)

    # IRR
    cf = [-sponsor_eq_in] + [0.0] * (exit_year - 1) + [sponsor_proceeds]
    irr_val = compute_irr(cf)

    # Value Creation Bridge
    entry_ebitda = target["ebitda"]
    entry_mult = tx["ev"] / entry_ebitda if entry_ebitda > 0 else 0
    entry_debt = tx["new_debt_total"]

    # EBITDA growth contribution: (exit_ebitda - entry_ebitda) * entry_mult
    ebitda_growth_contrib = (exit_ebitda - entry_ebitda) * entry_mult
    # Multiple expansion: exit_ebitda * (exit_mult - entry_mult)
    mult_exp_contrib = exit_ebitda * (exit_mult - entry_mult)
    # Debt paydown: entry_debt - exit_debt (negatives paid down add to equity)
    exit_debt_total = exit_row["Close Total"]
    cash_build = exit_row["Cash"] - tx["min_cash"]
    debt_paydown_contrib = (entry_debt - exit_debt_total) + cash_build

    total_value_created = sponsor_proceeds - sponsor_eq_in

    return {
        "exit_ebitda": exit_ebitda,
        "exit_ev": exit_ev,
        "exit_net_debt": exit_net_debt,
        "exit_equity": exit_equity,
        "sponsor_proceeds": sponsor_proceeds,
        "sponsor_eq_in": sponsor_eq_in,
        "moic": moic_val,
        "irr": irr_val,
        "value_created": total_value_created,
        "ebitda_growth_contrib": ebitda_growth_contrib,
        "mult_exp_contrib": mult_exp_contrib,
        "debt_paydown_contrib": debt_paydown_contrib,
        "entry_mult": entry_mult,
    }


# =============================================================================
# TABS
# =============================================================================
tabs = st.tabs([
    T("tab_target"),
    T("tab_tx"),
    T("tab_ops"),
    T("tab_debt"),
    T("tab_returns"),
    T("tab_sens"),
    T("tab_3s"),
])

# =============================================================================
# TAB 1 — TARGET
# =============================================================================
with tabs[0]:
    section_header(T("target_inputs"))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state["lbo_company_name"] = st.text_input(
            T("company_name"), value=st.session_state["lbo_company_name"]
        )
        st.session_state["lbo_sector"] = st.text_input(
            T("sector"), value=st.session_state["lbo_sector"]
        )
        st.session_state["lbo_revenue"] = st.number_input(
            T("revenue"), value=float(st.session_state["lbo_revenue"]),
            min_value=0.0, step=10.0, format="%.1f"
        )
        st.session_state["lbo_ebitda_margin"] = st.number_input(
            T("ebitda_margin"), value=float(st.session_state["lbo_ebitda_margin"]),
            min_value=0.0, max_value=100.0, step=0.5, format="%.1f"
        )
    with c2:
        ebitda_calc = st.session_state["lbo_revenue"] * st.session_state["lbo_ebitda_margin"] / 100.0
        st.number_input(
            T("ebitda"), value=float(ebitda_calc),
            disabled=True, format="%.1f", key="lbo_ebitda_display"
        )
        st.session_state["lbo_net_income"] = st.number_input(
            T("net_income"), value=float(st.session_state["lbo_net_income"]),
            step=1.0, format="%.1f"
        )
        st.session_state["lbo_total_debt"] = st.number_input(
            T("total_debt"), value=float(st.session_state["lbo_total_debt"]),
            min_value=0.0, step=5.0, format="%.1f"
        )
        st.session_state["lbo_cash"] = st.number_input(
            T("cash"), value=float(st.session_state["lbo_cash"]),
            min_value=0.0, step=5.0, format="%.1f"
        )
    with c3:
        st.session_state["lbo_shares_out"] = st.number_input(
            T("shares_out"), value=float(st.session_state["lbo_shares_out"]),
            min_value=0.0, step=1.0, format="%.1f"
        )
        st.session_state["lbo_share_price"] = st.number_input(
            T("share_price"), value=float(st.session_state["lbo_share_price"]),
            min_value=0.0, step=0.5, format="%.2f"
        )
        st.session_state["lbo_proj_years"] = st.slider(
            T("proj_years"), min_value=3, max_value=7,
            value=int(st.session_state["lbo_proj_years"])
        )

    # Derived metrics
    ebitda = st.session_state["lbo_revenue"] * st.session_state["lbo_ebitda_margin"] / 100.0
    net_debt = st.session_state["lbo_total_debt"] - st.session_state["lbo_cash"]
    market_cap = st.session_state["lbo_shares_out"] * st.session_state["lbo_share_price"]
    implied_ev = market_cap + net_debt
    implied_ev_ebitda = implied_ev / ebitda if ebitda > 0 else 0.0
    eq_value = market_cap

    section_header(T("target_metrics"))
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card(T("revenue"), fmt_money(st.session_state["lbo_revenue"]))
    with m2:
        metric_card(T("ebitda"), fmt_money(ebitda), f"{st.session_state['lbo_ebitda_margin']:.1f}% margin", True)
    with m3:
        metric_card(T("net_debt"), fmt_money(net_debt), color="amber")
    with m4:
        metric_card(T("implied_ev_ebitda"), fmt_mult(implied_ev_ebitda), color="purple")

    m5, m6, m7, m8 = st.columns(4)
    with m5:
        metric_card(T("market_cap"), fmt_money(market_cap))
    with m6:
        metric_card(T("equity_value"), fmt_money(eq_value))
    with m7:
        metric_card("Enterprise Value", fmt_money(implied_ev), color="purple")
    with m8:
        metric_card(T("net_income"), fmt_money(st.session_state["lbo_net_income"]),
                    color="green" if st.session_state["lbo_net_income"] > 0 else "red")

    with st.expander(T("target_edu")):
        if st.session_state["lbo_lang"] == "en":
            st.markdown("""
**Characteristics of an ideal LBO target (Rosenbaum & Pearl):**
- **Stable, predictable cash flows** — able to service high debt loads
- **Mature industry** with defensive demand characteristics
- **Low CapEx requirements** and high FCF conversion
- **Strong market position** and barriers to entry
- **Clean balance sheet** or undermanaged assets offering upside
- **Asset base** that can serve as debt collateral
- **Opportunity for operational improvements** (margin expansion, working capital, etc.)
- **Clear exit path** (strategic sale, IPO, secondary buyout)

**Typical LBO metrics:**
- Debt/EBITDA: 5.0–7.0x
- Sponsor equity: 30–40% of EV
- Target IRR: 20%+
- Target MOIC: 2.0–3.0x over 5 years
- Hold period: 3–7 years
            """)
        else:
            st.markdown("""
**Características de um alvo LBO ideal (Rosenbaum & Pearl):**
- **Fluxos de caixa estáveis e previsíveis** — capazes de servir alta dívida
- **Indústria madura** com características defensivas
- **Baixa necessidade de CapEx** e alta conversão em FCF
- **Posição forte de mercado** e barreiras de entrada
- **Balanço limpo** ou ativos sub-gerenciados com potencial
- **Base de ativos** que pode servir de garantia
- **Oportunidades de melhoria operacional** (margem, capital de giro, etc.)
- **Rota clara de saída** (venda estratégica, IPO, secondary buyout)

**Métricas típicas de LBO:**
- Dívida/EBITDA: 5.0–7.0x
- Equity do sponsor: 30–40% do EV
- TIR alvo: 20%+
- MOIC alvo: 2.0–3.0x em 5 anos
- Período de hold: 3–7 anos
            """)


# Store target dict
target = {
    "company_name": st.session_state["lbo_company_name"],
    "sector": st.session_state["lbo_sector"],
    "revenue": st.session_state["lbo_revenue"],
    "ebitda_margin": st.session_state["lbo_ebitda_margin"] / 100.0,
    "ebitda": ebitda,
    "net_income": st.session_state["lbo_net_income"],
    "total_debt": st.session_state["lbo_total_debt"],
    "cash": st.session_state["lbo_cash"],
    "shares_out": st.session_state["lbo_shares_out"],
    "share_price": st.session_state["lbo_share_price"],
    "market_cap": market_cap,
    "implied_ev": implied_ev,
    "implied_ev_ebitda": implied_ev_ebitda,
}

# =============================================================================
# TAB 2 — TRANSACTION
# =============================================================================
with tabs[1]:
    section_header(T("tx_inputs"))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state["lbo_entry_mult"] = st.number_input(
            T("entry_multiple"), value=float(st.session_state["lbo_entry_mult"]),
            min_value=1.0, max_value=30.0, step=0.25, format="%.2f"
        )
        st.session_state["lbo_tx_fees_pct"] = st.number_input(
            T("tx_fees_pct"), value=float(st.session_state["lbo_tx_fees_pct"]),
            min_value=0.0, max_value=10.0, step=0.1, format="%.2f"
        )
    with c2:
        st.session_state["lbo_fin_fees_pct"] = st.number_input(
            T("fin_fees_pct"), value=float(st.session_state["lbo_fin_fees_pct"]),
            min_value=0.0, max_value=10.0, step=0.1, format="%.2f"
        )
        st.session_state["lbo_min_cash"] = st.number_input(
            T("min_cash"), value=float(st.session_state["lbo_min_cash"]),
            min_value=0.0, step=5.0, format="%.1f"
        )
    with c3:
        st.session_state["lbo_refi_debt"] = st.checkbox(
            T("refi_debt"), value=bool(st.session_state["lbo_refi_debt"])
        )
        st.session_state["lbo_rollover"] = st.number_input(
            T("rollover_eq"), value=float(st.session_state["lbo_rollover"]),
            min_value=0.0, step=5.0, format="%.1f"
        )

    section_header(T("sources"))

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        sub_header(T("tla"))
        st.session_state["lbo_tla_pct"] = st.number_input(
            T("pct_ev") + " TLA", value=float(st.session_state["lbo_tla_pct"]),
            min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="in_tla_pct"
        )
        st.session_state["lbo_tla_rate"] = st.number_input(
            T("rate") + " TLA", value=float(st.session_state["lbo_tla_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_tla_rate"
        )
        st.session_state["lbo_tla_tenor"] = st.number_input(
            T("tenor") + " TLA", value=int(st.session_state["lbo_tla_tenor"]),
            min_value=1, max_value=15, step=1, key="in_tla_tenor"
        )

    with sc2:
        sub_header(T("tlb"))
        st.session_state["lbo_tlb_pct"] = st.number_input(
            T("pct_ev") + " TLB", value=float(st.session_state["lbo_tlb_pct"]),
            min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="in_tlb_pct"
        )
        st.session_state["lbo_tlb_rate"] = st.number_input(
            T("rate") + " TLB", value=float(st.session_state["lbo_tlb_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_tlb_rate"
        )
        st.session_state["lbo_tlb_tenor"] = st.number_input(
            T("tenor") + " TLB", value=int(st.session_state["lbo_tlb_tenor"]),
            min_value=1, max_value=15, step=1, key="in_tlb_tenor"
        )

    with sc3:
        sub_header(T("sr_notes"))
        st.session_state["lbo_srn_pct"] = st.number_input(
            T("pct_ev") + " SrN", value=float(st.session_state["lbo_srn_pct"]),
            min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="in_srn_pct"
        )
        st.session_state["lbo_srn_rate"] = st.number_input(
            T("rate") + " SrN", value=float(st.session_state["lbo_srn_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_srn_rate"
        )
        st.session_state["lbo_srn_tenor"] = st.number_input(
            T("tenor") + " SrN", value=int(st.session_state["lbo_srn_tenor"]),
            min_value=1, max_value=15, step=1, key="in_srn_tenor"
        )

    with sc4:
        sub_header(T("sub_notes"))
        st.session_state["lbo_subn_pct"] = st.number_input(
            T("pct_ev") + " SubN", value=float(st.session_state["lbo_subn_pct"]),
            min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="in_subn_pct"
        )
        st.session_state["lbo_subn_rate"] = st.number_input(
            T("rate") + " SubN", value=float(st.session_state["lbo_subn_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_subn_rate"
        )
        st.session_state["lbo_subn_tenor"] = st.number_input(
            T("tenor") + " SubN", value=int(st.session_state["lbo_subn_tenor"]),
            min_value=1, max_value=15, step=1, key="in_subn_tenor"
        )

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        sub_header(T("mezz"))
        st.session_state["lbo_mezz_pct"] = st.number_input(
            T("pct_ev") + " Mezz", value=float(st.session_state["lbo_mezz_pct"]),
            min_value=0.0, max_value=100.0, step=1.0, format="%.1f", key="in_mezz_pct"
        )
    with mc2:
        st.session_state["lbo_mezz_cash_rate"] = st.number_input(
            T("cash_rate"), value=float(st.session_state["lbo_mezz_cash_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_mezz_cr"
        )
    with mc3:
        st.session_state["lbo_mezz_pik_rate"] = st.number_input(
            T("pik_rate"), value=float(st.session_state["lbo_mezz_pik_rate"]),
            min_value=0.0, max_value=30.0, step=0.25, format="%.2f", key="in_mezz_pr"
        )
    with mc4:
        st.session_state["lbo_mezz_tenor"] = st.number_input(
            T("tenor") + " Mezz", value=int(st.session_state["lbo_mezz_tenor"]),
            min_value=1, max_value=15, step=1, key="in_mezz_tenor"
        )

    # Build transaction
    tx_inputs = {
        "ebitda": ebitda,
        "entry_mult": st.session_state["lbo_entry_mult"],
        "total_debt": st.session_state["lbo_total_debt"],
        "cash": st.session_state["lbo_cash"],
        "tx_fees_pct": st.session_state["lbo_tx_fees_pct"],
        "fin_fees_pct": st.session_state["lbo_fin_fees_pct"],
        "refi_debt": st.session_state["lbo_refi_debt"],
        "min_cash": st.session_state["lbo_min_cash"],
        "tla_pct": st.session_state["lbo_tla_pct"],
        "tlb_pct": st.session_state["lbo_tlb_pct"],
        "srn_pct": st.session_state["lbo_srn_pct"],
        "subn_pct": st.session_state["lbo_subn_pct"],
        "mezz_pct": st.session_state["lbo_mezz_pct"],
        "rollover": st.session_state["lbo_rollover"],
    }
    tx = build_transaction(tx_inputs)

    section_header(T("sources") + " & " + T("uses"))
    col_left, col_right = st.columns(2)

    with col_left:
        sub_header(T("sources"))
        sources_data = {
            T("tla"): tx["tla"],
            T("tlb"): tx["tlb"],
            T("sr_notes"): tx["srn"],
            T("sub_notes"): tx["subn"],
            T("mezz"): tx["mezz"],
            T("sponsor_eq"): tx["sponsor_eq"],
            "Rollover": tx["rollover"],
        }
        src_df = pd.DataFrame([
            {"Item": k, "Amount ($M)": v, "% of Total": (v / tx["total_sources"] * 100) if tx["total_sources"] > 0 else 0}
            for k, v in sources_data.items() if v > 0.001
        ])
        src_df.loc[len(src_df)] = [T("total_sources"), tx["total_sources"], 100.0]
        st.dataframe(
            src_df.style.format({"Amount ($M)": "{:,.1f}", "% of Total": "{:.1f}%"}),
            hide_index=True, use_container_width=True,
        )

    with col_right:
        sub_header(T("uses"))
        uses_data = {
            T("purchase_eq"): tx["eq_purchase"],
            T("refi_exist"): tx["refi_amt"],
            T("tx_fees"): tx["tx_fees"],
            T("fin_fees"): tx["fin_fees"],
            T("min_cash_use"): tx["min_cash"],
        }
        uses_df = pd.DataFrame([
            {"Item": k, "Amount ($M)": v, "% of Total": (v / tx["total_uses"] * 100) if tx["total_uses"] > 0 else 0}
            for k, v in uses_data.items() if v > 0.001
        ])
        uses_df.loc[len(uses_df)] = [T("total_uses"), tx["total_uses"], 100.0]
        st.dataframe(
            uses_df.style.format({"Amount ($M)": "{:,.1f}", "% of Total": "{:.1f}%"}),
            hide_index=True, use_container_width=True,
        )

    # Balance check
    diff = tx["balance_diff"]
    if abs(diff) < 0.1:
        success_box(f"{T('balance_chk')}: {T('balanced')} ({fmt_money(tx['total_sources'])} = {fmt_money(tx['total_uses'])})")
    else:
        error_box(f"{T('balance_chk')}: {T('imbalanced')} (Δ = {fmt_money(diff)})")

    # Leverage metrics
    lc1, lc2, lc3, lc4 = st.columns(4)
    with lc1:
        metric_card("EV", fmt_money(tx["ev"]), color="purple")
    with lc2:
        metric_card(T("total_leverage"), fmt_mult(tx["total_lev"]), color="amber")
    with lc3:
        metric_card(T("senior_leverage"), fmt_mult(tx["senior_lev"]))
    with lc4:
        sponsor_pct = tx["sponsor_eq"] / tx["total_sources"] * 100 if tx["total_sources"] > 0 else 0
        metric_card(T("sponsor_eq"), fmt_money(tx["sponsor_eq"]), f"{sponsor_pct:.1f}% of Sources", True)

    # Charts
    ch1, ch2 = st.columns(2)
    with ch1:
        sub_header(T("sources_mix"))
        src_labels = []
        src_values = []
        src_colors = []
        color_map = {
            T("tla"): DEBT_COLORS["TLA"],
            T("tlb"): DEBT_COLORS["TLB"],
            T("sr_notes"): DEBT_COLORS["Senior Notes"],
            T("sub_notes"): DEBT_COLORS["Sub Notes"],
            T("mezz"): DEBT_COLORS["Mezzanine"],
            T("sponsor_eq"): DEBT_COLORS["Sponsor Equity"],
            "Rollover": DEBT_COLORS["Rollover"],
        }
        for k, v in sources_data.items():
            if v > 0.001:
                src_labels.append(k)
                src_values.append(v)
                src_colors.append(color_map.get(k, PRIMARY))

        fig_src = go.Figure(data=[go.Pie(
            labels=src_labels,
            values=src_values,
            hole=0.5,
            marker=dict(colors=src_colors),
            textinfo="label+percent",
            textposition="outside",
        )])
        fig_src.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(orientation="v", x=1.1, y=0.5),
        )
        st.plotly_chart(fig_src, use_container_width=True)

    with ch2:
        sub_header(T("uses_breakdown"))
        uses_labels = [k for k, v in uses_data.items() if v > 0.001]
        uses_values = [v for v in uses_data.values() if v > 0.001]
        fig_uses = go.Figure(data=[go.Bar(
            x=uses_values,
            y=uses_labels,
            orientation="h",
            marker=dict(color=PRIMARY),
            text=[fmt_money(v) for v in uses_values],
            textposition="outside",
        )])
        fig_uses.update_layout(
            height=380, margin=dict(l=10, r=50, t=10, b=10),
            xaxis_title="USD ($M)",
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig_uses, use_container_width=True)

    with st.expander("Sources & Uses Primer"):
        if st.session_state["lbo_lang"] == "en":
            st.markdown("""
**Sources & Uses:** the foundational LBO schedule that must balance.

**Uses** represent everything the deal pays for:
- Equity purchase price (what shareholders receive)
- Refinancing of existing debt (often triggered by change-of-control)
- Transaction fees (M&A advisors, legal, accounting) — typically 1-3% of EV
- Financing fees (OID, upfront arrangement fees) — typically 2-3% of new debt
- Minimum cash on the balance sheet post-close

**Sources** = how the deal is funded:
- Senior secured debt (TLA/TLB, Revolver)
- High-yield/senior unsecured notes
- Subordinated/mezzanine with PIK options
- Sponsor equity (the plug)
- Management rollover equity (alignment)

**Sponsor equity is the plug:** Sources minus all debt and rollover = equity check required.
            """)
        else:
            st.markdown("""
**Fontes & Usos:** o balanço fundacional de um LBO que deve fechar.

**Usos** representam tudo que a transação paga:
- Preço de compra do equity (o que acionistas recebem)
- Refinanciamento da dívida existente (por cláusula de change-of-control)
- Taxas de transação (M&A, jurídico, contábil) — 1-3% do EV
- Taxas de financiamento (OID, estruturação) — 2-3% da nova dívida
- Caixa mínimo no balanço pós-fechamento

**Fontes** = como a transação é financiada:
- Dívida sênior secured (TLA/TLB, revolver)
- High-yield / notes sêniores unsecured
- Subordinadas / mezanino com opções PIK
- Equity do sponsor (plug)
- Rollover equity do management (alinhamento)

**Equity do sponsor é o plug:** Usos menos dívida e rollover = cheque de equity necessário.
            """)


# =============================================================================
# TAB 3 — OPERATING PROJECTIONS
# =============================================================================
with tabs[2]:
    section_header(T("ops_inputs"))
    years = int(st.session_state["lbo_proj_years"])

    # Build per-year operating assumptions as session dicts
    # Initialize if not present or year count changed
    def _init_ops_list(key: str, default_val: float, years: int):
        if key not in st.session_state or len(st.session_state[key]) != years:
            st.session_state[key] = [default_val] * years

    _init_ops_list("lbo_ops_rev_growth", st.session_state["lbo_rev_growth"], years)
    _init_ops_list("lbo_ops_ebitda_mgn", st.session_state["lbo_ebitda_mgn_proj"], years)
    _init_ops_list("lbo_ops_da_pct", st.session_state["lbo_da_pct"], years)
    _init_ops_list("lbo_ops_capex_pct", st.session_state["lbo_capex_pct"], years)
    _init_ops_list("lbo_ops_wc_pct", st.session_state["lbo_wc_pct"], years)
    _init_ops_list("lbo_ops_tax_rate", st.session_state["lbo_tax_rate"], years)

    st.markdown(f"**{T('ops_inputs')} — per year (Year 1 → Year {years})**")

    ops_cols = st.columns(years)
    for i, col in enumerate(ops_cols):
        with col:
            st.markdown(f"**Year {i+1}**")
            st.session_state["lbo_ops_rev_growth"][i] = st.number_input(
                T("rev_growth"), value=float(st.session_state["lbo_ops_rev_growth"][i]),
                min_value=-50.0, max_value=100.0, step=0.5, format="%.1f",
                key=f"lbo_op_rg_{i}"
            )
            st.session_state["lbo_ops_ebitda_mgn"][i] = st.number_input(
                T("ebitda_mgn"), value=float(st.session_state["lbo_ops_ebitda_mgn"][i]),
                min_value=0.0, max_value=100.0, step=0.5, format="%.1f",
                key=f"lbo_op_em_{i}"
            )
            st.session_state["lbo_ops_da_pct"][i] = st.number_input(
                T("da_pct"), value=float(st.session_state["lbo_ops_da_pct"][i]),
                min_value=0.0, max_value=50.0, step=0.25, format="%.2f",
                key=f"lbo_op_da_{i}"
            )
            st.session_state["lbo_ops_capex_pct"][i] = st.number_input(
                T("capex_pct"), value=float(st.session_state["lbo_ops_capex_pct"][i]),
                min_value=0.0, max_value=50.0, step=0.25, format="%.2f",
                key=f"lbo_op_cx_{i}"
            )
            st.session_state["lbo_ops_wc_pct"][i] = st.number_input(
                T("wc_pct"), value=float(st.session_state["lbo_ops_wc_pct"][i]),
                min_value=-100.0, max_value=100.0, step=1.0, format="%.1f",
                key=f"lbo_op_wc_{i}"
            )
            st.session_state["lbo_ops_tax_rate"][i] = st.number_input(
                T("tax_rate"), value=float(st.session_state["lbo_ops_tax_rate"][i]),
                min_value=0.0, max_value=60.0, step=0.5, format="%.1f",
                key=f"lbo_op_tx_{i}"
            )

    st.session_state["lbo_int_income_rate"] = st.number_input(
        T("int_income_rate"), value=float(st.session_state["lbo_int_income_rate"]),
        min_value=0.0, max_value=20.0, step=0.25, format="%.2f"
    )

    ops = {
        "rev_growth": st.session_state["lbo_ops_rev_growth"],
        "ebitda_mgn": st.session_state["lbo_ops_ebitda_mgn"],
        "da_pct": st.session_state["lbo_ops_da_pct"],
        "capex_pct": st.session_state["lbo_ops_capex_pct"],
        "wc_pct": st.session_state["lbo_ops_wc_pct"],
        "tax_rate": st.session_state["lbo_ops_tax_rate"],
        "int_income_rate": st.session_state["lbo_int_income_rate"],
    }

    ops_df = project_operations(target, tx, ops, years)

    # Build debt schedule now that we have ops
    tranche_inputs = {
        "tla_rate": st.session_state["lbo_tla_rate"],
        "tla_tenor": st.session_state["lbo_tla_tenor"],
        "tlb_rate": st.session_state["lbo_tlb_rate"],
        "tlb_tenor": st.session_state["lbo_tlb_tenor"],
        "srn_rate": st.session_state["lbo_srn_rate"],
        "srn_tenor": st.session_state["lbo_srn_tenor"],
        "subn_rate": st.session_state["lbo_subn_rate"],
        "subn_tenor": st.session_state["lbo_subn_tenor"],
        "mezz_cash_rate": st.session_state["lbo_mezz_cash_rate"],
        "mezz_pik_rate": st.session_state["lbo_mezz_pik_rate"],
        "mezz_tenor": st.session_state["lbo_mezz_tenor"],
    }
    debt_pkg = build_debt_schedule(
        tx, ops_df, tranche_inputs, ops, target, years,
        st.session_state["lbo_cash_sweep"]
    )
    debt_df = debt_pkg["debt_df"]

    section_header(T("ops_proj"))

    display_rows = []
    for idx, row in debt_df.iterrows():
        display_rows.append({
            T("year"): int(row["Year"]),
            T("revenue"): ops_df.iloc[idx]["Revenue"],
            T("ebitda"): row["EBITDA"],
            "D&A": row["D&A"],
            T("ebit"): row["EBIT"],
            T("int_exp"): row["Total Interest (Tax)"],
            T("ebt"): row["EBT"],
            T("tax"): row["Tax"],
            T("ni"): row["NI"],
            "CapEx": row["CapEx"],
            "ΔWC": row["ΔWC"],
            T("fcf"): row["FCF"],
        })
    disp_df = pd.DataFrame(display_rows)
    num_cols = [c for c in disp_df.columns if c != T("year")]
    st.dataframe(
        disp_df.style.format({c: "{:,.1f}" for c in num_cols}),
        hide_index=True, use_container_width=True,
    )

    # Revenue & EBITDA chart
    sub_header(T("rev_ebitda_chart"))
    fig_re = go.Figure()
    fig_re.add_trace(go.Bar(
        x=[f"Y{int(y)}" for y in ops_df["Year"]],
        y=ops_df["Revenue"],
        name=T("revenue"),
        marker=dict(color=PRIMARY_LIGHT),
        yaxis="y1",
    ))
    fig_re.add_trace(go.Scatter(
        x=[f"Y{int(y)}" for y in ops_df["Year"]],
        y=ops_df["EBITDA"],
        name=T("ebitda"),
        mode="lines+markers",
        line=dict(color=PRIMARY, width=3),
        marker=dict(size=10),
        yaxis="y2",
    ))
    fig_re.update_layout(
        height=380, margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Revenue ($M)", side="left"),
        yaxis2=dict(title="EBITDA ($M)", side="right", overlaying="y"),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_re, use_container_width=True)

    with st.expander("Operating Projections Primer"):
        if st.session_state["lbo_lang"] == "en":
            st.markdown("""
**FCF Build:**
- EBITDA (operating cash proxy)
- Less: Cash Taxes (tax shield from interest flows through)
- Less: CapEx (maintenance + growth)
- Less: Change in Working Capital
- Less: Cash Interest (+ Interest Income on cash balance)
- = **Free Cash Flow available for debt paydown**

In an LBO, FCF is the fuel that deleverages the company. The more predictable and robust FCF, the more leverage can be supported at close.
            """)
        else:
            st.markdown("""
**Construção do FCF:**
- EBITDA (proxy de caixa operacional)
- Menos: Imposto pago (escudo fiscal dos juros flui aqui)
- Menos: CapEx (manutenção + crescimento)
- Menos: Variação de capital de giro
- Menos: Juros pagos (+ receita financeira sobre caixa)
- = **FCF disponível para amortizar dívida**

Em LBO, o FCF é o combustível que desalavanca a empresa. Quanto mais previsível e robusto, mais dívida pode ser suportada no fechamento.
            """)


# =============================================================================
# TAB 4 — DEBT SCHEDULE
# =============================================================================
with tabs[3]:
    section_header(T("debt_config"))

    dc1, dc2 = st.columns(2)
    with dc1:
        st.session_state["lbo_cash_sweep"] = st.slider(
            T("cash_sweep"), min_value=0.0, max_value=100.0,
            value=float(st.session_state["lbo_cash_sweep"]),
            step=5.0, format="%.0f%%"
        )
    with dc2:
        info_box(
            "TLA: straight-line amortization. TLB: 1%/yr + bullet. Notes: bullet. Mezz: bullet + PIK accrual."
            if st.session_state["lbo_lang"] == "en"
            else "TLA: linear. TLB: 1%/ano + bullet. Notes: bullet. Mezz: bullet + PIK."
        )

    # Rebuild with latest sweep
    debt_pkg = build_debt_schedule(
        tx, ops_df, tranche_inputs, ops, target, years,
        st.session_state["lbo_cash_sweep"]
    )
    debt_df = debt_pkg["debt_df"]

    section_header(T("debt_table"))

    # Build a cleaner debt schedule display
    debt_display = []
    for idx, row in debt_df.iterrows():
        debt_display.append({
            T("year"): int(row["Year"]),
            "TLA " + T("open_bal"): row["Open TLA"],
            "TLA " + T("mand_amort"): row["Mand TLA"],
            "TLA " + T("sweep"): row["Sweep TLA"],
            "TLA " + T("close_bal"): row["Close TLA"],
            "TLB " + T("close_bal"): row["Close TLB"],
            "SrN " + T("close_bal"): row["Close SrN"],
            "SubN " + T("close_bal"): row["Close SubN"],
            "Mezz " + T("close_bal"): row["Close Mezz"],
            "Total " + T("close_bal"): row["Close Total"],
            T("cash"): row["Cash"],
            T("net_debt"): row["Net Debt"],
            T("int_exp"): row["Interest Cash"],
            "PIK": row["Interest PIK"],
        })
    dd = pd.DataFrame(debt_display)
    num_cols = [c for c in dd.columns if c != T("year")]
    st.dataframe(
        dd.style.format({c: "{:,.1f}" for c in num_cols}),
        hide_index=True, use_container_width=True,
    )

    # Debt balance chart
    sub_header(T("debt_chart"))
    years_axis = [f"Y{int(y)}" for y in debt_df["Year"]]
    # Prepend Y0
    years_axis_full = ["Y0"] + years_axis

    tla_series = [tx["tla"]] + debt_df["Close TLA"].tolist()
    tlb_series = [tx["tlb"]] + debt_df["Close TLB"].tolist()
    srn_series = [tx["srn"]] + debt_df["Close SrN"].tolist()
    subn_series = [tx["subn"]] + debt_df["Close SubN"].tolist()
    mezz_series = [tx["mezz"]] + debt_df["Close Mezz"].tolist()

    fig_debt = go.Figure()
    fig_debt.add_trace(go.Bar(x=years_axis_full, y=tla_series, name="TLA", marker_color=DEBT_COLORS["TLA"]))
    fig_debt.add_trace(go.Bar(x=years_axis_full, y=tlb_series, name="TLB", marker_color=DEBT_COLORS["TLB"]))
    fig_debt.add_trace(go.Bar(x=years_axis_full, y=srn_series, name="Sr Notes", marker_color=DEBT_COLORS["Senior Notes"]))
    fig_debt.add_trace(go.Bar(x=years_axis_full, y=subn_series, name="Sub Notes", marker_color=DEBT_COLORS["Sub Notes"]))
    fig_debt.add_trace(go.Bar(x=years_axis_full, y=mezz_series, name="Mezz", marker_color=DEBT_COLORS["Mezzanine"]))
    fig_debt.update_layout(
        barmode="stack",
        height=420, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Debt Balance ($M)",
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_debt, use_container_width=True)

    # Leverage profile
    sub_header(T("leverage_chart"))
    lev_total = (debt_df["Close Total"] / debt_df["EBITDA"]).tolist()
    lev_senior = (debt_df["Senior Close"] / debt_df["EBITDA"]).tolist()
    net_lev = (debt_df["Net Debt"] / debt_df["EBITDA"]).tolist()

    fig_lev = go.Figure()
    fig_lev.add_trace(go.Scatter(
        x=years_axis, y=lev_total, name=T("total_leverage"),
        mode="lines+markers", line=dict(color=PRIMARY, width=3), marker=dict(size=10)
    ))
    fig_lev.add_trace(go.Scatter(
        x=years_axis, y=lev_senior, name=T("senior_leverage"),
        mode="lines+markers", line=dict(color=ACCENT_GREEN, width=3, dash="dash"), marker=dict(size=10)
    ))
    fig_lev.add_trace(go.Scatter(
        x=years_axis, y=net_lev, name="Net Debt / EBITDA",
        mode="lines+markers", line=dict(color=ACCENT_PURPLE, width=3, dash="dot"), marker=dict(size=10)
    ))
    fig_lev.update_layout(
        height=380, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="x EBITDA",
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_lev, use_container_width=True)

    # Coverage metrics
    sub_header(T("int_cov") + " & " + T("dscr"))
    cov_rows = []
    for idx, row in debt_df.iterrows():
        ebitda_y = row["EBITDA"]
        interest = row["Interest Cash"] if row["Interest Cash"] > 0 else 0.001
        mand = (row["Mand TLA"] + row["Mand TLB"] + row["Mand SrN"] + row["Mand SubN"] + row["Mand Mezz"])
        debt_service = interest + mand if interest + mand > 0 else 0.001
        int_cov = row["EBITDA"] / interest
        dscr = row["EBITDA"] / debt_service
        cov_rows.append({
            T("year"): int(row["Year"]),
            T("dscr"): dscr,
            T("int_cov"): int_cov,
            "Total Debt/EBITDA": row["Close Total"] / ebitda_y if ebitda_y > 0 else 0,
            "Senior/EBITDA": row["Senior Close"] / ebitda_y if ebitda_y > 0 else 0,
        })
    cov_df = pd.DataFrame(cov_rows)
    st.dataframe(
        cov_df.style.format({c: "{:,.2f}x" for c in cov_df.columns if c != T("year")}),
        hide_index=True, use_container_width=True,
    )


# =============================================================================
# TAB 5 — RETURNS
# =============================================================================
with tabs[4]:
    section_header(T("returns_inputs"))

    rc1, rc2 = st.columns(2)
    with rc1:
        st.session_state["lbo_exit_year"] = st.slider(
            T("exit_year"), min_value=1, max_value=years,
            value=min(int(st.session_state["lbo_exit_year"]), years)
        )
    with rc2:
        st.session_state["lbo_exit_mult"] = st.number_input(
            T("exit_multiple"), value=float(st.session_state["lbo_exit_mult"]),
            min_value=1.0, max_value=30.0, step=0.25, format="%.2f"
        )

    returns = compute_returns(
        debt_df, tx, target,
        st.session_state["lbo_exit_year"],
        st.session_state["lbo_exit_mult"]
    )

    section_header(T("returns_metrics"))
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        irr_val = returns.get("irr", float("nan"))
        metric_card(T("irr"), fmt_pct(irr_val) if not math.isnan(irr_val) else "n/a",
                    color="green" if (not math.isnan(irr_val) and irr_val >= 0.20) else "amber")
    with r2:
        moic_val = returns.get("moic", float("nan"))
        metric_card(T("moic"), fmt_mult(moic_val) if not math.isnan(moic_val) else "n/a",
                    color="green" if (not math.isnan(moic_val) and moic_val >= 2.0) else "amber")
    with r3:
        metric_card(T("sponsor_proceeds"), fmt_money(returns.get("sponsor_proceeds", 0)), color="purple")
    with r4:
        metric_card(T("value_created"), fmt_money(returns.get("value_created", 0)),
                    color="green" if returns.get("value_created", 0) > 0 else "red")

    r5, r6, r7, r8 = st.columns(4)
    with r5:
        metric_card(T("exit_ev"), fmt_money(returns.get("exit_ev", 0)))
    with r6:
        metric_card(T("exit_net_debt"), fmt_money(returns.get("exit_net_debt", 0)), color="amber")
    with r7:
        metric_card(T("exit_equity"), fmt_money(returns.get("exit_equity", 0)))
    with r8:
        metric_card(T("sponsor_eq_inv"), fmt_money(returns.get("sponsor_eq_in", 0)))

    # Value creation bridge
    section_header(T("value_bridge"))

    ebitda_growth_contrib = returns.get("ebitda_growth_contrib", 0)
    mult_exp_contrib = returns.get("mult_exp_contrib", 0)
    debt_paydown_contrib = returns.get("debt_paydown_contrib", 0)

    fig_vb = go.Figure(go.Waterfall(
        name="Value Creation",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Entry Equity", T("ebitda_growth"), T("mult_expansion"), T("debt_paydown"), "Exit Equity"],
        y=[tx["sponsor_eq"] + tx["rollover"],
           ebitda_growth_contrib,
           mult_exp_contrib,
           debt_paydown_contrib,
           0],
        connector=dict(line=dict(color=TEXT_MUTED)),
        increasing=dict(marker=dict(color=ACCENT_GREEN)),
        decreasing=dict(marker=dict(color=ACCENT_RED)),
        totals=dict(marker=dict(color=PRIMARY)),
        text=[fmt_money(tx["sponsor_eq"] + tx["rollover"]),
              fmt_money(ebitda_growth_contrib),
              fmt_money(mult_exp_contrib),
              fmt_money(debt_paydown_contrib),
              ""],
        textposition="outside",
    ))
    fig_vb.update_layout(
        height=420, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="$M",
    )
    st.plotly_chart(fig_vb, use_container_width=True)

    # Returns sensitivity: Exit Multiple × Hold Period
    section_header(T("sens_table"))

    exit_mults = np.arange(
        max(2.0, st.session_state["lbo_exit_mult"] - 2.0),
        st.session_state["lbo_exit_mult"] + 2.25, 0.5
    )
    hold_periods = list(range(1, years + 1))

    sens_matrix = []
    for em in exit_mults:
        row_vals = []
        for hp in hold_periods:
            r = compute_returns(debt_df, tx, target, hp, em)
            irr_v = r.get("irr", float("nan"))
            row_vals.append(irr_v * 100 if not math.isnan(irr_v) else 0)
        sens_matrix.append(row_vals)

    sens_arr = np.array(sens_matrix)

    fig_sens = go.Figure(data=go.Heatmap(
        z=sens_arr,
        x=[f"{hp}Y" for hp in hold_periods],
        y=[f"{em:.1f}x" for em in exit_mults],
        colorscale="RdYlGn",
        text=[[f"{v:.1f}%" for v in row] for row in sens_arr],
        texttemplate="%{text}",
        colorbar=dict(title="IRR (%)"),
    ))
    fig_sens.update_layout(
        height=380, margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title=T("hold_period"),
        yaxis_title=T("exit_multiple"),
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    with st.expander("MOIC vs IRR Primer"):
        if st.session_state["lbo_lang"] == "en":
            st.markdown("""
**MOIC (Multiple on Invested Capital)** = Total Distributions / Equity Invested
- Simple cash-on-cash metric, ignores time value of money
- A 2.0x MOIC means you doubled your money regardless of time

**IRR (Internal Rate of Return)** = discount rate that sets NPV of cash flows to zero
- Captures time value of money
- Approximations: 2.0x in 5 years ≈ 15% IRR; 3.0x in 5 years ≈ 25% IRR
- 2.0x in 3 years ≈ 26% IRR (shorter hold = higher IRR for same MOIC)

**Classic PE returns target:** 2.0-2.5x MOIC / 20-25% IRR over 5 years.

**Value Creation Bridge decomposes sponsor value into:**
1. **EBITDA growth** (operational improvement) — most sustainable
2. **Multiple expansion** (exit > entry) — market-dependent, less reliable
3. **Debt paydown** (financial engineering) — FCF-dependent
            """)
        else:
            st.markdown("""
**MOIC (Multiple on Invested Capital)** = Distribuições Totais / Equity Investido
- Métrica cash-on-cash simples, ignora o valor do dinheiro no tempo
- 2.0x MOIC = dobrou o dinheiro, independente do prazo

**TIR (Taxa Interna de Retorno)** = taxa que zera o VPL dos fluxos
- Captura o valor do dinheiro no tempo
- Aproximações: 2.0x em 5 anos ≈ 15% TIR; 3.0x em 5 anos ≈ 25% TIR
- 2.0x em 3 anos ≈ 26% TIR (hold menor = maior TIR para mesmo MOIC)

**Alvo clássico de PE:** 2.0-2.5x MOIC / 20-25% TIR em 5 anos.

**A ponte de criação de valor decompõe o valor em:**
1. **Crescimento de EBITDA** (melhoria operacional) — mais sustentável
2. **Expansão de múltiplo** (saída > entrada) — depende do mercado
3. **Amortização de dívida** (engenharia financeira) — depende do FCF
            """)


# =============================================================================
# TAB 6 — SENSITIVITY & SCENARIOS
# =============================================================================
with tabs[5]:
    section_header(T("sens_2d"))

    # Helper: recompute IRR for a modified parameter set
    def compute_scenario_irr(entry_mult_override=None, exit_mult_override=None,
                              rev_cagr_override=None, leverage_override=None,
                              hold_override=None, margin_override=None):
        # Deep copy inputs
        scenario_tx_inputs = dict(tx_inputs)
        if entry_mult_override is not None:
            scenario_tx_inputs["entry_mult"] = entry_mult_override
        if leverage_override is not None:
            # Scale total leverage — distribute proportionally
            base_total_pct = (st.session_state["lbo_tla_pct"] + st.session_state["lbo_tlb_pct"]
                              + st.session_state["lbo_srn_pct"] + st.session_state["lbo_subn_pct"]
                              + st.session_state["lbo_mezz_pct"])
            if base_total_pct > 0:
                # leverage_override in turns — convert to %EV: lev * EBITDA / EV
                target_debt_dollars = leverage_override * ebitda
                new_ev = ebitda * scenario_tx_inputs["entry_mult"]
                target_pct = target_debt_dollars / new_ev * 100 if new_ev > 0 else 0
                scale = target_pct / base_total_pct if base_total_pct > 0 else 1.0
                scenario_tx_inputs["tla_pct"] *= scale
                scenario_tx_inputs["tlb_pct"] *= scale
                scenario_tx_inputs["srn_pct"] *= scale
                scenario_tx_inputs["subn_pct"] *= scale
                scenario_tx_inputs["mezz_pct"] *= scale

        s_tx = build_transaction(scenario_tx_inputs)

        # Modify ops
        s_ops = {
            "rev_growth": [rev_cagr_override if rev_cagr_override is not None else g
                           for g in ops["rev_growth"]],
            "ebitda_mgn": [margin_override if margin_override is not None else m
                           for m in ops["ebitda_mgn"]],
            "da_pct": ops["da_pct"],
            "capex_pct": ops["capex_pct"],
            "wc_pct": ops["wc_pct"],
            "tax_rate": ops["tax_rate"],
            "int_income_rate": ops["int_income_rate"],
        }

        s_ops_df = project_operations(target, s_tx, s_ops, years)
        s_debt_pkg = build_debt_schedule(
            s_tx, s_ops_df, tranche_inputs, s_ops, target, years,
            st.session_state["lbo_cash_sweep"]
        )
        s_debt_df = s_debt_pkg["debt_df"]

        hp = hold_override if hold_override is not None else st.session_state["lbo_exit_year"]
        em = exit_mult_override if exit_mult_override is not None else st.session_state["lbo_exit_mult"]
        r = compute_returns(s_debt_df, s_tx, target, hp, em)
        return r.get("irr", float("nan")), r.get("moic", float("nan"))

    # --- Entry × Exit Multiple ---
    sub_header(T("sens_entry_exit"))
    entry_range = np.arange(
        max(4.0, st.session_state["lbo_entry_mult"] - 2.0),
        st.session_state["lbo_entry_mult"] + 2.25, 0.5
    )
    exit_range = np.arange(
        max(4.0, st.session_state["lbo_exit_mult"] - 2.0),
        st.session_state["lbo_exit_mult"] + 2.25, 0.5
    )

    sens_ee = np.zeros((len(exit_range), len(entry_range)))
    for i, em in enumerate(exit_range):
        for j, en in enumerate(entry_range):
            irrv, _ = compute_scenario_irr(entry_mult_override=en, exit_mult_override=em)
            sens_ee[i, j] = irrv * 100 if not math.isnan(irrv) else 0

    fig_ee = go.Figure(data=go.Heatmap(
        z=sens_ee,
        x=[f"{e:.1f}x" for e in entry_range],
        y=[f"{e:.1f}x" for e in exit_range],
        colorscale="RdYlGn",
        text=[[f"{v:.1f}%" for v in row] for row in sens_ee],
        texttemplate="%{text}",
        colorbar=dict(title="IRR %"),
    ))
    fig_ee.update_layout(
        height=360, margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title=T("entry_multiple"),
        yaxis_title=T("exit_multiple"),
    )
    st.plotly_chart(fig_ee, use_container_width=True)

    # --- Revenue CAGR × Exit Multiple ---
    sub_header(T("sens_cagr_exit"))
    cagr_range = np.arange(
        max(-5.0, st.session_state["lbo_rev_growth"] - 6.0),
        st.session_state["lbo_rev_growth"] + 6.5, 1.5
    )
    sens_ce = np.zeros((len(exit_range), len(cagr_range)))
    for i, em in enumerate(exit_range):
        for j, g in enumerate(cagr_range):
            irrv, _ = compute_scenario_irr(rev_cagr_override=g, exit_mult_override=em)
            sens_ce[i, j] = irrv * 100 if not math.isnan(irrv) else 0

    fig_ce = go.Figure(data=go.Heatmap(
        z=sens_ce,
        x=[f"{g:.1f}%" for g in cagr_range],
        y=[f"{e:.1f}x" for e in exit_range],
        colorscale="RdYlGn",
        text=[[f"{v:.1f}%" for v in row] for row in sens_ce],
        texttemplate="%{text}",
        colorbar=dict(title="IRR %"),
    ))
    fig_ce.update_layout(
        height=360, margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Revenue CAGR",
        yaxis_title=T("exit_multiple"),
    )
    st.plotly_chart(fig_ce, use_container_width=True)

    # --- Leverage × Exit Multiple ---
    sub_header(T("sens_lev_exit"))
    lev_range = np.arange(
        max(3.0, tx["total_lev"] - 2.0),
        tx["total_lev"] + 2.25, 0.5
    )
    sens_le = np.zeros((len(exit_range), len(lev_range)))
    for i, em in enumerate(exit_range):
        for j, lev in enumerate(lev_range):
            irrv, _ = compute_scenario_irr(leverage_override=lev, exit_mult_override=em)
            sens_le[i, j] = irrv * 100 if not math.isnan(irrv) else 0

    fig_le = go.Figure(data=go.Heatmap(
        z=sens_le,
        x=[f"{l:.1f}x" for l in lev_range],
        y=[f"{e:.1f}x" for e in exit_range],
        colorscale="RdYlGn",
        text=[[f"{v:.1f}%" for v in row] for row in sens_le],
        texttemplate="%{text}",
        colorbar=dict(title="IRR %"),
    ))
    fig_le.update_layout(
        height=360, margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Total Leverage",
        yaxis_title=T("exit_multiple"),
    )
    st.plotly_chart(fig_le, use_container_width=True)

    # --- Tornado ---
    section_header(T("tornado"))
    base_irr, _ = compute_scenario_irr()

    drivers = []
    # EBITDA margin: +/- 2pp
    base_margin = st.session_state["lbo_ebitda_mgn_proj"]
    irr_lo, _ = compute_scenario_irr(margin_override=base_margin - 2.0)
    irr_hi, _ = compute_scenario_irr(margin_override=base_margin + 2.0)
    drivers.append(("EBITDA Margin ±2pp", irr_lo, irr_hi))

    # Revenue growth +/- 3pp
    base_g = st.session_state["lbo_rev_growth"]
    irr_lo, _ = compute_scenario_irr(rev_cagr_override=base_g - 3.0)
    irr_hi, _ = compute_scenario_irr(rev_cagr_override=base_g + 3.0)
    drivers.append(("Revenue Growth ±3pp", irr_lo, irr_hi))

    # Exit multiple +/- 1.0x
    base_em = st.session_state["lbo_exit_mult"]
    irr_lo, _ = compute_scenario_irr(exit_mult_override=base_em - 1.0)
    irr_hi, _ = compute_scenario_irr(exit_mult_override=base_em + 1.0)
    drivers.append(("Exit Multiple ±1.0x", irr_lo, irr_hi))

    # Leverage +/- 1.0x
    base_lev = tx["total_lev"]
    irr_lo, _ = compute_scenario_irr(leverage_override=max(0.5, base_lev - 1.0))
    irr_hi, _ = compute_scenario_irr(leverage_override=base_lev + 1.0)
    drivers.append(("Leverage ±1.0x", irr_lo, irr_hi))

    # Hold period +/- 1 year
    base_hp = st.session_state["lbo_exit_year"]
    if base_hp > 1:
        irr_lo, _ = compute_scenario_irr(hold_override=base_hp - 1)
    else:
        irr_lo = base_irr
    if base_hp < years:
        irr_hi, _ = compute_scenario_irr(hold_override=base_hp + 1)
    else:
        irr_hi = base_irr
    drivers.append(("Hold Period ±1yr", irr_lo, irr_hi))

    # Sort by impact
    def impact(d):
        lo, hi = d[1], d[2]
        if math.isnan(lo) or math.isnan(hi):
            return 0
        return abs(hi - lo)

    drivers.sort(key=impact, reverse=True)

    t_labels = [d[0] for d in drivers]
    lo_vals = [(d[1] - base_irr) * 100 if not math.isnan(d[1]) else 0 for d in drivers]
    hi_vals = [(d[2] - base_irr) * 100 if not math.isnan(d[2]) else 0 for d in drivers]

    fig_t = go.Figure()
    fig_t.add_trace(go.Bar(
        y=t_labels, x=lo_vals, orientation="h",
        name="Downside", marker=dict(color=ACCENT_RED),
        text=[f"{v:+.1f}pp" for v in lo_vals], textposition="outside",
    ))
    fig_t.add_trace(go.Bar(
        y=t_labels, x=hi_vals, orientation="h",
        name="Upside", marker=dict(color=ACCENT_GREEN),
        text=[f"{v:+.1f}pp" for v in hi_vals], textposition="outside",
    ))
    fig_t.update_layout(
        barmode="overlay",
        height=380, margin=dict(l=10, r=80, t=30, b=10),
        xaxis_title=f"IRR Δ from Base ({fmt_pct(base_irr) if not math.isnan(base_irr) else 'n/a'})",
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig_t, use_container_width=True)

    # --- Scenarios ---
    section_header(T("scenarios"))

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        sub_header(T("bear"))
        bear_g = st.number_input("Rev Growth", value=max(0.0, st.session_state["lbo_rev_growth"] - 4.0),
                                 step=0.5, format="%.1f", key="lbo_bear_g")
        bear_m = st.number_input("EBITDA Mgn", value=max(5.0, st.session_state["lbo_ebitda_mgn_proj"] - 3.0),
                                 step=0.5, format="%.1f", key="lbo_bear_m")
        bear_em = st.number_input("Exit Mult", value=max(3.0, st.session_state["lbo_exit_mult"] - 2.0),
                                  step=0.25, format="%.2f", key="lbo_bear_em")
        st.session_state["lbo_bear_prob"] = st.number_input(
            T("probability"), value=float(st.session_state["lbo_bear_prob"]),
            min_value=0.0, max_value=100.0, step=5.0, format="%.1f", key="lbo_bear_p"
        )

    with sc2:
        sub_header(T("base"))
        base_g_disp = st.session_state["lbo_rev_growth"]
        base_m_disp = st.session_state["lbo_ebitda_mgn_proj"]
        base_em_disp = st.session_state["lbo_exit_mult"]
        st.markdown(f"- Rev Growth: **{base_g_disp:.1f}%**")
        st.markdown(f"- EBITDA Mgn: **{base_m_disp:.1f}%**")
        st.markdown(f"- Exit Mult: **{base_em_disp:.2f}x**")
        st.session_state["lbo_base_prob"] = st.number_input(
            T("probability"), value=float(st.session_state["lbo_base_prob"]),
            min_value=0.0, max_value=100.0, step=5.0, format="%.1f", key="lbo_base_p"
        )

    with sc3:
        sub_header(T("bull"))
        bull_g = st.number_input("Rev Growth", value=st.session_state["lbo_rev_growth"] + 3.0,
                                 step=0.5, format="%.1f", key="lbo_bull_g")
        bull_m = st.number_input("EBITDA Mgn", value=st.session_state["lbo_ebitda_mgn_proj"] + 2.0,
                                 step=0.5, format="%.1f", key="lbo_bull_m")
        bull_em = st.number_input("Exit Mult", value=st.session_state["lbo_exit_mult"] + 1.5,
                                  step=0.25, format="%.2f", key="lbo_bull_em")
        st.session_state["lbo_bull_prob"] = st.number_input(
            T("probability"), value=float(st.session_state["lbo_bull_prob"]),
            min_value=0.0, max_value=100.0, step=5.0, format="%.1f", key="lbo_bull_p"
        )

    # Evaluate scenarios
    bear_irr, bear_moic = compute_scenario_irr(
        rev_cagr_override=bear_g, margin_override=bear_m, exit_mult_override=bear_em
    )
    bull_irr, bull_moic = compute_scenario_irr(
        rev_cagr_override=bull_g, margin_override=bull_m, exit_mult_override=bull_em
    )
    base_irr_sc, base_moic_sc = compute_scenario_irr()

    prob_sum = (st.session_state["lbo_bear_prob"] + st.session_state["lbo_base_prob"]
                + st.session_state["lbo_bull_prob"])
    if prob_sum > 0:
        w_bear = st.session_state["lbo_bear_prob"] / prob_sum
        w_base = st.session_state["lbo_base_prob"] / prob_sum
        w_bull = st.session_state["lbo_bull_prob"] / prob_sum
    else:
        w_bear = w_base = w_bull = 1 / 3

    def _safe(v):
        return 0 if math.isnan(v) else v

    exp_irr = (_safe(bear_irr) * w_bear + _safe(base_irr_sc) * w_base + _safe(bull_irr) * w_bull)
    exp_moic = (_safe(bear_moic) * w_bear + _safe(base_moic_sc) * w_base + _safe(bull_moic) * w_bull)

    sc_df = pd.DataFrame([
        {"Scenario": T("bear"), "Probability": st.session_state["lbo_bear_prob"] / 100,
         T("irr"): bear_irr, T("moic"): bear_moic},
        {"Scenario": T("base"), "Probability": st.session_state["lbo_base_prob"] / 100,
         T("irr"): base_irr_sc, T("moic"): base_moic_sc},
        {"Scenario": T("bull"), "Probability": st.session_state["lbo_bull_prob"] / 100,
         T("irr"): bull_irr, T("moic"): bull_moic},
    ])
    st.dataframe(
        sc_df.style.format({
            "Probability": "{:.1%}",
            T("irr"): "{:.1%}",
            T("moic"): "{:.2f}x",
        }),
        hide_index=True, use_container_width=True,
    )

    ec1, ec2 = st.columns(2)
    with ec1:
        metric_card(T("expected_irr"), fmt_pct(exp_irr), color="purple")
    with ec2:
        metric_card(T("expected_moic"), fmt_mult(exp_moic), color="purple")


# =============================================================================
# TAB 7 — THREE-STATEMENT INTEGRATION
# =============================================================================
with tabs[6]:
    section_header(T("three_stmt"))

    st.session_state["lbo_ppa_writeup"] = st.slider(
        T("ppa_writeup"), min_value=0.0, max_value=100.0,
        value=float(st.session_state["lbo_ppa_writeup"]),
        step=5.0, format="%.0f%%"
    )

    # Rebuild with current params — debt_df already computed
    # Compute Goodwill (at close)
    book_equity_pre = max(0.0, (target["revenue"] * target["ebitda_margin"]) * 5.0)  # simple proxy
    # Better: book equity = shares * book value per share, we don't have that; use market_cap minus PPA uplift
    # PPA write-up: portion of premium allocated to intangibles/PP&E that receives a step-up
    purchase_premium = tx["eq_purchase"] - book_equity_pre
    ppa_writeup_amt = max(0.0, purchase_premium) * (st.session_state["lbo_ppa_writeup"] / 100.0)
    goodwill = max(0.0, purchase_premium - ppa_writeup_amt)

    # ---- INCOME STATEMENT ----
    sub_header(T("income_stmt"))

    is_rows = []
    for idx, row in debt_df.iterrows():
        is_rows.append({
            T("year"): int(row["Year"]),
            T("revenue"): ops_df.iloc[idx]["Revenue"],
            T("ebitda"): row["EBITDA"],
            "D&A": row["D&A"],
            T("ebit"): row["EBIT"],
            "Interest Expense (Cash)": row["Interest Cash"],
            "Interest Income": row["Interest Income"],
            "PIK Interest": row["Interest PIK"],
            T("ebt"): row["EBT"],
            T("tax"): row["Tax"],
            T("ni"): row["NI"],
        })
    is_df = pd.DataFrame(is_rows)
    num_cols = [c for c in is_df.columns if c != T("year")]
    st.dataframe(
        is_df.style.format({c: "{:,.1f}" for c in num_cols}),
        hide_index=True, use_container_width=True,
    )

    # ---- CASH FLOW STATEMENT ----
    sub_header(T("cf_stmt"))
    cf_rows = []
    prior_cash = tx["min_cash"]
    for idx, row in debt_df.iterrows():
        ni = row["NI"]
        da = row["D&A"]
        pik = row["Interest PIK"]
        delta_wc = row["ΔWC"]
        cfo = ni + da + pik - delta_wc  # PIK is non-cash, add back
        capex = row["CapEx"]
        cfi = -capex
        total_mand = row["Mand TLA"] + row["Mand TLB"] + row["Mand SrN"] + row["Mand SubN"] + row["Mand Mezz"]
        total_sweep = row["Sweep TLA"] + row["Sweep TLB"] + row["Sweep SrN"] + row["Sweep SubN"]
        cff = -(total_mand + total_sweep)
        delta_cash = cfo + cfi + cff
        ending_cash = row["Cash"]
        cf_rows.append({
            T("year"): int(row["Year"]),
            T("ni"): ni,
            "+ D&A": da,
            "+ PIK (non-cash)": pik,
            "- ΔWC": -delta_wc,
            "CFO": cfo,
            "- CapEx": -capex,
            "CFI": cfi,
            "Debt Repayments": -(total_mand + total_sweep),
            "CFF": cff,
            "Δ Cash": delta_cash,
            "Ending Cash": ending_cash,
        })
        prior_cash = ending_cash
    cf_df = pd.DataFrame(cf_rows)
    num_cols = [c for c in cf_df.columns if c != T("year")]
    st.dataframe(
        cf_df.style.format({c: "{:,.1f}" for c in num_cols}),
        hide_index=True, use_container_width=True,
    )

    # ---- BALANCE SHEET ----
    sub_header(T("bs_stmt"))

    # Opening (Day 0) BS — post-transaction
    # Assets: Cash + PPE (write-up) + Goodwill + Other (revenue-based proxy)
    # For simplicity: Net PP&E proxy = original book equity portion
    # Other assets (working capital) approximated as % of revenue
    day0_cash = tx["min_cash"]
    day0_ppe_writeup = ppa_writeup_amt
    day0_goodwill = goodwill
    # Operating assets (net WC + PPE base) — proxy
    day0_other_assets = target["revenue"] * 0.35  # simple operating asset proxy
    day0_total_assets = day0_cash + day0_ppe_writeup + day0_goodwill + day0_other_assets

    day0_debt = tx["new_debt_total"]
    day0_other_liab = target["revenue"] * 0.10  # operating liabilities proxy
    day0_equity = tx["sponsor_eq"] + tx["rollover"]
    day0_total_le = day0_debt + day0_other_liab + day0_equity

    # Plug any difference into goodwill (standard PPA method)
    day0_plug = day0_total_le - (day0_cash + day0_ppe_writeup + day0_other_assets)
    day0_goodwill = max(0.0, day0_plug)
    day0_total_assets = day0_cash + day0_ppe_writeup + day0_goodwill + day0_other_assets

    bs_rows = []
    bs_rows.append({
        T("year"): "Y0 (Close)",
        T("cash"): day0_cash,
        "Other Assets": day0_other_assets,
        "PP&E Write-Up": day0_ppe_writeup,
        T("goodwill"): day0_goodwill,
        T("assets"): day0_total_assets,
        "Total Debt": day0_debt,
        "Other Liab": day0_other_liab,
        "Equity": day0_equity,
        T("liab_eq"): day0_total_le,
        T("diff"): day0_total_assets - day0_total_le,
    })

    cum_ni = 0.0
    prior_other_assets = day0_other_assets
    prior_other_liab = day0_other_liab
    prior_ppe = day0_ppe_writeup
    for idx, row in debt_df.iterrows():
        cum_ni += row["NI"]
        cash_bal = row["Cash"]
        # PP&E: grows with CapEx, shrinks with D&A
        prior_ppe = prior_ppe + row["CapEx"] - row["D&A"]
        prior_ppe = max(0.0, prior_ppe)
        # Other operating assets scale with revenue
        rev_now = ops_df.iloc[idx]["Revenue"]
        other_assets_now = target["revenue"] * 0.35 * (rev_now / target["revenue"]) if target["revenue"] > 0 else day0_other_assets
        other_liab_now = target["revenue"] * 0.10 * (rev_now / target["revenue"]) if target["revenue"] > 0 else day0_other_liab

        # Goodwill stays constant (no impairment)
        gw = day0_goodwill

        total_assets = cash_bal + other_assets_now + prior_ppe + gw

        # Debt & equity
        total_debt_now = row["Close Total"]
        # Equity = initial equity + cumulative retained earnings
        equity_now = day0_equity + cum_ni

        total_le = total_debt_now + other_liab_now + equity_now

        bs_rows.append({
            T("year"): f"Y{int(row['Year'])}",
            T("cash"): cash_bal,
            "Other Assets": other_assets_now,
            "PP&E Write-Up": prior_ppe,
            T("goodwill"): gw,
            T("assets"): total_assets,
            "Total Debt": total_debt_now,
            "Other Liab": other_liab_now,
            "Equity": equity_now,
            T("liab_eq"): total_le,
            T("diff"): total_assets - total_le,
        })

    bs_df = pd.DataFrame(bs_rows)
    num_cols = [c for c in bs_df.columns if c != T("year")]
    st.dataframe(
        bs_df.style.format({c: "{:,.1f}" for c in num_cols}),
        hide_index=True, use_container_width=True,
    )

    # Balance check
    section_header(T("bs_check"))
    max_diff = bs_df[T("diff")].abs().max()
    if max_diff < 1.0:
        success_box(f"{T('bs_pass')} (max diff: {max_diff:.2f})")
    else:
        warning_box(
            f"{T('bs_fail')} — residuals reflect simplified PPA/plug approximations "
            f"(max diff: {max_diff:.2f}). In a full model, plug to goodwill or retained earnings."
        )

    g1, g2, g3 = st.columns(3)
    with g1:
        metric_card(T("goodwill"), fmt_money(day0_goodwill), color="purple")
    with g2:
        metric_card("PP&E Write-Up", fmt_money(day0_ppe_writeup))
    with g3:
        metric_card("Purchase Premium", fmt_money(purchase_premium), color="amber")

    with st.expander("Purchase Price Allocation (PPA) Primer"):
        if st.session_state["lbo_lang"] == "en":
            st.markdown("""
**Purchase Price Allocation (PPA) — ASC 805 / IFRS 3:**

When an LBO closes, the buyer must allocate the purchase price across the target's identifiable net assets at **fair value**. Any residual is **Goodwill**.

**Standard PPA waterfall:**
1. Start with Equity Purchase Price
2. Add: Assumed net debt (if stock deal)
3. Subtract: Fair value of identifiable net assets (net of deferred tax liabilities)
4. = **Goodwill** (residual)

**Common write-ups:**
- Intangible assets (customer relationships, trade names, technology)
- PP&E step-up to fair value
- Inventory step-up

**Key impact for LBO model:**
- Write-ups create **additional D&A** (lowers EBIT → lowers cash taxes)
- Under IFRS/US GAAP, Goodwill is **not amortized** but tested annually for impairment
- Creates a Deferred Tax Liability (not modeled here for simplicity)
            """)
        else:
            st.markdown("""
**Purchase Price Allocation (PPA) — CPC 15 / IFRS 3:**

Ao fechar um LBO, o comprador aloca o preço de compra entre os ativos identificáveis do alvo ao **valor justo**. O resíduo é o **Ágio (Goodwill)**.

**Cascata padrão de PPA:**
1. Comece com Preço de Compra do Equity
2. Some: dívida líquida assumida
3. Subtraia: valor justo dos ativos líquidos identificáveis
4. = **Ágio** (residual)

**Write-ups comuns:**
- Intangíveis (carteira de clientes, marca, tecnologia)
- PP&E ao valor justo
- Estoque

**Impacto no modelo LBO:**
- Write-ups criam **D&A adicional** (reduz EBIT → reduz IR caixa)
- Goodwill **não é amortizado** — sujeito a impairment anual
- Cria passivo fiscal diferido (não modelado aqui)
            """)


# =============================================================================
# FOOTER
# =============================================================================
st.markdown('<div style="text-align:center;padding:24px 0 12px 0;margin-top:40px;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.72rem">Corpet · MVP — Powered by Streamlit + Plotly</div>', unsafe_allow_html=True)
