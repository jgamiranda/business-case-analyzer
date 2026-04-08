import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="M&A", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "page_title": "M&A — Fusoes e Aquisicoes",
    "page_sub": "Modelo completo de avaliacao de targets, sinergias e analise de acrecao/diluicao.",
    "dark_mode": "Modo Escuro",
    # Tabs
    "tab_target": "  Target  ",
    "tab_valuation": "  Avaliacao  ",
    "tab_synergies": "  Sinergias  ",
    "tab_deal": "  Estrutura  ",
    "tab_proforma": "  Pro-Forma  ",
    "tab_results": "  Resultados  ",
    # Target
    "tgt_title": "Dados da Empresa-Alvo (Target)",
    "tgt_cap": "Insira as informacoes financeiras da empresa a ser adquirida.",
    "tgt_name": "Nome da empresa-alvo",
    "tgt_name_ph": "Ex: Empresa ABC Ltda",
    "tgt_revenue": "Receita Anual",
    "tgt_ebitda": "EBITDA",
    "tgt_net_income": "Lucro Liquido",
    "tgt_total_debt": "Divida Total",
    "tgt_cash": "Caixa e Equivalentes",
    "tgt_shares": "Acoes em circulacao (milhoes)",
    "tgt_sector": "Setor",
    "tgt_currency": "Moeda",
    "tgt_summary": "Resumo do Target",
    "tgt_ev_simple": "EV Simplificado (EBITDA - Caixa + Divida)",
    "tgt_equity_simple": "Equity Value Simplificado",
    "tgt_ebitda_margin": "Margem EBITDA",
    "tgt_net_margin": "Margem Liquida",
    # Acquirer
    "acq_title": "Dados da Adquirente",
    "acq_cap": "Informacoes financeiras da empresa adquirente.",
    "acq_name": "Nome da adquirente",
    "acq_name_ph": "Ex: Grupo XYZ S.A.",
    "acq_revenue": "Receita Anual",
    "acq_ebitda": "EBITDA",
    "acq_net_income": "Lucro Liquido",
    "acq_shares": "Acoes em circulacao (milhoes)",
    "acq_share_price": "Preco por acao",
    "acq_tax_rate": "Aliquota IR/CSLL (%)",
    # Valuation
    "val_title": "Avaliacao do Target",
    "val_cap": "Multiplos de mercado e valor implicito.",
    "val_ev_ebitda": "Multiplo EV/EBITDA",
    "val_ev_revenue": "Multiplo EV/Receita",
    "val_pe": "Multiplo P/L (Preco/Lucro)",
    "val_method": "Metodo principal de avaliacao",
    "val_ev": "Enterprise Value (EV)",
    "val_equity": "Equity Value Implicito",
    "val_price_per_share": "Preco Implicito por Acao",
    "val_ev_rev_implied": "EV/Receita Implicito",
    "val_ev_ebitda_implied": "EV/EBITDA Implicito",
    "val_pe_implied": "P/L Implicito",
    "val_comparison": "Comparacao de Metodos de Avaliacao",
    "val_method_evebitda": "EV/EBITDA",
    "val_method_evrev": "EV/Receita",
    "val_method_pe": "P/L",
    # Synergies
    "syn_title": "Sinergias",
    "syn_cap": "Estimativas de sinergias de receita e custo da combinacao.",
    "syn_rev_title": "Sinergias de Receita",
    "syn_rev_pct": "Uplift de receita (%)",
    "syn_rev_phase": "Fase de integracao (meses)",
    "syn_rev_prob": "Probabilidade de realizacao (%)",
    "syn_cost_title": "Sinergias de Custo",
    "syn_cost_abs": "Economia de custos anual",
    "syn_cost_phase": "Fase de integracao (meses)",
    "syn_cost_prob": "Probabilidade de realizacao (%)",
    "syn_npv_title": "NPV das Sinergias",
    "syn_discount": "Taxa de desconto para sinergias (%)",
    "syn_horizon": "Horizonte de projecao (anos)",
    "syn_annual_rev": "Sinergia de receita anual (estabilizada)",
    "syn_annual_cost": "Sinergia de custo anual (estabilizada)",
    "syn_total_annual": "Sinergia total anual (estabilizada)",
    "syn_npv": "NPV das Sinergias",
    "syn_timeline": "Timeline de Realizacao das Sinergias",
    # Deal
    "deal_title": "Estrutura da Transacao",
    "deal_cap": "Defina o preco, forma de pagamento e financiamento.",
    "deal_price": "Purchase Price (Equity Value)",
    "deal_premium_pct": "Premio sobre valor de mercado (%)",
    "deal_pct_cash": "% Pagamento em Cash",
    "deal_pct_stock": "% Pagamento em Acoes",
    "deal_new_debt": "Nova divida levantada para a aquisicao",
    "deal_advisory_fees": "Fees de assessoria",
    "deal_integration_cost": "Custo de integracao estimado",
    "deal_summary": "Resumo da Transacao",
    "deal_total_cost": "Custo Total da Transacao",
    "deal_cash_component": "Componente Cash",
    "deal_stock_component": "Componente em Acoes",
    "deal_new_shares": "Novas acoes emitidas (milhoes)",
    "deal_financing": "Fontes de Financiamento",
    "deal_existing_cash": "Caixa existente utilizado",
    "deal_debt_raised": "Divida levantada",
    "deal_equity_issued": "Acoes emitidas (valor)",
    # Pro-forma
    "pf_title": "Demonstracao Pro-Forma Combinada",
    "pf_cap": "P&L combinado e analise de acrecao/diluicao.",
    "pf_acquirer": "Adquirente",
    "pf_target": "Target",
    "pf_synergies": "Sinergias",
    "pf_adjustments": "Ajustes",
    "pf_combined": "Combinado",
    "pf_revenue": "Receita",
    "pf_ebitda": "EBITDA",
    "pf_dep_amort": "(–) D&A",
    "pf_ebit": "EBIT",
    "pf_interest": "(–) Despesas Financeiras",
    "pf_ebt": "LAIR / EBT",
    "pf_taxes": "(–) IR/CSLL",
    "pf_net_income": "Lucro Liquido",
    "pf_shares_out": "Acoes (milhoes)",
    "pf_eps": "LPA / EPS",
    "pf_accretion": "Acrecao / Diluicao",
    "pf_accretion_pct": "Acrecao / Diluicao (%)",
    "pf_da_pct_rev": "D&A como % da receita (%)",
    "pf_interest_new_debt": "Juros sobre nova divida (%)",
    # Results
    "res_title": "Resultados e Metricas-Chave",
    "res_cap": "Visao consolidada da transacao.",
    "res_ev": "Enterprise Value",
    "res_equity_val": "Equity Value",
    "res_premium": "Premio Pago",
    "res_accretion_dilution": "Acrecao / Diluicao por Acao",
    "res_accretion_dilution_pct": "Acrecao / Diluicao (%)",
    "res_synergy_npv": "NPV das Sinergias",
    "res_total_cost": "Custo Total",
    "res_combined_ebitda": "EBITDA Combinado (c/ sinergias)",
    "res_leverage": "Alavancagem (Divida / EBITDA Combinado)",
    "res_verdict_title": "Avaliacao Geral",
    "res_accretive": "A transacao e ACCRETIVA para o adquirente — aumenta o LPA.",
    "res_dilutive": "A transacao e DILUTIVA para o adquirente — reduz o LPA.",
    "res_neutral": "A transacao e NEUTRA — nao altera significativamente o LPA.",
    "res_waterfall": "Waterfall — Construcao do Enterprise Value",
    "res_sensitivity": "Sensibilidade: Acrecao/Diluicao vs. Multiplo e % Cash",
},
"EN": {
    "page_title": "M&A — Mergers & Acquisitions",
    "page_sub": "Complete target valuation, synergies and accretion/dilution analysis model.",
    "dark_mode": "Dark Mode",
    "tab_target": "  Target  ",
    "tab_valuation": "  Valuation  ",
    "tab_synergies": "  Synergies  ",
    "tab_deal": "  Deal Structure  ",
    "tab_proforma": "  Pro-Forma  ",
    "tab_results": "  Results  ",
    "tgt_title": "Target Company Data",
    "tgt_cap": "Enter the financial information for the acquisition target.",
    "tgt_name": "Target company name",
    "tgt_name_ph": "E.g.: ABC Corp.",
    "tgt_revenue": "Annual Revenue",
    "tgt_ebitda": "EBITDA",
    "tgt_net_income": "Net Income",
    "tgt_total_debt": "Total Debt",
    "tgt_cash": "Cash & Equivalents",
    "tgt_shares": "Shares outstanding (millions)",
    "tgt_sector": "Sector",
    "tgt_currency": "Currency",
    "tgt_summary": "Target Summary",
    "tgt_ev_simple": "Simplified EV (EBITDA - Cash + Debt)",
    "tgt_equity_simple": "Simplified Equity Value",
    "tgt_ebitda_margin": "EBITDA Margin",
    "tgt_net_margin": "Net Margin",
    "acq_title": "Acquirer Data",
    "acq_cap": "Financial information for the acquiring company.",
    "acq_name": "Acquirer name",
    "acq_name_ph": "E.g.: XYZ Group Inc.",
    "acq_revenue": "Annual Revenue",
    "acq_ebitda": "EBITDA",
    "acq_net_income": "Net Income",
    "acq_shares": "Shares outstanding (millions)",
    "acq_share_price": "Share price",
    "acq_tax_rate": "Tax rate (%)",
    "val_title": "Target Valuation",
    "val_cap": "Market multiples and implied value.",
    "val_ev_ebitda": "EV/EBITDA Multiple",
    "val_ev_revenue": "EV/Revenue Multiple",
    "val_pe": "P/E Multiple",
    "val_method": "Primary valuation method",
    "val_ev": "Enterprise Value (EV)",
    "val_equity": "Implied Equity Value",
    "val_price_per_share": "Implied Price per Share",
    "val_ev_rev_implied": "Implied EV/Revenue",
    "val_ev_ebitda_implied": "Implied EV/EBITDA",
    "val_pe_implied": "Implied P/E",
    "val_comparison": "Valuation Method Comparison",
    "val_method_evebitda": "EV/EBITDA",
    "val_method_evrev": "EV/Revenue",
    "val_method_pe": "P/E",
    "syn_title": "Synergies",
    "syn_cap": "Revenue and cost synergy estimates from the combination.",
    "syn_rev_title": "Revenue Synergies",
    "syn_rev_pct": "Revenue uplift (%)",
    "syn_rev_phase": "Integration phase-in (months)",
    "syn_rev_prob": "Probability of realization (%)",
    "syn_cost_title": "Cost Synergies",
    "syn_cost_abs": "Annual cost savings",
    "syn_cost_phase": "Integration phase-in (months)",
    "syn_cost_prob": "Probability of realization (%)",
    "syn_npv_title": "Synergies NPV",
    "syn_discount": "Discount rate for synergies (%)",
    "syn_horizon": "Projection horizon (years)",
    "syn_annual_rev": "Annual revenue synergy (stabilized)",
    "syn_annual_cost": "Annual cost synergy (stabilized)",
    "syn_total_annual": "Total annual synergy (stabilized)",
    "syn_npv": "Synergies NPV",
    "syn_timeline": "Synergy Realization Timeline",
    "deal_title": "Deal Structure",
    "deal_cap": "Define the price, payment method and financing.",
    "deal_price": "Purchase Price (Equity Value)",
    "deal_premium_pct": "Premium over market value (%)",
    "deal_pct_cash": "% Cash Payment",
    "deal_pct_stock": "% Stock Payment",
    "deal_new_debt": "New debt raised for acquisition",
    "deal_advisory_fees": "Advisory fees",
    "deal_integration_cost": "Estimated integration cost",
    "deal_summary": "Deal Summary",
    "deal_total_cost": "Total Transaction Cost",
    "deal_cash_component": "Cash Component",
    "deal_stock_component": "Stock Component",
    "deal_new_shares": "New shares issued (millions)",
    "deal_financing": "Financing Sources",
    "deal_existing_cash": "Existing cash used",
    "deal_debt_raised": "Debt raised",
    "deal_equity_issued": "Equity issued (value)",
    "pf_title": "Combined Pro-Forma Statement",
    "pf_cap": "Combined P&L and accretion/dilution analysis.",
    "pf_acquirer": "Acquirer",
    "pf_target": "Target",
    "pf_synergies": "Synergies",
    "pf_adjustments": "Adjustments",
    "pf_combined": "Combined",
    "pf_revenue": "Revenue",
    "pf_ebitda": "EBITDA",
    "pf_dep_amort": "(–) D&A",
    "pf_ebit": "EBIT",
    "pf_interest": "(–) Interest Expense",
    "pf_ebt": "EBT",
    "pf_taxes": "(–) Taxes",
    "pf_net_income": "Net Income",
    "pf_shares_out": "Shares (millions)",
    "pf_eps": "EPS",
    "pf_accretion": "Accretion / Dilution",
    "pf_accretion_pct": "Accretion / Dilution (%)",
    "pf_da_pct_rev": "D&A as % of revenue (%)",
    "pf_interest_new_debt": "Interest on new debt (%)",
    "res_title": "Key Results & Metrics",
    "res_cap": "Consolidated transaction overview.",
    "res_ev": "Enterprise Value",
    "res_equity_val": "Equity Value",
    "res_premium": "Premium Paid",
    "res_accretion_dilution": "Accretion / Dilution per Share",
    "res_accretion_dilution_pct": "Accretion / Dilution (%)",
    "res_synergy_npv": "Synergies NPV",
    "res_total_cost": "Total Cost",
    "res_combined_ebitda": "Combined EBITDA (w/ synergies)",
    "res_leverage": "Leverage (Debt / Combined EBITDA)",
    "res_verdict_title": "Overall Assessment",
    "res_accretive": "The transaction is ACCRETIVE to the acquirer — increases EPS.",
    "res_dilutive": "The transaction is DILUTIVE to the acquirer — decreases EPS.",
    "res_neutral": "The transaction is NEUTRAL — no significant impact on EPS.",
    "res_waterfall": "Waterfall — Enterprise Value Build-Up",
    "res_sensitivity": "Sensitivity: Accretion/Dilution vs. Multiple & % Cash",
},
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS (same visual style as the rest of the app)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"]{display:none}
.stTabs [data-baseweb="tab-list"]{gap:5px}
.stTabs [data-baseweb="tab"]{background:#dbeafe;border-radius:6px 6px 0 0;color:#1a56db;font-weight:600;padding:8px 18px;border:1px solid #bfdbfe;border-bottom:none;transition:all .2s ease}
.stTabs [data-baseweb="tab"]:hover{background:#1a56db;color:white;transform:translateY(-1px)}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:white !important;border-color:#1a56db !important}
[data-testid="stExpander"] details summary{background:#1a56db !important;border-radius:6px !important;padding:10px 16px !important;transition:background .2s ease}
[data-testid="stExpander"] details summary:hover{background:#1e429f !important}
[data-testid="stExpander"] details summary p,[data-testid="stExpander"] details summary span{color:white !important;font-weight:600 !important}
[data-testid="stExpander"] details summary svg{fill:white !important;stroke:white !important}
[data-testid="stExpander"] details{border:1px solid #1a56db !important;border-radius:6px !important}
.metric-card{background:linear-gradient(135deg,#f0f7ff 0%,#dbeafe 100%);border:1px solid #bfdbfe;border-radius:10px;padding:16px 18px;text-align:center;transition:all .2s ease}
.metric-card:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(26,86,219,.14)}
.metric-card .mc-label{font-size:.72rem;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.metric-card .mc-value{font-size:1.5rem;font-weight:800;color:#1a56db;margin:2px 0}
.metric-card .mc-delta{font-size:.78rem;font-weight:600;margin-top:2px}
.mc-pos{color:#16a34a}.mc-neg{color:#dc2626}
.metric-card-green{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-color:#a3d9a5}
.metric-card-green .mc-value{color:#16a34a}
.metric-card-red{background:linear-gradient(135deg,#f8d7da 0%,#f5c6cb 100%);border-color:#f1aeb5}
.metric-card-red .mc-value{color:#dc2626}
.veredicto-verde{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-left:6px solid #28a745;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(40,167,69,.12)}
.veredicto-amarelo{background:linear-gradient(135deg,#fff3cd 0%,#ffeeba 100%);border-left:6px solid #ffc107;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(255,193,7,.12)}
.veredicto-vermelho{background:linear-gradient(135deg,#f8d7da 0%,#f5c6cb 100%);border-left:6px solid #dc3545;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(220,53,69,.12)}
.veredicto-titulo{font-size:1.5rem;font-weight:700;margin-bottom:6px}
.df-styled{overflow-x:auto;border-radius:8px;margin:4px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.df-styled table{width:100%;border-collapse:collapse;font-size:.86rem;font-family:inherit}
.df-styled table thead th{background:#1a56db !important;color:#fff !important;padding:8px 14px;font-weight:700;text-align:right;border:1px solid #1e429f !important}
.df-styled table thead th:first-child{background:#1e3a8a !important;text-align:left}
.df-styled table tbody th{color:#374151;font-weight:500;padding:6px 14px;text-align:left;border:1px solid #e5e7eb !important;white-space:nowrap;background:#fafafa}
.df-styled table tbody td{padding:6px 14px;text-align:right;border:1px solid #e5e7eb !important}
.df-styled table tbody tr:hover td,.df-styled table tbody tr:hover th{background:#f0f7ff !important}
.hero-bar{background:linear-gradient(135deg,#1e3a8a 0%,#1a56db 100%);border-radius:16px;padding:28px 34px;margin-bottom:20px;color:white}
.hero-bar h1{font-size:1.8rem;font-weight:800;margin:0 0 6px 0;color:white !important}
.hero-bar p{font-size:.92rem;color:#bfdbfe;margin:0;line-height:1.5}
.app-footer{text-align:center;padding:20px 0 10px 0;margin-top:40px;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.75rem}
.sens-tbl{overflow-x:auto;border-radius:8px;margin:4px 0;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.sens-tbl table{width:100%;border-collapse:collapse;font-size:.86rem;font-family:inherit}
.sens-tbl table thead th{background:#1a56db !important;color:#fff !important;padding:9px 16px;font-weight:700;text-align:center;border:1px solid #1e429f !important}
.sens-tbl table thead th:first-child{background:#1e3a8a !important}
.sens-tbl table tbody th{background:#dbeafe !important;color:#1e3a8a !important;font-weight:700;padding:7px 16px;text-align:right;border:1px solid #bfdbfe !important;white-space:nowrap}
.sens-tbl table tbody td{padding:7px 14px;text-align:center;border:1px solid #e5e7eb !important;font-weight:600;font-size:.85rem}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE TOGGLE + HEADER
# ─────────────────────────────────────────────────────────────────────────────
_hc1, _hc2 = st.columns([8, 1])
with _hc2:
    _lang_sel = st.segmented_control("lang_ma", ["PT", "EN"], default="PT",
                                      key="ma_lang", label_visibility="collapsed")
lang = _lang_sel or "PT"
def T(k): return _L.get(lang, _L["PT"]).get(k, _L["PT"].get(k, k))

st.markdown(f"""
<div class="hero-bar">
    <h1>{T("page_title")}</h1>
    <p>{T("page_sub")}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: metric card HTML
# ─────────────────────────────────────────────────────────────────────────────
def metric_card(label, value, delta=None, card_class="metric-card"):
    delta_html = ""
    if delta is not None:
        cls = "mc-pos" if delta >= 0 else "mc-neg"
        sign = "+" if delta >= 0 else ""
        delta_html = f'<div class="mc-delta {cls}">{sign}{delta:.2f}%</div>'
    return f"""<div class="{card_class}">
        <div class="mc-label">{label}</div>
        <div class="mc-value">{value}</div>
        {delta_html}
    </div>"""

def fmt(v, decimals=1, prefix="", suffix=""):
    """Format number with thousands separators."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    if abs(v) >= 1e9:
        return f"{prefix}{v/1e9:,.{decimals}f}B{suffix}"
    if abs(v) >= 1e6:
        return f"{prefix}{v/1e6:,.{decimals}f}M{suffix}"
    if abs(v) >= 1e3:
        return f"{prefix}{v/1e3:,.{decimals}f}K{suffix}"
    return f"{prefix}{v:,.{decimals}f}{suffix}"

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    # Target
    "ma_tgt_name": "Target Corp.",
    "ma_tgt_revenue": 500_000_000.0,
    "ma_tgt_ebitda": 100_000_000.0,
    "ma_tgt_net_income": 50_000_000.0,
    "ma_tgt_debt": 80_000_000.0,
    "ma_tgt_cash": 30_000_000.0,
    "ma_tgt_shares": 50.0,
    "ma_tgt_sector": "Tecnologia",
    "ma_tgt_currency": "BRL",
    # Acquirer
    "ma_acq_name": "Acquirer S.A.",
    "ma_acq_revenue": 2_000_000_000.0,
    "ma_acq_ebitda": 500_000_000.0,
    "ma_acq_net_income": 250_000_000.0,
    "ma_acq_shares": 200.0,
    "ma_acq_share_price": 25.0,
    "ma_acq_tax_rate": 34.0,
    # Valuation
    "ma_val_ev_ebitda": 10.0,
    "ma_val_ev_revenue": 2.0,
    "ma_val_pe": 15.0,
    "ma_val_method": "EV/EBITDA",
    # Synergies
    "ma_syn_rev_pct": 5.0,
    "ma_syn_rev_phase": 24,
    "ma_syn_rev_prob": 60.0,
    "ma_syn_cost_abs": 30_000_000.0,
    "ma_syn_cost_phase": 18,
    "ma_syn_cost_prob": 80.0,
    "ma_syn_discount": 12.0,
    "ma_syn_horizon": 10,
    # Deal
    "ma_deal_premium_pct": 25.0,
    "ma_deal_pct_cash": 60.0,
    "ma_deal_new_debt": 200_000_000.0,
    "ma_deal_advisory_fees": 15_000_000.0,
    "ma_deal_integration_cost": 25_000_000.0,
    # Pro-forma
    "ma_pf_da_pct": 5.0,
    "ma_pf_interest_new_debt": 8.0,
}

for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get(k, d=0.0):
    return st.session_state.get(k, d)

# ─────────────────────────────────────────────────────────────────────────────
# SECTOR OPTIONS
# ─────────────────────────────────────────────────────────────────────────────
SECTORS_PT = ["Tecnologia", "Saude", "Varejo", "Industria", "Servicos Financeiros",
              "Energia", "Logistica", "Educacao", "Agronegocio", "Outro"]
SECTORS_EN = ["Technology", "Healthcare", "Retail", "Industry", "Financial Services",
              "Energy", "Logistics", "Education", "Agribusiness", "Other"]

CURRENCIES = ["BRL", "USD", "EUR"]

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    T("tab_target"), T("tab_valuation"), T("tab_synergies"),
    T("tab_deal"), T("tab_proforma"), T("tab_results"),
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: TARGET
# ═════════════════════════════════════════════════════════════════════════════
with tabs[0]:

    # ── Target Company ──────────────────────────────────────────────────────
    with st.expander(f"1.  {T('tgt_title')}", expanded=True):
        st.caption(T("tgt_cap"))

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.text_input(T("tgt_name"), key="ma_tgt_name", placeholder=T("tgt_name_ph"))
        with c2:
            sectors = SECTORS_EN if lang == "EN" else SECTORS_PT
            idx = 0
            st.selectbox(T("tgt_sector"), sectors, key="ma_tgt_sector_display", index=idx)
        with c3:
            st.selectbox(T("tgt_currency"), CURRENCIES, key="ma_tgt_currency")

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(T("tgt_revenue"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_tgt_revenue")
            st.number_input(T("tgt_total_debt"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_tgt_debt")
        with c2:
            st.number_input(T("tgt_ebitda"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_tgt_ebitda")
            st.number_input(T("tgt_cash"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_tgt_cash")
        with c3:
            st.number_input(T("tgt_net_income"), step=1_000_000.0,
                            format="%.0f", key="ma_tgt_net_income")
            st.number_input(T("tgt_shares"), min_value=0.1, step=1.0,
                            format="%.1f", key="ma_tgt_shares")

        # Summary metrics
        tgt_rev = get("ma_tgt_revenue")
        tgt_ebitda = get("ma_tgt_ebitda")
        tgt_ni = get("ma_tgt_net_income")
        tgt_debt = get("ma_tgt_debt")
        tgt_cash = get("ma_tgt_cash")
        tgt_shares = get("ma_tgt_shares", 1.0)

        ebitda_margin = (tgt_ebitda / tgt_rev * 100) if tgt_rev else 0
        net_margin = (tgt_ni / tgt_rev * 100) if tgt_rev else 0

        st.markdown(f"#### {T('tgt_summary')}")
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(metric_card(T("tgt_ebitda_margin"), f"{ebitda_margin:.1f}%"), unsafe_allow_html=True)
        with mc2:
            st.markdown(metric_card(T("tgt_net_margin"), f"{net_margin:.1f}%"), unsafe_allow_html=True)
        with mc3:
            ev_simple = tgt_ebitda + tgt_debt - tgt_cash
            st.markdown(metric_card(T("tgt_ev_simple"), fmt(ev_simple)), unsafe_allow_html=True)
        with mc4:
            eq_simple = ev_simple - tgt_debt + tgt_cash
            st.markdown(metric_card(T("tgt_equity_simple"), fmt(eq_simple)), unsafe_allow_html=True)

    # ── Acquirer ────────────────────────────────────────────────────────────
    with st.expander(f"2.  {T('acq_title')}", expanded=True):
        st.caption(T("acq_cap"))

        c1, c2 = st.columns(2)
        with c1:
            st.text_input(T("acq_name"), key="ma_acq_name", placeholder=T("acq_name_ph"))
        with c2:
            st.number_input(T("acq_tax_rate"), min_value=0.0, max_value=100.0,
                            step=1.0, format="%.1f", key="ma_acq_tax_rate")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(T("acq_revenue"), min_value=0.0, step=10_000_000.0,
                            format="%.0f", key="ma_acq_revenue")
            st.number_input(T("acq_shares"), min_value=0.1, step=1.0,
                            format="%.1f", key="ma_acq_shares")
        with c2:
            st.number_input(T("acq_ebitda"), min_value=0.0, step=10_000_000.0,
                            format="%.0f", key="ma_acq_ebitda")
            st.number_input(T("acq_share_price"), min_value=0.01, step=1.0,
                            format="%.2f", key="ma_acq_share_price")
        with c3:
            st.number_input(T("acq_net_income"), step=10_000_000.0,
                            format="%.0f", key="ma_acq_net_income")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: VALUATION
# ═════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    with st.expander(f"3.  {T('val_title')}", expanded=True):
        st.caption(T("val_cap"))

        methods = [T("val_method_evebitda"), T("val_method_evrev"), T("val_method_pe")]
        c1, c2 = st.columns([1, 2])
        with c1:
            method_sel = st.radio(T("val_method"), methods, key="ma_val_method_radio",
                                  horizontal=False)
        with c2:
            st.number_input(T("val_ev_ebitda"), min_value=0.0, step=0.5,
                            format="%.1f", key="ma_val_ev_ebitda")
            st.number_input(T("val_ev_revenue"), min_value=0.0, step=0.1,
                            format="%.1f", key="ma_val_ev_revenue")
            st.number_input(T("val_pe"), min_value=0.0, step=0.5,
                            format="%.1f", key="ma_val_pe")

    # ── Calculations ────────────────────────────────────────────────────────
    tgt_rev = get("ma_tgt_revenue")
    tgt_ebitda = get("ma_tgt_ebitda")
    tgt_ni = get("ma_tgt_net_income")
    tgt_debt = get("ma_tgt_debt")
    tgt_cash = get("ma_tgt_cash")
    tgt_shares = get("ma_tgt_shares", 1.0)

    ev_ebitda_mult = get("ma_val_ev_ebitda", 10.0)
    ev_rev_mult = get("ma_val_ev_revenue", 2.0)
    pe_mult = get("ma_val_pe", 15.0)

    # EV/EBITDA method
    ev_from_ebitda = tgt_ebitda * ev_ebitda_mult
    eq_from_ebitda = ev_from_ebitda - tgt_debt + tgt_cash

    # EV/Revenue method
    ev_from_rev = tgt_rev * ev_rev_mult
    eq_from_rev = ev_from_rev - tgt_debt + tgt_cash

    # P/E method
    eq_from_pe = tgt_ni * pe_mult
    ev_from_pe = eq_from_pe + tgt_debt - tgt_cash

    # Determine primary based on selection
    if method_sel == methods[0]:  # EV/EBITDA
        primary_ev = ev_from_ebitda
        primary_eq = eq_from_ebitda
    elif method_sel == methods[1]:  # EV/Revenue
        primary_ev = ev_from_rev
        primary_eq = eq_from_rev
    else:  # P/E
        primary_ev = ev_from_pe
        primary_eq = eq_from_pe

    price_per_share = primary_eq / (tgt_shares * 1e6) if tgt_shares > 0 else 0
    implied_ev_rev = primary_ev / tgt_rev if tgt_rev > 0 else 0
    implied_ev_ebitda = primary_ev / tgt_ebitda if tgt_ebitda > 0 else 0
    implied_pe = primary_eq / tgt_ni if tgt_ni > 0 else 0

    # Metric cards
    st.markdown(f"#### {T('val_title')}")
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(metric_card(T("val_ev"), fmt(primary_ev)), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card(T("val_equity"), fmt(primary_eq)), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card(T("val_price_per_share"), f"{price_per_share:,.2f}"), unsafe_allow_html=True)

    mc4, mc5, mc6 = st.columns(3)
    with mc4:
        st.markdown(metric_card(T("val_ev_ebitda_implied"), f"{implied_ev_ebitda:.1f}x"), unsafe_allow_html=True)
    with mc5:
        st.markdown(metric_card(T("val_ev_rev_implied"), f"{implied_ev_rev:.1f}x"), unsafe_allow_html=True)
    with mc6:
        st.markdown(metric_card(T("val_pe_implied"), f"{implied_pe:.1f}x"), unsafe_allow_html=True)

    # Comparison chart
    st.markdown(f"#### {T('val_comparison')}")
    comp_df = pd.DataFrame({
        ("Metodo" if lang == "PT" else "Method"): [
            T("val_method_evebitda"), T("val_method_evrev"), T("val_method_pe")
        ],
        "Enterprise Value": [ev_from_ebitda, ev_from_rev, ev_from_pe],
        "Equity Value": [eq_from_ebitda, eq_from_rev, eq_from_pe],
    })

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Enterprise Value",
        x=comp_df.iloc[:, 0], y=comp_df["Enterprise Value"],
        marker_color="#1a56db", text=[fmt(v) for v in comp_df["Enterprise Value"]],
        textposition="outside",
    ))
    fig_comp.add_trace(go.Bar(
        name="Equity Value",
        x=comp_df.iloc[:, 0], y=comp_df["Equity Value"],
        marker_color="#60a5fa", text=[fmt(v) for v in comp_df["Equity Value"]],
        textposition="outside",
    ))
    fig_comp.update_layout(
        barmode="group", height=380,
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        margin=dict(t=30, b=40),
        legend=dict(orientation="h", y=1.08),
    )
    st.plotly_chart(fig_comp, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: SYNERGIES
# ═════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    with st.expander(f"4.  {T('syn_title')}", expanded=True):
        st.caption(T("syn_cap"))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{T('syn_rev_title')}**")
            st.number_input(T("syn_rev_pct"), min_value=0.0, max_value=100.0,
                            step=0.5, format="%.1f", key="ma_syn_rev_pct")
            st.number_input(T("syn_rev_phase"), min_value=1, max_value=60,
                            step=1, key="ma_syn_rev_phase")
            st.number_input(T("syn_rev_prob"), min_value=0.0, max_value=100.0,
                            step=5.0, format="%.0f", key="ma_syn_rev_prob")
        with c2:
            st.markdown(f"**{T('syn_cost_title')}**")
            st.number_input(T("syn_cost_abs"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_syn_cost_abs")
            st.number_input(T("syn_cost_phase"), min_value=1, max_value=60,
                            step=1, key="ma_syn_cost_phase")
            st.number_input(T("syn_cost_prob"), min_value=0.0, max_value=100.0,
                            step=5.0, format="%.0f", key="ma_syn_cost_prob")

        st.markdown("---")
        st.markdown(f"**{T('syn_npv_title')}**")
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(T("syn_discount"), min_value=0.1, max_value=50.0,
                            step=0.5, format="%.1f", key="ma_syn_discount")
        with c2:
            st.number_input(T("syn_horizon"), min_value=1, max_value=30,
                            step=1, key="ma_syn_horizon")

    # ── Synergy calculations ────────────────────────────────────────────────
    syn_rev_pct = get("ma_syn_rev_pct") / 100
    syn_rev_phase = int(get("ma_syn_rev_phase", 24))
    syn_rev_prob = get("ma_syn_rev_prob") / 100
    syn_cost_abs = get("ma_syn_cost_abs")
    syn_cost_phase = int(get("ma_syn_cost_phase", 18))
    syn_cost_prob = get("ma_syn_cost_prob") / 100
    syn_discount = get("ma_syn_discount") / 100
    syn_horizon = int(get("ma_syn_horizon", 10))

    combined_rev = get("ma_tgt_revenue") + get("ma_acq_revenue")
    annual_rev_synergy = combined_rev * syn_rev_pct * syn_rev_prob
    annual_cost_synergy = syn_cost_abs * syn_cost_prob
    total_annual_synergy = annual_rev_synergy + annual_cost_synergy

    # NPV of synergies with phase-in
    syn_npv = 0.0
    syn_timeline_data = []
    for yr in range(1, syn_horizon + 1):
        month_mid = yr * 12 - 6  # mid-year convention
        # Revenue synergy phase-in (linear ramp)
        rev_pct_realized = min(1.0, month_mid / syn_rev_phase) if syn_rev_phase > 0 else 1.0
        rev_syn_yr = combined_rev * syn_rev_pct * syn_rev_prob * rev_pct_realized
        # Cost synergy phase-in
        cost_pct_realized = min(1.0, month_mid / syn_cost_phase) if syn_cost_phase > 0 else 1.0
        cost_syn_yr = syn_cost_abs * syn_cost_prob * cost_pct_realized
        total_yr = rev_syn_yr + cost_syn_yr
        pv = total_yr / ((1 + syn_discount) ** yr)
        syn_npv += pv
        syn_timeline_data.append({
            ("Ano" if lang == "PT" else "Year"): yr,
            (T("syn_annual_rev")): rev_syn_yr,
            (T("syn_annual_cost")): cost_syn_yr,
            "Total": total_yr,
            "PV": pv,
        })

    st.markdown(f"#### {T('syn_npv_title')}")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(metric_card(T("syn_annual_rev"), fmt(annual_rev_synergy)), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card(T("syn_annual_cost"), fmt(annual_cost_synergy)), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card(T("syn_total_annual"), fmt(total_annual_synergy)), unsafe_allow_html=True)
    with mc4:
        cls = "metric-card-green" if syn_npv > 0 else "metric-card"
        st.markdown(metric_card(T("syn_npv"), fmt(syn_npv), card_class=cls), unsafe_allow_html=True)

    # Timeline chart
    if syn_timeline_data:
        st.markdown(f"#### {T('syn_timeline')}")
        tl_df = pd.DataFrame(syn_timeline_data)
        yr_col = tl_df.columns[0]
        fig_syn = go.Figure()
        fig_syn.add_trace(go.Bar(
            name=T("syn_annual_rev"),
            x=tl_df[yr_col], y=tl_df[T("syn_annual_rev")],
            marker_color="#1a56db",
        ))
        fig_syn.add_trace(go.Bar(
            name=T("syn_annual_cost"),
            x=tl_df[yr_col], y=tl_df[T("syn_annual_cost")],
            marker_color="#60a5fa",
        ))
        fig_syn.add_trace(go.Scatter(
            name="NPV (cumul.)",
            x=tl_df[yr_col], y=tl_df["PV"].cumsum(),
            mode="lines+markers", line=dict(color="#16a34a", width=2),
            yaxis="y2",
        ))
        fig_syn.update_layout(
            barmode="stack", height=380,
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
            margin=dict(t=30, b=40),
            legend=dict(orientation="h", y=1.08),
            yaxis=dict(title="Synergy" if lang == "EN" else "Sinergia"),
            yaxis2=dict(title="NPV Cumul.", overlaying="y", side="right",
                        showgrid=False),
        )
        st.plotly_chart(fig_syn, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4: DEAL STRUCTURE
# ═════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    with st.expander(f"5.  {T('deal_title')}", expanded=True):
        st.caption(T("deal_cap"))

        # Purchase price derived from valuation + premium
        acq_mkt_cap = get("ma_acq_shares") * 1e6 * get("ma_acq_share_price")
        tgt_market_eq = primary_eq  # from valuation tab

        c1, c2 = st.columns(2)
        with c1:
            st.number_input(T("deal_premium_pct"), min_value=0.0, max_value=200.0,
                            step=1.0, format="%.1f", key="ma_deal_premium_pct")
        with c2:
            premium_pct = get("ma_deal_premium_pct") / 100
            purchase_price = primary_eq * (1 + premium_pct)
            st.metric(T("deal_price"), fmt(purchase_price))

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            pct_cash = st.slider(T("deal_pct_cash"), 0, 100,
                                 int(get("ma_deal_pct_cash")), 5,
                                 key="ma_deal_pct_cash_slider")
            # Sync to session state
            st.session_state["ma_deal_pct_cash"] = float(pct_cash)
        with c2:
            pct_stock = 100 - pct_cash
            st.metric(T("deal_pct_stock"), f"{pct_stock}%")

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(T("deal_new_debt"), min_value=0.0, step=10_000_000.0,
                            format="%.0f", key="ma_deal_new_debt")
        with c2:
            st.number_input(T("deal_advisory_fees"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_deal_advisory_fees")
        with c3:
            st.number_input(T("deal_integration_cost"), min_value=0.0, step=1_000_000.0,
                            format="%.0f", key="ma_deal_integration_cost")

    # ── Deal calculations ───────────────────────────────────────────────────
    cash_component = purchase_price * (pct_cash / 100)
    stock_component = purchase_price * (pct_stock / 100)
    acq_share_price = get("ma_acq_share_price", 1.0)
    new_shares = (stock_component / acq_share_price) / 1e6 if acq_share_price > 0 else 0
    total_cost = purchase_price + get("ma_deal_advisory_fees") + get("ma_deal_integration_cost")
    new_debt = get("ma_deal_new_debt")

    st.markdown(f"#### {T('deal_summary')}")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(metric_card(T("deal_total_cost"), fmt(total_cost)), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card(T("deal_cash_component"), fmt(cash_component)), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card(T("deal_stock_component"), fmt(stock_component)), unsafe_allow_html=True)
    with mc4:
        st.markdown(metric_card(T("deal_new_shares"), f"{new_shares:,.1f}M"), unsafe_allow_html=True)

    # Financing sources chart
    st.markdown(f"#### {T('deal_financing')}")
    sources = {
        T("deal_debt_raised"): new_debt,
        T("deal_equity_issued"): stock_component,
        T("deal_existing_cash"): max(0, cash_component - new_debt),
    }
    # Only show non-zero
    sources = {k: v for k, v in sources.items() if v > 0}
    if sources:
        fig_pie = go.Figure(go.Pie(
            labels=list(sources.keys()),
            values=list(sources.values()),
            marker=dict(colors=["#1a56db", "#60a5fa", "#bfdbfe"]),
            textinfo="label+percent",
            hole=0.4,
        ))
        fig_pie.update_layout(
            height=340,
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
            margin=dict(t=20, b=20),
            showlegend=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 5: PRO-FORMA
# ═════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    with st.expander(f"6.  {T('pf_title')}", expanded=True):
        st.caption(T("pf_cap"))

        c1, c2 = st.columns(2)
        with c1:
            st.number_input(T("pf_da_pct_rev"), min_value=0.0, max_value=50.0,
                            step=0.5, format="%.1f", key="ma_pf_da_pct")
        with c2:
            st.number_input(T("pf_interest_new_debt"), min_value=0.0, max_value=50.0,
                            step=0.5, format="%.1f", key="ma_pf_interest_new_debt")

    # ── Pro-forma calculations ──────────────────────────────────────────────
    acq_rev = get("ma_acq_revenue")
    acq_ebitda = get("ma_acq_ebitda")
    acq_ni = get("ma_acq_net_income")
    acq_shares_total = get("ma_acq_shares")
    tax_rate = get("ma_acq_tax_rate") / 100
    da_pct = get("ma_pf_da_pct") / 100
    interest_rate_new = get("ma_pf_interest_new_debt") / 100

    # Acquirer standalone
    acq_da = acq_rev * da_pct
    acq_ebit = acq_ebitda - acq_da
    # Back-calculate acquirer interest from NI: NI = (EBIT - Interest)(1 - tax)
    # => Interest = EBIT - NI/(1-tax)
    acq_interest = acq_ebit - (acq_ni / (1 - tax_rate)) if tax_rate < 1 else 0
    acq_ebt = acq_ebit - acq_interest
    acq_taxes = acq_ebt * tax_rate
    acq_ni_calc = acq_ebt - acq_taxes

    # Target standalone
    tgt_da = tgt_rev * da_pct
    tgt_ebit = tgt_ebitda - tgt_da
    # Similar back-calc for target interest
    tgt_interest = tgt_ebit - (tgt_ni / (1 - tax_rate)) if tax_rate < 1 else 0
    tgt_ebt = tgt_ebit - tgt_interest
    tgt_taxes = tgt_ebt * tax_rate
    tgt_ni_calc = tgt_ebt - tgt_taxes

    # Synergies (year 1 — partial realization)
    syn_rev_yr1_pct = min(1.0, 6 / syn_rev_phase) if syn_rev_phase > 0 else 1.0
    syn_cost_yr1_pct = min(1.0, 6 / syn_cost_phase) if syn_cost_phase > 0 else 1.0
    syn_rev_yr1 = combined_rev * syn_rev_pct * syn_rev_prob * syn_rev_yr1_pct
    syn_cost_yr1 = syn_cost_abs * syn_cost_prob * syn_cost_yr1_pct
    syn_ebitda = syn_rev_yr1 + syn_cost_yr1

    # Adjustments: new debt interest
    adj_interest = new_debt * interest_rate_new
    adj_ebitda = 0.0

    # Combined
    comb_rev = acq_rev + tgt_rev + syn_rev_yr1
    comb_ebitda = acq_ebitda + tgt_ebitda + syn_ebitda + adj_ebitda
    comb_da = comb_rev * da_pct
    comb_ebit = comb_ebitda - comb_da
    comb_interest = acq_interest + tgt_interest + adj_interest
    comb_ebt = comb_ebit - comb_interest
    comb_taxes = max(0, comb_ebt * tax_rate)
    comb_ni = comb_ebt - comb_taxes

    # EPS calculation
    pro_forma_shares = acq_shares_total + new_shares
    acq_eps_before = acq_ni / acq_shares_total if acq_shares_total > 0 else 0
    eps_combined = comb_ni / pro_forma_shares if pro_forma_shares > 0 else 0
    accretion_per_share = eps_combined - acq_eps_before
    accretion_pct = (accretion_per_share / acq_eps_before * 100) if acq_eps_before != 0 else 0

    # Build the pro-forma table
    rows = [
        (T("pf_revenue"),     acq_rev,      tgt_rev,      syn_rev_yr1,   0.0,           comb_rev),
        (T("pf_ebitda"),      acq_ebitda,   tgt_ebitda,   syn_ebitda,    adj_ebitda,    comb_ebitda),
        (T("pf_dep_amort"),   -acq_da,      -tgt_da,      0.0,           0.0,           -comb_da),
        (T("pf_ebit"),        acq_ebit,     tgt_ebit,     syn_ebitda,    0.0,           comb_ebit),
        (T("pf_interest"),    -acq_interest,-tgt_interest, 0.0,          -adj_interest,  -comb_interest),
        (T("pf_ebt"),         acq_ebt,      tgt_ebt,      syn_ebitda,   -adj_interest,  comb_ebt),
        (T("pf_taxes"),       -acq_taxes,   -tgt_taxes,   0.0,           0.0,           -comb_taxes),
        (T("pf_net_income"),  acq_ni_calc,  tgt_ni_calc,  syn_ebitda*(1-tax_rate), -adj_interest*(1-tax_rate), comb_ni),
    ]

    pf_df = pd.DataFrame(rows, columns=[
        "", T("pf_acquirer"), T("pf_target"), T("pf_synergies"),
        T("pf_adjustments"), T("pf_combined"),
    ])
    pf_df = pf_df.set_index("")

    # Format for display
    pf_display = pf_df.copy()
    for col in pf_display.columns:
        pf_display[col] = pf_display[col].apply(lambda v: f"{v:,.0f}")

    # Highlight rows
    subtotal_rows = {T("pf_ebitda"), T("pf_ebit"), T("pf_ebt"), T("pf_net_income")}

    def style_pf(row):
        if row.name in subtotal_rows:
            return ["background:#dbeafe;font-weight:700;color:#1e3a8a"] * len(row)
        return [""] * len(row)

    st.markdown(f"#### {T('pf_title')}")
    styled_html = pf_display.style.apply(style_pf, axis=1).to_html()
    st.markdown(f'<div class="df-styled">{styled_html}</div>', unsafe_allow_html=True)

    # EPS summary
    st.markdown("---")
    st.markdown(f"#### {T('pf_accretion')}")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(metric_card(
            f"EPS ({T('pf_acquirer')})",
            f"{acq_eps_before:,.2f}",
        ), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card(
            f"EPS ({T('pf_combined')})",
            f"{eps_combined:,.2f}",
        ), unsafe_allow_html=True)
    with mc3:
        cls = "metric-card-green" if accretion_per_share >= 0 else "metric-card-red"
        st.markdown(metric_card(
            T("pf_accretion"),
            f"{accretion_per_share:+,.4f}",
            card_class=cls,
        ), unsafe_allow_html=True)
    with mc4:
        cls = "metric-card-green" if accretion_pct >= 0 else "metric-card-red"
        st.markdown(metric_card(
            T("pf_accretion_pct"),
            f"{accretion_pct:+,.2f}%",
            card_class=cls,
        ), unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 6: RESULTS
# ═════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown(f"#### {T('res_title')}")
    st.caption(T("res_cap"))

    # Key metrics
    premium_value = purchase_price - primary_eq
    combined_ebitda_w_syn = acq_ebitda + tgt_ebitda + total_annual_synergy
    total_debt_combined = tgt_debt + new_debt
    leverage = total_debt_combined / combined_ebitda_w_syn if combined_ebitda_w_syn > 0 else 0

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(metric_card(T("res_ev"), fmt(primary_ev)), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card(T("res_equity_val"), fmt(primary_eq)), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card(T("res_premium"), fmt(premium_value)), unsafe_allow_html=True)

    mc4, mc5, mc6 = st.columns(3)
    with mc4:
        cls = "metric-card-green" if accretion_pct >= 0 else "metric-card-red"
        st.markdown(metric_card(T("res_accretion_dilution"), f"{accretion_per_share:+,.4f}", card_class=cls), unsafe_allow_html=True)
    with mc5:
        cls = "metric-card-green" if accretion_pct >= 0 else "metric-card-red"
        st.markdown(metric_card(T("res_accretion_dilution_pct"), f"{accretion_pct:+,.2f}%", card_class=cls), unsafe_allow_html=True)
    with mc6:
        st.markdown(metric_card(T("res_synergy_npv"), fmt(syn_npv), card_class="metric-card-green" if syn_npv > 0 else "metric-card"), unsafe_allow_html=True)

    mc7, mc8, mc9 = st.columns(3)
    with mc7:
        st.markdown(metric_card(T("res_total_cost"), fmt(total_cost)), unsafe_allow_html=True)
    with mc8:
        st.markdown(metric_card(T("res_combined_ebitda"), fmt(combined_ebitda_w_syn)), unsafe_allow_html=True)
    with mc9:
        lev_cls = "metric-card-green" if leverage < 3.0 else ("metric-card-red" if leverage > 5.0 else "metric-card")
        st.markdown(metric_card(T("res_leverage"), f"{leverage:.1f}x", card_class=lev_cls), unsafe_allow_html=True)

    # ── Verdict ─────────────────────────────────────────────────────────────
    st.markdown(f"#### {T('res_verdict_title')}")
    if accretion_pct > 1.0:
        st.markdown(f"""<div class="veredicto-verde">
            <div class="veredicto-titulo">{T('res_accretive')}</div>
        </div>""", unsafe_allow_html=True)
    elif accretion_pct < -1.0:
        st.markdown(f"""<div class="veredicto-vermelho">
            <div class="veredicto-titulo">{T('res_dilutive')}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="veredicto-amarelo">
            <div class="veredicto-titulo">{T('res_neutral')}</div>
        </div>""", unsafe_allow_html=True)

    # ── EV Waterfall Chart ──────────────────────────────────────────────────
    st.markdown(f"#### {T('res_waterfall')}")
    wf_labels = ["EBITDA", f"x {ev_ebitda_mult:.1f}", "= EV",
                 f"- {'Divida' if lang == 'PT' else 'Debt'}", f"+ {'Caixa' if lang == 'PT' else 'Cash'}",
                 f"= Equity", f"+ {'Premio' if lang == 'PT' else 'Premium'}",
                 f"= {'Preco' if lang == 'PT' else 'Price'}"]
    wf_values = [tgt_ebitda, primary_ev - tgt_ebitda, 0,
                 -tgt_debt, tgt_cash, 0,
                 premium_value, 0]
    wf_measures = ["absolute", "relative", "total",
                   "relative", "relative", "total",
                   "relative", "total"]

    fig_wf = go.Figure(go.Waterfall(
        x=wf_labels, y=wf_values, measure=wf_measures,
        connector=dict(line=dict(color="#1a56db", width=1)),
        increasing=dict(marker=dict(color="#1a56db")),
        decreasing=dict(marker=dict(color="#dc2626")),
        totals=dict(marker=dict(color="#1e3a8a")),
        text=[fmt(abs(v)) if v != 0 else "" for v in
              [tgt_ebitda, primary_ev - tgt_ebitda, primary_ev,
               tgt_debt, tgt_cash, primary_eq,
               premium_value, purchase_price]],
        textposition="outside",
    ))
    fig_wf.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        margin=dict(t=30, b=40),
        showlegend=False,
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── Sensitivity table: Accretion/Dilution vs Multiple & % Cash ──────────
    st.markdown(f"#### {T('res_sensitivity')}")
    mult_range = np.arange(max(1, ev_ebitda_mult - 3), ev_ebitda_mult + 4, 1.0)
    cash_range = np.arange(0, 101, 20)

    sens_data = {}
    for mult in mult_range:
        col_vals = []
        for cash_pct_s in cash_range:
            # Recalculate for this scenario
            s_ev = tgt_ebitda * mult
            s_eq = s_ev - tgt_debt + tgt_cash
            s_pp = s_eq * (1 + premium_pct)
            s_stock = s_pp * ((100 - cash_pct_s) / 100)
            s_new_shares = (s_stock / acq_share_price) / 1e6 if acq_share_price > 0 else 0
            s_pf_shares = acq_shares_total + s_new_shares

            # Simplified combined NI (use same structure)
            s_tgt_ebitda_val = tgt_ebitda  # target EBITDA unchanged
            s_comb_ebitda = acq_ebitda + s_tgt_ebitda_val + syn_ebitda
            s_comb_da = (acq_rev + tgt_rev + syn_rev_yr1) * da_pct
            s_comb_ebit = s_comb_ebitda - s_comb_da
            s_adj_int = new_debt * interest_rate_new
            s_comb_int = acq_interest + tgt_interest + s_adj_int
            s_comb_ebt = s_comb_ebit - s_comb_int
            s_comb_tax = max(0, s_comb_ebt * tax_rate)
            s_comb_ni = s_comb_ebt - s_comb_tax

            s_eps = s_comb_ni / s_pf_shares if s_pf_shares > 0 else 0
            s_accretion = ((s_eps - acq_eps_before) / acq_eps_before * 100) if acq_eps_before != 0 else 0
            col_vals.append(s_accretion)
        sens_data[f"{mult:.0f}x"] = col_vals

    sens_df = pd.DataFrame(sens_data, index=[f"{int(c)}% Cash" for c in cash_range]).T
    sens_df.index.name = "EV/EBITDA"

    # Color code the cells
    def color_sens(val):
        if val > 2:
            return "background:#d4edda;color:#155724;font-weight:700"
        elif val > 0:
            return "background:#e8f5e9;color:#2e7d32"
        elif val > -2:
            return "background:#fff3cd;color:#856404"
        else:
            return "background:#f8d7da;color:#721c24;font-weight:700"

    sens_display = sens_df.copy()
    for col in sens_display.columns:
        sens_display[col] = sens_display[col].apply(lambda v: f"{v:+.1f}%")

    # Use map (pandas >=1.4) with fallback to applymap for older versions
    try:
        styled_sens = sens_df.style.map(color_sens).format("{:+.1f}%")
    except AttributeError:
        styled_sens = sens_df.style.applymap(color_sens).format("{:+.1f}%")
    sens_html = styled_sens.to_html()
    st.markdown(f'<div class="sens-tbl">{sens_html}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    M&A Financial Model &middot; Built with Streamlit
</div>
""", unsafe_allow_html=True)
