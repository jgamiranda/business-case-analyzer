import json

kb_path = r'C:\Users\jgrac\Desktop\business-case-analyzer\boobinho_knowledge_base.json'

with open(kb_path, 'r', encoding='utf-8') as f:
    kb = json.load(f)

# Update metadata
kb['metadata']['version'] = '13.0'
kb['metadata']['last_updated'] = '2026-04-12T18:00:00'
if 'Breaking Into Wall Street (BIWS) — Core Financial Modeling' not in kb['metadata']['sources']:
    kb['metadata']['sources'].append('Breaking Into Wall Street (BIWS) — Core Financial Modeling')
    kb['metadata']['sources'].append('Breaking Into Wall Street (BIWS) — Advanced Financial Modeling')

new_topics = [
    'Revenue Build-Up (Units*Price, Market Share, Growth Rate)',
    '3-Statement Projection Methodology (5-step)',
    'Working Capital Projection (DSO/DIO/DPO drivers)',
    'Circular Reference Resolution (Interest/Cash)',
    'Accretion/Dilution Analysis (5-step)',
    'Merger Model Walkthrough (7-step BIWS)',
    'Purchase Price Allocation (Goodwill + DTL)',
    'Contribution Analysis',
    'Break-even Synergies Formula',
    'Stock vs Asset vs 338(h)(10) Election',
    'NOL Limitations Section 382',
    'Stub Period Modeling',
    'Spinoff/Carveout Models',
    'SOTP Valuation',
    'UFCF Formula (BIWS)',
    'EV to Equity Value Bridge (complete)',
    'Treasury Stock Method (Diluted Shares)',
    'Trading Comps Methodology',
    'Precedent Transactions',
    'Mid-Year Convention',
    'Convertible Bond WACC',
    'Paper LBO Quick Math',
    'Cash Sweep Mechanics (ECF formula)',
    'Covenant Analysis (Maintenance vs Incurrence)',
    'Capital Structure Optimization Hierarchy',
    'Refinancing Mechanics (Call Premium, Make-Whole)',
    'Dividend Recap IRR Impact',
    'Returns to Lenders (OID, PIK IRR)',
    'Convertible Bond Accounting (ASC)',
    'SBC Excess Tax Benefits (ASC 718)',
    'Financial Investments (FVPL/FVOCI/HTM)',
    'Equity Method vs Consolidation',
    'Pension DB Accounting',
    'Quick IRR Math (Rule of 72/115)',
]
for t in new_topics:
    if t not in kb['metadata']['topics_covered']:
        kb['metadata']['topics_covered'].append(t)

