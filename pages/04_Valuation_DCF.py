"""
04_Valuation_DCF.py — Streamlit page: Professional DCF Valuation Model
Self-contained, bilingual PT/EN, blue theme (#1a56db).
Enhanced with FCFE, advanced WACC, terminal value cross-checks,
valuation bridge, comparable company analysis, Monte Carlo, and scenarios.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Valuation DCF", layout="wide")

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
    "title": "Modelo de Valuation — DCF",
    "dark_mode": "Modo Escuro",
    # Tabs
    "tab_company": "  Empresa  ",
    "tab_proj": "  Projecoes  ",
    "tab_wacc": "  WACC  ",
    "tab_tv": "  Valor Terminal  ",
    "tab_val": "  Valuation  ",
    "tab_fs": "  DFs  ",
    "tab_sens": "  Sensibilidade  ",
    "tab_comps": "  Comparaveis  ",
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
    "dcf_approach": "Abordagem do DCF",
    "fcff_label": "FCFF (Firma)",
    "fcfe_label": "FCFE (Acionista)",
    "net_borrowings_pct": "Captacao Liquida como % da receita",
    "interest_expense": "Despesa de Juros (R$ MM)",
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
    "beta_type": "Tipo de Beta",
    "levered_beta": "Beta Alavancado",
    "unlevered_beta": "Beta Desalavancado",
    "relevered_beta": "Beta Re-alavancado",
    "cost_debt": "Custo da divida pre-tax (%)",
    "tax_wacc": "Aliquota de imposto (%)",
    "de_ratio": "Relacao D/E",
    "calc_wacc": "WACC Calculado",
    "cost_equity": "Custo do Equity (Ke)",
    "cost_debt_at": "Custo da Divida pos-tax (Kd)",
    "weight_e": "Peso do Equity",
    "weight_d": "Peso da Divida",
    "wacc_info": "Calculo do WACC via CAPM com ajustes profissionais.",
    "crp": "Premio de Risco-Pais (%)",
    "size_premium": "Premio de Tamanho (%)",
    "company_risk": "Premio de Risco Especifico (%)",
    "wacc_buildup": "Decomposicao do WACC",
    "iterative_wacc": "WACC Iterativo (recalcula com estrutura de capital)",
    # Terminal Value
    "tv_method": "Metodo de valor terminal",
    "gordon": "Gordon Growth (Perpetuidade)",
    "exit_mult": "Multiplo de Saida (EV/EBITDA)",
    "perp_growth": "Taxa de crescimento na perpetuidade (%)",
    "exit_multiple": "Multiplo EV/EBITDA de saida",
    "tv_info": "Selecione o metodo e as premissas para o valor terminal.",
    "tv_crosscheck": "Cross-Check do Valor Terminal",
    "implied_exit_mult": "Multiplo de Saida Implicito",
    "implied_perp_growth": "Crescimento Perpetuo Implicito",
    "tv_pct_warning": "ATENCAO: Valor terminal representa {pct:.1f}% do EV (>75%)",
    "fade_period": "Periodo de Transicao (anos)",
    "fade_info": "Transicao gradual da taxa de crescimento explicita para a terminal",
    "mid_year_convention": "Convencao de meio de ano",
    "terminal_growth_fade": "Crescimento no inicio do fade (%)",
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
    "fcfe": "FCFE",
    "net_borr": "(+) Captacao Liquida",
    "interest": "(-) Juros Liquidos",
    "pv_fcff": "VP do FCFF",
    "pv_fcfe": "VP do FCFE",
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
    "val_info": "Calculo completo do FCF, valor presente e ponte para valor por acao.",
    # Valuation Bridge
    "vb_title": "Ponte de Valuation Detalhada",
    "total_debt": "(-) Divida Total",
    "minority_interest": "(-) Participacao Minoritaria",
    "preferred_equity": "(-) Acoes Preferenciais",
    "cash_equiv": "(+) Caixa e Equivalentes",
    "equity_investments": "(+) Investimentos em Equity",
    "diluted_shares": "Acoes Diluidas (MM)",
    "per_share_value": "Valor por Acao",
    "enter_total_debt": "Divida Total (R$ MM)",
    "enter_minority": "Participacao Minoritaria (R$ MM)",
    "enter_preferred": "Acoes Preferenciais (R$ MM)",
    "enter_cash": "Caixa e Equivalentes (R$ MM)",
    "enter_eq_invest": "Investimentos em Equity (R$ MM)",
    "enter_diluted_shares": "Acoes Diluidas (MM)",
    "use_detailed_bridge": "Usar Ponte Detalhada",
    # Sensitivity
    "sens_title": "Analise de Sensibilidade",
    "sens_wacc_label": "Faixa de WACC (%)",
    "sens_growth_label": "Faixa de crescimento perpetuo (%)",
    "sens_exit_label": "Faixa de multiplo de saida (x)",
    "sens_info": "Tabela bidimensional, Monte Carlo e analise de cenarios.",
    "football_title": "Football Field — Faixa de Valor por Acao",
    "implied_price": "Preco Implicito por Acao (R$)",
    "current_price_line": "Preco Atual",
    "scenario": "Cenario",
    "sens_rev_margin": "Crescimento de Receita vs Margem",
    "sens_rev_label": "Faixa de crescimento de receita (%)",
    "sens_margin_label": "Faixa de margem EBITDA (%)",
    "monte_carlo_title": "Simulacao Monte Carlo",
    "mc_iterations": "Numero de iteracoes",
    "mc_wacc_std": "Desvio padrao do WACC (%)",
    "mc_growth_std": "Desvio padrao do crescimento (%)",
    "mc_margin_std": "Desvio padrao da margem (%)",
    "mc_run": "Executar Monte Carlo",
    "mc_mean": "Media",
    "mc_median": "Mediana",
    "mc_p10": "Percentil 10",
    "mc_p90": "Percentil 90",
    "mc_std": "Desvio Padrao",
    "scenario_title": "Analise de Cenarios",
    "bull_case": "Cenario Otimista",
    "base_case": "Caso Base",
    "bear_case": "Cenario Pessimista",
    "probability": "Probabilidade (%)",
    "rev_growth_adj": "Ajuste no cresc. receita (p.p.)",
    "margin_adj": "Ajuste na margem (p.p.)",
    "wacc_adj": "Ajuste no WACC (p.p.)",
    "expected_value": "Valor Esperado (ponderado)",
    "scenario_price": "Preco por Acao",
    # Financial Statements (3-Statement Integration)
    "fs_info": "Modelo integrado de 3 demonstracoes: DRE, Fluxo de Caixa e Balanco Patrimonial.",
    "fs_assumptions": "Premissas de Demonstracoes Financeiras",
    "fs_cogs_pct": "CMV como % da receita",
    "fs_sga_pct": "SG&A como % da receita",
    "fs_dso": "DSO (dias de contas a receber)",
    "fs_dio": "DIO (dias de estoque)",
    "fs_dpo": "DPO (dias de contas a pagar)",
    "fs_oca_pct": "Outros ativos circulantes (% receita)",
    "fs_goodwill": "Goodwill inicial (MM)",
    "fs_lt_debt": "Divida de longo prazo inicial (MM)",
    "fs_st_debt": "Divida de curto prazo inicial (MM)",
    "fs_payout": "Payout de dividendos (%)",
    "fs_int_rate": "Taxa de juros sobre divida (%)",
    "fs_init_cash": "Caixa inicial (MM)",
    "fs_common_stock": "Capital social inicial (MM)",
    "fs_other_lta": "Outros ativos nao-circulantes (MM)",
    "fs_is_title": "Demonstracao do Resultado (DRE)",
    "fs_cf_title": "Demonstracao do Fluxo de Caixa (DFC)",
    "fs_bs_title": "Balanco Patrimonial (BP)",
    "fs_revenue": "Receita",
    "fs_cogs": "(-) CMV",
    "fs_gross": "Lucro Bruto",
    "fs_sga": "(-) SG&A",
    "fs_ebitda": "EBITDA",
    "fs_da": "(-) D&A",
    "fs_ebit": "EBIT",
    "fs_interest": "(-) Juros",
    "fs_pretax": "Lucro Antes do Imposto",
    "fs_tax": "(-) Imposto",
    "fs_ni": "Lucro Liquido",
    "fs_plus_da": "(+) D&A",
    "fs_min_nwc": "(-) Variacao do NWC",
    "fs_cfo": "= Caixa Operacional (CFO)",
    "fs_min_capex": "(-) CapEx",
    "fs_cfi": "= Caixa de Investimento (CFI)",
    "fs_net_borr": "(+) Captacao Liquida",
    "fs_min_div": "(-) Dividendos",
    "fs_cff": "= Caixa de Financiamento (CFF)",
    "fs_net_change": "Variacao Liquida de Caixa",
    "fs_beg_cash": "Caixa Inicial",
    "fs_end_cash": "Caixa Final",
    "fs_assets": "ATIVO",
    "fs_cash": "Caixa e Equivalentes",
    "fs_ar": "Contas a Receber",
    "fs_inv": "Estoques",
    "fs_oca": "Outros Ativos Circulantes",
    "fs_tca": "Total Ativo Circulante",
    "fs_ppe": "Imobilizado Liquido (PP&E)",
    "fs_gw": "Goodwill",
    "fs_olta": "Outros Ativos Nao-Circulantes",
    "fs_ta": "TOTAL DO ATIVO",
    "fs_liab": "PASSIVO",
    "fs_ap": "Fornecedores",
    "fs_std": "Divida de Curto Prazo",
    "fs_tcl": "Total Passivo Circulante",
    "fs_ltd": "Divida de Longo Prazo",
    "fs_tl": "TOTAL DO PASSIVO",
    "fs_eq": "PATRIMONIO LIQUIDO",
    "fs_cs": "Capital Social",
    "fs_re": "Lucros Acumulados",
    "fs_te": "Total Patrimonio Liquido",
    "fs_tle": "TOTAL PASSIVO + PL",
    "fs_balance_check": "Verificacao do Balanco",
    "fs_balanced": "BALANCO FECHADO",
    "fs_unbalanced": "BALANCO NAO FECHA",
    "fs_diff": "Diferenca",
    # Comps
    "comps_title": "Analise de Empresas Comparaveis",
    "comps_info": "Adicione empresas comparaveis para calcular multiplos de mercado.",
    "comp_name": "Nome",
    "comp_ev": "EV (MM)",
    "comp_revenue": "Receita (MM)",
    "comp_ebitda": "EBITDA (MM)",
    "comp_net_income": "Lucro Liquido (MM)",
    "comp_mktcap": "Market Cap (MM)",
    "num_comps": "Numero de comparaveis",
    "ev_revenue": "EV/Receita",
    "ev_ebitda": "EV/EBITDA",
    "pe_ratio": "P/L",
    "mean": "Media",
    "median": "Mediana",
    "high": "Maximo",
    "low": "Minimo",
    "comps_valuation": "Valuation via Multiplos",
    "comps_football": "Football Field: DCF + Comparaveis",
    "target_metrics": "Metricas da Empresa Alvo",
},
"EN": {
    "title": "Valuation Model — DCF",
    "dark_mode": "Dark Mode",
    "tab_company": "  Company  ",
    "tab_proj": "  Projections  ",
    "tab_wacc": "  WACC  ",
    "tab_tv": "  Terminal Value  ",
    "tab_val": "  Valuation  ",
    "tab_fs": "  DFs  ",
    "tab_sens": "  Sensitivity  ",
    "tab_comps": "  Comparables  ",
    "company_name": "Company name",
    "company_name_ph": "E.g.: Apple Inc.",
    "sector": "Sector",
    "current_revenue": "Current revenue ($ MM)",
    "ebitda_margin": "Current EBITDA margin (%)",
    "net_income": "Net income ($ MM)",
    "shares_out": "Shares outstanding (MM)",
    "share_price": "Current share price ($)",
    "company_info": "Fill in the company basics to feed the DCF model.",
    "dcf_approach": "DCF Approach",
    "fcff_label": "FCFF (Firm)",
    "fcfe_label": "FCFE (Equity)",
    "net_borrowings_pct": "Net Borrowings as % of revenue",
    "interest_expense": "Interest Expense ($ MM)",
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
    "beta_type": "Beta Type",
    "levered_beta": "Levered Beta",
    "unlevered_beta": "Unlevered Beta",
    "relevered_beta": "Relevered Beta",
    "cost_debt": "Pre-tax cost of debt (%)",
    "tax_wacc": "Tax rate (%)",
    "de_ratio": "D/E ratio",
    "calc_wacc": "Calculated WACC",
    "cost_equity": "Cost of Equity (Ke)",
    "cost_debt_at": "After-tax Cost of Debt (Kd)",
    "weight_e": "Equity Weight",
    "weight_d": "Debt Weight",
    "wacc_info": "WACC calculation via CAPM with professional adjustments.",
    "crp": "Country Risk Premium (%)",
    "size_premium": "Size Premium (%)",
    "company_risk": "Company-Specific Risk Premium (%)",
    "wacc_buildup": "WACC Buildup",
    "iterative_wacc": "Iterative WACC (recalculates with capital structure)",
    "tv_method": "Terminal value method",
    "gordon": "Gordon Growth (Perpetuity)",
    "exit_mult": "Exit Multiple (EV/EBITDA)",
    "perp_growth": "Perpetuity growth rate (%)",
    "exit_multiple": "Exit EV/EBITDA multiple",
    "tv_info": "Select the method and assumptions for terminal value.",
    "tv_crosscheck": "Terminal Value Cross-Check",
    "implied_exit_mult": "Implied Exit Multiple",
    "implied_perp_growth": "Implied Perpetuity Growth",
    "tv_pct_warning": "WARNING: Terminal value represents {pct:.1f}% of EV (>75%)",
    "fade_period": "Fade Period (years)",
    "fade_info": "Gradual transition from explicit growth rate to terminal growth",
    "mid_year_convention": "Mid-year convention",
    "terminal_growth_fade": "Growth at start of fade (%)",
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
    "fcfe": "FCFE",
    "net_borr": "(+) Net Borrowings",
    "interest": "(-) Net Interest",
    "pv_fcff": "PV of FCFF",
    "pv_fcfe": "PV of FCFE",
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
    "val_info": "Full FCF calculation, present value, and bridge to per-share value.",
    "vb_title": "Detailed Valuation Bridge",
    "total_debt": "(-) Total Debt",
    "minority_interest": "(-) Minority Interest",
    "preferred_equity": "(-) Preferred Equity",
    "cash_equiv": "(+) Cash & Equivalents",
    "equity_investments": "(+) Equity Investments",
    "diluted_shares": "Diluted Shares (MM)",
    "per_share_value": "Per-Share Value",
    "enter_total_debt": "Total Debt ($ MM)",
    "enter_minority": "Minority Interest ($ MM)",
    "enter_preferred": "Preferred Equity ($ MM)",
    "enter_cash": "Cash & Equivalents ($ MM)",
    "enter_eq_invest": "Equity Investments ($ MM)",
    "enter_diluted_shares": "Diluted Shares (MM)",
    "use_detailed_bridge": "Use Detailed Bridge",
    "sens_title": "Sensitivity Analysis",
    "sens_wacc_label": "WACC range (%)",
    "sens_growth_label": "Perpetuity growth range (%)",
    "sens_exit_label": "Exit multiple range (x)",
    "sens_info": "Two-dimensional tables, Monte Carlo, and scenario analysis.",
    "football_title": "Football Field — Price per Share Range",
    "implied_price": "Implied Price per Share ($)",
    "current_price_line": "Current Price",
    "scenario": "Scenario",
    "sens_rev_margin": "Revenue Growth vs Margin",
    "sens_rev_label": "Revenue growth range (%)",
    "sens_margin_label": "EBITDA margin range (%)",
    "monte_carlo_title": "Monte Carlo Simulation",
    "mc_iterations": "Number of iterations",
    "mc_wacc_std": "WACC std deviation (%)",
    "mc_growth_std": "Growth std deviation (%)",
    "mc_margin_std": "Margin std deviation (%)",
    "mc_run": "Run Monte Carlo",
    "mc_mean": "Mean",
    "mc_median": "Median",
    "mc_p10": "10th Percentile",
    "mc_p90": "90th Percentile",
    "mc_std": "Std Deviation",
    "scenario_title": "Scenario Analysis",
    "bull_case": "Bull Case",
    "base_case": "Base Case",
    "bear_case": "Bear Case",
    "probability": "Probability (%)",
    "rev_growth_adj": "Revenue growth adj (pp)",
    "margin_adj": "Margin adj (pp)",
    "wacc_adj": "WACC adj (pp)",
    "expected_value": "Expected Value (weighted)",
    "scenario_price": "Price per Share",
    "fs_info": "Integrated 3-statement model: Income Statement, Cash Flow, and Balance Sheet.",
    "fs_assumptions": "Financial Statement Assumptions",
    "fs_cogs_pct": "COGS as % of revenue",
    "fs_sga_pct": "SG&A as % of revenue",
    "fs_dso": "DSO (days sales outstanding)",
    "fs_dio": "DIO (days inventory outstanding)",
    "fs_dpo": "DPO (days payable outstanding)",
    "fs_oca_pct": "Other current assets (% revenue)",
    "fs_goodwill": "Initial Goodwill (MM)",
    "fs_lt_debt": "Initial Long-term Debt (MM)",
    "fs_st_debt": "Initial Short-term Debt (MM)",
    "fs_payout": "Dividend Payout Ratio (%)",
    "fs_int_rate": "Interest Rate on Debt (%)",
    "fs_init_cash": "Initial Cash (MM)",
    "fs_common_stock": "Initial Common Stock (MM)",
    "fs_other_lta": "Other Long-term Assets (MM)",
    "fs_is_title": "Income Statement",
    "fs_cf_title": "Cash Flow Statement",
    "fs_bs_title": "Balance Sheet",
    "fs_revenue": "Revenue",
    "fs_cogs": "(-) COGS",
    "fs_gross": "Gross Profit",
    "fs_sga": "(-) SG&A",
    "fs_ebitda": "EBITDA",
    "fs_da": "(-) D&A",
    "fs_ebit": "EBIT",
    "fs_interest": "(-) Interest Expense",
    "fs_pretax": "Pre-tax Income",
    "fs_tax": "(-) Tax",
    "fs_ni": "Net Income",
    "fs_plus_da": "(+) D&A",
    "fs_min_nwc": "(-) Change in NWC",
    "fs_cfo": "= Cash from Operations (CFO)",
    "fs_min_capex": "(-) CapEx",
    "fs_cfi": "= Cash from Investing (CFI)",
    "fs_net_borr": "(+) Net Borrowings",
    "fs_min_div": "(-) Dividends",
    "fs_cff": "= Cash from Financing (CFF)",
    "fs_net_change": "Net Change in Cash",
    "fs_beg_cash": "Beginning Cash",
    "fs_end_cash": "Ending Cash",
    "fs_assets": "ASSETS",
    "fs_cash": "Cash & Equivalents",
    "fs_ar": "Accounts Receivable",
    "fs_inv": "Inventory",
    "fs_oca": "Other Current Assets",
    "fs_tca": "Total Current Assets",
    "fs_ppe": "PP&E Net",
    "fs_gw": "Goodwill",
    "fs_olta": "Other Long-term Assets",
    "fs_ta": "TOTAL ASSETS",
    "fs_liab": "LIABILITIES",
    "fs_ap": "Accounts Payable",
    "fs_std": "Short-term Debt",
    "fs_tcl": "Total Current Liabilities",
    "fs_ltd": "Long-term Debt",
    "fs_tl": "TOTAL LIABILITIES",
    "fs_eq": "EQUITY",
    "fs_cs": "Common Stock",
    "fs_re": "Retained Earnings",
    "fs_te": "Total Equity",
    "fs_tle": "TOTAL LIABILITIES + EQUITY",
    "fs_balance_check": "Balance Sheet Check",
    "fs_balanced": "BALANCE SHEET BALANCED",
    "fs_unbalanced": "BALANCE SHEET DOES NOT BALANCE",
    "fs_diff": "Difference",
    "comps_title": "Comparable Company Analysis",
    "comps_info": "Add comparable companies to compute market multiples.",
    "comp_name": "Name",
    "comp_ev": "EV (MM)",
    "comp_revenue": "Revenue (MM)",
    "comp_ebitda": "EBITDA (MM)",
    "comp_net_income": "Net Income (MM)",
    "comp_mktcap": "Market Cap (MM)",
    "num_comps": "Number of comparables",
    "ev_revenue": "EV/Revenue",
    "ev_ebitda": "EV/EBITDA",
    "pe_ratio": "P/E",
    "mean": "Mean",
    "median": "Median",
    "high": "High",
    "low": "Low",
    "comps_valuation": "Comps-Derived Valuation",
    "comps_football": "Football Field: DCF + Comps",
    "target_metrics": "Target Company Metrics",
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
.metric-card-amber{background:linear-gradient(135deg,#fff3cd 0%,#ffeeba 100%);border-color:#ffc107}
.metric-card-amber .mc-value{color:#856404}
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
    dark_mode = st.toggle("\U0001f319", key="dark_mode_dcf", help=T("dark_mode"))

_dcf_subtitle = ("Avaliação de empresas por fluxo de caixa descontado: CAPM, WACC, "
                 "Gordon Growth e múltiplos comparáveis." if lang == "PT" else
                 "Company valuation via discounted cash flow: CAPM, WACC, "
                 "Gordon Growth and trading comparables.")
_hc_title.markdown(
    "<style>.main-title{font-size:2.1rem;font-weight:800;color:#1a56db;"
    "margin-bottom:0.2rem;letter-spacing:-0.5px}"
    ".subtitle{font-size:1rem;color:#6b7280;margin-bottom:1.4rem}</style>"
    f'<div class="main-title">{T("title")}</div>'
    f'<div class="subtitle">{_dcf_subtitle}</div>',
    unsafe_allow_html=True)

if dark_mode:
    st.markdown("""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#0f172a !important}
