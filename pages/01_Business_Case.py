import datetime
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from constants import (BENCHMARKS, INDEXADORES_CUSTO, INDEXADORES_DIVIDA, TIPOS_AMORT,
                       TIPOS_DIVIDA, FREQ_OPTS, SENS_VARS, SENS_VARS_EN, SENS_ABS,
                       UNIDADES, MULT, FMT, STEP, DEF, DEFAULTS, MODEL_TYPES)
from translations import _OPT_TR_EN, _DF_ROW_EN, _DF_ROW_EN_INV, _METRIC_EN, _ROW_CSS, _L
from backend import (tm, idx_custo, taxa_div_anual, fv, fp, calcular_operacional,
                     calcular_da, run_sens_case, run_sens_multi, gerar_schedule,
                     agregar_schedules, saldo_total_por_mes,
                     calcular_irr, calcular_mirr, calcular_profitability_index,
                     calcular_wacc, calcular_custo_medio_divida,
                     calcular_dscr, calcular_dscr_anual,
                     calcular_icr_anual, calcular_divida_ebitda,
                     verificar_covenants,
                     monte_carlo, monte_carlo_stats,
                     _fetch_last, _fetch_hist, _fetch_focus)
from slides import gerar_deck, SLIDE_TRANSLATIONS

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACAO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Analise de Viabilidade", layout="wide",
                   initial_sidebar_state="expanded")

# Inject global design system (Section 4 of AGENT_BRIEF.md)
import sys, os as _os
_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _root not in sys.path: sys.path.insert(0, _root)
import _design_tokens as ds
ds.inject()

# BCB cache wrappers (decorator applied here so Streamlit is available)
fetch_last  = st.cache_data(ttl=3600, show_spinner=False)(_fetch_last)
fetch_hist  = st.cache_data(ttl=3600, show_spinner=False)(_fetch_hist)
fetch_focus = st.cache_data(ttl=3600, show_spinner=False)(_fetch_focus)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
import datetime as _dt
_today = _dt.date.today().isoformat()
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = _today if k == "data_inicio" else v

