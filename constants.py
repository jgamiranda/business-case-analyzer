# ─────────────────────────────────────────────────────────────────────────────
# constants.py — Constantes de domínio e defaults de sessão
# ─────────────────────────────────────────────────────────────────────────────

BENCHMARKS = {
    "Tecnologia (SaaS)":    {"crescimento_min":5,  "crescimento_max":10, "margem_min":20, "margem_max":40, "payback_min":18, "payback_max":36},
    "Varejo":               {"crescimento_min":1,  "crescimento_max":3,  "margem_min":3,  "margem_max":8,  "payback_min":12, "payback_max":24},
    "Saude":                {"crescimento_min":2,  "crescimento_max":5,  "margem_min":8,  "margem_max":15, "payback_min":24, "payback_max":48},
    "Logistica":            {"crescimento_min":1,  "crescimento_max":3,  "margem_min":5,  "margem_max":12, "payback_min":18, "payback_max":30},
    "Educacao":             {"crescimento_min":2,  "crescimento_max":6,  "margem_min":10, "margem_max":25, "payback_min":12, "payback_max":24},
    "Servicos Financeiros": {"crescimento_min":3,  "crescimento_max":8,  "margem_min":15, "margem_max":30, "payback_min":12, "payback_max":24},
    "Industria":            {"crescimento_min":1,  "crescimento_max":2,  "margem_min":5,  "margem_max":10, "payback_min":24, "payback_max":60},
    "Outro": None,
}

INDEXADORES_CUSTO  = ["Nenhum", "IPCA", "IGPM", "Personalizado"]
INDEXADORES_DIVIDA = ["CDI", "IPCA", "IGPM", "Selic", "TJLP", "Pre-fixado"]
TIPOS_AMORT        = ["SAC", "Price", "Bullet"]
TIPOS_DIVIDA       = ["Emprestimo Bancario","CCB","Debenture","CRI","CRA","BNDES","FINAME","FGTS","Outro"]
FREQ_OPTS          = {"Mensal":1, "Trimestral":3, "Semestral":6, "Anual":12}

SENS_VARS = {
    "Crescimento de receita (% a.a.)":           "cresc_rec",
    "Taxa de desconto (% a.a.)":                 "taxa_desc_v",
    "IPCA (% a.a.)":                             "ipca_v",
    "Volume de receita (+/- % sobre base)":      "rec_var",
    "Custo de produto — CPV (+/- % sobre base)": "cpv_var",
    "Despesas OpEx / G&A (+/- % sobre base)":    "opex_var",
    "Investimento CapEx (+/- % sobre base)":     "capex_var",
}
SENS_VARS_EN = {
    "Revenue growth (% p.a.)":              "cresc_rec",
    "Discount rate (% p.a.)":               "taxa_desc_v",
    "IPCA (% p.a.)":                        "ipca_v",
    "Revenue volume (+/- % vs. base)":      "rec_var",
    "Product cost — COGS (+/- % vs. base)": "cpv_var",
    "OpEx / G&A expenses (+/- % vs. base)": "opex_var",
    "CapEx investment (+/- % vs. base)":    "capex_var",
}
# Keys that use absolute rate values; others use % variation from base
SENS_ABS = {"cresc_rec", "taxa_desc_v", "ipca_v"}

UNIDADES = ["R$ Mil", "R$ MM"]
MULT     = {"R$ Mil": 1_000,    "R$ MM": 1_000_000}
FMT      = {"R$ Mil": "%.0f",   "R$ MM": "%.2f"}
STEP     = {"R$ Mil": 10.0,     "R$ MM": 0.01}
DEF      = {
    "receita": {"R$ Mil": 240.0, "R$ MM": 0.24},
    "capex":   {"R$ Mil": 500.0, "R$ MM": 0.50},
    "cpv":     {"R$ Mil":  60.0, "R$ MM": 0.06},
    "opex":    {"R$ Mil": 120.0, "R$ MM": 0.12},
    "divida":  {"R$ Mil": 300.0, "R$ MM": 0.30},
}

# Session-state defaults (data_inicio resolved at runtime in app.py)
DEFAULTS = {
    "unit": "R$ Mil",
    "n_rec_v": 1, "n_cpv_v": 1, "n_opex_v": 1, "n_capex_v": 1, "n_div_v": 1,
    "horizonte": 36, "taxa_desc": 13.75,
    "ipca_ref": 4.83, "igpm_ref": 3.69, "cdi_ref": 13.65, "tjlp_ref": 6.0,
    "taxa_ir": 34.0, "lang": "PT",
    # Tax regime
    "regime_fiscal": "Lucro Real", "pis_cofins_rate": 9.25, "nol_ativo": True,
    "marg_pres_irpj": 32.0, "marg_pres_csll": 32.0, "simples_aliq": 6.0, "csll_rate": 9.0,
    # Project identity
    "data_inicio": "",   # resolved to today in app.py
    "responsavel": "", "descricao": "",
    # Working capital
    "tem_ncg": False, "ncg_method": "pct", "ncg_pct": 10.0,
    "dso": 30, "dio": 15, "dpo": 30,
}