# --- CORE FM ---
kb['biws_core_fm'] = {
    "source": "Breaking Into Wall Street - Core Financial Modeling Modules 1-13",
    "business_case": {
        "three_statement_projections": {
            "process": "IS -> BS -> CFS sequencial, circular refs resolvidos por iteracao",
            "step_1_revenue": {
                "methods": [
                    "Simple % growth rate",
                    "Units Sold * Avg Price per Unit (mais defensavel)",
                    "Market Share * Market Size (oligopolistas)"
                ],
                "rule": "Sempre justificar growth rate com drivers operacionais"
            },
            "step_2_cogs_opex": {
                "method": "% de Revenue baseado em tendencia historica",
                "rule": "Margem operacional deve seguir trend logico"
            },
            "step_3_balance_sheet": {
                "current_assets": "AR, Inventory, Prepaid = % of Revenue",
                "current_liabilities": "AP, Accrued Expenses = % of COGS ou OpEx",
                "wc_change_formula": "Change in WC = (Old Liabilities - New Liabilities) + (New Assets - Old Assets)",
                "check": "Change in WC como % de Change in Revenue consistente com historico"
            },
            "step_4_capex_da": {
                "capex": "Schedule separado (capital-intensive) ou % Revenue (tech)",
                "da": "% of CapEx ou PP&E"
            },
            "step_5_cash_debt": {
                "process": "Projetar Cash -> Interest Income. Projetar Debt -> Interest Expense.",
                "circularity": "Resolvida com iteracao no Excel ou solver iterativo em JS"
            },
            "model_checks": [
                "Growth rates convergem para single-digits no longo prazo",
                "BS balanceia (Assets = L + E)",
                "CFS: Beginning Cash + Net Change = Ending Cash"
            ]
        }
    },
    "ma": {
        "accretion_dilution": {
            "step_1": "Get Buyer NI, EPS, Seller NI, EPS (standalone)",
            "step_2": "Purchase Equity Value = Share Price * (1 + Premium%) * Diluted Shares",
            "step_3": "Determine financing mix (Cash/Debt/Stock) + custos",
            "step_4_combined_ni": "Buyer NI + Seller NI - Foregone Interest*(1-t) - New Interest*(1-t) + Seller Cash Interest*(1-t)",
            "step_4_combined_shares": "Buyer Shares + New Shares Issued",
            "step_5_formula": "EPS Accretion = (Combined EPS - Buyer Standalone EPS) / Buyer EPS",
            "quick_rules": {
                "100pct_stock": "Buyer P/E > Seller Purchase P/E -> Accretive",
                "any_mix": "Weighted Cost < Seller Yield -> Accretive"
            },
            "cost_of_source": {
                "cash": "Risk-Free Rate * (1-t)",
                "debt": "Coupon Rate * (1-t)",
                "stock": "Buyer NI / Buyer Equity Value"
            }
        },
        "ppa": {
            "goodwill_formula": "Purchase Eq Value - Seller CSE - Write-Ups + New DTL(Write-Ups*t) + DTA Write-Down - DTL Write-Down",
            "dtl_reason": "D&A dos write-ups dedutivel para book mas NAO para cash taxes"
        },
        "sources_uses": {
            "sources": "Cash + New Debt + Stock Issued + Seller Debt Refinanced",
            "uses": "Purchase Equity Value + Fees + Seller Debt Refinanced"
        },
        "synergies": {
            "types": ["Revenue (cross-selling)", "Expense (headcount, buildings)"],
            "mi_costs": "M&I Costs como % das synergies realizadas",
            "errors": ["Esquecer M&I costs", "Ignorar COGS de revenue synergies"]
        },
        "contribution_analysis": "X% de Revenue/EBITDA/NI -> ownership split",
        "break_even_synergies": "(Lost Cash Earnings + New Interest - Target NI) / (1-t) / Acquirer Shares"
    },
    "valuation_dcf": {
        "ufcf": {
            "formula": "EBIT*(1-t) + D&A +/- Delta WC - CapEx",
            "exclude": ["SBC", "Net Interest", "Other Income", "Non-recurring"],
            "include_lease": "Deduzir full Lease Expense"
        },
        "wacc": {
            "formula": "Ke*%E + Kd*(1-t)*%D + Kp*%P",
            "ke_capm": "Rf + ERP * Levered Beta",
            "erp": "4-6% developed, mais em emerging",
            "kd": "YTM ou average interest rate"
        },
        "beta": {
            "unlever": "Levered Beta / (1 + D/E*(1-t) + Pref/E)",
            "relever": "Unlevered Beta * (1 + D/E*(1-t) + Pref/E)",
            "rule": "Median unlevered de comps, re-lever com target capital structure"
        },
        "terminal_value": {
            "gordon": "UFCF_n*(1+g) / (WACC-g). g < GDP growth",
            "exit_multiple": "EBITDA_n * Multiple",
            "cross_check_multiple": "TV / Terminal EBITDA",
            "cross_check_g": "(TV*WACC - UFCF) / (TV + UFCF)"
        },
        "ev_equity_bridge": {
            "add": ["Cash", "Financial Investments", "Equity Investments", "NOLs (tax-effected)"],
            "subtract": ["Debt (FMV)", "Preferred", "Capital Leases", "NCI", "Unfunded Pensions*(1-t)", "Op Leases (maybe)"],
            "share_price": "Equity Value / Diluted Shares",
            "anti_double_count": "Deduziu expense no UFCF -> NAO subtrair liability no bridge"
        },
        "ev_top_down": "Equity Value - Cash + Debt + Preferred + NCI",
        "tsm": "New Shares = Options - (Options * Exercise Price / Current Price)",
        "multiples": {
            "tev_revenue": "EV / Revenue",
            "tev_ebitda": "EV / (EBIT + D&A + Non-Recurring)",
            "pe": "Equity Value / NI to Common",
            "trading_comps": "Current EV / NTM EBITDA, 5-10 comps",
            "precedent_transactions": "EV pago / LTM EBITDA, inclui 20-40% control premium"
        }
    },
    "lbo": {
        "purchase_price": "EBITDA * Entry Multiple. Cash-free, debt-free.",
        "sources_uses": {
            "sources": "Senior + Sub + Mezz + Equity (plug) + Min Cash",
            "uses": "Purchase EV + Transaction Fees + Financing Fees",
            "equity_plug": "Uses - Debt = Equity",
            "no_stock": "Stock NAO e source em LBOs"
        },
        "debt_schedule": {
            "fcf": "NI + D&A +/- Delta WC - CapEx",
            "cash_available": "FCF + Beg Cash - Min Cash",
            "order": "Revolver -> Term Loans (mandatory) -> Sweeps"
        },
        "returns": {
            "exit_ev": "Exit EBITDA * Exit Multiple",
            "exit_equity": "Exit EV - Net Debt",
            "mom": "Exit Equity / Investor Equity",
            "irr": "(MoM)^(1/n) - 1",
            "rule_72": "2x anos = 72/IRR%",
            "rule_115": "3x anos = 115/IRR%"
        },
        "quick_irr": {"2x_3yr": "~25%", "2x_5yr": "~15%", "3x_3yr": "~45%", "3x_5yr": "~25%"},
        "attribution": {
            "ebitda_growth": "(Exit-Entry EBITDA) * Purchase Multiple",
            "multiple_expansion": "(Exit-Purchase Multiple) * Exit EBITDA",
            "debt_paydown": "Total Return - EBITDA Growth - Multiple Expansion"
        },
        "pe_targets_5yr": {"downside": "1.5x", "base": "2.0x/15%IRR", "upside": "3.0x/25%IRR"},
        "credit_metrics": {
            "leverage": "Debt/EBITDA max ~5x",
            "interest_coverage": "EBITDA/Interest min 2.0x",
            "dscr": "(FCF+Interest+Leases)/Fixed Charges",
            "fccr": "(EBITDA-CapEx-Taxes-Divs)/Fixed Charges",
            "debt_capital": "<50%"
        },
        "ideal_candidate": "Stable CF, low CapEx, asset-rich, mature, reasonable price, clear exit"
    }
}