def get(k, d=0.0): return st.session_state.get(k, d)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="collapsedControl"]{display:none}
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{gap:5px}
.stTabs [data-baseweb="tab"]{background:#dbeafe;border-radius:6px 6px 0 0;color:#1a56db;font-weight:600;padding:8px 18px;border:1px solid #bfdbfe;border-bottom:none;transition:all .2s ease}
.stTabs [data-baseweb="tab"]:hover{background:#1a56db;color:white;transform:translateY(-1px)}
.stTabs [aria-selected="true"]{background:#1a56db !important;color:white !important;border-color:#1a56db !important}
/* ── Expanders ── */
[data-testid="stExpander"] details summary{background:#1a56db !important;border-radius:6px !important;padding:10px 16px !important;transition:background .2s ease}
[data-testid="stExpander"] details summary:hover{background:#1e429f !important}
[data-testid="stExpander"] details summary p,[data-testid="stExpander"] details summary span{color:white !important;font-weight:600 !important}
[data-testid="stExpander"] details summary svg{fill:white !important;stroke:white !important}
[data-testid="stExpander"] details{border:1px solid #1a56db !important;border-radius:6px !important}
/* ── Verdict boxes ── */
.veredicto-verde{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-left:6px solid #28a745;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(40,167,69,.12)}
.veredicto-amarelo{background:linear-gradient(135deg,#fff3cd 0%,#ffeeba 100%);border-left:6px solid #ffc107;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(255,193,7,.12)}
.veredicto-vermelho{background:linear-gradient(135deg,#f8d7da 0%,#f5c6cb 100%);border-left:6px solid #dc3545;padding:18px 22px;border-radius:10px;box-shadow:0 2px 8px rgba(220,53,69,.12)}
.veredicto-titulo{font-size:1.5rem;font-weight:700;margin-bottom:6px}
/* ── Alert badges ── */
.alerta-ok{color:#155724;background:#d4edda;padding:8px 14px;border-radius:6px;margin:4px 0;display:block;border-left:4px solid #28a745;transition:transform .15s ease}
.alerta-ok:hover{transform:translateX(4px)}
.alerta-warn{color:#856404;background:#fff3cd;padding:8px 14px;border-radius:6px;margin:4px 0;display:block;border-left:4px solid #ffc107;transition:transform .15s ease}
.alerta-warn:hover{transform:translateX(4px)}
.alerta-bad{color:#721c24;background:#f8d7da;padding:8px 14px;border-radius:6px;margin:4px 0;display:block;border-left:4px solid #dc3545;transition:transform .15s ease}
.alerta-bad:hover{transform:translateX(4px)}
/* ── Grid headers ── */
.grid-hdr{display:flex;gap:0;padding:6px 0 4px 0;border-bottom:2px solid #1a56db;margin-bottom:6px}
.grid-hdr span{font-size:.72rem;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.linha-hdr{font-weight:600;color:#374151;font-size:0.82rem;margin:10px 0 2px 0;border-left:3px solid #1a56db;padding-left:8px}
/* ── Macro cards ── */
.macro-card{background:linear-gradient(135deg,#f0f7ff 0%,#e8f0fe 100%);border:1px solid #bfdbfe;border-radius:10px;padding:14px 16px;text-align:center;transition:all .2s ease;box-shadow:0 1px 4px rgba(26,86,219,.06)}
.macro-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(26,86,219,.12)}
.macro-label{font-size:.72rem;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.macro-value{font-size:1.6rem;font-weight:700;color:#1a56db;margin:4px 0}
.macro-date{font-size:.7rem;color:#9ca3af}
/* ── Unit bar ── */
.unit-bar{background:linear-gradient(90deg,#1a56db 0%,#1e429f 100%);border-radius:8px;padding:10px 20px;margin-bottom:6px}
.unit-label{color:white;font-weight:700;font-size:.95rem}
/* ── Metric cards (custom) ── */
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
/* ── Model type cards ── */
.mt-grid{display:flex;gap:12px;flex-wrap:wrap;margin:8px 0 16px 0}
.mt-card{flex:1;min-width:160px;border:2px solid #e5e7eb;border-radius:12px;padding:18px 16px;text-align:center;cursor:pointer;transition:all .25s ease;background:#fff;position:relative}
.mt-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.1)}
.mt-card.mt-active{border-width:3px;box-shadow:0 4px 16px rgba(26,86,219,.18)}
.mt-card .mt-icon{font-size:2.2rem;margin-bottom:6px;display:block}
.mt-card .mt-name{font-size:.9rem;font-weight:700;color:#1f2937;margin-bottom:4px}
.mt-card .mt-desc{font-size:.7rem;color:#6b7280;line-height:1.4}
.mt-card .mt-badge{position:absolute;top:-8px;right:-8px;background:#1a56db;color:white;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.05em}
/* ── DF tables ── */
.df-header{background:#1a56db;color:white;font-weight:700;padding:6px 10px;border-radius:4px;font-size:.85rem;margin:12px 0 4px 0}
.df-subtotal{font-weight:700}
/* ── Sensitivity heatmap table ── */
.sens-tbl{overflow-x:auto;border-radius:8px;margin:4px 0;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.sens-tbl table{width:100%;border-collapse:collapse;font-size:.86rem;font-family:inherit}
.sens-tbl table thead th{background:#1a56db !important;color:#fff !important;padding:9px 16px;font-weight:700;text-align:center;border:1px solid #1e429f !important}
.sens-tbl table thead th:first-child{background:#1e3a8a !important}
.sens-tbl table tbody th{background:#dbeafe !important;color:#1e3a8a !important;font-weight:700;padding:7px 16px;text-align:right;border:1px solid #bfdbfe !important;white-space:nowrap}
.sens-tbl table tbody td{padding:7px 14px;text-align:center;border:1px solid #e5e7eb !important;font-weight:600;font-size:.85rem}
/* ── DF styled tables (DRE / DFC / BP) ── */
.df-styled{overflow-x:auto;border-radius:8px;margin:4px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.df-styled table{width:100%;border-collapse:collapse;font-size:.86rem;font-family:inherit}
.df-styled table thead th{background:#1a56db !important;color:#fff !important;padding:8px 14px;font-weight:700;text-align:right;border:1px solid #1e429f !important}
.df-styled table thead th:first-child{background:#1e3a8a !important;text-align:left}
.df-styled table tbody th{color:#374151;font-weight:500;padding:6px 14px;text-align:left;border:1px solid #e5e7eb !important;white-space:nowrap;background:#fafafa}
.df-styled table tbody td{padding:6px 14px;text-align:right;border:1px solid #e5e7eb !important}
.df-styled table tbody tr:hover td,.df-styled table tbody tr:hover th{background:#f0f7ff !important}
/* ── Sidebar ── */
.sb-metric{background:linear-gradient(135deg,#f0f7ff,#dbeafe);border-radius:8px;padding:10px 12px;margin:4px 0;text-align:center;border:1px solid #bfdbfe}
.sb-metric .sb-val{font-size:1.1rem;font-weight:800;color:#1a56db}
.sb-metric .sb-lbl{font-size:.68rem;color:#6b7280;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
/* ── Footer ── */
.app-footer{text-align:center;padding:20px 0 10px 0;margin-top:40px;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:.75rem}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER + LINGUA + TEMA
# ─────────────────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state: st.session_state["dark_mode"] = False

_hc_title, _hc_lang, _hc_dark = st.columns([6, 1, 1])

with _hc_lang:
    st.write("")
    lang_sel = st.segmented_control("lang", ["PT", "EN"], default="PT", key="lang",
                                    label_visibility="collapsed")
lang = lang_sel or "PT"

with _hc_dark:
    st.write("")
    dark_mode = st.toggle(_L[lang]["dark_mode"], key="dark_mode")

# Translation helpers — available after lang is resolved
def T(k): return _L.get(lang, _L["PT"]).get(k, _L["PT"].get(k, k))
def fmt_opt(x): return _OPT_TR_EN.get(x, x) if lang == "EN" else x

_hc_title.title(T("app_title"))

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
.macro-card{background:#1e293b !important;border-color:#334155 !important}
.macro-label{color:#94a3b8 !important}.macro-date{color:#6b7280 !important}.macro-value{color:#60a5fa !important}
.linha-hdr{color:#93c5fd !important;border-color:#60a5fa !important}
.unit-bar{background:#1e3a8a !important}
hr{border-color:#334155 !important}
.alerta-ok{background:#064e3b !important;color:#6ee7b7 !important}
.alerta-warn{background:#78350f !important;color:#fcd34d !important}
.alerta-bad{background:#7f1d1d !important;color:#fca5a5 !important}
.veredicto-verde{background:#064e3b !important;border-color:#10b981 !important}
.veredicto-amarelo{background:#78350f !important;border-color:#f59e0b !important}
.veredicto-vermelho{background:#7f1d1d !important;border-color:#ef4444 !important}
.veredicto-titulo{color:#f9fafb !important}
.sens-tbl table tbody td{border-color:#334155 !important}
.mt-card{background:#1e293b !important;border-color:#334155 !important}
.mt-card:hover{box-shadow:0 6px 20px rgba(0,0,0,.3) !important}
.mt-card .mt-name{color:#e2e8f0 !important}.mt-card .mt-desc{color:#94a3b8 !important}
.metric-card{background:linear-gradient(135deg,#1e293b,#1e3a5f) !important;border-color:#334155 !important}
.metric-card .mc-label{color:#94a3b8 !important}.metric-card .mc-value{color:#60a5fa !important}
.metric-card-green{background:linear-gradient(135deg,#064e3b,#065f46) !important;border-color:#10b981 !important}
.metric-card-green .mc-value{color:#6ee7b7 !important}
.metric-card-red{background:linear-gradient(135deg,#7f1d1d,#991b1b) !important;border-color:#ef4444 !important}
.metric-card-red .mc-value{color:#fca5a5 !important}
.sb-metric{background:linear-gradient(135deg,#1e293b,#1e3a5f) !important;border-color:#334155 !important}
.sb-metric .sb-val{color:#60a5fa !important}.sb-metric .sb-lbl{color:#94a3b8 !important}
.df-styled table tbody tr:hover td,.df-styled table tbody tr:hover th{background:#1e3a5f !important}
.df-styled table tbody th{background:#1e293b !important;color:#e2e8f0 !important;border-color:#334155 !important}
.df-styled table tbody td{border-color:#334155 !important;color:#e2e8f0 !important}
.app-footer{border-color:#334155 !important;color:#6b7280 !important}
</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MODEL TYPE SELECTOR PANEL
# ─────────────────────────────────────────────────────────────────────────────
if "model_type" not in st.session_state:
    st.session_state["model_type"] = "business_case"

with st.expander(f"\U0001f3af  {T('mt_panel_title')}", expanded=False):
    st.caption(T("mt_panel_cap"))
    _mt_keys = list(MODEL_TYPES.keys())
    _mt_cards_html = '<div class="mt-grid">'
    for mk in _mt_keys:
        mt = MODEL_TYPES[mk]
        is_active = st.session_state.get("model_type") == mk
        active_cls = "mt-active" if is_active else ""
        border_color = mt["color"] if is_active else "#e5e7eb"
        badge = f'<span class="mt-badge" style="background:{mt["color"]}">{T("mt_selected")}</span>' if is_active else ""
        _mt_cards_html += (
            f'<div class="mt-card {active_cls}" style="border-color:{border_color}">'
            f'{badge}'
            f'<span class="mt-icon">{mt["icon"]}</span>'
            f'<div class="mt-name">{T(f"mt_{mk}_name")}</div>'
            f'<div class="mt-desc">{T(f"mt_{mk}_desc")}</div>'
            f'</div>'
        )
    _mt_cards_html += '</div>'
    st.markdown(_mt_cards_html, unsafe_allow_html=True)

    _mt_col1, _mt_col2 = st.columns([3, 2])
    _mt_sel = _mt_col1.selectbox(
        T("mt_panel_title"), _mt_keys,
        format_func=lambda k: f'{MODEL_TYPES[k]["icon"]}  {T(f"mt_{k}_name")}',
        index=_mt_keys.index(st.session_state.get("model_type", "business_case")),
        key="mt_selector", label_visibility="collapsed")
    with _mt_col2:
        if st.button(T("mt_apply"), type="primary", use_container_width=True):
            st.session_state["model_type"] = _mt_sel
            for k, v in MODEL_TYPES[_mt_sel]["defaults"].items():
                st.session_state[k] = v
            st.success(T("mt_applied"))
            st.rerun()

st.markdown(f'<div class="unit-bar"><span class="unit-label">{T("unit_label")}</span></div>', unsafe_allow_html=True)
unit = st.segmented_control("u", UNIDADES, key="unit", label_visibility="collapsed")
if not unit: unit = st.session_state.get("unit","R$ Mil")
ufmt=FMT[unit]; ustep=STEP[unit]; umult=MULT[unit]
st.divider()

_tab_icons = ["\U0001f4cb", "\U0001f4c8", "\U0001f3e6", "\U0001f3af", "\U0001f4ca", "\U0001f50d", "\U0001f4fd"]
_tab_names = [T("tab_premissas"), T("tab_macro"), T("tab_divida"),
              T("tab_resultados"), T("tab_dfs"), T("tab_sens"), T("tab_slides")]
tab_prem,tab_macro,tab_div,tab_res,tab_df,tab_sens,tab_slides = st.tabs(
    [f"{ico}  {nm}" for ico, nm in zip(_tab_icons, _tab_names)]
)

# ─────────────────────────────────────────────────────────────────────────────
# ABA 1 — PREMISSAS
# ─────────────────────────────────────────────────────────────────────────────
with tab_prem:
    with st.expander(T("sec_geral"), expanded=True):
        st.caption(T("cap_geral"))
        _g1, _g2, _g3 = st.columns([2, 1.5, 1.5])
        _g1.text_input(T("nome_proj_lbl"), placeholder=T("nome_proj_ph"), key="nome_proj")
        _g2.selectbox(T("setor_lbl"), list(BENCHMARKS.keys()), format_func=fmt_opt, key="setor")
        _raw_dt = get("data_inicio", _dt.date.today().isoformat())
        _default_dt = _dt.date.fromisoformat(_raw_dt) if isinstance(_raw_dt, str) else _raw_dt
        _picked = _g3.date_input(T("data_inicio_lbl"), value=_default_dt, key="data_inicio_picker",
                                  format="DD/MM/YYYY")
        if _picked: st.session_state["data_inicio"] = _picked.isoformat()

        _g4, _g5 = st.columns([2, 3])
        _g4.text_input(T("responsavel_lbl"), placeholder=T("responsavel_ph"), key="responsavel")
        _g5.text_input(T("descricao_lbl"), placeholder=T("descricao_ph"), key="descricao")

        st.markdown("---")
        _p1, _p2 = st.columns(2)
        _p1.slider(T("horizonte_lbl"), 6, 60, int(get("horizonte", 36)), key="horizonte")
        _p1.caption(f"{int(get('horizonte',36))//12}a {int(get('horizonte',36))%12}m")
        _p2.slider(T("taxa_desc_lbl"), 0.0, 30.0, float(get("taxa_desc", 13.75)), 0.25, key="taxa_desc")

    with st.expander(T("sec_receita"), expanded=True):
        st.caption(T("cap_receita").format(unit=unit))
        n_rec = st.slider(T("n_rec_lbl"),1,8,int(get("n_rec_v",1)),key="n_rec_v")
        _rh=st.columns([2,1.8,1.2,1.2,1.2])
        _rh[0].caption(T("hdr_nome")); _rh[1].caption(T("hdr_valor").format(unit=unit))
        _rh[2].caption(T("hdr_cresc")); _rh[3].caption(T("hdr_idx")); _rh[4].caption(T("hdr_taxa"))
        for i in range(n_rec):
            st.markdown(f'<div class="linha-hdr">{T("rec_prefix")} {i+1}</div>',unsafe_allow_html=True)
            c1,c2,c3,c4,c5=st.columns([2,1.8,1.2,1.2,1.2])
            c1.text_input(T("rec_nome"),key=f"rec_nome_{i}",placeholder=T("rec_nome_ph"),label_visibility="collapsed")
            c2.number_input(T("rec_valor").format(unit=unit),key=f"rec_valor_{i}",min_value=0.0,value=DEF["receita"][unit],step=ustep,format=ufmt,label_visibility="collapsed")
            c3.number_input(T("rec_cresc"),key=f"rec_cresc_{i}",min_value=0.0,max_value=200.0,value=20.0,step=1.0,format="%.0f",label_visibility="collapsed")
            idx=c4.selectbox(T("rec_idx"),INDEXADORES_CUSTO,format_func=fmt_opt,key=f"rec_idx_{i}",label_visibility="collapsed")
            if idx=="Personalizado": c5.number_input(T("taxa_custom"),key=f"rec_idx_custom_{i}",min_value=0.0,max_value=50.0,value=5.0,step=0.5,format="%.1f",label_visibility="collapsed")
            else: c5.empty()

    nomes_receita=[(get(f"rec_nome_{i}","").strip() or f"{T('rec_prefix')} {i+1}") for i in range(int(get("n_rec_v",1)))]

    with st.expander(T("sec_cpv"), expanded=False):
        st.caption(T("cap_cpv"))
        n_cpv=st.slider(T("n_cpv_lbl"),1,8,int(get("n_cpv_v",1)),key="n_cpv_v")
        for i in range(n_cpv):
            st.markdown(f'<div class="linha-hdr">{T("cpv_prefix")} {i+1}</div>',unsafe_allow_html=True)
            c1,c2,resto=st.columns([2,1.8,5])
            c1.text_input(T("cpv_nome"),key=f"cpv_nome_{i}",placeholder=T("cpv_nome_ph"),label_visibility="collapsed")
            tipo=c2.selectbox(T("cpv_tipo"),["Valor fixo","Percentual de receita"],format_func=fmt_opt,key=f"cpv_tipo_{i}",label_visibility="collapsed")
            with resto:
                if tipo=="Valor fixo":
                    cc1,cc2,cc3,cc4=st.columns(4)
                    cc1.number_input(T("cpv_valor").format(unit=unit),key=f"cpv_valor_{i}",min_value=0.0,value=DEF["cpv"][unit],step=ustep,format=ufmt,label_visibility="collapsed")
                    cc2.number_input(T("cpv_cresc"),key=f"cpv_cresc_{i}",min_value=0.0,max_value=100.0,value=5.0,step=1.0,format="%.0f",label_visibility="collapsed")
                    idx_c=cc3.selectbox(T("cpv_idx"),INDEXADORES_CUSTO,format_func=fmt_opt,key=f"cpv_idx_{i}",label_visibility="collapsed")
                    if idx_c=="Personalizado": cc4.number_input(T("taxa_custom"),key=f"cpv_idx_custom_{i}",min_value=0.0,max_value=50.0,value=5.0,step=0.5,format="%.1f",label_visibility="collapsed")
                else:
                    cp1,cp2,_=st.columns([2,1,2])
                    cp1.selectbox(T("cpv_linha_rec"),nomes_receita or ["(sem receitas)"],key=f"cpv_linha_{i}",label_visibility="collapsed")
                    cp2.number_input(T("cpv_pct_rec"),key=f"cpv_pct_{i}",min_value=0.0,max_value=100.0,value=25.0,step=1.0,format="%.0f",label_visibility="collapsed")
                    if get(f"cpv_linha_{i}","") not in nomes_receita: st.warning(T("cpv_warn_linha"))

    with st.expander(T("sec_opex"), expanded=False):
        st.caption(T("cap_opex"))
        n_opex=st.slider(T("n_opex_lbl"),1,8,int(get("n_opex_v",1)),key="n_opex_v")
        _oh=st.columns([2,1.2,1.8,1.2,1.2,1.2])
        _oh[0].caption(T("hdr_nome")); _oh[1].caption(T("hdr_cat")); _oh[2].caption(T("hdr_valor").format(unit=unit))
        _oh[3].caption(T("hdr_cresc")); _oh[4].caption(T("hdr_idx")); _oh[5].caption(T("hdr_taxa"))
        for i in range(n_opex):
            st.markdown(f'<div class="linha-hdr">{T("opex_prefix")} {i+1}</div>',unsafe_allow_html=True)
            c1,c2,c3,c4,c5,c6=st.columns([2,1.2,1.8,1.2,1.2,1.2])
            c1.text_input(T("opex_nome"),key=f"opex_nome_{i}",placeholder=T("opex_nome_ph"),label_visibility="collapsed")
            c2.selectbox(T("opex_cat"),["OpEx","G&A"],key=f"opex_cat_{i}",label_visibility="collapsed")
            c3.number_input(T("opex_valor").format(unit=unit),key=f"opex_valor_{i}",min_value=0.0,value=DEF["opex"][unit],step=ustep,format=ufmt,label_visibility="collapsed")
            c4.number_input(T("opex_cresc"),key=f"opex_cresc_{i}",min_value=0.0,max_value=100.0,value=5.0,step=1.0,format="%.0f",label_visibility="collapsed")
            idx_o=c5.selectbox(T("opex_idx"),INDEXADORES_CUSTO,format_func=fmt_opt,key=f"opex_idx_{i}",label_visibility="collapsed")
            if idx_o=="Personalizado": c6.number_input(T("taxa_custom"),key=f"opex_idx_custom_{i}",min_value=0.0,max_value=50.0,value=5.0,step=0.5,format="%.1f",label_visibility="collapsed")
            else: c6.empty()

    with st.expander(T("sec_capex"), expanded=True):
        st.caption(T("cap_capex"))
        n_capex=st.slider(T("n_capex_lbl"),1,8,int(get("n_capex_v",1)),key="n_capex_v")
        _ch=st.columns([2,1.8,1.4,1.2,1.8])
        _ch[0].caption(T("hdr_nome")); _ch[1].caption(T("hdr_valor").format(unit=unit))
        _ch[2].caption(T("hdr_vida")); _ch[3].caption(T("hdr_residual")); _ch[4].caption(T("hdr_pct_res"))
        for i in range(n_capex):
            st.markdown(f'<div class="linha-hdr">{T("capex_prefix")} {i+1}</div>',unsafe_allow_html=True)
            c1,c2,c3,c4,c5=st.columns([2,1.8,1.4,1.2,1.8])
            c1.text_input(T("capex_nome"),key=f"cap_nome_{i}",placeholder=T("capex_nome_ph"),label_visibility="collapsed")
            c2.number_input(T("capex_valor").format(unit=unit),key=f"cap_valor_{i}",min_value=0.0,value=DEF["capex"][unit],step=ustep,format=ufmt,label_visibility="collapsed")
            c3.slider(T("capex_vida"),1,20,int(get(f"cap_vida_{i}",5)),key=f"cap_vida_{i}")
            tem_res=c4.checkbox(T("capex_tem_res"),key=f"cap_tem_res_{i}",value=False)
            if tem_res: c5.slider(T("capex_pct_res"),0,100,int(get(f"cap_pct_res_{i}",10)),key=f"cap_pct_res_{i}")
            else: c5.empty()

    with st.expander(T("sec_tributos"), expanded=False):
        st.caption(T("cap_tributos"))
        _REGIMES = ["Lucro Real", "Lucro Presumido", "Simples Nacional"]
        _REGIME_EN = {"Lucro Real":"Lucro Real","Lucro Presumido":"Lucro Presumido","Simples Nacional":"Simples Nacional"}
        _tr1, _tr2 = st.columns([2, 3])
        regime_sel = _tr1.selectbox(T("regime_lbl"), _REGIMES, key="regime_fiscal",
                                    index=_REGIMES.index(get("regime_fiscal","Lucro Real")),
                                    format_func=lambda x: _REGIME_EN.get(x, x))
        if regime_sel == "Lucro Real":
            _ta, _tb, _tc = st.columns(3)
            _ta.number_input(T("csll_lbl"), 0.0, 20.0, float(get("csll_rate", 9.0)), 0.5,
                             format="%.1f", key="csll_rate")
            _tb.number_input(T("pis_cofins_lbl"), 0.0, 15.0, float(get("pis_cofins_rate", 9.25)), 0.05,
                             format="%.2f", key="pis_cofins_rate", help=T("pis_cofins_help"))
            _tc.write("")
            _tc.checkbox(T("nol_lbl"), value=bool(get("nol_ativo", True)), key="nol_ativo",
                         help=T("nol_help"))
            st.info(T("tributos_info_lr").format(csll=float(get("csll_rate", 9.0))))
        elif regime_sel == "Lucro Presumido":
            _ta, _tb, _tc = st.columns(3)
            _ta.number_input(T("marg_pres_irpj_lbl"), 1.0, 100.0, float(get("marg_pres_irpj", 32.0)), 1.0,
                             format="%.1f", key="marg_pres_irpj")
            _tb.number_input(T("marg_pres_csll_lbl"), 1.0, 100.0, float(get("marg_pres_csll", 32.0)), 1.0,
                             format="%.1f", key="marg_pres_csll")
            _tc.number_input(T("pis_cofins_lbl"), 0.0, 10.0, float(get("pis_cofins_rate", 3.65)), 0.05,
                             format="%.2f", key="pis_cofins_rate", help=T("pis_cofins_help"))
            st.info(T("tributos_info_lp").format(irpj=float(get("marg_pres_irpj", 32.0)),
                                                  csll=float(get("marg_pres_csll", 32.0))))
        else:  # Simples Nacional
            _ta, _ = st.columns([2, 3])
            _ta.number_input(T("simples_aliq_lbl"), 0.5, 33.0, float(get("simples_aliq", 6.0)), 0.1,
                             format="%.1f", key="simples_aliq", help=T("simples_help"))
            st.info(T("tributos_info_sn").format(aliq=float(get("simples_aliq", 6.0))))

    with st.expander(T("sec_ncg"), expanded=False):
        st.caption(T("cap_ncg"))
        tem_ncg = st.checkbox(T("ncg_tem"), value=bool(get("tem_ncg", False)), key="tem_ncg")
        if tem_ncg:
            ncg_method = st.segmented_control(
                "ncg_method_sel", ["pct", "dias"],
                format_func=lambda x: T(f"ncg_method_{x}"),
                key="ncg_method", default=get("ncg_method", "pct"),
                label_visibility="collapsed")
            ncg_method = ncg_method or "pct"
            st.write("")
            if ncg_method == "pct":
                st.slider(T("ncg_pct_lbl"), 0.0, 50.0,
                          float(get("ncg_pct", 10.0)), 0.5,
                          format="%.1f%%", key="ncg_pct")
            else:
                _nc1, _nc2, _nc3 = st.columns(3)
                _nc1.slider(T("dso_lbl"), 0, 180, int(get("dso", 30)), key="dso")
                _nc2.slider(T("dio_lbl"), 0, 180, int(get("dio", 15)), key="dio")
                _nc3.slider(T("dpo_lbl"), 0, 180, int(get("dpo", 30)), key="dpo")
                _ccc = int(get("dso", 30)) + int(get("dio", 15)) - int(get("dpo", 30))
                st.caption(T("ncg_ccc_preview").format(ccc=_ccc))

        # ── Rolling Working Capital detail (only when dias method) ──────────
        st.markdown("---")
        with st.expander(T("ncg_detail_title"), expanded=False):
            st.caption(T("ncg_detail_cap"))
            if tem_ncg and get("ncg_method", "pct") == "dias":
                st.caption(T("ncg_detail_note"))
                st.info("ℹ  " + T("ncg_row_delta_nwc") +
                        " → " + T("dfc_delta_ncg"))
            else:
                st.info(T("ncg_detail_only_dias"))

    with st.expander(T("sec_revolver"), expanded=False):
        _rv1, _rv2 = st.columns([1, 3])
        _rv1.checkbox(T("rev_use_lbl"), value=bool(get("use_revolver", True)),
                      key="use_revolver", help=T("rev_use_help"))
        _rv2.write("")
        if bool(get("use_revolver", True)):
            _rvc1, _rvc2, _rvc3 = st.columns(3)
            _rvc1.number_input(T("rev_min_cash_lbl"), 0.0, 50.0,
                               float(get("rev_min_cash_pct", 5.0)), 0.5,
                               format="%.1f", key="rev_min_cash_pct")
            _rvc2.number_input(T("rev_rate_lbl"), 0.0, 30.0,
                               float(get("rev_rate_spread", 3.0)), 0.25,
                               format="%.2f", key="rev_rate_spread")
            _rvc3.number_input(T("rev_max_cap_lbl"), 0.0, 200.0,
                               float(get("rev_max_cap_pct", 30.0)), 1.0,
                               format="%.0f", key="rev_max_cap_pct")
            _cdi_cur = float(get("cdi_ref", 13.65))
            _sp_cur  = float(get("rev_rate_spread", 3.0))
            st.info(T("rev_effective_rate").format(cdi=_cdi_cur, sp=_sp_cur,
                                                   tot=_cdi_cur + _sp_cur))
    # ── Comparables (Valuation DCF) ─────────────────────────────────────────
    if st.session_state.get("model_type") == "valuation_dcf":
        with st.expander(T("comp_sec"), expanded=True):
            st.caption(T("comp_cap"))
            n_comp = st.slider(T("comp_n_lbl"), 1, 8, int(get("n_comp_v", 3)), key="n_comp_v")
            _cph = st.columns([2.5, 1.5, 1.5, 1.5, 1.5])
            _cph[0].caption(T("comp_hdr_empresa")); _cph[1].caption(T("comp_hdr_ev"))
            _cph[2].caption(T("comp_hdr_receita")); _cph[3].caption(T("comp_hdr_ebitda"))
            _cph[4].caption(T("comp_hdr_ni"))
            for ci in range(n_comp):
                st.markdown(f'<div class="linha-hdr">Comp {ci+1}</div>', unsafe_allow_html=True)
                cc1, cc2, cc3, cc4, cc5 = st.columns([2.5, 1.5, 1.5, 1.5, 1.5])
                cc1.text_input(T("comp_nome"), key=f"comp_nome_{ci}",
                               placeholder=T("comp_nome_ph"), label_visibility="collapsed")
                cc2.number_input(T("comp_ev").format(unit=unit), key=f"comp_ev_{ci}",
                                 min_value=0.0, value=0.0, step=ustep, format=ufmt,
                                 label_visibility="collapsed")
                cc3.number_input(T("comp_receita").format(unit=unit), key=f"comp_receita_{ci}",
                                 min_value=0.0, value=0.0, step=ustep, format=ufmt,
                                 label_visibility="collapsed")
                cc4.number_input(T("comp_ebitda").format(unit=unit), key=f"comp_ebitda_{ci}",
                                 min_value=0.0, value=0.0, step=ustep, format=ufmt,
                                 label_visibility="collapsed")
                cc5.number_input(T("comp_ni").format(unit=unit), key=f"comp_ni_{ci}",
                                 min_value=0.0, value=0.0, step=ustep, format=ufmt,
                                 label_visibility="collapsed")

    st.info(T("pr_info_done"))

# ─────────────────────────────────────────────────────────────────────────────
# ABA 2 — MACROECONOMIA
# ─────────────────────────────────────────────────────────────────────────────
with tab_macro:
    st.subheader(T("mc_title"))
    st.caption(T("mc_cap"))
    if st.button(T("mc_btn_refresh")): st.cache_data.clear(); st.rerun()
    st.divider()

    if lang == "EN":
        indicadores=[
            ("Selic",   "Selic (% p.m.)",      432,  lambda v:f"{v:.2f}%", lambda v:(1+v/100)**12-1,"% p.a. equiv."),
            ("IPCA12m", "IPCA 12 months",       13522,lambda v:f"{v:.2f}%", None, None),
            ("CDI",     "CDI (% p.a.)",         4389, lambda v:f"{v:.2f}%", None, None),
            ("IGPM",    "IGP-M (% p.m.)",       189,  lambda v:f"{v:.2f}%", lambda v:(1+v/100)**12-1,"% p.a. equiv."),
            ("USDBRL",  "USD/BRL (PTAX)",       1,    lambda v:f"R$ {v:.4f}",None,None),
            ("PIB",     "GDP — qtrly chg. (%)", 4380, lambda v:f"{v:.1f}%", None, None),
        ]
        opcoes_hist={"Selic (% p.m.)":432,"IPCA 12 months (%)":13522,"CDI (% p.a.)":4389,"IGP-M (% p.m.)":189,"USD/BRL":1}
    else:
        indicadores=[
            ("Selic",   "Selic (% a.m.)",      432,  lambda v:f"{v:.2f}%", lambda v:(1+v/100)**12-1,"% a.a. equiv."),
            ("IPCA12m", "IPCA 12 meses",        13522,lambda v:f"{v:.2f}%", None, None),
            ("CDI",     "CDI (% a.a.)",         4389, lambda v:f"{v:.2f}%", None, None),
            ("IGPM",    "IGP-M (% a.m.)",       189,  lambda v:f"{v:.2f}%", lambda v:(1+v/100)**12-1,"% a.a. equiv."),
            ("USDBRL",  "USD/BRL (PTAX)",       1,    lambda v:f"R$ {v:.4f}",None,None),
            ("PIB",     "PIB - var. trim. (%)", 4380, lambda v:f"{v:.1f}%", None, None),
        ]
        opcoes_hist={"Selic (% a.m.)":432,"IPCA 12 meses (%)":13522,"CDI (% a.a.)":4389,"IGP-M (% a.m.)":189,"USD/BRL":1}

    cols=st.columns(len(indicadores)); fetched={}
    for col,(key,label,sid,fmt_fn,conv_fn,conv_lbl) in zip(cols,indicadores):
        val,data=fetch_last(sid); fetched[key]=val
        extra=f" ({conv_fn(val)*100:.1f} {conv_lbl})" if (val and conv_fn) else ""
        v_str=fmt_fn(val) if val is not None else "—"
        d_str=data if data else T("mc_sem_conexao")
        col.markdown(f'<div class="macro-card"><div class="macro-label">{label}</div><div class="macro-value">{v_str}</div><div class="macro-date">{d_str}{extra}</div></div>',unsafe_allow_html=True)

    st.divider()
    st.subheader(T("mc_serie_hist"))
    sel=st.selectbox(T("mc_indicador"),list(opcoes_hist.keys()),key="macro_sel")
    n_m=st.slider(T("mc_meses"),12,120,36,key="macro_n")
    df_hist=fetch_hist(opcoes_hist[sel],n_m)
    if not df_hist.empty:
        fig_m=go.Figure()
        fig_m.add_trace(go.Scatter(x=df_hist["data"],y=df_hist["valor"],mode="lines",line=dict(color="#1a56db",width=2)))
        fig_m.update_layout(xaxis_title="Data" if lang=="PT" else "Date",yaxis_title=sel,height=340,hovermode="x unified",margin=dict(t=20))
        st.plotly_chart(fig_m,use_container_width=True)
    else: st.info(T("mc_hist_indisponivel"))

    st.divider()
    st.subheader(T("mc_sec_aplicar"))
    selic_aa = ((1+fetched.get("Selic",0.0)/100)**12-1)*100 if fetched.get("Selic") else None
    ipca_v   = fetched.get("IPCA12m"); igpm_aa=((1+fetched.get("IGPM",0.0)/100)**12-1)*100 if fetched.get("IGPM") else None
    cdi_v    = fetched.get("CDI")
    a1,a2,a3,a4=st.columns(4)
    a1.metric(T("mc_selic"), f"{selic_aa:.2f}% {'a.a.' if lang=='PT' else 'p.a.'}" if selic_aa else "—")
    a2.metric(T("mc_ipca"),  f"{ipca_v:.2f}%" if ipca_v else "—")
    a3.metric(T("mc_igpm"),  f"{igpm_aa:.2f}% {'a.a.' if lang=='PT' else 'p.a.'}" if igpm_aa else "—")
    a4.metric(T("mc_cdi"),   f"{cdi_v:.2f}% {'a.a.' if lang=='PT' else 'p.a.'}" if cdi_v else "—")
    if st.button(T("mc_btn_aplicar"), type="primary"):
        if selic_aa: st.session_state["taxa_desc"]=round(selic_aa,2)
        if ipca_v:   st.session_state["ipca_ref"] =round(ipca_v,2)
        if igpm_aa:  st.session_state["igpm_ref"] =round(igpm_aa,2)
        if cdi_v:    st.session_state["cdi_ref"]  =round(cdi_v,2)
        st.success(T("mc_aplicado"))

    st.divider()
    st.subheader(T("mc_focus_title"))
    st.caption(T("mc_focus_cap"))

    focus_map = {
        "IPCA (%)":             "IPCA",
        "PIB (%)":              "PIB Total",
        "Cambio — USD/BRL":     "Taxa de câmbio",
        "Selic — fim de ano (%)":"Meta para taxa over-selic",
    }
    anos_focus = [str(datetime.date.today().year),
                  str(datetime.date.today().year + 1),
                  str(datetime.date.today().year + 2)]

    focus_rows = {}; focus_date = None
    for label, ind in focus_map.items():
        date_f, vals_f = fetch_focus(ind)
        if date_f: focus_date = date_f
        focus_rows[label] = {yr: vals_f.get(yr, None) for yr in anos_focus}

    if any(any(v is not None for v in row.values()) for row in focus_rows.values()):
        df_focus = pd.DataFrame(focus_rows, index=anos_focus).T
        df_focus.columns.name = "Ano" if lang=="PT" else "Year"
        st.dataframe(df_focus.style.format(
            lambda v: f"{v:.2f}" if v is not None else "—"
        ), use_container_width=True)
        if focus_date:
            st.caption(T("mc_focus_coleta").format(d=focus_date))
    else:
        st.info(T("mc_focus_indisponivel"))

# ─────────────────────────────────────────────────────────────────────────────
# ABA 3 — DIVIDA (inputs)
# ─────────────────────────────────────────────────────────────────────────────
with tab_div:
    st.subheader(T("dv_title"))
    st.caption(T("dv_cap"))
    horizonte_div = int(get("horizonte",36))
    n_div = st.slider(T("dv_n_tranches"),1,6,int(get("n_div_v",1)),key="n_div_v")
    for i in range(n_div):
        nm=get(f"div_nome_{i}","").strip() or f"Tranche {i+1}"
        with st.expander(f"Tranche {i+1}  —  {nm}", expanded=(i==0)):

            # ── Identificacao ────────────────────────────────────────────────
            st.markdown(T("dv_sec_ident"))
            ia, ib = st.columns(2)
            ia.text_input(T("dv_nome"), key=f"div_nome_{i}", placeholder=T("dv_nome_ph"))
            ib.selectbox(T("dv_tipo_inst"), TIPOS_DIVIDA, format_func=fmt_opt, key=f"div_tipo_{i}")
            st.number_input(T("dv_valor").format(unit=unit), key=f"div_valor_{i}",
                            min_value=0.0, value=DEF["divida"][unit], step=ustep, format=ufmt)

            st.markdown("---")

            # ── Estrutura Temporal ───────────────────────────────────────────
            st.markdown(T("dv_sec_temporal"))
            ta, tb = st.columns(2)
            ta.slider(T("dv_mes_desemb"), 1, horizonte_div,
                      int(get(f"div_start_{i}", 1)), key=f"div_start_{i}")
            tb.slider(T("dv_tenor"), 6, 120,
                      int(get(f"div_tenor_{i}", 36)), key=f"div_tenor_{i}")

            tc, td = st.columns(2)
            tc.slider(T("dv_carencia_amort"), 0, 24,
                      int(get(f"div_graca_amort_{i}", 6)), key=f"div_graca_amort_{i}")
            td.slider(T("dv_carencia_juros"), 0, 12,
                      int(get(f"div_graca_juros_{i}", 0)), key=f"div_graca_juros_{i}",
                      help=T("dv_carencia_juros_help"))

            st.markdown("---")

            # ── Amortizacao ──────────────────────────────────────────────────
            st.markdown(T("dv_sec_amort"))
            aa, ab, ac = st.columns(3)
            aa.selectbox(T("dv_tipo_amort"), TIPOS_AMORT, key=f"div_tipo_amort_{i}")
            ab.selectbox(T("dv_freq_amort"), list(FREQ_OPTS.keys()), format_func=fmt_opt, key=f"div_freq_amort_{i}")
            ac.selectbox(T("dv_freq_juros"), list(FREQ_OPTS.keys()), format_func=fmt_opt, key=f"div_freq_juros_{i}")

            st.markdown("---")

            # ── Taxa ─────────────────────────────────────────────────────────
            st.markdown(T("dv_sec_taxa"))
            ra, rb = st.columns(2)
            ra.selectbox(T("dv_indexador"), INDEXADORES_DIVIDA, key=f"div_idx_{i}")
            rb.number_input(T("dv_spread"), 0.0, 30.0,
                            float(get(f"div_spread_{i}", 2.5)), 0.1,
                            format="%.2f", key=f"div_spread_{i}")

            idx_s = get(f"div_idx_{i}", "CDI")
            sp    = float(get(f"div_spread_{i}", 2.5))
            mr    = {"ipca": get("ipca_ref", 4.83), "igpm": get("igpm_ref", 3.69),
                     "cdi": get("cdi_ref", 13.65), "selic": get("taxa_desc", 13.75),
                     "tjlp": get("tjlp_ref", 6.0)}
            te    = taxa_div_anual(idx_s, sp, **mr)
            st.info(T("dv_taxa_efetiva").format(idx=idx_s, sp=sp, te=te))

            st.markdown("---")

            # ── Covenants ────────────────────────────────────────────────────
            _COV_TYPES = ["DSCR minimo (x)", "Divida / EBITDA maximo (x)",
                          "Cobertura de juros — ICR (x)", "Texto livre"]

            tem_cov = st.checkbox(T("dv_tem_cov"),
                                  value=bool(get(f"div_tem_cov_{i}", False)),
                                  key=f"div_tem_cov_{i}")
            if tem_cov:
                n_cov = int(get(f"div_n_cov_{i}", 0))
                _ch, _ca, _cb = st.columns([3, 1, 1])
                _ch.markdown(f"<span style='font-size:.85rem;font-weight:700;color:#92400e'>{T('dv_cov_title')}</span>",
                             unsafe_allow_html=True)
                if _ca.button(T("dv_add_cov"), key=f"div_add_cov_{i}", use_container_width=True):
                    st.session_state[f"div_n_cov_{i}"] = n_cov + 1
                    st.rerun()
                if n_cov > 0 and _cb.button(T("dv_cov_limpar"), key=f"div_clr_cov_{i}", use_container_width=True):
                    st.session_state[f"div_n_cov_{i}"] = 0
                    st.rerun()

                if n_cov == 0:
                    st.caption(T("dv_cov_vazio"))
                else:
                    for j in range(n_cov):
                        _ct, _cv = st.columns([3, 2])
                        cov_type = _ct.selectbox(T("dv_cov_tipo"), _COV_TYPES,
                                                 format_func=fmt_opt,
                                                 key=f"div_cov_type_{i}_{j}",
                                                 label_visibility="collapsed")
                        if cov_type == "Texto livre":
                            _cv.text_input(T("dv_cov_texto"),
                                           key=f"div_cov_txt_{i}_{j}",
                                           label_visibility="collapsed",
                                           placeholder="...")
                        else:
                            _cv.number_input(T("dv_cov_valor"), 0.0, 20.0,
                                             float(get(f"div_cov_val_{i}_{j}", 1.5)), 0.05,
                                             format="%.2f", key=f"div_cov_val_{i}_{j}",
                                             label_visibility="collapsed")

    # Grafico consolidado (placeholder — preenchido apos computacoes globais)
    st.divider()
    st.subheader(T("dv_schedule_title"))
    div_chart_placeholder = st.empty()

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTACOES GLOBAIS
# ─────────────────────────────────────────────────────────────────────────────
n_rec_g=int(get("n_rec_v",1)); n_cpv_g=int(get("n_cpv_v",1))
n_opex_g=int(get("n_opex_v",1)); n_capex_g=int(get("n_capex_v",1)); n_div_g=int(get("n_div_v",1))

receitas=[{"nome":get(f"rec_nome_{i}","").strip() or f"Receita {i+1}","valor_anual":get(f"rec_valor_{i}",DEF["receita"][unit])*umult,"crescimento":get(f"rec_cresc_{i}",20.0),"idx":get(f"rec_idx_{i}","Nenhum"),"idx_custom":get(f"rec_idx_custom_{i}",0.0)} for i in range(n_rec_g)]
cpvs=[{"nome":get(f"cpv_nome_{i}","").strip() or f"CPV {i+1}","tipo":get(f"cpv_tipo_{i}","Valor fixo"),"valor_anual":get(f"cpv_valor_{i}",DEF["cpv"][unit])*umult,"crescimento":get(f"cpv_cresc_{i}",5.0),"idx":get(f"cpv_idx_{i}","Nenhum"),"idx_custom":get(f"cpv_idx_custom_{i}",0.0),"linha_ref":get(f"cpv_linha_{i}",""),"pct":get(f"cpv_pct_{i}",25.0)} for i in range(n_cpv_g)]
opexs=[{"nome":get(f"opex_nome_{i}","").strip() or f"Linha {i+1}","cat":get(f"opex_cat_{i}","OpEx"),"valor_anual":get(f"opex_valor_{i}",DEF["opex"][unit])*umult,"crescimento":get(f"opex_cresc_{i}",5.0),"idx":get(f"opex_idx_{i}","Nenhum"),"idx_custom":get(f"opex_idx_custom_{i}",0.0)} for i in range(n_opex_g)]
capex_lines=[{"nome":get(f"cap_nome_{i}","").strip() or f"Ativo {i+1}","valor":get(f"cap_valor_{i}",DEF["capex"][unit])*umult,"vida_util":get(f"cap_vida_{i}",5),"tem_residual":bool(get(f"cap_tem_res_{i}",False)),"pct_residual":get(f"cap_pct_res_{i}",10.0)} for i in range(n_capex_g)]
tranches=[{"nome":get(f"div_nome_{i}","").strip() or f"Tranche {i+1}","valor":get(f"div_valor_{i}",DEF["divida"][unit])*umult,"start_mes":int(get(f"div_start_{i}",1)),"tenor":int(get(f"div_tenor_{i}",36)),"graca_amort":int(get(f"div_graca_amort_{i}",6)),"graca_juros":int(get(f"div_graca_juros_{i}",0)),"tipo_amort":get(f"div_tipo_amort_{i}","SAC"),"freq_amort":get(f"div_freq_amort_{i}","Mensal"),"freq_juros":get(f"div_freq_juros_{i}","Mensal"),"indexador":get(f"div_idx_{i}","CDI"),"spread":get(f"div_spread_{i}",2.5)} for i in range(n_div_g)]

horizonte=int(get("horizonte",36)); taxa_desc=get("taxa_desc",13.75)
ipca_ref=get("ipca_ref",4.83); igpm_ref=get("igpm_ref",3.69); taxa_ir=get("taxa_ir",34.0)
setor=get("setor","Outro"); nome_proj=get("nome_proj","")
responsavel=get("responsavel",""); descricao=get("descricao","")
data_inicio_str=get("data_inicio",_dt.date.today().isoformat())
macro_rates={"ipca":ipca_ref,"igpm":igpm_ref,"cdi":get("cdi_ref",13.65),"selic":taxa_desc,"tjlp":get("tjlp_ref",6.0)}

df_op,payback,roi,npv,mg_med,total_capex = calcular_operacional(receitas,cpvs,opexs,capex_lines,horizonte,taxa_desc,ipca_ref,igpm_ref)
depr_m = calcular_da(capex_lines, horizonte)

# Schedules de divida
schedules={}
proceeds_m  = pd.Series(0.0,index=range(1,horizonte+1))
total_debt  = 0.0

for t in tranches:
    df_t = gerar_schedule(t, macro_rates, horizonte)
    schedules[t["nome"]] = df_t
    sm=t["start_mes"]
    if 1<=sm<=horizonte: proceeds_m[sm]+=t["valor"]
    total_debt+=t["valor"]

# Vectorized debt aggregation (replaces slow iterrows)
interest_m, principal_m = agregar_schedules(schedules, horizonte)

equity_required = max(total_capex-total_debt,0)

# ─── New financial metrics ────────────────────────────────────────────────────
# IRR (project-level): cash flows = [-CapEx, FCF_1, FCF_2, ...]
_irr_flows = [-total_capex] + df_op["FCF"].tolist()
irr_projeto = calcular_irr(_irr_flows)

# Cost of debt & WACC
custo_divida = calcular_custo_medio_divida(tranches, macro_rates)
wacc = calcular_wacc(total_capex, total_debt, equity_required,
                     taxa_desc, custo_divida, taxa_ir)

# Profitability Index
pi_projeto = calcular_profitability_index(npv, total_capex)

# DSCR
dscr_mensal = calcular_dscr(df_op, interest_m, principal_m, horizonte)

# FCF Levered
meses_ser = pd.Series(range(1,horizonte+1))
serv_m = interest_m+principal_m
df_lev = df_op.copy()
df_lev["Servico Divida"] = df_lev["Mes"].map(serv_m)
df_lev["Entrada Divida"] = df_lev["Mes"].map(proceeds_m)
df_lev["FCF Levered"]    = df_lev["FCF"]-df_lev["Servico Divida"]+df_lev["Entrada Divida"]
acum_lev = -equity_required + df_lev["FCF Levered"].cumsum()
df_lev["Acumulado Levered"] = acum_lev.values
pb_lev_s = df_lev[df_lev["Acumulado Levered"]>=0]["Mes"]
payback_lev = int(pb_lev_s.iloc[0]) if not pb_lev_s.empty else None
t_desc_m = tm(taxa_desc)
npv_levered = sum(df_lev["FCF Levered"].iloc[m]/(1+t_desc_m)**(m+1) for m in range(len(df_lev))) - equity_required

# IRR levered (equity-level)
_irr_lev_flows = [-equity_required] + df_lev["FCF Levered"].tolist()
irr_equity = calcular_irr(_irr_lev_flows)

# MIRR (project-level): finance at WACC, reinvest at WACC
mirr_projeto = calcular_mirr(_irr_flows, wacc, wacc)

# Demonstracoes anuais
n_anos = math.ceil(horizonte/12)
df_op_idx = df_op.set_index("Mes")
_regime     = get("regime_fiscal", "Lucro Real")
_pis_r      = get("pis_cofins_rate", 9.25) / 100
_nol_flag   = bool(get("nol_ativo", True)) and (_regime == "Lucro Real")
_csll_r     = get("csll_rate", 9.0) / 100
_marg_irpj  = get("marg_pres_irpj", 32.0) / 100
_marg_csll  = get("marg_pres_csll", 32.0) / 100
_simples_r  = get("simples_aliq", 6.0) / 100
_nol_bal    = 0.0   # carried-forward NOL balance (Lucro Real only)
# NWC / NCG parameters
_tem_ncg    = bool(get("tem_ncg", False))
_ncg_method = get("ncg_method", "pct")
_ncg_pct_r  = get("ncg_pct", 10.0) / 100
_dso        = int(get("dso", 30))
_dio        = int(get("dio", 15))
_dpo        = int(get("dpo", 30))
_prev_nwc   = 0.0   # NWC balance at end of prior year
# ── Revolver parameters ─────────────────────────────────────────────────────
_use_rev         = bool(get("use_revolver", True))
_rev_min_cash_r  = float(get("rev_min_cash_pct", 5.0)) / 100
_rev_rate_r      = (float(get("cdi_ref", 13.65)) + float(get("rev_rate_spread", 3.0))) / 100
_rev_max_cap     = total_capex * float(get("rev_max_cap_pct", 30.0)) / 100
_rev_bal         = 0.0   # outstanding revolver balance
_cash_pre_rev    = 0.0   # cumulative cash before revolver adjustments
annual={}
for y in range(1,n_anos+1):
    idx=list(range((y-1)*12+1, min(y*12,horizonte)+1))
    def s(col, _idx=idx): return sum(df_op_idx.loc[m,col] for m in _idx if m in df_op_idx.index)
    receita_y=s("Receita"); cpv_y=s("CPV")
    # PIS/COFINS deduction (Simples: zero, included in aliquota)
    pis_cofins_y = 0.0 if _regime == "Simples Nacional" else receita_y * _pis_r
    rec_liq_y    = receita_y - pis_cofins_y
    lb_y         = rec_liq_y - cpv_y
    opex_y=s("OpEx"); ga_y=s("G&A"); ebitda_y=lb_y-opex_y-ga_y
    da_y=float(sum(depr_m.get(m,0) for m in idx))
    ebit_y=ebitda_y-da_y
    juros_y=float(sum(interest_m.get(m,0) for m in idx))
    # Revolver interest charged on opening balance (this year, before new draws)
    rev_int_y = _rev_bal * _rev_rate_r if _use_rev else 0.0
    juros_y += rev_int_y
    res_y=s("Rec. Residual")
    lair_y=ebit_y-juros_y+res_y
    # Regime-specific tax
    if _regime == "Lucro Real":
        taxable = max(0.0, lair_y)
        if _nol_flag and _nol_bal > 0:
            used = min(_nol_bal, taxable * 0.30)
            taxable -= used; _nol_bal -= used
        tax_y = taxable * taxa_ir / 100
        if lair_y < 0: _nol_bal += abs(lair_y)
    elif _regime == "Lucro Presumido":
        base_irpj = max(0.0, rec_liq_y) * _marg_irpj
        base_csll  = max(0.0, rec_liq_y) * _marg_csll
        irpj_y = base_irpj * 0.15 + max(0.0, base_irpj - 240_000) * 0.10
        csll_y = base_csll * _csll_r
        tax_y  = irpj_y + csll_y
    else:  # Simples Nacional
        tax_y = max(0.0, receita_y) * _simples_r
    ni_y=lair_y-tax_y
    proc_y=float(sum(proceeds_m.get(m,0) for m in idx))
    prin_y=float(sum(principal_m.get(m,0) for m in idx))
    # NWC / NCG — rolling schedule (AR, INV, AP computed regardless for display)
    ar_y  = receita_y * _dso / 365
    inv_y = cpv_y * _dio / 365
    ap_y  = cpv_y * _dpo / 365
    if _tem_ncg:
        if _ncg_method == "pct":
            nwc_y = receita_y * _ncg_pct_r
        else:
            nwc_y = ar_y + inv_y - ap_y
    else:
        nwc_y = 0.0
    delta_nwc_y = nwc_y - _prev_nwc
    _prev_nwc   = nwc_y
    # Indirect method: start with NI, add back non-cash (D&A) and reclassify interest
    # (juros) to financing activities → add back to FCO, subtract again in FCF_fin
    fco_y=ni_y+da_y+juros_y-delta_nwc_y
    fcf_fin_y=proc_y-prin_y-juros_y
    # ── Revolver mechanics ──────────────────────────────────────────────────
    # Cash before revolver draw/repay adjustments (rev_int already in juros → NI)
    var_cash_pre = fco_y + fcf_fin_y
    _cash_pre_rev += var_cash_pre
    min_cash_y   = receita_y * _rev_min_cash_r
    rev_draw_y   = 0.0
    rev_repay_y  = 0.0
    if _use_rev:
        shortfall = min_cash_y - _cash_pre_rev
        if shortfall > 0:
            rev_draw_y = min(shortfall, max(0.0, _rev_max_cap - _rev_bal))
        else:
            excess = _cash_pre_rev - min_cash_y
            rev_repay_y = min(excess, _rev_bal)
        _rev_bal += rev_draw_y - rev_repay_y
        _cash_pre_rev += rev_draw_y - rev_repay_y
    variacao_caixa_y = var_cash_pre + rev_draw_y - rev_repay_y
    annual[f"Ano {y}"]={"receita":receita_y,"pis_cofins":pis_cofins_y,"rec_liq":rec_liq_y,
        "cpv":cpv_y,"lb":lb_y,
        "mb_pct":lb_y/rec_liq_y*100 if rec_liq_y else 0,
        "opex":opex_y,"ga":ga_y,"ebitda":ebitda_y,
        "ebitda_pct":ebitda_y/rec_liq_y*100 if rec_liq_y else 0,
        "da":da_y,"ebit":ebit_y,"ebit_pct":ebit_y/rec_liq_y*100 if rec_liq_y else 0,
        "juros":juros_y,"lair":lair_y,"tax":tax_y,"ni":ni_y,
        "ni_pct":ni_y/rec_liq_y*100 if rec_liq_y else 0,
        "fco":fco_y,"fcf_fin":fcf_fin_y,
        "variacao_caixa":variacao_caixa_y,
        "proc":proc_y,"prin":prin_y,
        "nwc":nwc_y,"delta_nwc":delta_nwc_y,
        "ar":ar_y,"inv":inv_y,"ap":ap_y,
        "rev_draw":rev_draw_y,"rev_repay":rev_repay_y,"rev_interest":rev_int_y,
        "rev_balance":_rev_bal,"cash_min":min_cash_y}

# Balanco
depr_acc=ni_acc=0.0
# Initial cash after equity injection & CapEx purchase (t=0).
# Debt proceeds flow through fcf_fin during the horizon as they are disbursed.
cash_bs = equity_required - total_capex
balanco={}
for y in range(1,n_anos+1):
    yr=f"Ano {y}"; d=annual[yr]
    depr_acc+=d["da"]; ni_acc+=d["ni"]
    # Cash on BS = cumulative change in cash (which already includes revolver effects)
    cash_bs+=d["variacao_caixa"]
    m_end=min(y*12,horizonte)
    debt_bal=0.0
    for df_t in schedules.values():
        rows_until=df_t[df_t["Mes"]<=m_end]
        if not rows_until.empty: debt_bal+=rows_until.iloc[-1]["Saldo Final"]
    fa_net=max(total_capex-depr_acc,0)
    # Include working capital assets net (AR + Inventory on assets, AP on liabilities)
    nwc_y = d.get("nwc", 0.0)
    rev_bal_y = d.get("rev_balance", 0.0)
    eq_total=equity_required+ni_acc
    total_ativo = cash_bs + fa_net + nwc_y
    total_pas_pl = debt_bal + rev_bal_y + eq_total
    balanco[yr]={"Caixa":cash_bs,"Ativo Imobilizado Liquido":fa_net,
                 "NWC":nwc_y,
                 "Total Ativo":total_ativo,"Divida Total":debt_bal,
                 "Revolver":rev_bal_y,
                 "Capital Social":equity_required,"Lucros Acumulados":ni_acc,
                 "Total PL":eq_total,"Total Passivo + PL":total_pas_pl}

# ─── Financial ratios (annual) ────────────────────────────────────────────────
dscr_anual = calcular_dscr_anual(dscr_mensal, horizonte)
icr_anual = calcular_icr_anual(annual)
divida_ebitda_anual = calcular_divida_ebitda(balanco, annual)

# ─── Sidebar — key metrics summary ────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {T('sb_title')}")
    st.divider()
    st.markdown(f"**{T('sb_metricas')}**")
    _sb_pb_txt = f"{payback} {T('sb_meses')}" if payback else T("sb_na")
    _sb_irr = f"{irr_projeto:.1f}%" if irr_projeto is not None else "N/A"
    _sb_items = [
        (T("sb_roi"), f"{roi:.0f}%"),
        (T("sb_npv"), fv(npv, unit)),
        (T("sb_pb"), _sb_pb_txt),
        (T("sb_mg"), f"{mg_med:.0f}%"),
        ("IRR", _sb_irr),
        ("WACC", f"{wacc:.1f}%"),
    ]
    for _lbl, _val in _sb_items:
        st.markdown(f'<div class="sb-metric"><div class="sb-lbl">{_lbl}</div><div class="sb-val">{_val}</div></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown(f"**{T('sb_config')}**")
    _sb_info = [
        (T("sb_horizonte"), f"{horizonte} {T('sb_meses')}"),
        (T("sb_taxa"), f"{taxa_desc:.1f}%"),
        (T("sb_setor"), fmt_opt(setor)),
        (T("sb_divida"), fv(total_debt, unit)),
        (T("sb_equity"), fv(equity_required, unit)),
    ]
    for _lbl, _val in _sb_info:
        st.caption(f"**{_lbl}:** {_val}")

# ─── Grafico consolidado divida (preenche placeholder) ────────────────────────
with div_chart_placeholder.container():
    if any(not df_t.empty for df_t in schedules.values()):
        meses_div=list(range(1,horizonte+1))
        fig_d=go.Figure()
        cores=["#1a56db","#16a34a","#f97316","#dc2626","#7c3aed","#0891b2"]
        for i,(nome_t,df_t) in enumerate(schedules.items()):
            cor=cores[i%len(cores)]
            amort_s=pd.Series(0.0,index=meses_div)
            juros_s=pd.Series(0.0,index=meses_div)
            if not df_t.empty:
                valid = df_t[df_t["Mes"].between(1, horizonte)]
                if not valid.empty:
                    grp = valid.groupby("Mes").agg({"Amortizacao":"sum","Juros Pagos":"sum"})
                    amort_s = amort_s.add(grp["Amortizacao"], fill_value=0)
                    juros_s = juros_s.add(grp["Juros Pagos"], fill_value=0)
            fig_d.add_trace(go.Bar(x=meses_div,y=(amort_s/umult).tolist(),name=f"{nome_t} — {T('dv_chart_amort')}",marker_color=cor,opacity=0.9))
            fig_d.add_trace(go.Bar(x=meses_div,y=(juros_s/umult).tolist(),name=f"{nome_t} — {T('dv_chart_juros')}",marker_color=cor,opacity=0.5))

        saldo_tot = saldo_total_por_mes(schedules, horizonte)
        fig_d.add_trace(go.Scatter(x=meses_div,y=(saldo_tot/umult).tolist(),mode="lines",
                                   name=T("dv_chart_saldo"),line=dict(color="#dc2626",width=2.5),yaxis="y2"))
        fig_d.update_layout(barmode="stack",height=400,hovermode="x unified",
                            xaxis_title=T("dv_chart_xaxis"),
                            yaxis=dict(title=T("dv_chart_yserv").format(unit=unit),tickformat=",.1f"),
                            yaxis2=dict(title=T("dv_chart_ysaldo").format(unit=unit),overlaying="y",side="right",tickformat=",.1f"),
                            legend=dict(orientation="h",yanchor="bottom",y=1.02))
        st.plotly_chart(fig_d,use_container_width=True)
    else:
        st.info(T("dv_schedule_empty"))

    # ── Covenant compliance dashboard ────────────────────────────────────────
    _any_cov = any(bool(get(f"div_tem_cov_{i}", False)) and int(get(f"div_n_cov_{i}", 0)) > 0
                   for i in range(n_div_g))
    if _any_cov and total_debt > 0:
        st.divider()
        st.subheader(T("dv_cov_dashboard") if T("dv_cov_dashboard") != "dv_cov_dashboard" else "Covenant Compliance")

        # Build covenant data from session state
        _cov_tranches = []
        for i in range(n_div_g):
            if not bool(get(f"div_tem_cov_{i}", False)):
                continue
            nc = int(get(f"div_n_cov_{i}", 0))
            if nc == 0:
                continue
            t_nome = get(f"div_nome_{i}", "").strip() or f"Tranche {i+1}"
            for j in range(nc):
                cov_type = get(f"div_cov_type_{i}_{j}", "")
                cov_val = float(get(f"div_cov_val_{i}_{j}", 1.5))
                _cov_tranches.append({"nome": t_nome, f"cov_type_0": cov_type,
                                       f"cov_val_0": cov_val, "n_cov": 1})

        _violations = verificar_covenants(_cov_tranches, dscr_anual, icr_anual, divida_ebitda_anual)
        if _violations:
            _viol_rows = []
            for v in _violations:
                _status = "\u2705" if v["compliant"] else "\u274c"
                _val_str = f"{v['value']:.2f}" if v["value"] != float('inf') else "\u221e"
                _viol_rows.append({
                    "Tranche": v["tranche"],
                    "Covenant": v["covenant"],
                    ("Limite" if lang == "PT" else "Limit"): f"{v['limit']:.2f}",
                    ("Valor" if lang == "PT" else "Value"): _val_str,
                    ("Ano" if lang == "PT" else "Year"): v["year"],
                    "Status": _status,
                })
            df_cov = pd.DataFrame(_viol_rows)
            _n_fail = sum(1 for v in _violations if not v["compliant"])
            if _n_fail > 0:
                st.warning(f"{'Atenção' if lang=='PT' else 'Warning'}: {_n_fail} {'violações de covenant detectadas' if lang=='PT' else 'covenant violations detected'}.")
            else:
                st.success(f"{'Todos os covenants atendidos' if lang=='PT' else 'All covenants met'}.")
            st.dataframe(df_cov, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# ABA 4 — RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────
with tab_res:
    st.subheader(nome_proj or "Projeto sem nome" if lang=="PT" else nome_proj or "Unnamed project")
    st.caption(T("res_cap").format(
        s=fmt_opt(setor), h=horizonte,
        cx=fv(total_capex,unit), dv=fv(total_debt,unit), eq=fv(equity_required,unit)))
    st.divider()

    bench=BENCHMARKS.get(setor)
    if bench:
        st.subheader(T("res_val_prem"))
        cresc_m=((1+sum(r["crescimento"] for r in receitas)/len(receitas)/100)**(1/12)-1)*100
        alertas=[]
        if cresc_m>bench["crescimento_max"]:   alertas.append(("warn",T("al_cresc_above").format(c=cresc_m,mn=bench["crescimento_min"],mx=bench["crescimento_max"])))
        elif cresc_m<bench["crescimento_min"]: alertas.append(("ok",  T("al_cresc_below").format(c=cresc_m,mn=bench["crescimento_min"],mx=bench["crescimento_max"])))
        else:                                  alertas.append(("ok",  T("al_cresc_ok").format(c=cresc_m,mn=bench["crescimento_min"],mx=bench["crescimento_max"])))
        if mg_med>bench["margem_max"]:         alertas.append(("warn",T("al_mg_above").format(m=mg_med,mn=bench["margem_min"],mx=bench["margem_max"])))
        elif mg_med<bench["margem_min"]:       alertas.append(("bad", T("al_mg_below").format(m=mg_med,mn=bench["margem_min"],mx=bench["margem_max"])))
        else:                                  alertas.append(("ok",  T("al_mg_ok").format(m=mg_med,mn=bench["margem_min"],mx=bench["margem_max"])))
        if payback is None:               alertas.append(("bad", T("al_pb_none").format(mn=bench["payback_min"],mx=bench["payback_max"])))
        elif payback>bench["payback_max"]:alertas.append(("warn",T("al_pb_above").format(pb=payback,mn=bench["payback_min"],mx=bench["payback_max"])))
        else:                             alertas.append(("ok",  T("al_pb_ok").format(pb=payback,mn=bench["payback_min"],mx=bench["payback_max"])))
        css={"ok":"alerta-ok","warn":"alerta-warn","bad":"alerta-bad"}
        icn={"ok":"✓","warn":"!","bad":"x"}
        for tipo,msg in alertas: st.markdown(f'<div class="{css[tipo]}">{icn[tipo]}  {msg}</div>',unsafe_allow_html=True)
        st.divider()

    st.subheader(T("res_metricas"))

    def _metric_card(label, value, positive=None):
        cls = "metric-card"
        if positive is True: cls += " metric-card-green"
        elif positive is False: cls += " metric-card-red"
        delta_html = ""
        if positive is not None:
            d_cls = "mc-pos" if positive else "mc-neg"
            d_txt = T("res_positivo") if positive else T("res_negativo")
            d_arrow = "\u2191" if positive else "\u2193"
            delta_html = f'<div class="mc-delta {d_cls}">{d_arrow} {d_txt}</div>'
        return f'<div class="{cls}"><div class="mc-label">{label}</div><div class="mc-value">{value}</div>{delta_html}</div>'

    r1,r2=st.tabs([T("res_tab_proj"), T("res_tab_eq")])
    with r1:
        m1,m2,m3,m4=st.columns(4)
        m1.markdown(ds.metric_card(T("res_roi_proj"), f"{roi:.0f}%",
                                    "green" if roi > 0 else "red"), unsafe_allow_html=True)
        _pb_status = ("green" if payback and payback < horizonte * 0.6
                      else "amber" if payback and payback < horizonte
                      else "red")
        m2.markdown(ds.metric_card(T("res_pb_proj"),
                                    f"{payback} {'meses' if lang=='PT' else 'mo'}" if payback else T("res_nao_atingido"),
                                    _pb_status), unsafe_allow_html=True)
        m3.markdown(ds.metric_card(T("res_npv_proj"), fv(npv,unit),
                                    "green" if npv > 0 else "red"), unsafe_allow_html=True)
        m4.markdown(ds.metric_card(T("res_mg_proj"), f"{mg_med:.0f}%", "neutral"), unsafe_allow_html=True)
        # Row 2: IRR, MIRR, PI, WACC
        m5,m6,m7,m8=st.columns(4)
        _irr_str = f"{irr_projeto:.1f}%" if irr_projeto is not None else "N/A"
        # Use design-system status thresholds (Section 4.3): IRR >25% green, 20-25% amber, <20% red
        _irr_status = ds.status_for("irr", irr_projeto) if irr_projeto is not None else "neutral"
        m5.markdown(ds.metric_card(T("res_irr_proj"), _irr_str, _irr_status,
                                    sub=f"vs WACC {wacc:.1f}%" if irr_projeto is not None else ""),
                    unsafe_allow_html=True)
        _mirr_str = f"{mirr_projeto:.1f}%" if mirr_projeto is not None else "N/A"
        _mirr_status = ds.status_for("irr", mirr_projeto) if mirr_projeto is not None else "neutral"
        m6.markdown(ds.metric_card(T("res_mirr"), _mirr_str, _mirr_status), unsafe_allow_html=True)
        _pi_str = f"{pi_projeto:.2f}x" if pi_projeto is not None else "N/A"
        _pi_status = ("green" if pi_projeto > 1.5 else "amber" if pi_projeto > 1 else "red") if pi_projeto is not None else "neutral"
        m7.markdown(ds.metric_card(T("res_pi"), _pi_str, _pi_status), unsafe_allow_html=True)
        m8.markdown(ds.metric_card(T("res_wacc"), f"{wacc:.2f}%", "neutral"), unsafe_allow_html=True)
    with r2:
        e1,e2,e3,e4=st.columns(4)
        eq_roi=(df_lev["FCF Levered"].sum()/equity_required*100) if equity_required>0 else 0
        e1.markdown(ds.metric_card(T("res_roi_eq"), f"{eq_roi:.0f}%",
                                    "green" if eq_roi > 0 else "red"), unsafe_allow_html=True)
        _pb_eq_status = ("green" if payback_lev and payback_lev < horizonte * 0.6
                         else "amber" if payback_lev and payback_lev < horizonte
                         else "red")
        e2.markdown(ds.metric_card(T("res_pb_eq"),
                                    f"{payback_lev} {'meses' if lang=='PT' else 'mo'}" if payback_lev else T("res_nao_atingido"),
                                    _pb_eq_status), unsafe_allow_html=True)
        e3.markdown(ds.metric_card(T("res_npv_eq"), fv(npv_levered,unit),
                                    "green" if npv_levered > 0 else "red"), unsafe_allow_html=True)
        e4.markdown(ds.metric_card(T("res_eq_req"), fv(equity_required,unit), "neutral"), unsafe_allow_html=True)
        # Row 2: IRR equity, DSCR min — design system status thresholds
        e5,e6,e7,e8=st.columns(4)
        _irr_eq_str = f"{irr_equity:.1f}%" if irr_equity is not None else "N/A"
        _irr_eq_status = ds.status_for("irr", irr_equity) if irr_equity is not None else "neutral"
        e5.markdown(ds.metric_card(T("res_irr_eq"), _irr_eq_str, _irr_eq_status), unsafe_allow_html=True)
        _dscr_vals = [v for v in dscr_anual.values() if v != float('inf')]
        _dscr_min = min(_dscr_vals) if _dscr_vals else None
        _dscr_str = f"{_dscr_min:.2f}x" if _dscr_min is not None else "N/A"
        _dscr_status = ds.status_for("dscr", _dscr_min) if _dscr_min is not None else "neutral"
        e6.markdown(ds.metric_card(T("res_dscr_min"), _dscr_str, _dscr_status,
                                    sub="min > 1.3x"), unsafe_allow_html=True)
        _cd_str = f"{custo_divida:.2f}%" if total_debt > 0 else "N/A"
        e7.markdown(ds.metric_card(T("res_custo_divida"), _cd_str, "neutral"), unsafe_allow_html=True)
        e8.empty()
    st.divider()

    st.subheader(T("res_veredicto"))
    lim=horizonte*(2/3)
    if payback and payback<=lim and npv>0:
        cls,ttl="veredicto-verde",T("res_viavel")
        txt=T("res_txt_viavel").format(pb=payback,npv=fv(npv,unit))
    elif (payback and payback<=horizonte) or npv>0:
        cls,ttl="veredicto-amarelo",T("res_atencao")
        mot=[]
        if payback and payback>lim: mot.append(T("res_mot_pb").format(pb=payback))
        if npv<=0: mot.append(T("res_mot_npv"))
        txt=T("res_txt_atencao").format(mot="; ".join(mot))
    else:
        cls,ttl="veredicto-vermelho",T("res_inviavel")
        txt=T("res_txt_inviavel").format(h=horizonte,npv=fv(npv,unit))
    st.markdown(f'<div class="{cls}"><div class="veredicto-titulo">{ttl}</div><p>{txt}</p></div>',unsafe_allow_html=True)
    st.divider()

    # ── Comparables Valuation (Resultados) ───────────────────────────────────
    if st.session_state.get("model_type") == "valuation_dcf":
        import statistics as _stats
        _n_comp_r = int(get("n_comp_v", 3))
        _comps = []
        for ci in range(_n_comp_r):
            _c_ev = get(f"comp_ev_{ci}", 0.0) * umult
            _c_rec = get(f"comp_receita_{ci}", 0.0) * umult
            _c_ebitda = get(f"comp_ebitda_{ci}", 0.0) * umult
            _c_ni = get(f"comp_ni_{ci}", 0.0) * umult
            _c_nome = get(f"comp_nome_{ci}", "").strip() or f"Comp {ci+1}"
            if _c_ev > 0 and (_c_rec > 0 or _c_ebitda > 0):
                _comps.append({"nome": _c_nome, "ev": _c_ev, "rec": _c_rec,
                               "ebitda": _c_ebitda, "ni": _c_ni})
        if _comps:
            st.subheader(T("comp_resultados"))
            st.caption(T("comp_res_cap").format(n=len(_comps)))

            # Calculate multiples
            _comp_rows = []
            _ev_rev_list, _ev_ebitda_list, _pe_list = [], [], []
            for c in _comps:
                ev_rev = c["ev"] / c["rec"] if c["rec"] > 0 else None
                ev_ebitda = c["ev"] / c["ebitda"] if c["ebitda"] > 0 else None
                pe = c["ev"] / c["ni"] if c["ni"] > 0 else None
                _comp_rows.append({
                    T("comp_hdr_empresa"): c["nome"],
                    T("comp_hdr_ev"): fv(c["ev"], unit),
                    T("comp_hdr_ev_rev"): f"{ev_rev:.1f}x" if ev_rev else "\u2014",
                    T("comp_hdr_ev_ebitda"): f"{ev_ebitda:.1f}x" if ev_ebitda else "\u2014",
                    T("comp_hdr_pe"): f"{pe:.1f}x" if pe else "\u2014",
                })
                if ev_rev: _ev_rev_list.append(ev_rev)
                if ev_ebitda: _ev_ebitda_list.append(ev_ebitda)
                if pe: _pe_list.append(pe)

            _med_ev_rev = _stats.median(_ev_rev_list) if _ev_rev_list else None
            _med_ev_ebitda = _stats.median(_ev_ebitda_list) if _ev_ebitda_list else None
            _med_pe = _stats.median(_pe_list) if _pe_list else None
            _mean_ev_rev = _stats.mean(_ev_rev_list) if _ev_rev_list else None
            _mean_ev_ebitda = _stats.mean(_ev_ebitda_list) if _ev_ebitda_list else None
            _mean_pe = _stats.mean(_pe_list) if _pe_list else None

            # Summary rows
            _comp_rows.append({
                T("comp_hdr_empresa"): f"**{T('comp_mediana')}**",
                T("comp_hdr_ev"): "\u2014",
                T("comp_hdr_ev_rev"): f"**{_med_ev_rev:.1f}x**" if _med_ev_rev else "\u2014",
                T("comp_hdr_ev_ebitda"): f"**{_med_ev_ebitda:.1f}x**" if _med_ev_ebitda else "\u2014",
                T("comp_hdr_pe"): f"**{_med_pe:.1f}x**" if _med_pe else "\u2014",
            })
            _comp_rows.append({
                T("comp_hdr_empresa"): f"**{T('comp_media')}**",
                T("comp_hdr_ev"): "\u2014",
                T("comp_hdr_ev_rev"): f"**{_mean_ev_rev:.1f}x**" if _mean_ev_rev else "\u2014",
                T("comp_hdr_ev_ebitda"): f"**{_mean_ev_ebitda:.1f}x**" if _mean_ev_ebitda else "\u2014",
                T("comp_hdr_pe"): f"**{_mean_pe:.1f}x**" if _mean_pe else "\u2014",
            })

            st.markdown(f"**{T('comp_tabela_title')}**")
            st.dataframe(pd.DataFrame(_comp_rows), use_container_width=True, hide_index=True)

            # Implied valuation from Year 1 projections
            _ano1 = annual.get("Ano 1", {})
            _target_rec = _ano1.get("receita", 0)
            _target_ebitda = _ano1.get("ebitda", 0)
            _target_ni = _ano1.get("ni", 0)

            if _target_rec > 0 or _target_ebitda > 0:
                st.markdown(f"**{T('comp_implied_title')}**")
                st.caption(T("comp_implied_cap"))

                _imp_cols = st.columns(3)
                if _med_ev_rev and _target_rec > 0:
                    _vals_rev = [v * _target_rec for v in _ev_rev_list]
                    _imp_cols[0].markdown(_metric_card(
                        T("comp_por_receita"), fv(_med_ev_rev * _target_rec, unit), True
                    ), unsafe_allow_html=True)
                    _imp_cols[0].caption(
                        f"{T('comp_min')}: {fv(min(_vals_rev), unit)} \u00b7 "
                        f"{T('comp_max')}: {fv(max(_vals_rev), unit)}")

                if _med_ev_ebitda and _target_ebitda > 0:
                    _vals_ebitda = [v * _target_ebitda for v in _ev_ebitda_list]
                    _imp_cols[1].markdown(_metric_card(
                        T("comp_por_ebitda"), fv(_med_ev_ebitda * _target_ebitda, unit), True
                    ), unsafe_allow_html=True)
                    _imp_cols[1].caption(
                        f"{T('comp_min')}: {fv(min(_vals_ebitda), unit)} \u00b7 "
                        f"{T('comp_max')}: {fv(max(_vals_ebitda), unit)}")

                if _med_pe and _target_ni > 0:
                    _vals_pe = [v * _target_ni for v in _pe_list]
                    _imp_cols[2].markdown(_metric_card(
                        T("comp_por_ni"), fv(_med_pe * _target_ni, unit), True
                    ), unsafe_allow_html=True)
                    _imp_cols[2].caption(
                        f"{T('comp_min')}: {fv(min(_vals_pe), unit)} \u00b7 "
                        f"{T('comp_max')}: {fv(max(_vals_pe), unit)}")

                # Football field chart
                _range_data = []
                if _ev_rev_list and _target_rec > 0:
                    _range_data.append({"method": T("comp_por_receita"),
                        "lo": min(v * _target_rec for v in _ev_rev_list) / umult,
                        "hi": max(v * _target_rec for v in _ev_rev_list) / umult,
                        "med": _med_ev_rev * _target_rec / umult})
                if _ev_ebitda_list and _target_ebitda > 0:
                    _range_data.append({"method": T("comp_por_ebitda"),
                        "lo": min(v * _target_ebitda for v in _ev_ebitda_list) / umult,
                        "hi": max(v * _target_ebitda for v in _ev_ebitda_list) / umult,
                        "med": _med_ev_ebitda * _target_ebitda / umult})
                if _pe_list and _target_ni > 0:
                    _range_data.append({"method": T("comp_por_ni"),
                        "lo": min(v * _target_ni for v in _pe_list) / umult,
                        "hi": max(v * _target_ni for v in _pe_list) / umult,
                        "med": _med_pe * _target_ni / umult})

                if _range_data:
                    fig_comp = go.Figure()
                    for rd in _range_data:
                        fig_comp.add_trace(go.Bar(
                            x=[rd["hi"] - rd["lo"]], y=[rd["method"]],
                            base=[rd["lo"]], orientation="h",
                            marker_color="#1a56db", opacity=0.7, showlegend=False,
                            hovertemplate=(f"{rd['method']}<br>"
                                          f"{T('comp_min')}: {rd['lo']:,.1f}<br>"
                                          f"{T('comp_med')}: {rd['med']:,.1f}<br>"
                                          f"{T('comp_max')}: {rd['hi']:,.1f}<extra></extra>")))
                        fig_comp.add_trace(go.Scatter(
                            x=[rd["med"]], y=[rd["method"]],
                            mode="markers", marker=dict(color="#dc2626", size=12, symbol="diamond"),
                            showlegend=False,
                            hovertemplate=f"{T('comp_med')}: {rd['med']:,.1f}<extra></extra>"))
                    fig_comp.update_layout(
                        height=max(200, len(_range_data) * 80),
                        xaxis_title=f"Enterprise Value ({unit})",
                        xaxis=dict(tickformat=",.0f"),
                        yaxis=dict(autorange=True),
                        margin=dict(t=20, l=10))
                    st.plotly_chart(fig_comp, use_container_width=True)
            st.divider()

    st.subheader(T("res_visualizacoes"))
    _g_titles = [T("g1_title"), T("g2_title"), T("g3_title"), T("g4_title"), T("g5_waterfall")]
    g1, g2, g3, g4, g5 = st.tabs(_g_titles)
    meses=df_op["Mes"].tolist()
    def yu(s): return (s/umult).tolist()

    # ── Helper: CAGR annotation for time-series ─────────────────────────────
    def _cagr_annotation(fig, series, meses_list, unit_str, color="#1e3a8a"):
        """Add CAGR annotation between first and last positive value."""
        if len(series) < 13:
            return
        v0 = next((v for v in series if v > 0), None)
        v1 = series[-1]
        if v0 is None or v0 <= 0 or v1 <= 0:
            return
        n_years = len(series) / 12
        try:
            cagr = ((v1 / v0) ** (1 / n_years) - 1) * 100
        except (ZeroDivisionError, ValueError):
            return
        m_last = meses_list[-1]
        fig.add_annotation(
            x=m_last, y=v1, ax=-60, ay=-30,
            text=f"<b>CAGR: {cagr:+.1f}%</b>",
            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2,
            arrowcolor=color, bgcolor="rgba(255,255,255,0.85)",
            bordercolor=color, borderwidth=1, borderpad=4,
            font=dict(color=color, size=11, family="Arial Black"),
        )

    with g1:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=meses,y=yu(df_op["Acumulado"]),mode="lines",name=T("g_fcf_proj"),line=dict(color="#1a56db",width=2.5)))
        if total_debt>0: fig.add_trace(go.Scatter(x=meses,y=yu(df_lev["Acumulado Levered"]),mode="lines",name=T("g_fcf_eq"),line=dict(color="#16a34a",width=2,dash="dot")))
        fig.add_hline(y=0,line_dash="dash",line_color="#9ca3af",annotation_text=T("g_breakeven"))
        if payback:
            vp=yu(df_op[df_op["Mes"]==payback]["Acumulado"])
            if vp: fig.add_trace(go.Scatter(x=[payback],y=[vp[0]],mode="markers",name=T("g_pb_proj").format(pb=payback),marker=dict(color="#1a56db",size=10,symbol="star")))
        if payback_lev:
            vp2=yu(df_lev[df_lev["Mes"]==payback_lev]["Acumulado Levered"])
            if vp2: fig.add_trace(go.Scatter(x=[payback_lev],y=[vp2[0]],mode="markers",name=T("g_pb_eq").format(pb=payback_lev),marker=dict(color="#16a34a",size=10,symbol="star")))
        fig.update_layout(xaxis_title=T("g_xaxis_mes"),yaxis_title=unit,hovermode="x unified",height=420,legend=dict(orientation="h",yanchor="bottom",y=1.02))
        fig.update_yaxes(tickformat=",.1f"); st.plotly_chart(fig,use_container_width=True)

    with g2:
        fig2=go.Figure()
        for col,cor,nm in [("Receita","#1a56db",T("g_receita")),("CPV","#f97316",T("g_cpv"))]:
            fig2.add_trace(go.Scatter(x=meses,y=yu(df_op[col]),mode="lines",name=nm,line=dict(color=cor,width=2)))
        fig2.add_trace(go.Scatter(x=meses,y=yu(df_op["OpEx"]+df_op["G&A"]),mode="lines",name=T("g_opex_ga"),line=dict(color="#dc2626",width=2)))
        # CAGR annotation on Receita
        _cagr_annotation(fig2, yu(df_op["Receita"]), meses, unit, color="#1e3a8a")
        fig2.update_layout(xaxis_title=T("g_xaxis_mes"),yaxis_title=unit,hovermode="x unified",height=420,legend=dict(orientation="h",yanchor="bottom",y=1.02))
        fig2.update_yaxes(tickformat=",.1f"); st.plotly_chart(fig2,use_container_width=True)

    with g3:
        fig3=go.Figure()
        fig3.add_trace(go.Bar(x=meses,y=yu(df_op["Margem Bruta"]),name=T("g_mb"),marker_color="#1a56db"))
        fig3.add_trace(go.Bar(x=meses,y=[-v for v in yu(df_op["OpEx"])],name=T("g_opex"),marker_color="#f97316"))
        fig3.add_trace(go.Bar(x=meses,y=[-v for v in yu(df_op["G&A"])],name=T("g_ga"),marker_color="#dc2626"))
        fig3.add_trace(go.Scatter(x=meses,y=yu(df_op["EBIT"]),mode="lines",name=T("g_ebit"),line=dict(color="#16a34a",width=2.5)))
        fig3.update_layout(barmode="relative",xaxis_title=T("g_xaxis_mes"),yaxis_title=unit,hovermode="x unified",height=420,legend=dict(orientation="h",yanchor="bottom",y=1.02))
        fig3.update_yaxes(tickformat=",.1f"); st.plotly_chart(fig3,use_container_width=True)

    with g4:
        fig4=go.Figure()
        fig4.add_trace(go.Bar(x=meses,y=yu(df_lev["Servico Divida"]),name=T("g_serv_div"),marker_color="#dc2626"))
        fig4.add_trace(go.Scatter(x=meses,y=yu(df_op["EBIT"]),mode="lines",name=T("g_ebit"),line=dict(color="#1a56db",width=2)))
        fig4.update_layout(xaxis_title=T("g_xaxis_mes"),yaxis_title=unit,hovermode="x unified",height=420,legend=dict(orientation="h",yanchor="bottom",y=1.02))
        fig4.update_yaxes(tickformat=",.1f"); st.plotly_chart(fig4,use_container_width=True)

    with g5:
        # Waterfall chart: Receita Bruta → ... → Lucro Liquido (Year 1 totals)
        st.caption(T("g5_waterfall_cap"))
        _y1 = annual.get("Ano 1", {})
        if _y1 and _y1.get("receita", 0) > 0:
            _wf_labels = [
                T("dre_rec_bruta") if T("dre_rec_bruta") != "dre_rec_bruta" else ("Receita Bruta" if lang=="PT" else "Gross Revenue"),
            ]
            _wf_vals = [_y1["receita"] / umult]
            _wf_meas = ["absolute"]

            if _y1.get("pis_cofins", 0) > 0:
                _wf_labels.append("(–) PIS/COFINS")
                _wf_vals.append(-_y1["pis_cofins"] / umult)
                _wf_meas.append("relative")
                _wf_labels.append(T("dre_rec_liq"))
                _wf_vals.append(0)
                _wf_meas.append("total")

            _wf_labels.append("(–) " + ("CPV" if lang=="PT" else "COGS"))
            _wf_vals.append(-_y1["cpv"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("Lucro Bruto" if lang=="PT" else "Gross Profit")
            _wf_vals.append(0)
            _wf_meas.append("total")

            _wf_labels.append("(–) OpEx")
            _wf_vals.append(-_y1["opex"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("(–) G&A")
            _wf_vals.append(-_y1["ga"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("EBITDA")
            _wf_vals.append(0)
            _wf_meas.append("total")

            _wf_labels.append("(–) D&A")
            _wf_vals.append(-_y1["da"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("EBIT")
            _wf_vals.append(0)
            _wf_meas.append("total")

            _wf_labels.append("(–) " + ("Juros" if lang=="PT" else "Interest"))
            _wf_vals.append(-_y1["juros"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("(–) " + ("Imposto" if lang=="PT" else "Tax"))
            _wf_vals.append(-_y1["tax"] / umult)
            _wf_meas.append("relative")

            _wf_labels.append("Lucro Liquido" if lang=="PT" else "Net Income")
            _wf_vals.append(0)
            _wf_meas.append("total")

            fig_wf = go.Figure(go.Waterfall(
                orientation="v",
                measure=_wf_meas,
                x=_wf_labels,
                y=_wf_vals,
                text=[f"{v:+,.1f}" if m == "relative" else "" for v, m in zip(_wf_vals, _wf_meas)],
                textposition="outside",
                connector={"line": {"color": "#94a3b8", "width": 1}},
                increasing={"marker": {"color": "#16a34a"}},
                decreasing={"marker": {"color": "#dc2626"}},
                totals={"marker": {"color": "#1a56db"}},
            ))
            fig_wf.update_layout(
                title=f"{T('g5_waterfall_title')} — {'Ano 1' if lang=='PT' else 'Year 1'} ({unit})",
                height=480, showlegend=False,
                yaxis=dict(tickformat=",.1f"),
                xaxis=dict(tickangle=-30),
                margin=dict(t=60, b=80, l=20, r=20),
            )
            st.plotly_chart(fig_wf, use_container_width=True)
        else:
            st.info(T("g5_waterfall_empty"))

# ─────────────────────────────────────────────────────────────────────────────
# ABA 5 — DFs
# ─────────────────────────────────────────────────────────────────────────────
def mn(v): return round(v / umult, 2)   # monetary → unit scale
def pn(v): return round(v, 1)           # percentage → float


def _row_styles(df):
    """Return same-shape DataFrame of CSS strings for subtotal rows."""
    out = pd.DataFrame("", index=df.index, columns=df.columns)
    for idx in df.index:
        # Direct PT match OR reverse-translate EN→PT then look up
        pt_key = _DF_ROW_EN_INV.get(idx, idx)
        css = _ROW_CSS.get(pt_key)
        if css:
            out.loc[idx] = css
    return out

def _heatmap_styles(df_num, reverse=False):
    """Pure-Python RdYlGn gradient — no matplotlib needed."""
    vals = df_num.values.flatten().astype(float)
    vmin, vmax = float(vals.min()), float(vals.max())
    rng = vmax - vmin if vmax != vmin else 1.0
    def _c(v):
        t = max(0.0, min(1.0, (v - vmin) / rng))
        if reverse: t = 1 - t
        if t < 0.5:
            s = t * 2
            r,g,b = int(215+(255-215)*s), int(48+(255-48)*s), int(39+(191-39)*s)
        else:
            s = (t-0.5)*2
            r,g,b = int(255+(26-255)*s), int(255+(152-255)*s), int(191+(80-191)*s)
        txt = "#1a1a1a" if (0.299*r+0.587*g+0.114*b) > 150 else "#fff"
        return f"background-color:rgb({r},{g},{b});color:{txt};font-weight:600"
    return pd.DataFrame(
        [[_c(df_num.iloc[i,j]) for j in range(df_num.shape[1])]
         for i in range(df_num.shape[0])],
        index=df_num.index, columns=df_num.columns
    )

with tab_df:
    st.subheader(nome_proj or "Projeto sem nome" if lang=="PT" else nome_proj or "Unnamed project")
    st.caption(T("df_cap").format(r=taxa_ir, cx=fv(total_capex,unit)))
    anos = list(annual.keys())
    unit_note = T("df_unit_note").format(unit=unit)

    # Annual column labels: "Ano 1" in PT, "Year 1" in EN
    ano_lbl = {yr: yr.replace("Ano", "Year") for yr in anos} if lang == "EN" else {yr: yr for yr in anos}

    def _render_df(data_dict):
        fmt = {}
        for key, vals in data_dict.items():
            is_pct = "(%)" in key
            fmt[key] = {ano_lbl[yr]: (f"{v:.1f}%" if is_pct else f"{v:,.2f}") for yr, v in vals.items()}
        df_str = pd.DataFrame(fmt, index=[ano_lbl[yr] for yr in anos]).T
        # Rename rows to EN if needed
        if lang == "EN":
            df_str = df_str.rename(index=_DF_ROW_EN)
        html = df_str.style.apply(lambda d: _row_styles(d), axis=None).to_html()
        st.markdown(f'<div class="df-styled">{html}</div>', unsafe_allow_html=True)

    # Dynamic IR row label (already in target language)
    ir_row_key = T("df_ir_row").format(r=taxa_ir)

    with st.expander(T("df_dre"), expanded=True):
        st.caption(unit_note)
        _pis_any = any(d["pis_cofins"] != 0 for d in annual.values())
        _dre_data = {"Receita Bruta": {yr: mn(d["receita"]) for yr,d in annual.items()}}
        if _pis_any:
            _dre_data[T("dre_pis_cofins")] = {yr: mn(d["pis_cofins"]) for yr,d in annual.items()}
            _dre_data[T("dre_rec_liq")]    = {yr: mn(d["rec_liq"])    for yr,d in annual.items()}
        _dre_data.update({
            "(–) CPV":                        {yr: mn(d["cpv"])        for yr,d in annual.items()},
            "Lucro Bruto":                    {yr: mn(d["lb"])         for yr,d in annual.items()},
            "Margem Bruta (%)":               {yr: pn(d["mb_pct"])    for yr,d in annual.items()},
            "(–) OpEx":                       {yr: mn(d["opex"])       for yr,d in annual.items()},
            "(–) G&A":                        {yr: mn(d["ga"])         for yr,d in annual.items()},
            "EBITDA":                         {yr: mn(d["ebitda"])     for yr,d in annual.items()},
            "Margem EBITDA (%)":              {yr: pn(d["ebitda_pct"])for yr,d in annual.items()},
            "(–) Depreciacao e Amortizacao":  {yr: mn(d["da"])         for yr,d in annual.items()},
            "EBIT":                           {yr: mn(d["ebit"])       for yr,d in annual.items()},
            "Margem EBIT (%)":                {yr: pn(d["ebit_pct"])  for yr,d in annual.items()},
            "(–) Despesas Financeiras":       {yr: mn(d["juros"])      for yr,d in annual.items()},
            "LAIR":                           {yr: mn(d["lair"])       for yr,d in annual.items()},
            ir_row_key:                       {yr: mn(d["tax"])        for yr,d in annual.items()},
            "Lucro Liquido":                  {yr: mn(d["ni"])         for yr,d in annual.items()},
            "Margem Liquida (%)":             {yr: pn(d["ni_pct"])    for yr,d in annual.items()},
        })
        _render_df(_dre_data)
        if _pis_any:
            st.caption(T("dre_pis_note"))

    with st.expander(T("df_dfc"), expanded=False):
        st.caption(unit_note)
        _dfc_data = {
            "Lucro Liquido":                     {yr: mn(d["ni"])  for yr,d in annual.items()},
            "(+) Depreciacao e Amortizacao":     {yr: mn(d["da"])  for yr,d in annual.items()},
            "(+) Juros (reclassificados)":       {yr: mn(d["juros"]) for yr,d in annual.items()},
        }
        if _tem_ncg:
            _dfc_data[T("dfc_delta_ncg")] = {yr: mn(d["delta_nwc"]) for yr,d in annual.items()}
        _dfc_data.update({
            "FCO — Atividades Operacionais":     {yr: mn(d["fco"])            for yr,d in annual.items()},
            "FCI — Atividades de Investimento":  {yr: 0.0                     for yr  in annual.keys()  },
            "(+) Captacao de Divida":            {yr: mn(d["proc"])           for yr,d in annual.items()},
            "(–) Amortizacao de Principal":      {yr: mn(d["prin"])           for yr,d in annual.items()},
            "(–) Despesas Financeiras":          {yr: mn(d["juros"])          for yr,d in annual.items()},
            "FCF — Atividades de Financiamento": {yr: mn(d["fcf_fin"])        for yr,d in annual.items()},
        })
        _any_rev = any(d.get("rev_draw", 0) > 0 or d.get("rev_repay", 0) > 0
                       for d in annual.values())
        if _any_rev or bool(get("use_revolver", True)):
            _dfc_data["(+) Saque do Revolver"]       = {yr: mn(d.get("rev_draw",0))  for yr,d in annual.items()}
            _dfc_data["(–) Amortizacao do Revolver"] = {yr: mn(d.get("rev_repay",0)) for yr,d in annual.items()}
        _dfc_data["Variacao Liquida de Caixa"] = {yr: mn(d["variacao_caixa"]) for yr,d in annual.items()}
        _render_df(_dfc_data)
        notes = [T("df_dfc_note").format(cx=fv(total_capex,unit))]
        if _tem_ncg: notes.append(T("ncg_note"))
        for n in notes: st.caption(n)

        # ── Rolling Working Capital schedule (when dias method) ─────────────
        if _tem_ncg and _ncg_method == "dias":
            with st.expander(T("ncg_detail_title"), expanded=False):
                st.caption(T("ncg_detail_cap") + "  ·  " + unit_note)
                _nwc_data = {
                    T("ncg_row_ar"):         {yr: mn(d["ar"])        for yr,d in annual.items()},
                    T("ncg_row_inv"):        {yr: mn(d["inv"])       for yr,d in annual.items()},
                    T("ncg_row_ap"):         {yr: mn(d["ap"])        for yr,d in annual.items()},
                    T("ncg_row_nwc"):        {yr: mn(d["nwc"])       for yr,d in annual.items()},
                    T("ncg_row_delta_nwc"):  {yr: mn(d["delta_nwc"]) for yr,d in annual.items()},
                }
                _fmt_nwc = {}
                for key, vals in _nwc_data.items():
                    _fmt_nwc[key] = {ano_lbl[yr]: f"{v:,.2f}" for yr, v in vals.items()}
                _df_nwc = pd.DataFrame(_fmt_nwc, index=[ano_lbl[yr] for yr in anos]).T
                _html_nwc = _df_nwc.style.to_html()
                st.markdown(f'<div class="df-styled">{_html_nwc}</div>', unsafe_allow_html=True)
                st.caption(T("ncg_detail_note"))

    with st.expander(T("df_bp"), expanded=False):
        st.caption(unit_note)
        _bp_data = {
            "Caixa e Equivalentes de Caixa": {yr: mn(balanco[yr]["Caixa"])                     for yr in anos},
            "Ativo Imobilizado Liquido":      {yr: mn(balanco[yr]["Ativo Imobilizado Liquido"]) for yr in anos},
        }
        _any_nwc_bal = any(abs(balanco[yr].get("NWC", 0)) > 1e-6 for yr in anos)
        if _any_nwc_bal:
            _bp_data["Capital de Giro Liquido (NWC)" if lang=="PT" else "Net Working Capital (NWC)"] = {
                yr: mn(balanco[yr].get("NWC", 0)) for yr in anos}
        _bp_data["Total Ativo"] = {yr: mn(balanco[yr]["Total Ativo"]) for yr in anos}
        _bp_data["Divida Total"] = {yr: mn(balanco[yr]["Divida Total"]) for yr in anos}
        _any_rev_bal = any(abs(balanco[yr].get("Revolver", 0)) > 1e-6 for yr in anos)
        if _any_rev_bal:
            _bp_data["Saldo do Revolver"] = {yr: mn(balanco[yr].get("Revolver", 0)) for yr in anos}
        _bp_data.update({
            "Capital Social":                {yr: mn(balanco[yr]["Capital Social"])            for yr in anos},
            "Lucros / Prejuizos Acumulados": {yr: mn(balanco[yr]["Lucros Acumulados"])         for yr in anos},
            "Total Patrimonio Liquido":      {yr: mn(balanco[yr]["Total PL"])                 for yr in anos},
            "Total Passivo + PL":            {yr: mn(balanco[yr]["Total Passivo + PL"])       for yr in anos},
        })
        _render_df(_bp_data)

    # ── Balance Sheet Check (assets vs liabilities + equity) ────────────────
    st.markdown(f"#### {T('bp_check_title')}")
    _bs_check_cols = st.columns(len(anos))
    for _ci, yr in enumerate(anos):
        ta_v  = balanco[yr]["Total Ativo"]
        tle_v = balanco[yr]["Total Passivo + PL"]
        diff  = ta_v - tle_v
        pct   = abs(diff) / ta_v * 100 if abs(ta_v) > 1e-9 else 0
        ok    = abs(diff) < max(abs(ta_v), 1.0) * 0.0001  # 0.01% tolerance
        _cls  = "metric-card metric-card-green" if ok else "metric-card metric-card-red"
        _icon = "✓" if ok else "✗"
        _html = (
            f'<div class="{_cls}">'
            f'<div class="mc-label">{ano_lbl[yr]}</div>'
            f'<div class="mc-value">{_icon} {mn(diff):,.2f}</div>'
            f'<div class="mc-delta">{pct:.4f}% {T("bp_check_assets")}</div>'
            f'</div>'
        )
        _bs_check_cols[_ci].markdown(_html, unsafe_allow_html=True)
    _all_ok = all(
        abs(balanco[yr]["Total Ativo"] - balanco[yr]["Total Passivo + PL"])
        < max(abs(balanco[yr]["Total Ativo"]), 1.0) * 0.0001
        for yr in anos
    )
    if _all_ok:
        st.success(f"✓  {T('bp_check_ok')}")
    else:
        st.error(f"✗  {T('bp_check_fail')}")

    # ── Three-statement Model Integrity Check ──────────────────────────────
    with st.expander(T("bp_integrity_title"), expanded=False):
        st.caption(T("bp_integrity_cap"))
        # (1) Cash on BP vs. cumulative CF (variacao_caixa + initial cash)
        _cf_cum = cash_bs  # already = initial + Σ variacao_caixa for last year
        _bp_cash_last = balanco[anos[-1]]["Caixa"]
        _chk1_ok = abs(_bp_cash_last - _cf_cum) < max(abs(_bp_cash_last), 1.0) * 0.0001

        # (2) Retained Earnings on BP = Σ NI from DRE
        _ni_sum = sum(annual[yr]["ni"] for yr in anos)
        _bp_re_last = balanco[anos[-1]]["Lucros Acumulados"]
        _chk2_ok = abs(_bp_re_last - _ni_sum) < max(abs(_bp_re_last), 1.0) * 0.0001

        # (3) Debt on BP = debt schedule balance
        _m_end_last = min(n_anos * 12, horizonte)
        _sched_debt_last = 0.0
        for _df_t in schedules.values():
            _rows_until = _df_t[_df_t["Mes"] <= _m_end_last]
            if not _rows_until.empty:
                _sched_debt_last += _rows_until.iloc[-1]["Saldo Final"]
        _bp_debt_last = balanco[anos[-1]]["Divida Total"]
        _chk3_ok = abs(_bp_debt_last - _sched_debt_last) < max(abs(_sched_debt_last), 1.0) * 0.0001

        def _chk_row(label, bs_val, src_val, ok):
            _cls = "metric-card metric-card-green" if ok else "metric-card metric-card-red"
            _icon = "✓" if ok else "✗"
            _status = T("bp_integrity_ok") if ok else T("bp_integrity_fail")
            return (
                f'<div class="{_cls}" style="text-align:left">'
                f'<div class="mc-label">{_icon} {label}</div>'
                f'<div class="mc-value" style="font-size:1.0rem">'
                f'BP: {mn(bs_val):,.2f} &nbsp;·&nbsp; '
                f'{"CF" if lang=="EN" else "DFC"}/{"IS" if lang=="EN" else "DRE"}: {mn(src_val):,.2f}'
                f'</div>'
                f'<div class="mc-delta">{_status} — Δ {mn(bs_val - src_val):+,.4f}</div>'
                f'</div>'
            )

        _ic1, _ic2, _ic3 = st.columns(3)
        _ic1.markdown(_chk_row(T("bp_integrity_cash"), _bp_cash_last, _cf_cum, _chk1_ok),
                      unsafe_allow_html=True)
        _ic2.markdown(_chk_row(T("bp_integrity_re"),   _bp_re_last,  _ni_sum, _chk2_ok),
                      unsafe_allow_html=True)
        _ic3.markdown(_chk_row(T("bp_integrity_debt"), _bp_debt_last, _sched_debt_last, _chk3_ok),
                      unsafe_allow_html=True)

    # Financial ratios table (DSCR, ICR, Debt/EBITDA)
    if total_debt > 0:
        with st.expander(T("df_ratios"), expanded=False):
            st.caption(T("df_ratios_cap"))
            _ratios_data = {}
            _ratios_data["DSCR (x)"] = {yr: f"{v:.2f}" if v != float('inf') else "—"
                                         for yr, v in dscr_anual.items()}
            _ratios_data["ICR (x)"] = {yr: f"{v:.2f}" if v != float('inf') else "—"
                                        for yr, v in icr_anual.items()}
            _ratios_data[T("df_ratio_debt_ebitda")] = {
                yr: f"{v:.2f}" if v != float('inf') else "—"
                for yr, v in divida_ebitda_anual.items()}
            if lang == "EN":
                _ratio_cols = {yr: yr.replace("Ano", "Year") for yr in anos}
            else:
                _ratio_cols = {yr: yr for yr in anos}
            df_ratios = pd.DataFrame(_ratios_data, index=[_ratio_cols[yr] for yr in anos]).T
            st.dataframe(df_ratios, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ABA 6 — ANALISE DE SENSIBILIDADE
# ─────────────────────────────────────────────────────────────────────────────
if "sens_tables" not in st.session_state: st.session_state["sens_tables"] = []
if "sc_results"  not in st.session_state: st.session_state["sc_results"]  = None
if "tn_data"     not in st.session_state: st.session_state["tn_data"]     = None
if "ff_data"     not in st.session_state: st.session_state["ff_data"]     = None

# Active sensitivity variable dict (display_name → internal_key)
sens_vars_active = SENS_VARS_EN if lang == "EN" else SENS_VARS
sens_vars_list   = list(sens_vars_active.keys())

# Metrics — PT strings stored internally; translated for display
sens_metrics = ["NPV (R$)", "ROI (%)", "Payback (meses)", "Margem Bruta Media (%)"]
sens_metric_fmt = lambda x: (_METRIC_EN.get(x, x) if lang == "EN" else x)

def _sv_base(key):
    if key == "cresc_rec":   return round(sum(x["crescimento"] for x in receitas) / max(len(receitas), 1), 1)
    if key == "taxa_desc_v": return taxa_desc
    if key == "ipca_v":      return ipca_ref
    return 0.0

def _sv_preview(vals, is_abs):
    fmt = (lambda v: f"{v:.1f}%") if is_abs else (lambda v: f"{v:+.0f}%")
    return "  →  ".join(fmt(v) for v in vals)

with tab_sens:
    st.subheader(T("sv_title"))

    # ── 5-view toggle ─────────────────────────────────────────────────────────
    _SV_VIEWS = ["table", "scenario", "tornado", "football", "montecarlo"]
    sv_view = st.segmented_control(
        "sv_view_sel", _SV_VIEWS,
        format_func=lambda x: T(f"sv_view_{x}"),
        key="sv_view_sel", default="table",
        label_visibility="collapsed")
    sv_view = sv_view or "table"
    st.divider()

    # ── helpers shared across views ───────────────────────────────────────────
    def _get_metric_val(npv_c, roi_c, pb_c, mg_c, metric):
        if metric == "NPV (R$)":           return round(npv_c / umult, 2)
        if metric == "ROI (%)":             return round(roi_c, 1)
        if metric == "Payback (meses)":     return float(pb_c) if pb_c else float(horizonte + 1)
        return round(mg_c, 1)

    def _fmt_metric(val, metric, h=horizonte, u=unit):
        if metric == "Payback (meses)":
            return (T("sv_sc_pb_na") if val >= h + 1 else f"{int(round(val))} m")
        if metric == "NPV (R$)": return f"{val:,.1f} ({u})"
        return f"{val:.1f}%"

    # base-case run (no variable changes)
    _base_metrics = run_sens_case(
        receitas, cpvs, opexs, capex_lines, horizonte,
        taxa_desc, ipca_ref, igpm_ref, "__noop__", 0, "__noop__", 0)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW 1 — TABELA DE SENSIBILIDADE
    # ══════════════════════════════════════════════════════════════════════════
    if sv_view == "table":
        # ── Linha de controles ──────────────────────────────────────────────
        _cm, _cs, _cc = st.columns([3, 2, 2])
        metric_sel = _cm.selectbox(T("sv_metrica"), sens_metrics,
                                   format_func=sens_metric_fmt, key="smet")
        n_steps    = _cs.slider(T("sv_pontos"), 3, 9, 5, step=2, key="ssteps")
        with _cc:
            st.write("")
            calc_btn = st.button(T("sv_calcular"), type="primary", use_container_width=True)
            if st.button(T("sv_limpar"), use_container_width=True):
                st.session_state["sens_tables"] = []
                st.rerun()
        st.divider()

        # ── Variavel Y ───────────────────────────────────────────────────────
        _yla, _yva, _yfa, _yta = st.columns([1.4, 3.5, 1.2, 1.2])
        with _yva: v1_name = st.selectbox(T("sv_eixo_y"), sens_vars_list, index=0, key="sv1")
        v1_key = sens_vars_active[v1_name]; v1_abs = v1_key in SENS_ABS; b1 = _sv_base(v1_key)
        with _yla:
            st.markdown(f"**{T('sv_eixo_y')}**")
            st.caption("% a.a." if v1_abs else "+/- %")
        if v1_abs:
            v1_min = _yfa.number_input(T("sv_de"), value=round(max(b1*0.4,0.5),1), format="%.1f", step=0.5, key=f"sv1_min_{v1_key}")
            v1_max = _yta.number_input(T("sv_ate"), value=round(b1*2.0,1), format="%.1f", step=0.5, key=f"sv1_max_{v1_key}")
        else:
            v1_min = _yfa.number_input(T("sv_de_pct"), value=-40.0, step=5.0, format="%.0f", key=f"sv1_min_{v1_key}")
            v1_max = _yta.number_input(T("sv_ate_pct"), value=40.0, step=5.0, format="%.0f", key=f"sv1_max_{v1_key}")

        # ── Variavel X ───────────────────────────────────────────────────────
        _xla, _xva, _xfa, _xta = st.columns([1.4, 3.5, 1.2, 1.2])
        with _xva: v2_name = st.selectbox(T("sv_eixo_x"), sens_vars_list, index=1, key="sv2")
        v2_key = sens_vars_active[v2_name]; v2_abs = v2_key in SENS_ABS; b2 = _sv_base(v2_key)
        with _xla:
            st.markdown(f"**{T('sv_eixo_x')}**")
            st.caption("% a.a." if v2_abs else "+/- %")
        if v2_abs:
            v2_min = _xfa.number_input(T("sv_de"), value=round(max(b2*0.4,0.5),1), format="%.1f", step=0.5, key=f"sv2_min_{v2_key}")
            v2_max = _xta.number_input(T("sv_ate"), value=round(b2*2.0,1), format="%.1f", step=0.5, key=f"sv2_max_{v2_key}")
        else:
            v2_min = _xfa.number_input(T("sv_de_pct"), value=-40.0, step=5.0, format="%.0f", key=f"sv2_min_{v2_key}")
            v2_max = _xta.number_input(T("sv_ate_pct"), value=40.0, step=5.0, format="%.0f", key=f"sv2_max_{v2_key}")

        # ── Validacoes ───────────────────────────────────────────────────────
        erros = []
        if v1_name == v2_name:      erros.append(T("sv_erro_vars"))
        if v1_min >= v1_max:        erros.append(T("sv_erro_v1_range"))
        if v2_min >= v2_max:        erros.append(T("sv_erro_v2_range"))
        if erros:
            for e in erros: st.warning(e)
        else:
            n = int(n_steps)
            v1_vals = [v1_min+(v1_max-v1_min)*i/(n-1) for i in range(n)] if n>1 else [v1_min]
            v2_vals = [v2_min+(v2_max-v2_min)*i/(n-1) for i in range(n)] if n>1 else [v2_min]
            if calc_btn:
                with st.spinner(T("sv_calculando")):
                    try:
                        table_data = {}
                        for v1v in v1_vals:
                            row = {}
                            for v2v in v2_vals:
                                res = run_sens_case(receitas,cpvs,opexs,capex_lines,horizonte,
                                                    taxa_desc,ipca_ref,igpm_ref,v1_key,v1v,v2_key,v2v)
                                val = _get_metric_val(*res, metric_sel)
                                row[f"{v2v:.1f}%" if v2_abs else f"{v2v:+.0f}%"] = val
                            table_data[f"{v1v:.1f}%" if v1_abs else f"{v1v:+.0f}%"] = row
                        df_sens = pd.DataFrame(table_data).T
                        df_sens.index.name = v1_name; df_sens.columns.name = v2_name
                        entry = {"df":df_sens,"metric":metric_sel,"v1":v1_name,"v2":v2_name,
                                 "unit":unit,"horizonte":horizonte}
                        st.session_state["sens_tables"].append(entry)
                        if len(st.session_state["sens_tables"])>5: st.session_state["sens_tables"].pop(0)
                    except Exception as ex: st.error(T("sv_erro_calc").format(e=ex))

        # ── Exibicao ─────────────────────────────────────────────────────────
        st.divider()
        total_t = len(st.session_state["sens_tables"])
        if total_t == 0:
            st.info(T("sv_nenhuma_tabela"))
        else:
            st.caption(T("sv_n_tabelas").format(n=total_t))
            for idx, t in enumerate(reversed(st.session_state["sens_tables"])):
                num = total_t - idx
                metric_disp = _METRIC_EN.get(t["metric"],t["metric"]) if lang=="EN" else t["metric"]
                with st.expander(T("sv_tabela_lbl").format(n=num,m=metric_disp), expanded=(idx==0)):
                    df_t=t["df"]; h=t["horizonte"]; u=t["unit"]
                    if t["metric"]=="Payback (meses)":
                        num_df=df_t.where(df_t<h+1,h+1)
                        fmt_fn=lambda v,_h=h: "N/A" if v>=_h+1 else f"{int(round(v))} m"
                        rev=True
                    elif t["metric"]=="NPV (R$)":
                        num_df=df_t; fmt_fn=lambda v: f"{v:,.1f}"; rev=False
                    else:
                        num_df=df_t; fmt_fn=lambda v: f"{v:.1f}%"; rev=False
                    heat_styles=_heatmap_styles(num_df,reverse=rev)
                    html_tbl=(df_t.rename_axis(index=None,columns=None).style
                              .apply(lambda _:heat_styles,axis=None).format(fmt_fn).to_html())
                    v1_lbl=t["v1"]; v2_lbl=t["v2"]
                    unit_lbl=f"({u})" if t["metric"]=="NPV (R$)" else ""
                    st.markdown(f"""
<div style="margin-bottom:4px"><span style="font-size:.78rem;color:#6b7280;font-weight:600;
text-transform:uppercase;letter-spacing:.04em">{T("sv_metrica_lbl").format(m=metric_disp,u=unit_lbl)}</span></div>
<div style="text-align:center;font-size:.8rem;font-weight:700;color:#1a56db;margin-bottom:2px">
  ← &nbsp;{v2_lbl}&nbsp; →</div>
<div style="display:flex;align-items:center;gap:6px">
  <div style="writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;
  font-size:.8rem;font-weight:700;color:#1a56db;text-align:center;min-width:18px">
    ↑ &nbsp;{v1_lbl}&nbsp; ↓</div>
  <div class="sens-tbl" style="flex:1;min-width:0">{html_tbl}</div></div>""",
                        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW 2 — ANALISE DE CENARIOS
    # ══════════════════════════════════════════════════════════════════════════
    elif sv_view == "scenario":
        _base_cresc = round(sum(x["crescimento"] for x in receitas)/max(len(receitas),1),1)

        # ── Configuracao dos cenarios ────────────────────────────────────────
        _sc_col_a, _sc_col_b = st.columns([1,4])
        n_sc = _sc_col_a.slider(T("sv_sc_n"), 2, 5, int(get("sc_n",3)), key="sc_n")

        _sc_names_default = (["Pessimista","Base","Otimista","Agressivo","Conservador"]
                              if lang=="PT" else
                              ["Bear","Base","Bull","Aggressive","Conservative"])
        _sc_rec_var_def   = [-20.0, 0.0, 20.0, 40.0, -35.0]
        _sc_cresc_def     = [max(_base_cresc*0.6,1.0), _base_cresc, _base_cresc*1.4,
                             _base_cresc*1.8, _base_cresc*0.4]
        _sc_cpv_def       = [15.0, 0.0, -10.0, -15.0, 20.0]
        _sc_opex_def      = [10.0, 0.0, -5.0,  -10.0, 15.0]

        sc_cols = st.columns(n_sc)
        for si, col in enumerate(sc_cols):
            with col:
                st.markdown(f"<div class='linha-hdr'>Cenario {si+1}</div>", unsafe_allow_html=True)
                col.text_input(T("sv_sc_nome"), key=f"sc_nome_{si}",
                               value=get(f"sc_nome_{si}", "") or _sc_names_default[si],
                               label_visibility="visible")
                col.number_input(T("sv_sc_rec_var"),  -80.0, 150.0,
                                 float(get(f"sc_rec_var_{si}",  _sc_rec_var_def[si])), 5.0,
                                 format="%.0f", key=f"sc_rec_var_{si}")
                col.number_input(T("sv_sc_cresc"), 0.0, 200.0,
                                 float(get(f"sc_cresc_{si}", round(_sc_cresc_def[si],1))), 1.0,
                                 format="%.1f", key=f"sc_cresc_{si}")
                col.number_input(T("sv_sc_cpv_var"),  -50.0, 100.0,
                                 float(get(f"sc_cpv_var_{si}",  _sc_cpv_def[si])), 5.0,
                                 format="%.0f", key=f"sc_cpv_var_{si}")
                col.number_input(T("sv_sc_opex_var"), -50.0, 100.0,
                                 float(get(f"sc_opex_var_{si}", _sc_opex_def[si])), 5.0,
                                 format="%.0f", key=f"sc_opex_var_{si}")

        _sc_metric = st.selectbox(T("sv_sc_metrica"), sens_metrics,
                                  format_func=sens_metric_fmt, key="sc_metric")
        _sc_btn = st.button(T("sv_sc_calcular"), type="primary")
        st.divider()

        if _sc_btn:
            with st.spinner(T("sv_calculando")):
                sc_results = []
                for si in range(n_sc):
                    nome_sc = get(f"sc_nome_{si}", _sc_names_default[si]) or f"C{si+1}"
                    # Apply all 4 variables simultaneously via run_sens_multi
                    _rfull = run_sens_multi(
                        receitas, cpvs, opexs, capex_lines, horizonte,
                        taxa_desc, ipca_ref, igpm_ref,
                        [("rec_var",   float(get(f"sc_rec_var_{si}",  0.0))),
                         ("cresc_rec", float(get(f"sc_cresc_{si}",    _base_cresc))),
                         ("cpv_var",   float(get(f"sc_cpv_var_{si}",  0.0))),
                         ("opex_var",  float(get(f"sc_opex_var_{si}", 0.0)))])
                    sc_results.append({
                        "nome": nome_sc,
                        "npv":  _rfull[0], "roi": _rfull[1],
                        "pb":   _rfull[2], "mg":  _rfull[3],
                    })
                st.session_state["sc_results"] = sc_results

        if st.session_state.get("sc_results"):
            res_list = st.session_state["sc_results"]
            # Comparison table
            rows_table = {}
            pb_lbl = ("Payback (meses)" if lang=="PT" else "Payback (months)")
            npv_lbl = f"NPV ({unit})"; roi_lbl = "ROI (%)"; mg_lbl = "Margem Bruta (%)" if lang=="PT" else "Gross Margin (%)"
            for r in res_list:
                rows_table[r["nome"]] = {
                    npv_lbl: f"{r['npv']/umult:,.1f}",
                    roi_lbl: f"{r['roi']:.1f}%",
                    pb_lbl:  (T("sv_sc_pb_na") if r["pb"] is None else f"{r['pb']} m"),
                    mg_lbl:  f"{r['mg']:.1f}%",
                }
            df_sc = pd.DataFrame(rows_table).T
            df_sc.index.name = ""
            st.dataframe(df_sc, use_container_width=True)

            # Bar chart for selected metric
            _sc_m = _sc_metric
            sc_vals  = []
            sc_names = []
            for r in res_list:
                sc_names.append(r["nome"])
                if _sc_m == "NPV (R$)":            sc_vals.append(round(r["npv"]/umult,2))
                elif _sc_m == "ROI (%)":            sc_vals.append(round(r["roi"],1))
                elif _sc_m == "Payback (meses)":    sc_vals.append(r["pb"] if r["pb"] else horizonte+1)
                else:                               sc_vals.append(round(r["mg"],1))
            colors = ["#f97316" if v == min(sc_vals) else "#16a34a" if v == max(sc_vals)
                      else "#1a56db" for v in sc_vals]
            if _sc_m == "Payback (meses)": colors = ["#f97316" if v==max(sc_vals) else "#16a34a" if v==min(sc_vals) else "#1a56db" for v in sc_vals]
            fig_sc = go.Figure(go.Bar(x=sc_names, y=sc_vals, marker_color=colors,
                                      text=[_fmt_metric(v, _sc_m) for v in sc_vals],
                                      textposition="outside"))
            m_disp = _METRIC_EN.get(_sc_m, _sc_m) if lang=="EN" else _sc_m
            fig_sc.update_layout(yaxis_title=m_disp, height=380, showlegend=False,
                                  margin=dict(t=30,b=10))
            st.plotly_chart(fig_sc, use_container_width=True)
        else:
            st.info(T("sv_sc_empty"))

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW 3 — TORNADO CHART
    # ══════════════════════════════════════════════════════════════════════════
    elif sv_view == "tornado":
        _tc1, _tc2, _tc3 = st.columns([3, 2, 2])
        tn_metric = _tc1.selectbox(T("sv_metrica"), sens_metrics,
                                   format_func=sens_metric_fmt, key="tn_metric")
        tn_range  = _tc2.slider(T("sv_tn_range") if False else ("+/- %" if lang=="EN" else "+/- %"),
                                5, 50, 20, step=5, key="tn_range")
        with _tc3:
            st.write("")
            tn_btn = st.button(T("sv_tn_calcular"), type="primary", use_container_width=True)
        st.caption(T("sv_tn_range"))
        st.divider()

        if tn_btn:
            with st.spinner(T("sv_calculando")):
                base_val = _get_metric_val(*_base_metrics, tn_metric)
                tn_data = []
                for vname, vkey in sens_vars_active.items():
                    b = _sv_base(vkey)
                    is_abs = vkey in SENS_ABS
                    if is_abs:
                        low_v  = max(b - tn_range * b / 100, 0.1)
                        high_v = b + tn_range * b / 100
                    else:
                        low_v  = -float(tn_range)
                        high_v =  float(tn_range)
                    r_lo = run_sens_case(receitas,cpvs,opexs,capex_lines,horizonte,
                                         taxa_desc,ipca_ref,igpm_ref,vkey,low_v,"__noop__",0)
                    r_hi = run_sens_case(receitas,cpvs,opexs,capex_lines,horizonte,
                                         taxa_desc,ipca_ref,igpm_ref,vkey,high_v,"__noop__",0)
                    m_lo = _get_metric_val(*r_lo, tn_metric)
                    m_hi = _get_metric_val(*r_hi, tn_metric)
                    tn_data.append({"var":vname,"lo":m_lo,"hi":m_hi,"impact":abs(m_hi-m_lo)})
                tn_data.sort(key=lambda x: x["impact"])
                st.session_state["tn_data"]   = tn_data
                st.session_state["tn_metric"] = tn_metric
                st.session_state["tn_base"]   = base_val

        if st.session_state.get("tn_data"):
            tn_data   = st.session_state["tn_data"]
            tn_metric = st.session_state.get("tn_metric", "NPV (R$)")
            base_val  = st.session_state.get("tn_base", 0)
            m_disp = _METRIC_EN.get(tn_metric, tn_metric) if lang=="EN" else tn_metric

            fig_tn = go.Figure()
            for d in tn_data:
                lo_rel = d["lo"] - base_val
                hi_rel = d["hi"] - base_val
                lo_min = min(lo_rel, hi_rel)
                span   = abs(hi_rel - lo_rel)
                col_lo = "#f97316" if d["lo"] < base_val else "#16a34a"
                col_hi = "#16a34a" if d["hi"] > base_val else "#f97316"
                # upside bar
                fig_tn.add_trace(go.Bar(
                    x=[max(hi_rel, lo_rel)], y=[d["var"]], orientation="h",
                    base=[0], marker_color="#16a34a", opacity=0.85,
                    name=T("sv_tn_alto"), showlegend=(d == tn_data[-1]),
                    hovertemplate=f"{d['var']}<br>{T('sv_tn_alto')}: {_fmt_metric(d['hi'],tn_metric)}<extra></extra>"))
                # downside bar
                fig_tn.add_trace(go.Bar(
                    x=[min(hi_rel, lo_rel)], y=[d["var"]], orientation="h",
                    base=[0], marker_color="#f97316", opacity=0.85,
                    name=T("sv_tn_baixo"), showlegend=(d == tn_data[-1]),
                    hovertemplate=f"{d['var']}<br>{T('sv_tn_baixo')}: {_fmt_metric(d['lo'],tn_metric)}<extra></extra>"))
            fig_tn.add_vline(x=0, line_dash="dash", line_color="#374151", line_width=2,
                             annotation_text=f"{T('sv_tn_base')}: {_fmt_metric(base_val,tn_metric)}",
                             annotation_position="top")
            fig_tn.update_layout(
                barmode="overlay", height=max(320, len(tn_data)*52),
                xaxis_title=f"{m_disp} ({T('sv_tn_impacto')} vs. Base)",
                yaxis=dict(autorange=True),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                margin=dict(t=40, l=10))
            st.plotly_chart(fig_tn, use_container_width=True)
        else:
            st.info(T("sv_tn_empty"))

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW 4 — FOOTBALL FIELD CHART
    # ══════════════════════════════════════════════════════════════════════════
    elif sv_view == "football":
        _fc1, _fc2, _fc3 = st.columns([3, 2, 2])
        ff_metric = _fc1.selectbox(T("sv_metrica"), sens_metrics,
                                   format_func=sens_metric_fmt, key="ff_metric")
        ff_range  = _fc2.slider("+/- %", 5, 50, 20, step=5, key="ff_range")
        with _fc3:
            st.write("")
            ff_btn = st.button(T("sv_tn_calcular"), type="primary", use_container_width=True, key="ff_btn")
        st.caption(T("sv_tn_range"))
        st.divider()

        if ff_btn:
            with st.spinner(T("sv_calculando")):
                base_val = _get_metric_val(*_base_metrics, ff_metric)
                ff_data = []
                for vname, vkey in sens_vars_active.items():
                    b = _sv_base(vkey)
                    is_abs = vkey in SENS_ABS
                    if is_abs:
                        low_v  = max(b - ff_range * b / 100, 0.1)
                        high_v = b + ff_range * b / 100
                    else:
                        low_v  = -float(ff_range)
                        high_v =  float(ff_range)
                    r_lo = run_sens_case(receitas,cpvs,opexs,capex_lines,horizonte,
                                         taxa_desc,ipca_ref,igpm_ref,vkey,low_v,"__noop__",0)
                    r_hi = run_sens_case(receitas,cpvs,opexs,capex_lines,horizonte,
                                         taxa_desc,ipca_ref,igpm_ref,vkey,high_v,"__noop__",0)
                    m_lo = _get_metric_val(*r_lo, ff_metric)
                    m_hi = _get_metric_val(*r_hi, ff_metric)
                    ff_data.append({"var":vname,"lo":min(m_lo,m_hi),"hi":max(m_lo,m_hi),"impact":abs(m_hi-m_lo)})
                ff_data.sort(key=lambda x: x["impact"])
                st.session_state["ff_data"]   = ff_data
                st.session_state["ff_metric"] = ff_metric
                st.session_state["ff_base"]   = base_val

        if st.session_state.get("ff_data"):
            ff_data   = st.session_state["ff_data"]
            ff_metric = st.session_state.get("ff_metric", "NPV (R$)")
            base_val  = st.session_state.get("ff_base", 0)
            m_disp = _METRIC_EN.get(ff_metric, ff_metric) if lang=="EN" else ff_metric

            fig_ff = go.Figure()
            for d in ff_data:
                span = d["hi"] - d["lo"]
                fig_ff.add_trace(go.Bar(
                    x=[span], y=[d["var"]], base=[d["lo"]],
                    orientation="h", marker_color="#1a56db", opacity=0.75,
                    showlegend=False,
                    hovertemplate=(f"{d['var']}<br>"
                                   f"{T('sv_tn_baixo')}: {_fmt_metric(d['lo'],ff_metric)}<br>"
                                   f"{T('sv_tn_alto')}: {_fmt_metric(d['hi'],ff_metric)}"
                                   "<extra></extra>")))
            fig_ff.add_vline(x=base_val, line_dash="dash", line_color="#dc2626", line_width=2.5,
                             annotation_text=f"{T('sv_tn_base')}: {_fmt_metric(base_val,ff_metric)}",
                             annotation_position="top")
            fig_ff.update_layout(
                height=max(320, len(ff_data)*52),
                xaxis_title=m_disp,
                yaxis=dict(autorange=True),
                margin=dict(t=40, l=10))
            st.plotly_chart(fig_ff, use_container_width=True)
        else:
            st.info(T("sv_tn_empty"))

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW 5 — MONTE CARLO SIMULATION
    # ══════════════════════════════════════════════════════════════════════════
    else:  # montecarlo
        st.caption(T("sv_mc_cap"))
        if "mc_data" not in st.session_state:
            st.session_state["mc_data"] = None

        _mc1, _mc2 = st.columns([3, 2])
        mc_sims = _mc1.slider(T("sv_mc_nsims"), 100, 5000, 1000, step=100, key="mc_nsims")
        mc_seed = _mc2.number_input("Seed", value=42, step=1, key="mc_seed")

        st.markdown(f"**{T('sv_mc_std_title')}**")
        _mca, _mcb, _mcc = st.columns(3)
        mc_rec_std  = _mca.slider(T("sv_mc_rec_std"),  1.0, 50.0, 15.0, 1.0, key="mc_rec_std")
        mc_cpv_std  = _mcb.slider(T("sv_mc_cpv_std"),  1.0, 50.0, 10.0, 1.0, key="mc_cpv_std")
        mc_opex_std = _mcc.slider(T("sv_mc_opex_std"), 1.0, 50.0, 10.0, 1.0, key="mc_opex_std")
        _mcd, _mce, _ = st.columns(3)
        mc_cresc_std = _mcd.slider(T("sv_mc_cresc_std"), 0.5, 20.0, 5.0, 0.5, key="mc_cresc_std")
        mc_td_std    = _mce.slider(T("sv_mc_td_std"),    0.5, 10.0, 2.0, 0.5, key="mc_td_std")

        mc_btn = st.button(T("sv_mc_run"), type="primary")
        st.divider()

        if mc_btn:
            with st.spinner(T("sv_calculando")):
                mc_res = monte_carlo(
                    receitas, cpvs, opexs, capex_lines, horizonte,
                    taxa_desc, ipca_ref, igpm_ref,
                    n_sims=mc_sims, seed=mc_seed,
                    rec_std=mc_rec_std, cpv_std=mc_cpv_std, opex_std=mc_opex_std,
                    cresc_std=mc_cresc_std, taxa_desc_std=mc_td_std)
                mc_stats = monte_carlo_stats(mc_res)
                st.session_state["mc_data"] = {"results": mc_res, "stats": mc_stats}

        if st.session_state.get("mc_data"):
            mc = st.session_state["mc_data"]
            mc_res = mc["results"]
            mc_stats = mc["stats"]

            # Summary stats cards
            _s1, _s2, _s3, _s4 = st.columns(4)
            _npv_s = mc_stats["npv"]
            _s1.markdown(_metric_card(
                f"NPV {T('sv_mc_median')}",
                f"{_npv_s['median']/umult:,.1f} ({unit})",
                _npv_s["median"] > 0), unsafe_allow_html=True)
            _s2.markdown(_metric_card(
                f"NPV P5–P95",
                f"{_npv_s['p5']/umult:,.0f} ~ {_npv_s['p95']/umult:,.0f}"),
                unsafe_allow_html=True)
            _roi_s = mc_stats["roi"]
            _s3.markdown(_metric_card(
                f"ROI {T('sv_mc_median')}",
                f"{_roi_s['median']:.0f}%",
                _roi_s["median"] > 0), unsafe_allow_html=True)
            _pb_s = mc_stats["payback"]
            _pb_med = _pb_s["median"]
            _s4.markdown(_metric_card(
                f"Payback {T('sv_mc_median')}",
                f"{_pb_med:.0f} {'meses' if lang=='PT' else 'mo'}" if _pb_med <= horizonte else "N/A",
                _pb_med <= horizonte), unsafe_allow_html=True)

            # Probability of positive NPV
            _npv_arr = mc_res["npv"]
            _prob_pos = sum(1 for v in _npv_arr if v > 0) / len(_npv_arr) * 100
            st.markdown(f"**{T('sv_mc_prob_npv')}: {_prob_pos:.1f}%**")
            st.divider()

            # Distribution charts
            _mc_tab1, _mc_tab2, _mc_tab3 = st.tabs(["NPV", "ROI (%)", "Payback"])
            with _mc_tab1:
                fig_mc = go.Figure()
                fig_mc.add_trace(go.Histogram(
                    x=[v/umult for v in mc_res["npv"]], nbinsx=50,
                    marker_color="#1a56db", opacity=0.8, name="NPV"))
                fig_mc.add_vline(x=0, line_dash="dash", line_color="#dc2626", line_width=2,
                                 annotation_text="NPV=0")
                fig_mc.add_vline(x=_npv_s["median"]/umult, line_dash="dot",
                                 line_color="#16a34a", line_width=2,
                                 annotation_text=f"Median: {_npv_s['median']/umult:,.0f}")
                fig_mc.update_layout(
                    xaxis_title=f"NPV ({unit})", yaxis_title=T("sv_mc_freq"),
                    height=400, showlegend=False)
                st.plotly_chart(fig_mc, use_container_width=True)

            with _mc_tab2:
                fig_roi = go.Figure()
                fig_roi.add_trace(go.Histogram(
                    x=mc_res["roi"], nbinsx=50,
                    marker_color="#16a34a", opacity=0.8, name="ROI"))
                fig_roi.add_vline(x=0, line_dash="dash", line_color="#dc2626", line_width=2)
                fig_roi.update_layout(
                    xaxis_title="ROI (%)", yaxis_title=T("sv_mc_freq"),
                    height=400, showlegend=False)
                st.plotly_chart(fig_roi, use_container_width=True)

            with _mc_tab3:
                _pb_vals = [v for v in mc_res["payback"] if v <= horizonte]
                fig_pb = go.Figure()
                fig_pb.add_trace(go.Histogram(
                    x=_pb_vals, nbinsx=30,
                    marker_color="#f97316", opacity=0.8, name="Payback"))
                fig_pb.update_layout(
                    xaxis_title=f"Payback ({'meses' if lang=='PT' else 'months'})",
                    yaxis_title=T("sv_mc_freq"),
                    height=400, showlegend=False)
                st.plotly_chart(fig_pb, use_container_width=True)

            # Percentile table
            st.markdown(f"**{T('sv_mc_percentiles')}**")
            pct_data = {}
            for key, label in [("npv", f"NPV ({unit})"), ("roi", "ROI (%)"),
                                ("payback", f"Payback ({'meses' if lang=='PT' else 'mo'})"),
                                ("margem", f"{'Margem Bruta' if lang=='PT' else 'Gross Margin'} (%)")]:
                s = mc_stats[key]
                pct_data[label] = {
                    "P5": f"{s['p5']/umult:,.1f}" if key == "npv" else f"{s['p5']:.1f}",
                    "P25": f"{s['p25']/umult:,.1f}" if key == "npv" else f"{s['p25']:.1f}",
                    T("sv_mc_median"): f"{s['median']/umult:,.1f}" if key == "npv" else f"{s['median']:.1f}",
                    "P75": f"{s['p75']/umult:,.1f}" if key == "npv" else f"{s['p75']:.1f}",
                    "P95": f"{s['p95']/umult:,.1f}" if key == "npv" else f"{s['p95']:.1f}",
                }
            st.dataframe(pd.DataFrame(pct_data).T, use_container_width=True)
        else:
            st.info(T("sv_mc_empty"))

# ─────────────────────────────────────────────────────────────────────────────
# ABA 7 — SLIDES DECK
# ─────────────────────────────────────────────────────────────────────────────
with tab_slides:
    _SL = SLIDE_TRANSLATIONS[lang]
    st.subheader("Slides Deck")
    st.caption(
        "Generate a presentation deck from your model data." if lang == "EN" else
        "Gere um deck de apresentacao a partir dos dados do modelo."
    )
    st.divider()

    _sd1, _sd2, _sd3 = st.columns(3)
    _sd1.metric("Projeto" if lang=="PT" else "Project",
                nome_proj if nome_proj else "—")
    _sd2.metric("Setor" if lang=="PT" else "Sector", fmt_opt(setor))
    try:
        _dt_obj = _dt.date.fromisoformat(str(data_inicio_str))
        _dt_disp = _dt_obj.strftime("%d/%m/%Y")
    except Exception:
        _dt_disp = str(data_inicio_str)
    _sd3.metric("Inicio" if lang=="PT" else "Start", _dt_disp)

    st.markdown("---")

    _sl_slide_names = [
        _SL["slide_exec_title"], _SL["slide_assumptions_title"],
        _SL["slide_cashflow_title"], _SL["slide_rev_cost_title"],
        _SL["slide_dre_title"], _SL["slide_debt_title"],
        _SL["slide_sens_title"], _SL["slide_appendix_title"],
    ]
    _sl_info_md = " · ".join(f"**{i+1}.** {s}" for i, s in enumerate(_sl_slide_names))
    st.caption(f"Slides: Capa · {_sl_info_md}")
    st.divider()

    if st.button(_SL["slide_download"], type="primary", use_container_width=True):
        with st.spinner(_SL["slide_generating"]):
            # Build Plotly figures for export
            _fig_cf = go.Figure()
            _fig_cf.add_trace(go.Scatter(
                x=df_op["Mes"].tolist(), y=(df_op["Acumulado"]/umult).tolist(),
                mode="lines", name=T("g_fcf_proj"), line=dict(color="#1a56db", width=2.5)))
            if total_debt > 0:
                _fig_cf.add_trace(go.Scatter(
                    x=df_op["Mes"].tolist(), y=(df_lev["Acumulado Levered"]/umult).tolist(),
                    mode="lines", name=T("g_fcf_eq"), line=dict(color="#16a34a", width=2, dash="dot")))
            _fig_cf.add_hline(y=0, line_dash="dash", line_color="#9ca3af")
            _fig_cf.update_layout(xaxis_title=T("g_xaxis_mes"), yaxis_title=unit,
                                   hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02))
            _fig_cf.update_yaxes(tickformat=",.1f")

            _fig_rc = go.Figure()
            for col, cor, nm in [("Receita","#1a56db",T("g_receita")),("CPV","#f97316",T("g_cpv"))]:
                _fig_rc.add_trace(go.Scatter(x=df_op["Mes"].tolist(), y=(df_op[col]/umult).tolist(),
                                              mode="lines", name=nm, line=dict(color=cor, width=2)))
            _fig_rc.add_trace(go.Scatter(x=df_op["Mes"].tolist(),
                                          y=((df_op["OpEx"]+df_op["G&A"])/umult).tolist(),
                                          mode="lines", name=T("g_opex_ga"),
                                          line=dict(color="#dc2626", width=2)))
            _fig_rc.update_layout(xaxis_title=T("g_xaxis_mes"), yaxis_title=unit,
                                   hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02))
            _fig_rc.update_yaxes(tickformat=",.1f")

            # Tornado figure (if available)
            _fig_tn = None
            if st.session_state.get("tn_data"):
                tn_d = st.session_state["tn_data"]
                tn_base = st.session_state.get("tn_base", 0)
                _fig_tn = go.Figure()
                for d in tn_d:
                    lo_rel = d["lo"] - tn_base
                    hi_rel = d["hi"] - tn_base
                    _fig_tn.add_trace(go.Bar(x=[max(hi_rel, lo_rel)], y=[d["var"]],
                                              orientation="h", base=[0], marker_color="#16a34a", opacity=0.85,
                                              showlegend=False))
                    _fig_tn.add_trace(go.Bar(x=[min(hi_rel, lo_rel)], y=[d["var"]],
                                              orientation="h", base=[0], marker_color="#f97316", opacity=0.85,
                                              showlegend=False))
                _fig_tn.add_vline(x=0, line_dash="dash", line_color="#374151", line_width=2)
                _fig_tn.update_layout(barmode="overlay", yaxis=dict(autorange=True))

            # Debt figure
            _fig_dbt = None
            if total_debt > 0 and any(not df_t.empty for df_t in schedules.values()):
                _meses_dv = list(range(1, horizonte+1))
                _fig_dbt = go.Figure()
                _cores = ["#1a56db","#16a34a","#f97316","#dc2626","#7c3aed","#0891b2"]
                for ii, (nt, dt) in enumerate(schedules.items()):
                    _cr = _cores[ii % len(_cores)]
                    _as = pd.Series(0.0, index=_meses_dv)
                    _js = pd.Series(0.0, index=_meses_dv)
                    if not dt.empty:
                        _vl = dt[dt["Mes"].between(1, horizonte)]
                        if not _vl.empty:
                            _gr = _vl.groupby("Mes").agg({"Amortizacao":"sum","Juros Pagos":"sum"})
                            _as = _as.add(_gr["Amortizacao"], fill_value=0)
                            _js = _js.add(_gr["Juros Pagos"], fill_value=0)
                    _fig_dbt.add_trace(go.Bar(x=_meses_dv, y=(_as/umult).tolist(),
                                               name=f"{nt} — Amort.", marker_color=_cr, opacity=0.9))
                    _fig_dbt.add_trace(go.Bar(x=_meses_dv, y=(_js/umult).tolist(),
                                               name=f"{nt} — Juros", marker_color=_cr, opacity=0.5))
                _stot = saldo_total_por_mes(schedules, horizonte)
                _fig_dbt.add_trace(go.Scatter(x=_meses_dv, y=(_stot/umult).tolist(),
                                               mode="lines", name="Saldo", line=dict(color="#dc2626", width=2.5),
                                               yaxis="y2"))
                _fig_dbt.update_layout(barmode="stack",
                                        yaxis=dict(title=f"Servico ({unit})"),
                                        yaxis2=dict(title=f"Saldo ({unit})", overlaying="y", side="right"),
                                        legend=dict(orientation="h", yanchor="bottom", y=1.02))

            # Build context dict
            _deck_ctx = {
                "nome_proj": nome_proj, "setor": fmt_opt(setor),
                "responsavel": responsavel, "data_inicio": _dt_disp,
                "descricao": descricao, "receitas": receitas,
                "horizonte": horizonte, "taxa_desc": taxa_desc,
                "total_capex": total_capex, "total_debt": total_debt,
                "equity_required": equity_required,
                "npv": npv, "payback": payback, "roi": roi, "mg_med": mg_med,
                "irr_projeto": irr_projeto, "mirr_projeto": mirr_projeto,
                "wacc": wacc, "pi_projeto": pi_projeto,
                "annual": annual, "df_op": df_op, "df_lev": df_lev,
                "unit": unit, "umult": umult, "fv": fv, "lang": lang,
                "regime_fiscal": get("regime_fiscal", "Lucro Real"),
                "L": _SL,
                "fig_cashflow": _fig_cf, "fig_revcost": _fig_rc,
                "fig_debt": _fig_dbt, "fig_tornado": _fig_tn,
            }

            try:
                _deck_bytes = gerar_deck(_deck_ctx)
                _fname = _SL["slide_filename"].format(
                    nome=(nome_proj or "projeto").replace(" ", "_").lower()[:30])
                st.success(_SL["slide_ready"])
                st.download_button(
                    label=_SL["slide_download"],
                    data=_deck_bytes,
                    file_name=_fname,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    type="primary")
            except Exception as ex:
                st.error(f"Erro ao gerar deck: {ex}")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="app-footer">{T("footer_text")}<br>{T("footer_powered")}</div>', unsafe_allow_html=True)
