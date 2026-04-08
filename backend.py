# ─────────────────────────────────────────────────────────────────────────────
# backend.py — Pure calculation and data-fetch functions (no Streamlit)
# ─────────────────────────────────────────────────────────────────────────────
import copy
import datetime
import math
import random
import requests
import pandas as pd
import numpy as np

from constants import MULT, FREQ_OPTS


# ─── Core helpers ────────────────────────────────────────────────────────────

def tm(aa):
    """Annual rate → monthly rate."""
    return (1 + aa / 100) ** (1 / 12) - 1


def idx_custo(ind, custom, ipca, igpm):
    if ind == "IPCA":          return tm(ipca)
    if ind == "IGPM":          return tm(igpm)
    if ind == "Personalizado": return tm(custom)
    return 0.0


def taxa_div_anual(ind, spread, ipca, igpm, cdi, selic, tjlp):
    base = {"CDI": cdi, "IPCA": ipca, "IGPM": igpm,
            "Selic": selic, "TJLP": tjlp, "Pre-fixado": 0.0}.get(ind, 0.0)
    return ((1 + base / 100) * (1 + spread / 100) - 1) * 100


def fv(v, unit):
    s = v / MULT[unit]
    if unit == "R$ MM":
        return f"R$ {s:,.2f}MM"
    return f"R$ {s:,.0f} Mil"


def fp(v):
    return f"{v:.1f}%"


# ─── Operational cash flow ───────────────────────────────────────────────────

def calcular_operacional(receitas, cpvs, opexs, capex_lines, horizonte,
                         taxa_desc, ipca, igpm):
    total_capex = sum(c["valor"] for c in capex_lines) if capex_lines else 0.0
    t_desc = tm(taxa_desc)

    # Residual values
    residuais = {}
    for c in capex_lines:
        if c["tem_residual"] and c["pct_residual"] > 0:
            mes = int(c["vida_util"] * 12)
            if 1 <= mes <= horizonte:
                residuais[mes] = residuais.get(mes, 0.0) + c["valor"] * c["pct_residual"] / 100

    rows, acum, npv_acc = [], -total_capex, -total_capex
    for m in range(horizonte):
        mes = m + 1
        # Revenue per line
        rec_linha = {}
        for r in receitas:
            v = ((r["valor_anual"] / 12)
                 * (1 + tm(r["crescimento"])) ** m
                 * (1 + idx_custo(r["idx"], r["idx_custom"], ipca, igpm)) ** m)
            rec_linha[r["nome"]] = v
        receita = sum(rec_linha.values())

        # COGS
        cpv = 0.0
        for c in cpvs:
            if c["tipo"] == "Percentual de receita":
                cpv += rec_linha.get(c["linha_ref"], 0.0) * c["pct"] / 100
            else:
                cpv += ((c["valor_anual"] / 12)
                        * (1 + tm(c["crescimento"])) ** m
                        * (1 + idx_custo(c["idx"], c["idx_custom"], ipca, igpm)) ** m)

        # OpEx / G&A
        opex_t = ga_t = 0.0
        for o in opexs:
            v = ((o["valor_anual"] / 12)
                 * (1 + tm(o["crescimento"])) ** m
                 * (1 + idx_custo(o["idx"], o["idx_custom"], ipca, igpm)) ** m)
            if o["cat"] == "OpEx":
                opex_t += v
            else:
                ga_t += v

        mb = receita - cpv
        ebit = mb - opex_t - ga_t
        res = residuais.get(mes, 0.0)
        fluxo = ebit + res
        acum += fluxo
        npv_acc += fluxo / (1 + t_desc) ** mes

        rows.append({
            "Mes": mes, "Receita": receita, "CPV": cpv, "Margem Bruta": mb,
            "MB (%)": (mb / receita * 100) if receita else 0,
            "OpEx": opex_t, "G&A": ga_t, "EBIT": ebit,
            "Rec. Residual": res, "FCF": fluxo,
            "Acumulado": acum, "NPV Acumulado": npv_acc,
        })

    df = pd.DataFrame(rows)
    pb = df[df["Acumulado"] >= 0]["Mes"]
    payback = int(pb.iloc[0]) if not pb.empty else None
    roi = (df["FCF"].sum() / total_capex * 100) if total_capex > 0 else 0
    return df, payback, roi, npv_acc, df["MB (%)"].mean(), total_capex


# ─── Depreciation & Amortization ────────────────────────────────────────────

