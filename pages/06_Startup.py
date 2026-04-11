import datetime
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Startup", layout="wide")

import sys, os as _os
_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _root not in sys.path: sys.path.insert(0, _root)
import _design_tokens as ds
# ds.inject()  # disabled — conflicts with page-local CSS

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────
_L = {
"PT": {
    "page_title": "Modelagem de Startup com Cap Table",
    "lang_label": "Idioma",
    # Tabs
    "tab_company": "  🏢 Empresa  ",
    "tab_captable": "  📊 Cap Table  ",
    "tab_revenue": "  💰 Receita  ",
    "tab_unit_econ": "  📈 Unit Economics  ",
    "tab_runway": "  ⏳ Runway  ",
    "tab_results": "  🎯 Resultados  ",
    "tab_saas": "  📊 SaaS Metrics  ",
    "tab_cohort": "  👥 Coorte  ",
    "tab_funding": "  🏦 Funding  ",
    "tab_exit": "  🚪 Exit  ",
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
    # SAFEs & Convertible Notes
    "ct_safe_title": "SAFEs e Notas Conversiveis",
    "ct_safe_add": "Adicionar SAFE",
    "ct_note_add": "Adicionar Nota Conversivel",
    "ct_instrument": "Instrumento",
    "ct_val_cap": "Valuation Cap (USD)",
    "ct_discount": "Desconto (%)",
    "ct_principal": "Principal (USD)",
    "ct_interest_rate": "Taxa de Juros (%/ano)",
    "ct_maturity_months": "Vencimento (meses)",
    "ct_mfn": "Clausula MFN",
    "ct_pre_conversion": "Cap Table Pre-Conversao",
    "ct_post_conversion": "Cap Table Pos-Conversao",
    "ct_convert_at": "Converte na proxima rodada precificada",
    # ESOP Vesting
    "ct_vesting_title": "Vesting ESOP",
    "ct_vesting_cliff": "Cliff (meses)",
    "ct_vesting_total": "Vesting total (meses)",
    "ct_vested_shares": "Acoes vestidas",
    "ct_unvested_shares": "Acoes nao vestidas",
    "ct_months_elapsed": "Meses desde fundacao",
    # Liquidation Preferences
    "ct_liq_pref_title": "Preferencias de Liquidacao",
    "ct_liq_multiple": "Multiplo de Liquidacao",
    "ct_liq_participating": "Participante",
    "ct_liq_non_participating": "Nao-participante",
    "ct_anti_dilution": "Protecao Anti-diluicao",
    "ct_weighted_avg": "Media Ponderada",
    "ct_full_ratchet": "Full Ratchet",
    "ct_pro_rata": "Direitos Pro-Rata",
    "ct_waterfall_title": "Analise de Waterfall",
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
    # SaaS Metrics
    "saas_title": "Dashboard de Metricas SaaS",
    "saas_starting_mrr": "MRR Inicial do Periodo (USD)",
    "saas_expansion_mrr": "Expansion MRR (USD)",
    "saas_contraction_mrr": "Contraction MRR (USD)",
    "saas_churned_mrr": "Churned MRR (USD)",
    "saas_new_mrr": "New MRR (USD)",
    "saas_sm_spend": "Gasto S&M trimestre anterior (USD)",
    "saas_ebitda_margin": "Margem EBITDA (%)",
    "saas_rev_growth": "Crescimento de Receita (%)",
    "saas_gross_margin": "Margem Bruta (%)",
    "saas_nrr": "Net Revenue Retention (NRR)",
    "saas_grr": "Gross Revenue Retention (GRR)",
    "saas_magic": "Magic Number",
    "saas_rule40": "Rule of 40",
    "saas_cac_payback": "CAC Payback",
    "saas_quick_ratio": "Quick Ratio",
    "saas_burn_multiple": "Burn Multiple",
    "saas_net_burn": "Burn Liquido Mensal (USD)",
    "saas_net_new_arr": "Net New ARR (USD)",
    # Cohort
    "cohort_title": "Analise de Coorte",
    "cohort_initial": "Clientes iniciais na coorte",
    "cohort_months": "Meses de analise",
    "cohort_n_cohorts": "Numero de coortes",
    "cohort_base_retention": "Retencao base mensal (%)",
    "cohort_decay": "Decaimento da retencao (%/mes)",
    "cohort_arpu": "ARPU por coorte (USD/mes)",
    "cohort_retention_heatmap": "Heatmap de Retencao",
    "cohort_revenue": "Receita por Coorte",
    "cohort_churn_by_age": "Churn por Idade da Coorte",
    "cohort_retention_curve": "Curva de Retencao",
    # Funding
    "fund_title": "Previsao de Necessidade de Funding",
    "fund_eng_headcount": "Headcount Engenharia",
    "fund_sales_headcount": "Headcount Vendas",
    "fund_ga_headcount": "Headcount G&A",
    "fund_eng_salary": "Salario medio Eng (USD/mes)",
    "fund_sales_salary": "Salario medio Vendas (USD/mes)",
    "fund_ga_salary": "Salario medio G&A (USD/mes)",
    "fund_other_opex": "Outros OpEx (USD/mes)",
    "fund_cogs_pct": "COGS (% da receita)",
    "fund_monthly_pl": "P&L Mensal Projetado",
    "fund_headcount_plan": "Plano de Headcount",
    "fund_cash_flow": "Projecao de Fluxo de Caixa",
    "fund_gap": "Gap de Funding",
    "fund_required": "Capital Necessario",
    "fund_runway_target": "Meta de Runway (meses)",
    "fund_recommended": "Recomendado: 18-24 meses de runway",
    # Exit
    "exit_title": "Analise de Exit",
    "exit_arr_at_exit": "ARR no Exit (USD)",
    "exit_multiple_range": "Faixa de Multiplos ARR",
    "exit_waterfall": "Waterfall de Exit",
    "exit_valuation": "Valuation de Exit",
    "exit_proceeds": "Proceeds por Classe",
    "exit_founder_return": "Retorno do Fundador",
    "exit_investor_return": "Retorno do Investidor",
    "exit_irr": "IRR",
    "exit_moic": "MOIC (Multiplo sobre Capital)",
    "exit_years_to_exit": "Anos ate o Exit",
    "exit_scenario": "Cenario de Exit",
    "exit_total_invested": "Total Investido",
},
"EN": {
    "page_title": "Startup Modeling with Cap Table",
    "lang_label": "Language",
    # Tabs
    "tab_company": "  🏢 Company  ",
    "tab_captable": "  📊 Cap Table  ",
    "tab_revenue": "  💰 Revenue  ",
    "tab_unit_econ": "  📈 Unit Economics  ",
    "tab_runway": "  ⏳ Runway  ",
    "tab_results": "  🎯 Results  ",
    "tab_saas": "  📊 SaaS Metrics  ",
    "tab_cohort": "  👥 Cohort  ",
    "tab_funding": "  🏦 Funding  ",
    "tab_exit": "  🚪 Exit  ",
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
    # SAFEs & Convertible Notes
    "ct_safe_title": "SAFEs & Convertible Notes",
    "ct_safe_add": "Add SAFE",
    "ct_note_add": "Add Convertible Note",
    "ct_instrument": "Instrument",
    "ct_val_cap": "Valuation Cap (USD)",
    "ct_discount": "Discount (%)",
    "ct_principal": "Principal (USD)",
    "ct_interest_rate": "Interest Rate (%/yr)",
    "ct_maturity_months": "Maturity (months)",
    "ct_mfn": "MFN Clause",
    "ct_pre_conversion": "Pre-Conversion Cap Table",
    "ct_post_conversion": "Post-Conversion Cap Table",
    "ct_convert_at": "Converts at next priced round",
    # ESOP Vesting
    "ct_vesting_title": "ESOP Vesting",
    "ct_vesting_cliff": "Cliff (months)",
    "ct_vesting_total": "Total vesting (months)",
    "ct_vested_shares": "Vested shares",
    "ct_unvested_shares": "Unvested shares",
    "ct_months_elapsed": "Months since founding",
    # Liquidation Preferences
    "ct_liq_pref_title": "Liquidation Preferences",
    "ct_liq_multiple": "Liquidation Multiple",
    "ct_liq_participating": "Participating",
    "ct_liq_non_participating": "Non-participating",
    "ct_anti_dilution": "Anti-dilution Protection",
    "ct_weighted_avg": "Weighted Average",
    "ct_full_ratchet": "Full Ratchet",
    "ct_pro_rata": "Pro-Rata Rights",
    "ct_waterfall_title": "Waterfall Analysis",
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
    # SaaS Metrics
    "saas_title": "SaaS Metrics Dashboard",
    "saas_starting_mrr": "Starting MRR (USD)",
    "saas_expansion_mrr": "Expansion MRR (USD)",
    "saas_contraction_mrr": "Contraction MRR (USD)",
    "saas_churned_mrr": "Churned MRR (USD)",
    "saas_new_mrr": "New MRR (USD)",
    "saas_sm_spend": "S&M Spend Prior Quarter (USD)",
    "saas_ebitda_margin": "EBITDA Margin (%)",
    "saas_rev_growth": "Revenue Growth (%)",
    "saas_gross_margin": "Gross Margin (%)",
    "saas_nrr": "Net Revenue Retention (NRR)",
    "saas_grr": "Gross Revenue Retention (GRR)",
    "saas_magic": "Magic Number",
    "saas_rule40": "Rule of 40",
    "saas_cac_payback": "CAC Payback",
    "saas_quick_ratio": "Quick Ratio",
    "saas_burn_multiple": "Burn Multiple",
    "saas_net_burn": "Monthly Net Burn (USD)",
    "saas_net_new_arr": "Net New ARR (USD)",
    # Cohort
    "cohort_title": "Cohort Analysis",
    "cohort_initial": "Initial customers per cohort",
    "cohort_months": "Analysis months",
    "cohort_n_cohorts": "Number of cohorts",
    "cohort_base_retention": "Base monthly retention (%)",
    "cohort_decay": "Retention decay (%/month)",
    "cohort_arpu": "ARPU per cohort (USD/mo)",
    "cohort_retention_heatmap": "Retention Heatmap",
    "cohort_revenue": "Revenue by Cohort",
    "cohort_churn_by_age": "Churn by Cohort Age",
    "cohort_retention_curve": "Retention Curve",
    # Funding
    "fund_title": "Funding Requirement Forecast",
    "fund_eng_headcount": "Engineering Headcount",
    "fund_sales_headcount": "Sales Headcount",
    "fund_ga_headcount": "G&A Headcount",
    "fund_eng_salary": "Avg Engineering Salary (USD/mo)",
    "fund_sales_salary": "Avg Sales Salary (USD/mo)",
    "fund_ga_salary": "Avg G&A Salary (USD/mo)",
    "fund_other_opex": "Other OpEx (USD/mo)",
    "fund_cogs_pct": "COGS (% of revenue)",
    "fund_monthly_pl": "Monthly P&L Projection",
    "fund_headcount_plan": "Headcount Plan",
    "fund_cash_flow": "Cash Flow Projection",
    "fund_gap": "Funding Gap",
    "fund_required": "Required Capital",
    "fund_runway_target": "Target Runway (months)",
    "fund_recommended": "Recommended: 18-24 months runway",
    # Exit
    "exit_title": "Exit Analysis",
    "exit_arr_at_exit": "ARR at Exit (USD)",
    "exit_multiple_range": "ARR Multiple Range",
    "exit_waterfall": "Exit Waterfall",
    "exit_valuation": "Exit Valuation",
    "exit_proceeds": "Proceeds by Class",
    "exit_founder_return": "Founder Return",
    "exit_investor_return": "Investor Return",
    "exit_irr": "IRR",
    "exit_moic": "MOIC (Multiple on Invested Capital)",
    "exit_years_to_exit": "Years to Exit",
    "exit_scenario": "Exit Scenario",
    "exit_total_invested": "Total Invested",
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
    # SAFEs & Convertible Notes
    "su_n_safes": 0,
    "su_n_notes": 0,
    # ESOP Vesting
    "su_vesting_cliff": 12,
    "su_vesting_total": 48,
    "su_months_elapsed": 18,
    # Liquidation Preferences
    "su_liq_multiple": 1.0,
    "su_liq_type": "Non-participating",
    "su_anti_dilution": "Weighted Average",
    "su_pro_rata": True,
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
    # SaaS Metrics
    "su_saas_starting_mrr": 50_000.0,
    "su_saas_new_mrr": 12_000.0,
    "su_saas_expansion_mrr": 5_000.0,
    "su_saas_contraction_mrr": 2_000.0,
    "su_saas_churned_mrr": 3_000.0,
    "su_saas_sm_spend": 150_000.0,
    "su_saas_ebitda_margin": -20.0,
    "su_saas_rev_growth": 80.0,
    "su_saas_gross_margin_pct": 75.0,
    "su_saas_net_burn": 100_000.0,
    "su_saas_net_new_arr": 144_000.0,
    # Cohort
    "su_cohort_initial": 100,
    "su_cohort_months": 12,
    "su_cohort_n": 6,
    "su_cohort_base_retention": 90.0,
    "su_cohort_decay": 1.0,
    "su_cohort_arpu": 100.0,
    # Funding
    "su_fund_eng_hc": 8,
    "su_fund_sales_hc": 4,
    "su_fund_ga_hc": 3,
    "su_fund_eng_sal": 12_000.0,
    "su_fund_sales_sal": 8_000.0,
    "su_fund_ga_sal": 7_000.0,
    "su_fund_other_opex": 15_000.0,
    "su_fund_cogs_pct": 25.0,
    "su_fund_runway_target": 18,
    # Exit
    "su_exit_arr": 10_000_000.0,
    "su_exit_years": 5,
}

for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get(k, d=0.0):
    return st.session_state.get(k, d)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
_hc_title, _hc_dark, _hc_lang = st.columns([8, 1, 1])
with _hc_title:
    st.markdown(
        "<style>.main-title{font-size:2.1rem;font-weight:800;color:#1a56db;"
        "margin-bottom:0.2rem;letter-spacing:-0.5px}"
        ".subtitle{font-size:1rem;color:#6b7280;margin-bottom:1.4rem}</style>"
        '<div class="main-title">Startup Modeling</div>',
        unsafe_allow_html=True)
with _hc_dark:
    dark_mode = st.toggle("🌙", value=st.session_state.get("su_dark_mode", False), key="su_dark_mode")
with _hc_lang:
    lang_sel = st.segmented_control("lang", ["PT", "EN"], default="PT", key="su_lang",
                                     label_visibility="collapsed")
lang = lang_sel or "PT"
def T(k):
    return _L.get(lang, _L["PT"]).get(k, _L["PT"].get(k, k))

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


def compute_safe_conversion(cap_results, safes, notes):
    """Convert SAFEs and Convertible Notes at the first priced round."""
    if not cap_results or (not safes and not notes):
        return cap_results, []

    first_round = cap_results[0]
    price_per_share = first_round["price_per_share"]
    pre_money = first_round["pre_money"]
    post_money = first_round["post_money"]

    converted = []

    for s in safes:
        val_cap = s.get("val_cap", pre_money)
        discount = s.get("discount", 0) / 100.0
        amount = s.get("amount", 0)

        # Effective price: min of (val_cap price, discounted price)
        total_shares_at_cap = first_round["total_shares"]
        cap_price = val_cap / total_shares_at_cap if total_shares_at_cap > 0 and val_cap > 0 else price_per_share
        discount_price = price_per_share * (1 - discount)
        effective_price = min(cap_price, discount_price) if val_cap > 0 else discount_price
        if effective_price <= 0:
            effective_price = price_per_share

        new_shares = int(amount / effective_price)
        converted.append({
            "type": "SAFE",
            "amount": amount,
            "effective_price": effective_price,
            "shares": new_shares,
            "val_cap": val_cap,
            "discount": s.get("discount", 0),
        })

    for n in notes:
        principal = n.get("principal", 0)
        interest_rate = n.get("interest_rate", 0) / 100.0
        maturity_months = n.get("maturity_months", 24)
        val_cap = n.get("val_cap", pre_money)
        discount = n.get("discount", 0) / 100.0

        # Accrued interest
        accrued = principal * interest_rate * (maturity_months / 12.0)
        total_owed = principal + accrued

        total_shares_at_cap = first_round["total_shares"]
        cap_price = val_cap / total_shares_at_cap if total_shares_at_cap > 0 and val_cap > 0 else price_per_share
        discount_price = price_per_share * (1 - discount)
        effective_price = min(cap_price, discount_price) if val_cap > 0 else discount_price
        if effective_price <= 0:
            effective_price = price_per_share

        new_shares = int(total_owed / effective_price)
        converted.append({
            "type": "Conv. Note",
            "amount": principal,
            "accrued_interest": accrued,
            "total_owed": total_owed,
            "effective_price": effective_price,
            "shares": new_shares,
            "val_cap": val_cap,
            "discount": n.get("discount", 0),
        })

    return cap_results, converted


def compute_vesting(total_esop_shares, cliff_months, total_months, months_elapsed):
    """Compute vested vs unvested ESOP shares (4yr with 1yr cliff, monthly vesting)."""
    if months_elapsed < cliff_months:
        return 0, total_esop_shares
    # At cliff: vest cliff_months worth
    monthly_vest = total_esop_shares / total_months if total_months > 0 else 0
    vested = int(min(months_elapsed, total_months) * monthly_vest)
    vested = min(vested, total_esop_shares)
    unvested = total_esop_shares - vested
    return vested, unvested


def compute_waterfall(exit_value, cap_results, converted_instruments, liq_multiple, liq_type):
    """Compute liquidation waterfall at a given exit value.
    Returns dict of {shareholder: payout}."""
    if not cap_results:
        return {}

    latest = cap_results[-1]
    ownership = latest["ownership"]
    cumulative_shares = latest["cumulative_shares"]
    total_shares = latest["total_shares"]

    # Add converted instrument shares
    for ci in converted_instruments:
        name = f"{ci['type']} Holder"
        sh = ci.get("shares", 0)
        cumulative_shares[name] = cumulative_shares.get(name, 0) + sh
        total_shares += sh

    # Recalculate ownership
    for sh in cumulative_shares:
        ownership[sh] = (cumulative_shares[sh] / total_shares * 100) if total_shares > 0 else 0

    remaining = exit_value
    payouts = {sh: 0.0 for sh in cumulative_shares}

    # Step 1: Liquidation preferences for investors (not founders, not ESOP)
    investor_rounds = [r for r in cumulative_shares if r not in ("Founders", "ESOP") and "SAFE" not in r and "Conv." not in r]
    # Reverse order (later rounds have seniority)
    investor_rounds_ordered = list(reversed(investor_rounds))

    for inv_round in investor_rounds_ordered:
        # Find how much was raised in this round
        invested = 0
        for rnd in cap_results:
            if rnd["round_name"] == inv_round:
                invested = rnd["raised"]
                break

        liq_pref_amount = invested * liq_multiple
        payout = min(liq_pref_amount, remaining)
        payouts[inv_round] = payout
        remaining -= payout
        if remaining <= 0:
            break

    # SAFEs / Notes liquidation preference (1x by default)
    for ci in converted_instruments:
        name = f"{ci['type']} Holder"
        invested = ci.get("amount", 0)
        liq_pref_amount = invested * liq_multiple
        payout = min(liq_pref_amount, remaining)
        payouts[name] = payouts.get(name, 0) + payout
        remaining -= payout
        if remaining <= 0:
            break

    if remaining <= 0:
        return payouts

    # Step 2: Distribute remaining
    if liq_type == "Participating" or liq_type == "Participante":
        # Participating: investors get liq pref + pro-rata of remainder
        for sh, cnt in cumulative_shares.items():
            pct = cnt / total_shares if total_shares > 0 else 0
            payouts[sh] += remaining * pct
    else:
        # Non-participating: investors choose max(liq pref, pro-rata of total)
        # Recalculate: see if pro-rata of full exit > liq pref
        for inv_round in investor_rounds_ordered:
            cnt = cumulative_shares.get(inv_round, 0)
            pct = cnt / total_shares if total_shares > 0 else 0
            pro_rata_full = exit_value * pct

            invested = 0
            for rnd in cap_results:
                if rnd["round_name"] == inv_round:
                    invested = rnd["raised"]
                    break
            liq_pref_amount = invested * liq_multiple

            if pro_rata_full > liq_pref_amount:
                # Convert to common: give back liq pref, take pro-rata
                remaining += payouts[inv_round]  # give back liq pref
                payouts[inv_round] = 0

        # Now distribute remaining pro-rata to all converting + founders + ESOP
        converting_shares = total_shares
        for sh, cnt in cumulative_shares.items():
            if payouts.get(sh, 0) > 0 and sh not in ("Founders", "ESOP"):
                converting_shares -= cnt  # these keep their liq pref

        for sh, cnt in cumulative_shares.items():
            if sh not in ("Founders", "ESOP") and payouts.get(sh, 0) > 0:
                continue  # keeps liq pref
            pct = cnt / converting_shares if converting_shares > 0 else 0
            payouts[sh] += remaining * pct

    return payouts


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


def compute_saas_metrics():
    """Compute SaaS metrics dashboard values."""
    starting_mrr = get("su_saas_starting_mrr", 50_000)
    new_mrr = get("su_saas_new_mrr", 12_000)
    expansion = get("su_saas_expansion_mrr", 5_000)
    contraction = get("su_saas_contraction_mrr", 2_000)
    churned = get("su_saas_churned_mrr", 3_000)
    sm_spend = get("su_saas_sm_spend", 150_000)
    ebitda_margin = get("su_saas_ebitda_margin", -20)
    rev_growth = get("su_saas_rev_growth", 80)
    gross_margin_pct = get("su_saas_gross_margin_pct", 75) / 100.0
    net_burn = get("su_saas_net_burn", 100_000)
    net_new_arr = get("su_saas_net_new_arr", 144_000)
    cac = get("su_cac", 500)
    arpu = get("su_arpu", 100)

    # NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
    nrr = ((starting_mrr + expansion - contraction - churned) / starting_mrr * 100) if starting_mrr > 0 else 0

    # GRR = (Starting MRR - Contraction - Churn) / Starting MRR
    grr = ((starting_mrr - contraction - churned) / starting_mrr * 100) if starting_mrr > 0 else 0

    # Magic Number = Net New ARR / S&M Spend (prior quarter)
    magic_number = net_new_arr / sm_spend if sm_spend > 0 else 0

    # Rule of 40
    rule_of_40 = rev_growth + ebitda_margin

    # CAC Payback = CAC / (ARPU * Gross Margin)
    cac_payback = cac / (arpu * gross_margin_pct) if (arpu * gross_margin_pct) > 0 else float('inf')

    # Quick Ratio = (New MRR + Expansion) / (Contraction + Churned)
    quick_ratio = (new_mrr + expansion) / (contraction + churned) if (contraction + churned) > 0 else float('inf')

    # Burn Multiple = Net Burn / Net New ARR
    burn_multiple = net_burn / (net_new_arr / 12) if net_new_arr > 0 else float('inf')

    return {
        "nrr": nrr,
        "grr": grr,
        "magic_number": magic_number,
        "rule_of_40": rule_of_40,
        "cac_payback": cac_payback,
        "quick_ratio": quick_ratio,
        "burn_multiple": burn_multiple,
    }


def compute_cohort_data():
    """Compute cohort retention and revenue data."""
    initial = int(get("su_cohort_initial", 100))
    months = int(get("su_cohort_months", 12))
    n_cohorts = int(get("su_cohort_n", 6))
    base_retention = get("su_cohort_base_retention", 90) / 100.0
    decay = get("su_cohort_decay", 1.0) / 100.0
    arpu = get("su_cohort_arpu", 100)

    retention_matrix = []
    revenue_matrix = []

    for c in range(n_cohorts):
        ret_row = []
        rev_row = []
        customers = initial
        for m in range(months):
            if m == 0:
                ret_row.append(100.0)
                rev_row.append(customers * arpu)
            else:
                # Retention decays over time
                monthly_retention = max(base_retention - decay * m, 0.5)
                customers = customers * monthly_retention
                ret_pct = (customers / initial) * 100
                ret_row.append(ret_pct)
                rev_row.append(customers * arpu)
        retention_matrix.append(ret_row)
        revenue_matrix.append(rev_row)

    cohort_labels = [f"{'Coorte' if lang == 'PT' else 'Cohort'} {c+1}" for c in range(n_cohorts)]
    month_labels = [f"M{m}" for m in range(months)]

    ret_df = pd.DataFrame(retention_matrix, index=cohort_labels, columns=month_labels)
    rev_df = pd.DataFrame(revenue_matrix, index=cohort_labels, columns=month_labels)

    return ret_df, rev_df


def compute_funding_forecast():
    """Compute monthly P&L, headcount plan, and funding gap."""
    eng_hc = int(get("su_fund_eng_hc", 8))
    sales_hc = int(get("su_fund_sales_hc", 4))
    ga_hc = int(get("su_fund_ga_hc", 3))
    eng_sal = get("su_fund_eng_sal", 12_000)
    sales_sal = get("su_fund_sales_sal", 8_000)
    ga_sal = get("su_fund_ga_sal", 7_000)
    other_opex = get("su_fund_other_opex", 15_000)
    cogs_pct = get("su_fund_cogs_pct", 25) / 100.0
    runway_target = int(get("su_fund_runway_target", 18))
    cash = get("su_current_cash", 1_000_000)

    rev_df = compute_revenue()
    months = int(get("su_proj_months", 36))

    rows = []
    cumulative_cash = cash
    min_cash = cash
    funding_gap_month = None

    for m in range(min(months + 1, len(rev_df))):
        mrr = rev_df.iloc[m]["mrr"]
        revenue = mrr
        cogs = revenue * cogs_pct
        gross_profit = revenue - cogs

        eng_cost = eng_hc * eng_sal
        sales_cost = sales_hc * sales_sal
        ga_cost = ga_hc * ga_sal
        total_opex = eng_cost + sales_cost + ga_cost + other_opex

        net_income = gross_profit - total_opex
        cumulative_cash += net_income

        if cumulative_cash < 0 and funding_gap_month is None:
            funding_gap_month = m

        min_cash = min(min_cash, cumulative_cash)

        rows.append({
            "month": m,
            "revenue": revenue,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "eng_cost": eng_cost,
            "sales_cost": sales_cost,
            "ga_cost": ga_cost,
            "other_opex": other_opex,
            "total_opex": total_opex,
            "net_income": net_income,
            "cumulative_cash": cumulative_cash,
        })

    df = pd.DataFrame(rows)

    # Calculate required raise
    if min_cash < 0:
        required_raise = abs(min_cash)
    else:
        # Even if cash stays positive, recommend raise for runway_target months
        avg_burn = df["net_income"].mean() if len(df) > 0 else 0
        if avg_burn < 0:
            required_raise = abs(avg_burn) * runway_target
        else:
            required_raise = 0

    # Monthly burn for runway calculation
    avg_monthly_burn = abs(df["net_income"].mean()) if len(df) > 0 and df["net_income"].mean() < 0 else 0
    implied_runway = int(cash / avg_monthly_burn) if avg_monthly_burn > 0 else None

    return df, required_raise, implied_runway, funding_gap_month


# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
BLUE = "#1a56db"
BLUE_LIGHT = "#dbeafe"
BLUE_MID = "#93bbfd"
GREEN = "#16a34a"
RED = "#dc2626"
YELLOW = "#f59e0b"
PURPLE = "#8b5cf6"
ORANGE = "#f97316"
TEAL = "#14b8a6"

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
    T("tab_saas"), T("tab_cohort"), T("tab_funding"), T("tab_exit"),
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

    # ── SAFEs & Convertible Notes ──
    st.markdown("---")
    st.subheader(T("ct_safe_title"))
    st.caption(T("ct_convert_at"))

    safe_col, note_col = st.columns(2)

    # SAFEs
    with safe_col:
        st.markdown(f"**SAFE**")
        n_safes = st.number_input(T("ct_safe_add"), min_value=0, max_value=5, step=1, key="su_n_safes")
        safes = []
        for i in range(int(n_safes)):
            with st.container():
                st.markdown(f"**SAFE #{i+1}**")
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    amt = st.number_input(f"{'Valor' if lang == 'PT' else 'Amount'} (USD)", min_value=0,
                                          max_value=50_000_000, step=25_000,
                                          key=f"su_safe_{i}_amt", value=250_000)
                with sc2:
                    vcap = st.number_input(T("ct_val_cap"), min_value=0, max_value=500_000_000,
                                           step=500_000, key=f"su_safe_{i}_cap", value=8_000_000)
                with sc3:
                    disc = st.number_input(T("ct_discount"), min_value=0.0, max_value=50.0,
                                           step=5.0, key=f"su_safe_{i}_disc", value=20.0)
                mfn = st.toggle(T("ct_mfn"), key=f"su_safe_{i}_mfn")
                safes.append({"amount": amt, "val_cap": vcap, "discount": disc, "mfn": mfn})

    # Convertible Notes
    with note_col:
        st.markdown(f"**{'Nota Conversivel' if lang == 'PT' else 'Convertible Note'}**")
        n_notes = st.number_input(T("ct_note_add"), min_value=0, max_value=5, step=1, key="su_n_notes")
        notes = []
        for i in range(int(n_notes)):
            with st.container():
                st.markdown(f"**Note #{i+1}**")
                nc1, nc2 = st.columns(2)
                with nc1:
                    principal = st.number_input(T("ct_principal"), min_value=0, max_value=50_000_000,
                                                step=25_000, key=f"su_note_{i}_principal", value=500_000)
                    interest = st.number_input(T("ct_interest_rate"), min_value=0.0, max_value=20.0,
                                               step=0.5, key=f"su_note_{i}_interest", value=5.0)
                with nc2:
                    maturity = st.number_input(T("ct_maturity_months"), min_value=6, max_value=60,
                                               step=6, key=f"su_note_{i}_maturity", value=24)
                    ncap = st.number_input(T("ct_val_cap") + f" #{i+1}", min_value=0, max_value=500_000_000,
                                           step=500_000, key=f"su_note_{i}_cap", value=10_000_000)
                ndisc = st.number_input(T("ct_discount") + f" #{i+1}", min_value=0.0, max_value=50.0,
                                        step=5.0, key=f"su_note_{i}_disc", value=20.0)
                notes.append({"principal": principal, "interest_rate": interest,
                              "maturity_months": maturity, "val_cap": ncap, "discount": ndisc})

    # ── ESOP Vesting ──
    st.markdown("---")
    st.subheader(T("ct_vesting_title"))
    vc1, vc2, vc3 = st.columns(3)
    with vc1:
        st.number_input(T("ct_vesting_cliff"), min_value=0, max_value=24, step=1, key="su_vesting_cliff")
    with vc2:
        st.number_input(T("ct_vesting_total"), min_value=12, max_value=72, step=12, key="su_vesting_total")
    with vc3:
        st.number_input(T("ct_months_elapsed"), min_value=0, max_value=120, step=1, key="su_months_elapsed")

    # ── Liquidation Preferences ──
    st.markdown("---")
    st.subheader(T("ct_liq_pref_title"))
    lp1, lp2, lp3 = st.columns(3)
    with lp1:
        st.selectbox(T("ct_liq_multiple"), [1.0, 1.5, 2.0, 3.0], key="su_liq_multiple")
    with lp2:
        liq_opts = [T("ct_liq_non_participating"), T("ct_liq_participating")]
        st.selectbox(T("ct_liq_pref_title"), liq_opts, key="su_liq_type")
    with lp3:
        ad_opts = [T("ct_weighted_avg"), T("ct_full_ratchet")]
        st.selectbox(T("ct_anti_dilution"), ad_opts, key="su_anti_dilution")
    st.toggle(T("ct_pro_rata"), key="su_pro_rata")

    # ── Compute and display ──
    cap_results = compute_cap_table()
    cap_results, converted_instruments = compute_safe_conversion(cap_results, safes, notes)

    if cap_results:
        st.markdown("---")

        # Pre-conversion cap table
        if converted_instruments:
            st.markdown(f"#### {T('ct_pre_conversion')}")

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

        # Post-conversion cap table (if SAFEs/Notes exist)
        if converted_instruments:
            st.markdown(f"#### {T('ct_post_conversion')}")
            latest = cap_results[-1]
            post_shares = dict(latest["cumulative_shares"])
            for ci in converted_instruments:
                name = f"{ci['type']} Holder"
                post_shares[name] = post_shares.get(name, 0) + ci["shares"]

            total_post = sum(post_shares.values())
            post_rows = []
            for sh, cnt in post_shares.items():
                sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
                pct = (cnt / total_post * 100) if total_post > 0 else 0
                post_rows.append({
                    T("ct_shareholder"): sh_label,
                    T("ct_shares"): f"{cnt:,}",
                    T("ct_pct"): f"{pct:.2f}%",
                })
            st.dataframe(pd.DataFrame(post_rows), use_container_width=True, hide_index=True)

            # Converted instruments detail
            ci_rows = []
            for ci in converted_instruments:
                ci_rows.append({
                    T("ct_instrument"): ci["type"],
                    "Amount": fmt_usd(ci.get("amount", ci.get("principal", 0))),
                    T("ct_val_cap"): fmt_usd(ci.get("val_cap", 0)),
                    T("ct_discount"): f"{ci.get('discount', 0)}%",
                    T("ct_price_share"): f"${ci['effective_price']:,.4f}",
                    T("ct_shares"): f"{ci['shares']:,}",
                })
            st.dataframe(pd.DataFrame(ci_rows), use_container_width=True, hide_index=True)

        # ESOP Vesting display
        if cap_results:
            latest = cap_results[-1]
            esop_total = latest["cumulative_shares"].get("ESOP", 0)
            if esop_total > 0:
                st.markdown("---")
                st.markdown(f"#### {T('ct_vesting_title')}")
                vested, unvested = compute_vesting(
                    esop_total,
                    int(get("su_vesting_cliff", 12)),
                    int(get("su_vesting_total", 48)),
                    int(get("su_months_elapsed", 18))
                )
                ev1, ev2, ev3 = st.columns(3)
                ev1.markdown(metric_card(T("ct_vested_shares"), f"{vested:,}", "metric-card-green"), unsafe_allow_html=True)
                ev2.markdown(metric_card(T("ct_unvested_shares"), f"{unvested:,}", "metric-card-yellow"), unsafe_allow_html=True)
                pct_vested = (vested / esop_total * 100) if esop_total > 0 else 0
                ev3.markdown(metric_card("% Vested", f"{pct_vested:.1f}%"), unsafe_allow_html=True)

                # Vesting schedule chart
                vest_months = []
                vest_shares = []
                cliff = int(get("su_vesting_cliff", 12))
                total_vest_m = int(get("su_vesting_total", 48))
                monthly_vest = esop_total / total_vest_m if total_vest_m > 0 else 0
                cumul = 0
                for m in range(total_vest_m + 1):
                    if m < cliff:
                        cumul = 0
                    else:
                        cumul = int(min(m, total_vest_m) * monthly_vest)
                    vest_months.append(m)
                    vest_shares.append(cumul)

                fig_vest = go.Figure()
                fig_vest.add_trace(go.Scatter(
                    x=vest_months, y=vest_shares, mode="lines", fill="tozeroy",
                    name="Vested", line=dict(color=GREEN, width=2),
                    fillcolor="rgba(22,163,74,0.1)",
                ))
                fig_vest.add_vline(x=cliff, line_dash="dash", line_color=RED,
                                   annotation_text="Cliff", annotation_position="top right")
                # Mark current position
                fig_vest.add_vline(x=int(get("su_months_elapsed", 18)), line_dash="dot",
                                   line_color=BLUE, annotation_text="Now", annotation_position="top left")
                styled_layout(fig_vest, T("rev_month"), T("ct_vested_shares"), height=300)
                st.plotly_chart(fig_vest, use_container_width=True)

        # ── Waterfall Analysis ──
        if cap_results:
            st.markdown("---")
            st.markdown(f"#### {T('ct_waterfall_title')}")
            exit_values = [0, 5_000_000, 10_000_000, 25_000_000, 50_000_000,
                           100_000_000, 250_000_000, 500_000_000]
            liq_mult = float(get("su_liq_multiple", 1.0))
            liq_type = get("su_liq_type", "Non-participating")

            waterfall_data = {}
            for ev in exit_values:
                payouts = compute_waterfall(ev, cap_results, converted_instruments, liq_mult, liq_type)
                for sh, payout in payouts.items():
                    if sh not in waterfall_data:
                        waterfall_data[sh] = []
                    waterfall_data[sh].append(payout)

            fig_wf = go.Figure()
            colors = [BLUE, BLUE_MID, GREEN, YELLOW, RED, PURPLE, ORANGE, TEAL]
            for idx, (sh, payouts) in enumerate(waterfall_data.items()):
                sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
                fig_wf.add_trace(go.Bar(
                    name=sh_label,
                    x=[fmt_usd(ev) for ev in exit_values],
                    y=payouts,
                    marker_color=colors[idx % len(colors)],
                ))
            fig_wf.update_layout(barmode="stack")
            styled_layout(fig_wf, T("exit_valuation"), "Payout (USD)", height=400)
            st.plotly_chart(fig_wf, use_container_width=True)

            # Waterfall table
            wf_rows = []
            for i, ev in enumerate(exit_values):
                row = {T("exit_valuation"): fmt_usd(ev)}
                for sh, payouts in waterfall_data.items():
                    sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
                    row[sh_label] = fmt_usd(payouts[i])
                wf_rows.append(row)
            st.dataframe(pd.DataFrame(wf_rows), use_container_width=True, hide_index=True)

        # Ownership pie chart for latest round
        if cap_results:
            latest = cap_results[-1]
            pie_shares = dict(latest["ownership"])
            # Add converted instruments
            if converted_instruments:
                post_shares = dict(latest["cumulative_shares"])
                for ci in converted_instruments:
                    name = f"{ci['type']} Holder"
                    post_shares[name] = post_shares.get(name, 0) + ci["shares"]
                total_post = sum(post_shares.values())
                pie_shares = {sh: (cnt / total_post * 100) for sh, cnt in post_shares.items()}

            fig_pie = go.Figure(data=[go.Pie(
                labels=[T("ct_founders") if k == "Founders" else (T("ct_esop_pool") if k == "ESOP" else k)
                        for k in pie_shares.keys()],
                values=list(pie_shares.values()),
                marker=dict(colors=[BLUE, BLUE_MID, GREEN, YELLOW, RED, PURPLE, ORANGE, TEAL][:len(pie_shares)]),
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
    ltv_str = fmt_usd(ue["ltv"]) if ue["ltv"] != float('inf') else "---"
    km1.markdown(metric_card(T("ue_ltv"), ltv_str), unsafe_allow_html=True)

    # LTV/CAC
    if ue["ltv_cac"] == float('inf'):
        ratio_str = "---"
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
    pb_str = f"{ue['payback']:.1f}" if ue["payback"] != float('inf') else "---"
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

    # -- Ownership Summary --
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

    # -- Valuations per Round --
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

    # -- Revenue Milestones --
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

    # -- Unit Economics Summary --
    st.markdown(f"#### {T('res_unit_econ_summary')}")
    ue1, ue2, ue3, ue4 = st.columns(4)

    ltv_str = fmt_usd(ue_res["ltv"]) if ue_res["ltv"] != float('inf') else "---"
    ue1.markdown(metric_card("LTV", ltv_str), unsafe_allow_html=True)

    if ue_res["ltv_cac"] >= 3:
        r_cls = "metric-card-green"
    elif ue_res["ltv_cac"] >= 1:
        r_cls = "metric-card-yellow"
    else:
        r_cls = "metric-card-red"
    r_str = f"{ue_res['ltv_cac']:.1f}x" if ue_res["ltv_cac"] != float('inf') else "---"
    ue2.markdown(metric_card("LTV/CAC", r_str, r_cls), unsafe_allow_html=True)

    ue3.markdown(metric_card("CAC", fmt_usd(ue_res["cac"])), unsafe_allow_html=True)

    pb_str = f"{ue_res['payback']:.1f} {'meses' if lang == 'PT' else 'mo'}" if ue_res["payback"] != float('inf') else "---"
    ue4.markdown(metric_card(T("ue_payback"), pb_str), unsafe_allow_html=True)

    st.markdown("---")

    # -- Runway Summary --
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

    # -- Final MRR/ARR --
    st.markdown("---")
    fm1, fm2 = st.columns(2)
    final_mrr_res = rev_df_res.iloc[-1]["mrr"]
    final_arr_res = rev_df_res.iloc[-1]["arr"]
    fm1.markdown(metric_card(f"MRR (M{int(get('su_proj_months', 36))})", fmt_usd(final_mrr_res)), unsafe_allow_html=True)
    fm2.markdown(metric_card(f"ARR (M{int(get('su_proj_months', 36))})", fmt_usd(final_arr_res)), unsafe_allow_html=True)


# ===================== TAB 7: SAAS METRICS ===================================
with tabs[6]:
    st.subheader(T("saas_title"))

    st.markdown(f"#### {'Dados de Entrada' if lang == 'PT' else 'Input Data'}")

    si1, si2, si3, si4 = st.columns(4)
    with si1:
        st.number_input(T("saas_starting_mrr"), min_value=0.0, max_value=50_000_000.0,
                        step=5_000.0, key="su_saas_starting_mrr", format="%.0f")
        st.number_input(T("saas_new_mrr"), min_value=0.0, max_value=10_000_000.0,
                        step=1_000.0, key="su_saas_new_mrr", format="%.0f")
    with si2:
        st.number_input(T("saas_expansion_mrr"), min_value=0.0, max_value=10_000_000.0,
                        step=500.0, key="su_saas_expansion_mrr", format="%.0f")
        st.number_input(T("saas_contraction_mrr"), min_value=0.0, max_value=10_000_000.0,
                        step=500.0, key="su_saas_contraction_mrr", format="%.0f")
    with si3:
        st.number_input(T("saas_churned_mrr"), min_value=0.0, max_value=10_000_000.0,
                        step=500.0, key="su_saas_churned_mrr", format="%.0f")
        st.number_input(T("saas_sm_spend"), min_value=0.0, max_value=50_000_000.0,
                        step=10_000.0, key="su_saas_sm_spend", format="%.0f")
    with si4:
        st.number_input(T("saas_rev_growth"), min_value=-100.0, max_value=500.0,
                        step=5.0, key="su_saas_rev_growth", format="%.1f")
        st.number_input(T("saas_ebitda_margin"), min_value=-200.0, max_value=100.0,
                        step=5.0, key="su_saas_ebitda_margin", format="%.1f")

    si5, si6, si7 = st.columns(3)
    with si5:
        st.number_input(T("saas_gross_margin"), min_value=0.0, max_value=100.0,
                        step=5.0, key="su_saas_gross_margin_pct", format="%.1f")
    with si6:
        st.number_input(T("saas_net_burn"), min_value=0.0, max_value=50_000_000.0,
                        step=10_000.0, key="su_saas_net_burn", format="%.0f")
    with si7:
        st.number_input(T("saas_net_new_arr"), min_value=0.0, max_value=100_000_000.0,
                        step=10_000.0, key="su_saas_net_new_arr", format="%.0f")

    saas = compute_saas_metrics()

    st.markdown("---")
    st.markdown(f"#### {'Metricas Calculadas' if lang == 'PT' else 'Computed Metrics'}")

    sm1, sm2, sm3, sm4 = st.columns(4)

    # NRR
    nrr_cls = "metric-card-green" if saas["nrr"] >= 100 else ("metric-card-yellow" if saas["nrr"] >= 90 else "metric-card-red")
    sm1.markdown(metric_card(T("saas_nrr"), f"{saas['nrr']:.1f}%", nrr_cls), unsafe_allow_html=True)

    # GRR
    grr_cls = "metric-card-green" if saas["grr"] >= 90 else ("metric-card-yellow" if saas["grr"] >= 80 else "metric-card-red")
    sm2.markdown(metric_card(T("saas_grr"), f"{saas['grr']:.1f}%", grr_cls), unsafe_allow_html=True)

    # Magic Number
    mg_cls = "metric-card-green" if saas["magic_number"] >= 0.75 else ("metric-card-yellow" if saas["magic_number"] >= 0.5 else "metric-card-red")
    sm3.markdown(metric_card(T("saas_magic"), f"{saas['magic_number']:.2f}", mg_cls), unsafe_allow_html=True)

    # Rule of 40
    r40_cls = "metric-card-green" if saas["rule_of_40"] >= 40 else ("metric-card-yellow" if saas["rule_of_40"] >= 20 else "metric-card-red")
    sm4.markdown(metric_card(T("saas_rule40"), f"{saas['rule_of_40']:.1f}%", r40_cls), unsafe_allow_html=True)

    sm5, sm6, sm7 = st.columns(3)

    # CAC Payback
    cp_str = f"{saas['cac_payback']:.1f} {'meses' if lang == 'PT' else 'mo'}" if saas["cac_payback"] != float('inf') else "---"
    cp_cls = "metric-card-green" if saas["cac_payback"] < 12 else ("metric-card-yellow" if saas["cac_payback"] < 18 else "metric-card-red")
    sm5.markdown(metric_card(T("saas_cac_payback"), cp_str, cp_cls), unsafe_allow_html=True)

    # Quick Ratio
    qr_str = f"{saas['quick_ratio']:.2f}" if saas["quick_ratio"] != float('inf') else "---"
    qr_cls = "metric-card-green" if saas["quick_ratio"] >= 4 else ("metric-card-yellow" if saas["quick_ratio"] >= 2 else "metric-card-red")
    sm6.markdown(metric_card(T("saas_quick_ratio"), qr_str, qr_cls), unsafe_allow_html=True)

    # Burn Multiple
    bm_str = f"{saas['burn_multiple']:.2f}x" if saas["burn_multiple"] != float('inf') else "---"
    bm_cls = "metric-card-green" if saas["burn_multiple"] < 1.5 else ("metric-card-yellow" if saas["burn_multiple"] < 3 else "metric-card-red")
    sm7.markdown(metric_card(T("saas_burn_multiple"), bm_str, bm_cls), unsafe_allow_html=True)

    # Benchmarks
    st.markdown("---")
    st.markdown(f"#### {'Benchmarks de Referencia' if lang == 'PT' else 'Reference Benchmarks'}")

    benchmarks = [
        (T("saas_nrr"), "> 120%", f"{saas['nrr']:.1f}%", saas["nrr"] >= 120),
        (T("saas_grr"), "> 90%", f"{saas['grr']:.1f}%", saas["grr"] >= 90),
        (T("saas_magic"), "> 0.75", f"{saas['magic_number']:.2f}", saas["magic_number"] >= 0.75),
        (T("saas_rule40"), "> 40%", f"{saas['rule_of_40']:.1f}%", saas["rule_of_40"] >= 40),
        (T("saas_quick_ratio"), "> 4x", qr_str, saas["quick_ratio"] >= 4),
        (T("saas_burn_multiple"), "< 1.5x", bm_str, saas["burn_multiple"] < 1.5),
    ]

    bench_rows = []
    for name, target, actual, is_good in benchmarks:
        bench_rows.append({
            ("Metrica" if lang == "PT" else "Metric"): name,
            ("Meta" if lang == "PT" else "Target"): target,
            ("Atual" if lang == "PT" else "Actual"): actual,
            "Status": "🟢" if is_good else "🔴",
        })
    st.dataframe(pd.DataFrame(bench_rows), use_container_width=True, hide_index=True)

    # MRR Breakdown visual
    st.markdown("---")
    st.markdown(f"#### MRR {'Composicao' if lang == 'PT' else 'Breakdown'}")

    starting = get("su_saas_starting_mrr", 50_000)
    new_m = get("su_saas_new_mrr", 12_000)
    exp_m = get("su_saas_expansion_mrr", 5_000)
    cont_m = get("su_saas_contraction_mrr", 2_000)
    churn_m = get("su_saas_churned_mrr", 3_000)
    ending_mrr = starting + new_m + exp_m - cont_m - churn_m

    fig_mrr_wf = go.Figure(go.Waterfall(
        name="MRR",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["Starting MRR", "New MRR", "Expansion", "Contraction", "Churn", "Ending MRR"],
        y=[starting, new_m, exp_m, -cont_m, -churn_m, 0],
        connector=dict(line=dict(color=BLUE_MID)),
        increasing=dict(marker=dict(color=GREEN)),
        decreasing=dict(marker=dict(color=RED)),
        totals=dict(marker=dict(color=BLUE)),
    ))
    styled_layout(fig_mrr_wf, "", "MRR (USD)", height=350)
    st.plotly_chart(fig_mrr_wf, use_container_width=True)


# ===================== TAB 8: COHORT ANALYSIS ================================
with tabs[7]:
    st.subheader(T("cohort_title"))

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.number_input(T("cohort_initial"), min_value=10, max_value=10_000, step=10, key="su_cohort_initial")
        st.number_input(T("cohort_months"), min_value=3, max_value=36, step=1, key="su_cohort_months")
    with cc2:
        st.number_input(T("cohort_n_cohorts"), min_value=2, max_value=12, step=1, key="su_cohort_n")
        st.number_input(T("cohort_base_retention"), min_value=50.0, max_value=99.9, step=1.0,
                        key="su_cohort_base_retention", format="%.1f")
    with cc3:
        st.number_input(T("cohort_decay"), min_value=0.0, max_value=10.0, step=0.5,
                        key="su_cohort_decay", format="%.1f")
        st.number_input(T("cohort_arpu"), min_value=1.0, max_value=100_000.0, step=10.0,
                        key="su_cohort_arpu", format="%.0f")

    ret_df, rev_cohort_df = compute_cohort_data()

    # Retention Heatmap
    st.markdown("---")
    st.markdown(f"#### {T('cohort_retention_heatmap')}")

    fig_heat = go.Figure(data=go.Heatmap(
        z=ret_df.values,
        x=ret_df.columns.tolist(),
        y=ret_df.index.tolist(),
        colorscale=[[0, "#dc2626"], [0.5, "#fbbf24"], [1, "#16a34a"]],
        text=[[f"{v:.1f}%" for v in row] for row in ret_df.values],
        texttemplate="%{text}",
        textfont=dict(size=10),
        hovertemplate="Cohort: %{y}<br>Month: %{x}<br>Retention: %{z:.1f}%<extra></extra>",
        colorbar=dict(title="%"),
    ))
    fig_heat.update_layout(
        height=max(300, int(get("su_cohort_n", 6)) * 50 + 100),
        margin=dict(t=20, b=50, l=100, r=20),
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color="#374151"),
        xaxis=dict(title=T("rev_month")),
        yaxis=dict(title="", autorange="reversed"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # Retention Curve
    st.markdown(f"#### {T('cohort_retention_curve')}")
    fig_ret = go.Figure()
    colors_list = [BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE, TEAL, BLUE_MID]
    for i, cohort_name in enumerate(ret_df.index):
        fig_ret.add_trace(go.Scatter(
            x=list(range(len(ret_df.columns))),
            y=ret_df.iloc[i].values,
            mode="lines+markers",
            name=cohort_name,
            line=dict(color=colors_list[i % len(colors_list)], width=2),
            marker=dict(size=4),
        ))
    styled_layout(fig_ret, T("rev_month"), "Retention (%)", height=350)
    st.plotly_chart(fig_ret, use_container_width=True)

    # Revenue by Cohort
    st.markdown(f"#### {T('cohort_revenue')}")
    fig_rev_coh = go.Figure()
    for i, cohort_name in enumerate(rev_cohort_df.index):
        fig_rev_coh.add_trace(go.Bar(
            name=cohort_name,
            x=rev_cohort_df.columns.tolist(),
            y=rev_cohort_df.iloc[i].values,
            marker_color=colors_list[i % len(colors_list)],
        ))
    fig_rev_coh.update_layout(barmode="stack")
    styled_layout(fig_rev_coh, T("rev_month"), "Revenue (USD)", height=400)
    st.plotly_chart(fig_rev_coh, use_container_width=True)

    # Churn by Cohort Age
    st.markdown(f"#### {T('cohort_churn_by_age')}")
    n_months = int(get("su_cohort_months", 12))
    avg_churn_by_age = []
    for m in range(1, n_months):
        churns = []
        for i in range(len(ret_df)):
            prev = ret_df.iloc[i, m - 1]
            curr = ret_df.iloc[i, m]
            if prev > 0:
                churns.append((prev - curr) / prev * 100)
        avg_churn_by_age.append(sum(churns) / len(churns) if churns else 0)

    fig_churn_age = go.Figure()
    fig_churn_age.add_trace(go.Bar(
        x=[f"M{m}" for m in range(1, n_months)],
        y=avg_churn_by_age,
        marker_color=[RED if c > 5 else (YELLOW if c > 3 else GREEN) for c in avg_churn_by_age],
    ))
    styled_layout(fig_churn_age, f"{'Idade da Coorte' if lang == 'PT' else 'Cohort Age'}", "Churn (%)", height=300)
    st.plotly_chart(fig_churn_age, use_container_width=True)


# ===================== TAB 9: FUNDING FORECAST ===============================
with tabs[8]:
    st.subheader(T("fund_title"))

    st.markdown(f"#### {T('fund_headcount_plan')}")
    fh1, fh2, fh3 = st.columns(3)
    with fh1:
        st.number_input(T("fund_eng_headcount"), min_value=0, max_value=500, step=1, key="su_fund_eng_hc")
        st.number_input(T("fund_eng_salary"), min_value=0.0, max_value=500_000.0, step=1_000.0,
                        key="su_fund_eng_sal", format="%.0f")
    with fh2:
        st.number_input(T("fund_sales_headcount"), min_value=0, max_value=500, step=1, key="su_fund_sales_hc")
        st.number_input(T("fund_sales_salary"), min_value=0.0, max_value=500_000.0, step=1_000.0,
                        key="su_fund_sales_sal", format="%.0f")
    with fh3:
        st.number_input(T("fund_ga_headcount"), min_value=0, max_value=500, step=1, key="su_fund_ga_hc")
        st.number_input(T("fund_ga_salary"), min_value=0.0, max_value=500_000.0, step=1_000.0,
                        key="su_fund_ga_sal", format="%.0f")

    fo1, fo2, fo3 = st.columns(3)
    with fo1:
        st.number_input(T("fund_other_opex"), min_value=0.0, max_value=10_000_000.0, step=5_000.0,
                        key="su_fund_other_opex", format="%.0f")
    with fo2:
        st.number_input(T("fund_cogs_pct"), min_value=0.0, max_value=100.0, step=5.0,
                        key="su_fund_cogs_pct", format="%.1f")
    with fo3:
        st.number_input(T("fund_runway_target"), min_value=6, max_value=36, step=3,
                        key="su_fund_runway_target")

    fund_df, required_raise, implied_runway, gap_month = compute_funding_forecast()

    st.markdown("---")

    # Summary metrics
    st.markdown(f"#### {'Resumo' if lang == 'PT' else 'Summary'}")
    fs1, fs2, fs3, fs4 = st.columns(4)

    total_hc = int(get("su_fund_eng_hc", 8)) + int(get("su_fund_sales_hc", 4)) + int(get("su_fund_ga_hc", 3))
    fs1.markdown(metric_card("Headcount", str(total_hc)), unsafe_allow_html=True)

    monthly_payroll = (int(get("su_fund_eng_hc", 8)) * get("su_fund_eng_sal", 12_000) +
                       int(get("su_fund_sales_hc", 4)) * get("su_fund_sales_sal", 8_000) +
                       int(get("su_fund_ga_hc", 3)) * get("su_fund_ga_sal", 7_000))
    fs2.markdown(metric_card("Payroll/mo", fmt_usd(monthly_payroll)), unsafe_allow_html=True)

    rw_cls = "metric-card-green" if implied_runway and implied_runway >= 18 else (
        "metric-card-yellow" if implied_runway and implied_runway >= 12 else "metric-card-red")
    rw_str = f"{implied_runway} {'meses' if lang == 'PT' else 'mo'}" if implied_runway else T("rw_infinite")
    fs3.markdown(metric_card("Runway", rw_str, rw_cls), unsafe_allow_html=True)

    raise_cls = "metric-card-red" if required_raise > 0 else "metric-card-green"
    fs4.markdown(metric_card(T("fund_required"), fmt_usd(required_raise), raise_cls), unsafe_allow_html=True)

    st.info(T("fund_recommended"))

    # Monthly P&L Table
    st.markdown("---")
    st.markdown(f"#### {T('fund_monthly_pl')}")

    # Show every 3rd month for readability
    display_months = list(range(0, len(fund_df), 3))
    if (len(fund_df) - 1) not in display_months:
        display_months.append(len(fund_df) - 1)

    pl_rows = []
    for idx in display_months:
        row = fund_df.iloc[idx]
        pl_rows.append({
            T("rev_month"): f"M{int(row['month'])}",
            ("Receita" if lang == "PT" else "Revenue"): fmt_usd(row["revenue"]),
            "COGS": fmt_usd(row["cogs"]),
            ("Lucro Bruto" if lang == "PT" else "Gross Profit"): fmt_usd(row["gross_profit"]),
            ("Eng" if lang == "PT" else "Eng"): fmt_usd(row["eng_cost"]),
            ("Vendas" if lang == "PT" else "Sales"): fmt_usd(row["sales_cost"]),
            "G&A": fmt_usd(row["ga_cost"]),
            ("Outros" if lang == "PT" else "Other"): fmt_usd(row["other_opex"]),
            ("Resultado" if lang == "PT" else "Net Income"): fmt_usd(row["net_income"]),
            ("Caixa" if lang == "PT" else "Cash"): fmt_usd(row["cumulative_cash"]),
        })
    st.dataframe(pd.DataFrame(pl_rows), use_container_width=True, hide_index=True)

    # Cash Flow Chart
    st.markdown(f"#### {T('fund_cash_flow')}")
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Scatter(
        x=fund_df["month"], y=fund_df["cumulative_cash"],
        mode="lines", fill="tozeroy",
        name=T("rw_remaining"),
        line=dict(color=BLUE, width=2),
        fillcolor="rgba(26,86,219,0.08)",
    ))
    fig_cf.add_trace(go.Bar(
        x=fund_df["month"], y=fund_df["net_income"],
        name=("Resultado Mensal" if lang == "PT" else "Monthly Net"),
        marker_color=[GREEN if v >= 0 else RED for v in fund_df["net_income"]],
        opacity=0.5,
    ))
    fig_cf.add_hline(y=0, line_dash="dash", line_color=RED, line_width=1)
    styled_layout(fig_cf, T("rev_month"), "USD", height=400)
    st.plotly_chart(fig_cf, use_container_width=True)

    # Headcount cost breakdown pie
    st.markdown(f"#### {'Composicao de Custos' if lang == 'PT' else 'Cost Breakdown'}")
    eng_cost = int(get("su_fund_eng_hc", 8)) * get("su_fund_eng_sal", 12_000)
    sales_cost = int(get("su_fund_sales_hc", 4)) * get("su_fund_sales_sal", 8_000)
    ga_cost = int(get("su_fund_ga_hc", 3)) * get("su_fund_ga_sal", 7_000)
    other_cost = get("su_fund_other_opex", 15_000)

    fig_cost = go.Figure(data=[go.Pie(
        labels=["Engineering", "Sales", "G&A", "Other OpEx"],
        values=[eng_cost, sales_cost, ga_cost, other_cost],
        marker=dict(colors=[BLUE, GREEN, YELLOW, PURPLE]),
        textinfo="label+percent",
        hole=0.4,
    )])
    fig_cost.update_layout(
        height=300, margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
    )
    st.plotly_chart(fig_cost, use_container_width=True)


# ===================== TAB 10: EXIT ANALYSIS =================================
with tabs[9]:
    st.subheader(T("exit_title"))

    ex1, ex2 = st.columns(2)
    with ex1:
        st.number_input(T("exit_arr_at_exit"), min_value=100_000.0, max_value=1_000_000_000.0,
                        step=1_000_000.0, key="su_exit_arr", format="%.0f")
    with ex2:
        st.number_input(T("exit_years_to_exit"), min_value=1, max_value=15, step=1, key="su_exit_years")

    exit_arr = get("su_exit_arr", 10_000_000)
    exit_years = int(get("su_exit_years", 5))

    # Compute cap table for exit analysis
    cap_results_exit = compute_cap_table()

    # Exit at different multiples
    multiples = [5, 10, 15, 20, 25, 30]
    st.markdown("---")
    st.markdown(f"#### {T('exit_valuation')}")

    exit_cols = st.columns(len(multiples))
    for i, mult in enumerate(multiples):
        ev = exit_arr * mult
        exit_cols[i].markdown(metric_card(f"{mult}x ARR", fmt_usd(ev)), unsafe_allow_html=True)

    if cap_results_exit:
        st.markdown("---")
        st.markdown(f"#### {T('exit_waterfall')}")

        liq_mult = float(get("su_liq_multiple", 1.0))
        liq_type = get("su_liq_type", "Non-participating")

        # Compute total invested
        total_invested = sum(rnd["raised"] for rnd in cap_results_exit)

        # Exit waterfall table
        exit_rows = []
        latest_exit = cap_results_exit[-1]

        for mult in multiples:
            ev = exit_arr * mult
            payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)

            row = {
                T("exit_scenario"): f"{mult}x ARR",
                T("exit_valuation"): fmt_usd(ev),
            }

            for sh, payout in payouts.items():
                sh_label = T("ct_founders") if sh == "Founders" else (T("ct_esop_pool") if sh == "ESOP" else sh)
                row[sh_label] = fmt_usd(payout)

            exit_rows.append(row)

        st.dataframe(pd.DataFrame(exit_rows), use_container_width=True, hide_index=True)

        # Founder Return Analysis
        st.markdown("---")
        st.markdown(f"#### {T('exit_founder_return')}")

        founder_rows = []
        for mult in multiples:
            ev = exit_arr * mult
            payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)
            founder_payout = payouts.get("Founders", 0)

            # IRR calculation: founders "invested" time, not money
            # Use first round valuation as reference for founder equity value
            founder_initial_value = cap_results_exit[0]["pre_money"] * (
                cap_results_exit[0]["ownership"].get("Founders", 100) / 100)

            if founder_initial_value > 0 and exit_years > 0:
                try:
                    founder_irr = ((founder_payout / founder_initial_value) ** (1 / exit_years) - 1) * 100
                except (ValueError, ZeroDivisionError):
                    founder_irr = 0
            else:
                founder_irr = 0

            founder_moic = founder_payout / founder_initial_value if founder_initial_value > 0 else 0

            founder_rows.append({
                T("exit_scenario"): f"{mult}x ARR",
                T("exit_valuation"): fmt_usd(ev),
                ("Retorno Fundador" if lang == "PT" else "Founder Payout"): fmt_usd(founder_payout),
                T("exit_moic"): f"{founder_moic:.1f}x",
                T("exit_irr"): f"{founder_irr:.1f}%",
            })

        st.dataframe(pd.DataFrame(founder_rows), use_container_width=True, hide_index=True)

        # Investor Return Analysis
        st.markdown("---")
        st.markdown(f"#### {T('exit_investor_return')}")

        for rnd in cap_results_exit:
            rnd_label = round_labels.get(rnd["round_name"], rnd["round_name"])
            st.markdown(f'<span class="round-badge">{rnd_label}</span>', unsafe_allow_html=True)

            inv_rows = []
            for mult in multiples:
                ev = exit_arr * mult
                payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)
                inv_payout = payouts.get(rnd["round_name"], 0)
                invested = rnd["raised"]

                moic = inv_payout / invested if invested > 0 else 0
                if invested > 0 and exit_years > 0 and inv_payout > 0:
                    try:
                        irr = ((inv_payout / invested) ** (1 / exit_years) - 1) * 100
                    except (ValueError, ZeroDivisionError):
                        irr = 0
                else:
                    irr = 0

                inv_rows.append({
                    T("exit_scenario"): f"{mult}x ARR",
                    T("exit_valuation"): fmt_usd(ev),
                    T("exit_total_invested"): fmt_usd(invested),
                    ("Retorno" if lang == "PT" else "Payout"): fmt_usd(inv_payout),
                    T("exit_moic"): f"{moic:.1f}x",
                    T("exit_irr"): f"{irr:.1f}%",
                })

            st.dataframe(pd.DataFrame(inv_rows), use_container_width=True, hide_index=True)

        # Exit Return Chart
        st.markdown("---")
        st.markdown(f"#### {'Retorno por Cenario' if lang == 'PT' else 'Return by Scenario'}")

        fig_exit = go.Figure()
        exit_vals = [exit_arr * m for m in multiples]

        for rnd in cap_results_exit:
            rnd_label = round_labels.get(rnd["round_name"], rnd["round_name"])
            moics = []
            for mult in multiples:
                ev = exit_arr * mult
                payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)
                inv_payout = payouts.get(rnd["round_name"], 0)
                invested = rnd["raised"]
                moics.append(inv_payout / invested if invested > 0 else 0)

            fig_exit.add_trace(go.Scatter(
                x=[f"{m}x" for m in multiples],
                y=moics,
                mode="lines+markers",
                name=rnd_label,
            ))

        # Add founder MOIC
        founder_moics = []
        for mult in multiples:
            ev = exit_arr * mult
            payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)
            founder_payout = payouts.get("Founders", 0)
            founder_initial = cap_results_exit[0]["pre_money"] * (
                cap_results_exit[0]["ownership"].get("Founders", 100) / 100)
            founder_moics.append(founder_payout / founder_initial if founder_initial > 0 else 0)

        fig_exit.add_trace(go.Scatter(
            x=[f"{m}x" for m in multiples],
            y=founder_moics,
            mode="lines+markers",
            name=T("ct_founders"),
            line=dict(color=BLUE, width=3),
        ))

        styled_layout(fig_exit, "ARR Multiple", T("exit_moic"), height=400)
        st.plotly_chart(fig_exit, use_container_width=True)

        # Time to Exit Scenarios
        st.markdown("---")
        st.markdown(f"#### {'Cenarios de Tempo ate o Exit' if lang == 'PT' else 'Time to Exit Scenarios'}")

        years_range = [3, 5, 7, 10]
        target_mult = 10  # 10x ARR as base

        time_rows = []
        for yr in years_range:
            ev = exit_arr * target_mult
            payouts = compute_waterfall(ev, cap_results_exit, [], liq_mult, liq_type)

            for rnd in cap_results_exit:
                rnd_label = round_labels.get(rnd["round_name"], rnd["round_name"])
                inv_payout = payouts.get(rnd["round_name"], 0)
                invested = rnd["raised"]
                moic = inv_payout / invested if invested > 0 else 0
                if invested > 0 and yr > 0 and inv_payout > 0:
                    try:
                        irr = ((inv_payout / invested) ** (1 / yr) - 1) * 100
                    except (ValueError, ZeroDivisionError):
                        irr = 0
                else:
                    irr = 0

                time_rows.append({
                    T("exit_years_to_exit"): f"{yr} {'anos' if lang == 'PT' else 'years'}",
                    T("ct_round"): rnd_label,
                    T("exit_valuation"): fmt_usd(ev),
                    T("exit_moic"): f"{moic:.1f}x",
                    T("exit_irr"): f"{irr:.1f}%",
                })

        st.dataframe(pd.DataFrame(time_rows), use_container_width=True, hide_index=True)

    else:
        st.info("Ative ao menos uma rodada no Cap Table." if lang == "PT" else "Enable at least one round in the Cap Table.")

st.markdown('<div style="text-align:center;padding:24px 0 12px 0;margin-top:40px;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.72rem">Corpet · MVP — Powered by Streamlit + Plotly</div>', unsafe_allow_html=True)
