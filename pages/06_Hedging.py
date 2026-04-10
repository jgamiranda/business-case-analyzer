# -*- coding: utf-8 -*-
"""
06_Hedging.py — Institutional-Grade Hedging Strategies Analyzer
================================================================
Multi-instrument hedging toolkit based on CME, ISDA, and multi-curve
framework standards. Covers FX Forwards, FX Futures, Interest Rate
Swaps, Cross-Currency Swaps, Total Return Swaps, and Portfolio Hedge
Effectiveness analysis.

References:
- Covered Interest Rate Parity (CIRP)
- CME Contract Specifications (6L, 6E, 6J, 6B)
- ISDA Master Agreement 2002 / 2021 definitions
- Multi-Curve Framework (post-2008 OIS discounting)
- IFRS 9 / ASC 815 Hedge Accounting (80-125% effectiveness rule)
- Ederington (1979) Minimum Variance Hedge Ratio
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime, timedelta

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Hedging Strategies",
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
BG_SOFT = "#f8fafc"
BORDER = "#e2e8f0"
TEXT_DARK = "#0f172a"
TEXT_MUTED = "#64748b"

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
    .metric-card {{
        background: linear-gradient(135deg, #ffffff 0%, {BG_SOFT} 100%);
        border: 1px solid {BORDER};
        border-left: 4px solid {PRIMARY};
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
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
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# BILINGUAL DICT
# =============================================================================
_L = {
    "en": {
        "title": "Hedging Strategies — Institutional Toolkit",
        "subtitle": "FX Forwards, Futures, IRS, CCS, TRS & Portfolio Hedge Effectiveness",
        "language": "Language",
        "tab_fwd": "FX Forward",
        "tab_fut": "FX Futures (CME)",
        "tab_irs": "Interest Rate Swap",
        "tab_ccs": "Cross-Currency Swap",
        "tab_trs": "Total Return Swap",
        "tab_eff": "Hedge Effectiveness",
        # FX Forward
        "fx_inputs": "Contract Inputs",
        "fx_pair": "Currency Pair",
        "fx_spot": "Spot Rate (S)",
        "fx_rd": "Domestic Rate (rd) % p.a.",
        "fx_rf": "Foreign Rate (rf) % p.a.",
        "fx_tenor": "Tenor (days)",
        "fx_basis": "Day Count Basis",
        "fx_notional": "Notional (Foreign CCY)",
        "fx_direction": "Hedge Direction",
        "buy_fwd": "Buy Forward (Long)",
        "sell_fwd": "Sell Forward (Short)",
        "fx_results": "Results — Covered Interest Rate Parity",
        "fwd_rate": "Forward Rate",
        "fwd_points": "Forward Points (pips)",
        "ann_prem": "Annualized Premium",
        "cost_hedge": "Cost of Hedge",
        "pnl_scenario": "P&L Scenario Analysis",
        "scenario_tbl": "Scenario Table",
        "spot_at_mat": "Spot at Maturity",
        "unhedged_pnl": "Unhedged P&L",
        "hedged_pnl": "Hedged P&L",
        "hedge_benefit": "Hedge Benefit",
        # Futures
        "fut_inputs": "Futures Contract",
        "fut_contract": "Contract Type",
        "fut_size": "Contract Size",
        "fut_num": "Number of Contracts",
        "fut_entry": "Entry Price",
        "fut_margin": "Initial Margin / Contract (USD)",
        "fut_current": "Current Price",
        "fut_dte": "Days to Expiry",
        "fut_port": "Portfolio Value Hedged (USD)",
        "hedge_params": "Optimal Hedge Parameters",
        "sigma_s": "Spot Volatility (% ann.)",
        "sigma_f": "Futures Volatility (% ann.)",
        "correl": "Correlation (ρ)",
        "notional_hedged": "Notional Hedged",
        "opt_hr": "Optimal Hedge Ratio (h*)",
        "num_contracts": "# Contracts Needed",
        "margin_req": "Margin Required",
        "mtm_pnl": "Mark-to-Market P&L",
        "basis_risk": "Basis Risk",
        "min_var": "Minimum Variance Hedge",
        "naive_hedge": "Naive 1:1 Hedge",
        # IRS
        "irs_inputs": "Swap Terms",
        "irs_not": "Notional",
        "irs_tenor": "Tenor (years)",
        "irs_freq": "Payment Frequency",
        "irs_fixed": "Fixed Rate (% p.a.)",
        "irs_index": "Floating Index",
        "irs_spread": "Floating Spread (bps)",
        "irs_position": "Position",
        "pay_fixed": "Pay Fixed",
        "rec_fixed": "Receive Fixed",
        "irs_dcb": "Day Count",
        "curve_input": "Yield Curve Input",
        "par_rate": "Par Swap Rate",
        "swap_pv": "Swap PV",
        "dv01": "DV01",
        "annuity": "Annuity Factor",
        "cf_table": "Cash Flows",
        "curve_viz": "Yield Curve",
        "sensitivity": "PV Sensitivity",
        # CCS
        "ccs_inputs": "CCS Parameters",
        "ccy1": "Currency 1",
        "ccy2": "Currency 2",
        "ccs_spot": "Spot Rate",
        "ccs_type": "Swap Type",
        "ff": "Fixed-Fixed",
        "fflt": "Fixed-Float",
        "fltflt": "Float-Float",
        "not_exch": "Notional Exchange",
        "mtm": "MTM (rebalanced)",
        "nonmtm": "Non-MTM",
        "basis_sp": "Basis Spread (bps)",
        "not_c1": "Notional CCY1",
        "not_c2": "Notional CCY2",
        "all_in": "All-in Cost (base)",
        # TRS
        "trs_inputs": "TRS Parameters",
        "under_type": "Underlying Type",
        "under_name": "Underlying Name",
        "ref_price": "Initial Reference Price",
        "trs_position": "Position",
        "tr_rec": "TR Receiver (Long)",
        "tr_pay": "TR Payer (Short)",
        "fin_idx": "Financing Index",
        "fin_sp": "Financing Spread (bps)",
        "trs_tenor": "Tenor (months)",
        "div_yld": "Expected Dividends / Coupons (% per period)",
        "collateral": "Initial Collateral (% of notional)",
        "leverage": "Leverage",
        "fin_cost": "Financing Cost",
        "exp_return": "Expected Return",
        # Effectiveness
        "port_val": "Portfolio Value",
        "asset_class": "Asset Class",
        "beta": "Beta to Market",
        "duration": "Duration (years)",
        "fx_exp": "FX Exposure",
        "hedge_instr": "Hedge Instrument",
        "hedge_ratio": "Hedge Ratio (%)",
        "var_red": "Variance Reduction",
        "eff_ratio": "Effectiveness Ratio",
        "var_unh": "VaR Unhedged (95%)",
        "var_h": "VaR Hedged (95%)",
        "recommend": "Recommendation",
        "eff_hedge": "Effective Hedge (qualifies for hedge accounting)",
        "partial_hedge": "Partial Hedge",
        "ineff_hedge": "Ineffective Hedge",
    },
    "pt": {
        "title": "Estratégias de Hedge — Toolkit Institucional",
        "subtitle": "FX Forward, Futuros, IRS, CCS, TRS e Efetividade de Hedge de Carteira",
        "language": "Idioma",
        "tab_fwd": "FX Forward",
        "tab_fut": "Futuros FX (CME)",
        "tab_irs": "Swap de Juros",
        "tab_ccs": "Swap Cambial",
        "tab_trs": "Total Return Swap",
        "tab_eff": "Efetividade de Hedge",
        "fx_inputs": "Dados do Contrato",
        "fx_pair": "Par de Moedas",
        "fx_spot": "Taxa Spot (S)",
        "fx_rd": "Taxa Doméstica (rd) % a.a.",
        "fx_rf": "Taxa Estrangeira (rf) % a.a.",
        "fx_tenor": "Prazo (dias)",
        "fx_basis": "Base (Day Count)",
        "fx_notional": "Nocional (Moeda Estrangeira)",
        "fx_direction": "Direção do Hedge",
        "buy_fwd": "Compra a Termo (Long)",
        "sell_fwd": "Venda a Termo (Short)",
        "fx_results": "Resultados — Paridade Coberta de Juros",
        "fwd_rate": "Taxa Forward",
        "fwd_points": "Pontos Forward (pips)",
        "ann_prem": "Prêmio Anualizado",
        "cost_hedge": "Custo do Hedge",
        "pnl_scenario": "Análise de Cenários P&L",
        "scenario_tbl": "Tabela de Cenários",
        "spot_at_mat": "Spot no Vencimento",
        "unhedged_pnl": "P&L Sem Hedge",
        "hedged_pnl": "P&L Com Hedge",
        "hedge_benefit": "Benefício do Hedge",
        "fut_inputs": "Contrato Futuro",
        "fut_contract": "Tipo de Contrato",
        "fut_size": "Tamanho do Contrato",
        "fut_num": "Número de Contratos",
        "fut_entry": "Preço de Entrada",
        "fut_margin": "Margem Inicial / Contrato (USD)",
        "fut_current": "Preço Atual",
        "fut_dte": "Dias até Vencimento",
        "fut_port": "Valor do Portfólio (USD)",
        "hedge_params": "Parâmetros Ótimos de Hedge",
        "sigma_s": "Volatilidade Spot (% a.a.)",
        "sigma_f": "Volatilidade Futuros (% a.a.)",
        "correl": "Correlação (ρ)",
        "notional_hedged": "Nocional Coberto",
        "opt_hr": "Hedge Ratio Ótimo (h*)",
        "num_contracts": "# Contratos Necessários",
        "margin_req": "Margem Requerida",
        "mtm_pnl": "P&L Mark-to-Market",
        "basis_risk": "Risco de Base",
        "min_var": "Hedge Variância Mínima",
        "naive_hedge": "Hedge Ingênuo 1:1",
        "irs_inputs": "Termos do Swap",
        "irs_not": "Nocional",
        "irs_tenor": "Prazo (anos)",
        "irs_freq": "Frequência de Pagamento",
        "irs_fixed": "Taxa Fixa (% a.a.)",
        "irs_index": "Índice Flutuante",
        "irs_spread": "Spread Flutuante (bps)",
        "irs_position": "Posição",
        "pay_fixed": "Paga Fixo",
        "rec_fixed": "Recebe Fixo",
        "irs_dcb": "Base Day Count",
        "curve_input": "Input da Curva de Juros",
        "par_rate": "Taxa Par do Swap",
        "swap_pv": "PV do Swap",
        "dv01": "DV01",
        "annuity": "Fator de Anuidade",
        "cf_table": "Fluxos de Caixa",
        "curve_viz": "Curva de Juros",
        "sensitivity": "Sensibilidade do PV",
        "ccs_inputs": "Parâmetros CCS",
        "ccy1": "Moeda 1",
        "ccy2": "Moeda 2",
        "ccs_spot": "Taxa Spot",
        "ccs_type": "Tipo de Swap",
        "ff": "Fixo-Fixo",
        "fflt": "Fixo-Flutuante",
        "fltflt": "Flutuante-Flutuante",
        "not_exch": "Troca de Nocional",
        "mtm": "MTM (rebalanceado)",
        "nonmtm": "Non-MTM",
        "basis_sp": "Basis Spread (bps)",
        "not_c1": "Nocional Moeda 1",
        "not_c2": "Nocional Moeda 2",
        "all_in": "Custo All-in (base)",
        "trs_inputs": "Parâmetros TRS",
        "under_type": "Tipo de Ativo",
        "under_name": "Nome do Ativo",
        "ref_price": "Preço de Referência Inicial",
        "trs_position": "Posição",
        "tr_rec": "Recebedor TR (Long)",
        "tr_pay": "Pagador TR (Short)",
        "fin_idx": "Índice de Financiamento",
        "fin_sp": "Spread Financiamento (bps)",
        "trs_tenor": "Prazo (meses)",
        "div_yld": "Dividendos/Cupons Esperados (% por período)",
        "collateral": "Colateral Inicial (% do nocional)",
        "leverage": "Alavancagem",
        "fin_cost": "Custo de Financiamento",
        "exp_return": "Retorno Esperado",
        "port_val": "Valor do Portfólio",
        "asset_class": "Classe de Ativo",
        "beta": "Beta ao Mercado",
        "duration": "Duration (anos)",
        "fx_exp": "Exposição FX",
        "hedge_instr": "Instrumento de Hedge",
        "hedge_ratio": "Hedge Ratio (%)",
        "var_red": "Redução de Variância",
        "eff_ratio": "Razão de Efetividade",
        "var_unh": "VaR Sem Hedge (95%)",
        "var_h": "VaR Com Hedge (95%)",
        "recommend": "Recomendação",
        "eff_hedge": "Hedge Efetivo (qualifica para hedge accounting)",
        "partial_hedge": "Hedge Parcial",
        "ineff_hedge": "Hedge Inefetivo",
    },
}

# =============================================================================
# LANGUAGE HELPERS
# =============================================================================
if "hg_lang" not in st.session_state:
    st.session_state["hg_lang"] = "en"


def T(key: str) -> str:
    lang = st.session_state.get("hg_lang", "en")
    return _L.get(lang, _L["en"]).get(key, key)


# =============================================================================
# UTILITIES
# =============================================================================
def fmt_money(x: float, ccy: str = "USD", decimals: int = 2) -> str:
    try:
        sign = "-" if x < 0 else ""
        x = abs(x)
        return f"{sign}{ccy} {x:,.{decimals}f}"
    except Exception:
        return f"{ccy} 0.00"


def fmt_pct(x: float, decimals: int = 2) -> str:
    try:
        return f"{x*100:,.{decimals}f}%"
    except Exception:
        return "0.00%"


def fmt_num(x: float, decimals: int = 4) -> str:
    try:
        return f"{x:,.{decimals}f}"
    except Exception:
        return "0.0000"


def metric_card(label: str, value: str, delta: str = "", delta_pos: bool = True):
    delta_class = "metric-delta-pos" if delta_pos else "metric-delta-neg"
    delta_html = (
        f'<div class="{delta_class}">{delta}</div>' if delta else ""
    )
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def info_box(text: str):
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def warning_box(text: str):
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)


def success_box(text: str):
    st.markdown(f'<div class="success-box">{text}</div>', unsafe_allow_html=True)


def formula_box(text: str):
    st.markdown(f'<div class="formula-box">{text}</div>', unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================
col_title, col_lang, col_dark = st.columns([5, 1, 1])
with col_title:
    st.markdown(f'<div class="main-title">{T("title")}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtitle">{T("subtitle")}</div>', unsafe_allow_html=True
    )
with col_lang:
    lang_choice = st.selectbox(
        T("language"),
        options=["en", "pt"],
        index=0 if st.session_state["hg_lang"] == "en" else 1,
        format_func=lambda x: "English" if x == "en" else "Português",
        key="hg_lang_select",
    )
    if lang_choice != st.session_state["hg_lang"]:
        st.session_state["hg_lang"] = lang_choice
        st.rerun()
with col_dark:
    st.write("")
    dark_mode = st.toggle("\U0001f319", key="hg_dark_mode", help="Dark Mode")

# ── Dark mode CSS override ──────────────────────────────────────────────────
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
.main-title{color:#60a5fa !important}
.subtitle{color:#94a3b8 !important}
.section-header{color:#93c5fd !important;border-color:#60a5fa !important}
.metric-card{background:linear-gradient(135deg,#1e293b,#1e3a5f) !important;border-color:#334155 !important;border-left-color:#1a56db !important}
.metric-label{color:#94a3b8 !important}
.metric-value{color:#e2e8f0 !important}
.info-box{background:#1e3a5f !important;color:#e2e8f0 !important;border-left-color:#60a5fa !important}
.warning-box{background:#78350f !important;color:#fcd34d !important;border-left-color:#f59e0b !important}
.success-box{background:#064e3b !important;color:#6ee7b7 !important;border-left-color:#10b981 !important}
.formula-box{background:#1e293b !important;color:#cbd5e1 !important;border-color:#475569 !important}
hr{border-color:#334155 !important}
</style>""", unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# TABS
# =============================================================================
_hg_icons = ["\U0001f4b1", "\U0001f4c8", "\U0001f4ca", "\U0001f30d", "\U0001f504", "\U0001f6e1"]
_hg_names = [T("tab_fwd"), T("tab_fut"), T("tab_irs"),
             T("tab_ccs"), T("tab_trs"), T("tab_eff")]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [f"{i}  {n}" for i, n in zip(_hg_icons, _hg_names)]
)