def calcular_da(capex_lines, horizonte):
    s = pd.Series(0.0, index=range(1, horizonte + 1))
    for c in capex_lines:
        vm = int(c["vida_util"] * 12)
        res_pct = c["pct_residual"] / 100 if c["tem_residual"] else 0
        dep_amount = c["valor"] * (1 - res_pct)
        dep_m = dep_amount / vm if vm > 0 else 0
        for m in range(1, min(vm, horizonte) + 1):
            s[m] += dep_m
    return s


# ─── Sensitivity — multi-variable runner ─────────────────────────────────────

def run_sens_case(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                  v1k, v1v, v2k, v2v):
    """Run a sensitivity case with up to 2 variable overrides."""
    return _run_sens_multi(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                           [(v1k, v1v), (v2k, v2v)])


def run_sens_multi(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                   overrides):
    """Run a sensitivity case with N variable overrides.

    overrides: list of (key, value) tuples, e.g.:
        [("rec_var", -20), ("cresc_rec", 15.0), ("cpv_var", 10), ("opex_var", 5)]
    """
    return _run_sens_multi(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                           overrides)


def _run_sens_multi(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                    overrides):
    r  = copy.deepcopy(rec_b)
    c  = copy.deepcopy(cpv_b)
    o  = copy.deepcopy(opex_b)
    ca = copy.deepcopy(cap_b)
    td = td_b
    ip = ip_b

    for key, val in overrides:
        if key == "__noop__":
            continue
        if key == "cresc_rec":
            for x in r: x["crescimento"] = val
        elif key == "taxa_desc_v":
            td = val
        elif key == "ipca_v":
            ip = val
        elif key == "rec_var":
            for x in r: x["valor_anual"] = x["valor_anual"] * (1 + val / 100)
        elif key == "cpv_var":
            for x in c:
                if x["tipo"] == "Valor fixo":
                    x["valor_anual"] = x["valor_anual"] * (1 + val / 100)
                else:
                    x["pct"] = min(x["pct"] * (1 + val / 100), 100)
        elif key == "opex_var":
            for x in o: x["valor_anual"] = x["valor_anual"] * (1 + val / 100)
        elif key == "capex_var":
            for x in ca: x["valor"] = x["valor"] * (1 + val / 100)

    _, pb, roi, npv, mg, _ = calcular_operacional(r, c, o, ca, hor, td, ip, ig)
    return npv, roi, pb, mg


# ─── IRR (Internal Rate of Return) ──────────────────────────────────────────

def calcular_irr(cash_flows):
    """Compute IRR using Newton-Raphson.

    cash_flows: list of monthly cash flows, index 0 = initial investment (negative).
    Returns annualized IRR (%) or None if no convergence.
    """
    if not cash_flows or len(cash_flows) < 2:
        return None

    # Initial guess from simple ROI
    total_in = sum(abs(cf) for cf in cash_flows if cf < 0) or 1
    total_out = sum(cf for cf in cash_flows if cf > 0)
    r = max(min((total_out / total_in - 1) / max(len(cash_flows), 1), 0.5), -0.5)

    for _ in range(200):
        npv = sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows))
        dnpv = sum(-t * cf / (1 + r) ** (t + 1) for t, cf in enumerate(cash_flows))
        if abs(dnpv) < 1e-14:
            break
        r_new = r - npv / dnpv
        if abs(r_new - r) < 1e-9:
            r = r_new
            break
        r = r_new

    # Verify convergence
    npv_check = sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows))
    if abs(npv_check) > abs(cash_flows[0]) * 0.01:
        return None

    # Monthly → Annual
    irr_annual = ((1 + r) ** 12 - 1) * 100
    return irr_annual


def calcular_mirr(cash_flows, finance_rate_aa, reinvest_rate_aa):
    """Compute Modified IRR (MIRR).

    finance_rate_aa: annual rate for financing negative flows (% p.a.)
    reinvest_rate_aa: annual rate for reinvesting positive flows (% p.a.)
    Returns annualized MIRR (%) or None.
    """
    if not cash_flows or len(cash_flows) < 2:
        return None

    n = len(cash_flows) - 1  # periods (months)
    r_fin = tm(finance_rate_aa)
    r_inv = tm(reinvest_rate_aa)

    # PV of negative cash flows at finance rate
    pv_neg = sum(cf / (1 + r_fin) ** t
                 for t, cf in enumerate(cash_flows) if cf < 0)
    if pv_neg == 0:
        return None

    # FV of positive cash flows at reinvestment rate
    fv_pos = sum(cf * (1 + r_inv) ** (n - t)
                 for t, cf in enumerate(cash_flows) if cf > 0)
    if fv_pos <= 0:
        return None

    # MIRR monthly
    mirr_m = (fv_pos / abs(pv_neg)) ** (1 / n) - 1
    # Annual
    return ((1 + mirr_m) ** 12 - 1) * 100


