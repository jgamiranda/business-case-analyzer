# ─────────────────────────────────────────────────────────────────────────────
# backend.py — Pure calculation and data-fetch functions (no Streamlit)
# ─────────────────────────────────────────────────────────────────────────────
import copy
import datetime
import math
import requests
import pandas as pd

from constants import MULT, FREQ_OPTS


def tm(aa): return (1 + aa/100)**(1/12) - 1

def idx_custo(ind, custom, ipca, igpm):
    if ind=="IPCA": return tm(ipca)
    if ind=="IGPM": return tm(igpm)
    if ind=="Personalizado": return tm(custom)
    return 0.0

def taxa_div_anual(ind, spread, ipca, igpm, cdi, selic, tjlp):
    base = {"CDI":cdi,"IPCA":ipca,"IGPM":igpm,"Selic":selic,"TJLP":tjlp,"Pre-fixado":0.0}.get(ind,0.0)
    return ((1 + base/100) * (1 + spread/100) - 1) * 100

def fv(v, unit):
    s = v / MULT[unit]
    if unit=="R$ MM": return f"R$ {s:,.2f}MM"
    return f"R$ {s:,.0f} Mil"

def fp(v): return f"{v:.1f}%"

def calcular_operacional(receitas, cpvs, opexs, capex_lines, horizonte, taxa_desc, ipca, igpm):
    total_capex = sum(c["valor"] for c in capex_lines) if capex_lines else 0.0
    t_desc = tm(taxa_desc)
    residuais = {}
    for c in capex_lines:
        if c["tem_residual"] and c["pct_residual"]>0:
            mes = int(c["vida_util"]*12)
            if 1<=mes<=horizonte:
                residuais[mes] = residuais.get(mes,0.0) + c["valor"]*c["pct_residual"]/100
    rows, acum, npv_acc = [], -total_capex, -total_capex
    for m in range(horizonte):
        mes = m+1
        rec_linha = {}
        for r in receitas:
            v = (r["valor_anual"]/12)*(1+tm(r["crescimento"]))**m*(1+idx_custo(r["idx"],r["idx_custom"],ipca,igpm))**m
            rec_linha[r["nome"]] = v
        receita = sum(rec_linha.values())
        cpv = 0.0
        for c in cpvs:
            if c["tipo"]=="Percentual de receita": cpv += rec_linha.get(c["linha_ref"],0.0)*c["pct"]/100
            else: cpv += (c["valor_anual"]/12)*(1+tm(c["crescimento"]))**m*(1+idx_custo(c["idx"],c["idx_custom"],ipca,igpm))**m
        opex_t=ga_t=0.0
        for o in opexs:
            v=(o["valor_anual"]/12)*(1+tm(o["crescimento"]))**m*(1+idx_custo(o["idx"],o["idx_custom"],ipca,igpm))**m
            if o["cat"]=="OpEx": opex_t+=v
            else: ga_t+=v
        mb=receita-cpv; ebit=mb-opex_t-ga_t; res=residuais.get(mes,0.0); fluxo=ebit+res
        acum+=fluxo; npv_acc+=fluxo/(1+t_desc)**mes
        rows.append({"Mes":mes,"Receita":receita,"CPV":cpv,"Margem Bruta":mb,
                     "MB (%)": (mb/receita*100) if receita else 0,
                     "OpEx":opex_t,"G&A":ga_t,"EBIT":ebit,"Rec. Residual":res,
                     "FCF":fluxo,"Acumulado":acum,"NPV Acumulado":npv_acc})
    df = pd.DataFrame(rows)
    pb = df[df["Acumulado"]>=0]["Mes"]
    payback = int(pb.iloc[0]) if not pb.empty else None
    roi = (df["FCF"].sum()/total_capex*100) if total_capex>0 else 0
    return df, payback, roi, npv_acc, df["MB (%)"].mean(), total_capex

def calcular_da(capex_lines, horizonte):
    s = pd.Series(0.0, index=range(1, horizonte+1))
    for c in capex_lines:
        vm = int(c["vida_util"]*12)
        res_pct = c["pct_residual"]/100 if c["tem_residual"] else 0
        dep_amount = c["valor"]*(1-res_pct)
        dep_m = dep_amount/vm if vm>0 else 0
        for m in range(1, min(vm, horizonte)+1):
            s[m] += dep_m
    return s