# =============================================================================
# TAB 1 — FX FORWARD
# =============================================================================
with tab1:
    section_header(T("tab_fwd") + " — Covered Interest Rate Parity")

    with st.expander("About FX Forward / Sobre o Contrato a Termo de Moedas", expanded=False):
        st.markdown(
            """
            **Covered Interest Rate Parity (CIRP)** ensures that forward FX rates
            reflect the interest rate differential between two currencies. Any
            deviation would create arbitrage opportunities.

            **Formula:**
            """
        )
        formula_box("F = S × (1 + rd × d/basis) / (1 + rf × d/basis)")
        st.markdown(
            """
            Where:
            - **F** = Forward rate (units of domestic per 1 unit foreign)
            - **S** = Spot rate
            - **rd** = Domestic interest rate (annualized)
            - **rf** = Foreign interest rate (annualized)
            - **d** = Days to maturity
            - **basis** = 360 or 365 depending on day-count convention

            If **rd > rf**, forward is at a **premium** (F > S).
            If **rd < rf**, forward is at a **discount** (F < S).
            """
        )

    col_in, col_out = st.columns([1, 2])

    with col_in:
        st.markdown(f"**{T('fx_inputs')}**")
        pair_options = ["USD/BRL", "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "EUR/BRL"]
        default_spots = {
            "USD/BRL": 5.05,
            "EUR/USD": 1.0850,
            "USD/JPY": 148.50,
            "GBP/USD": 1.2650,
            "USD/CHF": 0.8850,
            "EUR/BRL": 5.48,
        }
        default_rd = {
            "USD/BRL": 11.25,
            "EUR/USD": 5.25,
            "USD/JPY": 5.25,
            "GBP/USD": 5.00,
            "USD/CHF": 5.25,
            "EUR/BRL": 11.25,
        }
        default_rf = {
            "USD/BRL": 5.25,
            "EUR/USD": 4.00,
            "USD/JPY": 0.10,
            "GBP/USD": 5.25,
            "USD/CHF": 1.50,
            "EUR/BRL": 4.00,
        }

        pair = st.selectbox(T("fx_pair"), pair_options, index=0, key="hg_fx_pair")
        S = st.number_input(
            T("fx_spot"),
            value=float(default_spots[pair]),
            step=0.0001,
            format="%.4f",
            key="hg_fx_spot",
        )
        rd_pct = st.number_input(
            T("fx_rd"),
            value=float(default_rd[pair]),
            step=0.05,
            format="%.2f",
            key="hg_fx_rd",
        )
        rf_pct = st.number_input(
            T("fx_rf"),
            value=float(default_rf[pair]),
            step=0.05,
            format="%.2f",
            key="hg_fx_rf",
        )
        d_opts = [30, 60, 90, 180, 360]
        d = st.selectbox(T("fx_tenor"), d_opts, index=2, key="hg_fx_d")
        basis_choice = st.selectbox(
            T("fx_basis"), ["ACT/360", "ACT/365"], index=0, key="hg_fx_basis"
        )
        basis = 360.0 if basis_choice == "ACT/360" else 365.0
        notional = st.number_input(
            T("fx_notional"),
            value=1_000_000.0,
            step=10_000.0,
            format="%.2f",
            key="hg_fx_notional",
        )
        direction = st.radio(
            T("fx_direction"),
            [T("buy_fwd"), T("sell_fwd")],
            index=0,
            horizontal=True,
            key="hg_fx_dir",
        )

    # --- Calculations ---
    rd = rd_pct / 100.0
    rf = rf_pct / 100.0
    F = S * (1 + rd * d / basis) / (1 + rf * d / basis)
    fwd_points_pips = (F - S) * 10000.0
    ann_premium = ((F / S) - 1.0) * (360.0 / d) if d > 0 else 0.0
    cost_hedge_domestic = notional * (F - S)  # cost/benefit in domestic vs spot

    with col_out:
        st.markdown(f"**{T('fx_results')}**")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(T("fwd_rate"), fmt_num(F, 4))
        with m2:
            metric_card(T("fwd_points"), fmt_num(fwd_points_pips, 2))
        with m3:
            metric_card(T("ann_prem"), fmt_pct(ann_premium, 3))
        with m4:
            is_cost = cost_hedge_domestic > 0
            metric_card(
                T("cost_hedge"),
                fmt_money(cost_hedge_domestic, "", 2),
                delta=("Premium" if is_cost else "Discount"),
                delta_pos=not is_cost,
            )

        # Scenario analysis
        scenarios = np.linspace(-0.20, 0.20, 9)
        rows = []
        is_buy = direction == T("buy_fwd")
        for sc in scenarios:
            spot_mat = S * (1 + sc)
            if is_buy:
                unh = notional * (S - spot_mat)  # short exposure unhedged
                hed = notional * (S - F)
            else:
                unh = notional * (spot_mat - S)
                hed = notional * (F - S)
            benefit = hed - unh
            rows.append(
                {
                    T("spot_at_mat"): round(spot_mat, 4),
                    "Δ Spot": f"{sc*100:+.0f}%",
                    T("unhedged_pnl"): round(unh, 2),
                    T("hedged_pnl"): round(hed, 2),
                    T("hedge_benefit"): round(benefit, 2),
                }
            )
        df_sc = pd.DataFrame(rows)

        st.markdown(f"**{T('pnl_scenario')}**")
        fig_fx = go.Figure()
        fig_fx.add_trace(
            go.Scatter(
                x=df_sc[T("spot_at_mat")],
                y=df_sc[T("unhedged_pnl")],
                mode="lines+markers",
                name=T("unhedged_pnl"),
                line=dict(color=ACCENT_RED, width=3),
                marker=dict(size=8),
            )
        )
        fig_fx.add_trace(
            go.Scatter(
                x=df_sc[T("spot_at_mat")],
                y=df_sc[T("hedged_pnl")],
                mode="lines+markers",
                name=T("hedged_pnl"),
                line=dict(color=PRIMARY, width=3),
                marker=dict(size=8),
            )
        )
        fig_fx.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
        fig_fx.add_vline(
            x=F, line_dash="dot", line_color=ACCENT_GREEN,
            annotation_text=f"Forward = {F:.4f}",
        )
        fig_fx.update_layout(
            height=380,
            xaxis_title=T("spot_at_mat"),
            yaxis_title="P&L",
            hovermode="x unified",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        fig_fx.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        fig_fx.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_fx, use_container_width=True)

    st.markdown(f"**{T('scenario_tbl')}**")
    st.dataframe(df_sc, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 2 — FX FUTURES
# =============================================================================
with tab2:
    section_header(T("tab_fut") + " — Minimum Variance Hedge (Ederington)")

    with st.expander("About FX Futures & Optimal Hedge Ratio", expanded=False):
        st.markdown(
            """
            **Optimal (Minimum Variance) Hedge Ratio** from Ederington (1979):
            """
        )
        formula_box("h* = ρ × (σS / σF)")
        st.markdown(
            """
            Where:
            - **ρ** = correlation between spot and futures returns
            - **σS** = standard deviation of spot returns
            - **σF** = standard deviation of futures returns

            Number of contracts: **N = h\\* × (Portfolio Value / Contract Notional)**.

            **CME Contract Specifications:**
            - **6L** (BRL/USD futures): BRL 100,000
            - **6E** (EUR/USD futures): EUR 125,000
            - **6J** (JPY/USD futures): JPY 12,500,000
            - **6B** (GBP/USD futures): GBP 62,500
            """
        )

    contract_specs = {
        "6L — BRL/USD": {"size": 100_000, "ccy": "BRL", "default_price": 0.1980, "margin": 2_500},
        "6E — EUR/USD": {"size": 125_000, "ccy": "EUR", "default_price": 1.0855, "margin": 3_000},
        "6J — JPY/USD": {"size": 12_500_000, "ccy": "JPY", "default_price": 0.006730, "margin": 3_500},
        "6B — GBP/USD": {"size": 62_500, "ccy": "GBP", "default_price": 1.2650, "margin": 2_800},
    }

    col_ft_in, col_ft_out = st.columns([1, 2])

    with col_ft_in:
        st.markdown(f"**{T('fut_inputs')}**")
        ft_contract = st.selectbox(
            T("fut_contract"),
            list(contract_specs.keys()),
            index=0,
            key="hg_ft_contract",
        )
        spec = contract_specs[ft_contract]
        ft_size = st.number_input(
            T("fut_size"),
            value=float(spec["size"]),
            step=1000.0,
            format="%.2f",
            key="hg_ft_size",
            disabled=True,
        )
        ft_num = st.number_input(
            T("fut_num"), value=10, step=1, min_value=1, key="hg_ft_num"
        )
        ft_entry = st.number_input(
            T("fut_entry"),
            value=float(spec["default_price"]),
            step=0.0001,
            format="%.6f",
            key="hg_ft_entry",
        )
        ft_margin = st.number_input(
            T("fut_margin"),
            value=float(spec["margin"]),
            step=100.0,
            format="%.2f",
            key="hg_ft_margin",
        )
        ft_current = st.number_input(
            T("fut_current"),
            value=float(spec["default_price"]) * 1.015,
            step=0.0001,
            format="%.6f",
            key="hg_ft_current",
        )
        ft_dte = st.number_input(
            T("fut_dte"), value=60, step=1, min_value=1, key="hg_ft_dte"
        )
        ft_port = st.number_input(
            T("fut_port"),
            value=5_000_000.0,
            step=100_000.0,
            format="%.2f",
            key="hg_ft_port",
        )

        st.markdown(f"**{T('hedge_params')}**")
        sigma_s = st.slider(
            T("sigma_s"), min_value=1.0, max_value=50.0, value=15.0, step=0.5, key="hg_ft_ss"
        )
        sigma_f = st.slider(
            T("sigma_f"), min_value=1.0, max_value=50.0, value=14.5, step=0.5, key="hg_ft_sf"
        )
        rho = st.slider(
            T("correl"), min_value=-1.0, max_value=1.0, value=0.92, step=0.01, key="hg_ft_rho"
        )

    # Calculations
    contract_notional_usd = ft_size * ft_entry
    notional_hedged_total = ft_num * contract_notional_usd
    h_star = rho * (sigma_s / sigma_f) if sigma_f > 0 else 0.0
    optimal_num_contracts = (
        (h_star * ft_port / contract_notional_usd) if contract_notional_usd > 0 else 0.0
    )
    mtm_pnl = ft_num * (ft_current - ft_entry) * ft_size
    margin_total = ft_num * ft_margin
    basis = ft_current - ft_entry  # simplification: proxy for basis
    naive_contracts = ft_port / contract_notional_usd if contract_notional_usd > 0 else 0.0

    with col_ft_out:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            metric_card(T("notional_hedged"), fmt_money(notional_hedged_total, "USD", 0))
        with m2:
            metric_card(T("opt_hr"), f"{h_star:.4f}")
        with m3:
            metric_card(T("num_contracts"), f"{optimal_num_contracts:.1f}")
        with m4:
            metric_card(T("margin_req"), fmt_money(margin_total, "USD", 0))
        with m5:
            metric_card(
                T("mtm_pnl"),
                fmt_money(mtm_pnl, "USD", 0),
                delta=("Profit" if mtm_pnl >= 0 else "Loss"),
                delta_pos=(mtm_pnl >= 0),
            )

        # P&L chart at expiry
        price_range = np.linspace(ft_entry * 0.85, ft_entry * 1.15, 50)
        pnl_futures = ft_num * (price_range - ft_entry) * ft_size

        fig_ft = go.Figure()
        fig_ft.add_trace(
            go.Scatter(
                x=price_range,
                y=pnl_futures,
                mode="lines",
                name="Futures P&L",
                line=dict(color=PRIMARY, width=3),
                fill="tozeroy",
                fillcolor="rgba(26, 86, 219, 0.1)",
            )
        )
        fig_ft.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
        fig_ft.add_vline(
            x=ft_entry,
            line_dash="dot",
            line_color=ACCENT_GREEN,
            annotation_text=f"Entry = {ft_entry:.4f}",
        )
        fig_ft.add_vline(
            x=ft_current,
            line_dash="dot",
            line_color=ACCENT_AMBER,
            annotation_text=f"Current = {ft_current:.4f}",
        )
        fig_ft.update_layout(
            height=340,
            xaxis_title="Futures Price",
            yaxis_title="P&L (USD)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=10),
        )
        fig_ft.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        fig_ft.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_ft, use_container_width=True)

        st.markdown(f"**{T('min_var')} vs {T('naive_hedge')}**")
        comp_df = pd.DataFrame(
            {
                "Strategy": [T("min_var"), T("naive_hedge")],
                "Hedge Ratio": [f"{h_star:.4f}", "1.0000"],
                "Contracts": [
                    f"{optimal_num_contracts:.2f}",
                    f"{naive_contracts:.2f}",
                ],
                "Variance Reduction": [
                    f"{(rho**2)*100:.1f}%",
                    f"{max(0, (2*rho*(sigma_s/sigma_f) - (sigma_s/sigma_f)**2))*100:.1f}%",
                ],
                "Basis Risk": [
                    fmt_money(basis * ft_size * optimal_num_contracts, "USD", 0),
                    fmt_money(basis * ft_size * naive_contracts, "USD", 0),
                ],
            }
        )
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    info_box(
        f"<b>{T('basis_risk')}:</b> {basis:.6f} "
        f"(spot − futures). Contract notional: USD {contract_notional_usd:,.2f}. "
        f"Variance reduction (optimal): {(rho**2)*100:.1f}%"
    )

# =============================================================================
# TAB 3 — INTEREST RATE SWAP
# =============================================================================
with tab3:
    section_header(T("tab_irs") + " — Multi-Curve Framework")

    with st.expander("About IRS / Sobre o Swap de Juros", expanded=False):
        st.markdown(
            """
            **Interest Rate Swap (IRS)** — An OTC derivative where two parties
            exchange cash flows, typically a fixed rate against a floating rate
            (SOFR, EURIBOR, SONIA, CDI, etc.), based on a notional amount.

            **Par Swap Rate** (multi-curve framework):
            """
        )
        formula_box("S = Σ(f_j × d_j × DF_j) / Σ(d_i × DF_i)")
        st.markdown(
            """
            - **f_j** = forward rate for period j
            - **d_j** = day count fraction
            - **DF_j** = discount factor at period j (from OIS curve post-2008)

            **DV01** (Dollar Value of 01): sensitivity of swap PV to a 1bp parallel
            shift in the yield curve. Central to hedging bond portfolio duration risk.
            """
        )

    col_irs_in, col_irs_out = st.columns([1, 2])

    with col_irs_in:
        st.markdown(f"**{T('irs_inputs')}**")
        irs_not = st.number_input(
            T("irs_not"),
            value=10_000_000.0,
            step=1_000_000.0,
            format="%.2f",
            key="hg_irs_not",
        )
        irs_tenor = st.number_input(
            T("irs_tenor"),
            value=5,
            min_value=1,
            max_value=30,
            step=1,
            key="hg_irs_tenor",
        )
        freq_map = {"Monthly": 12, "Quarterly": 4, "Semi-annual": 2, "Annual": 1}
        irs_freq = st.selectbox(
            T("irs_freq"),
            list(freq_map.keys()),
            index=1,
            key="hg_irs_freq",
        )
        freq_n = freq_map[irs_freq]
        irs_fixed = st.number_input(
            T("irs_fixed"),
            value=4.50,
            step=0.05,
            format="%.3f",
            key="hg_irs_fixed",
        )
        irs_index = st.selectbox(
            T("irs_index"),
            ["SOFR", "CDI", "Selic", "EURIBOR", "SONIA"],
            index=0,
            key="hg_irs_index",
        )
        irs_spread = st.number_input(
            T("irs_spread"), value=25.0, step=5.0, format="%.1f", key="hg_irs_spread"
        )
        irs_pos = st.radio(
            T("irs_position"),
            [T("pay_fixed"), T("rec_fixed")],
            index=0,
            horizontal=True,
            key="hg_irs_pos",
        )
        irs_dcb = st.selectbox(
            T("irs_dcb"),
            ["30/360", "ACT/360", "ACT/365"],
            index=0,
            key="hg_irs_dcb",
        )

        st.markdown(f"**{T('curve_input')}**")
        tenors_yrs = [1 / 12, 3 / 12, 6 / 12, 1.0, 2.0, 5.0, 10.0]
        tenors_labels = ["1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y"]
        default_rates = [4.75, 4.80, 4.85, 4.70, 4.55, 4.50, 4.65]
        curve_rates = []
        for i, (lbl, dr) in enumerate(zip(tenors_labels, default_rates)):
            val = st.number_input(
                f"{lbl}",
                value=float(dr),
                step=0.05,
                format="%.3f",
                key=f"hg_irs_curve_{i}",
            )
            curve_rates.append(val / 100.0)

    # ---- Curve Bootstrapping ----
    def discount_factor_from_curve(t: float, curve_t, curve_r) -> float:
        """Simple linear interpolation on zero rates, then DF = 1/(1+r*t)."""
        if t <= curve_t[0]:
            r = curve_r[0]
        elif t >= curve_t[-1]:
            r = curve_r[-1]
        else:
            for i in range(len(curve_t) - 1):
                if curve_t[i] <= t <= curve_t[i + 1]:
                    w = (t - curve_t[i]) / (curve_t[i + 1] - curve_t[i])
                    r = curve_r[i] * (1 - w) + curve_r[i + 1] * w
                    break
        return 1.0 / (1.0 + r * t)

    dcb_map = {"30/360": 360.0, "ACT/360": 360.0, "ACT/365": 365.0}
    dcb_denom = dcb_map[irs_dcb]

    n_periods = int(irs_tenor * freq_n)
    period_frac = 1.0 / freq_n  # year fraction per period

    times = [period_frac * (i + 1) for i in range(n_periods)]
    dfs = [discount_factor_from_curve(t, tenors_yrs, curve_rates) for t in times]

    # Forward rates
    fwd_rates = []
    for i, t in enumerate(times):
        if i == 0:
            df_prev = 1.0
            t_prev = 0.0
        else:
            df_prev = dfs[i - 1]
            t_prev = times[i - 1]
        f = (df_prev / dfs[i] - 1.0) / (t - t_prev) if (t - t_prev) > 0 else 0.0
        fwd_rates.append(f)

    # Annuity
    annuity = sum(period_frac * df for df in dfs)
    # Par rate
    par_rate = sum(f * period_frac * df for f, df in zip(fwd_rates, dfs)) / annuity if annuity > 0 else 0.0

    # Fixed and floating leg PVs
    R = irs_fixed / 100.0
    spread_dec = irs_spread / 10000.0
    pv_fixed = irs_not * R * annuity
    pv_float = irs_not * sum(
        (f + spread_dec) * period_frac * df for f, df in zip(fwd_rates, dfs)
    )

    if irs_pos == T("pay_fixed"):
        swap_pv = pv_float - pv_fixed
    else:
        swap_pv = pv_fixed - pv_float

    # DV01: shift curve +1bp
    bump = 0.0001
    curve_rates_up = [r + bump for r in curve_rates]
    curve_rates_dn = [r - bump for r in curve_rates]
    dfs_up = [discount_factor_from_curve(t, tenors_yrs, curve_rates_up) for t in times]
    dfs_dn = [discount_factor_from_curve(t, tenors_yrs, curve_rates_dn) for t in times]

    fwd_up = []
    fwd_dn = []
    for i, t in enumerate(times):
        t_prev = 0.0 if i == 0 else times[i - 1]
        df_prev_up = 1.0 if i == 0 else dfs_up[i - 1]
        df_prev_dn = 1.0 if i == 0 else dfs_dn[i - 1]
        fwd_up.append((df_prev_up / dfs_up[i] - 1.0) / (t - t_prev) if (t - t_prev) > 0 else 0.0)
        fwd_dn.append((df_prev_dn / dfs_dn[i] - 1.0) / (t - t_prev) if (t - t_prev) > 0 else 0.0)

    annuity_up = sum(period_frac * df for df in dfs_up)
    annuity_dn = sum(period_frac * df for df in dfs_dn)
    pv_fixed_up = irs_not * R * annuity_up
    pv_fixed_dn = irs_not * R * annuity_dn
    pv_float_up = irs_not * sum((f + spread_dec) * period_frac * df for f, df in zip(fwd_up, dfs_up))
    pv_float_dn = irs_not * sum((f + spread_dec) * period_frac * df for f, df in zip(fwd_dn, dfs_dn))

    if irs_pos == T("pay_fixed"):
        swap_pv_up = pv_float_up - pv_fixed_up
        swap_pv_dn = pv_float_dn - pv_fixed_dn
    else:
        swap_pv_up = pv_fixed_up - pv_float_up
        swap_pv_dn = pv_fixed_dn - pv_float_dn

    dv01 = (swap_pv_dn - swap_pv_up) / 2.0  # average sensitivity per 1bp

    with col_irs_out:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(T("par_rate"), fmt_pct(par_rate, 3))
        with m2:
            metric_card(
                T("swap_pv"),
                fmt_money(swap_pv, "", 0),
                delta=("ITM" if swap_pv > 0 else "OTM"),
                delta_pos=(swap_pv > 0),
            )
        with m3:
            metric_card(T("dv01"), fmt_money(dv01, "", 2))
        with m4:
            metric_card(T("annuity"), f"{annuity:.4f}")

        # Cash Flow Table
        cf_rows = []
        for i, (t, df, fwd) in enumerate(zip(times, dfs, fwd_rates)):
            fixed_cf = irs_not * R * period_frac
            float_cf = irs_not * (fwd + spread_dec) * period_frac
            net_cf = (float_cf - fixed_cf) if irs_pos == T("pay_fixed") else (fixed_cf - float_cf)
            cf_rows.append(
                {
                    "Period": i + 1,
                    "Time (y)": round(t, 3),
                    "DF": round(df, 6),
                    "Fwd Rate": f"{fwd*100:.3f}%",
                    "Fixed CF": round(fixed_cf, 2),
                    "Float CF": round(float_cf, 2),
                    "Net CF": round(net_cf, 2),
                    "PV Net": round(net_cf * df, 2),
                }
            )
        cf_df = pd.DataFrame(cf_rows)

        tab_cf, tab_curve, tab_sens = st.tabs(
            [T("cf_table"), T("curve_viz"), T("sensitivity")]
        )

        with tab_cf:
            st.dataframe(cf_df, use_container_width=True, hide_index=True, height=280)

        with tab_curve:
            fig_curve = go.Figure()
            fig_curve.add_trace(
                go.Scatter(
                    x=tenors_yrs,
                    y=[r * 100 for r in curve_rates],
                    mode="lines+markers",
                    name="Yield Curve",
                    line=dict(color=PRIMARY, width=3),
                    marker=dict(size=10),
                )
            )
            fig_curve.add_hline(
                y=par_rate * 100,
                line_dash="dash",
                line_color=ACCENT_GREEN,
                annotation_text=f"Par Rate = {par_rate*100:.3f}%",
            )
            fig_curve.update_layout(
                height=330,
                xaxis_title="Tenor (years)",
                yaxis_title="Rate (%)",
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=20, b=10),
            )
            fig_curve.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
            fig_curve.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig_curve, use_container_width=True)

        with tab_sens:
            shifts = np.arange(-200, 210, 10)
            sens_pvs = []
            for sh in shifts:
                bp = sh / 10000.0
                cr_s = [r + bp for r in curve_rates]
                dfs_s = [discount_factor_from_curve(t, tenors_yrs, cr_s) for t in times]
                fwd_s = []
                for i, t in enumerate(times):
                    t_prev = 0.0 if i == 0 else times[i - 1]
                    df_prev = 1.0 if i == 0 else dfs_s[i - 1]
                    fwd_s.append((df_prev / dfs_s[i] - 1.0) / (t - t_prev) if (t - t_prev) > 0 else 0.0)
                ann_s = sum(period_frac * df for df in dfs_s)
                pv_fx_s = irs_not * R * ann_s
                pv_fl_s = irs_not * sum(
                    (f + spread_dec) * period_frac * df for f, df in zip(fwd_s, dfs_s)
                )
                if irs_pos == T("pay_fixed"):
                    sens_pvs.append(pv_fl_s - pv_fx_s)
                else:
                    sens_pvs.append(pv_fx_s - pv_fl_s)

            fig_sens = go.Figure()
            fig_sens.add_trace(
                go.Scatter(
                    x=shifts,
                    y=sens_pvs,
                    mode="lines",
                    name="Swap PV",
                    line=dict(color=PRIMARY, width=3),
                    fill="tozeroy",
                    fillcolor="rgba(26, 86, 219, 0.12)",
                )
            )
            fig_sens.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
            fig_sens.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
            fig_sens.update_layout(
                height=330,
                xaxis_title="Parallel Shift (bps)",
                yaxis_title="Swap PV",
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=20, b=10),
            )
            fig_sens.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
            fig_sens.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig_sens, use_container_width=True)