# ─── Profitability Index ─────────────────────────────────────────────────────

def calcular_profitability_index(npv, total_capex):
    """PI = (NPV + Investment) / Investment = 1 + NPV/Investment.
    PI > 1 means value-creating project.
    """
    if total_capex <= 0:
        return None
    return 1 + npv / total_capex


# ─── WACC ────────────────────────────────────────────────────────────────────

def calcular_wacc(total_capex, total_debt, equity_required,
                  cost_of_equity_aa, cost_of_debt_aa, tax_rate_pct):
    """Compute Weighted Average Cost of Capital (WACC).

    cost_of_equity_aa: annual cost of equity (% p.a.) — typically from CAPM or hurdle rate
    cost_of_debt_aa: weighted average annual cost of debt (% p.a.)
    tax_rate_pct: effective tax rate (%)
    Returns WACC (% p.a.)
    """
    total = total_debt + equity_required
    if total <= 0:
        return cost_of_equity_aa  # 100% equity → WACC = Ke

    w_debt = total_debt / total
    w_equity = equity_required / total
    tax_shield = 1 - tax_rate_pct / 100

    return w_equity * cost_of_equity_aa + w_debt * cost_of_debt_aa * tax_shield


def calcular_custo_medio_divida(tranches, macro_rates):
    """Compute weighted-average cost of debt from all tranches."""
    total_val = sum(t["valor"] for t in tranches)
    if total_val <= 0:
        return 0.0
    custo = sum(
        t["valor"] * taxa_div_anual(t["indexador"], t["spread"], **macro_rates)
        for t in tranches
    )
    return custo / total_val


# ─── DSCR (Debt Service Coverage Ratio) ─────────────────────────────────────

def calcular_dscr(df_op, interest_m, principal_m, horizonte):
    """Compute DSCR per month and annual averages.

    DSCR = EBIT / Debt Service (interest + principal).
    Returns pd.Series indexed by month.
    """
    dscr = pd.Series(dtype=float, index=range(1, horizonte + 1))
    df_idx = df_op.set_index("Mes")

    for m in range(1, horizonte + 1):
        ebit = df_idx.loc[m, "EBIT"] if m in df_idx.index else 0.0
        serv = interest_m.get(m, 0.0) + principal_m.get(m, 0.0)
        dscr[m] = ebit / serv if serv > 0 else float('inf')

    return dscr


def calcular_dscr_anual(dscr_mensal, horizonte):
    """Aggregate monthly DSCR into annual averages."""
    n_anos = math.ceil(horizonte / 12)
    result = {}
    for y in range(1, n_anos + 1):
        meses = list(range((y - 1) * 12 + 1, min(y * 12, horizonte) + 1))
        vals = [dscr_mensal[m] for m in meses
                if m in dscr_mensal.index and dscr_mensal[m] != float('inf')]
        result[f"Ano {y}"] = sum(vals) / len(vals) if vals else float('inf')
    return result


# ─── ICR (Interest Coverage Ratio) ──────────────────────────────────────────

def calcular_icr_anual(annual_data):
    """ICR = EBITDA / Interest Expense, per year."""
    result = {}
    for yr, d in annual_data.items():
        juros = d.get("juros", 0)
        ebitda = d.get("ebitda", 0)
        result[yr] = ebitda / juros if juros > 0 else float('inf')
    return result


# ─── Debt/EBITDA ratio ──────────────────────────────────────────────────────

def calcular_divida_ebitda(balanco, annual_data):
    """Debt / EBITDA ratio per year."""
    result = {}
    for yr in annual_data:
        debt = balanco.get(yr, {}).get("Divida Total", 0)
        ebitda = annual_data[yr].get("ebitda", 0)
        result[yr] = debt / ebitda if ebitda > 0 else float('inf')
    return result


# ─── Monte Carlo Simulation ─────────────────────────────────────────────────

