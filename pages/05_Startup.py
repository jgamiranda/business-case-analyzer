import datetime
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Startup", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "page_title": "Modelagem de Startup com Cap Table",
    "lang_label": "Idioma",
    # Tabs
    "tab_company": "  Empresa  ",
    "tab_captable": "  Cap Table  ",
    "tab_revenue": "  Receita  ",
    "tab_unit_econ": "  Unit Economics  ",
    "tab_runway": "  Runway  ",
    "tab_results": "  Resultados  ",
    # Company
    "company_name": "Nome da empresa",
    "company_name_ph": "Ex: TechCo Brasil",
    "company_stage": "Estagio",
    "stages": ["Pre-Seed", "Seed", "Serie A", "Serie B", "Serie C", "Growth"],
    "founding_date": "Data de fundacao",
    "n_founders": "Numero de fundadores",
    "shares_per_founder": "Acoes por fundador",
    "total_founder_shares": "Total de acoes dos fundadores",
    "company_saved": "Dados da empresa salvos.",
    # Cap Table
    "ct_title": "Cap Table — Rodadas de Investimento",
    "ct_round": "Rodada",
    "ct_pre_money": "Valuation pre-money (USD)",
    "ct_raised": "Capital levantado (USD)",
    "ct_esop": "Pool ESOP (%)",
    "ct_include": "Incluir rodada",
    "ct_ownership": "Tabela de Participacao",
    "ct_shareholder": "Acionista",
    "ct_shares": "Acoes",
    "ct_pct": "Participacao (%)",
    "ct_dilution": "Diluicao vs. Anterior (%)",
    "ct_post_money": "Valuation pos-money",
    "ct_price_share": "Preco por acao",
    "ct_new_shares": "Novas acoes emitidas",
    "ct_esop_shares": "Acoes ESOP",
    "ct_founders": "Fundadores",
    "ct_esop_pool": "Pool ESOP",
    "ct_round_summary": "Resumo da Rodada",
    # Revenue
    "rev_title": "Projecao de Receita (MRR / ARR)",
    "rev_initial_mrr": "MRR inicial (USD)",
    "rev_growth": "Taxa de crescimento mensal (%)",
    "rev_churn": "Taxa de churn mensal (%)",
    "rev_months": "Meses de projecao",
    "rev_mrr_chart": "Evolucao do MRR",
    "rev_arr_chart": "Evolucao do ARR",
    "rev_month": "Mes",
    "rev_mrr": "MRR (USD)",
    "rev_arr": "ARR (USD)",
    "rev_net_growth": "Crescimento liquido mensal",
    # Unit Economics
    "ue_title": "Unit Economics",
    "ue_cac": "CAC — Custo de Aquisicao de Cliente (USD)",
    "ue_arpu": "ARPU — Receita Media por Usuario (USD/mes)",
    "ue_churn": "Taxa de Churn Mensal (%)",
    "ue_ltv": "LTV — Lifetime Value (USD)",
    "ue_ltv_cac": "LTV / CAC",
    "ue_payback": "Payback (meses)",
    "ue_ltv_formula": "LTV = ARPU / Churn Mensal",
    "ue_payback_formula": "Payback = CAC / ARPU",
    "ue_healthy": "Saudavel (>3x)",
    "ue_warning": "Atencao (1-3x)",
    "ue_critical": "Critico (<1x)",
    "ue_benchmark": "Benchmark SaaS",
    "ue_gross_margin": "Margem bruta mensal (USD)",
    # Runway
    "rw_title": "Analise de Runway",
    "rw_burn": "Burn rate mensal (USD)",
    "rw_cash": "Caixa atual (USD)",
    "rw_months": "Meses de runway",
    "rw_cashout": "Data de cash-out estimada",
    "rw_chart": "Projecao de Caixa",
    "rw_remaining": "Caixa restante (USD)",
    "rw_month": "Mes",
    "rw_infinite": "Sustentavel (burn <= 0)",
    "rw_danger": "Critico — menos de 6 meses",
    "rw_caution": "Atencao — menos de 12 meses",
    "rw_ok": "Saudavel — mais de 12 meses",
    "rw_net_burn": "Burn liquido mensal (USD)",
    "rw_revenue_offset": "Incluir receita para reduzir burn",
    # Results
    "res_title": "Dashboard de Metricas",
    "res_ownership": "Resumo de Participacao",
    "res_valuations": "Valuations Implicitos por Rodada",
    "res_revenue_milestones": "Marcos de Receita",
    "res_unit_econ_summary": "Unit Economics",
    "res_runway_summary": "Runway",
    "res_round": "Rodada",
    "res_pre": "Pre-money (USD)",
    "res_post": "Pos-money (USD)",
    "res_raised": "Levantado (USD)",
    "res_price_share": "Preco/Acao (USD)",
    "res_milestone": "Marco",
    "res_month_reached": "Mes atingido",
    "res_value": "Valor",
    "res_mrr_100k": "MRR USD 100k",
    "res_mrr_500k": "MRR USD 500k",
    "res_mrr_1m": "MRR USD 1M",
    "res_arr_1m": "ARR USD 1M",
    "res_arr_10m": "ARR USD 10M",
    "res_not_reached": "Nao atingido no periodo",
    "res_founder_pct": "Participacao dos fundadores",
    "res_final_valuation": "Ultimo valuation pos-money",
},
"EN": {
    "page_title": "Startup Modeling with Cap Table",
    "lang_label": "Language",
    # Tabs
    "tab_company": "  Company  ",
    "tab_captable": "  Cap Table  ",
    "tab_revenue": "  Revenue  ",
    "tab_unit_econ": "  Unit Economics  ",
    "tab_runway": "  Runway  ",
    "tab_results": "  Results  ",
    # Company
    "company_name": "Company name",
    "company_name_ph": "e.g. TechCo Inc.",
    "company_stage": "Stage",
    "stages": ["Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Growth"],
    "founding_date": "Founding date",
    "n_founders": "Number of founders",
    "shares_per_founder": "Shares per founder",
    "total_founder_shares": "Total founder shares",
    "company_saved": "Company data saved.",
    # Cap Table
    "ct_title": "Cap Table — Investment Rounds",
    "ct_round": "Round",
    "ct_pre_money": "Pre-money valuation (USD)",
    "ct_raised": "Capital raised (USD)",
    "ct_esop": "ESOP Pool (%)",
    "ct_include": "Include round",
    "ct_ownership": "Ownership Table",
    "ct_shareholder": "Shareholder",
    "ct_shares": "Shares",
    "ct_pct": "Ownership (%)",
    "ct_dilution": "Dilution vs. Prior (%)",
    "ct_post_money": "Post-money valuation",
    "ct_price_share": "Price per share",
    "ct_new_shares": "New shares issued",
    "ct_esop_shares": "ESOP shares",
    "ct_founders": "Founders",
    "ct_esop_pool": "ESOP Pool",
    "ct_round_summary": "Round Summary",
    # Revenue
    "rev_title": "Revenue Projection (MRR / ARR)",
    "rev_initial_mrr": "Initial MRR (USD)",
    "rev_growth": "Monthly growth rate (%)",
    "rev_churn": "Monthly churn rate (%)",
    "rev_months": "Projection months",
    "rev_mrr_chart": "MRR Evolution",
    "rev_arr_chart": "ARR Evolution",
    "rev_month": "Month",
    "rev_mrr": "MRR (USD)",
    "rev_arr": "ARR (USD)",
    "rev_net_growth": "Net monthly growth",
    # Unit Economics
    "ue_title": "Unit Economics",
    "ue_cac": "CAC — Customer Acquisition Cost (USD)",
    "ue_arpu": "ARPU — Avg Revenue Per User (USD/mo)",
    "ue_churn": "Monthly Churn Rate (%)",
    "ue_ltv": "LTV — Lifetime Value (USD)",
    "ue_ltv_cac": "LTV / CAC",
    "ue_payback": "Payback (months)",
    "ue_ltv_formula": "LTV = ARPU / Monthly Churn",
    "ue_payback_formula": "Payback = CAC / ARPU",
    "ue_healthy": "Healthy (>3x)",
    "ue_warning": "Warning (1-3x)",
    "ue_critical": "Critical (<1x)",
    "ue_benchmark": "SaaS Benchmark",
    "ue_gross_margin": "Monthly gross margin (USD)",
    # Runway
    "rw_title": "Runway Analysis",
    "rw_burn": "Monthly burn rate (USD)",
    "rw_cash": "Current cash (USD)",
    "rw_months": "Runway months",
    "rw_cashout": "Estimated cash-out date",
    "rw_chart": "Cash Projection",
    "rw_remaining": "Remaining cash (USD)",
    "rw_month": "Month",
    "rw_infinite": "Sustainable (burn <= 0)",
    "rw_danger": "Critical — less than 6 months",
    "rw_caution": "Caution — less than 12 months",
    "rw_ok": "Healthy — more than 12 months",
    "rw_net_burn": "Net monthly burn (USD)",
    "rw_revenue_offset": "Include revenue to offset burn",
    # Results
    "res_title": "Metrics Dashboard",
    "res_ownership": "Ownership Summary",
    "res_valuations": "Implied Valuations per Round",
    "res_revenue_milestones": "Revenue Milestones",
    "res_unit_econ_summary": "Unit Economics",
    "res_runway_summary": "Runway",
    "res_round": "Round",
    "res_pre": "Pre-money (USD)",
    "res_post": "Post-money (USD)",
    "res_raised": "Raised (USD)",
    "res_price_share": "Price/Share (USD)",
    "res_milestone": "Milestone",
    "res_month_reached": "Month reached",
    "res_value": "Value",
    "res_mrr_100k": "MRR USD 100k",
    "res_mrr_500k": "MRR USD 500k",
    "res_mrr_1m": "MRR USD 1M",
    "res_arr_1m": "ARR USD 1M",
    "res_arr_10m": "ARR USD 10M",
    "res_not_reached": "Not reached in period",
    "res_founder_pct": "Founder ownership",
    "res_final_valuation": "Latest post-money valuation",
},
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Blue theme (#1a56db)
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
.metric-card-yellow{background:linear-gradient(135deg,#fff3cd 0%,#ffeeba 100%);border-color:#ffc107}
.metric-card-yellow .mc-value{color:#856404}
.startup-header{background:linear-gradient(135deg,#1a56db 0%,#1e429f 100%);border-radius:10px;padding:18px 24px;margin-bottom:16px}
.startup-header h1{color:white !important;font-size:1.6rem;margin:0}
.startup-header p{color:#bfdbfe;font-size:.85rem;margin:4px 0 0 0}
.round-badge{display:inline-block;background:#1a56db;color:white;padding:4px 14px;border-radius:20px;font-weight:700;font-size:.82rem;margin:2px 4px}
.dilution-neg{color:#dc2626;font-weight:700}
.dilution-zero{color:#6b7280;font-weight:600}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "su_company_name": "",
    "su_stage": "Seed",
    "su_founding_date": datetime.date(2024, 1, 1),
    "su_n_founders": 2,
    "su_shares_per_founder": 1_000_000,
    # Cap Table rounds
    "su_seed_on": True, "su_seed_pre": 5_000_000, "su_seed_raised": 1_000_000, "su_seed_esop": 10.0,
    "su_seriesa_on": True, "su_seriesa_pre": 20_000_000, "su_seriesa_raised": 5_000_000, "su_seriesa_esop": 5.0,
    "su_seriesb_on": False, "su_seriesb_pre": 80_000_000, "su_seriesb_raised": 15_000_000, "su_seriesb_esop": 3.0,
    "su_seriesc_on": False, "su_seriesc_pre": 250_000_000, "su_seriesc_raised": 40_000_000, "su_seriesc_esop": 2.0,
    # Revenue
    "su_initial_mrr": 10_000.0,
    "su_growth_rate": 15.0,
    "su_churn_rate": 3.0,
    "su_proj_months": 36,
    # Unit Economics
    "su_cac": 500.0,
    "su_arpu": 100.0,
    "su_ue_churn": 3.0,
    # Runway
    "su_burn_rate": 80_000.0,
    "su_current_cash": 1_000_000.0,
    "su_rw_include_rev": False,
}

for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get(k, d=0.0):
    return st.session_state.get(k, d)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
_hc_title, _hc_lang = st.columns([8, 1])
with _hc_title:
    st.markdown('<div class="startup-header"><h1>Startup Modeling</h1></div>', unsafe_allow_html=True)
with _hc_lang:
    lang_sel = st.segmented_control("lang", ["PT", "EN"], default="PT", key="su_lang",
                                     label_visibility="collapsed")
lang = lang_sel or "PT"
def T(k):
    return _L.get(lang, _L["PT"]).get(k, _L["PT"].get(k, k))

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: format USD
# ─────────────────────────────────────────────────────────────────────────────
def fmt_usd(v, decimals=0):
    if v is None:
        return "---"
    if abs(v) >= 1e9:
        return f"${v/1e9:,.1f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:,.1f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:,.1f}K"
    return f"${v:,.{decimals}f}"

def metric_card(label, value, card_class=""):
    cls = f"metric-card {card_class}" if card_class else "metric-card"
    return f'<div class="{cls}"><div class="mc-label">{label}</div><div class="mc-value">{value}</div></div>'

# ─────────────────────────────────────────────────────────────────────────────
# CAP TABLE ENGINE
# ─────────────────────────────────────────────────────────────────────────────
ROUNDS = [
    ("Seed", "su_seed"),
    ("Series A", "su_seriesa"),
    ("Series B", "su_seriesb"),
    ("Series C", "su_seriesc"),
]

def compute_cap_table():
    """Compute full cap table across all active rounds.
    Returns list of dicts per round with ownership breakdown."""
    n_founders = get("su_n_founders", 2)
    shares_per = get("su_shares_per_founder", 1_000_000)
    founder_shares = int(n_founders * shares_per)

    results = []
    cumulative_shares = {"Founders": founder_shares}
    total_esop = 0

    for round_name, prefix in ROUNDS:
        if not get(f"{prefix}_on", False):
            continue
        pre_money = get(f"{prefix}_pre", 0)
        raised = get(f"{prefix}_raised", 0)
        esop_pct = get(f"{prefix}_esop", 0) / 100.0

        if pre_money <= 0 or raised <= 0:
            continue

        post_money = pre_money + raised
        total_shares_before = sum(cumulative_shares.values())
        price_per_share = pre_money / total_shares_before if total_shares_before > 0 else 1
        new_investor_shares = int(raised / price_per_share) if price_per_share > 0 else 0

        # ESOP: calculated on post-round total
        total_after_investor = total_shares_before + new_investor_shares
        esop_new_shares = int((total_after_investor / (1 - esop_pct)) * esop_pct) - total_esop if esop_pct > 0 else 0
        if esop_new_shares < 0:
            esop_new_shares = 0

        # Update cumulative
        cumulative_shares[round_name] = new_investor_shares
        total_esop += esop_new_shares
        cumulative_shares["ESOP"] = total_esop

        total_all = sum(cumulative_shares.values())

        # Ownership percentages
        ownership = {}
        for sh, cnt in cumulative_shares.items():
            ownership[sh] = (cnt / total_all * 100) if total_all > 0 else 0

        # Calculate dilution (founders only for simplicity)
        prev_total = total_shares_before
        dilution_founders = ((total_all - prev_total) / total_all * 100) if total_all > 0 else 0

        results.append({
            "round_name": round_name,
            "pre_money": pre_money,
            "post_money": post_money,
            "raised": raised,
            "price_per_share": price_per_share,
            "new_investor_shares": new_investor_shares,
            "esop_new_shares": esop_new_shares,
            "total_shares": total_all,
            "cumulative_shares": dict(cumulative_shares),
            "ownership": dict(ownership),
            "dilution_this_round": dilution_founders,
        })

    return results

def compute_revenue():
    """Compute MRR / ARR projection."""
    mrr = get("su_initial_mrr", 10_000)
    growth = get("su_growth_rate", 15.0) / 100.0
    churn = get("su_churn_rate", 3.0) / 100.0
    months = int(get("su_proj_months", 36))

    data = []
    for m in range(months + 1):
        arr = mrr * 12
        data.append({"month": m, "mrr": mrr, "arr": arr})
        net_growth = growth - churn
        mrr = mrr * (1 + net_growth)
    return pd.DataFrame(data)

def compute_unit_economics():
    """Compute unit economics metrics."""
    cac = get("su_cac", 500)
    arpu = get("su_arpu", 100)
    churn = get("su_ue_churn", 3.0) / 100.0

    ltv = arpu / churn if churn > 0 else float('inf')
    ltv_cac = ltv / cac if cac > 0 else float('inf')
    payback = cac / arpu if arpu > 0 else float('inf')
    gross_margin = arpu - (cac * churn)  # simplified monthly margin after amortized CAC

    return {
        "cac": cac,
        "arpu": arpu,
        "churn": churn,
        "ltv": ltv,
        "ltv_cac": ltv_cac,
        "payback": payback,
        "gross_margin": gross_margin,
    }

def compute_runway(rev_df=None):
    """Compute runway analysis."""
    burn = get("su_burn_rate", 80_000)
    cash = get("su_current_cash", 1_000_000)
    include_rev = get("su_rw_include_rev", False)

    data = []
    remaining = cash
    month = 0
    max_months = 60

    while remaining > 0 and month <= max_months:
        revenue_offset = 0
        if include_rev and rev_df is not None and month < len(rev_df):
            revenue_offset = rev_df.iloc[month]["mrr"]
        net_burn = burn - revenue_offset
        data.append({"month": month, "cash": remaining, "net_burn": net_burn})
        remaining -= net_burn
        month += 1

    if remaining > 0:
        data.append({"month": month, "cash": remaining, "net_burn": burn})

    df = pd.DataFrame(data)
    runway_months = len(df) - 1 if remaining <= 0 else None
    return df, runway_months

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
BLUE = "#1a56db"
BLUE_LIGHT = "#dbeafe"
BLUE_MID = "#93bbfd"
GREEN = "#16a34a"
RED = "#dc2626"
YELLOW = "#f59e0b"

def styled_layout(fig, xtitle="", ytitle="", height=400):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color="#374151"),
        xaxis=dict(title=xtitle, gridcolor="#f3f4f6", showgrid=True),
        yaxis=dict(title=ytitle, gridcolor="#e5e7eb", showgrid=True),
        height=height,
        margin=dict(t=30, b=50, l=60, r=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    T("tab_company"), T("tab_captable"), T("tab_revenue"),
    T("tab_unit_econ"), T("tab_runway"), T("tab_results"),
])

# ===================== TAB 1: COMPANY ========================================
with tabs[0]:
    st.subheader(T("tab_company").strip())

    c1, c2 = st.columns(2)
    with c1:
        st.text_input(T("company_name"), placeholder=T("company_name_ph"), key="su_company_name")
        st.selectbox(T("company_stage"), T("stages"), key="su_stage")
        st.date_input(T("founding_date"), key="su_founding_date")
    with c2:
        st.number_input(T("n_founders"), min_value=1, max_value=10, step=1, key="su_n_founders")
        st.number_input(T("shares_per_founder"), min_value=1_000, max_value=100_000_000,
                        step=100_000, key="su_shares_per_founder")
        total = get("su_n_founders", 2) * get("su_shares_per_founder", 1_000_000)
        st.metric(T("total_founder_shares"), f"{int(total):,}")

# ===================== TAB 2: CAP TABLE ======================================
with tabs[1]:
    st.subheader(T("ct_title"))

    round_labels = {"Seed": "Seed", "Series A": "Serie A" if lang == "PT" else "Series A",
                    "Series B": "Serie B" if lang == "PT" else "Series B",
                    "Series C": "Serie C" if lang == "PT" else "Series C"}

    for round_name, prefix in ROUNDS:
        label = round_labels.get(round_name, round_name)
        with st.expander(f"{T('ct_round')}: {label}", expanded=get(f"{prefix}_on", False)):
            st.toggle(T("ct_include"), key=f"{prefix}_on")
            if get(f"{prefix}_on", False):
                r1, r2, r3 = st.columns(3)
                with r1:
                    st.number_input(T("ct_pre_money"), min_value=100_000, max_value=10_000_000_000,
                                    step=1_000_000, key=f"{prefix}_pre", format="%d")
                with r2:
                    st.number_input(T("ct_raised"), min_value=10_000, max_value=5_000_000_000,
                                    step=500_000, key=f"{prefix}_raised", format="%d")
                with r3:
                    st.number_input(T("ct_esop"), min_value=0.0, max_value=30.0,
                                    step=0.5, key=f"{prefix}_esop", format="%.1f")

    # Compute and display
    cap_results = compute_cap_table()

    if cap_results:
        st.markdown("---")
        for i, rnd in enumerate(cap_results):
            label = round_labels.get(rnd["round_name"], rnd["round_name"])
            st.markdown(f'<span class="round-badge">{label}</span>', unsafe_allow_html=True)

            # Round summary metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(metric_card(T("ct_post_money"), fmt_usd(rnd["post_money"])), unsafe_allow_html=True)
            m2.markdown(metric_card(T("ct_price_share"), f"${rnd['price_per_share']:,.4f}"), unsafe_allow_html=True)
            m3.markdown(metric_card(T("ct_new_shares"), f"{rnd['new_investor_shares']:,}"), unsafe_allow_html=True)
            m4.markdown(metric_card(T("ct_esop_shares"), f"{rnd['esop_new_shares']:,}"), unsafe_allow_html=True)

            # Ownership table
            rows = []
            prev_round = cap_results[i - 1] if i > 0 else None
            for sh, pct in rnd["ownership"].items():
                sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
                shares = rnd["cumulative_shares"][sh]
                prev_pct = prev_round["ownership"].get(sh, 0) if prev_round else (100.0 if sh == "Founders" else 0)
                dilution = pct - prev_pct
                rows.append({
                    T("ct_shareholder"): sh_label,
                    T("ct_shares"): f"{shares:,}",
                    T("ct_pct"): f"{pct:.2f}%",
                    T("ct_dilution"): f"{dilution:+.2f}%" if dilution != 0 else "---",
                })

            df_own = pd.DataFrame(rows)
            st.dataframe(df_own, use_container_width=True, hide_index=True)
            st.markdown("")

        # Ownership pie chart for latest round
        latest = cap_results[-1]
        fig_pie = go.Figure(data=[go.Pie(
            labels=[T("ct_founders") if k == "Founders" else (T("ct_esop_pool") if k == "ESOP" else k)
                    for k in latest["ownership"].keys()],
            values=list(latest["ownership"].values()),
            marker=dict(colors=[BLUE, BLUE_MID, GREEN, YELLOW, RED, "#8b5cf6"][:len(latest["ownership"])]),
            textinfo="label+percent",
            hole=0.4,
        )])
        fig_pie.update_layout(
            height=350, margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info(T("ct_include") + " — " + ("Ative ao menos uma rodada." if lang == "PT" else "Enable at least one round."))

# ===================== TAB 3: REVENUE ========================================
with tabs[2]:
    st.subheader(T("rev_title"))

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.number_input(T("rev_initial_mrr"), min_value=0.0, max_value=10_000_000.0,
                        step=1_000.0, key="su_initial_mrr", format="%.0f")
    with r2:
        st.number_input(T("rev_growth"), min_value=0.0, max_value=100.0,
                        step=0.5, key="su_growth_rate", format="%.1f")
    with r3:
        st.number_input(T("rev_churn"), min_value=0.0, max_value=50.0,
                        step=0.5, key="su_churn_rate", format="%.1f")
    with r4:
        st.number_input(T("rev_months"), min_value=6, max_value=120,
                        step=6, key="su_proj_months")

    rev_df = compute_revenue()
    net_g = get("su_growth_rate", 15) - get("su_churn_rate", 3)

    mc1, mc2, mc3 = st.columns(3)
    final_mrr = rev_df.iloc[-1]["mrr"]
    final_arr = rev_df.iloc[-1]["arr"]
    mc1.markdown(metric_card(T("rev_mrr") + f" (M{int(get('su_proj_months', 36))})", fmt_usd(final_mrr)), unsafe_allow_html=True)
    mc2.markdown(metric_card(T("rev_arr") + f" (M{int(get('su_proj_months', 36))})", fmt_usd(final_arr)), unsafe_allow_html=True)
    mc3.markdown(metric_card(T("rev_net_growth"), f"{net_g:.1f}%",
                             "metric-card-green" if net_g > 0 else "metric-card-red"), unsafe_allow_html=True)

    # MRR chart
    fig_mrr = go.Figure()
    fig_mrr.add_trace(go.Scatter(
        x=rev_df["month"], y=rev_df["mrr"],
        mode="lines", fill="tozeroy",
        name="MRR",
        line=dict(color=BLUE, width=2),
        fillcolor="rgba(26,86,219,0.1)",
    ))
    styled_layout(fig_mrr, T("rev_month"), T("rev_mrr"))
    st.plotly_chart(fig_mrr, use_container_width=True)

    # ARR chart
    fig_arr = go.Figure()
    fig_arr.add_trace(go.Scatter(
        x=rev_df["month"], y=rev_df["arr"],
        mode="lines", fill="tozeroy",
        name="ARR",
        line=dict(color=GREEN, width=2),
        fillcolor="rgba(22,163,74,0.1)",
    ))
    styled_layout(fig_arr, T("rev_month"), T("rev_arr"))
    st.plotly_chart(fig_arr, use_container_width=True)

# ===================== TAB 4: UNIT ECONOMICS =================================
with tabs[3]:
    st.subheader(T("ue_title"))

    u1, u2, u3 = st.columns(3)
    with u1:
        st.number_input(T("ue_cac"), min_value=0.0, max_value=100_000.0,
                        step=50.0, key="su_cac", format="%.0f")
    with u2:
        st.number_input(T("ue_arpu"), min_value=0.0, max_value=100_000.0,
                        step=10.0, key="su_arpu", format="%.0f")
    with u3:
        st.number_input(T("ue_churn"), min_value=0.1, max_value=50.0,
                        step=0.5, key="su_ue_churn", format="%.1f")

    ue = compute_unit_economics()

    st.markdown("---")

    # Formula display
    st.markdown(f"**{T('ue_ltv_formula')}** | **{T('ue_payback_formula')}**")

    km1, km2, km3, km4 = st.columns(4)

    # LTV
    ltv_str = fmt_usd(ue["ltv"]) if ue["ltv"] != float('inf') else "∞"
    km1.markdown(metric_card(T("ue_ltv"), ltv_str), unsafe_allow_html=True)

    # LTV/CAC
    if ue["ltv_cac"] == float('inf'):
        ratio_str = "∞"
        ratio_cls = "metric-card-green"
    elif ue["ltv_cac"] >= 3:
        ratio_str = f"{ue['ltv_cac']:.1f}x"
        ratio_cls = "metric-card-green"
    elif ue["ltv_cac"] >= 1:
        ratio_str = f"{ue['ltv_cac']:.1f}x"
        ratio_cls = "metric-card-yellow"
    else:
        ratio_str = f"{ue['ltv_cac']:.1f}x"
        ratio_cls = "metric-card-red"
    km2.markdown(metric_card(T("ue_ltv_cac"), ratio_str, ratio_cls), unsafe_allow_html=True)

    # Payback
    pb_str = f"{ue['payback']:.1f}" if ue["payback"] != float('inf') else "∞"
    km3.markdown(metric_card(T("ue_payback"), pb_str + (" meses" if lang == "PT" else " mo")), unsafe_allow_html=True)

    # CAC
    km4.markdown(metric_card(T("ue_cac").split("—")[0].strip(), fmt_usd(ue["cac"])), unsafe_allow_html=True)

    # Benchmark guidance
    st.markdown("---")
    st.markdown(f"#### {T('ue_benchmark')}")
    bench_data = {
        ("LTV/CAC > 3x", T("ue_healthy")): ue["ltv_cac"] >= 3,
        ("LTV/CAC 1-3x", T("ue_warning")): 1 <= ue["ltv_cac"] < 3,
        ("LTV/CAC < 1x", T("ue_critical")): ue["ltv_cac"] < 1,
    }
    for (metric, label), active in bench_data.items():
        icon = "🟢" if ">" in metric else ("🟡" if "1-3" in metric else "🔴")
        style = "font-weight:700" if active else "color:#9ca3af"
        arrow = " ◄" if active else ""
        st.markdown(f'<span style="{style}">{icon} {metric} — {label}{arrow}</span>', unsafe_allow_html=True)

    # LTV/CAC sensitivity
    st.markdown("---")
    st.markdown(f"#### LTV/CAC — {'Sensibilidade' if lang == 'PT' else 'Sensitivity'}")
    churn_range = [1, 2, 3, 5, 7, 10]
    arpu_range = [50, 100, 200, 500, 1000]
    sens_data = []
    for c in churn_range:
        row = {}
        for a in arpu_range:
            ltv_s = a / (c / 100) if c > 0 else 0
            cac_s = ue["cac"]
            ratio_s = ltv_s / cac_s if cac_s > 0 else 0
            row[f"ARPU ${a}"] = f"{ratio_s:.1f}x"
        sens_data.append(row)
    sens_df = pd.DataFrame(sens_data, index=[f"Churn {c}%" for c in churn_range])
    st.dataframe(sens_df, use_container_width=True)

# ===================== TAB 5: RUNWAY =========================================
with tabs[4]:
    st.subheader(T("rw_title"))

    rw1, rw2 = st.columns(2)
    with rw1:
        st.number_input(T("rw_burn"), min_value=0.0, max_value=10_000_000.0,
                        step=5_000.0, key="su_burn_rate", format="%.0f")
    with rw2:
        st.number_input(T("rw_cash"), min_value=0.0, max_value=1_000_000_000.0,
                        step=50_000.0, key="su_current_cash", format="%.0f")

    st.toggle(T("rw_revenue_offset"), key="su_rw_include_rev")

    rev_df_rw = compute_revenue()
    rw_df, rw_months = compute_runway(rev_df_rw if get("su_rw_include_rev") else None)

    # Metrics
    rm1, rm2, rm3 = st.columns(3)

    if rw_months is None:
        rw_label = T("rw_infinite")
        rw_cls = "metric-card-green"
        cashout_str = "---"
    elif rw_months < 6:
        rw_label = f"{rw_months} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-red"
        cashout_str = (datetime.date.today() + datetime.timedelta(days=rw_months * 30)).strftime("%b %Y")
    elif rw_months < 12:
        rw_label = f"{rw_months} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-yellow"
        cashout_str = (datetime.date.today() + datetime.timedelta(days=rw_months * 30)).strftime("%b %Y")
    else:
        rw_label = f"{rw_months} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-green"
        cashout_str = (datetime.date.today() + datetime.timedelta(days=rw_months * 30)).strftime("%b %Y")

    rm1.markdown(metric_card(T("rw_months"), rw_label, rw_cls), unsafe_allow_html=True)
    rm2.markdown(metric_card(T("rw_cashout"), cashout_str), unsafe_allow_html=True)

    net_burn_initial = rw_df.iloc[0]["net_burn"] if len(rw_df) > 0 else get("su_burn_rate")
    rm3.markdown(metric_card(T("rw_net_burn"), fmt_usd(net_burn_initial)), unsafe_allow_html=True)

    # Status indicator
    if rw_months is None:
        st.success(T("rw_infinite"))
    elif rw_months < 6:
        st.error(T("rw_danger"))
    elif rw_months < 12:
        st.warning(T("rw_caution"))
    else:
        st.success(T("rw_ok"))

    # Runway chart
    fig_rw = go.Figure()
    fig_rw.add_trace(go.Scatter(
        x=rw_df["month"], y=rw_df["cash"],
        mode="lines+markers", fill="tozeroy",
        name=T("rw_remaining"),
        line=dict(color=BLUE, width=2),
        fillcolor="rgba(26,86,219,0.08)",
        marker=dict(size=4),
    ))
    # Zero line
    fig_rw.add_hline(y=0, line_dash="dash", line_color=RED, line_width=1)
    # 6-month danger zone
    if rw_months and rw_months > 6:
        fig_rw.add_vrect(x0=max(0, rw_months - 6), x1=rw_months,
                         fillcolor="rgba(220,53,69,0.07)", line_width=0)
    styled_layout(fig_rw, T("rw_month"), T("rw_remaining"))
    st.plotly_chart(fig_rw, use_container_width=True)

# ===================== TAB 6: RESULTS ========================================
with tabs[5]:
    st.subheader(T("res_title"))
    company_name = get("su_company_name", "") or ("Startup" if lang == "EN" else "Startup")
    st.markdown(f"**{company_name}** | {get('su_stage', 'Seed')} | "
                f"{'Fundada em' if lang == 'PT' else 'Founded'} {get('su_founding_date', '')}")

    cap_results = compute_cap_table()
    rev_df_res = compute_revenue()
    ue_res = compute_unit_economics()
    rw_df_res, rw_months_res = compute_runway(rev_df_res if get("su_rw_include_rev") else None)

    # ── Ownership Summary ──
    st.markdown(f"#### {T('res_ownership')}")
    if cap_results:
        latest = cap_results[-1]
        cols = st.columns(len(latest["ownership"]))
        colors = [BLUE, BLUE_MID, GREEN, YELLOW, RED, "#8b5cf6"]
        for idx, (sh, pct) in enumerate(latest["ownership"].items()):
            sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
            cols[idx].markdown(metric_card(sh_label, f"{pct:.1f}%"), unsafe_allow_html=True)

        # Founder ownership + last valuation
        f1, f2 = st.columns(2)
        founder_pct = latest["ownership"].get("Founders", 0)
        f1.markdown(metric_card(T("res_founder_pct"), f"{founder_pct:.1f}%",
                                "metric-card-green" if founder_pct > 50 else (
                                    "metric-card-yellow" if founder_pct > 20 else "metric-card-red")),
                    unsafe_allow_html=True)
        f2.markdown(metric_card(T("res_final_valuation"), fmt_usd(latest["post_money"])), unsafe_allow_html=True)
    else:
        st.info("---")

    st.markdown("---")

    # ── Valuations per Round ──
    st.markdown(f"#### {T('res_valuations')}")
    if cap_results:
        val_rows = []
        for rnd in cap_results:
            label = round_labels.get(rnd["round_name"], rnd["round_name"])
            val_rows.append({
                T("res_round"): label,
                T("res_pre"): fmt_usd(rnd["pre_money"]),
                T("res_post"): fmt_usd(rnd["post_money"]),
                T("res_raised"): fmt_usd(rnd["raised"]),
                T("res_price_share"): f"${rnd['price_per_share']:,.4f}",
            })
        st.dataframe(pd.DataFrame(val_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Revenue Milestones ──
    st.markdown(f"#### {T('res_revenue_milestones')}")
    milestones = [
        ("res_mrr_100k", "mrr", 100_000),
        ("res_mrr_500k", "mrr", 500_000),
        ("res_mrr_1m", "mrr", 1_000_000),
        ("res_arr_1m", "arr", 1_000_000),
        ("res_arr_10m", "arr", 10_000_000),
    ]
    ms_rows = []
    for key, col, target in milestones:
        hit = rev_df_res[rev_df_res[col] >= target]
        if len(hit) > 0:
            m = int(hit.iloc[0]["month"])
            val = hit.iloc[0][col]
            ms_rows.append({
                T("res_milestone"): T(key),
                T("res_month_reached"): f"M{m}",
                T("res_value"): fmt_usd(val),
            })
        else:
            ms_rows.append({
                T("res_milestone"): T(key),
                T("res_month_reached"): T("res_not_reached"),
                T("res_value"): "---",
            })
    st.dataframe(pd.DataFrame(ms_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Unit Economics Summary ──
    st.markdown(f"#### {T('res_unit_econ_summary')}")
    ue1, ue2, ue3, ue4 = st.columns(4)

    ltv_str = fmt_usd(ue_res["ltv"]) if ue_res["ltv"] != float('inf') else "∞"
    ue1.markdown(metric_card("LTV", ltv_str), unsafe_allow_html=True)

    if ue_res["ltv_cac"] >= 3:
        r_cls = "metric-card-green"
    elif ue_res["ltv_cac"] >= 1:
        r_cls = "metric-card-yellow"
    else:
        r_cls = "metric-card-red"
    r_str = f"{ue_res['ltv_cac']:.1f}x" if ue_res["ltv_cac"] != float('inf') else "∞"
    ue2.markdown(metric_card("LTV/CAC", r_str, r_cls), unsafe_allow_html=True)

    ue3.markdown(metric_card("CAC", fmt_usd(ue_res["cac"])), unsafe_allow_html=True)

    pb_str = f"{ue_res['payback']:.1f} {'meses' if lang == 'PT' else 'mo'}" if ue_res["payback"] != float('inf') else "∞"
    ue4.markdown(metric_card(T("ue_payback"), pb_str), unsafe_allow_html=True)

    st.markdown("---")

    # ── Runway Summary ──
    st.markdown(f"#### {T('res_runway_summary')}")
    rr1, rr2, rr3 = st.columns(3)

    if rw_months_res is None:
        rw_str = T("rw_infinite")
        rw_cls = "metric-card-green"
    elif rw_months_res < 6:
        rw_str = f"{rw_months_res} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-red"
    elif rw_months_res < 12:
        rw_str = f"{rw_months_res} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-yellow"
    else:
        rw_str = f"{rw_months_res} {'meses' if lang == 'PT' else 'months'}"
        rw_cls = "metric-card-green"

    rr1.markdown(metric_card(T("rw_months"), rw_str, rw_cls), unsafe_allow_html=True)
    rr2.markdown(metric_card(T("rw_cash"), fmt_usd(get("su_current_cash"))), unsafe_allow_html=True)
    rr3.markdown(metric_card(T("rw_burn"), fmt_usd(get("su_burn_rate"))), unsafe_allow_html=True)

    # ── Final MRR/ARR ──
    st.markdown("---")
    fm1, fm2 = st.columns(2)
    final_mrr_res = rev_df_res.iloc[-1]["mrr"]
    final_arr_res = rev_df_res.iloc[-1]["arr"]
    fm1.markdown(metric_card(f"MRR (M{int(get('su_proj_months', 36))})", fmt_usd(final_mrr_res)), unsafe_allow_html=True)
    fm2.markdown(metric_card(f"ARR (M{int(get('su_proj_months', 36))})", fmt_usd(final_arr_res)), unsafe_allow_html=True)