# --- ADVANCED FM ---
kb['biws_advanced_fm'] = {
    "source": "Breaking Into Wall Street - Advanced Financial Modeling",
    "business_case_advanced": {
        "convertible_bonds": {
            "debt_component": "PV cash flows at equivalent non-convertible rate",
            "equity_component": "Face Value - Debt Component",
            "amortization": "(Beg BV + Beg Fee) * Equiv Rate - Cash Interest",
            "conversion": "IF(Year=Conv Year, -MIN(Beg FV, Initial FV), 0)"
        },
        "sbc_asc718": {
            "excess_tax_benefit": "(FV - Grant Value) * Tax Rate",
            "us_gaap_post2017": "Excess Tax Benefit direto no IS",
            "ifrs": "DTA reavaliado anualmente, Tax Surplus em OCI"
        },
        "financial_investments": {
            "fvpl": "Unrealized G/L no IS + DTA/DTL",
            "fvoci": "G/L em AOCI, sem IS",
            "htm": "Sem G/L (so bonds)",
            "post_asu_2016": "Equity = so FVPL; bonds = qualquer"
        },
        "equity_method_vs_consolidation": {
            "below_50": "Equity Method: Investment no BS, earnings reversed CFS, so dividends = cash",
            "above_50": "Consolidation 100% + NCI",
            "partial_sale": "(MktCap * Prev% - Cost) * (-DeltaPct / Prev%)"
        },
        "pension_db": {
            "asset": "Return + Employer + Participant - Benefits",
            "pbo": "Service Cost + Interest + Participant - Benefits +/- Actuarial",
            "interest_cost": "PBO * Discount Rate"
        }
    },
    "ma_advanced": {
        "deal_structures": {
            "stock_purchase": {"goodwill_amort_tax": False, "writeup_deductible": False},
            "asset_purchase": {"goodwill_amort_tax": "15y", "writeup_deductible": True},
            "s338h10": {
                "goodwill_amort_tax": "15y", "writeup_deductible": True,
                "form": "Stock (legal) / Asset (tax)",
                "reqs": "Buyer C-corp, Seller US, >=80% in 12mo"
            }
        },
        "nol_s382": {
            "annual_limit": "Equity Purchase Price * MAX(3mo Adj LT Rates)",
            "writedown": "MAX(0, NOL - Limit * Years)",
            "dta_writedown": "MAX(0, DTA - Limit * TaxRate * Years)",
            "asset_338": "100% write-down",
            "stock": "Limited annual use"
        },
        "stub_periods": {
            "is_cfs": "Full-year * fraction",
            "bs": "Rollforward from prior +/- CFS stub",
            "wc": "Old + (FY diff * fraction)",
            "quarterly": "YoY growth (not QoQ)"
        },
        "spinoffs": {
            "distribution_ratio": "SpunOff shares per Parent share",
            "bs": "Reallocate assets/liabilities, excess cash -> Parent",
            "is": "Remove SpunOff items, recalc taxes standalone",
            "dis_synergies": "Added costs of separate ops (IT, HR, overhead)",
            "beta": "Re-levered from Public Comps",
            "sotp": "Parent EV + SpunOff EV - Capitalized Overhead",
            "shares": "Parent * (1 + Distribution Ratio)"
        }
    },
    "valuation_dcf_advanced": {
        "mid_year_convention": {
            "factor": "1/(1+WACC)^(t-0.5)",
            "tv_pct_flag": "Flag se TV > 85% do EV"
        },
        "sotp": {
            "method": "Each entity via Comps + DCF",
            "range": "25th-75th percentile",
            "overhead": "Annual * Median EBITDA Multiple",
            "total": "Sum EVs - overhead, divide by post-dist shares"
        },
        "convertible_wacc": {
            "debt_cost": "Equiv Non-Conv Coupon * (1-t)",
            "option_cost": "Rf + ERP * Option Beta",
            "option_beta": "Elasticity * Levered Beta",
            "elasticity": "Delta * (Conv Value / Market Price)",
            "delta": "N(d1) Black-Scholes",
            "convergence": "Stock up -> Blended Cost -> Cost of Equity"
        },
        "duration": {
            "formula": "Sum(PV(CF)*t) / Price",
            "ytm_approx": "(Interest + (Redemption-Price)/Yrs) / ((Redemption+Price)/2)"
        },
        "sensitivity": {"axes": "WACC x Terminal Growth", "range": "WACC+/-1%, g+/-0.5%"}
    },
    "lbo_advanced_biws": {
        "covenants": {
            "maintenance": "Rigid limits, quarterly. Violation = penalty/rate increase/repayment",
            "incurrence": "Action-triggered only, no monitoring",
            "cushion": "% EBITDA decline before breach"
        },
        "cap_structure_hierarchy": [
            "Revolver", "TLA", "TLB", "Sr Unsecured Notes",
            "Sub Notes", "Mezz/Preferred", "Equity"
        ],
        "refinancing": {
            "call_premiums": "105->104->100",
            "make_whole": "PV lost CFs at T+50bps",
            "penalty_vs_rates": "Inversely proportional",
            "ytw": "MIN(YTM, YTC each date)",
            "rule": "Coupon savings must exceed premium + costs"
        },
        "dividend_recap": {
            "timing": "Year 3-4",
            "irr_impact": "Small: fraction of investment, more debt reduces exit eq",
            "irr_vs_moic": "IRR impact > MOIC impact (time value)"
        },
        "cash_sweep": {
            "ecf": "EBITDA - Interest - Taxes - CapEx - Delta NWC - Mandatory Amort",
            "amount": "ECF * Sweep% (50-75%)",
            "step_down": ">4x=75%, <3x=25%"
        },
        "lender_returns": {
            "components": ["OID", "Fees", "Cash interest", "Principal", "Prepayment penalties"],
            "pik_impact": "Worse IRR vs cash (no intermediate CF)",
            "small_deals": "One-time items weigh more on IRR"
        },
        "debt_capacity": {
            "senior": "4-6x EBITDA",
            "total": "5-7x EBITDA",
            "fcc": ">1.0x",
            "interest_coverage": ">2.0x"
        }
    }
}

with open(kb_path, 'w', encoding='utf-8') as f:
    json.dump(kb, f, indent=2, ensure_ascii=False)

print(f"Version: {kb['metadata']['version']}")
print(f"Topics: {len(kb['metadata']['topics_covered'])}")
print(f"Top-level keys: {list(kb.keys())}")