def monte_carlo(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig,
                n_sims=1000, seed=42,
                rec_std=15.0, cpv_std=10.0, opex_std=10.0,
                cresc_std=5.0, taxa_desc_std=2.0):
    """Run Monte Carlo simulation on key variables.

    Varies: revenue volume, COGS, OpEx, growth rate, discount rate.
    Each variable is perturbed by a normal distribution with given std (in %).
    Returns dict with arrays of NPV, ROI, Payback, Margin for each simulation.
    """
    rng = random.Random(seed)
    results = {"npv": [], "roi": [], "payback": [], "margem": []}

    base_cresc = sum(x["crescimento"] for x in rec_b) / max(len(rec_b), 1)

    for _ in range(n_sims):
        overrides = []

        # Revenue volume variation (%)
        rv = rng.gauss(0, rec_std)
        overrides.append(("rec_var", rv))

        # COGS variation (%)
        cv = rng.gauss(0, cpv_std)
        overrides.append(("cpv_var", cv))

        # OpEx variation (%)
        ov = rng.gauss(0, opex_std)
        overrides.append(("opex_var", ov))

        # Growth rate (absolute, % a.a.)
        cresc_v = max(base_cresc + rng.gauss(0, cresc_std), 0)
        overrides.append(("cresc_rec", cresc_v))

        # Discount rate (absolute, % a.a.)
        td_v = max(td_b + rng.gauss(0, taxa_desc_std), 0.5)
        overrides.append(("taxa_desc_v", td_v))

        npv, roi, pb, mg = _run_sens_multi(
            rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig, overrides)

        results["npv"].append(npv)
        results["roi"].append(roi)
        results["payback"].append(pb if pb is not None else hor + 1)
        results["margem"].append(mg)

    return results


def monte_carlo_stats(mc_results):
    """Compute summary statistics from Monte Carlo results."""
    stats = {}
    for key, vals in mc_results.items():
        arr = np.array(vals, dtype=float)
        stats[key] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "p5": float(np.percentile(arr, 5)),
            "p25": float(np.percentile(arr, 25)),
            "p75": float(np.percentile(arr, 75)),
            "p95": float(np.percentile(arr, 95)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
        }
    return stats


# ─── Debt schedule ───────────────────────────────────────────────────────────

def gerar_schedule(tranche, macro_rates, horizonte):
    valor = tranche["valor"]
    tenor = tranche["tenor"]
    start = tranche["start_mes"]
    g_amort = tranche["graca_amort"]
    g_juros = tranche["graca_juros"]
    tipo = tranche["tipo_amort"]
    f_a = FREQ_OPTS[tranche["freq_amort"]]
    f_j = FREQ_OPTS[tranche["freq_juros"]]
    taxa_aa = taxa_div_anual(tranche["indexador"], tranche["spread"], **macro_rates)
    taxa_m = tm(taxa_aa)

    # Grace period — capitalize interest
    saldo_sim = valor
    for t in range(g_amort):
        j = saldo_sim * taxa_m
        if t < g_juros:
            saldo_sim += j

    saldo_base = saldo_sim
    n_pay = max(math.ceil((tenor - g_amort) / f_a), 1) if tenor > g_amort else 1
    amort_sac = saldo_base / n_pay
    r_per = (1 + taxa_m) ** f_a - 1
    if tipo == "Price" and r_per > 0:
        pmt_price = saldo_base * r_per * (1 + r_per) ** n_pay / ((1 + r_per) ** n_pay - 1)
    else:
        pmt_price = saldo_base / n_pay if n_pay > 0 else saldo_base

    saldo = valor
    j_acum = 0.0
    rows = []
    for t in range(tenor):
        mes = start + t
        if mes > horizonte:
            break
        s_ini = saldo
        j_mes = saldo * taxa_m
        if t < g_juros:
            saldo += j_mes
            rows.append({
                "Mes": mes, "Saldo Inicial": s_ini, "Juros Pagos": 0.0,
                "Amortizacao": 0.0, "Servico": 0.0, "Saldo Final": saldo,
                "Fase": "Carencia (cap.)"
            })
            continue
        j_acum += j_mes
        pay_j = (t - g_juros + 1) % f_j == 0
        pay_a = (t >= g_amort) and ((t - g_amort + 1) % f_a == 0)
        j_pago = principal = 0.0
        if pay_j:
            j_pago = j_acum
            j_acum = 0.0
        if pay_a:
            if tipo == "Bullet":
                ultima = g_amort + (n_pay - 1) * f_a
                principal = saldo if t >= ultima else 0.0
            elif tipo == "SAC":
                principal = min(amort_sac, saldo)
            elif tipo == "Price":
                jp = saldo * r_per
                principal = max(min(pmt_price - jp, saldo), 0.0)
        saldo = max(saldo - principal, 0.0)
        fase = "Carencia (juros)" if t < g_amort else "Amortizacao"
        rows.append({
            "Mes": mes, "Saldo Inicial": s_ini, "Juros Pagos": j_pago,
            "Amortizacao": principal, "Servico": j_pago + principal,
            "Saldo Final": saldo, "Fase": fase
        })
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ─── Vectorized debt aggregation (replaces iterrows loops) ──────────────────