def run_sens_case(rec_b, cpv_b, opex_b, cap_b, hor, td_b, ip_b, ig, v1k, v1v, v2k, v2v):
    r  = copy.deepcopy(rec_b)
    c  = copy.deepcopy(cpv_b)
    o  = copy.deepcopy(opex_b)
    ca = copy.deepcopy(cap_b)
    td = td_b
    ip = ip_b
    for key, val in [(v1k, v1v), (v2k, v2v)]:
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

def gerar_schedule(tranche, macro_rates, horizonte):
    valor=tranche["valor"]; tenor=tranche["tenor"]; start=tranche["start_mes"]
    g_amort=tranche["graca_amort"]; g_juros=tranche["graca_juros"]
    tipo=tranche["tipo_amort"]; f_a=FREQ_OPTS[tranche["freq_amort"]]; f_j=FREQ_OPTS[tranche["freq_juros"]]
    taxa_aa = taxa_div_anual(tranche["indexador"], tranche["spread"], **macro_rates)
    taxa_m  = tm(taxa_aa)
    saldo_sim=valor
    for t in range(g_amort):
        j=saldo_sim*taxa_m
        if t<g_juros: saldo_sim+=j
    saldo_base=saldo_sim
    n_pay = max(math.ceil((tenor-g_amort)/f_a),1) if tenor>g_amort else 1
    amort_sac = saldo_base/n_pay
    r_per = (1+taxa_m)**f_a-1
    pmt_price = (saldo_base*r_per*(1+r_per)**n_pay/((1+r_per)**n_pay-1)) if (tipo=="Price" and r_per>0) else (saldo_base/n_pay if n_pay>0 else saldo_base)
    saldo=valor; j_acum=0.0; rows=[]
    for t in range(tenor):
        mes=start+t
        if mes>horizonte: break
        s_ini=saldo; j_mes=saldo*taxa_m
        if t<g_juros:
            saldo+=j_mes
            rows.append({"Mes":mes,"Saldo Inicial":s_ini,"Juros Pagos":0.0,"Amortizacao":0.0,"Servico":0.0,"Saldo Final":saldo,"Fase":"Carencia (cap.)"})
            continue
        j_acum+=j_mes
        pay_j=(t-g_juros+1)%f_j==0
        pay_a=(t>=g_amort) and ((t-g_amort+1)%f_a==0)
        j_pago=principal=0.0
        if pay_j: j_pago=j_acum; j_acum=0.0
        if pay_a:
            if tipo=="Bullet":
                ultima=g_amort+(n_pay-1)*f_a
                principal=saldo if t>=ultima else 0.0
            elif tipo=="SAC": principal=min(amort_sac,saldo)
            elif tipo=="Price":
                jp=saldo*r_per; principal=max(min(pmt_price-jp,saldo),0.0)
        saldo=max(saldo-principal,0.0)
        fase="Carencia (juros)" if t<g_amort else "Amortizacao"
        rows.append({"Mes":mes,"Saldo Inicial":s_ini,"Juros Pagos":j_pago,"Amortizacao":principal,
                     "Servico":j_pago+principal,"Saldo Final":saldo,"Fase":fase})
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ─── BCB data fetchers (no @st.cache_data — app.py wraps these) ──────────────

def _fetch_last(sid):
    try:
        r=requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sid}/dados/ultimos/1?formato=json",timeout=8)
        d=r.json()[0]; return float(d["valor"].replace(",",".")), d["data"]
    except: return None,None

def _fetch_hist(sid,n=36):
    try:
        r=requests.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sid}/dados/ultimos/{n}?formato=json",timeout=8)
        df=pd.DataFrame(r.json())
        df["valor"]=pd.to_numeric(df["valor"].str.replace(",","."),errors="coerce")
        df["data"]=pd.to_datetime(df["data"],dayfirst=True)
        return df
    except: return pd.DataFrame()

def _fetch_focus(indicador):
    """BCB Focus Bulletin — retorna (data_coleta, {ano: mediana}) para o indicador."""
    try:
        d0 = (datetime.date.today() - datetime.timedelta(days=14)).isoformat()
        url = (f"https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
               f"ExpectativasMercadoAnuais?$top=50"
               f"&$filter=Indicador eq '{indicador}' and Data ge '{d0}'"
               f"&$orderby=Data desc,DataReferencia asc&$format=json"
               f"&$select=Data,DataReferencia,Mediana")
        rows = requests.get(url, timeout=10).json().get("value", [])
        if not rows: return None, {}
        last_date = max(d["Data"] for d in rows)
        return last_date, {
            d["DataReferencia"]: d["Mediana"]
            for d in rows if d["Data"] == last_date and d["Mediana"] is not None
        }
    except: return None, {}