# =============================================================================
# TAB 4 — CROSS-CURRENCY SWAP
# =============================================================================
with tab4:
    section_header(T("tab_ccs") + " — Multi-Currency Funding")

    with st.expander("About CCS / Sobre o Swap Cambial", expanded=False):
        st.markdown(
            """
            **Cross-Currency Swap (CCS)** — Exchange of principal and interest
            in one currency for principal and interest in another. Used by
            corporates issuing debt in foreign currency and seeking to hedge
            FX and rate risk.

            **Typical use case:** A Brazilian company issues USD 100M bond at
            6% and swaps it to BRL to match its revenues. The counterparty
            pays USD 6% and the company pays CDI + spread in BRL.

            Key concepts:
            - **Initial notional exchange** at spot rate
            - **Periodic interest payments** in both currencies
            - **Final notional re-exchange** at original spot (Non-MTM) or
              rebalanced to current spot (MTM)
            - **Cross-currency basis spread** reflects supply/demand for
              USD funding in FX markets
            """
        )

    col_ccs_in, col_ccs_out = st.columns([1, 2])

    with col_ccs_in:
        st.markdown(f"**{T('ccs_inputs')}**")
        c1 = st.selectbox(T("ccy1"), ["USD", "EUR", "BRL", "GBP", "JPY"], index=0, key="hg_ccs_c1")
        c2 = st.selectbox(T("ccy2"), ["BRL", "USD", "EUR", "GBP", "JPY"], index=0, key="hg_ccs_c2")
        ccs_not1 = st.number_input(
            f"{T('not_c1')} ({c1})",
            value=100_000_000.0,
            step=1_000_000.0,
            format="%.2f",
            key="hg_ccs_not1",
        )
        ccs_spot = st.number_input(
            T("ccs_spot"),
            value=5.05,
            step=0.01,
            format="%.4f",
            key="hg_ccs_spot",
        )
        ccs_not2 = ccs_not1 * ccs_spot
        st.info(f"{T('not_c2')} ({c2}): {ccs_not2:,.2f}")

        ccs_tenor = st.number_input(
            "Tenor (years)", value=5, min_value=1, max_value=30, step=1, key="hg_ccs_tenor"
        )
        ccs_freq_lbl = st.selectbox(
            "Frequency", ["Quarterly", "Semi-annual", "Annual"], index=1, key="hg_ccs_freq"
        )
        ccs_freq_map = {"Quarterly": 4, "Semi-annual": 2, "Annual": 1}
        ccs_freq_n = ccs_freq_map[ccs_freq_lbl]

        ccs_type = st.radio(
            T("ccs_type"), [T("ff"), T("fflt"), T("fltflt")], index=0, horizontal=True, key="hg_ccs_type"
        )

        ccs_r1 = st.number_input(
            f"Rate {c1} (% p.a.)", value=5.50, step=0.05, format="%.3f", key="hg_ccs_r1"
        )
        ccs_r2 = st.number_input(
            f"Rate {c2} (% p.a.)", value=11.25, step=0.05, format="%.3f", key="hg_ccs_r2"
        )
        ccs_basis_sp = st.number_input(
            T("basis_sp"), value=-35.0, step=5.0, format="%.1f", key="hg_ccs_bsp"
        )
        ccs_not_exch = st.radio(
            T("not_exch"), [T("nonmtm"), T("mtm")], index=0, horizontal=True, key="hg_ccs_exch"
        )

    # Calculations
    n_cp = int(ccs_tenor * ccs_freq_n)
    period = 1.0 / ccs_freq_n
    r1 = ccs_r1 / 100.0
    r2 = (ccs_r2 + ccs_basis_sp / 100.0) / 100.0  # add basis spread to leg2

    cf_rows_ccs = []
    cumulative_base = -ccs_not1  # initial exchange: pay C1, receive C2
    cumulative_base += 0  # base is C1

    # Initial exchange
    cf_rows_ccs.append(
        {
            "Period": 0,
            "Time": 0.0,
            f"CF {c1}": -ccs_not1,
            f"CF {c2}": ccs_not2,
            f"Net ({c1})": -ccs_not1 + ccs_not2 / ccs_spot,
        }
    )

    for i in range(1, n_cp + 1):
        t = i * period
        int1 = -ccs_not1 * r1 * period  # pay interest on C1 leg
        int2 = ccs_not2 * r2 * period  # receive interest on C2 leg

        principal1 = 0.0
        principal2 = 0.0
        if i == n_cp:
            principal1 = ccs_not1  # receive back C1 principal
            principal2 = -ccs_not2  # pay back C2 principal

        cf1 = int1 + principal1
        cf2 = int2 + principal2
        # translate C2 to C1 at spot (simplification)
        net_base = cf1 + cf2 / ccs_spot
        cf_rows_ccs.append(
            {
                "Period": i,
                "Time": round(t, 3),
                f"CF {c1}": round(cf1, 2),
                f"CF {c2}": round(cf2, 2),
                f"Net ({c1})": round(net_base, 2),
            }
        )

    ccs_df = pd.DataFrame(cf_rows_ccs)

    # All-in cost (IRR approximation): sum of C1 interest / notional
    total_int1 = ccs_not1 * r1 * ccs_tenor
    all_in = r1 + (ccs_basis_sp / 10000.0) * (ccs_not2 / ccs_not1 / ccs_spot)
    all_in_simple = r1 + (ccs_basis_sp / 10000.0)

    # Cumulative base cash flow
    cum_vals = np.cumsum(ccs_df[f"Net ({c1})"].values)

    with col_ccs_out:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(T("not_c1"), fmt_money(ccs_not1, c1, 0))
        with m2:
            metric_card(T("not_c2"), fmt_money(ccs_not2, c2, 0))
        with m3:
            metric_card(T("basis_sp"), f"{ccs_basis_sp:+.1f} bps")
        with m4:
            metric_card(T("all_in"), fmt_pct(all_in_simple, 3))

        st.markdown(f"**{T('cf_table')}**")
        st.dataframe(ccs_df, use_container_width=True, hide_index=True, height=280)

        # Cumulative cash flow chart
        fig_ccs = go.Figure()
        fig_ccs.add_trace(
            go.Bar(
                x=ccs_df["Period"],
                y=ccs_df[f"Net ({c1})"],
                name=f"Period CF ({c1})",
                marker_color=PRIMARY,
            )
        )
        fig_ccs.add_trace(
            go.Scatter(
                x=ccs_df["Period"],
                y=cum_vals,
                mode="lines+markers",
                name=f"Cumulative ({c1})",
                line=dict(color=ACCENT_GREEN, width=3),
                yaxis="y2",
            )
        )
        fig_ccs.update_layout(
            height=340,
            xaxis_title="Period",
            yaxis=dict(title=f"Period CF ({c1})"),
            yaxis2=dict(title=f"Cumulative ({c1})", overlaying="y", side="right"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        fig_ccs.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_ccs, use_container_width=True)

    info_box(
        f"<b>Use Case:</b> Brazilian corporate issues {c1} {ccs_not1/1e6:.0f}M bond at "
        f"{ccs_r1:.2f}% and swaps to {c2} at {ccs_r2:.2f}% + {ccs_basis_sp:.0f}bp basis. "
        f"Effective {c1} cost: {all_in_simple*100:.3f}%."
    )

# =============================================================================
# TAB 5 — TOTAL RETURN SWAP
# =============================================================================
with tab5:
    section_header(T("tab_trs") + " — Synthetic Leverage & Capital Efficiency")

    with st.expander("About TRS / Sobre o Total Return Swap", expanded=False):
        st.markdown(
            """
            **Total Return Swap (TRS)** — The TR Receiver gets the total return
            (price appreciation + dividends) of a reference asset and pays a
            financing leg (usually floating rate + spread). The TR Payer has
            the opposite exposure.

            **Key advantage: Leverage & Capital Efficiency** — Investor gains
            economic exposure to the underlying without full capital outlay,
            posting only initial collateral (5-25% typically).

            **P&L (TR Receiver):**
            """
        )
        formula_box("P&L = (P_end − P_start)/P_start × N + D − (idx + spread) × N × t")
        st.markdown(
            """
            Where N = notional, D = dividends received, idx + spread =
            financing rate, t = time fraction.

            Used by hedge funds, banks (synthetic prime brokerage), and to
            gain exposure to illiquid / restricted assets.
            """
        )

    col_trs_in, col_trs_out = st.columns([1, 2])

    with col_trs_in:
        st.markdown(f"**{T('trs_inputs')}**")
        trs_type = st.selectbox(
            T("under_type"),
            ["Equity Index", "Single Stock", "Bond", "Loan Portfolio"],
            index=0,
            key="hg_trs_type",
        )
        trs_name = st.text_input(T("under_name"), value="S&P 500", key="hg_trs_name")
        trs_not = st.number_input(
            T("irs_not"),
            value=10_000_000.0,
            step=100_000.0,
            format="%.2f",
            key="hg_trs_not",
        )
        trs_ref = st.number_input(
            T("ref_price"),
            value=5100.0,
            step=1.0,
            format="%.2f",
            key="hg_trs_ref",
        )
        trs_pos = st.radio(
            T("trs_position"),
            [T("tr_rec"), T("tr_pay")],
            index=0,
            horizontal=True,
            key="hg_trs_pos",
        )
        trs_idx = st.selectbox(
            T("fin_idx"),
            ["SOFR", "CDI", "EURIBOR", "SONIA"],
            index=0,
            key="hg_trs_idx",
        )
        trs_idx_rate = st.number_input(
            f"{trs_idx} rate (% p.a.)", value=5.25, step=0.05, format="%.3f", key="hg_trs_idx_r"
        )
        trs_fin_sp = st.number_input(
            T("fin_sp"), value=75.0, step=5.0, format="%.1f", key="hg_trs_fin_sp"
        )
        trs_tenor_m = st.number_input(
            T("trs_tenor"),
            value=12,
            min_value=1,
            max_value=120,
            step=1,
            key="hg_trs_tenor",
        )
        trs_freq_lbl = st.selectbox(
            "Frequency",
            ["Monthly", "Quarterly", "Semi-annual"],
            index=1,
            key="hg_trs_freq",
        )
        trs_freq_map = {"Monthly": 12, "Quarterly": 4, "Semi-annual": 2}
        trs_freq_n = trs_freq_map[trs_freq_lbl]
        trs_div = st.number_input(
            T("div_yld"), value=0.50, step=0.05, format="%.3f", key="hg_trs_div"
        )
        trs_coll_pct = st.slider(
            T("collateral"), min_value=5.0, max_value=100.0, value=20.0, step=5.0, key="hg_trs_coll"
        )
        trs_end_price = st.number_input(
            "Expected End Price",
            value=float(trs_ref) * 1.08,
            step=1.0,
            format="%.2f",
            key="hg_trs_end",
        )

    # Calculations
    trs_collateral = trs_not * trs_coll_pct / 100.0
    leverage = trs_not / trs_collateral if trs_collateral > 0 else 0.0

    tenor_years = trs_tenor_m / 12.0
    fin_rate_total = (trs_idx_rate + trs_fin_sp / 100.0) / 100.0
    financing_cost = trs_not * fin_rate_total * tenor_years

    n_periods_trs = int(trs_tenor_m / (12 / trs_freq_n))
    div_per_period = trs_div / 100.0
    total_divs = trs_not * div_per_period * n_periods_trs

    price_return_pct = (trs_end_price - trs_ref) / trs_ref
    price_return_abs = trs_not * price_return_pct

    if trs_pos == T("tr_rec"):
        net_pnl = price_return_abs + total_divs - financing_cost
    else:
        net_pnl = -price_return_abs - total_divs + financing_cost

    roi_on_collateral = net_pnl / trs_collateral if trs_collateral > 0 else 0.0

    with col_trs_out:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(T("irs_not"), fmt_money(trs_not, "", 0))
        with m2:
            metric_card(T("leverage"), f"{leverage:.1f}×")
        with m3:
            metric_card(T("fin_cost"), fmt_money(financing_cost, "", 0))
        with m4:
            metric_card(
                T("exp_return"),
                fmt_money(net_pnl, "", 0),
                delta=f"ROI: {roi_on_collateral*100:+.2f}%",
                delta_pos=(net_pnl > 0),
            )

        # Scenario table
        scenarios_trs = np.linspace(-0.30, 0.30, 13)
        trs_rows = []
        for sc in scenarios_trs:
            end_p = trs_ref * (1 + sc)
            pr_abs = trs_not * sc
            if trs_pos == T("tr_rec"):
                net = pr_abs + total_divs - financing_cost
            else:
                net = -pr_abs - total_divs + financing_cost
            roi_c = net / trs_collateral if trs_collateral > 0 else 0.0
            trs_rows.append(
                {
                    "Scenario": f"{sc*100:+.0f}%",
                    "End Price": round(end_p, 2),
                    "Price Return": round(pr_abs, 2),
                    "Dividends": round(total_divs, 2),
                    "Financing": round(-financing_cost, 2),
                    "Net P&L": round(net, 2),
                    "ROI on Collateral": f"{roi_c*100:+.2f}%",
                }
            )
        trs_df = pd.DataFrame(trs_rows)

        # Chart: P&L breakdown
        fig_trs = go.Figure()
        fig_trs.add_trace(
            go.Bar(
                x=trs_df["Scenario"],
                y=[trs_not * s for s in scenarios_trs],
                name="Price Return",
                marker_color=PRIMARY,
            )
        )
        fig_trs.add_trace(
            go.Bar(
                x=trs_df["Scenario"],
                y=[total_divs] * len(scenarios_trs),
                name="Dividends",
                marker_color=ACCENT_GREEN,
            )
        )
        fig_trs.add_trace(
            go.Bar(
                x=trs_df["Scenario"],
                y=[-financing_cost] * len(scenarios_trs),
                name="Financing",
                marker_color=ACCENT_RED,
            )
        )
        fig_trs.add_trace(
            go.Scatter(
                x=trs_df["Scenario"],
                y=trs_df["Net P&L"],
                mode="lines+markers",
                name="Net P&L",
                line=dict(color="black", width=3),
                marker=dict(size=8),
            )
        )
        fig_trs.update_layout(
            height=340,
            barmode="relative",
            xaxis_title="Price Scenario",
            yaxis_title="P&L",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        fig_trs.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        fig_trs.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_trs, use_container_width=True)

        st.dataframe(trs_df, use_container_width=True, hide_index=True, height=240)

        # TRS vs Direct Ownership
        direct_capital = trs_not
        direct_return = trs_not * price_return_pct + total_divs
        direct_roi = direct_return / direct_capital
        trs_roi = roi_on_collateral

        comp_rows = [
            {
                "Strategy": "Direct Ownership",
                "Capital Required": round(direct_capital, 2),
                "Expected Return": round(direct_return, 2),
                "ROI": f"{direct_roi*100:+.2f}%",
                "Leverage": "1.0×",
            },
            {
                "Strategy": "TRS (synthetic)",
                "Capital Required": round(trs_collateral, 2),
                "Expected Return": round(net_pnl, 2),
                "ROI": f"{trs_roi*100:+.2f}%",
                "Leverage": f"{leverage:.1f}×",
            },
        ]
        comp_trs_df = pd.DataFrame(comp_rows)
        st.markdown("**TRS vs Direct Ownership — Capital Efficiency**")
        st.dataframe(comp_trs_df, use_container_width=True, hide_index=True)

    warning_box(
        f"<b>Margin Call Risk:</b> A price drop of {trs_coll_pct*0.5:.1f}% "
        f"would erode ~50% of posted collateral ({trs_collateral*0.5:,.0f}), "
        f"likely triggering a variation margin call under ISDA CSA."
    )

# =============================================================================
# TAB 6 — HEDGE EFFECTIVENESS
# =============================================================================
with tab6:
    section_header(T("tab_eff") + " — IFRS 9 / ASC 815 Framework")

    with st.expander("About Hedge Effectiveness / Sobre a Efetividade de Hedge", expanded=False):
        st.markdown(
            """
            **Hedge Accounting Standards** (IFRS 9 & ASC 815) require a hedge
            to be "highly effective" — traditionally interpreted as
            **80%-125% effectiveness** — to qualify for special accounting
            treatment (smoothing of P&L).

            **Variance reduction** under a hedge:
            """
        )
        formula_box("σ²_hedged = σ²_unhedged × (1 − ρ² × h²)")
        st.markdown(
            """
            **Effectiveness Ratio:**
            """
        )
        formula_box("E = 1 − (σ²_hedged / σ²_unhedged) = ρ² × h² (when h = h*)")
        st.markdown(
            """
            With the **optimal hedge ratio h\\* = ρ × σS/σF**, effectiveness
            becomes ρ² (squared correlation). Therefore:
            - ρ > 0.90 → Hedge typically qualifies (E > 81%)
            - 0.80 < ρ < 0.90 → Partial hedge
            - ρ < 0.80 → Likely fails effectiveness test
            """
        )

    col_ef_in, col_ef_out = st.columns([1, 2])

    with col_ef_in:
        st.markdown("**Portfolio Inputs**")
        ef_port = st.number_input(
            T("port_val"),
            value=50_000_000.0,
            step=1_000_000.0,
            format="%.2f",
            key="hg_ef_port",
        )
        ef_class = st.selectbox(
            T("asset_class"),
            ["Equity", "Fixed Income", "FX Exposure", "Commodity"],
            index=0,
            key="hg_ef_class",
        )
        ef_beta = st.number_input(
            T("beta"), value=1.05, step=0.05, format="%.2f", key="hg_ef_beta"
        )
        ef_dur = st.number_input(
            T("duration"), value=5.8, step=0.1, format="%.2f", key="hg_ef_dur"
        )
        ef_fx_exp = st.number_input(
            T("fx_exp"),
            value=10_000_000.0,
            step=100_000.0,
            format="%.2f",
            key="hg_ef_fx",
        )

        st.markdown("**Risk Parameters**")
        ef_sigma_port = st.slider(
            "Portfolio Volatility (% ann.)",
            min_value=1.0,
            max_value=60.0,
            value=18.0,
            step=0.5,
            key="hg_ef_sig_p",
        )
        ef_sigma_hdg = st.slider(
            "Hedge Instrument Volatility (% ann.)",
            min_value=1.0,
            max_value=60.0,
            value=17.5,
            step=0.5,
            key="hg_ef_sig_h",
        )
        ef_rho = st.slider(
            T("correl"),
            min_value=-1.0,
            max_value=1.0,
            value=0.93,
            step=0.01,
            key="hg_ef_rho",
        )
        ef_hr = st.slider(
            T("hedge_ratio"),
            min_value=0.0,
            max_value=150.0,
            value=95.0,
            step=1.0,
            key="hg_ef_hr",
        )
        ef_instr = st.selectbox(
            T("hedge_instr"),
            ["FX Forward", "FX Futures", "IRS", "CCS", "TRS", "Index Futures"],
            index=0,
            key="hg_ef_instr",
        )
        ef_hedge_cost_bps = st.number_input(
            "Hedge Cost (bps p.a.)",
            value=25.0,
            step=5.0,
            format="%.1f",
            key="hg_ef_cost",
        )

    # Calculations
    h = ef_hr / 100.0
    sig_p = ef_sigma_port / 100.0
    sig_h = ef_sigma_hdg / 100.0
    rho = ef_rho

    # h* optimal
    h_opt = rho * (sig_p / sig_h) if sig_h > 0 else 0.0

    # Variance reduction
    # σ²_hedged = σ²_p + h² σ²_f − 2 h ρ σ_p σ_f  (cross-hedge variance)
    var_unhedged = sig_p**2
    var_hedged = sig_p**2 + (h**2) * (sig_h**2) - 2 * h * rho * sig_p * sig_h
    var_hedged = max(var_hedged, 1e-10)

    variance_reduction = 1.0 - (var_hedged / var_unhedged)
    effectiveness_ratio = variance_reduction  # same metric

    # VaR 95%
    z95 = 1.645
    sigma_hedged_eff = math.sqrt(var_hedged)
    var_unh = ef_port * sig_p * z95
    var_h = ef_port * sigma_hedged_eff * z95
    var_saving = var_unh - var_h

    # Hedge cost
    hedge_cost_total = ef_port * (ef_hedge_cost_bps / 10000.0)

    with col_ef_out:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(T("var_red"), f"{variance_reduction*100:.1f}%")
        with m2:
            eff_pct = effectiveness_ratio * 100
            metric_card(
                T("eff_ratio"),
                f"{eff_pct:.1f}%",
                delta=("IFRS 9 OK" if eff_pct >= 80 else "Below 80%"),
                delta_pos=(eff_pct >= 80),
            )
        with m3:
            metric_card(T("var_unh"), fmt_money(var_unh, "", 0))
        with m4:
            metric_card(
                T("var_h"),
                fmt_money(var_h, "", 0),
                delta=f"Saved: {fmt_money(var_saving, '', 0)}",
                delta_pos=True,
            )

        # P&L Distribution Histogram (Monte Carlo)
        np.random.seed(42)
        n_sim = 5000
        # Unhedged returns
        ret_port = np.random.normal(0, sig_p, n_sim)
        ret_hdg = rho * ret_port + math.sqrt(max(0, 1 - rho**2)) * np.random.normal(
            0, sig_h, n_sim
        )
        pnl_unhedged = ef_port * ret_port
        pnl_hedged = ef_port * (ret_port - h * (sig_p / sig_h) * ret_hdg) if sig_h > 0 else pnl_unhedged
        # More accurate: subtract h times hedge return (scaled)
        pnl_hedged = ef_port * ret_port - h * ef_port * ret_hdg

        fig_eff = go.Figure()
        fig_eff.add_trace(
            go.Histogram(
                x=pnl_unhedged,
                name="Unhedged",
                opacity=0.55,
                marker_color=ACCENT_RED,
                nbinsx=60,
            )
        )
        fig_eff.add_trace(
            go.Histogram(
                x=pnl_hedged,
                name="Hedged",
                opacity=0.70,
                marker_color=PRIMARY,
                nbinsx=60,
            )
        )
        fig_eff.add_vline(
            x=-var_unh,
            line_dash="dash",
            line_color=ACCENT_RED,
            annotation_text=f"VaR unh = {-var_unh:,.0f}",
        )
        fig_eff.add_vline(
            x=-var_h,
            line_dash="dash",
            line_color=PRIMARY,
            annotation_text=f"VaR h = {-var_h:,.0f}",
        )
        fig_eff.update_layout(
            barmode="overlay",
            height=360,
            xaxis_title="P&L",
            yaxis_title="Frequency",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        fig_eff.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        fig_eff.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_eff, use_container_width=True)

        # Summary table
        summary_rows = [
            {"Metric": "Optimal Hedge Ratio (h*)", "Value": f"{h_opt:.4f}"},
            {"Metric": "Current Hedge Ratio (h)", "Value": f"{h:.4f}"},
            {"Metric": "Correlation (ρ)", "Value": f"{rho:.4f}"},
            {"Metric": "Max Possible Effectiveness (ρ²)", "Value": f"{(rho**2)*100:.2f}%"},
            {"Metric": "Current Effectiveness", "Value": f"{effectiveness_ratio*100:.2f}%"},
            {"Metric": "VaR Reduction", "Value": fmt_money(var_saving, "", 0)},
            {"Metric": "Hedge Cost (p.a.)", "Value": fmt_money(hedge_cost_total, "", 0)},
            {
                "Metric": "Cost / VaR Saved Ratio",
                "Value": f"{(hedge_cost_total/var_saving*100):.2f}%" if var_saving > 0 else "N/A",
            },
        ]
        st.markdown("**Detailed Metrics**")
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        # Recommendation
        if effectiveness_ratio >= 0.80:
            success_box(
                f"<b>{T('recommend')}:</b> {T('eff_hedge')}. "
                f"Effectiveness ratio {effectiveness_ratio*100:.1f}% exceeds the 80% "
                f"threshold under IFRS 9 / ASC 815, qualifying for hedge accounting."
            )
        elif effectiveness_ratio >= 0.50:
            warning_box(
                f"<b>{T('recommend')}:</b> {T('partial_hedge')}. "
                f"Effectiveness ratio {effectiveness_ratio*100:.1f}% is below the 80% "
                f"accounting threshold but provides meaningful economic risk reduction. "
                f"Consider adjusting hedge ratio towards h* = {h_opt:.3f}."
            )
        else:
            st.markdown(
                f"""
                <div style="background: #fee2e2; border-left: 4px solid {ACCENT_RED};
                            border-radius: 6px; padding: 0.75rem 1rem; margin: 0.7rem 0;">
                    <b>{T('recommend')}:</b> {T('ineff_hedge')}.
                    Effectiveness ratio only {effectiveness_ratio*100:.1f}%. Correlation
                    (ρ={rho:.2f}) is too low or hedge ratio is sub-optimal. Review
                    instrument selection or increase hedge ratio towards h* = {h_opt:.3f}.
                </div>
                """,
                unsafe_allow_html=True,
            )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: {TEXT_MUTED}; font-size: 0.82rem; padding: 1rem 0;">
        Hedging Strategies Toolkit — Built on CME, ISDA, IFRS 9 / ASC 815 standards.
        For educational and analytical purposes only. Not investment advice.
        <br>
        Covered Interest Rate Parity · Ederington Minimum Variance · Multi-Curve Framework (OIS Discounting)
    </div>
    """,
    unsafe_allow_html=True,
)