def agregar_schedules(schedules, horizonte):
    """Aggregate all debt schedules into monthly interest, principal, and balance.

    Returns (interest_m, principal_m, proceeds_m) as pd.Series indexed 1..horizonte.
    Much faster than iterrows-based aggregation.
    """
    interest_m  = pd.Series(0.0, index=range(1, horizonte + 1))
    principal_m = pd.Series(0.0, index=range(1, horizonte + 1))

    for df_t in schedules.values():
        if df_t.empty:
            continue
        # Filter to valid months and aggregate via groupby
        valid = df_t[df_t["Mes"].between(1, horizonte)]
        if valid.empty:
            continue
        grouped = valid.groupby("Mes").agg({"Juros Pagos": "sum", "Amortizacao": "sum"})
        interest_m = interest_m.add(grouped["Juros Pagos"], fill_value=0)
        principal_m = principal_m.add(grouped["Amortizacao"], fill_value=0)

    return interest_m, principal_m


def saldo_total_por_mes(schedules, horizonte):
    """Compute total outstanding balance per month (vectorized)."""
    saldo = pd.Series(0.0, index=range(1, horizonte + 1))
    for df_t in schedules.values():
        if df_t.empty:
            continue
        valid = df_t[df_t["Mes"].between(1, horizonte)].set_index("Mes")
        # Forward-fill balance for months between payments
        bal = valid["Saldo Final"].reindex(range(1, horizonte + 1), method="ffill").fillna(0)
        saldo = saldo.add(bal, fill_value=0)
    return saldo


# ─── Covenant compliance check ──────────────────────────────────────────────

def verificar_covenants(tranches, dscr_anual, icr_anual, divida_ebitda_anual):
    """Check covenant compliance for all tranches.

    Returns list of dicts: {tranche, covenant_type, limit, worst_value, compliant, year}.
    """
    violations = []
    for t in tranches:
        nome = t.get("nome", "?")
        n_cov = t.get("n_cov", 0)
        for j in range(n_cov):
            cov_type = t.get(f"cov_type_{j}", "")
            cov_val = t.get(f"cov_val_{j}", 0)

            if "DSCR" in cov_type:
                for yr, v in dscr_anual.items():
                    violations.append({
                        "tranche": nome, "covenant": cov_type,
                        "limit": cov_val, "value": v,
                        "compliant": v >= cov_val, "year": yr,
                    })
            elif "EBITDA" in cov_type:
                for yr, v in divida_ebitda_anual.items():
                    violations.append({
                        "tranche": nome, "covenant": cov_type,
                        "limit": cov_val, "value": v,
                        "compliant": v <= cov_val, "year": yr,
                    })
            elif "ICR" in cov_type:
                for yr, v in icr_anual.items():
                    violations.append({
                        "tranche": nome, "covenant": cov_type,
                        "limit": cov_val, "value": v,
                        "compliant": v >= cov_val, "year": yr,
                    })
    return violations


# ─── BCB data fetchers (no @st.cache_data — app.py wraps these) ─────────────

def _fetch_last(sid):
    try:
        r = requests.get(
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sid}/dados/ultimos/1?formato=json",
            timeout=8)
        d = r.json()[0]
        return float(d["valor"].replace(",", ".")), d["data"]
    except Exception:
        return None, None


def _fetch_hist(sid, n=36):
    try:
        r = requests.get(
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sid}/dados/ultimos/{n}?formato=json",
            timeout=8)
        df = pd.DataFrame(r.json())
        df["valor"] = pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")
        df["data"] = pd.to_datetime(df["data"], dayfirst=True)
        return df
    except Exception:
        return pd.DataFrame()


def _fetch_focus(indicador):
    """BCB Focus Bulletin — retorna (data_coleta, {ano: mediana}) para o indicador."""
    try:
        d0 = (datetime.date.today() - datetime.timedelta(days=14)).isoformat()
        url = (
            f"https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
            f"ExpectativasMercadoAnuais?$top=50"
            f"&$filter=Indicador eq '{indicador}' and Data ge '{d0}'"
            f"&$orderby=Data desc,DataReferencia asc&$format=json"
            f"&$select=Data,DataReferencia,Mediana"
        )
        rows = requests.get(url, timeout=10).json().get("value", [])
        if not rows:
            return None, {}
        last_date = max(d["Data"] for d in rows)
        return last_date, {
            d["DataReferencia"]: d["Mediana"]
            for d in rows if d["Data"] == last_date and d["Mediana"] is not None
        }
    except Exception:
        return None, {}