p,h1,h2,h3,h4,label,li{color:#e2e8f0 !important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#e2e8f0 !important}
[data-testid="stCaption"] p,.stCaption p{color:#94a3b8 !important}
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
[data-testid="stSidebar"]{background:#1e293b !important;border-right:1px solid #334155 !important}
[data-testid="stSidebar"] *{color:#e2e8f0 !important}
[data-testid="stSidebar"] a,[data-testid="stSidebarNav"] a{color:#93c5fd !important}
[data-testid="stSidebarNavItems"] span{color:#e2e8f0 !important}
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
    # New defaults
    "dcf_approach": 0,
    "dcf_net_borrowings_pct": 1.0,
    "dcf_interest_expense": 30.0,
    "dcf_crp": 0.0,
    "dcf_size_premium": 0.0,
    "dcf_company_risk": 0.0,
    "dcf_beta_type": 0,
    "dcf_unlevered_beta": 0.85,
    "dcf_fade_period": 0,
    "dcf_fade_start_growth": 6.0,
    "dcf_mid_year": False,
    # Detailed bridge
    "dcf_use_detailed_bridge": False,
    "dcf_total_debt": 300.0,
    "dcf_minority_interest": 0.0,
    "dcf_preferred_equity": 0.0,
    "dcf_cash_equiv": 100.0,
    "dcf_equity_investments": 0.0,
    "dcf_diluted_shares": 520.0,
    # Comps
    "dcf_num_comps": 3,
    # Scenario
    "dcf_bull_prob": 25.0,
    "dcf_base_prob": 50.0,
    "dcf_bear_prob": 25.0,
    "dcf_bull_rev_adj": 3.0,
    "dcf_bull_margin_adj": 2.0,
    "dcf_bull_wacc_adj": -0.5,
    "dcf_bear_rev_adj": -3.0,
    "dcf_bear_margin_adj": -2.0,
    "dcf_bear_wacc_adj": 1.0,
    # Financial Statements (3-statement integration)
    "dcf_fs_cogs_pct": 60.0,
    "dcf_fs_sga_pct": 20.0,
    "dcf_fs_dso": 45.0,
    "dcf_fs_dio": 60.0,
    "dcf_fs_dpo": 30.0,
    "dcf_fs_oca_pct": 2.0,
    "dcf_fs_goodwill": 0.0,
    "dcf_fs_lt_debt": 300.0,
    "dcf_fs_st_debt": 50.0,
    "dcf_fs_payout": 30.0,
    "dcf_fs_int_rate": 7.0,
    "dcf_fs_init_cash": 100.0,
    "dcf_fs_common_stock": 500.0,
    "dcf_fs_other_lta": 50.0,
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

# Comps defaults
for i in range(1, 9):
    for fld in ["name", "ev", "revenue", "ebitda", "net_income", "mktcap"]:
        key = f"dcf_comp_{i}_{fld}"
        if key not in st.session_state:
            if fld == "name":
                st.session_state[key] = f"Comp {i}" if i <= 3 else ""
            elif fld == "ev":
                st.session_state[key] = 5000.0 + i * 1000.0
            elif fld == "revenue":
                st.session_state[key] = 2000.0 + i * 500.0
            elif fld == "ebitda":
                st.session_state[key] = 500.0 + i * 100.0
            elif fld == "net_income":
                st.session_state[key] = 200.0 + i * 50.0
            elif fld == "mktcap":
                st.session_state[key] = 4000.0 + i * 800.0

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: metric card
# ─────────────────────────────────────────────────────────────────────────────
def _mc(label, value, delta=None, color=None):
    cls = "metric-card"
    if color == "green":
        cls = "metric-card metric-card-green"
    elif color == "red":
        cls = "metric-card metric-card-red"
    elif color == "amber":
        cls = "metric-card metric-card-amber"
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
    """Format value: BR convention (1.234,5) + Macabacus parentheses."""
    if v is None:
        return "—"
    decimals = 0 if abs(v) >= 1_000 else 1
    def _br(s): return s.replace(",", "X").replace(".", ",").replace("X", ".")
    if v < 0:
        return f"({_br(f'{abs(v):,.{decimals}f}')})"
    return _br(f"{v:,.{decimals}f}")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
_dcf_icons = ["\U0001f3e2", "\U0001f4c8", "\U0001f4b1", "\U0001f3af",
              "\U0001f4b0", "\U0001f4d1", "\U0001f50d", "\U0001f4ca"]
_dcf_names = [T("tab_company"), T("tab_proj"), T("tab_wacc"),
              T("tab_tv"), T("tab_val"), T("tab_fs"), T("tab_sens"), T("tab_comps")]
tabs = st.tabs([f"{i}  {n}" for i, n in zip(_dcf_icons, _dcf_names)])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — COMPANY
# ═════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.info(T("company_info"))
    sectors = SECTORS_EN if lang == "EN" else SECTORS_PT

    # DCF approach toggle
    approach_options = [T("fcff_label"), T("fcfe_label")]
    st.radio(T("dcf_approach"), approach_options, horizontal=True,
             key="dcf_approach_radio")
    is_fcfe = (st.session_state.get("dcf_approach_radio", approach_options[0])
               == approach_options[1])

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
        if is_fcfe:
            st.number_input(T("interest_expense"), min_value=0.0, step=5.0,
                            format="%.1f", key="dcf_interest_expense")

    # Summary metrics
    rev = st.session_state["dcf_revenue"]
    marg = st.session_state["dcf_ebitda_margin"]
    ebitda_now = rev * marg / 100
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(_mc(T("current_revenue"), f"{fmt_mm(rev)}"), unsafe_allow_html=True)
    m2.markdown(_mc("EBITDA", f"{fmt_mm(ebitda_now)}"), unsafe_allow_html=True)
    ev_ebitda = (st.session_state["dcf_share_price"] * st.session_state["dcf_shares"]
                 + st.session_state.get("dcf_net_debt", 0)) / ebitda_now if ebitda_now else 0
    m3.markdown(_mc("EV/EBITDA", f"{ev_ebitda:.1f}x"), unsafe_allow_html=True)
    approach_label = T("fcfe_label") if is_fcfe else T("fcff_label")
    m4.markdown(_mc(T("dcf_approach"), approach_label), unsafe_allow_html=True)

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

    # FCFE-specific inputs
    if is_fcfe:
        st.markdown("---")
        st.subheader("FCFE")
        fp1, fp2 = st.columns(2)
        with fp1:
            st.number_input(T("net_borrowings_pct"), -10.0, 20.0, step=0.5,
                            format="%.1f", key="dcf_net_borrowings_pct")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — WACC (Enhanced)
# ═════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.info(T("wacc_info"))

    w1, w2 = st.columns(2)
    with w1:
        st.number_input(T("risk_free"), 0.0, 30.0, step=0.1, format="%.2f",
                        key="dcf_risk_free")
        st.number_input(T("erp"), 0.0, 30.0, step=0.1, format="%.2f",
                        key="dcf_erp")

        beta_type_opts = [T("levered_beta"), T("unlevered_beta")]
        st.radio(T("beta_type"), beta_type_opts, horizontal=True,
                 key="dcf_beta_type_radio")
        use_unlevered = (st.session_state.get("dcf_beta_type_radio",
                         beta_type_opts[0]) == beta_type_opts[1])

        if use_unlevered:
            st.number_input(T("unlevered_beta"), 0.0, 5.0, step=0.05,
                            format="%.2f", key="dcf_unlevered_beta")
        else:
            st.number_input(T("beta"), 0.0, 5.0, step=0.05, format="%.2f",
                            key="dcf_beta")

    with w2:
        st.number_input(T("cost_debt"), 0.0, 50.0, step=0.1, format="%.2f",
                        key="dcf_cost_debt")
        st.number_input(T("tax_wacc"), 0.0, 60.0, step=0.5, format="%.1f",
                        key="dcf_tax_wacc")
        st.number_input(T("de_ratio"), 0.0, 10.0, step=0.05, format="%.2f",
                        key="dcf_de_ratio")

    # Additional risk premiums
    st.markdown("---")
    st.subheader("Risk Premiums" if lang == "EN" else "Prêmios de Risco Adicionais")
    rp1, rp2, rp3 = st.columns(3)
    with rp1:
        st.number_input(T("crp"), 0.0, 20.0, step=0.1, format="%.2f",
                        key="dcf_crp")
    with rp2:
        st.number_input(T("size_premium"), 0.0, 10.0, step=0.1, format="%.2f",
                        key="dcf_size_premium")
    with rp3:
        st.number_input(T("company_risk"), 0.0, 10.0, step=0.1, format="%.2f",
                        key="dcf_company_risk")

    # ── WACC Calculation ──
    rf = st.session_state["dcf_risk_free"] / 100
    erp = st.session_state["dcf_erp"] / 100
    kd_pre = st.session_state["dcf_cost_debt"] / 100
    tax_w = st.session_state["dcf_tax_wacc"] / 100
    de = st.session_state["dcf_de_ratio"]
    crp_val = st.session_state["dcf_crp"] / 100
    size_prem = st.session_state["dcf_size_premium"] / 100
    comp_risk = st.session_state["dcf_company_risk"] / 100

    # Beta: levered or relevered from unlevered
    if use_unlevered:
        beta_u = st.session_state["dcf_unlevered_beta"]
        beta = beta_u * (1 + (1 - tax_w) * de)  # Hamada equation
    else:
        beta = st.session_state["dcf_beta"]
        beta_u = beta / (1 + (1 - tax_w) * de) if (1 + (1 - tax_w) * de) != 0 else beta

    # Cost of equity = Rf + Beta * ERP + CRP + Size Premium + Company-specific
    ke = rf + beta * erp + crp_val + size_prem + comp_risk
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

    if use_unlevered:
        st.latex(r"\beta_L = \beta_U \times (1 + (1-t) \times D/E) = "
                 f"{beta_u:.2f} \\times (1 + (1-{tax_w:.2f}) \\times {de:.2f}) = {beta:.2f}")

    ke_formula_parts = f"{rf*100:.2f}\\% + {beta:.2f} \\times {erp*100:.2f}\\%"
    if crp_val > 0:
        ke_formula_parts += f" + {crp_val*100:.2f}\\%_{{CRP}}"
    if size_prem > 0:
        ke_formula_parts += f" + {size_prem*100:.2f}\\%_{{size}}"
    if comp_risk > 0:
        ke_formula_parts += f" + {comp_risk*100:.2f}\\%_{{co}}"
    st.latex(r"K_e = R_f + \beta \times ERP + \text{premia} = " +
             ke_formula_parts + f" = {ke*100:.2f}\\%")
    st.latex(r"WACC = w_e \cdot K_e + w_d \cdot K_d(1-t) = "
             f"{we:.3f} \\times {ke*100:.2f}\\% + {wd:.3f} \\times {kd_post*100:.2f}\\% = {wacc*100:.2f}\\%")

    # ── WACC Buildup Chart ──
    st.subheader(T("wacc_buildup"))
    buildup_labels = ["Rf", "Beta x ERP"]
    buildup_vals = [rf * 100, beta * erp * 100]
    if crp_val > 0:
        buildup_labels.append("CRP")
        buildup_vals.append(crp_val * 100)
    if size_prem > 0:
        buildup_labels.append(T("size_premium").replace(" (%)", ""))
        buildup_vals.append(size_prem * 100)
    if comp_risk > 0:
        buildup_labels.append(T("company_risk").replace(" (%)", ""))
        buildup_vals.append(comp_risk * 100)

    fig_bu = go.Figure()
    # Ke buildup as stacked
    fig_bu.add_trace(go.Bar(
        x=["Ke"], y=[rf * 100], name="Rf", marker_color="#93c5fd",
        text=f"{rf*100:.2f}%", textposition="inside",
    ))
    fig_bu.add_trace(go.Bar(
        x=["Ke"], y=[beta * erp * 100], name="Beta x ERP", marker_color="#1a56db",
        text=f"{beta * erp * 100:.2f}%", textposition="inside",
    ))
    if crp_val > 0:
        fig_bu.add_trace(go.Bar(
            x=["Ke"], y=[crp_val * 100], name="CRP", marker_color="#f59e0b",
            text=f"{crp_val*100:.2f}%", textposition="inside",
        ))
    if size_prem > 0:
        fig_bu.add_trace(go.Bar(
            x=["Ke"], y=[size_prem * 100], name="Size", marker_color="#8b5cf6",
            text=f"{size_prem*100:.2f}%", textposition="inside",
        ))
    if comp_risk > 0:
        fig_bu.add_trace(go.Bar(
            x=["Ke"], y=[comp_risk * 100], name="Co. Risk", marker_color="#ef4444",
            text=f"{comp_risk*100:.2f}%", textposition="inside",
        ))
    # WACC composition
    fig_bu.add_trace(go.Bar(
        x=["WACC"], y=[we * ke * 100], name=f"Ke x {we*100:.0f}%",
        marker_color="#1a56db",
        text=f"{we * ke * 100:.2f}%", textposition="inside",
    ))
    fig_bu.add_trace(go.Bar(
        x=["WACC"], y=[wd * kd_post * 100], name=f"Kd x {wd*100:.0f}%",
        marker_color="#64748b",
        text=f"{wd * kd_post * 100:.2f}%", textposition="inside",
    ))
    fig_bu.update_layout(
        barmode="stack", height=350,
        title=T("wacc_buildup"),
        yaxis_title="%",
        margin=dict(t=50, b=40),
        showlegend=True,
    )
    st.plotly_chart(fig_bu, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — TERMINAL VALUE (Enhanced)
# ═════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.info(T("tv_info"))

    tv_options = [T("gordon"), T("exit_mult")]
    tv_method = st.radio(T("tv_method"), tv_options, horizontal=True,
                         key="dcf_tv_method_radio")
    is_gordon = tv_method == tv_options[0]

    tv1, tv2 = st.columns(2)
    with tv1:
        if is_gordon:
            st.number_input(T("perp_growth"), 0.0, 15.0, step=0.1, format="%.2f",
                            key="dcf_perp_growth")
        else:
            st.number_input(T("exit_multiple"), 1.0, 50.0, step=0.5, format="%.1f",
                            key="dcf_exit_multiple")

    with tv2:
        st.toggle(T("mid_year_convention"), key="dcf_mid_year")

    # Fade period
    st.markdown("---")
    with st.expander(T("fade_info")):
        f1, f2 = st.columns(2)
        with f1:
            st.number_input(T("fade_period"), 0, 10, step=1, key="dcf_fade_period")
        with f2:
            st.number_input(T("terminal_growth_fade"), 0.0, 30.0, step=0.5,
                            format="%.1f", key="dcf_fade_start_growth")

# ═════════════════════════════════════════════════════════════════════════════
# CORE DCF CALCULATION (shared by Valuation + Sensitivity tabs)
# ═════════════════════════════════════════════════════════════════════════════
def _run_dcf(wacc_override=None, g_override=None, exit_mult_override=None,
             rev_growth_adj=0.0, margin_adj=0.0):
    """Return dict with full DCF outputs. Supports FCFF and FCFE."""
    n = st.session_state["dcf_proj_years"]
    base_rev = st.session_state["dcf_revenue"]
    capex_pct = st.session_state["dcf_capex_pct"] / 100
    da_pct = st.session_state["dcf_da_pct"] / 100
    nwc_pct = st.session_state["dcf_nwc_pct"] / 100
    tax = st.session_state["dcf_tax_rate"] / 100
    _wacc = wacc_override if wacc_override is not None else wacc
    mid_year = st.session_state.get("dcf_mid_year", False)
    fade_n = st.session_state.get("dcf_fade_period", 0)
    fade_start_g = st.session_state.get("dcf_fade_start_growth", 6.0) / 100

    # FCFE specific
    approach_opts = [T("fcff_label"), T("fcfe_label")]
    _is_fcfe = (st.session_state.get("dcf_approach_radio", approach_opts[0])
                == approach_opts[1])
    net_borr_pct = st.session_state.get("dcf_net_borrowings_pct", 1.0) / 100
    interest_exp = st.session_state.get("dcf_interest_expense", 30.0)

    # Discount rate for FCFE = cost of equity
    if _is_fcfe:
        _discount = ke if wacc_override is None else wacc_override
    else:
        _discount = _wacc

    rows = {
        "revenue": [], "ebitda": [], "da": [], "ebit": [], "taxes": [],
        "nopat": [], "plus_da": [], "capex": [], "nwc": [], "fcff": [],
        "fcfe": [], "net_borr": [], "interest": [],
        "pv_fcff": [], "pv_fcfe": [],
    }

    rev_prev = base_rev
    for y in range(1, n + 1):
        g = st.session_state.get(f"dcf_rev_growth_{y}", 5.0) / 100 + rev_growth_adj / 100
        m = st.session_state.get(f"dcf_ebitda_margin_{y}", 25.0) / 100 + margin_adj / 100
        m = max(m, 0.0)  # floor margin at 0
        rev = rev_prev * (1 + g)
        ebitda = rev * m
        da = rev * da_pct
        ebit = ebitda - da
        taxes_val = max(ebit * tax, 0)
        nopat = ebit - taxes_val
        capex = rev * capex_pct
        nwc_val = rev * nwc_pct
        fcff = nopat + da - capex - nwc_val

        # FCFE: Net Income + D&A - CapEx - dNWC + Net Borrowings
        net_inc_y = (ebit - interest_exp) * (1 - tax)
        net_borr_y = rev * net_borr_pct
        fcfe = net_inc_y + da - capex - nwc_val + net_borr_y

        # Discount factor with mid-year convention
        disc_period = y - 0.5 if mid_year else y
        pv_ff = fcff / ((1 + _discount) ** disc_period)
        pv_fe = fcfe / ((1 + _discount) ** disc_period)

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
        rows["fcfe"].append(fcfe)
        rows["net_borr"].append(net_borr_y)
        rows["interest"].append(interest_exp)
        rows["pv_fcff"].append(pv_ff)
        rows["pv_fcfe"].append(pv_fe)

        rev_prev = rev

    if _is_fcfe:
        sum_pv_fcf = sum(rows["pv_fcfe"])
    else:
        sum_pv_fcf = sum(rows["pv_fcff"])

    # Fade period cash flows
    fade_pv = 0.0
    fade_rows = {"year": [], "growth": [], "fcf": [], "pv": []}
    if fade_n > 0:
        perp_g = (g_override if g_override is not None
                  else st.session_state["dcf_perp_growth"] / 100)
        last_rev = rows["revenue"][-1]
        last_margin = st.session_state.get(f"dcf_ebitda_margin_{n}", 25.0) / 100 + margin_adj / 100
        for fy in range(1, fade_n + 1):
            # Linear interpolation from fade_start_g to perp_g
            fade_g = fade_start_g + (perp_g - fade_start_g) * (fy / fade_n)
            last_rev = last_rev * (1 + fade_g)
            ebitda_f = last_rev * last_margin
            da_f = last_rev * da_pct
            ebit_f = ebitda_f - da_f
            tax_f = max(ebit_f * tax, 0)
            nopat_f = ebit_f - tax_f
            capex_f = last_rev * capex_pct
            nwc_f = last_rev * nwc_pct
            fcf_f = nopat_f + da_f - capex_f - nwc_f
            disc_p = (n + fy - 0.5) if mid_year else (n + fy)
            pv_f = fcf_f / ((1 + _discount) ** disc_p)
            fade_pv += pv_f
            fade_rows["year"].append(n + fy)
            fade_rows["growth"].append(fade_g * 100)
            fade_rows["fcf"].append(fcf_f)
            fade_rows["pv"].append(pv_f)
        sum_pv_fcf += fade_pv

    # Terminal value
    last_fcff = rows["fcff"][-1] if fade_n == 0 else fade_rows["fcf"][-1]
    last_fcfe = rows["fcfe"][-1]
    last_ebitda = rows["ebitda"][-1] if fade_n == 0 else (rows["ebitda"][-1])

    # Recalculate last_ebitda for fade
    if fade_n > 0:
        _last_rev_fade = rows["revenue"][-1]
        for fy in range(1, fade_n + 1):
            fade_g = fade_start_g + ((g_override if g_override is not None
                      else st.session_state["dcf_perp_growth"] / 100) - fade_start_g) * (fy / fade_n)
            _last_rev_fade = _last_rev_fade * (1 + fade_g)
        last_margin_f = st.session_state.get(f"dcf_ebitda_margin_{n}", 25.0) / 100 + margin_adj / 100
        last_ebitda = _last_rev_fade * last_margin_f

    # Determine method from radio
    use_gordon = (st.session_state.get("dcf_tv_method_radio", T("gordon")) == tv_options[0]
                  if exit_mult_override is None and g_override is None else
                  g_override is not None)

    total_n = n + fade_n

    if use_gordon or g_override is not None:
        g_tv = (g_override if g_override is not None
                else st.session_state["dcf_perp_growth"] / 100)
        if _is_fcfe:
            cf_for_tv = last_fcfe
        else:
            cf_for_tv = last_fcff
        if _discount <= g_tv:
            tv = cf_for_tv * 50  # cap to avoid infinity
        else:
            tv = cf_for_tv * (1 + g_tv) / (_discount - g_tv)
        # Implied exit multiple cross-check
        implied_exit = tv / last_ebitda if last_ebitda != 0 else 0
        implied_perp_g = None
    else:
        em = exit_mult_override if exit_mult_override is not None else st.session_state["dcf_exit_multiple"]
        tv = last_ebitda * em
        implied_exit = em
        # Implied perpetuity growth rate cross-check: g = WACC - FCF*(1)/TV
        if tv != 0 and _discount > 0:
            if _is_fcfe:
                implied_perp_g = _discount - (last_fcfe / tv)
            else:
                implied_perp_g = _discount - (last_fcff / tv)
        else:
            implied_perp_g = None

    disc_tv_period = (total_n - 0.5) if mid_year else total_n
    pv_tv = tv / ((1 + _discount) ** disc_tv_period)
    ev = sum_pv_fcf + pv_tv

    # Bridge to equity
    use_detailed = st.session_state.get("dcf_use_detailed_bridge", False)
    if _is_fcfe:
        # FCFE gives equity value directly
        equity = ev
        net_debt_val = 0
    elif use_detailed:
        total_debt_v = st.session_state.get("dcf_total_debt", 300.0)
        minority_v = st.session_state.get("dcf_minority_interest", 0.0)
        preferred_v = st.session_state.get("dcf_preferred_equity", 0.0)
        cash_v = st.session_state.get("dcf_cash_equiv", 100.0)
        eq_inv_v = st.session_state.get("dcf_equity_investments", 0.0)
        pension_v = st.session_state.get("dcf_unfunded_pensions", 0.0)
        nol_v = st.session_state.get("dcf_nol_value", 0.0)
        # Pensions after tax shield; NOLs add value
        pension_adj = pension_v * (1 - st.session_state["dcf_tax_rate"] / 100)
        net_debt_val = (total_debt_v + minority_v + preferred_v + pension_adj
                        - cash_v - eq_inv_v - nol_v)
        equity = ev - net_debt_val
    else:
        net_debt_val = st.session_state.get("dcf_net_debt", 0)
        equity = ev - net_debt_val

    if use_detailed and not _is_fcfe:
        shares = st.session_state.get("dcf_diluted_shares",
                                       st.session_state["dcf_shares"])
    else:
        shares = st.session_state["dcf_shares"]
    price = equity / shares if shares > 0 else 0
    current = st.session_state["dcf_share_price"]
    upside_pct = ((price / current) - 1) * 100 if current > 0 else 0
    tv_pct = (pv_tv / ev * 100) if ev != 0 else 0

    return {
        "rows": rows, "n": n, "sum_pv_fcf": sum_pv_fcf, "tv": tv,
        "pv_tv": pv_tv, "ev": ev, "net_debt": net_debt_val,
        "equity": equity, "price": price, "upside": upside_pct,
        "tv_pct": tv_pct,
        "wacc_used": _discount, "is_fcfe": _is_fcfe,
        "implied_exit": implied_exit if use_gordon or g_override is not None else em,
        "implied_perp_g": implied_perp_g,
        "fade_rows": fade_rows, "fade_n": fade_n,
        "shares": shares,
    }

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — VALUATION
# ═════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.info(T("val_info"))

    # Bridge inputs
    val_c1, val_c2 = st.columns(2)
    with val_c1:
        st.toggle(T("use_detailed_bridge"), key="dcf_use_detailed_bridge")

    use_detailed = st.session_state.get("dcf_use_detailed_bridge", False)

    if not is_fcfe:
        if use_detailed:
            st.subheader(T("vb_title"))
            br1, br2, br3 = st.columns(3)
            with br1:
                st.number_input(T("enter_total_debt"), step=10.0, format="%.1f",
                                key="dcf_total_debt")
                st.number_input(T("enter_minority"), step=5.0, format="%.1f",
                                key="dcf_minority_interest")
            with br2:
                st.number_input(T("enter_preferred"), step=5.0, format="%.1f",
                                key="dcf_preferred_equity")
                st.number_input(T("enter_cash"), step=10.0, format="%.1f",
                                key="dcf_cash_equiv")
            with br3:
                st.number_input(T("enter_eq_invest"), step=5.0, format="%.1f",
                                key="dcf_equity_investments")
                st.number_input("Unfunded Pensions" if lang == "EN" else "Pensoes nao-financiadas",
                                step=5.0, format="%.1f", key="dcf_unfunded_pensions")
                st.number_input("NOL Value (Tax Asset)" if lang == "EN" else "Valor NOL (Ativo Fiscal)",
                                step=5.0, format="%.1f", key="dcf_nol_value")
                st.number_input(T("enter_diluted_shares"), min_value=0.1, step=10.0,
                                format="%.1f", key="dcf_diluted_shares")
        else:
            st.number_input(T("enter_net_debt"), step=10.0, format="%.1f",
                            key="dcf_net_debt")

    res = _run_dcf()

    # ── Projection table ──
    st.subheader(T("val_title"))
    year_labels = [f"{T('year')} {y}" for y in range(1, res["n"] + 1)]

    if res["is_fcfe"]:
        tbl = pd.DataFrame({
            T("year"): year_labels,
            T("revenue"): [fmt_mm(v) for v in res["rows"]["revenue"]],
            T("ebitda"): [fmt_mm(v) for v in res["rows"]["ebitda"]],
            T("da"): [fmt_mm(v) for v in res["rows"]["da"]],
            T("ebit"): [fmt_mm(v) for v in res["rows"]["ebit"]],
            T("interest"): [fmt_mm(v) for v in res["rows"]["interest"]],
            T("taxes"): [fmt_mm(v) for v in res["rows"]["taxes"]],
            T("plus_da"): [fmt_mm(v) for v in res["rows"]["plus_da"]],
            T("minus_capex"): [fmt_mm(v) for v in res["rows"]["capex"]],
            T("minus_nwc"): [fmt_mm(v) for v in res["rows"]["nwc"]],
            T("net_borr"): [fmt_mm(v) for v in res["rows"]["net_borr"]],
            T("fcfe"): [fmt_mm(v) for v in res["rows"]["fcfe"]],
            T("pv_fcfe"): [fmt_mm(v) for v in res["rows"]["pv_fcfe"]],
        })
    else:
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

    # Fade period table
    if res["fade_n"] > 0 and len(res["fade_rows"]["year"]) > 0:
        st.subheader(T("fade_info"))
        fade_tbl = pd.DataFrame({
            T("year"): [f"{T('year')} {y}" for y in res["fade_rows"]["year"]],
            "Growth (%)": [f"{g:.2f}" for g in res["fade_rows"]["growth"]],
            "FCF": [fmt_mm(v) for v in res["fade_rows"]["fcf"]],
            "PV": [fmt_mm(v) for v in res["fade_rows"]["pv"]],
        })
        st.dataframe(fade_tbl, use_container_width=True, hide_index=True)

    # ── Bridge ──
    st.subheader(T("bridge_title"))

    # Terminal value warning
    if res["tv_pct"] > 75:
        st.warning(T("tv_pct_warning").format(pct=res["tv_pct"]))

    if use_detailed and not res["is_fcfe"]:
        # Detailed bridge cards
        bk1, bk2, bk3, bk4 = st.columns(4)
        bk1.markdown(_mc(T("sum_pv_fcf"), fmt_mm(res["sum_pv_fcf"])), unsafe_allow_html=True)
        bk2.markdown(_mc(T("pv_tv"), fmt_mm(res["pv_tv"])), unsafe_allow_html=True)
        bk3.markdown(_mc(T("enterprise_value"), fmt_mm(res["ev"])), unsafe_allow_html=True)
        bk4.markdown(_mc(T("tv_pct_ev"), f"{res['tv_pct']:.1f}%",
                         color="amber" if res["tv_pct"] > 75 else None),
                     unsafe_allow_html=True)

        st.markdown("---")
        st.subheader(T("vb_title"))
        db1, db2, db3, db4, db5, db6 = st.columns(6)
        db1.markdown(_mc(T("enterprise_value"), fmt_mm(res["ev"])), unsafe_allow_html=True)
        db2.markdown(_mc(T("total_debt"), fmt_mm(-st.session_state["dcf_total_debt"])),
                     unsafe_allow_html=True)
        db3.markdown(_mc(T("minority_interest"), fmt_mm(-st.session_state["dcf_minority_interest"])),
                     unsafe_allow_html=True)
        db4.markdown(_mc(T("cash_equiv"), fmt_mm(st.session_state["dcf_cash_equiv"])),
                     unsafe_allow_html=True)
        db5.markdown(_mc(T("equity_investments"), fmt_mm(st.session_state["dcf_equity_investments"])),
                     unsafe_allow_html=True)
        db6.markdown(_mc(T("equity_value"), fmt_mm(res["equity"]), color="green" if res["equity"] > 0 else "red"),
                     unsafe_allow_html=True)

        # Waterfall for detailed bridge
        wf_labels = [T("enterprise_value"), T("total_debt"), T("minority_interest"),
                     T("preferred_equity"), T("cash_equiv"), T("equity_investments"),
                     T("equity_value")]
        wf_values = [res["ev"], -st.session_state["dcf_total_debt"],
                     -st.session_state["dcf_minority_interest"],
                     -st.session_state["dcf_preferred_equity"],
                     st.session_state["dcf_cash_equiv"],
                     st.session_state["dcf_equity_investments"],
                     res["equity"]]
        wf_measures = ["absolute", "relative", "relative", "relative",
                       "relative", "relative", "total"]
    else:
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        b1.markdown(_mc(T("sum_pv_fcf"), fmt_mm(res["sum_pv_fcf"])), unsafe_allow_html=True)
        b2.markdown(_mc(T("pv_tv"), fmt_mm(res["pv_tv"])), unsafe_allow_html=True)
        b3.markdown(_mc(T("enterprise_value") if not res["is_fcfe"] else T("equity_value"),
                        fmt_mm(res["ev"])), unsafe_allow_html=True)
        if not res["is_fcfe"]:
            b4.markdown(_mc(T("net_debt"), fmt_mm(res["net_debt"])), unsafe_allow_html=True)
            b5.markdown(_mc(T("equity_value"), fmt_mm(res["equity"])), unsafe_allow_html=True)
        else:
            b4.markdown(_mc(T("equity_value"), fmt_mm(res["equity"])), unsafe_allow_html=True)
            b5.markdown(_mc(T("dcf_approach"), T("fcfe_label")), unsafe_allow_html=True)
        b6.markdown(_mc(T("tv_pct_ev"), f"{res['tv_pct']:.1f}%",
                        color="amber" if res["tv_pct"] > 75 else None),
                    unsafe_allow_html=True)

        if res["is_fcfe"]:
            wf_labels = [T("sum_pv_fcf"), T("pv_tv"), T("equity_value")]
            wf_values = [res["sum_pv_fcf"], res["pv_tv"], res["equity"]]
            wf_measures = ["relative", "relative", "total"]
        else:
            wf_labels = [T("sum_pv_fcf"), T("pv_tv"), T("enterprise_value"),
                         T("net_debt"), T("equity_value")]
            wf_values = [res["sum_pv_fcf"], res["pv_tv"], res["ev"],
                         -res["net_debt"], res["equity"]]
            wf_measures = ["relative", "relative", "total", "relative", "total"]

    # ── Terminal Value Cross-Check ──
    st.markdown("---")
    st.subheader(T("tv_crosscheck"))
    xc1, xc2 = st.columns(2)
    with xc1:
        ie = res.get("implied_exit", 0)
        st.markdown(_mc(T("implied_exit_mult"), f"{ie:.1f}x"), unsafe_allow_html=True)
    with xc2:
        ig = res.get("implied_perp_g")
        if ig is not None:
            st.markdown(_mc(T("implied_perp_growth"), f"{ig*100:.2f}%"), unsafe_allow_html=True)
        else:
            st.markdown(_mc(T("implied_perp_growth"), "N/A (Gordon)"), unsafe_allow_html=True)

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
    fig_w = go.Figure(go.Waterfall(
        x=wf_labels,
        y=wf_values,
        measure=wf_measures,
        textposition="outside",
        text=[fmt_mm(v) for v in wf_values],
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
# TAB 6 — FINANCIAL STATEMENTS (3-Statement Integration)
# ═════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.info(T("fs_info"))

    # ── Assumptions ──
    with st.expander(T("fs_assumptions"), expanded=True):
        fa1, fa2, fa3, fa4 = st.columns(4)
        with fa1:
            st.number_input(T("fs_cogs_pct"), 0.0, 100.0, step=0.5,
                            format="%.1f", key="dcf_fs_cogs_pct")
            st.number_input(T("fs_sga_pct"), 0.0, 100.0, step=0.5,
                            format="%.1f", key="dcf_fs_sga_pct")
            st.number_input(T("fs_oca_pct"), 0.0, 50.0, step=0.5,
                            format="%.1f", key="dcf_fs_oca_pct")
        with fa2:
            st.number_input(T("fs_dso"), 0.0, 365.0, step=1.0,
                            format="%.0f", key="dcf_fs_dso")
            st.number_input(T("fs_dio"), 0.0, 365.0, step=1.0,
                            format="%.0f", key="dcf_fs_dio")
            st.number_input(T("fs_dpo"), 0.0, 365.0, step=1.0,
                            format="%.0f", key="dcf_fs_dpo")
        with fa3:
            st.number_input(T("fs_init_cash"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_init_cash")
            st.number_input(T("fs_st_debt"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_st_debt")
            st.number_input(T("fs_lt_debt"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_lt_debt")
        with fa4:
            st.number_input(T("fs_goodwill"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_goodwill")
            st.number_input(T("fs_other_lta"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_other_lta")
            st.number_input(T("fs_common_stock"), 0.0, step=10.0, format="%.1f",
                            key="dcf_fs_common_stock")

        fb1, fb2 = st.columns(2)
        with fb1:
            st.number_input(T("fs_int_rate"), 0.0, 30.0, step=0.25,
                            format="%.2f", key="dcf_fs_int_rate")
        with fb2:
            st.number_input(T("fs_payout"), 0.0, 100.0, step=1.0,
                            format="%.1f", key="dcf_fs_payout")

    # ── Build 3 statements using shared DCF projections ──
    _fs_res = _run_dcf()
    n_fs = _fs_res["n"]
    _rev = _fs_res["rows"]["revenue"]
    _ebitda = _fs_res["rows"]["ebitda"]
    _da = _fs_res["rows"]["da"]
    _capex = _fs_res["rows"]["capex"]
    _nwc_proj = _fs_res["rows"]["nwc"]

    # Assumption values
    cogs_pct = st.session_state["dcf_fs_cogs_pct"] / 100
    sga_pct = st.session_state["dcf_fs_sga_pct"] / 100
    dso = st.session_state["dcf_fs_dso"]
    dio = st.session_state["dcf_fs_dio"]
    dpo = st.session_state["dcf_fs_dpo"]
    oca_pct = st.session_state["dcf_fs_oca_pct"] / 100
    gw_val = st.session_state["dcf_fs_goodwill"]
    olta_val = st.session_state["dcf_fs_other_lta"]
    ltd_0 = st.session_state["dcf_fs_lt_debt"]
    std_0 = st.session_state["dcf_fs_st_debt"]
    payout = st.session_state["dcf_fs_payout"] / 100
    int_rate = st.session_state["dcf_fs_int_rate"] / 100
    cash_0 = st.session_state["dcf_fs_init_cash"]
    cs_val = st.session_state["dcf_fs_common_stock"]
    tax_rate_fs = st.session_state["dcf_tax_rate"] / 100
    net_borr_pct_fs = st.session_state.get("dcf_net_borrowings_pct", 1.0) / 100

    # Compute Income Statement
    is_cogs = [r * cogs_pct for r in _rev]
    is_gross = [r - c for r, c in zip(_rev, is_cogs)]
    is_sga = [r * sga_pct for r in _rev]
    # EBITDA from projections (already revenue * margin). Keep consistent.
    is_ebitda = _ebitda
    is_da = _da
    is_ebit = [e - d for e, d in zip(is_ebitda, is_da)]

    # Debt schedule: opening LTD + STD, change in LTD from net borrowings %
    ltd_schedule = []
    std_schedule = []
    ltd_prev = ltd_0
    std_prev = std_0
    net_borr_list = []
    int_exp_list = []
    for i in range(n_fs):
        nb = _rev[i] * net_borr_pct_fs
        net_borr_list.append(nb)
        # Apply all net borrowings to long-term debt
        ltd_new = ltd_prev + nb
        std_new = std_prev  # keep ST debt flat
        # Interest on average of beginning and ending total debt
        avg_debt = ((ltd_prev + std_prev) + (ltd_new + std_new)) / 2
        int_exp = avg_debt * int_rate
        int_exp_list.append(int_exp)
        ltd_schedule.append(ltd_new)
        std_schedule.append(std_new)
        ltd_prev = ltd_new
        std_prev = std_new

    is_pretax = [ebit - ie for ebit, ie in zip(is_ebit, int_exp_list)]
    is_tax = [max(pt * tax_rate_fs, 0) for pt in is_pretax]
    is_ni = [pt - tx for pt, tx in zip(is_pretax, is_tax)]

    # ── Compute BS working capital line items first (needed for ΔNWC) ───────
    bs_ar_pre = [r * dso / 365 for r in _rev]
    bs_inv_pre = [c * dio / 365 for c in is_cogs]
    bs_oca_pre = [r * oca_pct for r in _rev]
    bs_ap_pre = [c * dpo / 365 for c in is_cogs]

    # Opening NWC (t=0) using base-year revenue
    _open_ar = st.session_state["dcf_revenue"] * dso / 365
    _open_cogs_now = st.session_state["dcf_revenue"] * cogs_pct
    _open_inv = _open_cogs_now * dio / 365
    _open_oca = st.session_state["dcf_revenue"] * oca_pct
    _open_ap = _open_cogs_now * dpo / 365
    _opening_nwc = _open_ar + _open_inv + _open_oca - _open_ap

    # Year-by-year NWC and ΔNWC (consistent with BS line items)
    nwc_series = [bs_ar_pre[i] + bs_inv_pre[i] + bs_oca_pre[i] - bs_ap_pre[i]
                  for i in range(n_fs)]
    cf_nwc = []
    _prev_nwc = _opening_nwc
    for n in nwc_series:
        cf_nwc.append(n - _prev_nwc)
        _prev_nwc = n

    # Cash Flow Statement
    cf_ni = is_ni
    cf_da = is_da
    cf_cfo = [ni + da - nwc for ni, da, nwc in zip(cf_ni, cf_da, cf_nwc)]
    cf_capex = _capex
    cf_cfi = [-cp for cp in cf_capex]
    cf_net_borr = net_borr_list
    cf_div = [max(ni, 0) * payout for ni in cf_ni]
    cf_cff = [nb - dv for nb, dv in zip(cf_net_borr, cf_div)]
    cf_net_change = [o + i + f for o, i, f in zip(cf_cfo, cf_cfi, cf_cff)]

    # Beginning/ending cash walk
    cf_beg_cash = []
    cf_end_cash = []
    _cash_prev = cash_0
    for nc in cf_net_change:
        cf_beg_cash.append(_cash_prev)
        _cash_prev = _cash_prev + nc
        cf_end_cash.append(_cash_prev)

    # Balance Sheet
    bs_cash = cf_end_cash
    bs_ar = [r * dso / 365 for r in _rev]
    bs_inv = [c * dio / 365 for c in is_cogs]
    bs_oca = [r * oca_pct for r in _rev]
    bs_tca = [c + a + i + o for c, a, i, o in zip(bs_cash, bs_ar, bs_inv, bs_oca)]

    # PP&E walk: opening PP&E = initial guess. Use revenue*capex_pct seed? Set opening = sum approach:
    # Simpler: initial PP&E such that first-year opening is reasonable. Use revenue * da_pct / (capex_pct - da_pct) may be negative.
    # Use practical initial PP&E = 3x last year DA as a placeholder seed; but better: start with initial = first year revenue * capex_pct * 3.
    ppe_0 = _rev[0] * st.session_state["dcf_capex_pct"] / 100 * 3.0 if n_fs > 0 else 0.0
    bs_ppe = []
    _ppe_prev = ppe_0
    for i in range(n_fs):
        _ppe_new = _ppe_prev + cf_capex[i] - is_da[i]
        bs_ppe.append(_ppe_new)
        _ppe_prev = _ppe_new

    bs_gw = [gw_val] * n_fs
    bs_olta = [olta_val] * n_fs
    bs_ta = [ca + pp + g + o for ca, pp, g, o in zip(bs_tca, bs_ppe, bs_gw, bs_olta)]

    bs_ap = [c * dpo / 365 for c in is_cogs]
    bs_std = std_schedule
    bs_tcl = [a + s for a, s in zip(bs_ap, bs_std)]
    bs_ltd = ltd_schedule
    bs_tl = [tcl + ltd for tcl, ltd in zip(bs_tcl, bs_ltd)]

    bs_cs = [cs_val] * n_fs
    # Retained earnings walk - seed initial RE so balance sheet balances in year 0 (opening)
    # Opening balance requirement: Assets_0 = Liab_0 + Equity_0
    # Use an initial RE computed from opening balance sheet (t=0):
    open_ar = st.session_state["dcf_revenue"] * dso / 365
    open_cogs = st.session_state["dcf_revenue"] * cogs_pct
    open_inv = open_cogs * dio / 365
    open_oca = st.session_state["dcf_revenue"] * oca_pct
    open_ap = open_cogs * dpo / 365
    open_ta = cash_0 + open_ar + open_inv + open_oca + ppe_0 + gw_val + olta_val
    open_tl = open_ap + std_0 + ltd_0
    re_0 = open_ta - open_tl - cs_val  # plug to balance opening

    bs_re = []
    _re_prev = re_0
    for i in range(n_fs):
        _re_new = _re_prev + cf_ni[i] - cf_div[i]
        bs_re.append(_re_new)
        _re_prev = _re_new

    bs_te = [cs + re for cs, re in zip(bs_cs, bs_re)]
    bs_tle = [tl + te for tl, te in zip(bs_tl, bs_te)]

    # Balance check
    bs_diff = [ta - tle for ta, tle in zip(bs_ta, bs_tle)]
    max_abs_diff = max([abs(d) for d in bs_diff]) if bs_diff else 0
    is_balanced = max_abs_diff < 0.5  # threshold in MM

    year_labels_fs = [f"{T('year')} {y}" for y in range(1, n_fs + 1)]

    # ── Balance Check Indicator ──
    st.markdown("---")
    bc1, bc2, bc3 = st.columns([2, 2, 2])
    bc_color = "green" if is_balanced else "red"
    bc_label = T("fs_balanced") if is_balanced else T("fs_unbalanced")
    bc1.markdown(_mc(T("fs_balance_check"), bc_label, color=bc_color),
                 unsafe_allow_html=True)
    bc2.markdown(_mc(T("fs_diff") + " (Max)", fmt_mm(max_abs_diff),
                     color=("green" if is_balanced else "red")),
                 unsafe_allow_html=True)
    bc3.markdown(_mc(T("fs_ta") + f" ({T('year')} {n_fs})", fmt_mm(bs_ta[-1] if bs_ta else 0)),
                 unsafe_allow_html=True)

    # ── Income Statement (unified renderer) ──
    st.markdown("---")
    st.subheader(T("fs_is_title"))
    from backend import render_3stmt_table, DF_TABLE_CSS as _DCF_DF_CSS
    def _fmt_list(arr):
        return [fmt_mm(x) for x in arr]
    _is_rows = [
        (T("fs_revenue"),  _fmt_list(_rev),         "line"),
        (T("fs_cogs"),     _fmt_list(is_cogs),      "line"),
        (T("fs_gross"),    _fmt_list(is_gross),     "subtotal"),
        (T("fs_sga"),      _fmt_list(is_sga),       "line"),
        (T("fs_ebitda"),   _fmt_list(is_ebitda),    "subtotal"),
        (T("fs_da"),       _fmt_list(is_da),        "line"),
        (T("fs_ebit"),     _fmt_list(is_ebit),      "subtotal"),
        (T("fs_interest"), _fmt_list(int_exp_list), "line"),
        (T("fs_pretax"),   _fmt_list(is_pretax),    "subtotal"),
        (T("fs_tax"),      _fmt_list(is_tax),       "line"),
        (T("fs_ni"),       _fmt_list(is_ni),        "total"),
    ]
    st.markdown(_DCF_DF_CSS + render_3stmt_table(_is_rows, year_labels_fs),
                unsafe_allow_html=True)

    # ── Cash Flow Statement (unified renderer) ──
    st.markdown("---")
    st.subheader(T("fs_cf_title"))
    _cf_rows = [
        (T("fs_ni"),         _fmt_list(cf_ni),         "line"),
        (T("fs_plus_da"),    _fmt_list(cf_da),         "line"),
        (T("fs_min_nwc"),    _fmt_list(cf_nwc),        "line"),
        (T("fs_cfo"),        _fmt_list(cf_cfo),        "subtotal"),
        (T("fs_min_capex"),  _fmt_list(cf_capex),      "line"),
        (T("fs_cfi"),        _fmt_list(cf_cfi),        "subtotal"),
        (T("fs_net_borr"),   _fmt_list(cf_net_borr),   "line"),
        (T("fs_min_div"),    _fmt_list(cf_div),        "line"),
        (T("fs_cff"),        _fmt_list(cf_cff),        "subtotal"),
        (T("fs_net_change"), _fmt_list(cf_net_change), "subtotal"),
        (T("fs_beg_cash"),   _fmt_list(cf_beg_cash),   "line"),
        (T("fs_end_cash"),   _fmt_list(cf_end_cash),   "total"),
    ]
    st.markdown(_DCF_DF_CSS + render_3stmt_table(_cf_rows, year_labels_fs),
                unsafe_allow_html=True)

    # ── Balance Sheet (standardized renderer) ──
    st.markdown("---")
    st.subheader(T("fs_bs_title"))
    from backend import render_3stmt_table, DF_TABLE_CSS
    _bs_rows = [
        (T("fs_assets"), [], "header"),
        (T("fs_cash"),   [fmt_mm(bs_cash[i])  for i in range(n_fs)], "line"),
        (T("fs_ar"),     [fmt_mm(bs_ar[i])    for i in range(n_fs)], "line"),
        (T("fs_inv"),    [fmt_mm(bs_inv[i])   for i in range(n_fs)], "line"),
        (T("fs_oca"),    [fmt_mm(bs_oca[i])   for i in range(n_fs)], "line"),
        (T("fs_tca"),    [fmt_mm(bs_tca[i])   for i in range(n_fs)], "subtotal"),
        (T("fs_ppe"),    [fmt_mm(bs_ppe[i])   for i in range(n_fs)], "line"),
        (T("fs_gw"),     [fmt_mm(bs_gw[i])    for i in range(n_fs)], "line"),
        (T("fs_olta"),   [fmt_mm(bs_olta[i])  for i in range(n_fs)], "line"),
        (T("fs_ta"),     [fmt_mm(bs_ta[i])    for i in range(n_fs)], "total"),
        ("", [], "spacer"),
        (T("fs_liab"),   [], "header"),
        (T("fs_ap"),     [fmt_mm(bs_ap[i])    for i in range(n_fs)], "line"),
        (T("fs_std"),    [fmt_mm(bs_std[i])   for i in range(n_fs)], "line"),
        (T("fs_tcl"),    [fmt_mm(bs_tcl[i])   for i in range(n_fs)], "subtotal"),
        (T("fs_ltd"),    [fmt_mm(bs_ltd[i])   for i in range(n_fs)], "line"),
        (T("fs_tl"),     [fmt_mm(bs_tl[i])    for i in range(n_fs)], "subtotal"),
        ("", [], "spacer"),
        (T("fs_eq"),     [], "header"),
        (T("fs_cs"),     [fmt_mm(bs_cs[i])    for i in range(n_fs)], "line"),
        (T("fs_re"),     [fmt_mm(bs_re[i])    for i in range(n_fs)], "line"),
        (T("fs_te"),     [fmt_mm(bs_te[i])    for i in range(n_fs)], "subtotal"),
        (T("fs_tle"),    [fmt_mm(bs_tle[i])   for i in range(n_fs)], "total"),
    ]
    st.markdown(
        DF_TABLE_CSS + render_3stmt_table(_bs_rows, year_labels_fs),
        unsafe_allow_html=True)

    if not is_balanced:
        st.warning(
            f"{T('fs_unbalanced')}: {T('fs_diff')} = {fmt_mm(max_abs_diff)} "
            f"({'MM' if lang == 'EN' else 'MM'}). "
            + ("Adjust initial Cash, Debt, Common Stock or working capital assumptions."
               if lang == "EN"
               else "Ajuste Caixa inicial, Divida, Capital Social ou premissas de capital de giro.")
        )

    # ── Export to Excel ──
    from backend import export_dataframes_to_xlsx
    _dcf_sheets = {
        "Income Statement": pd.DataFrame({
            year_labels_fs[i]: {
                T("fs_revenue"): fmt_mm(_rev[i]), "COGS": fmt_mm(is_cogs[i]),
                "Gross": fmt_mm(is_gross[i]), "EBITDA": fmt_mm(is_ebitda[i]),
                "EBIT": fmt_mm(is_ebit[i]), "Interest": fmt_mm(int_exp_list[i]),
                "Pre-tax": fmt_mm(is_pretax[i]), "Tax": fmt_mm(is_tax[i]),
                "Net Income": fmt_mm(is_ni[i]),
            } for i in range(n_fs)
        }),
        "Balance Sheet": pd.DataFrame({
            year_labels_fs[i]: {
                "Cash": fmt_mm(bs_cash[i]), "AR": fmt_mm(bs_ar[i]),
                "Inventory": fmt_mm(bs_inv[i]), "Total Assets": fmt_mm(bs_ta[i]),
                "AP": fmt_mm(bs_ap[i]), "LT Debt": fmt_mm(bs_ltd[i]),
                "Total Liab": fmt_mm(bs_tl[i]), "Equity": fmt_mm(bs_te[i]),
                "Total L+E": fmt_mm(bs_tle[i]),
            } for i in range(n_fs)
        }),
    }
    st.download_button(
        label="⬇️  Download Statements (.xlsx)",
        data=export_dataframes_to_xlsx(_dcf_sheets),
        file_name="DCF_Financial_Statements.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 7 — SENSITIVITY (Enhanced)
# ═════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.info(T("sens_info"))

    # Determine if Gordon or Exit method
    tv_radio_val = st.session_state.get("dcf_tv_method_radio", tv_options[0])
    is_gordon_sens = tv_radio_val == tv_options[0]

    sens_tab1, sens_tab2, sens_tab3, sens_tab4 = st.tabs([
        "WACC vs Growth/Multiple",
        T("sens_rev_margin"),
        T("monte_carlo_title"),
        T("scenario_title"),
    ])

    # ── Sub-tab 1: WACC vs Growth/Multiple ──
    with sens_tab1:
        s1, s2 = st.columns(2)
        with s1:
            wacc_min, wacc_max = st.slider(
                T("sens_wacc_label"), 3.0, 25.0, (wacc * 100 - 2.0, wacc * 100 + 2.0),
                step=0.5, format="%.1f%%", key="sens_wacc_slider_1")
        with s2:
            if is_gordon_sens:
                g_min, g_max = st.slider(
                    T("sens_growth_label"), 0.0, 10.0,
                    (max(0.0, st.session_state["dcf_perp_growth"] - 1.5),
                     st.session_state["dcf_perp_growth"] + 1.5),
                    step=0.25, format="%.2f%%", key="sens_g_slider_1")
            else:
                em_min, em_max = st.slider(
                    T("sens_exit_label"), 2.0, 30.0,
                    (max(2.0, st.session_state["dcf_exit_multiple"] - 3.0),
                     st.session_state["dcf_exit_multiple"] + 3.0),
                    step=0.5, format="%.1f", key="sens_em_slider_1")

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

        # ── WACC vs Exit Multiple table (if using Gordon, show additional table) ──
        if is_gordon_sens:
            st.markdown("---")
            st.markdown(f"**WACC** vs **{T('sens_exit_label')}** -- {T('implied_price')}")
            em_range_2 = np.linspace(
                max(2.0, st.session_state["dcf_exit_multiple"] - 3.0),
                st.session_state["dcf_exit_multiple"] + 3.0, 7)
            price_grid_2 = np.zeros((len(wacc_range), len(em_range_2)))
            for i, w in enumerate(wacc_range):
                for j, em in enumerate(em_range_2):
                    r2 = _run_dcf(wacc_override=w, exit_mult_override=em)
                    price_grid_2[i, j] = r2["price"]
            em_labels_2 = [f"{e:.1f}x" for e in em_range_2]
            sens_df_2 = pd.DataFrame(
                [[f"{price_grid_2[i,j]:.2f}" for j in range(len(em_range_2))]
                 for i in range(len(wacc_range))],
                index=wacc_labels, columns=em_labels_2,
            )
            sens_df_2.index.name = "WACC"
            st.dataframe(sens_df_2.style.map(_color_cell), use_container_width=True)

        # ── Football Field Chart ──
        st.subheader(T("football_title"))

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

        fig_ff = go.Figure()
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

        fig_ff.add_vline(
            x=current_price, line_dash="dash", line_color="#dc2626", line_width=2,
            annotation_text=f"{T('current_price_line')}: {current_price:.2f}",
            annotation_position="top", annotation_font_color="#dc2626",
        )
        fig_ff.update_layout(
            title=T("football_title"),
            xaxis_title=T("implied_price"),
            yaxis_title=T("scenario"),
            height=350, margin=dict(l=20, r=20, t=60, b=40), bargap=0.3,
        )
        st.plotly_chart(fig_ff, use_container_width=True)

        # ── Heatmap ──
        fig_hm = go.Figure(data=go.Heatmap(
            z=price_grid,
            x=sec_labels,
            y=wacc_labels,
            colorscale=[
                [0, "#dc2626"], [0.35, "#fbbf24"], [0.5, "#fef3c7"],
                [0.65, "#86efac"], [1, "#16a34a"],
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
            title=f"{T('sens_title')} -- Heatmap",
            xaxis_title=sec_header, yaxis_title="WACC",
            height=450, margin=dict(t=50, b=40),
        )
        st.plotly_chart(fig_hm, use_container_width=True)

    # ── Sub-tab 2: Revenue Growth vs Margin ──
    with sens_tab2:
        st.subheader(T("sens_rev_margin"))
        rm1, rm2 = st.columns(2)
        with rm1:
            rev_min, rev_max = st.slider(
                T("sens_rev_label"), -10.0, 30.0, (5.0, 15.0),
                step=1.0, format="%.0f%%", key="sens_rev_slider")
        with rm2:
            mar_min, mar_max = st.slider(
                T("sens_margin_label"), 5.0, 50.0, (20.0, 35.0),
                step=1.0, format="%.0f%%", key="sens_margin_slider")

        rev_adj_range = np.linspace(rev_min, rev_max, 7)
        mar_adj_range = np.linspace(mar_min, mar_max, 7)

        # For rev/margin sens, we override all years by adjusting from base
        base_avg_growth = np.mean([st.session_state.get(f"dcf_rev_growth_{y}", 5.0)
                                   for y in range(1, n_years + 1)])
        base_avg_margin = np.mean([st.session_state.get(f"dcf_ebitda_margin_{y}", 25.0)
                                   for y in range(1, n_years + 1)])

        price_grid_rm = np.zeros((len(rev_adj_range), len(mar_adj_range)))
        for i, rg in enumerate(rev_adj_range):
            for j, mg in enumerate(mar_adj_range):
                r_rm = _run_dcf(rev_growth_adj=rg - base_avg_growth,
                                margin_adj=(mg - base_avg_margin) / 100)
                price_grid_rm[i, j] = r_rm["price"]

        rev_labels_rm = [f"{r:.0f}%" for r in rev_adj_range]
        mar_labels_rm = [f"{m:.0f}%" for m in mar_adj_range]

        sens_df_rm = pd.DataFrame(
            [[f"{price_grid_rm[i,j]:.2f}" for j in range(len(mar_adj_range))]
             for i in range(len(rev_adj_range))],
            index=rev_labels_rm, columns=mar_labels_rm,
        )
        sens_df_rm.index.name = T("sens_rev_label")

        st.markdown(f"**{T('sens_rev_label')}** vs **{T('sens_margin_label')}** -- {T('implied_price')}")
        st.dataframe(sens_df_rm.style.map(_color_cell), use_container_width=True)

        # Heatmap
        fig_rm = go.Figure(data=go.Heatmap(
            z=price_grid_rm,
            x=mar_labels_rm,
            y=rev_labels_rm,
            colorscale=[[0, "#dc2626"], [0.35, "#fbbf24"], [0.5, "#fef3c7"],
                        [0.65, "#86efac"], [1, "#16a34a"]],
            text=[[f"{price_grid_rm[i,j]:.1f}" for j in range(len(mar_adj_range))]
                  for i in range(len(rev_adj_range))],
            texttemplate="%{text}", textfont={"size": 11},
            colorbar=dict(title=T("implied_price")),
        ))
        fig_rm.update_layout(
            title=T("sens_rev_margin"),
            xaxis_title=T("sens_margin_label"),
            yaxis_title=T("sens_rev_label"),
            height=450, margin=dict(t=50, b=40),
        )
        st.plotly_chart(fig_rm, use_container_width=True)

    # ── Sub-tab 3: Monte Carlo ──
    with sens_tab3:
        st.subheader(T("monte_carlo_title"))

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            mc_n = st.number_input(T("mc_iterations"), 500, 50000, value=5000,
                                   step=500, key="dcf_mc_n")
        with mc2:
            mc_wacc_std = st.number_input(T("mc_wacc_std"), 0.1, 5.0, value=1.0,
                                          step=0.1, format="%.1f", key="dcf_mc_wacc_std")
        with mc3:
            mc_g_std = st.number_input(T("mc_growth_std"), 0.1, 5.0, value=1.0,
                                       step=0.1, format="%.1f", key="dcf_mc_g_std")
        with mc4:
            mc_m_std = st.number_input(T("mc_margin_std"), 0.1, 10.0, value=2.0,
                                       step=0.5, format="%.1f", key="dcf_mc_m_std")

        if st.button(T("mc_run"), key="dcf_mc_run", type="primary"):
            mc_n = int(mc_n)
            base_wacc_pct = wacc * 100
            base_g = st.session_state["dcf_perp_growth"]

            np.random.seed(42)
            wacc_samples = np.random.normal(base_wacc_pct, mc_wacc_std, mc_n) / 100
            g_samples = np.random.normal(base_g, mc_g_std, mc_n) / 100
            margin_samples = np.random.normal(0, mc_m_std, mc_n)

            wacc_samples = np.clip(wacc_samples, 0.02, 0.30)
            g_samples = np.clip(g_samples, 0.0, 0.10)

            mc_prices = np.zeros(mc_n)
            progress = st.progress(0)
            for idx in range(mc_n):
                try:
                    if is_gordon_sens:
                        r_mc = _run_dcf(wacc_override=wacc_samples[idx],
                                        g_override=g_samples[idx],
                                        margin_adj=margin_samples[idx] / 100)
                    else:
                        r_mc = _run_dcf(wacc_override=wacc_samples[idx],
                                        margin_adj=margin_samples[idx] / 100)
                    mc_prices[idx] = r_mc["price"]
                except Exception:
                    mc_prices[idx] = 0
                if idx % max(1, mc_n // 20) == 0:
                    progress.progress(min(idx / mc_n, 1.0))
            progress.progress(1.0)

            # Filter out extreme outliers (cap at 5x current price)
            cap = st.session_state["dcf_share_price"] * 5
            mc_prices = np.clip(mc_prices, 0, cap)

            # Results
            st.markdown("---")
            r1, r2, r3, r4, r5 = st.columns(5)
            r1.markdown(_mc(T("mc_mean"), f"{np.mean(mc_prices):.2f}"), unsafe_allow_html=True)
            r2.markdown(_mc(T("mc_median"), f"{np.median(mc_prices):.2f}"), unsafe_allow_html=True)
            r3.markdown(_mc(T("mc_p10"), f"{np.percentile(mc_prices, 10):.2f}"), unsafe_allow_html=True)
            r4.markdown(_mc(T("mc_p90"), f"{np.percentile(mc_prices, 90):.2f}"), unsafe_allow_html=True)
            r5.markdown(_mc(T("mc_std"), f"{np.std(mc_prices):.2f}"), unsafe_allow_html=True)

            # Histogram
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=mc_prices, nbinsx=80,
                marker_color="#1a56db", opacity=0.7,
                name=T("implied_price"),
            ))
            fig_mc.add_vline(x=st.session_state["dcf_share_price"],
                             line_dash="dash", line_color="#dc2626", line_width=2,
                             annotation_text=T("current_price_line"),
                             annotation_font_color="#dc2626")
            fig_mc.add_vline(x=np.mean(mc_prices),
                             line_dash="dot", line_color="#16a34a", line_width=2,
                             annotation_text=T("mc_mean"),
                             annotation_font_color="#16a34a")
            fig_mc.update_layout(
                title=T("monte_carlo_title"),
                xaxis_title=T("implied_price"),
                yaxis_title="Frequency" if lang == "EN" else "Frequencia",
                height=400, margin=dict(t=50, b=40),
                showlegend=False,
            )
            st.plotly_chart(fig_mc, use_container_width=True)

            # Probability of upside
            prob_upside = np.mean(mc_prices > st.session_state["dcf_share_price"]) * 100
            st.markdown(
                f"**{'Probability of upside' if lang == 'EN' else 'Probabilidade de upside'}:"
                f" {prob_upside:.1f}%**"
            )

    # ── Sub-tab 4: Scenario Analysis ──
    with sens_tab4:
        st.subheader(T("scenario_title"))

        sc1, sc2, sc3 = st.columns(3)

        with sc1:
            st.markdown(f"### {T('bull_case')}")
            st.number_input(T("probability"), 0.0, 100.0, step=5.0,
                            format="%.0f", key="dcf_bull_prob")
            st.number_input(T("rev_growth_adj"), -20.0, 20.0, step=0.5,
                            format="%.1f", key="dcf_bull_rev_adj")
            st.number_input(T("margin_adj"), -20.0, 20.0, step=0.5,
                            format="%.1f", key="dcf_bull_margin_adj")
            st.number_input(T("wacc_adj"), -5.0, 5.0, step=0.1,
                            format="%.1f", key="dcf_bull_wacc_adj")

        with sc2:
            st.markdown(f"### {T('base_case')}")
            base_prob = 100.0 - st.session_state["dcf_bull_prob"] - st.session_state["dcf_bear_prob"]
            base_prob = max(base_prob, 0.0)
            st.markdown(f"**{T('probability')}: {base_prob:.0f}%**")
            st.markdown(f"*{T('rev_growth_adj')}: 0.0*")
            st.markdown(f"*{T('margin_adj')}: 0.0*")
            st.markdown(f"*{T('wacc_adj')}: 0.0*")

        with sc3:
            st.markdown(f"### {T('bear_case')}")
            st.number_input(T("probability"), 0.0, 100.0, step=5.0,
                            format="%.0f", key="dcf_bear_prob")
            st.number_input(T("rev_growth_adj"), -20.0, 20.0, step=0.5,
                            format="%.1f", key="dcf_bear_rev_adj")
            st.number_input(T("margin_adj"), -20.0, 20.0, step=0.5,
                            format="%.1f", key="dcf_bear_margin_adj")
            st.number_input(T("wacc_adj"), -5.0, 5.0, step=0.1,
                            format="%.1f", key="dcf_bear_wacc_adj")

        # Calculate scenarios
        st.markdown("---")

        bull_wacc = wacc + st.session_state["dcf_bull_wacc_adj"] / 100
        bear_wacc = wacc + st.session_state["dcf_bear_wacc_adj"] / 100

        bull_res = _run_dcf(wacc_override=bull_wacc,
                            rev_growth_adj=st.session_state["dcf_bull_rev_adj"],
                            margin_adj=st.session_state["dcf_bull_margin_adj"] / 100)
        base_res_sc = _run_dcf()
        bear_res = _run_dcf(wacc_override=bear_wacc,
                            rev_growth_adj=st.session_state["dcf_bear_rev_adj"],
                            margin_adj=st.session_state["dcf_bear_margin_adj"] / 100)

        bull_p = st.session_state["dcf_bull_prob"] / 100
        bear_p = st.session_state["dcf_bear_prob"] / 100
        base_p = max(1.0 - bull_p - bear_p, 0.0)

        expected_price = (bull_p * bull_res["price"] +
                          base_p * base_res_sc["price"] +
                          bear_p * bear_res["price"])

        # Display results
        sr1, sr2, sr3, sr4 = st.columns(4)
        sr1.markdown(_mc(T("bull_case"),
                         f"{bull_res['price']:.2f} ({bull_p*100:.0f}%)",
                         color="green"), unsafe_allow_html=True)
        sr2.markdown(_mc(T("base_case"),
                         f"{base_res_sc['price']:.2f} ({base_p*100:.0f}%)"),
                     unsafe_allow_html=True)
        sr3.markdown(_mc(T("bear_case"),
                         f"{bear_res['price']:.2f} ({bear_p*100:.0f}%)",
                         color="red"), unsafe_allow_html=True)

        ev_color = "green" if expected_price > st.session_state["dcf_share_price"] else "red"
        sr4.markdown(_mc(T("expected_value"), f"{expected_price:.2f}",
                         color=ev_color), unsafe_allow_html=True)

        # Scenario football field
        fig_sc = go.Figure()
        sc_names = [T("bear_case"), T("base_case"), T("bull_case"), T("expected_value")]
        sc_prices = [bear_res["price"], base_res_sc["price"],
                     bull_res["price"], expected_price]
        sc_colors = ["#dc2626", "#1a56db", "#16a34a", "#f59e0b"]

        for name, price_val, clr in zip(sc_names, sc_prices, sc_colors):
            fig_sc.add_trace(go.Bar(
                y=[name], x=[price_val], orientation="h",
                marker_color=clr, opacity=0.8,
                text=f"{price_val:.2f}", textposition="outside",
                showlegend=False,
            ))

        fig_sc.add_vline(
            x=st.session_state["dcf_share_price"],
            line_dash="dash", line_color="#64748b", line_width=2,
            annotation_text=T("current_price_line"),
            annotation_font_color="#64748b",
        )
        fig_sc.update_layout(
            title=T("scenario_title"),
            xaxis_title=T("implied_price"),
            height=300, margin=dict(l=20, r=20, t=60, b=40),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

        # Expected value formula
        st.latex(
            r"E[V] = " +
            f"{bull_p*100:.0f}\\% \\times {bull_res['price']:.2f} + "
            f"{base_p*100:.0f}\\% \\times {base_res_sc['price']:.2f} + "
            f"{bear_p*100:.0f}\\% \\times {bear_res['price']:.2f} = "
            f"{expected_price:.2f}"
        )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 8 — COMPARABLE COMPANY ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.info(T("comps_info"))

    num_comps = st.slider(T("num_comps"), 3, 8, value=st.session_state.get("dcf_num_comps", 3),
                          key="dcf_num_comps")

    # Input table for comps
    st.subheader(T("comps_title"))
    comp_data = []
    for i in range(1, num_comps + 1):
        with st.expander(f"{'Comparavel' if lang == 'PT' else 'Comparable'} {i}", expanded=(i <= 3)):
            cc1, cc2, cc3, cc4, cc5 = st.columns(5)
            with cc1:
                st.text_input(T("comp_name"), key=f"dcf_comp_{i}_name")
            with cc2:
                st.number_input(T("comp_ev"), min_value=0.0, step=100.0,
                                format="%.0f", key=f"dcf_comp_{i}_ev")
            with cc3:
                st.number_input(T("comp_revenue"), min_value=0.0, step=100.0,
                                format="%.0f", key=f"dcf_comp_{i}_revenue")
            with cc4:
                st.number_input(T("comp_ebitda"), min_value=0.0, step=50.0,
                                format="%.0f", key=f"dcf_comp_{i}_ebitda")
            with cc5:
                st.number_input(T("comp_net_income"), step=50.0,
                                format="%.0f", key=f"dcf_comp_{i}_net_income")
            # Market cap for P/E
            st.number_input(T("comp_mktcap"), min_value=0.0, step=100.0,
                            format="%.0f", key=f"dcf_comp_{i}_mktcap")

    # Gather data
    comp_records = []
    for i in range(1, num_comps + 1):
        name = st.session_state.get(f"dcf_comp_{i}_name", f"Comp {i}")
        ev_c = st.session_state.get(f"dcf_comp_{i}_ev", 0)
        rev_c = st.session_state.get(f"dcf_comp_{i}_revenue", 0)
        ebitda_c = st.session_state.get(f"dcf_comp_{i}_ebitda", 0)
        ni_c = st.session_state.get(f"dcf_comp_{i}_net_income", 0)
        mktcap_c = st.session_state.get(f"dcf_comp_{i}_mktcap", 0)

        ev_rev = ev_c / rev_c if rev_c > 0 else 0
        ev_ebitda_c = ev_c / ebitda_c if ebitda_c > 0 else 0
        pe = mktcap_c / ni_c if ni_c > 0 else 0

        comp_records.append({
            T("comp_name"): name,
            T("comp_ev"): f"{ev_c:,.0f}",
            T("comp_revenue"): f"{rev_c:,.0f}",
            T("comp_ebitda"): f"{ebitda_c:,.0f}",
            T("comp_net_income"): f"{ni_c:,.0f}",
            T("ev_revenue"): f"{ev_rev:.2f}x",
            T("ev_ebitda"): f"{ev_ebitda_c:.1f}x",
            T("pe_ratio"): f"{pe:.1f}x" if pe > 0 else "N/A",
        })

    comp_df = pd.DataFrame(comp_records)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # Calculate summary stats
    ev_revs = []
    ev_ebitdas = []
    pes = []
    for i in range(1, num_comps + 1):
        ev_c = st.session_state.get(f"dcf_comp_{i}_ev", 0)
        rev_c = st.session_state.get(f"dcf_comp_{i}_revenue", 0)
        ebitda_c = st.session_state.get(f"dcf_comp_{i}_ebitda", 0)
        ni_c = st.session_state.get(f"dcf_comp_{i}_net_income", 0)
        mktcap_c = st.session_state.get(f"dcf_comp_{i}_mktcap", 0)
        if rev_c > 0:
            ev_revs.append(ev_c / rev_c)
        if ebitda_c > 0:
            ev_ebitdas.append(ev_c / ebitda_c)
        if ni_c > 0:
            pes.append(mktcap_c / ni_c)

    if ev_revs and ev_ebitdas:
        st.markdown("---")
        st.subheader("Multiples Summary" if lang == "EN" else "Resumo de Multiplos")

        stats_data = {
            "": [T("mean"), T("median"), T("high"), T("low")],
            T("ev_revenue"): [
                f"{np.mean(ev_revs):.2f}x", f"{np.median(ev_revs):.2f}x",
                f"{np.max(ev_revs):.2f}x", f"{np.min(ev_revs):.2f}x",
            ],
            T("ev_ebitda"): [
                f"{np.mean(ev_ebitdas):.1f}x", f"{np.median(ev_ebitdas):.1f}x",
                f"{np.max(ev_ebitdas):.1f}x", f"{np.min(ev_ebitdas):.1f}x",
            ],
        }
        if pes:
            stats_data[T("pe_ratio")] = [
                f"{np.mean(pes):.1f}x", f"{np.median(pes):.1f}x",
                f"{np.max(pes):.1f}x", f"{np.min(pes):.1f}x",
            ]
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

        # Apply comps to target
        st.markdown("---")
        st.subheader(T("comps_valuation"))

        target_rev = st.session_state["dcf_revenue"]
        target_ebitda = target_rev * st.session_state["dcf_ebitda_margin"] / 100
        target_ni = st.session_state["dcf_net_income"]
        target_shares = st.session_state["dcf_shares"]
        target_nd = st.session_state.get("dcf_net_debt", 0)

        # Target metrics display
        tm1, tm2, tm3 = st.columns(3)
        tm1.markdown(_mc(T("revenue"), fmt_mm(target_rev)), unsafe_allow_html=True)
        tm2.markdown(_mc("EBITDA", fmt_mm(target_ebitda)), unsafe_allow_html=True)
        tm3.markdown(_mc(T("net_income") if lang == "EN" else "Lucro Liquido",
                         fmt_mm(target_ni)), unsafe_allow_html=True)

        # Implied valuations
        comps_vals = {}

        # EV/Revenue
        ev_rev_mean = np.mean(ev_revs)
        ev_rev_med = np.median(ev_revs)
        ev_rev_lo = np.min(ev_revs)
        ev_rev_hi = np.max(ev_revs)

        # EV/EBITDA
        ev_eb_mean = np.mean(ev_ebitdas)
        ev_eb_med = np.median(ev_ebitdas)
        ev_eb_lo = np.min(ev_ebitdas)
        ev_eb_hi = np.max(ev_ebitdas)

        def _ev_to_price(ev_val, nd, sh):
            return (ev_val - nd) / sh if sh > 0 else 0

        comps_results = []
        # EV/Revenue
        for label, mult in [(T("mean"), ev_rev_mean), (T("median"), ev_rev_med),
                            (T("low"), ev_rev_lo), (T("high"), ev_rev_hi)]:
            ev_impl = target_rev * mult
            pr = _ev_to_price(ev_impl, target_nd, target_shares)
            comps_results.append({
                "Multiple": T("ev_revenue"),
                "Stat": label,
                "Multiple Value": f"{mult:.2f}x",
                "Implied EV": fmt_mm(ev_impl),
                T("price_per_share"): f"{pr:.2f}",
            })

        # EV/EBITDA
        for label, mult in [(T("mean"), ev_eb_mean), (T("median"), ev_eb_med),
                            (T("low"), ev_eb_lo), (T("high"), ev_eb_hi)]:
            ev_impl = target_ebitda * mult
            pr = _ev_to_price(ev_impl, target_nd, target_shares)
            comps_results.append({
                "Multiple": T("ev_ebitda"),
                "Stat": label,
                "Multiple Value": f"{mult:.1f}x",
                "Implied EV": fmt_mm(ev_impl),
                T("price_per_share"): f"{pr:.2f}",
            })

        # P/E
        if pes:
            pe_mean = np.mean(pes)
            pe_med = np.median(pes)
            pe_lo = np.min(pes)
            pe_hi = np.max(pes)
            for label, mult in [(T("mean"), pe_mean), (T("median"), pe_med),
                                (T("low"), pe_lo), (T("high"), pe_hi)]:
                eq_impl = target_ni * mult
                pr = eq_impl / target_shares if target_shares > 0 else 0
                comps_results.append({
                    "Multiple": T("pe_ratio"),
                    "Stat": label,
                    "Multiple Value": f"{mult:.1f}x",
                    "Implied EV": "N/A",
                    T("price_per_share"): f"{pr:.2f}",
                })

        comps_val_df = pd.DataFrame(comps_results)
        st.dataframe(comps_val_df, use_container_width=True, hide_index=True)

        # ── Combined Football Field: DCF + Comps ──
        st.markdown("---")
        st.subheader(T("comps_football"))

        dcf_res = _run_dcf()
        current_price_comp = st.session_state["dcf_share_price"]

        football_scenarios = []

        # DCF range (use base +/- 15% for simple range)
        dcf_lo = dcf_res["price"] * 0.85
        dcf_hi = dcf_res["price"] * 1.15
        football_scenarios.append(("DCF", dcf_lo, dcf_hi))

        # EV/Revenue range
        evr_lo = _ev_to_price(target_rev * ev_rev_lo, target_nd, target_shares)
        evr_hi = _ev_to_price(target_rev * ev_rev_hi, target_nd, target_shares)
        football_scenarios.append((T("ev_revenue"), min(evr_lo, evr_hi), max(evr_lo, evr_hi)))

        # EV/EBITDA range
        eveb_lo = _ev_to_price(target_ebitda * ev_eb_lo, target_nd, target_shares)
        eveb_hi = _ev_to_price(target_ebitda * ev_eb_hi, target_nd, target_shares)
        football_scenarios.append((T("ev_ebitda"), min(eveb_lo, eveb_hi), max(eveb_lo, eveb_hi)))

        # P/E range
        if pes:
            pe_lo_pr = target_ni * pe_lo / target_shares if target_shares > 0 else 0
            pe_hi_pr = target_ni * pe_hi / target_shares if target_shares > 0 else 0
            football_scenarios.append((T("pe_ratio"), min(pe_lo_pr, pe_hi_pr),
                                       max(pe_lo_pr, pe_hi_pr)))

        fig_cff = go.Figure()
        colors_ff = ["#1a56db", "#16a34a", "#f59e0b", "#8b5cf6", "#dc2626"]

        for idx, (name, lo, hi) in enumerate(football_scenarios):
            fig_cff.add_trace(go.Bar(
                y=[name], x=[hi - lo], base=[lo],
                orientation="h",
                marker_color=colors_ff[idx % len(colors_ff)],
                opacity=0.75,
                text=f"{lo:.1f} - {hi:.1f}",
                textposition="inside",
                textfont=dict(color="white", size=12),
                showlegend=False,
            ))

        fig_cff.add_vline(
            x=current_price_comp,
            line_dash="dash", line_color="#dc2626", line_width=2,
            annotation_text=f"{T('current_price_line')}: {current_price_comp:.2f}",
            annotation_position="top", annotation_font_color="#dc2626",
        )
        fig_cff.update_layout(
            title=T("comps_football"),
            xaxis_title=T("implied_price"),
            height=350, margin=dict(l=20, r=20, t=60, b=40), bargap=0.3,
        )
        st.plotly_chart(fig_cff, use_container_width=True)
    else:
        st.warning("Enter comparable company data above to see multiples analysis."
                   if lang == "EN" else
                   "Preencha os dados das empresas comparaveis acima para ver a analise de multiplos.")

# ─── Sidebar — Key Metrics ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {'Métricas-chave' if lang=='PT' else 'Key Metrics'}")
    st.divider()
    try:
        _sb_res = _run_dcf()
        st.metric("Enterprise Value", fmt_mm(_sb_res["ev"]))
        st.metric("Equity Value", fmt_mm(_sb_res["equity"]))
        st.metric(T("per_share_value"), fmt_mm(_sb_res["price"]))
        st.metric(T("upside"), f"{_sb_res['upside']:+.1f}%".replace(".",","))
        st.metric("WACC", f"{_sb_res['wacc_used']*100:.2f}%".replace(".",","))
    except Exception:
        st.caption("Preencha os inputs." if lang == "PT" else "Fill inputs.")

st.markdown('<div style="text-align:center;padding:24px 0 12px 0;margin-top:40px;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.72rem">Corpet · MVP — Powered by Streamlit + Plotly</div>', unsafe_allow_html=True)
