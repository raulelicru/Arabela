"""
Dashboard Profesional de Gestión de Cartera Financiera
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import io

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  CONFIGURACIÓN GLOBAL DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard · Gestión de Cartera",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  ESTILOS CSS — TEMA CLARO CORPORATIVO
# ─────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Fondo general ── */
[data-testid="stAppViewContainer"] {
    background: #f0f2f6;
}
[data-testid="stSidebar"] {
    background: #1a3c6e;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #e8edf5 !important; }
[data-testid="stSidebar"] h2 { color: #ffffff !important; font-size: 1.1rem; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #a8bbcf !important; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

/* ── Encabezados ── */
h1, h2, h3, h4 { color: #1a3c6e; font-weight: 700; }

/* ── Tabs ── */
[data-testid="stTabs"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 0.3rem 0.5rem 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}
[data-testid="stTabs"] button {
    color: #6b7280;
    font-weight: 600;
    font-size: 0.88rem;
    border-radius: 8px 8px 0 0;
    padding: 0.6rem 1.2rem;
    transition: all 0.2s ease;
}
[data-testid="stTabs"] button:hover { color: #1a3c6e; background: #f0f4ff; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1a3c6e !important;
    border-bottom: 3px solid #1a3c6e !important;
    background: #f0f4ff;
}

/* ── Métricas ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e9f0;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 8px rgba(26,60,110,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(26,60,110,0.12);
}
[data-testid="stMetricLabel"] { color: #6b7280; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #1a1a2e; font-size: 1.55rem; font-weight: 700; }

/* ── Tarjetas de gráfica ── */
.chart-card {
    background: #ffffff;
    border: 1px solid #e5e9f0;
    border-radius: 14px;
    padding: 1rem 1.2rem 0.5rem;
    box-shadow: 0 2px 8px rgba(26,60,110,0.06);
    margin-bottom: 1rem;
    transition: box-shadow 0.25s ease;
    animation: fadeSlideIn 0.35s ease both;
}
.chart-card:hover {
    box-shadow: 0 6px 24px rgba(26,60,110,0.13);
}
.chart-card-expanded {
    background: #ffffff;
    border: 2px solid #1a3c6e;
    border-radius: 16px;
    padding: 1.4rem 1.6rem 0.8rem;
    box-shadow: 0 12px 40px rgba(26,60,110,0.18);
    margin-bottom: 1.5rem;
    animation: fadeSlideIn 0.3s ease both;
}
.chart-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
}
.badge-pagado   { background:#dcfce7; color:#16a34a; padding:2px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
.badge-pendiente{ background:#fee2e2; color:#dc2626; padding:2px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }

/* ── Animaciones ── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ── KPI banner ── */
.kpi-banner {
    background: linear-gradient(135deg, #1a3c6e 0%, #2563eb 100%);
    border-radius: 14px;
    padding: 1.2rem 1.8rem;
    color: white;
    margin-bottom: 1.2rem;
    animation: fadeSlideIn 0.3s ease both;
}
.kpi-banner h1 { color: white !important; font-size: 1.4rem; margin: 0; }
.kpi-banner p  { color: rgba(255,255,255,0.75); margin: 0.2rem 0 0; font-size: 0.85rem; }

/* ── Botones expand ── */
[data-testid="stButton"] button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 0.3rem 0.9rem;
    white-space: nowrap;
    transition: all 0.2s ease;
}
[data-testid="stButton"] button:hover {
    background: #1a3c6e !important;
    color: #fff !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(26,60,110,0.25);
}

/* ── Divider ── */
hr { border-color: #e5e9f0; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #c5d0de;
    border-radius: 12px;
    padding: 1rem;
    background: #ffffff;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f0f2f6; }
::-webkit-scrollbar-thumb { background: #c5d0de; border-radius: 4px; }

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: #1a3c6e !important;
    color: white !important;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PALETA DE COLORES (PLOTLY) — PASTEL
# ─────────────────────────────────────────────
COLORS = {
    "primary":  "#1a3c6e",   # navy (títulos y UI, no gráficas)
    "accent":   "#93c5fd",   # pastel azul
    "success":  "#86efac",   # pastel verde
    "warning":  "#fde68a",   # pastel amarillo
    "danger":   "#fca5a5",   # pastel rojo/rosa
    "purple":   "#c4b5fd",   # pastel morado
    "teal":     "#67e8f9",   # pastel teal
    "orange":   "#fdba74",   # pastel naranja
    "muted":    "#9ca3af",
    "bg":       "#ffffff",
    "grid":     "#e5e7eb",
    "text":     "#374151",
}
# Secuencia pastel para series múltiples
PASTEL_SEQ = [
    "#93c5fd", "#86efac", "#fca5a5", "#fde68a",
    "#c4b5fd", "#67e8f9", "#fdba74", "#a5f3fc",
    "#f9a8d4", "#d9f99d", "#fed7aa", "#e9d5ff",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor=COLORS["bg"],
    plot_bgcolor="#f9fafb",
    font=dict(color=COLORS["text"], family="Inter, sans-serif", size=12),
    margin=dict(l=40, r=20, t=50, b=60),
    hovermode="x unified",
)
# Defaults de ejes — aplicar por separado cuando no se sobreescriben
_AXIS_DEFAULTS = dict(gridcolor=COLORS["grid"], zeroline=False, showline=False)

# ─────────────────────────────────────────────
#  INTERNO — CATÁLOGOS DE TIPIFICACIÓN
# ─────────────────────────────────────────────
TIPIF_CATALOG = {
    2:  "Negativa de Pago",
    3:  "Cobrada GDC/consejera",
    6:  "Reclamación Premio",
    7:  "Promesa de Pago",
    8:  "Caja Devuelta GDC",
    9:  "Pago a Porteador",
    10: "Producto devuelto GDC",
    11: "Contratación Menor Edad",
    14: "Pedido no solicitado",
    15: "No recibió producto",
    16: "Ajuste Pendiente",
    20: "Notifica saldo a terceros",
    22: "Tel no corresponde",
    23: "Pago a Cobrador",
    24: "Defunción",
    25: "Tel GDC/consejera",
    27: "Cuelgan llamada",
    28: "No contestan",
    29: "Fuera de servicio",
    30: "Directo a Buzón",
    31: "Ya pagó",
    32: "Promesa Incumplida",
    33: "Seguimiento Promesa",
    34: "No existe teléfono",
    35: "Teléfono incompleto",
    36: "Ya pagó",
}
CONTACTO_EFECTIVO = {2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 16, 20, 23, 24, 25, 31, 32, 33, 36}

# ─────────────────────────────────────────────
#  HELPERS BÁSICOS
# ─────────────────────────────────────────────

def clean_str(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()


def _find_col(df: pd.DataFrame, candidates: list) -> str | None:
    lower_cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        for key, real in lower_cols.items():
            if cand in key:
                return real
    return None


def read_excel_safe(file) -> pd.DataFrame:
    """Lee el Excel y normaliza nombres de columnas. Si hay varias hojas, elige la más grande."""
    xl = pd.ExcelFile(file)
    if len(xl.sheet_names) == 1:
        df = xl.parse(xl.sheet_names[0])
    else:
        # Tomar la hoja con más filas (ignorar hojas de resumen/pivot)
        best, best_rows = xl.sheet_names[0], 0
        for sheet in xl.sheet_names:
            try:
                n = xl.parse(sheet, nrows=0).shape[0]  # solo cabecera
                tmp = xl.parse(sheet)
                if len(tmp) > best_rows:
                    best, best_rows = sheet, len(tmp)
            except Exception:
                pass
        df = xl.parse(best)
    df.columns = [str(c).strip() for c in df.columns]
    return df


# ─────────────────────────────────────────────
#  MAPEO INTERACTIVO DE COLUMNAS
# ─────────────────────────────────────────────

def render_column_mapper(df_cartera: pd.DataFrame, df_saldos: pd.DataFrame,
                         df_moras: pd.DataFrame | None = None) -> dict | None:
    cols_c = list(df_cartera.columns)
    cols_s = list(df_saldos.columns)

    # Auto-detectar columnas
    c_dama  = cols_c[_best_guess(cols_c, ["dama", "num", "nro", "id"])]
    c_anio  = cols_c[_best_guess(cols_c, ["anio", "año", "campaña", "saldo"])]
    s_dama  = cols_s[_best_guess(cols_s, ["dama", "num", "nro", "id"])]
    s_anio  = cols_s[_best_guess(cols_s, ["anio", "año", "campaña", "saldo"])]
    s_saldo = cols_s[_best_guess(cols_s, ["saldocampaña", "saldocampana", "saldo", "deuda", "valor", "monto", "pendiente"])]
    _c_monto_idx = _best_guess(["(ninguna)"] + cols_c, ["saldocobro", "saldocampaña", "saldocampana", "valor", "monto", "deuda", "total"])
    c_monto_auto = (["(ninguna)"] + cols_c)[_c_monto_idx]
    c_fecha_inicio_auto = (["(ninguna)"] + cols_c)[_best_guess(["(ninguna)"] + cols_c, ["inicio", "fecha_i", "start", "vigencia", "fecha"])]
    c_fecha_fin_auto    = (["(ninguna)"] + cols_c)[_best_guess(["(ninguna)"] + cols_c, ["fin", "final", "venc", "end", "termino"])]

    # ── Resumen auto-detectado ────────────────────────────────────────
    st.markdown(
        f"<div style='background:#f0fdf4;border:1px solid #86efac;border-radius:12px;"
        f"padding:1rem 1.2rem;margin-bottom:1rem'>"
        f"<p style='margin:0 0 0.5rem;font-weight:700;color:#15803d;font-size:0.95rem'>"
        f" Archivos detectados correctamente</p>"
        f"<p style='margin:0;font-size:0.82rem;color:#166534'>"
        f"Detectamos las columnas automáticamente. Revisa el resumen y confirma para continuar.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown(
            f"<div style='background:white;border-radius:10px;padding:0.8rem 1rem;"
            f"border:1px solid #e5e7eb'>"
            f"<p style='margin:0 0 0.4rem;font-weight:700;color:{COLORS['primary']};font-size:0.85rem'>"
            f" Archivo Cartera</p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> N° Dama: <b>{c_dama}</b></p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> Campaña: <b>{c_anio}</b></p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> Monto: <b>{c_monto_auto if c_monto_auto != '(ninguna)' else '— no detectado'}</b></p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_r2:
        st.markdown(
            f"<div style='background:white;border-radius:10px;padding:0.8rem 1rem;"
            f"border:1px solid #e5e7eb'>"
            f"<p style='margin:0 0 0.4rem;font-weight:700;color:{COLORS['primary']};font-size:0.85rem'>"
            f" Archivo Saldos</p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> N° Dama: <b>{s_dama}</b></p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> Campaña: <b>{s_anio}</b></p>"
            f"<p style='margin:0;font-size:0.8rem;color:#374151'> Saldo: <b>{s_saldo}</b></p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_r3:
        if df_moras is not None:
            moras_nod = _get_nodama_col(df_moras) or "—"
            st.markdown(
                f"<div style='background:white;border-radius:10px;padding:0.8rem 1rem;"
                f"border:1px solid #e5e7eb'>"
                f"<p style='margin:0 0 0.4rem;font-weight:700;color:{COLORS['primary']};font-size:0.85rem'>"
                f" Archivo Moras</p>"
                f"<p style='margin:0;font-size:0.8rem;color:#374151'> N° Dama: <b>{moras_nod}</b></p>"
                f"<p style='margin:0;font-size:0.8rem;color:#16a34a'> {len(df_moras):,} registros cargados</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background:#fafafa;border-radius:10px;padding:0.8rem 1rem;"
                f"border:1px dashed #d1d5db'>"
                f"<p style='margin:0 0 0.4rem;font-weight:700;color:#9ca3af;font-size:0.85rem'>"
                f" Archivo Moras</p>"
                f"<p style='margin:0;font-size:0.8rem;color:#9ca3af'>Opcional — no cargado</p>"
                f"<p style='margin:0;font-size:0.75rem;color:#9ca3af'>Activa el Tracking Completo</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(" Confirmar y procesar", type="primary", use_container_width=True):
        return {
            "c_dama":         c_dama,
            "c_anio":         c_anio,
            "c_monto":        None if c_monto_auto == "(ninguna)" else c_monto_auto,
            "s_dama":         s_dama,
            "s_anio":         s_anio,
            "s_saldo":        s_saldo,
            "c_fecha_inicio": None if c_fecha_inicio_auto == "(ninguna)" else c_fecha_inicio_auto,
            "c_fecha_fin":    None if c_fecha_fin_auto    == "(ninguna)" else c_fecha_fin_auto,
        }

    # ── Ajuste manual (colapsado) ─────────────────────────────────────
    with st.expander(" Ajustar columnas manualmente"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Cartera**")
            c_dama  = st.selectbox("N° Dama", cols_c, index=cols_c.index(c_dama), key="map_c_dama")
            c_anio  = st.selectbox("Año/Campaña", cols_c, index=cols_c.index(c_anio), key="map_c_anio")
            c_monto_opts = ["(ninguna)"] + cols_c
            c_monto = st.selectbox("Monto original", c_monto_opts,
                                   index=c_monto_opts.index(c_monto_auto), key="map_c_monto")
        with col_b:
            st.markdown("**Saldos**")
            s_dama  = st.selectbox("N° Dama", cols_s, index=cols_s.index(s_dama), key="map_s_dama")
            s_anio  = st.selectbox("Año/Campaña", cols_s, index=cols_s.index(s_anio), key="map_s_anio")
            s_saldo = st.selectbox("Saldo/Deuda", cols_s, index=cols_s.index(s_saldo), key="map_s_saldo")
        fecha_opts = ["(ninguna)"] + cols_c
        fc1, fc2 = st.columns(2)
        with fc1:
            c_fecha_inicio = st.selectbox("Fecha inicio", fecha_opts,
                                          index=fecha_opts.index(c_fecha_inicio_auto), key="map_c_fi")
        with fc2:
            c_fecha_fin = st.selectbox("Fecha fin", fecha_opts,
                                       index=fecha_opts.index(c_fecha_fin_auto), key="map_c_ff")
        if st.button(" Confirmar ajuste manual", type="primary", use_container_width=True, key="map_manual_ok"):
            return {
                "c_dama":         c_dama,
                "c_anio":         c_anio,
                "c_monto":        None if c_monto == "(ninguna)" else c_monto,
                "s_dama":         s_dama,
                "s_anio":         s_anio,
                "s_saldo":        s_saldo,
                "c_fecha_inicio": None if c_fecha_inicio == "(ninguna)" else c_fecha_inicio,
                "c_fecha_fin":    None if c_fecha_fin    == "(ninguna)" else c_fecha_fin,
            }

    return None


def _best_guess(cols: list, keywords: list) -> int:
    for kw in keywords:
        for i, c in enumerate(cols):
            if kw in c.lower():
                return i
    return 0


# ─────────────────────────────────────────────
#  CARGA Y CRUCE DE DATOS
# ─────────────────────────────────────────────

def load_and_clean_data(df_cartera: pd.DataFrame, df_saldos: pd.DataFrame,
                        mapping: dict) -> dict:
    # ── Llave: NumDama + AñoCampañaSaldo (igual en ambos archivos) ────
    df_cartera["_key"] = (
        clean_str(df_cartera[mapping["c_dama"]])
        + "_"
        + clean_str(df_cartera[mapping["c_anio"]])
    )
    df_saldos["_key"] = (
        clean_str(df_saldos[mapping["s_dama"]])
        + "_"
        + clean_str(df_saldos[mapping["s_anio"]])
    )

    # ── Deduplicar Saldos: una sola fila por llave (conserva la última)
    # Esto evita que el merge duplique registros de Cartera
    df_saldos = df_saldos.drop_duplicates(subset="_key", keep="last")

    # ── Merge LEFT desde Cartera → siempre conserva los 68,467 registros
    df_merged = pd.merge(
        df_cartera, df_saldos,
        on="_key", how="left",
        suffixes=("_cartera", "_saldos"),
    )

    # ── Resolver columna de saldo tras el merge ───────────────────────
    s_saldo = mapping["s_saldo"]
    saldo_col = (
        s_saldo if s_saldo in df_merged.columns
        else s_saldo + "_saldos" if s_saldo + "_saldos" in df_merged.columns
        else None
    )

    c_monto = mapping.get("c_monto")
    valor_col = (
        c_monto if c_monto and c_monto in df_merged.columns
        else c_monto + "_cartera" if c_monto and c_monto + "_cartera" in df_merged.columns
        else None
    )

    # ── Convertir saldo a numérico ────────────────────────────────────
    if saldo_col:
        df_merged[saldo_col] = pd.to_numeric(df_merged[saldo_col], errors="coerce").fillna(0)

    # ── Estado de pago: saldo >= 51 → Pagado, saldo < 51 → Pendiente ───
    pagado_mask = df_merged[saldo_col] >= 51 if saldo_col else pd.Series([False] * len(df_merged))
    df_merged["Estado_Pago"] = np.where(pagado_mask, "Pagado", "Pendiente")

    # ── Fechas opcionales de Cartera ─────────────────────────────────
    fecha_inicio_col = None
    fecha_fin_col    = None
    for key, suffix in [("c_fecha_inicio", "_cartera"), ("c_fecha_inicio", "")]:
        raw = mapping.get("c_fecha_inicio")
        if not raw:
            break
        candidate = raw if raw in df_merged.columns else raw + suffix
        if candidate in df_merged.columns:
            df_merged[candidate] = pd.to_datetime(df_merged[candidate], errors="coerce")
            fecha_inicio_col = candidate
            break
    for key, suffix in [("c_fecha_fin", "_cartera"), ("c_fecha_fin", "")]:
        raw = mapping.get("c_fecha_fin")
        if not raw:
            break
        candidate = raw if raw in df_merged.columns else raw + suffix
        if candidate in df_merged.columns:
            df_merged[candidate] = pd.to_datetime(df_merged[candidate], errors="coerce")
            fecha_fin_col = candidate
            break

    # Drop join key and downcast numeric columns to reduce memory footprint
    df_merged = df_merged.drop(columns=["_key"], errors="ignore")
    for col in df_merged.select_dtypes(include=["int64"]).columns:
        df_merged[col] = pd.to_numeric(df_merged[col], downcast="integer")
    for col in df_merged.select_dtypes(include=["float64"]).columns:
        df_merged[col] = pd.to_numeric(df_merged[col], downcast="float")

    return {
        "merged":           df_merged,
        "saldo_col":        saldo_col,
        "valor_col":        valor_col,
        "fecha_inicio_col": fecha_inicio_col,
        "fecha_fin_col":    fecha_fin_col,
    }


# ─────────────────────────────────────────────
#  MÉTRICAS
# ─────────────────────────────────────────────

def calculate_metrics(data: dict) -> dict:
    df        = data["merged"]
    saldo_col = data["saldo_col"]
    valor_col = data.get("valor_col") or _find_col(df, ["saldocobro", "saldocampaña", "saldocampana", "valor", "monto", "deuda", "total"])

    total_registros  = len(df)
    pagados          = (df["Estado_Pago"] == "Pagado").sum()
    pendientes       = total_registros - pagados
    pct_cumplimiento = pagados / total_registros * 100 if total_registros else 0

    monto_total     = 0.0
    monto_pendiente = 0.0
    monto_cobrado   = 0.0

    if valor_col and valor_col in df.columns:
        df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
        monto_total = df[valor_col].sum()
        # Cobrado = suma de Cartera donde Saldos indica saldo = 0 (ya pagaron)
        monto_cobrado   = df.loc[df["Estado_Pago"] == "Pagado",   valor_col].sum()
        # Pendiente = Total Cartera - Cobrado (siempre cuadra)
        monto_pendiente = max(0.0, monto_total - monto_cobrado)

    # ── Serie por campaña: eje X = etiqueta de campaña (string) ──────
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "campaña", "anio", "año", "campaign"])
    if camp_col and saldo_col and camp_col in df.columns:
        grp = (
            df.groupby(camp_col)[saldo_col]
            .sum()
            .reset_index()
            .sort_values(camp_col)
        )
        grp[camp_col] = grp[camp_col].astype(str)   # siempre string → sin fechas falsas
        ts = grp.rename(columns={camp_col: "fecha", saldo_col: "valor"})
    else:
        # Fallback: serie con fechas reales si existe columna de fecha
        fecha_col = _find_col(df, ["fecha", "date", "periodo", "mes"])
        if fecha_col and saldo_col and fecha_col in df.columns:
            df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")
            ts = (
                df.dropna(subset=[fecha_col])
                .sort_values(fecha_col)
                .groupby(fecha_col)[saldo_col]
                .sum()
                .reset_index()
                .rename(columns={fecha_col: "fecha", saldo_col: "valor"})
            )
        else:
            n  = min(60, total_registros)
            ts = pd.DataFrame({
                "fecha": [f"Semana {i+1}" for i in range(n)],
                "valor": np.cumsum(np.random.normal(500, 200, n)),
            })

    return {
        "total_registros":  total_registros,
        "pagados":          pagados,
        "pendientes":       pendientes,
        "pct_cumplimiento": pct_cumplimiento,
        "monto_total":      monto_total,
        "monto_pendiente":  monto_pendiente,
        "monto_cobrado":    monto_cobrado,
        "ts":               ts,
        "df":               df,
        "saldo_col":        saldo_col,
        "valor_col":        valor_col,
        "fecha_inicio_col": data.get("fecha_inicio_col"),
        "fecha_fin_col":    data.get("fecha_fin_col"),
    }


# ─────────────────────────────────────────────
#  RSI
# ─────────────────────────────────────────────

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta    = series.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period).mean()
    rs       = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


# ─────────────────────────────────────────────
#  PREDICCIÓN
# ─────────────────────────────────────────────

def predict_recovery(ts: pd.DataFrame, horizon: int = 10) -> pd.DataFrame:
    """Proyecta las próximas campañas usando regresión lineal."""
    df = ts.copy().dropna()
    if len(df) < 3:
        return pd.DataFrame()

    x = np.arange(len(df), dtype=float)
    y = df["valor"].values.astype(float)
    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(len(df), len(df) + horizon, dtype=float)
    future_y = slope * future_x + intercept

    # Etiquetas de campaña proyectadas (siguientes números después del último)
    last_label = str(df["fecha"].iloc[-1])
    try:
        last_num = int(last_label)
        future_labels = [str(last_num + i + 1) for i in range(horizon)]
    except ValueError:
        future_labels = [f"Proy.{i+1}" for i in range(horizon)]

    fitted    = slope * x + intercept
    residuals = y - fitted
    std_err   = np.std(residuals) * 1.5

    return pd.DataFrame({
        "fecha":      future_labels,
        "prediccion": future_y,
        "upper":      future_y + std_err,
        "lower":      future_y - std_err,
    })


# ─────────────────────────────────────────────
#  GRÁFICAS
# ─────────────────────────────────────────────

def _base_fig(**kwargs) -> go.Figure:
    fig = go.Figure(**kwargs)
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def _fmt(v):
    if v >= 1_000_000: return f"${v/1_000_000:.1f}M"
    if v >= 1_000:     return f"${v/1_000:.0f}K"
    return f"${v:,.0f}"


def plot_kpi_donut(pagados: int, pendientes: int) -> go.Figure:
    total = pagados + pendientes
    pct   = pagados / total * 100 if total else 0
    fig = _base_fig()
    fig.add_trace(go.Pie(
        labels=[" Pagado", " Pendiente"],
        values=[pagados, pendientes],
        hole=0.68,
        marker_colors=[COLORS["success"], COLORS["danger"]],
        textinfo="percent+label",
        textfont=dict(size=13),
        hovertemplate="<b>%{label}</b><br>%{value:,} damas (%{percent})<extra></extra>",
        pull=[0.03, 0],
    ))
    fig.add_annotation(
        text=f"<b>{pct:.1f}%</b><br><span style='font-size:11px'>Cobrado</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=18, color=COLORS["primary"]),
        xref="paper", yref="paper",
    )
    fig.update_layout(
        title_text="Damas cobradas vs pendientes",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=320,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
    )
    return fig


def plot_columnas_agrupadas(df: pd.DataFrame, valor_col: str) -> go.Figure:
    """Monto Cobrado vs Pendiente por campaña — columnas agrupadas."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or not valor_col or camp_col not in df.columns:
        return _base_fig()
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
    grp = df.groupby([camp_col, "Estado_Pago"])[valor_col].sum().reset_index()
    grp[camp_col] = grp[camp_col].astype(str)
    camps = sorted(grp[camp_col].unique())
    camp_labels = _sort_camps([_fmt_camp(c) for c in camps])
    raw_to_fmt  = {c: _fmt_camp(c) for c in camps}
    camps_sorted = sorted(camps, key=lambda c: _camp_sort_key(raw_to_fmt[c]))
    pagado    = grp[grp["Estado_Pago"] == "Pagado"].set_index(camp_col)[valor_col].reindex(camps_sorted, fill_value=0)
    pendiente = grp[grp["Estado_Pago"] == "Pendiente"].set_index(camp_col)[valor_col].reindex(camps_sorted, fill_value=0)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=camp_labels, y=pagado.values, name=" Cobrado",
        marker_color=COLORS["success"],
        text=[_fmt(v) for v in pagado.values], textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=camp_labels, y=pendiente.values, name=" Pendiente",
        marker_color=COLORS["danger"],
        text=[_fmt(v) for v in pendiente.values], textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>Campaña %{x}</b><br>Pendiente: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Monto cobrado vs pendiente por campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="group",
        xaxis_title="Campaña", yaxis_title="Monto ($)",
        height=380,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def plot_100pct_apilado(df: pd.DataFrame) -> go.Figure:
    """Columnas apiladas al 100%: % cobrado vs pendiente por campaña."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or camp_col not in df.columns:
        return _base_fig()
    grp = df.groupby([camp_col, "Estado_Pago"]).size().reset_index(name="n")
    grp[camp_col] = grp[camp_col].astype(str)
    camps = sorted(grp[camp_col].unique(), key=lambda c: _camp_sort_key(_fmt_camp(c)))
    camp_labels = [_fmt_camp(c) for c in camps]
    total_by_camp = grp.groupby(camp_col)["n"].sum()
    pagado    = grp[grp["Estado_Pago"] == "Pagado"].set_index(camp_col)["n"].reindex(camps, fill_value=0)
    pendiente = grp[grp["Estado_Pago"] == "Pendiente"].set_index(camp_col)["n"].reindex(camps, fill_value=0)
    total_s   = total_by_camp.reindex(camps, fill_value=1)
    pct_pag = (pagado / total_s * 100).values
    pct_pen = (pendiente / total_s * 100).values
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=camp_labels, y=pct_pag, name=" Cobrado",
        marker_color=COLORS["success"],
        text=[f"{v:.1f}%" for v in pct_pag], textposition="inside",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=camp_labels, y=pct_pen, name=" Pendiente",
        marker_color=COLORS["danger"],
        text=[f"{v:.1f}%" for v in pct_pen], textposition="inside",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>Campaña %{x}</b><br>Pendiente: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=60, line_dash="dot", line_color="#000000", line_width=1.5,
                  annotation_text="  Meta 60%", annotation_font_color="#000000")
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="% de recuperación por campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="stack",
        xaxis_title="Campaña", yaxis_title="% de Damas",
        yaxis_range=[0, 110],
        height=360,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def plot_funnel(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    """Embudo de cobranza: Total → Con Saldo → Pendiente → Pagado."""
    total   = len(df)
    con_saldo = int((pd.to_numeric(df.get(saldo_col, pd.Series(dtype=float)), errors="coerce").fillna(-1) >= 0).sum()) if saldo_col and saldo_col in df.columns else total
    pendiente = int((df["Estado_Pago"] == "Pendiente").sum())
    pagado    = int((df["Estado_Pago"] == "Pagado").sum())
    stages = [" Total Cartera", " Con Saldo Asignado", " Pendientes de Pago", " Pagadas"]
    values = [total, con_saldo, pendiente, pagado]
    colors = [COLORS["accent"], COLORS["teal"], COLORS["danger"], COLORS["success"]]
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textposition="inside",
        textinfo="value+percent initial",
        textfont=dict(color=COLORS["text"], size=12),
        marker=dict(color=colors, line=dict(width=1, color="white")),
        connector=dict(line=dict(color=COLORS["grid"], width=2)),
        hovertemplate="<b>%{y}</b><br>%{x:,} damas<br>%{percentInitial} del total<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="¿Dónde está la cartera?",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=380,
    )
    fig.update_layout(hovermode="y")
    return fig


def _fmt_camp(code: str) -> str:
    """202608 → 'C-8'  (solo los últimos 2 dígitos son el número de campaña)."""
    c = str(code).strip()
    if len(c) == 6 and c.isdigit():
        return f"C-{int(c[4:])}"
    return c


def _camp_sort_key(label: str):
    """Ordena etiquetas 'C-N' numéricamente; el resto alfabéticamente al final."""
    s = str(label)
    if s.startswith("C-") and s[2:].isdigit():
        return (0, int(s[2:]))
    return (1, s)


def _sort_camps(labels) -> list:
    """Devuelve la lista/índice de etiquetas de campaña en orden numérico."""
    return sorted(labels, key=_camp_sort_key)


def _fecha_valida(df: pd.DataFrame, fecha_col: str) -> bool:
    """Devuelve True si la columna tiene fechas reales (año >= 2000)."""
    if fecha_col not in df.columns:
        return False
    validas = df[fecha_col].dropna()
    if len(validas) == 0:
        return False
    try:
        anio_min = validas.dt.year.min()
        return bool(anio_min >= 2000)
    except Exception:
        return False


def _get_time_axis(df: pd.DataFrame, valor_col: str, fecha_col: str | None):
    """
    Devuelve (x_labels, cob_vals, pen_vals, x_title).
    Si hay fecha_col real válida, agrupa por mes. Si no, usa campaña.
    """
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)

    if fecha_col and _fecha_valida(df, fecha_col):
        df["_period"] = df[fecha_col].dt.to_period("M").astype(str)
        grp_col = "_period"
        x_title = "Mes"
    else:
        camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
        if not camp_col:
            return [], [], [], "Campaña"
        df["_period"] = df[camp_col].astype(str).apply(_fmt_camp)
        grp_col = "_period"
        x_title = "Campaña"

    cobrado   = df[df["Estado_Pago"] == "Pagado"].groupby(grp_col)[valor_col].sum()
    pendiente = df[df["Estado_Pago"] == "Pendiente"].groupby(grp_col)[valor_col].sum()
    periods   = _sort_camps(set(cobrado.index) | set(pendiente.index))
    cob_vals  = cobrado.reindex(periods, fill_value=0).values
    pen_vals  = pendiente.reindex(periods, fill_value=0).values
    return periods, cob_vals, pen_vals, x_title


def plot_linea_tendencia(df: pd.DataFrame, valor_col: str, fecha_col: str | None = None) -> go.Figure:
    """Gráfico de líneas: tendencia de cobro — usa fecha real si disponible."""
    if not valor_col:
        return _base_fig()
    periods, cob_vals, pen_vals, x_title = _get_time_axis(df, valor_col, fecha_col)
    if not len(periods):
        return _base_fig()
    x = [str(p) for p in periods]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=cob_vals, name=" Cobrado",
        mode="lines+markers",
        line=dict(color=COLORS["success"], width=3),
        marker=dict(size=7, color=COLORS["success"], line=dict(width=2, color="white")),
        fill="tozeroy", fillcolor="rgba(134,239,172,0.25)",
        hovertemplate=f"<b>%{{x}}</b><br>Cobrado: $%{{y:,.0f}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=pen_vals, name=" Pendiente",
        mode="lines+markers",
        line=dict(color=COLORS["danger"], width=3),
        marker=dict(size=7, color=COLORS["danger"], line=dict(width=2, color="white")),
        fill="tozeroy", fillcolor="rgba(252,165,165,0.20)",
        hovertemplate=f"<b>%{{x}}</b><br>Pendiente: $%{{y:,.0f}}<extra></extra>",
    ))
    if len(cob_vals) >= 3:
        rolling = pd.Series(cob_vals).rolling(3, min_periods=1).mean().values
        fig.add_trace(go.Scatter(
            x=x, y=rolling, name="Tendencia (prom. móvil 3)",
            mode="lines", line=dict(color="#000000", width=2, dash="dot"),
            hovertemplate="Tendencia: $%{y:,.0f}<extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Recuperación" + (" por mes" if fecha_col else " por campaña"),
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title=x_title, yaxis_title="Monto ($)",
        height=380,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def plot_area_apilada(df: pd.DataFrame, valor_col: str, fecha_col: str | None = None) -> go.Figure:
    """Área apilada: evolución cobrado + pendiente — usa fecha real si disponible."""
    if not valor_col:
        return _base_fig()
    periods, cob_vals, pen_vals, x_title = _get_time_axis(df, valor_col, fecha_col)
    if not len(periods):
        return _base_fig()
    x = [str(p) for p in periods]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=pen_vals, name=" Pendiente",
        stackgroup="one", mode="lines",
        line=dict(color=COLORS["danger"], width=1),
        fillcolor="rgba(252,165,165,0.70)",
        hovertemplate=f"<b>%{{x}}</b><br>Pendiente: $%{{y:,.0f}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=cob_vals, name=" Cobrado",
        stackgroup="one", mode="lines",
        line=dict(color=COLORS["success"], width=1),
        fillcolor="rgba(134,239,172,0.75)",
        hovertemplate=f"<b>%{{x}}</b><br>Cobrado: $%{{y:,.0f}}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Cobrado y pendiente" + (" por mes" if fecha_col else " por campaña"),
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title=x_title, yaxis_title="Monto Total ($)",
        height=380,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
    )
    return fig


def plot_heatmap(df: pd.DataFrame, valor_col: str, fecha_col: str | None = None) -> go.Figure:
    """
    Mapa de calor con fechas reales: Año (filas) × Mes (columnas) → % cobrado.
    Sin fechas: usa Año × Período extraídos del código de campaña (YYYYPP).
    """
    df = df.copy()
    if not valor_col:
        return _base_fig()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)

    MESES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

    if fecha_col and _fecha_valida(df, fecha_col):
        df["_anio"] = df[fecha_col].dt.year.astype(str)
        df["_mes"]  = df[fecha_col].dt.month
        cobrado_grp = (df[df["Estado_Pago"] == "Pagado"]
                       .groupby(["_anio", "_mes"])[valor_col].sum())
        total_grp   = df.groupby(["_anio", "_mes"])[valor_col].sum()
        pct_grp     = (cobrado_grp / total_grp.replace(0, np.nan) * 100).fillna(0)
        pivot       = pct_grp.unstack(fill_value=0)
        anios    = sorted(pivot.index.tolist())
        mes_nums = sorted(pivot.columns.tolist())
        x_labels = [MESES[m - 1] for m in mes_nums]
        z        = [[pivot.loc[a, m] if m in pivot.columns else 0 for m in mes_nums] for a in anios]
        hover    = "Año: %{y} · Mes: %{x}<br>% Cobrado: %{z:.1f}%<extra></extra>"
        title    = "Mapa de Calor · % Cobrado por Año y Mes (Fecha de Inicio)"
        ylab, xlab = "Año", "Mes"
    else:
        camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
        if not camp_col:
            return _base_fig()
        df["_camp_str"] = df[camp_col].astype(str).str.strip()
        mask_6 = df["_camp_str"].str.match(r"^\d{6}$")
        if mask_6.sum() < 2:
            grp = df.groupby(camp_col)
            pct = (grp.apply(lambda x: (x["Estado_Pago"] == "Pagado").sum() / len(x) * 100)
                   .reset_index(name="pct"))
            pct[camp_col] = pct[camp_col].astype(str).apply(_fmt_camp)
            pct = pct.iloc[sorted(range(len(pct)), key=lambda i: _camp_sort_key(pct[camp_col].iloc[i]))]
            fig = go.Figure(go.Bar(
                x=pct[camp_col], y=pct["pct"],
                marker=dict(color=pct["pct"],
                            colorscale=[[0, COLORS["danger"]], [0.5, COLORS["warning"]], [1, COLORS["success"]]],
                            showscale=True, colorbar=dict(title="% Cobrado")),
                text=[f"{v:.1f}%" for v in pct["pct"]], textposition="outside",
                hovertemplate="<b>Campaña %{x}</b><br>% Cobrado: %{y:.1f}%<extra></extra>",
            ))
            fig.update_layout(**PLOTLY_LAYOUT, height=340,
                              title_text="% cobrado por campaña",
                              title_font=dict(size=14, color=COLORS["primary"]))
            return fig
        df["_anio"] = df["_camp_str"].str[:4]
        df["_per"]  = df["_camp_str"].str[4:]
        cobrado_grp = (df[df["Estado_Pago"] == "Pagado"]
                       .groupby(["_anio", "_per"])[valor_col].sum())
        total_grp   = df.groupby(["_anio", "_per"])[valor_col].sum()
        pct_grp     = (cobrado_grp / total_grp.replace(0, np.nan) * 100).fillna(0)
        pivot    = pct_grp.unstack(fill_value=0)
        anios    = [str(a) for a in sorted(pivot.index.tolist())]   # strings → categorical
        raw_pers = sorted(pivot.columns.tolist())
        x_labels = [f"Camp. {int(p)}" for p in raw_pers]           # "01" → "Camp. 1"
        z        = [[pivot.loc[a, p] if p in pivot.columns else 0 for p in raw_pers] for a in pivot.index.sort_values()]
        hover    = "Año: %{y} · %{x}<br>% Cobrado: %{z:.1f}%<extra></extra>"
        title    = "Mapa de Calor · % Cobrado por Campaña y Año"
        ylab, xlab = "Año", "Campaña"

    text_z = [[f"{v:.1f}%" for v in row] for row in z]
    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=anios,
        text=text_z, texttemplate="%{text}",
        textfont=dict(size=12, color=COLORS["primary"]),
        colorscale=[[0, COLORS["danger"]], [0.5, COLORS["warning"]], [1, COLORS["success"]]],
        zmin=0, zmax=100,
        colorbar=dict(title="% Cobrado", ticksuffix="%"),
        hovertemplate=hover,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text=title,
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis=dict(title=xlab, type="category", **_AXIS_DEFAULTS),
        yaxis=dict(title=ylab, type="category", **_AXIS_DEFAULTS),
        height=max(280, len(anios) * 60 + 120),
    )
    return fig


def plot_waterfall(df: pd.DataFrame, valor_col: str) -> go.Figure:
    """Cascada: cómo se va recuperando la cartera campaña a campaña."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or not valor_col or camp_col not in df.columns:
        return _base_fig()
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
    cobrado_camp = (df[df["Estado_Pago"] == "Pagado"]
                    .groupby(camp_col)[valor_col].sum()
                    .sort_index().reset_index())
    cobrado_camp[camp_col] = cobrado_camp[camp_col].astype(str).apply(_fmt_camp)
    cobrado_camp = cobrado_camp.iloc[cobrado_camp[camp_col].apply(_camp_sort_key).argsort()]
    total = df[valor_col].sum()
    pendiente_final = df[df["Estado_Pago"] == "Pendiente"][valor_col].sum()
    x_labels  = ["Cartera Total"] + cobrado_camp[camp_col].tolist() + ["Saldo Pendiente"]
    measures  = ["absolute"] + ["relative"] * len(cobrado_camp) + ["total"]
    y_vals    = [total] + [-v for v in cobrado_camp[valor_col].tolist()] + [pendiente_final]
    text_vals = [_fmt(total)] + [f"-{_fmt(v)}" for v in cobrado_camp[valor_col].tolist()] + [_fmt(pendiente_final)]
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measures,
        x=x_labels, y=y_vals,
        text=text_vals, textposition="outside",
        textfont=dict(size=10),
        increasing=dict(marker_color=COLORS["danger"]),
        decreasing=dict(marker_color=COLORS["success"]),
        totals=dict(marker_color=COLORS["warning"]),
        connector=dict(line=dict(color=COLORS["grid"], width=1.5, dash="dot")),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Cómo se reduce la deuda campaña a campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="", yaxis_title="Monto ($)",
        height=420,
    )
    return fig


def plot_bullet(metrics: dict) -> go.Figure:
    """Bullet graph: cumplimiento actual vs metas."""
    pct   = metrics["pct_cumplimiento"]
    total = metrics["monto_total"]
    cob   = metrics["monto_cobrado"]
    metas = [50, 63]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(
        x=[pct], y=["% Damas que pagaron"],
        orientation="h",
        marker=dict(
            color=COLORS["success"] if pct >= 60 else COLORS["warning"] if pct >= 50 else COLORS["danger"],
        ),
        text=[f"{pct:.1f}%"], textposition="inside",
        textfont=dict(size=14, color=COLORS["primary"]),
        width=0.4,
        hovertemplate=f"Cumplimiento actual: {pct:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=[total], y=["Monto Total Cartera ($)"],
        orientation="h",
        marker_color=COLORS["accent"], opacity=0.35,
        width=0.4,
        hovertemplate=f"Total cartera: ${total:,.0f}<extra></extra>",
        showlegend=False,
    ))
    fig.add_trace(go.Bar(
        x=[cob], y=["Monto Total Cartera ($)"],
        orientation="h",
        marker_color=COLORS["success"],
        text=[f"  {_fmt(cob)} cobrado"], textposition="outside",
        textfont=dict(size=13, color=COLORS["primary"]),
        width=0.4,
        hovertemplate=f"Cobrado: ${cob:,.0f}<extra></extra>",
        showlegend=False,
    ))
    for meta in metas:
        fig.add_shape(type="line", x0=meta, x1=meta, y0=-0.5, y1=0.5,
                      line=dict(color=COLORS["primary"], width=2, dash="dash"),
                      row=1, col=1)
        fig.add_annotation(x=meta, y=0.55, text=f"Meta {meta}%",
                           showarrow=False, font=dict(size=10, color=COLORS["primary"]),
                           xanchor="center")
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Avance de cobranza vs meta",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="overlay",
        xaxis=dict(range=[0, 115], ticksuffix="%", gridcolor=COLORS["grid"]),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        height=280,
        showlegend=False,
    )
    return fig


def plot_top_damas(df: pd.DataFrame, saldo_col: str, n: int = 15) -> go.Figure:
    if not saldo_col:
        return _base_fig()
    col = next((c for c in ["Número de Dama_cartera", "Número de Dama", "NumDama_cartera", "NumDama"]
                if c in df.columns), None)
    if not col:
        return _base_fig()
    top = (
        df[df["Estado_Pago"] == "Pendiente"]
        .groupby(col)[saldo_col].sum()
        .nlargest(n).reset_index().sort_values(saldo_col)
    )
    top["label"] = top[saldo_col].apply(_fmt)
    fig = go.Figure(go.Bar(
        x=top[saldo_col], y=top[col].astype(str),
        orientation="h",
        marker=dict(
            color=top[saldo_col],
            colorscale=[[0, COLORS["warning"]], [0.5, COLORS["orange"]], [1, COLORS["danger"]]],
            showscale=False,
        ),
        text=top["label"], textposition="outside",
        textfont=dict(size=11, color=COLORS["primary"]),
        hovertemplate="<b>Dama %{y}</b><br>Saldo pendiente: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text=f"Las {n} damas con más deuda",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Saldo Pendiente ($)", yaxis_title="",
        height=max(320, n * 26),
        yaxis=dict(tickfont=dict(size=10)),
    )
    return fig


def plot_prediction(ts: pd.DataFrame, pred_df: pd.DataFrame) -> go.Figure:
    fig = _base_fig()
    hist_labels = [_fmt(v) for v in ts["valor"]]
    fig.add_trace(go.Bar(
        x=ts["fecha"].astype(str), y=ts["valor"],
        name="Histórico", marker_color=COLORS["accent"], opacity=0.9,
        text=hist_labels, textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>Campaña %{x}</b><br>Saldo real: $%{y:,.0f}<extra></extra>",
    ))
    if not pred_df.empty:
        proj_labels = [_fmt(v) for v in pred_df["prediccion"]]
        fig.add_trace(go.Bar(
            x=pred_df["fecha"].astype(str), y=pred_df["prediccion"],
            name=" Proyección", marker_color=COLORS["warning"], opacity=0.8,
            text=proj_labels, textposition="outside", textfont=dict(size=10),
            error_y=dict(
                type="data", symmetric=False,
                array=list(pred_df["upper"] - pred_df["prediccion"]),
                arrayminus=list(pred_df["prediccion"] - pred_df["lower"]),
                visible=True, color=COLORS["muted"],
            ),
            hovertemplate="<b>Campaña %{x}</b><br>Estimado: $%{y:,.0f}<extra></extra>",
        ))
        if len(ts):
            last_x = str(ts["fecha"].iloc[-1])
            fig.add_shape(type="line", xref="x", yref="paper",
                          x0=last_x, x1=last_x, y0=0, y1=1,
                          line=dict(dash="dash", color="#000000", width=1.5))
            fig.add_annotation(x=last_x, yref="paper", y=1.05,
                                text="Inicio proyección", showarrow=False,
                                font=dict(size=10, color=COLORS["muted"]), xanchor="left")
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Proyección de deuda pendiente",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Campaña", yaxis_title="Saldo ($)",
        height=440, bargap=0.2, barmode="group",
    )
    return fig


def _find_num_col(df: pd.DataFrame) -> str | None:
    return next((c for c in ["Número de Dama_cartera", "Número de Dama",
                              "NumDama_cartera", "NumDama"] if c in df.columns), None)


def plot_damas_por_temporalidad(df: pd.DataFrame) -> go.Figure:
    """
    Todas las damas Pendientes distribuidas por temporalidad (campaña destino).
    """
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col:
        return _base_fig()

    pendientes = df[df["Estado_Pago"] == "Pendiente"].copy()
    pendientes[camp_col] = pendientes[camp_col].astype(str).str.strip().apply(_fmt_camp)
    dist = pendientes.groupby(camp_col).size()
    dist = dist.reindex(_sort_camps(dist.index))

    fig = go.Figure(go.Bar(
        x=dist.index.tolist(),
        y=dist.values,
        marker=dict(
            color=dist.values,
            colorscale=[[0, COLORS["accent"]], [1, COLORS["primary"]]],
            showscale=False,
        ),
        text=[f"{v:,}" for v in dist.values],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["primary"]),
        hovertemplate="<b>Temporalidad %{x}</b><br>%{y:,} damas pendientes<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text=f"Damas pendientes de pago por campaña ({dist.values.sum():,} en total)",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis=dict(type="category", tickangle=-45),
        xaxis_title="Temporalidad (Año Campaña Saldo)",
        yaxis_title="Número de Damas",
        height=400,
    )
    return fig



def plot_delta_campanas(df: pd.DataFrame) -> go.Figure:
    """% cobrado por campaña con flecha vs campaña anterior — muy fácil de leer."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or camp_col not in df.columns:
        return _base_fig()

    total  = df.groupby(camp_col).size()
    pagado = df[df["Estado_Pago"] == "Pagado"].groupby(camp_col).size()
    pct    = (pagado / total * 100).fillna(0)
    pct.index = pct.index.astype(str).map(_fmt_camp)
    pct = pct.reindex(_sort_camps(pct.index))

    if len(pct) < 2:
        return _base_fig()

    camps  = pct.index.tolist()
    vals   = pct.values
    delta  = pct.diff()

    # Color de cada barra según si mejoró o empeoró vs la anterior
    colors = []
    for i, c in enumerate(camps):
        if i == 0:
            colors.append(COLORS["accent"])
        elif delta[c] > 0:
            colors.append(COLORS["success"])
        elif delta[c] < 0:
            colors.append(COLORS["danger"])
        else:
            colors.append(COLORS["accent"])

    # Etiqueta: % + flecha comparación vs anterior
    labels = []
    for i, c in enumerate(camps):
        if i == 0:
            labels.append(f"{vals[i]:.1f}%")
        else:
            d = delta[c]
            arrow = "▲" if d > 0 else "▼"
            labels.append(f"{vals[i]:.1f}%\n{arrow} {abs(d):.1f}% vs anterior")

    fig = go.Figure(go.Bar(
        x=camps, y=vals,
        marker_color=colors,
        text=labels,
        textposition="outside",
        textfont=dict(size=10, color=COLORS["text"]),
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: %{y:.1f}%<extra></extra>",
    ))

    # Línea de promedio general
    promedio = float(pct.mean())
    fig.add_hline(y=promedio, line_dash="dot", line_color="#000000", line_width=2,
                  annotation_text=f"  Promedio: {promedio:.1f}%",
                  annotation_font_color=COLORS["warning"], annotation_font_size=11)

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Cobro por campaña vs campaña anterior",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis=dict(type="category", tickangle=-30),
        xaxis_title="Campaña",
        yaxis_title="% de damas que pagaron",
        yaxis_range=[0, max(vals) * 1.35],
        height=420,
    )
    return fig


# ─────────────────────────────────────────────
#  HELPERS UI
# ─────────────────────────────────────────────

def fmt_currency(val: float) -> str:
    if val >= 1_000_000:
        return f"${val/1_000_000:.2f}M"
    elif val >= 1_000:
        return f"${val/1_000:.1f}K"
    return f"${val:,.2f}"


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"### {title}")
    if subtitle:
        st.markdown(
            f"<span style='color:{COLORS['muted']};font-size:0.85rem'>{subtitle}</span>",
            unsafe_allow_html=True,
        )


def chart_card(title: str, fig: go.Figure, key: str, height_normal: int = 340, height_expanded: int = 560):
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{title}</div></div>",
                unsafe_allow_html=True)
    fig.update_layout(height=height_normal)
    st.plotly_chart(fig, use_container_width=True, key=f"plot_{key}",
                    config={"displayModeBar": False, "scrollZoom": True})


# ─────────────────────────────────────────────
#  SIDEBAR CON FILTROS
# ─────────────────────────────────────────────

def render_sidebar(data: dict | None) -> dict:
    filters = {}
    with st.sidebar:
        st.markdown("## Cartera Dashboard")
        st.markdown(
            f"<span style='color:{COLORS['muted']};font-size:0.8rem'>Centro de Comando de Cobranza</span>",
            unsafe_allow_html=True,
        )
        st.divider()

        if data:
            df = data["merged"]
            st.markdown("#### Filtros")

            # ── Filtro principal: Año Campaña Saldo (multiselect) ─────
            camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
            if camp_col and camp_col in df.columns:
                camps_disponibles = sorted(df[camp_col].astype(str).unique().tolist())
                seleccion = st.multiselect(
                    "Año Campaña Saldo",
                    options=camps_disponibles,
                    default=[],
                    placeholder="Todas las campañas",
                )
                filters["campañas"] = seleccion
                filters["camp_col"] = camp_col

            # ── Filtro: Estado de Pago ─────────────────────────────────
            estados = ["Todos", "Pagado", "Pendiente"]
            filters["estado"] = st.selectbox("Estado de Pago", estados)

            st.divider()

            # ── Resumen en tiempo real ─────────────────────────────────
            total    = len(df)
            pagados  = (df["Estado_Pago"] == "Pagado").sum()
            pend     = total - pagados
            st.markdown(
                f"<small style='color:{COLORS['muted']}'>"
                f" Total registros: <b>{total:,}</b><br>"
                f" Pagadas: <b>{pagados:,}</b><br>"
                f" Pendientes: <b>{pend:,}</b>"
                f"</small>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Carga los archivos Excel para activar los filtros.")

        st.divider()

        # ── Personalización: color de fondo ───────────────────────────
        st.markdown(
            "<small style='color:#a8bbcf;font-weight:600;text-transform:uppercase;"
            "letter-spacing:.05em'>Color de fondo</small>",
            unsafe_allow_html=True,
        )
        PRESETS = {
            "Gris claro":  "#f0f2f6",
            "Blanco":      "#ffffff",
            "Azul suave":  "#e8eef7",
            "Menta":       "#e8f5f0",
            "Crema":       "#fdf6ec",
            "Oscuro":      "#1e2530",
        }
        if "bg_color" not in st.session_state:
            st.session_state.bg_color = "#f0f2f6"

        cols_p = st.columns(3)
        for i, (name, hex_val) in enumerate(PRESETS.items()):
            with cols_p[i % 3]:
                active = st.session_state.bg_color == hex_val
                border = "3px solid #fff" if active else "2px solid rgba(255,255,255,0.3)"
                if st.button(
                    " " if not active else "✓",
                    key=f"preset_{name}",
                    help=name,
                    use_container_width=True,
                ):
                    st.session_state.bg_color = hex_val
                    st.rerun()
                st.markdown(
                    f"<div style='background:{hex_val};height:6px;border-radius:3px;"
                    f"margin-top:-10px;border:{border}'></div>"
                    f"<p style='font-size:0.65rem;color:#a8bbcf;text-align:center;"
                    f"margin:2px 0 6px'>{name}</p>",
                    unsafe_allow_html=True,
                )

        custom = st.color_picker("Personalizado", st.session_state.bg_color,
                                 key="color_picker_custom",
                                 label_visibility="collapsed")
        if custom != st.session_state.bg_color:
            st.session_state.bg_color = custom
            st.rerun()

        # ── Modo Visual ───────────────────────────────────────────────────
        st.divider()
        st.markdown(
            "<small style='color:#a8bbcf;font-weight:600;text-transform:uppercase;"
            "letter-spacing:.05em'>Modo Visual</small>",
            unsafe_allow_html=True,
        )
        if "visual_mode" not in st.session_state:
            st.session_state.visual_mode = "Clásico"

        mode_col1, mode_col2 = st.columns(2)
        with mode_col1:
            active1 = st.session_state.visual_mode == "Clásico"
            if st.button(
                "🖥️ Clásico" if not active1 else "✓ Clásico",
                key="mode_clasico",
                use_container_width=True,
                help="Diseño limpio y profesional",
            ):
                st.session_state.visual_mode = "Clásico"
                st.rerun()
        with mode_col2:
            active2 = st.session_state.visual_mode == "3D Animado"
            if st.button(
                "✨ 3D" if not active2 else "✓ 3D",
                key="mode_3d",
                use_container_width=True,
                help="Cards flotantes, animaciones y efectos de profundidad",
            ):
                st.session_state.visual_mode = "3D Animado"
                st.rerun()

        if st.session_state.visual_mode == "3D Animado":
            st.markdown(
                "<p style='font-size:0.65rem;color:#a8bbcf;text-align:center;margin:2px 0 4px'>"
                "✨ Animaciones activas</p>",
                unsafe_allow_html=True,
            )

        st.divider()
        st.markdown(
            f"<small style='color:{COLORS['muted']}'>Motor de Inteligencia de Recuperación</small>",
            unsafe_allow_html=True,
        )
    return filters


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    camp_col  = filters.get("camp_col")
    seleccion = filters.get("campañas", [])
    estado    = filters.get("estado", "Todos")

    camp_active   = bool(camp_col and seleccion and camp_col in df.columns)
    estado_active = bool(estado and estado != "Todos")

    if not camp_active and not estado_active:
        return df.copy()  # full copy so tabs can mutate columns safely

    mask = pd.Series(True, index=df.index)
    if camp_active:
        mask &= df[camp_col].astype(str).isin(seleccion)
    if estado_active:
        mask &= df["Estado_Pago"] == estado

    return df.loc[mask].copy()


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────

def tab_resumen(metrics: dict):
    st.markdown(
        "<div class='kpi-banner'><h1> Resumen General de Cartera</h1>"
        "<p>Haz clic en <b> Ampliar</b> en cualquier gráfica para verla en grande</p></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4, c5 = st.columns(5)
    pct_cobrado = metrics["monto_cobrado"] / metrics["monto_total"] * 100 if metrics["monto_total"] else 0
    with c1: st.metric(" Total Registros",  f"{metrics['total_registros']:,}")
    with c2: st.metric(" Total Cartera",     fmt_currency(metrics["monto_total"]))
    with c3: st.metric(" Total Cobrado",      fmt_currency(metrics["monto_cobrado"]),
                       delta=f"+{pct_cobrado:.1f}% del total")
    with c4: st.metric(" Saldo Pendiente",   fmt_currency(metrics["monto_pendiente"]),
                       delta=f"{metrics['pendientes']:,} damas deben", delta_color="inverse")
    with c5: st.metric(" % Cumplimiento",    f"{metrics['pct_cumplimiento']:.1f}%",
                       delta=f"{metrics['pagados']:,} ya pagaron")
    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 1: Columnas agrupadas + 100% apilado
    col_a, col_b = st.columns(2)
    with col_a:
        chart_card("Cuanto cobramos y cuanto falta por campaña",
                   plot_columnas_agrupadas(metrics["df"], metrics["valor_col"]),
                   key="col_agrupadas", height_normal=380)
    with col_b:
        chart_card("Porcentaje cobrado por campaña",
                   plot_100pct_apilado(metrics["df"]),
                   key="pct100", height_normal=360)

    # Fila 2: solo Donut
    chart_card("Estado de cobro de la cartera",
               plot_kpi_donut(metrics["pagados"], metrics["pendientes"]),
               key="donut", height_normal=320)

    with st.expander(" Ver datos consolidados (primeros 200 registros)"):
        st.dataframe(metrics["df"].head(200), use_container_width=True, height=300)


def tab_temporalidad(metrics: dict):
    fi = metrics.get("fecha_inicio_col")
    usando_fechas = bool(fi) and _fecha_valida(metrics["df"], fi) if fi else False
    st.markdown(
        "<div class='kpi-banner'><h1> Temporalidad de Cobro</h1>"
        + (f"<p>Usando <b>Fecha de Inicio</b> real del archivo Cartera — análisis mes a mes</p>"
           if usando_fechas else
           "<p>Usando <b>Año Campaña Saldo</b> como eje temporal · Carga fechas en el mapper para análisis mensual</p>")
        + "</div>",
        unsafe_allow_html=True,
    )
    chart_card(
        "Como ha evolucionado el cobro" + (" mes a mes" if usando_fechas else " por campaña"),
        plot_linea_tendencia(metrics["df"], metrics["valor_col"], fi),
        key="linea", height_normal=380, height_expanded=560,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    fig_heatmap = plot_heatmap(metrics["df"], metrics["valor_col"], fi)
    fig_heatmap.update_layout(height=340)
    st.plotly_chart(fig_heatmap, use_container_width=True, key="plot_heatmap",
                    config={"displayModeBar": False, "scrollZoom": True})


def tab_flujo(metrics: dict):
    st.markdown(
        "<div class='kpi-banner'><h1>Operaciones y Territorio</h1>"
        "<p>Cumplimiento de meta, flujo de deuda, damas pendientes por campaña y análisis de rutas</p></div>",
        unsafe_allow_html=True,
    )
    # Bullet: meta vs real
    chart_card("Vamos a tiempo con la meta de cobranza",
               plot_bullet(metrics),
               key="bullet", height_normal=280, height_expanded=400)
    st.markdown("<br>", unsafe_allow_html=True)
    fig_wf = plot_waterfall(metrics["df"], metrics["valor_col"])
    fig_wf.update_layout(height=420)
    st.plotly_chart(fig_wf, use_container_width=True, key="plot_waterfall",
                    config={"displayModeBar": False, "scrollZoom": True})
    st.divider()

    # ── KPIs: cambio de temporalidad ─────────────────────────────────
    camp_col = _find_col(metrics["df"], ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if camp_col:
        pend_df    = metrics["df"][metrics["df"]["Estado_Pago"] == "Pendiente"]
        total_pend = len(pend_df)
        n_camps    = pend_df[camp_col].astype(str).nunique()
        c1, c2     = st.columns(2)
        with c1: st.metric("Damas asignadas a Mora", f"{total_pend:,}")
        with c2: st.metric(" Cierre de Campaña",                   f"{n_camps}")
        st.markdown("<br>", unsafe_allow_html=True)

    fig_temp = plot_damas_por_temporalidad(metrics["df"])
    fig_temp.update_layout(height=400)
    st.plotly_chart(fig_temp, use_container_width=True, key="plot_cambio_temp",
                    config={"displayModeBar": False, "scrollZoom": True})
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Análisis de Rutas (viene del archivo de moras) ───────────────
    df_moras_ss = st.session_state.get("df_moras")
    if df_moras_ss is not None:
        ruta_col    = _find_col(df_moras_ss, ["ruta", "rutas", "route"])
        nodama_mora = _get_nodama_col(df_moras_ss)
        nodama_col  = _find_col(metrics["df"], ["nodama", "no dama", "númdama", "numdama", "número de dama", "num_dama"])
        valor_col   = metrics.get("valor_col")

        if ruta_col and nodama_mora and nodama_col:
            st.divider()

            # Cruzar moras con pendientes para obtener el monto
            pendientes  = metrics["df"][metrics["df"]["Estado_Pago"] == "Pendiente"].copy()
            pendientes["_nodama_str"] = pendientes[nodama_col].astype(str).str.strip()
            df_moras_ruta = df_moras_ss[[nodama_mora, ruta_col]].copy()
            df_moras_ruta["_nodama_str"] = df_moras_ruta[nodama_mora].astype(str).str.strip()

            df_cruce = pendientes.merge(
                df_moras_ruta[["_nodama_str", ruta_col]].drop_duplicates("_nodama_str"),
                on="_nodama_str", how="inner"
            )

            if not df_cruce.empty:
                ruta_dist = (
                    df_cruce.groupby(ruta_col)
                    .agg(
                        Damas=(ruta_col, "count"),
                        **({ "Monto": (valor_col, lambda x: pd.to_numeric(x, errors="coerce").sum()) } if valor_col else {})
                    )
                    .sort_values("Damas", ascending=False)
                    .reset_index()
                )
                ruta_dist["% del total"] = (ruta_dist["Damas"] / ruta_dist["Damas"].sum() * 100).round(1)

                # KPIs top 3
                top3 = ruta_dist.head(3)
                cols_r = st.columns(min(len(top3), 3))
                for i, (col_r, (_, row_s)) in enumerate(zip(cols_r, top3.iterrows())):
                    with col_r:
                        label = "Ruta con mas moras" if i == 0 else f"#{i+1} con mas moras"
                        st.metric(label, f"Ruta {row_s[ruta_col]}", delta=f"{row_s['Damas']:,} damas · {row_s['% del total']:.1f}%", delta_color="off")
                        if valor_col and "Monto" in ruta_dist.columns:
                            st.caption(f"Monto: {fmt_currency(row_s['Monto'])}")

                st.markdown("<br>", unsafe_allow_html=True)

                # Barras: damas por ruta
                fig_ruta = go.Figure(go.Bar(
                    x=ruta_dist[ruta_col].astype(str),
                    y=ruta_dist["Damas"],
                    marker_color=[PASTEL_SEQ[i % len(PASTEL_SEQ)] for i in range(len(ruta_dist))],
                    text=ruta_dist["Damas"],
                    textposition="outside",
                    textfont=dict(color=COLORS["text"], size=11),
                    hovertemplate="<b>Ruta %{x}</b><br>Damas en mora: %{y:,}<br>%{customdata:.1f}%<extra></extra>",
                    customdata=ruta_dist["% del total"],
                ))
                fig_ruta.update_layout(
                    **PLOTLY_LAYOUT,
                    xaxis=dict(type="category", **_AXIS_DEFAULTS),
                    yaxis=dict(title="Numero de damas", **_AXIS_DEFAULTS),
                )
                chart_card("Damas por ruta enviadas a Mora", fig_ruta, key="ruta_moras", height_normal=420)

                # Barras: monto por ruta
                if valor_col and "Monto" in ruta_dist.columns:
                    st.markdown("<br>", unsafe_allow_html=True)
                    fig_ruta_m = go.Figure(go.Bar(
                        x=ruta_dist[ruta_col].astype(str),
                        y=ruta_dist["Monto"],
                        marker_color=COLORS["danger"],
                        text=ruta_dist["Monto"].apply(lambda v: f"${v/1e6:.2f}M" if v >= 1e6 else f"${v/1e3:.0f}K"),
                        textposition="outside",
                        textfont=dict(color=COLORS["text"], size=11),
                        hovertemplate="<b>Ruta %{x}</b><br>Monto en mora: $%{y:,.0f}<extra></extra>",
                    ))
                    fig_ruta_m.update_layout(
                        **PLOTLY_LAYOUT,
                        xaxis=dict(type="category", **_AXIS_DEFAULTS),
                        yaxis=dict(title="Monto ($)", **_AXIS_DEFAULTS),
                    )
                    chart_card("Cuanto dinero en mora tiene cada ruta", fig_ruta_m, key="ruta_moras_monto", height_normal=420)


                # ── Desglose de campañas por ruta ──────────────────────
                camp_col_ruta = _find_col(df_cruce, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
                if camp_col_ruta:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### Composicion de campañas dentro de cada ruta")

                    _agg = {ruta_col: "count"}
                    if valor_col and valor_col in df_cruce.columns:
                        _agg[valor_col] = "sum"
                    ruta_camp = (
                        df_cruce.groupby([ruta_col, camp_col_ruta])
                        .agg(**{"Damas": pd.NamedAgg(column=ruta_col, aggfunc="count"),
                                **( {"Saldo": pd.NamedAgg(column=valor_col, aggfunc="sum")}
                                    if valor_col and valor_col in df_cruce.columns else {})})
                        .reset_index()
                    )
                    ruta_camp["Campaña"] = ruta_camp[camp_col_ruta].astype(str).str.strip().apply(_fmt_camp)
                    total_por_camp = ruta_camp.groupby("Campaña")["Damas"].transform("sum")
                    ruta_camp["% en ruta"] = (ruta_camp["Damas"] / total_por_camp.replace(0, np.nan) * 100).round(1).fillna(0)

                    # Orden de rutas: mayor número de moras primero
                    orden_rutas = ruta_dist[ruta_col].tolist()
                    camps_sorted = _sort_camps(ruta_camp["Campaña"].unique())
                    pivot_pct = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="% en ruta", aggfunc="sum", fill_value=0)
                        .reindex(index=orden_rutas, columns=camps_sorted, fill_value=0)
                    )
                    pivot_cnt = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="Damas", aggfunc="sum", fill_value=0)
                        .reindex(index=orden_rutas, columns=camps_sorted, fill_value=0)
                    )

                    # Pivot: filas = ruta (orden: más moras primero), columnas = campaña
                    pivot_heat = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="Damas", aggfunc="sum", fill_value=0)
                        .reindex(index=orden_rutas, columns=camps_sorted, fill_value=0)
                    )
                    pivot_heat_pct = (
                        pivot_heat.div(pivot_heat.sum(axis=0), axis=1) * 100
                    ).round(1)

                    rutas_labels = [f"Ruta {r}" for r in pivot_heat.index]
                    z_cnt = pivot_heat.values.tolist()
                    z_pct = pivot_heat_pct.values.tolist()

                    def _heat_annotations(z_grid, x_labels, y_labels, fmt_fn,
                                          threshold=0.45, dark_color="#1a3c6e"):
                        """Anotación por celda con color blanco/oscuro según intensidad."""
                        flat = [v for row in z_grid for v in row]
                        z_max = max(flat) if flat else 1
                        anns = []
                        for i, y in enumerate(y_labels):
                            for j, x in enumerate(x_labels):
                                val = z_grid[i][j]
                                color = "white" if (val / z_max) > threshold else dark_color
                                anns.append(dict(
                                    x=x, y=y, text=fmt_fn(val),
                                    showarrow=False,
                                    font=dict(size=11, color=color),
                                    xref="x", yref="y",
                                ))
                        return anns

                    # — Heatmap 1: número de damas —
                    fig_heat_cnt = go.Figure(go.Heatmap(
                        z=z_cnt, x=camps_sorted, y=rutas_labels,
                        colorscale=[[0.0, "#f0f9ff"], [0.5, "#7dd3fc"], [1.0, "#1a3c6e"]],
                        showscale=True,
                        colorbar=dict(title="Damas", thickness=14, len=0.8),
                        hovertemplate="<b>%{y} · %{x}</b><br>Damas en mora: %{z:,}<extra></extra>",
                    ))
                    fig_heat_cnt.update_layout(
                        **PLOTLY_LAYOUT,
                        xaxis=dict(type="category", title="Campaña", side="bottom", **_AXIS_DEFAULTS),
                        yaxis=dict(title="", autorange="reversed", **_AXIS_DEFAULTS),
                        annotations=_heat_annotations(z_cnt, camps_sorted, rutas_labels,
                                                      lambda v: f"{int(v):,}"),
                    )
                    chart_card("Cuantas damas en mora tiene cada ruta por campaña",
                               fig_heat_cnt, key="heat_cnt", height_normal=400)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # — Heatmap 2: % de cada ruta dentro de la campaña —
                    fig_heat_pct = go.Figure(go.Heatmap(
                        z=z_pct, x=camps_sorted, y=rutas_labels,
                        colorscale=[[0.0, "#f0fdf4"], [0.5, "#6ee7b7"], [1.0, "#065f46"]],
                        showscale=True,
                        colorbar=dict(title="%", thickness=14, len=0.8),
                        hovertemplate="<b>%{y} · %{x}</b><br>%{z:.1f}% de la campaña<extra></extra>",
                        zmin=0, zmax=30,
                    ))
                    fig_heat_pct.update_layout(
                        **PLOTLY_LAYOUT,
                        xaxis=dict(type="category", title="Campaña", side="bottom", **_AXIS_DEFAULTS),
                        yaxis=dict(title="", autorange="reversed", **_AXIS_DEFAULTS),
                        annotations=_heat_annotations(z_pct, camps_sorted, rutas_labels,
                                                      lambda v: f"{v:.0f}%",
                                                      threshold=2.0, dark_color="#111111"),
                    )
                    chart_card("Porcentaje de cada campaña corresponde a cada ruta",
                               fig_heat_pct, key="heat_pct", height_normal=400)

                    # Selector: detalle de una campaña específica
                    st.markdown("<br>", unsafe_allow_html=True)
                    camp_sel = st.selectbox("Ver detalle de una campaña:",
                                            camps_sorted, key="sel_camp_ruta")
                    _det_cols = [ruta_col, "Damas", "% en ruta"] + (["Saldo"] if "Saldo" in ruta_camp.columns else [])
                    detalle_camp = (
                        ruta_camp[ruta_camp["Campaña"] == camp_sel]
                        [_det_cols]
                        .sort_values("Damas", ascending=False)
                        .rename(columns={ruta_col: "Ruta", "% en ruta": "% de la campaña"})
                    )
                    if "Saldo" in detalle_camp.columns:
                        detalle_camp["Saldo"] = detalle_camp["Saldo"].apply(fmt_currency)
                    total_camp_sel = int(detalle_camp["Damas"].sum())
                    st.caption(f"{camp_sel} — {total_camp_sel:,} damas en mora en total")
                    st.dataframe(detalle_camp, use_container_width=False, hide_index=True, height=320, width=480)

    else:
        st.info("Sube el archivo de moras para ver el analisis por ruta.")

    col_d, _ = st.columns([1, 2])
    with col_d:
        buf = io.BytesIO()
        metrics["df"].to_excel(buf, index=False)
        buf.seek(0)
        st.download_button(" Descargar Excel Consolidado", data=buf,
                           file_name="cartera_consolidada.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)




# ─────────────────────────────────────────────
#  HELPERS COMPARTIDOS
# ─────────────────────────────────────────────

def _get_nodama_col(df: pd.DataFrame) -> str | None:
    """Encuentra la columna de número de dama."""
    return _find_col(df, ["nodama", "no dama", "númdama", "numdama", "número de dama", "num_dama"])


# ─────────────────────────────────────────────
#  TAB TRACKING COMPLETO
# ─────────────────────────────────────────────

def tab_tracking(df_moras: pd.DataFrame | None, metrics: dict | None = None):
    if df_moras is None:
        st.markdown(
            "<div class='kpi-banner'><h1>Tracking Completo de Cartera</h1>"
            "<p>Seguimiento de pendientes de pago a través de las 10 campañas operativas</p></div>",
            unsafe_allow_html=True,
        )
        st.info("Sube el archivo GENERAL_CARTERA_MORAS para ver este análisis.")
        return

    nodama_col = _get_nodama_col(df_moras)
    camp_col   = _find_col(df_moras, ["campania", "campaña", "camp", "campana"])
    mora_col   = _find_col(df_moras, ["moras", "mora", "nivel de mora", "nivel_mora"])
    saldo_col  = _find_col(df_moras, ["saldodama", "saldo", "importe", "monto", "importenetofactura"])
    idsit_col  = _find_col(df_moras, ["idsituacion", "id_situacion", "situacion"])

    if not nodama_col or not camp_col:
        st.error("No se encontraron las columnas NoDama o Campaña en el archivo.")
        return

    MORA_LEVELS = ["Inactiva", "Mora 1", "Mora 2", "Mora 3"]
    MORA_COLORS = {
        "Inactiva": "#94A3B8",
        "Mora 1":   COLORS["warning"],
        "Mora 2":   COLORS["orange"],
        "Mora 3":   COLORS["danger"],
    }
    CHURN_WINDOW = 3

    def _cn(v):
        try:
            return int(str(v).upper().replace("C", ""))
        except Exception:
            return 99

    # ── Preparar datos ────────────────────────────────────────────────
    df = df_moras.copy()
    df[nodama_col] = df[nodama_col].astype(str).str.strip()
    df[camp_col]   = df[camp_col].astype(str).str.strip()
    if saldo_col:
        df[saldo_col] = pd.to_numeric(df[saldo_col], errors="coerce").fillna(0)

    mora_map = {
        "mora 1": "Mora 1", "mora 2": "Mora 2", "mora 3": "Mora 3",
        "1": "Mora 1", "2": "Mora 2", "3": "Mora 3",
    }
    df["_mora"] = (
        df[mora_col].astype(str).str.strip().str.lower().map(mora_map)
        if mora_col else pd.Series("Mora 1", index=df.index)
    )
    n_inac = 0
    if idsit_col:
        mask = df[idsit_col].astype(str).str.strip() == "0"
        df.loc[mask, "_mora"] = "Inactiva"
        n_inac = int(mask.sum())

    df["_cn"] = df[camp_col].apply(_cn)
    df = df[df["_cn"] <= 10].copy()

    camps_n      = sorted(df["_cn"].unique())
    camp_labels  = [f"C-{c}" for c in camps_n]
    pool         = set(df[nodama_col].unique())
    pool_size    = len(pool)

    # ── Motor de cohortes ─────────────────────────────────────────────
    sets = {c: set(df[df["_cn"] == c][nodama_col]) for c in camps_n}
    total_all_camps = sum(len(sets[c]) for c in camps_n)   # denominador para % del Pool
    first_camp_d = df.groupby(nodama_col)["_cn"].min().to_dict()
    mora_sets = {}
    for c in camps_n:
        df_c = df[df["_cn"] == c]
        for m in MORA_LEVELS:
            mora_sets[(c, m)] = set(df_c[df_c["_mora"] == m][nodama_col])

    summary_rows = []
    for i, c in enumerate(camps_n):
        prev_c  = camps_n[i - 1] if i > 0 else None
        prev2_c = camps_n[i - 2] if i > 1 else None
        next_c  = camps_n[i + 1] if i < len(camps_n) - 1 else None
        total_set   = sets[c]
        nuevas      = {d for d in total_set if first_camp_d.get(d) == c}
        de_anterior = (total_set & sets[prev_c]) if prev_c else set()
        persistentes = (total_set & sets[prev_c] & sets[prev2_c]) if (prev_c and prev2_c) else set()
        salen       = (total_set - sets[next_c]) if next_c else set()
        future      = [cx for cx in camps_n if cx > c and cx <= c + CHURN_WINDOW]
        fugadas     = (total_set - set().union(*[sets[cx] for cx in future])) if future else set()

        row = {
            "camp_n": c, "camp_label": f"C-{c}",
            "pool_size": pool_size,
            "total": len(total_set),
            "pct_pool": round(len(total_set) / total_all_camps * 100, 1) if total_all_camps else 0,
            "nuevas": len(nuevas),
            "de_anterior": len(de_anterior),
            "persistentes": len(persistentes),
            "salen": len(salen),
            "fugadas": len(fugadas),
            "saldo_total": df[df["_cn"] == c][saldo_col].sum() if saldo_col else 0,
        }
        for mora in MORA_LEVELS:
            ids_m = mora_sets[(c, mora)]
            row[f"{mora}_total"]       = len(ids_m)
            row[f"{mora}_nuevas"]      = len(ids_m & nuevas)
            row[f"{mora}_de_anterior"] = len(ids_m & de_anterior)
            row[f"{mora}_persistentes"]= len(ids_m & persistentes)
            row[f"{mora}_salen"]       = len(ids_m & salen)
            row[f"{mora}_fugadas"]     = len(ids_m & fugadas)
            row[f"{mora}_saldo"]       = (
                df[(df["_cn"] == c) & (df["_mora"] == mora)][saldo_col].sum()
                if saldo_col else 0
            )
        if prev_c:
            inac_p = mora_sets[(prev_c, "Inactiva")]
            row["fi_total"] = len(inac_p & total_set)
            for mora in MORA_LEVELS:
                row[f"fi_to_{mora}"] = len(inac_p & mora_sets[(c, mora)])
        else:
            row["fi_total"] = 0
            for mora in MORA_LEVELS:
                row[f"fi_to_{mora}"] = 0
        summary_rows.append(row)

    sdf = pd.DataFrame(summary_rows)   # summary dataframe

    # Transition matrix
    transitions = []
    for i in range(len(camps_n) - 1):
        c1, c2 = camps_n[i], camps_n[i + 1]
        shared = sets[c1] & sets[c2]
        df1 = (df[(df["_cn"] == c1) & df[nodama_col].isin(shared)]
               .drop_duplicates(nodama_col).set_index(nodama_col)["_mora"])
        df2 = (df[(df["_cn"] == c2) & df[nodama_col].isin(shared)]
               .drop_duplicates(nodama_col).set_index(nodama_col)["_mora"])
        joined = df1.to_frame("origen").join(df2.to_frame("destino"), how="inner")
        for (orig, dest), cnt in joined.groupby(["origen", "destino"]).size().items():
            transitions.append({
                "de": f"C-{c1}", "a": f"C-{c2}",
                "origen": orig, "destino": dest, "cuentas": int(cnt),
            })
    trans_df = pd.DataFrame(transitions) if transitions else pd.DataFrame()

    # Exit detail
    last_camp_d = df.groupby(nodama_col)["_cn"].max().to_dict()
    max_c = max(camps_n)
    exits = []
    for dama, lc in last_camp_d.items():
        if lc < max_c:
            sub = df[(df[nodama_col] == dama) & (df["_cn"] == lc)]
            exits.append({
                "NoDama": dama,
                "Última Campaña": f"C-{lc}",
                "Estado al Salir": sub["_mora"].iloc[0] if len(sub) > 0 else "N/A",
                "Saldo al Salir": float(sub[saldo_col].iloc[0]) if (saldo_col and len(sub) > 0) else 0,
            })
    exits_df = pd.DataFrame(exits) if exits else pd.DataFrame()

    # ── KPIs superiores ──────────────────────────────────────────────
    # Base/saldo pendientes → archivo principal (mismo dato que "Damas reclasificadas")
    base_inac  = metrics["pendientes"]    if metrics else df_moras[nodama_col].nunique()
    saldo_inac = metrics["monto_pendiente"] if metrics else None
    # Base/saldo de moras → archivo de moras completo
    base_moras  = len(df_moras)
    saldo_moras = df_moras[saldo_col].sum() if saldo_col else None

    st.markdown(
        f"<div class='kpi-banner' style='margin-bottom:0.5rem'>"
        f"<h1 style='margin:0'>Tracking Completo de Cartera</h1></div>",
        unsafe_allow_html=True,
    )
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Base Damas Inactivas", f"{base_inac:,}")
    with k2:
        st.metric("Saldo Damas Inactivas",
                  fmt_currency(saldo_inac) if saldo_inac is not None else "—")
    with k3:
        st.metric("Base Damas en Mora", f"{base_moras:,}")
    with k4:
        st.metric("Saldo Total Damas en Mora",
                  fmt_currency(saldo_moras) if saldo_moras is not None else "—")

    st.markdown("<br>", unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    ret_rates = [
        (sdf.loc[i, "total"] - sdf.loc[i, "nuevas"]) / sdf.loc[i - 1, "total"] * 100
        for i in sdf.index if i > 0 and sdf.loc[i - 1, "total"] > 0
    ]
    avg_ret = sum(ret_rates) / len(ret_rates) if ret_rates else 0
    with k1: st.metric("Total campañas", f"{len(camps_n)}")
    with k2: st.metric("Retención promedio por campaña", f"{avg_ret:.1f}%")
    with k3:
        mora1_nodamas = set(df[df["_mora"] == "Mora 1"][nodama_col].astype(str))
        if metrics and "df" in metrics:
            _pend_df  = metrics["df"][metrics["df"]["Estado_Pago"] == "Pendiente"]
            _nod_main = _find_col(_pend_df, ["nodama", "no dama", "númdama", "numdama", "número de dama", "num_dama"])
            if _nod_main:
                _mask_no_m1   = ~_pend_df[_nod_main].astype(str).isin(mora1_nodamas)
                pend_no_mora1 = _pend_df[_mask_no_m1][_nod_main].nunique()
                _vcol = metrics.get("valor_col")
                _saldo_no_m1  = _pend_df[_mask_no_m1][_vcol].sum() if _vcol and _vcol in _pend_df.columns else None
            else:
                pend_no_mora1 = 0
                _saldo_no_m1  = None
        else:
            pend_no_mora1 = 0
            _saldo_no_m1  = None
        st.metric("Pendientes sin Mora 1", f"{pend_no_mora1:,}",
                  delta=fmt_currency(_saldo_no_m1) if _saldo_no_m1 is not None else None,
                  delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Cómputos para Reporte Ejecutivo ──────────────────────────────────
    _total_pagaron  = metrics["pagados"]    if metrics else 0
    _total_sin_pago = metrics["pendientes"] if metrics else 0
    _total_inac     = _total_pagaron + _total_sin_pago   # pool completo asignado

    _migrated_to_m1 = set()
    for _i, _c in enumerate(camps_n[:-1]):
        _next_c = camps_n[_i + 1]
        _inac_c = mora_sets[(_c, "Inactiva")]
        _m1_next = mora_sets[(_next_c, "Mora 1")]
        _migrated_to_m1 |= (_inac_c & _m1_next)
    _total_migrated = len(_migrated_to_m1)

    _total_fuga = max(0, _total_sin_pago - _total_migrated)
    _pct_migr = round(_total_migrated / _total_sin_pago * 100, 1) if _total_sin_pago else 0.0
    _pct_fuga = round(_total_fuga / _total_sin_pago * 100, 1) if _total_sin_pago else 0.0

    _all_m1 = set().union(*[mora_sets[(c, "Mora 1")] for c in camps_n]) if camps_n else set()
    _all_m2 = set().union(*[mora_sets[(c, "Mora 2")] for c in camps_n]) if camps_n else set()
    _all_m3 = set().union(*[mora_sets[(c, "Mora 3")] for c in camps_n]) if camps_n else set()
    _direct_m2 = len(_all_m2 - _all_m1)
    _direct_m3 = len(_all_m3 - _all_m1 - _all_m2)
    _direct_entries = _direct_m2 + _direct_m3

    _m1_to_m2_to_m3 = len(_all_m1 & _all_m2 & _all_m3)
    _m1_to_m2_only  = len((_all_m1 & _all_m2) - _all_m3)
    _m1_only        = len(_all_m1 - _all_m2 - _all_m3)
    _m1_to_m2_total = len(_all_m1 & _all_m2)
    _m2_to_m3_total = len(_all_m2 & _all_m3)
    _m1_exits       = len(_all_m1) - _m1_to_m2_total
    _m2_exits       = len(_all_m2) - _m2_to_m3_total

    subtab0, subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
        "Reporte Ejecutivo",
        "Resumen Ejecutivo",
        "Por Campaña",
        "Por Mora",
        "Salidas",
        "Transiciones",
        "Flujo Inactivas",
    ])

    # ══════════════════════════════════════════
    # SUBTAB 0 — Reporte Ejecutivo
    # ══════════════════════════════════════════
    with subtab0:
        st.markdown(
            "<div class='kpi-banner'>"
            "<h1 style='margin:0'>Reporte Ejecutivo · Análisis de Migración y Fuga</h1>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # ── Fila 1 de KPIs ──────────────────────────────────────────────
        _re_k1, _re_k2, _re_k3, _re_k4 = st.columns(4)
        with _re_k1:
            st.metric("Total Damas Asignadas", f"{_total_inac:,}")
        with _re_k2:
            st.metric("Total que Pagaron", f"{_total_pagaron:,}")
        with _re_k3:
            st.metric("Total Sin Pago", f"{_total_sin_pago:,}")
        with _re_k4:
            st.metric("Migraron a Mora 1", f"{_total_migrated:,}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Fila 2 de KPIs ──────────────────────────────────────────────
        _re_k5, _re_k6, _re_k7, _re_k8 = st.columns(4)
        with _re_k5:
            st.metric("Sin Pago Sin Asignar", f"{_total_fuga:,}")
        with _re_k6:
            st.metric("% Migración a Mora 1", f"{_pct_migr:.1f}%")
        with _re_k7:
            st.metric("% Fuga", f"{_pct_fuga:.1f}%")
        with _re_k8:
            st.metric("Entradas Directas M2/M3", f"{_direct_entries:,}")

        st.divider()

        # ── Diagrama Sankey ─────────────────────────────────────────────
        st.markdown("#### Flujo de Migración (Sankey)")

        # Nivel 2: en mora vs sin mora dentro del pool Sin Pago
        _en_mora_tot = len(_all_m1 | _all_m2 | _all_m3)
        _sin_mora_sp = max(0, _total_sin_pago - _en_mora_tot)

        # Nivel 3: distribución de moras
        _solo_m1  = len(_all_m1 - _all_m2 - _all_m3)
        _solo_m2  = len(_all_m2 - _all_m3)
        _solo_m3  = len(_all_m3)

        # Nodos:  0=Total  1=Pagaron  2=SinPago  3=SinMora  4=EnMora  5=M1  6=M2  7=M3
        _sank_nodes = [
            "Total Asignadas",   # 0
            "Pagaron",           # 1
            "Sin Pago",          # 2
            "Sin mora asignada", # 3
            "En mora",           # 4
            "Mora 1",            # 5
            "Mora 2",            # 6
            "Mora 3",            # 7
        ]
        _sank_x = [0.01, 0.99, 0.40, 0.99, 0.70, 0.99, 0.99, 0.99]
        _sank_y = [0.50, 0.18, 0.72, 0.55, 0.80, 0.68, 0.82, 0.95]
        _sank_colors_node = [
            "#64748B",           # Total — gris azulado
            "#22C55E",           # Pagaron — verde
            "#F59E0B",           # Sin Pago — ámbar
            "#94A3B8",           # Sin mora — gris claro
            "#FB923C",           # En mora — naranja
            "#FBBF24",           # Mora 1 — amarillo
            "#F97316",           # Mora 2 — naranja fuerte
            "#EF4444",           # Mora 3 — rojo
        ]
        _sank_src = [0, 0, 2, 2, 4,       4,       4      ]
        _sank_tgt = [1, 2, 3, 4, 5,       6,       7      ]
        _sank_val = [
            max(1, _total_pagaron),
            max(1, _total_sin_pago),
            max(1, _sin_mora_sp),
            max(1, _en_mora_tot),
            max(1, _solo_m1),
            max(1, _solo_m2),
            max(1, _solo_m3),
        ]
        _sank_link_colors = [
            "rgba(34,197,94,0.30)",    # → Pagaron
            "rgba(245,158,11,0.30)",   # → Sin Pago
            "rgba(148,163,184,0.30)",  # → Sin mora
            "rgba(251,146,60,0.30)",   # → En mora
            "rgba(251,191,36,0.30)",   # → M1
            "rgba(249,115,22,0.30)",   # → M2
            "rgba(239,68,68,0.30)",    # → M3
        ]
        _fig_sank = go.Figure(go.Sankey(
            arrangement="fixed",
            node=dict(
                pad=28,
                thickness=28,
                line=dict(color="rgba(255,255,255,0.6)", width=1),
                label=_sank_nodes,
                color=_sank_colors_node,
                x=_sank_x,
                y=_sank_y,
                hovertemplate="<b>%{label}</b><br>%{value:,} damas<extra></extra>",
            ),
            link=dict(
                source=_sank_src,
                target=_sank_tgt,
                value=_sank_val,
                color=_sank_link_colors,
                hovertemplate="%{source.label} → %{target.label}<br><b>%{value:,}</b> damas<extra></extra>",
            ),
        ))
        _fig_sank.update_layout(
            **{**PLOTLY_LAYOUT,
               "margin": dict(t=30, b=30, l=20, r=20),
               "font": dict(size=14, color="#000000", family="Inter, sans-serif"),
               "paper_bgcolor": "rgba(0,0,0,0)"},
            height=500,
        )
        st.markdown(
            "<style>.js-plotly-plot .sankey text { text-shadow: none !important; "
            "filter: none !important; }</style>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(_fig_sank, use_container_width=True)

        st.divider()

        # ── Trayectorias ─────────────────────────────────────────────────
        st.markdown("#### Trayectorias de Cuentas")
        _traj_labels = [
            "Mora 1 → Sale",
            "Mora 1 → Mora 2 → Sale",
            "Mora 1 → Mora 2 → Mora 3",
            "Directo a Mora 2",
            "Directo a Mora 3",
        ]
        _traj_values = [
            _m1_only,
            _m1_to_m2_only,
            _m1_to_m2_to_m3,
            _direct_m2,
            _direct_m3,
        ]
        _traj_bar_colors = [
            COLORS["warning"],
            COLORS["orange"],
            COLORS["danger"],
            "#A78BFA",
            "#6D28D9",
        ]
        _fig_traj = go.Figure(go.Bar(
            x=_traj_values,
            y=_traj_labels,
            orientation="h",
            marker_color=_traj_bar_colors,
            text=[f"{v:,}" for v in _traj_values],
            textposition="outside",
            textfont=dict(size=11),
            hovertemplate="%{y}: %{x:,}<extra></extra>",
        ))
        _fig_traj.update_layout(
            **{**PLOTLY_LAYOUT, "margin": dict(t=20, b=20, l=180, r=80)},
            height=300,
            xaxis=dict(title="Cuentas", **_AXIS_DEFAULTS),
            yaxis=dict(**_AXIS_DEFAULTS),
        )
        st.plotly_chart(_fig_traj, use_container_width=True)

        st.divider()

        # ── Tabla resumen ─────────────────────────────────────────────────
        st.markdown("#### Tabla Resumen Ejecutivo")
        _re_table_rows = [
            {"#": 1, "Métrica": "Total Damas Asignadas",    "Cantidad": _total_inac,     "%": "100%"},
            {"#": 2, "Métrica": "Pagaron",                 "Cantidad": _total_pagaron,  "%": f"{round(_total_pagaron/_total_inac*100,1) if _total_inac else 0:.1f}%"},
            {"#": 3, "Métrica": "Sin Pago",                "Cantidad": _total_sin_pago, "%": f"{round(_total_sin_pago/_total_inac*100,1) if _total_inac else 0:.1f}%"},
            {"#": 4, "Métrica": "Migraron a Mora 1",       "Cantidad": _total_migrated, "%": f"{_pct_migr:.1f}% de sin pago"},
            {"#": 5, "Métrica": "Sin Pago sin asignar",    "Cantidad": _total_fuga,     "%": f"{_pct_fuga:.1f}% de sin pago"},
            {"#": 6, "Métrica": "% Migración",             "Cantidad": "—",             "%": f"{_pct_migr:.1f}%"},
            {"#": 7, "Métrica": "% Fuga",                  "Cantidad": "—",             "%": f"{_pct_fuga:.1f}%"},
            {"#": 8, "Métrica": "Entradas directas M2/M3", "Cantidad": _direct_entries, "%": "—"},
        ]
        st.dataframe(pd.DataFrame(_re_table_rows), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # SUBTAB 1 — Resumen Ejecutivo
    # ══════════════════════════════════════════
    with subtab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica: Mora 1/2/3 como barras apiladas + Inactiva como línea (eje secundario)
        fig_comp = go.Figure()
        for mora in ["Mora 1", "Mora 2", "Mora 3"]:
            fig_comp.add_trace(go.Bar(
                x=sdf["camp_label"], y=sdf[f"{mora}_total"],
                name=mora, marker_color=MORA_COLORS[mora], yaxis="y",
                hovertemplate=f"<b>%{{x}}</b><br>{mora}: %{{y:,}}<extra></extra>",
            ))
        fig_comp.add_trace(go.Scatter(
            x=sdf["camp_label"], y=sdf["Inactiva_total"],
            name="Inactiva", mode="lines+markers+text",
            line=dict(color=COLORS["primary"], width=2.5),
            marker=dict(size=8, color=COLORS["primary"]),
            text=sdf["Inactiva_total"].apply(lambda v: f"{v:,}"),
            textposition="top center",
            textfont=dict(size=10, color=COLORS["primary"]),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Inactiva: %{y:,}<extra></extra>",
        ))
        fig_comp.update_layout(
            **{**PLOTLY_LAYOUT, "margin": dict(t=20, b=80, l=10, r=10)},
            barmode="stack",
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas en Mora", **_AXIS_DEFAULTS),
            yaxis2=dict(
                title="Inactivas", overlaying="y", side="right",
                showgrid=False, **_AXIS_DEFAULTS,
            ),
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        )
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            chart_card("Composición por estado", fig_comp, key="trk_comp", height_normal=380)

        # Gráfica: Nuevas vs Fugadas (barras) + % Fuga (línea eje secundario)
        net = sdf["nuevas"] - sdf["fugadas"]
        fig_cohort = go.Figure()
        fig_cohort.add_trace(go.Bar(
            x=sdf["camp_label"], y=sdf["nuevas"],
            name="Entran", marker_color=COLORS["success"],
            text=sdf["nuevas"], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Entran: %{y:,}<extra></extra>",
        ))
        fig_cohort.add_trace(go.Bar(
            x=sdf["camp_label"], y=sdf["fugadas"],
            name="Se van", marker_color=COLORS["danger"],
            text=sdf["fugadas"], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Se van: %{y:,}<extra></extra>",
        ))
        fig_cohort.add_trace(go.Scatter(
            x=sdf["camp_label"], y=net,
            name="Neto", mode="lines+markers",
            line=dict(color=COLORS["primary"], width=2.5),
            marker=dict(size=8, color=COLORS["primary"]),
            text=net.apply(lambda v: f"+{v:,}" if v >= 0 else f"{v:,}"),
            textposition="top center", textfont=dict(size=9, color=COLORS["primary"]),
            hovertemplate="<b>%{x}</b><br>Neto: %{text}<extra></extra>",
            yaxis="y2",
        ))
        fig_cohort.update_layout(
            **{**PLOTLY_LAYOUT, "margin": dict(t=20, b=80, l=10, r=10)},
            barmode="group",
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            yaxis2=dict(title="Neto", overlaying="y", side="right",
                        showgrid=False, **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        )
        with col_c2:
            chart_card("Tendencias de cohorte", fig_cohort, key="trk_cohort", height_normal=380)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica saldo
        if saldo_col:
            fig_saldo = go.Figure(go.Bar(
                x=sdf["camp_label"], y=sdf["saldo_total"],
                marker_color=COLORS["accent"],
                text=sdf["saldo_total"].apply(lambda v: f"${v/1e6:.1f}M" if v >= 1e6 else f"${v/1e3:.0f}K"),
                textposition="outside", textfont=dict(size=10),
                hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
            ))
            fig_saldo.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Saldo pendiente por campaña",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(type="category", **_AXIS_DEFAULTS),
                yaxis=dict(title="Saldo ($)", **_AXIS_DEFAULTS),
            )
            chart_card("Saldo por campaña", fig_saldo, key="trk_saldo", height_normal=360)
            st.markdown("<br>", unsafe_allow_html=True)

        # Tabla resumen ejecutiva
        st.markdown("#### Tabla Resumen Ejecutiva")
        exec_rows = []
        for _, r in sdf.iterrows():
            tot = int(r["total"])
            exec_rows.append({
                "Campaña":           r["camp_label"],
                "Pendientes":        tot,
                "% del Pool":        f"{r['pct_pool']:.1f}%",
                "Nuevas":            int(r["nuevas"]),
                "% Nuevas":          f"{r['nuevas']/tot*100:.1f}%" if tot else "—",
                "De Anterior":       int(r["de_anterior"]),
                "% Retención":       f"{(tot - r['nuevas']) / sdf.loc[sdf['camp_n'] == r['camp_n'] - 1, 'total'].values[0] * 100:.1f}%"
                                     if r["camp_n"] > camps_n[0] and sdf.loc[sdf["camp_n"] == r["camp_n"] - 1, "total"].values[0] > 0 else "—",
                "Persistentes":      int(r["persistentes"]),
                "Salen Sig. Camp.":  int(r["salen"]),
                "Fugadas (3c)":      int(r["fugadas"]),
                "% Fuga":            f"{r['fugadas']/tot*100:.1f}%" if tot else "—",
                "Inactiva":          int(r["Inactiva_total"]),
                "Mora 1":            int(r["Mora 1_total"]),
                "Mora 2":            int(r["Mora 2_total"]),
                "Mora 3":            int(r["Mora 3_total"]),
                "Saldo":             fmt_currency(r["saldo_total"]) if saldo_col else "—",
            })
        st.dataframe(pd.DataFrame(exec_rows), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # SUBTAB 2 — Por Campaña
    # ══════════════════════════════════════════
    with subtab2:
        st.markdown("<br>", unsafe_allow_html=True)

        sel_camp = st.selectbox("Seleccionar campaña:", sdf["camp_label"].tolist(), key="trk_sel_camp")
        r = sdf[sdf["camp_label"] == sel_camp].iloc[0]
        tot = int(r["total"])
        prev_lbl = f"C-{int(r['camp_n'])-1}" if r["camp_n"] > 1 else None

        # KPIs
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.metric("Total damas", f"{tot:,}")
        with c2: st.metric("% del Pool", f"{r['pct_pool']:.1f}%")
        with c3:
            st.metric("Nuevas", f"{int(r['nuevas']):,}",
                      delta=f"{r['nuevas']/tot*100:.1f}%" if tot else None, delta_color="off")
        with c4:
            st.metric(f"De {prev_lbl}" if prev_lbl else "De anterior", f"{int(r['de_anterior']):,}",
                      delta=f"{r['de_anterior']/tot*100:.1f}%" if tot else None, delta_color="off")
        with c5:
            st.metric("Fugadas (3c)", f"{int(r['fugadas']):,}",
                      delta=f"{r['fugadas']/tot*100:.1f}%" if tot else None, delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabla mora detallada
        st.markdown("**Desglose por estado de mora:**")
        detail_rows = []
        for mora in MORA_LEVELS:
            m_tot  = int(r.get(f"{mora}_total", 0))
            m_nue  = int(r.get(f"{mora}_nuevas", 0))
            m_ant  = int(r.get(f"{mora}_de_anterior", 0))
            m_per  = int(r.get(f"{mora}_persistentes", 0))
            m_sal  = int(r.get(f"{mora}_salen", 0))
            m_fug  = int(r.get(f"{mora}_fugadas", 0))
            m_sld  = r.get(f"{mora}_saldo", 0)
            detail_rows.append({
                "Estado":       mora,
                "Total":        m_tot,
                "%":            f"{m_tot/tot*100:.1f}%" if tot else "—",
                "Nuevas":       m_nue,
                "% Nuevas":     f"{m_nue/m_tot*100:.1f}%" if m_tot else "—",
                "De Anterior":  m_ant,
                "% De Ant.":    f"{m_ant/m_tot*100:.1f}%" if m_tot else "—",
                "Persistentes": m_per,
                "Salen":        m_sal,
                "Fugadas":      m_fug,
                "% Fuga":       f"{m_fug/m_tot*100:.1f}%" if m_tot else "—",
                "Saldo":        fmt_currency(m_sld) if saldo_col else "—",
            })

        def _color_mora(row):
            c = {"Inactiva": "background-color:#E2E8F0",
                 "Mora 1": "background-color:#FEF9C3",
                 "Mora 2": "background-color:#FFEDD5",
                 "Mora 3": "background-color:#FEE2E2"}.get(row["Estado"], "")
            return [c] * len(row)

        st.dataframe(
            pd.DataFrame(detail_rows).style.apply(_color_mora, axis=1),
            use_container_width=True, hide_index=True,
        )

        # Inactivas del período anterior
        fi = int(r.get("fi_total", 0))
        if fi > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"**Inactivas de {prev_lbl} que reaparecen en {sel_camp}: {fi:,}**")
            fi_rows = []
            for mora in MORA_LEVELS:
                cnt = int(r.get(f"fi_to_{mora}", 0))
                m_tot_d = int(r.get(f"{mora}_total", 0))
                fi_rows.append({
                    "→ Estado":           mora,
                    "Cuentas":            cnt,
                    "% de Inactivas":     f"{cnt/fi*100:.1f}%" if fi else "—",
                    f"% del total {mora}":f"{cnt/m_tot_d*100:.1f}%" if m_tot_d else "—",
                })
            st.dataframe(pd.DataFrame(fi_rows), use_container_width=True, hide_index=True)

        # Dos gráficas más claras: donut de composición + barras de movimiento
        st.markdown("<br>", unsafe_allow_html=True)
        gcol1, gcol2 = st.columns(2)

        # — Gráfica 1: Donut composición por mora ——————————————————————
        with gcol1:
            donut_labels = [m for m in MORA_LEVELS if int(r.get(f"{m}_total", 0)) > 0]
            donut_values = [int(r.get(f"{m}_total", 0)) for m in donut_labels]
            donut_colors = [MORA_COLORS[m] for m in donut_labels]
            fig_donut = go.Figure(go.Pie(
                labels=donut_labels, values=donut_values,
                marker_colors=donut_colors,
                hole=0.55,
                textinfo="label+percent",
                textfont=dict(size=11),
                hovertemplate="<b>%{label}</b><br>%{value:,} damas (%{percent})<extra></extra>",
            ))
            total_camp = sum(donut_values)
            fig_donut.add_annotation(
                text=f"<b>{total_camp:,}</b><br>total",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color=COLORS["primary"]),
            )
            fig_donut.update_layout(
                **{**PLOTLY_LAYOUT, "margin": dict(t=10, b=60, l=10, r=10)},
                showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5),
                height=300,
                title_text="Composición por estado",
                title_font=dict(size=12, color=COLORS["primary"]),
            )
            st.plotly_chart(fig_donut, use_container_width=True, key=f"trk_donut_{sel_camp}")

        # — Gráfica 2: Movimientos como tarjetas de métricas ——————————————
        with gcol2:
            st.markdown(
                f"<p style='font-size:12px;color:{COLORS['primary']};font-weight:600;"
                f"margin:0 0 0.5rem'>Movimiento de cuentas</p>",
                unsafe_allow_html=True,
            )
            mov_items = [
                ("Nuevas",       int(r.get("nuevas", 0)),       COLORS["success"], "↑"),
                ("De Anterior",  int(r.get("de_anterior", 0)),  COLORS["accent"],  "→"),
                ("Persistentes", int(r.get("persistentes", 0)), COLORS["warning"], "⟳"),
                ("Fugadas",      int(r.get("fugadas", 0)),      COLORS["danger"],  "↓"),
            ]
            m1, m2 = st.columns(2)
            for i, (label, val, color, icon) in enumerate(mov_items):
                with (m1 if i % 2 == 0 else m2):
                    st.markdown(
                        f"<div style='background:{color};border-radius:14px;"
                        f"padding:1rem 0.8rem;margin-bottom:0.6rem;text-align:center;"
                        f"box-shadow:0 2px 6px rgba(0,0,0,0.12)'>"
                        f"<p style='margin:0;font-size:1.8rem;font-weight:800;color:white;"
                        f"line-height:1'>{val:,}</p>"
                        f"<p style='margin:0.3rem 0 0;font-size:0.68rem;color:rgba(255,255,255,0.9);"
                        f"font-weight:700;text-transform:uppercase;letter-spacing:.06em'>"
                        f"{icon} {label}</p></div>",
                        unsafe_allow_html=True,
                    )

    # ══════════════════════════════════════════
    # SUBTAB 3 — Por Mora
    # ══════════════════════════════════════════
    with subtab3:
        st.markdown("<br>", unsafe_allow_html=True)

        sel_mora = st.selectbox("Seleccionar estado:", MORA_LEVELS, key="trk_sel_mora")

        # Trend table for selected mora
        mora_rows = []
        for _, r in sdf.iterrows():
            tot = int(r["total"])
            m_tot = int(r.get(f"{sel_mora}_total", 0))
            mora_rows.append({
                "Campaña":       r["camp_label"],
                "Total Estado":  m_tot,
                "% Campaña":     f"{m_tot/tot*100:.1f}%" if tot else "—",
                "% Pool":        f"{m_tot/pool_size*100:.1f}%" if pool_size else "—",
                "Nuevas":        int(r.get(f"{sel_mora}_nuevas", 0)),
                "% Nuevas":      f"{r.get(f'{sel_mora}_nuevas',0)/m_tot*100:.1f}%" if m_tot else "—",
                "De Anterior":   int(r.get(f"{sel_mora}_de_anterior", 0)),
                "% Retención":   f"{r.get(f'{sel_mora}_de_anterior',0)/m_tot*100:.1f}%" if m_tot else "—",
                "Persistentes":  int(r.get(f"{sel_mora}_persistentes", 0)),
                "Fugadas":       int(r.get(f"{sel_mora}_fugadas", 0)),
                "% Fuga":        f"{r.get(f'{sel_mora}_fugadas',0)/m_tot*100:.1f}%" if m_tot else "—",
                "Saldo":         fmt_currency(r.get(f"{sel_mora}_saldo", 0)) if saldo_col else "—",
            })
        st.dataframe(pd.DataFrame(mora_rows), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Line chart for the selected mora
        fig_mora_line = go.Figure()
        for key, label, color, dash in [
            (f"{sel_mora}_total",       "Total",       MORA_COLORS[sel_mora], "solid"),
            (f"{sel_mora}_nuevas",      "Nuevas",      COLORS["success"],     "dash"),
            (f"{sel_mora}_de_anterior", "De Anterior", COLORS["accent"],      "dot"),
            (f"{sel_mora}_fugadas",     "Fugadas",     COLORS["danger"],      "longdash"),
        ]:
            fig_mora_line.add_trace(go.Scatter(
                x=sdf["camp_label"], y=sdf[key],
                mode="lines+markers", name=label,
                line=dict(color=color, width=2, dash=dash), marker=dict(size=6),
                hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y:,}}<extra></extra>",
            ))
        fig_mora_line.update_layout(
            **PLOTLY_LAYOUT,
            title_text=f"{sel_mora} — cómo evoluciona en cada campaña",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        )
        chart_card(f"Tendencia {sel_mora}", fig_mora_line, key=f"trk_ml_{sel_mora}", height_normal=380)

        st.markdown("<br>", unsafe_allow_html=True)

        # Comparativa todos los estados — una línea por mora
        st.markdown("#### Comparativa de todos los estados")
        fig_all = go.Figure()
        for mora in MORA_LEVELS:
            fig_all.add_trace(go.Scatter(
                x=sdf["camp_label"], y=sdf[f"{mora}_total"],
                mode="lines+markers", name=mora,
                line=dict(color=MORA_COLORS[mora], width=2), marker=dict(size=6),
                hovertemplate=f"<b>%{{x}}</b><br>{mora}: %{{y:,}}<extra></extra>",
            ))
        fig_all.update_layout(
            **PLOTLY_LAYOUT,
            title_text="Cuántas damas hay en cada estado por campaña",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        )
        chart_card("Todos los estados", fig_all, key="trk_all_mora", height_normal=380)

    # ══════════════════════════════════════════
    # SUBTAB 4 — Salidas
    # ══════════════════════════════════════════
    with subtab4:
        st.markdown("<br>", unsafe_allow_html=True)

        if exits_df.empty:
            st.info("No se encontraron cuentas con salida permanente.")
        else:
            n_exits = len(exits_df)
            e1, e2, e3 = st.columns(3)
            with e1: st.metric("Total salidas permanentes", f"{n_exits:,}")
            with e2: st.metric("% del pool", f"{n_exits/pool_size*100:.1f}%" if pool_size else "—")
            with e3:
                still = pool_size - n_exits
                st.metric("Aún presentes en C10", f"{still:,}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Salidas por campaña y mora
            grp = (
                exits_df.groupby(["Última Campaña", "Estado al Salir"])
                .agg(Cuentas=("NoDama", "count"), Saldo=("Saldo al Salir", "sum"))
                .reset_index()
            )
            pivot_exit = grp.pivot_table(
                index="Última Campaña", columns="Estado al Salir",
                values="Cuentas", fill_value=0, aggfunc="sum"
            ).reindex(columns=[m for m in MORA_LEVELS if m in grp["Estado al Salir"].values], fill_value=0)

            col_e1, col_e2 = st.columns([3, 2])
            with col_e1:
                fig_exit = go.Figure()
                for mora in MORA_LEVELS:
                    if mora in grp["Estado al Salir"].values:
                        sub_e = grp[grp["Estado al Salir"] == mora].set_index("Última Campaña")
                        fig_exit.add_trace(go.Bar(
                            x=sub_e.index, y=sub_e["Cuentas"],
                            name=mora, marker_color=MORA_COLORS[mora],
                            hovertemplate=f"<b>%{{x}}</b><br>{mora}: %{{y:,}}<extra></extra>",
                        ))
                fig_exit.update_layout(
                    **PLOTLY_LAYOUT, barmode="stack",
                    title_text="Damas que salieron de la cartera por campaña",
                    title_font=dict(size=12, color=COLORS["primary"]),
                    xaxis=dict(type="category", categoryorder="array",
                               categoryarray=[f"C-{c}" for c in range(1, 11)], **_AXIS_DEFAULTS),
                    yaxis=dict(title="Cuentas", **_AXIS_DEFAULTS),
                    legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
                    height=360,
                )
                st.plotly_chart(fig_exit, use_container_width=True, key="trk_exit_bar")

            with col_e2:
                st.markdown("**Distribución por estado al salir:**")
                exit_by_mora = exits_df["Estado al Salir"].value_counts().reset_index()
                exit_by_mora.columns = ["Estado", "Cuentas"]
                exit_by_mora["% del Total"] = exit_by_mora["Cuentas"].apply(
                    lambda v: f"{v/n_exits*100:.1f}%"
                )
                st.dataframe(exit_by_mora, use_container_width=True, hide_index=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Saldo promedio al salir por estado:**")
                saldo_by_mora = exits_df.groupby("Estado al Salir")["Saldo al Salir"].mean().reset_index()
                saldo_by_mora.columns = ["Estado", "Saldo Promedio"]
                saldo_by_mora["Saldo Promedio"] = saldo_by_mora["Saldo Promedio"].apply(fmt_currency)
                st.dataframe(saldo_by_mora, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Listado de salidas permanentes")
            st.dataframe(
                exits_df.head(3000),
                use_container_width=True, hide_index=True, height=400,
            )

    # ══════════════════════════════════════════
    # SUBTAB 5 — Transiciones
    # ══════════════════════════════════════════
    with subtab5:
        st.markdown("<br>", unsafe_allow_html=True)

        if trans_df.empty:
            st.info("No hay datos de transición disponibles.")
        else:
            trans_options = [
                f"C-{camps_n[i]} → C-{camps_n[i+1]}" for i in range(len(camps_n)-1)
            ]
            sel_t = st.selectbox("Seleccionar transición:", trans_options, key="trk_sel_trans")
            c_from = sel_t.split("→")[0].strip()
            c_to   = sel_t.split("→")[1].strip()

            sub_t = trans_df[(trans_df["de"] == c_from) & (trans_df["a"] == c_to)]
            pivot_t = (
                sub_t.pivot_table(index="origen", columns="destino",
                                  values="cuentas", fill_value=0, aggfunc="sum")
                .reindex(index=MORA_LEVELS, columns=MORA_LEVELS, fill_value=0)
            )
            total_sh = int(pivot_t.values.sum())

            st.markdown(f"**Damas presentes en ambas campañas: {total_sh:,}**")
            st.caption("Fila = estado en campaña origen  |  Columna = estado en campaña destino")

            col_h, col_k = st.columns([3, 2])
            with col_h:
                z = pivot_t.values.tolist()
                z_pct = [[round(v/total_sh*100,1) if total_sh else 0 for v in row] for row in z]
                text_h = [[f"{v:,}\n({p}%)" for v, p in zip(rv, rp)]
                          for rv, rp in zip(z, z_pct)]
                fig_h = go.Figure(go.Heatmap(
                    z=z, x=[f"→ {m}" for m in MORA_LEVELS], y=MORA_LEVELS,
                    text=text_h, texttemplate="%{text}",
                    textfont=dict(size=11),
                    colorscale=[[0,"#FFFFFF"],[0.3,"#BFDBFE"],[0.7,"#3B82F6"],[1,"#1A3C6E"]],
                    showscale=True,
                    hovertemplate="<b>%{y} → %{x}</b><br>%{z:,} damas<extra></extra>",
                ))
                fig_h.update_layout(
                    **PLOTLY_LAYOUT,
                    title_text=f"¿A dónde fueron las damas de {c_from} en {c_to}?",
                    title_font=dict(size=12, color=COLORS["primary"]),
                    xaxis=dict(title=f"Estado en {c_to}", **_AXIS_DEFAULTS),
                    yaxis=dict(title=f"Estado en {c_from}", autorange="reversed", **_AXIS_DEFAULTS),
                    height=360,
                )
                st.plotly_chart(fig_h, use_container_width=True, key=f"trk_heat_{c_from}_{c_to}")

            with col_k:
                st.markdown(f"**Tasas de transición desde {c_from}:**")
                for mora_o in MORA_LEVELS:
                    o_tot = int(pivot_t.loc[mora_o].sum()) if mora_o in pivot_t.index else 0
                    if o_tot == 0:
                        continue
                    bg = {"Inactiva":"#E2E8F0","Mora 1":"#FEF9C3","Mora 2":"#FFEDD5","Mora 3":"#FEE2E2"}.get(mora_o,"#fff")
                    detail = "  ·  ".join(
                        f"→ {d}: <b>{int(pivot_t.loc[mora_o,d])}</b> ({round(pivot_t.loc[mora_o,d]/o_tot*100,1)}%)"
                        for d in MORA_LEVELS if mora_o in pivot_t.index and d in pivot_t.columns
                    )
                    st.markdown(
                        f"<div style='background:{bg};padding:6px 10px;border-radius:6px;"
                        f"margin-bottom:6px'><b>{mora_o}</b> — {o_tot:,} damas<br>{detail}</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # Tabla resumen todas las transiciones
            with st.expander("Ver tabla de todas las transiciones"):
                all_t_rows = []
                for opt in trans_options:
                    cf = opt.split("→")[0].strip()
                    ct = opt.split("→")[1].strip()
                    s  = trans_df[(trans_df["de"]==cf)&(trans_df["a"]==ct)]
                    pv = (s.pivot_table(index="origen",columns="destino",
                                        values="cuentas",fill_value=0,aggfunc="sum")
                           .reindex(index=MORA_LEVELS,columns=MORA_LEVELS,fill_value=0))
                    for mo in MORA_LEVELS:
                        ot = int(pv.loc[mo].sum()) if mo in pv.index else 0
                        if ot == 0:
                            continue
                        for md in MORA_LEVELS:
                            v = int(pv.loc[mo,md]) if mo in pv.index and md in pv.columns else 0
                            all_t_rows.append({
                                "Transición": opt, "Origen": mo, "Destino": md,
                                "Damas": v,
                                "% del Origen": f"{v/ot*100:.1f}%" if ot else "—",
                            })
                if all_t_rows:
                    st.dataframe(pd.DataFrame(all_t_rows), use_container_width=True,
                                 hide_index=True, height=400)

    # ══════════════════════════════════════════
    # SUBTAB 6 — Flujo Inactivas → Mora 1 → Mora 2 → Mora 3
    # ══════════════════════════════════════════
    with subtab6:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h2 style='font-size:1.3rem'>Flujo: Inactivas → Mora 1 → Mora 2 → Mora 3</h2>"
            "<p style='font-size:0.85rem'>Seguimiento de cuentas Inactivas (IdSituacion = 0) "
            "y su progresión hacia Mora 1, Mora 2 y Mora 3.</p></div>",
            unsafe_allow_html=True,
        )

        # Las Inactivas ya están en la base de moras (IdSituacion=0 → _mora="Inactiva")
        # Las usamos como el pool de "pendientes de inactivas" por campaña
        FI_COLORS = {
            "Mora1 desde Inactivas": "#7C3AED",
            "Mora1 Nuevas":          "#16A34A",
            "Nuevas M2-M3":          "#2563EB",
            "Permanecen M2":         "#EAB308",
            "Permanecen M3":         "#F97316",
            "No continúan":          "#EF4444",
        }

        # Pool global de Inactivas: todas las NoDamas que aparecen como Inactiva en cualquier campaña
        pendientes_inac = set().union(*[mora_sets[(c, "Inactiva")] for c in camps_n])

        if not pendientes_inac:
            st.info(
                "No se encontraron cuentas Inactivas (IdSituacion = 0) en la base de moras. "
                "Verifica que el archivo contenga la columna **IdSituacion**."
            )
        else:
            # ── Calcular métricas por campaña ────────────────────────────
            fi_rows = []
            for i, c in enumerate(camps_n):
                prev_c = camps_n[i - 1] if i > 0 else None
                m1 = mora_sets[(c, "Mora 1")]
                m2 = mora_sets[(c, "Mora 2")]
                m3 = mora_sets[(c, "Mora 3")]
                all_cur  = sets[c]

                # Mora 1: viene del pool global de Inactivas vs es nueva entrada
                mora1_desde_inac = m1 & pendientes_inac   # en M1 Y alguna vez fue Inactiva
                mora1_nueva      = m1 - pendientes_inac   # en M1, nunca apareció como Inactiva

                if prev_c:
                    m1_prev  = mora_sets[(prev_c, "Mora 1")]
                    m2_prev  = mora_sets[(prev_c, "Mora 2")]
                    all_prev = sets[prev_c]
                    permanecen_m2 = m2 & m1_prev
                    permanecen_m3 = m3 & m2_prev
                    nuevas_m2     = m2 - m1_prev
                    nuevas_m3     = m3 - m2_prev
                    no_continuan  = all_prev - all_cur
                else:
                    permanecen_m2 = set()
                    permanecen_m3 = set()
                    nuevas_m2     = m2
                    nuevas_m3     = m3
                    no_continuan  = set()

                nuevas_m2_m3    = nuevas_m2 | nuevas_m3
                activos         = len(all_cur)
                total_reportado = activos + len(no_continuan)

                fi_rows.append({
                    "camp_n":                c,
                    "Campaña":               f"C-{c}",
                    "Inactivas (camp)":      len(mora_sets[(c, "Inactiva")]),
                    "Mora1 desde Inactivas": len(mora1_desde_inac),
                    "Mora1 Nuevas":          len(mora1_nueva),
                    "Nuevas M2-M3":          len(nuevas_m2_m3),
                    "Permanecen M2":         len(permanecen_m2),
                    "Permanecen M3":         len(permanecen_m3),
                    "No continúan":          len(no_continuan),
                    "Activos":               activos,
                    "Total":                 total_reportado,
                    "_m1_inac_pct": round(len(mora1_desde_inac) / len(m1) * 100, 1) if m1 else 0,
                    "_perm_m2_pct": round(len(permanecen_m2) / len(mora_sets[(prev_c, "Mora 1")]) * 100, 1)
                                    if prev_c and mora_sets[(prev_c, "Mora 1")] else 0,
                    "_perm_m3_pct": round(len(permanecen_m3) / len(mora_sets[(prev_c, "Mora 2")]) * 100, 1)
                                    if prev_c and mora_sets[(prev_c, "Mora 2")] else 0,
                    "_fuga_pct":    round(len(no_continuan) / len(sets[prev_c]) * 100, 1)
                                    if prev_c and sets[prev_c] else 0,
                })

            fi_df = pd.DataFrame(fi_rows)

            # ── KPIs ──────────────────────────────────────────────────────
            total_m1_all  = sum(len(mora_sets[(c, "Mora 1")]) for c in camps_n)
            total_inac_all = sum(len(mora_sets[(c, "Inactiva")]) for c in camps_n)
            total_inac_m1 = fi_df["Mora1 desde Inactivas"].sum()
            avg_conv      = fi_df["_m1_inac_pct"].iloc[1:].mean() if len(fi_df) > 1 else 0
            avg_perm_m2   = fi_df["_perm_m2_pct"].iloc[1:].mean() if len(fi_df) > 1 else 0
            avg_perm_m3   = fi_df["_perm_m3_pct"].iloc[1:].mean() if len(fi_df) > 1 else 0
            avg_fuga      = fi_df["_fuga_pct"].iloc[1:].mean() if len(fi_df) > 1 else 0

            ki1, ki2, ki3, ki4, ki5 = st.columns(5)
            with ki1: st.metric("Total Inactivas (todas las camps)", f"{total_inac_all:,}")
            with ki2: st.metric("Inactivas → Mora1 (acumulado)", f"{total_inac_m1:,}",
                                delta=f"Conv. prom. {avg_conv:.1f}%" if avg_conv else None)
            with ki3: st.metric("Permanencia M1→M2 prom.", f"{avg_perm_m2:.1f}%")
            with ki4: st.metric("Permanencia M2→M3 prom.", f"{avg_perm_m3:.1f}%")
            with ki5: st.metric("Fuga promedio", f"{avg_fuga:.1f}%")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabla resumen ─────────────────────────────────────────────
            cat_cols = ["Inactivas (camp)", "Mora1 desde Inactivas", "Mora1 Nuevas",
                        "Nuevas M2-M3", "Permanecen M2", "Permanecen M3",
                        "No continúan", "Total"]
            display_df = fi_df[["Campaña"] + cat_cols].copy()
            totals = {"Campaña": "TOTAL"}
            for col in cat_cols:
                totals[col] = int(display_df[col].sum())
            display_df = pd.concat([display_df, pd.DataFrame([totals])], ignore_index=True)
            st.markdown("#### Resumen por Campaña")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Gráficas ──────────────────────────────────────────────────
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                fig_fi = go.Figure()
                stacked_cols = ["Mora1 desde Inactivas", "Mora1 Nuevas", "Nuevas M2-M3",
                                "Permanecen M2", "Permanecen M3", "No continúan"]
                for col in stacked_cols:
                    fig_fi.add_trace(go.Bar(
                        x=fi_df["Campaña"], y=fi_df[col], name=col,
                        marker_color=FI_COLORS[col],
                        hovertemplate=f"<b>%{{x}}</b><br>{col}: %{{y:,}}<extra></extra>",
                    ))
                fig_fi.update_layout(
                    **PLOTLY_LAYOUT, barmode="stack",
                    title_text="Origen de las cuentas por campaña",
                    title_font=dict(size=12, color=COLORS["primary"]),
                    xaxis=dict(title="Campaña", **_AXIS_DEFAULTS),
                    yaxis=dict(title="Cuentas", **_AXIS_DEFAULTS),
                    legend=dict(orientation="h", yanchor="top", y=-0.18,
                                xanchor="center", x=0.5, font=dict(size=9)),
                    height=380,
                )
                st.plotly_chart(fig_fi, use_container_width=True, key="fi_bar_stacked")

            with col_g2:
                fig_perm = go.Figure()
                fig_perm.add_trace(go.Scatter(
                    x=fi_df["Campaña"], y=fi_df["Inactivas (camp)"],
                    mode="lines+markers", name="Inactivas",
                    line=dict(color="#94A3B8", width=2),
                    hovertemplate="<b>%{x}</b><br>Inactivas: %{y:,}<extra></extra>",
                ))
                fig_perm.add_trace(go.Scatter(
                    x=fi_df["Campaña"], y=fi_df["Mora1 desde Inactivas"],
                    mode="lines+markers", name="→ Mora1",
                    line=dict(color=FI_COLORS["Mora1 desde Inactivas"], width=2),
                    hovertemplate="<b>%{x}</b><br>Mora1 desde Inactivas: %{y:,}<extra></extra>",
                ))
                fig_perm.add_trace(go.Scatter(
                    x=fi_df["Campaña"], y=fi_df["Permanecen M2"],
                    mode="lines+markers", name="Perm. M2",
                    line=dict(color=FI_COLORS["Permanecen M2"], width=2),
                    hovertemplate="<b>%{x}</b><br>Permanecen M2: %{y:,}<extra></extra>",
                ))
                fig_perm.add_trace(go.Scatter(
                    x=fi_df["Campaña"], y=fi_df["Permanecen M3"],
                    mode="lines+markers", name="Perm. M3",
                    line=dict(color=FI_COLORS["Permanecen M3"], width=2),
                    hovertemplate="<b>%{x}</b><br>Permanecen M3: %{y:,}<extra></extra>",
                ))
                fig_perm.update_layout(
                    **PLOTLY_LAYOUT,
                    title_text="Inactivas que pasan a Mora 1, 2 y 3",
                    title_font=dict(size=12, color=COLORS["primary"]),
                    xaxis=dict(title="Campaña", **_AXIS_DEFAULTS),
                    yaxis=dict(title="Cuentas", **_AXIS_DEFAULTS),
                    legend=dict(orientation="h", yanchor="top", y=-0.18,
                                xanchor="center", x=0.5, font=dict(size=9)),
                    height=380,
                )
                st.plotly_chart(fig_perm, use_container_width=True, key="fi_line_perm")

            # ── Tabla de tasas ────────────────────────────────────────────
            st.markdown("#### Tasas de conversión y permanencia por transición")
            perm_rows = []
            for i, row in fi_df.iterrows():
                if row["camp_n"] == camps_n[0]:
                    continue
                prev_c_i = camps_n[i - 1]
                perm_rows.append({
                    "Transición":              f"C-{prev_c_i} → {row['Campaña']}",
                    "Inactivas anterior":      len(mora_sets[(prev_c_i, "Inactiva")]),
                    "→ Mora1":                 row["Mora1 desde Inactivas"],
                    "Conv. Inac→M1":           f"{row['_m1_inac_pct']:.1f}%",
                    "M1 anterior":             len(mora_sets[(prev_c_i, "Mora 1")]),
                    "Permanecen M2":           row["Permanecen M2"],
                    "Tasa perm. M2":           f"{row['_perm_m2_pct']:.1f}%",
                    "M2 anterior":             len(mora_sets[(prev_c_i, "Mora 2")]),
                    "Permanecen M3":           row["Permanecen M3"],
                    "Tasa perm. M3":           f"{row['_perm_m3_pct']:.1f}%",
                    "No continúan":            row["No continúan"],
                    "Tasa fuga":               f"{row['_fuga_pct']:.1f}%",
                })
            if perm_rows:
                st.dataframe(pd.DataFrame(perm_rows), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
#  PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────

def render_welcome():
    st.markdown(
        f"""
        <div style='text-align:center; padding: 3rem 0 1rem;'>
            <h1 style='font-size:2.8rem; color:{COLORS["primary"]}'> Dashboard de Gestión de Cartera</h1>
            <p style='color:{COLORS["muted"]}; font-size:1.1rem; max-width:600px; margin:0 auto 2rem;'>
                Visualiza, analiza y actúa sobre tu cartera de cobranza en tiempo real.
                Carga tus archivos Excel para comenzar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "", "KPIs en Tiempo Real",     "Total cartera, cobrado, pendiente y % de cumplimiento."),
        (c2, "", "RSI y Series Temporales", "Análisis técnico RSI-14 con zonas de sobrecompra/sobreventa."),
        (c3, "", "Clasificación de Moras",  "Identifica damas en mora, nivel de riesgo y monto en riesgo por campaña."),
    ]:
        with col:
            st.markdown(
                f"<div class='card' style='text-align:center'>"
                f"<div style='font-size:2rem'>{icon}</div>"
                f"<b style='color:{COLORS['primary']}'>{title}</b><br>"
                f"<small style='color:{COLORS['muted']}'>{desc}</small>"
                f"</div>",
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────
#  INTERNO — DASHBOARD DE COBRANZA
# ─────────────────────────────────────────────

def _render_interno_tab():
    """Renderiza el contenido completo de la pestaña 🏢 Interno."""

    # ── Inicializar session state ─────────────────────────────────────
    for key, default in [
        ("df_tel", None),
        ("df_campo", None),
        ("int_tel_names", []),
        ("int_campo_names", []),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Banner ───────────────────────────────────────────────────────
    st.markdown(
        "<div class='kpi-banner'>"
        "<h1>🏢 Dashboard de Cobranza — Interno</h1>"
        "<p>Gestión telefónica, visitas de campo y evolución de mora por temporalidad</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Carga de archivos ────────────────────────────────────────────
    with st.expander("📂 Cargar archivos de gestión", expanded=(
        st.session_state.df_tel is None and st.session_state.df_campo is None
        and st.session_state.get("df_cobranza") is None
    )):
        up_c1, up_c2, up_c3 = st.columns(3)

        with up_c1:
            st.markdown("**Gestión Telefónica**")
            st.caption("Hasta 6 archivos (uno por mes) — Columnas: NoDama, Fecha gestión, Tipificación (código), Promesa de pago")
            tel_files = st.file_uploader(
                "Gestión Telefónica", type=["xlsx", "xls"],
                label_visibility="collapsed", key="up_int_tel",
                accept_multiple_files=True,
            )
            if tel_files:
                names = sorted([f.name for f in tel_files])
                if names != st.session_state.int_tel_names:
                    try:
                        _dfs = []
                        for _f in tel_files:
                            _df = read_excel_safe(_f)
                            if _df is not None and not _df.empty:
                                _df["_mes_origen"] = _f.name
                                _dfs.append(_df)
                        if _dfs:
                            st.session_state.df_tel = pd.concat(_dfs, ignore_index=True)
                            st.session_state.int_tel_names = names
                    except Exception as e:
                        st.error(f"Error al leer Gestión Telefónica: {e}")
            if st.session_state.df_tel is not None:
                df_tel_info = st.session_state.df_tel
                n_archivos = len(st.session_state.int_tel_names)
                st.markdown(
                    f"<span style='background:#dcfce7;color:#16a34a;padding:2px 10px;"
                    f"border-radius:99px;font-size:0.78rem;font-weight:600'>"
                    f"✓ {n_archivos} archivo{'s' if n_archivos != 1 else ''} — {len(df_tel_info):,} registros</span>",
                    unsafe_allow_html=True,
                )

        with up_c2:
            st.markdown("**Visitas de Campo**")
            st.caption("Columnas esperadas: NoDama, Fecha dispositivo, Estatus visita, Gestor")
            campo_file = st.file_uploader(
                "Visitas de Campo", type=["xlsx", "xls"],
                label_visibility="collapsed", key="up_int_campo"
            )
            if campo_file:
                names = [campo_file.name]
                if names != st.session_state.int_campo_names:
                    try:
                        st.session_state.df_campo = read_excel_safe(campo_file)
                        st.session_state.int_campo_names = names
                    except Exception as e:
                        st.error(f"Error al leer Visitas de Campo: {e}")
            if st.session_state.df_campo is not None:
                df_campo_info = st.session_state.df_campo
                st.markdown(
                    f"<span style='background:#dcfce7;color:#16a34a;padding:2px 10px;"
                    f"border-radius:99px;font-size:0.78rem;font-weight:600'>"
                    f"✓ Cargado — {len(df_campo_info):,} registros</span>",
                    unsafe_allow_html=True,
                )

        with up_c3:
            st.markdown("**Base de Cobranza**")
            st.caption("Campos: Campaña, División, Ruta, Zona, NoDama, Segmento Mora, Saldo Asignado, Pago Aplicado, Visita, Resultado, Dictaminación, Estatus")
            cob_file = st.file_uploader(
                "Base de Cobranza", type=["xlsx", "xls"],
                label_visibility="collapsed", key="up_int_cob"
            )
            if cob_file:
                names = [cob_file.name]
                if names != st.session_state.get("int_cob_names", []):
                    try:
                        st.session_state.df_cobranza = read_excel_safe(cob_file)
                        st.session_state.int_cob_names = names
                    except Exception as e:
                        st.error(f"Error al leer Base de Cobranza: {e}")
            if st.session_state.get("df_cobranza") is not None:
                _cob_info = st.session_state.df_cobranza
                st.markdown(
                    f"<span style='background:#dcfce7;color:#16a34a;padding:2px 10px;"
                    f"border-radius:99px;font-size:0.78rem;font-weight:600'>"
                    f"✓ Cargado — {len(_cob_info):,} registros</span>",
                    unsafe_allow_html=True,
                )

        if st.session_state.get("df_moras") is not None:
            st.markdown(
                f"<span style='background:#dbeafe;color:#1d4ed8;padding:2px 10px;"
                f"border-radius:99px;font-size:0.78rem;font-weight:600'>"
                f"✓ Base de moras — {len(st.session_state.df_moras):,} registros (desde sección Arabela)</span>",
                unsafe_allow_html=True,
            )
        else:
            st.info("ℹ️ Carga el archivo de Moras en la sección Arabela para habilitar todos los análisis.")

    df_tel   = st.session_state.df_tel
    df_campo = st.session_state.df_campo
    df_moras = st.session_state.get("df_moras")

    # ── Detección de columnas ────────────────────────────────────────
    tel_cols   = {}
    campo_cols = {}

    if df_tel is not None:
        tel_cols = {
            "nodama": _find_col(df_tel, ["nodama", "no dama", "numdama", "número de dama", "num_dama", "dama"]),
            "camp":   _find_col(df_tel, ["campaña", "campana", "camp", "periodo", "anio", "año", "aniocampaña"]),
            "fecha":  _find_col(df_tel, ["fecha", "date", "fechagestión", "fecha_gestion", "fecha gestion"]),
            "tipif":  _find_col(df_tel, ["tipif", "tipificacion", "estatus", "status", "layout", "codigo"]),
            "promesa": _find_col(df_tel, ["promesa", "promise", "compromiso"]),
        }
        with st.expander("⚙️ Ajustar columnas — Gestión Telefónica"):
            all_tel_cols = list(df_tel.columns)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                tel_cols["nodama"] = st.selectbox(
                    "N° Dama", all_tel_cols,
                    index=all_tel_cols.index(tel_cols["nodama"]) if tel_cols["nodama"] in all_tel_cols else 0,
                    key="tel_nodama"
                )
            with c2:
                tel_cols["fecha"] = st.selectbox(
                    "Fecha gestión", all_tel_cols,
                    index=all_tel_cols.index(tel_cols["fecha"]) if tel_cols["fecha"] in all_tel_cols else 0,
                    key="tel_fecha"
                )
            with c3:
                tel_cols["tipif"] = st.selectbox(
                    "Tipificación", all_tel_cols,
                    index=all_tel_cols.index(tel_cols["tipif"]) if tel_cols["tipif"] in all_tel_cols else 0,
                    key="tel_tipif"
                )
            with c4:
                promesa_options = ["(ninguna)"] + all_tel_cols
                _promesa_idx = promesa_options.index(tel_cols["promesa"]) if tel_cols["promesa"] in promesa_options else 0
                _promesa_sel = st.selectbox("Promesa de pago", promesa_options, index=_promesa_idx, key="tel_promesa")
                tel_cols["promesa"] = None if _promesa_sel == "(ninguna)" else _promesa_sel

    if df_campo is not None:
        campo_cols = {
            "nodama": _find_col(df_campo, ["nodama", "no dama", "numdama", "número de dama", "num_dama", "dama"]),
            "camp":   _find_col(df_campo, ["campaña", "campana", "camp", "periodo", "anio", "año", "aniocampaña"]),
            "fecha":  _find_col(df_campo, ["fecha", "dispositivo", "fecha_dispositivo", "fecha dispositivo", "date"]),
            "estatus": _find_col(df_campo, ["estatus", "status", "resultado", "estado", "visita"]),
            "gestor":  _find_col(df_campo, ["gestor", "asesor", "cobrador", "agente", "agent"]),
        }
        with st.expander("⚙️ Ajustar columnas — Visitas de Campo"):
            all_campo_cols = list(df_campo.columns)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                campo_cols["nodama"] = st.selectbox(
                    "N° Dama", all_campo_cols,
                    index=all_campo_cols.index(campo_cols["nodama"]) if campo_cols["nodama"] in all_campo_cols else 0,
                    key="campo_nodama"
                )
            with c2:
                campo_cols["fecha"] = st.selectbox(
                    "Fecha dispositivo", all_campo_cols,
                    index=all_campo_cols.index(campo_cols["fecha"]) if campo_cols["fecha"] in all_campo_cols else 0,
                    key="campo_fecha"
                )
            with c3:
                campo_cols["estatus"] = st.selectbox(
                    "Estatus visita", all_campo_cols,
                    index=all_campo_cols.index(campo_cols["estatus"]) if campo_cols["estatus"] in all_campo_cols else 0,
                    key="campo_estatus"
                )
            with c4:
                campo_cols["gestor"] = st.selectbox(
                    "Gestor", all_campo_cols,
                    index=all_campo_cols.index(campo_cols["gestor"]) if campo_cols["gestor"] in all_campo_cols else 0,
                    key="campo_gestor"
                )

    # Columnas de moras
    mora_nodama_col = None
    mora_camp_col   = None
    mora_temp_col   = None
    mora_saldo_col  = None
    if df_moras is not None:
        mora_nodama_col = _find_col(df_moras, ["nodama", "no dama", "numdama", "dama"])
        mora_camp_col   = _find_col(df_moras, ["campaña", "campana", "camp", "periodo", "anio", "año"])
        mora_temp_col   = _find_col(df_moras, ["temporalidad", "mora", "nivel", "estado"])
        mora_saldo_col  = _find_col(df_moras, ["saldo", "deuda", "monto", "valor"])

    # ── Filtros ──────────────────────────────────────────────────────
    with st.expander("🔍 Filtros"):
        f_c1, f_c2, f_c3, f_c4 = st.columns(4)

        # Campaña
        camp_options = []
        if df_moras is not None and mora_camp_col:
            raw_camps = sorted(df_moras[mora_camp_col].dropna().astype(str).unique())
            camp_options = [_fmt_camp(c) for c in raw_camps]
        with f_c1:
            sel_campañas = st.multiselect("Campaña", camp_options, key="int_fil_camp")

        # Temporalidad
        with f_c2:
            sel_temporal = st.multiselect(
                "Temporalidad de mora",
                ["Mora 1", "Mora 2", "Mora 3"],
                key="int_fil_temp"
            )

        # Fechas
        fecha_min = pd.Timestamp("2020-01-01").date()
        fecha_max = pd.Timestamp.today().date()
        if df_tel is not None and tel_cols.get("fecha"):
            try:
                _dates = pd.to_datetime(df_tel[tel_cols["fecha"]], errors="coerce").dropna()
                if not _dates.empty:
                    fecha_min = _dates.min().date()
                    fecha_max = _dates.max().date()
            except Exception:
                pass
        with f_c3:
            sel_fecha_desde = st.date_input("Fecha desde", value=fecha_min, key="int_fil_desde")
        with f_c4:
            sel_fecha_hasta = st.date_input("Fecha hasta", value=fecha_max, key="int_fil_hasta")

        # Gestor
        gestor_options = []
        if df_campo is not None and campo_cols.get("gestor"):
            gestor_options = sorted(df_campo[campo_cols["gestor"]].dropna().astype(str).unique())
        sel_gestores = st.multiselect("Gestor", gestor_options, key="int_fil_gestor")

    # ── Aplicar filtros a df_moras ────────────────────────────────────
    df_moras_fil = None
    if df_moras is not None:
        df_moras_fil = df_moras.copy()
        if mora_nodama_col:
            df_moras_fil[mora_nodama_col] = df_moras_fil[mora_nodama_col].astype(str).str.strip()
        if mora_camp_col and sel_campañas:
            raw_sel = {c for c in df_moras_fil[mora_camp_col].astype(str).unique()
                       if _fmt_camp(c) in sel_campañas}
            df_moras_fil = df_moras_fil[df_moras_fil[mora_camp_col].astype(str).isin(raw_sel)]
        if mora_temp_col and sel_temporal:
            _mora_map = {"mora 1": "Mora 1", "mora 2": "Mora 2", "mora 3": "Mora 3",
                         "1": "Mora 1", "2": "Mora 2", "3": "Mora 3"}
            df_moras_fil["_mora_norm"] = (
                df_moras_fil[mora_temp_col].astype(str).str.strip().str.lower()
                .map(_mora_map).fillna(df_moras_fil[mora_temp_col].astype(str).str.strip())
            )
            df_moras_fil = df_moras_fil[df_moras_fil["_mora_norm"].isin(sel_temporal)]

    # Aplicar filtros a df_tel
    df_tel_fil = None
    if df_tel is not None:
        df_tel_fil = df_tel.copy()
        if tel_cols.get("nodama"):
            df_tel_fil[tel_cols["nodama"]] = df_tel_fil[tel_cols["nodama"]].astype(str).str.strip()
        if tel_cols.get("fecha"):
            try:
                df_tel_fil["_fecha_dt"] = pd.to_datetime(df_tel_fil[tel_cols["fecha"]], errors="coerce")
                df_tel_fil = df_tel_fil[
                    (df_tel_fil["_fecha_dt"].dt.date >= sel_fecha_desde) &
                    (df_tel_fil["_fecha_dt"].dt.date <= sel_fecha_hasta)
                ]
            except Exception:
                pass

    # Aplicar filtros a df_campo
    df_campo_fil = None
    if df_campo is not None:
        df_campo_fil = df_campo.copy()
        if campo_cols.get("nodama"):
            df_campo_fil[campo_cols["nodama"]] = df_campo_fil[campo_cols["nodama"]].astype(str).str.strip()
        if campo_cols.get("fecha"):
            try:
                df_campo_fil["_fecha_dt"] = pd.to_datetime(df_campo_fil[campo_cols["fecha"]], errors="coerce")
                df_campo_fil = df_campo_fil[
                    (df_campo_fil["_fecha_dt"].dt.date >= sel_fecha_desde) &
                    (df_campo_fil["_fecha_dt"].dt.date <= sel_fecha_hasta)
                ]
            except Exception:
                pass
        if campo_cols.get("gestor") and sel_gestores:
            df_campo_fil = df_campo_fil[df_campo_fil[campo_cols["gestor"]].astype(str).isin(sel_gestores)]

    df_cobranza = st.session_state.get("df_cobranza")

    # ── Sub-tabs ──────────────────────────────────────────────────────
    int0, int1, int2, int3, int4 = st.tabs([
        "📋 Cobertura",
        "✅ Efectividad",
        "📈 Evolución de Mora",
        "🔍 Por Temporalidad",
        "📊 Indicadores",
    ])

    # ═══════════════════════════════════════════
    #  int0 — COBERTURA
    # ═══════════════════════════════════════════
    with int0:
        if df_moras_fil is None:
            st.warning("Carga el archivo de Moras (sección Arabela) para ver la cobertura.")
        elif df_tel_fil is None and df_campo_fil is None:
            st.warning("Carga al menos uno de los archivos de gestión (Telefónica o Campo) para ver la cobertura.")
        else:
            st.markdown(
                "<div class='kpi-banner' style='margin-bottom:1rem'>"
                "<h1 style='font-size:1.1rem'>📋 Cobertura de Gestión</h1>"
                "<p>Comparativo entre damas asignadas y damas contactadas</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            # Conjuntos compuestos NoDama|Campaña
            def _cov_keys(df, nd_col, cp_col):
                if df is None or not nd_col or nd_col not in df.columns:
                    return set()
                _nd = df[nd_col].fillna("").astype(str).str.strip()
                if cp_col and cp_col in df.columns:
                    _cp = df[cp_col].fillna("").astype(str).str.strip()
                    return set((_nd + "|" + _cp).tolist())
                return set((_nd + "|*").tolist())

            base_keys   = _cov_keys(df_moras_fil,  mora_nodama_col,       mora_camp_col)
            tel_keys    = _cov_keys(df_tel_fil,     tel_cols.get("nodama"), tel_cols.get("camp"))
            campo_keys  = _cov_keys(df_campo_fil,   campo_cols.get("nodama"), campo_cols.get("camp"))

            tel_base    = tel_keys & base_keys
            campo_base  = campo_keys & base_keys
            solo_tel    = tel_base - campo_keys
            solo_campo  = campo_base - tel_keys
            mixta       = tel_keys & campo_keys & base_keys
            sin_gestion = base_keys - tel_keys - campo_keys
            con_gestion = base_keys - sin_gestion

            total_base = len(base_keys) or 1

            def _pct(n):
                return n / total_base * 100

            # KPI cards
            kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
            with kpi_c1:
                n = len(solo_tel | mixta)
                st.metric("📞 Gestión Telefónica", f"{n:,}", delta=f"{_pct(n):.1f}% de base")
            with kpi_c2:
                n = len(solo_campo | mixta)
                st.metric("🚗 Gestión Campo", f"{n:,}", delta=f"{_pct(n):.1f}% de base")
            with kpi_c3:
                n = len(mixta)
                st.metric("🔀 Gestión Mixta", f"{n:,}", delta=f"{_pct(n):.1f}% de base")
            with kpi_c4:
                n = len(sin_gestion)
                st.metric("⚠️ Sin Gestión", f"{n:,}", delta=f"{_pct(n):.1f}% de base", delta_color="inverse")

            st.markdown("<br>", unsafe_allow_html=True)

            chart_col, table_col = st.columns([1, 1])

            with chart_col:
                # Donut chart
                donut_labels = ["Solo Tel.", "Solo Campo", "Mixta", "Sin gestión"]
                donut_values = [len(solo_tel), len(solo_campo), len(mixta), len(sin_gestion)]
                donut_colors = [COLORS["accent"], COLORS["success"], COLORS["purple"], COLORS["muted"]]

                fig_donut = go.Figure(go.Pie(
                    labels=donut_labels,
                    values=donut_values,
                    hole=0.55,
                    marker_colors=donut_colors,
                    textinfo="percent+label",
                    hovertemplate="%{label}<br>%{value:,} damas<br>%{percent}<extra></extra>",
                ))
                fig_donut.update_layout(
                    **{**PLOTLY_LAYOUT, "title": "Distribución de cobertura",
                       "height": 360, "showlegend": False,
                       "annotations": [dict(
                           text=f"<b>{len(con_gestion):,}</b><br>gestionadas",
                           x=0.5, y=0.5, showarrow=False, font_size=14, align="center"
                       )]}
                )
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(fig_donut, use_container_width=True,
                                config={"displayModeBar": False}, key="int_donut_cob")
                st.markdown("</div>", unsafe_allow_html=True)

            with table_col:
                # Tabla resumen
                resumen_data = {
                    "Segmento": ["Base asignada", "Con gestión", "Solo telefónica", "Solo campo", "Mixta", "Sin gestión"],
                    "Damas": [len(base_keys), len(con_gestion), len(solo_tel), len(solo_campo), len(mixta), len(sin_gestion)],
                    "% Base": [100.0, _pct(len(con_gestion)), _pct(len(solo_tel)),
                               _pct(len(solo_campo)), _pct(len(mixta)), _pct(len(sin_gestion))],
                }
                df_resumen = pd.DataFrame(resumen_data)
                df_resumen["% Base"] = df_resumen["% Base"].map(lambda x: f"{x:.1f}%")
                st.markdown("**Resumen de cobertura**")
                st.dataframe(df_resumen, use_container_width=True, hide_index=True)

            # Gráfico por gestor (si hay campo)
            if df_campo_fil is not None and campo_cols.get("gestor") and campo_cols.get("nodama"):
                st.markdown("---")
                st.markdown("**Top 10 gestores por cuentas visitadas**")
                gestor_counts = (
                    df_campo_fil.dropna(subset=[campo_cols["gestor"]])
                    .groupby(campo_cols["gestor"])[campo_cols["nodama"]]
                    .nunique()
                    .sort_values(ascending=True)
                    .tail(10)
                )
                if not gestor_counts.empty:
                    fig_gestor = go.Figure(go.Bar(
                        y=gestor_counts.index.tolist(),
                        x=gestor_counts.values.tolist(),
                        orientation="h",
                        marker_color=COLORS["accent"],
                        text=gestor_counts.values.tolist(),
                        textposition="outside",
                        hovertemplate="%{y}<br>%{x:,} cuentas<extra></extra>",
                    ))
                    fig_gestor.update_layout(
                        **{**PLOTLY_LAYOUT, "title": "Cuentas visitadas por gestor (top 10)",
                           "height": 360, "xaxis_title": "Cuentas únicas",
                           "yaxis": dict(**_AXIS_DEFAULTS, automargin=True),
                           "xaxis": _AXIS_DEFAULTS}
                    )
                    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                    st.plotly_chart(fig_gestor, use_container_width=True,
                                    config={"displayModeBar": False}, key="int_bar_gestor")
                    st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  int1 — EFECTIVIDAD
    # ═══════════════════════════════════════════
    with int1:
        if df_tel_fil is None:
            st.warning("Carga el archivo de Gestión Telefónica para ver la efectividad.")
        else:
            st.markdown(
                "<div class='kpi-banner' style='margin-bottom:1rem'>"
                "<h1 style='font-size:1.1rem'>✅ Efectividad de Gestión Telefónica</h1>"
                "<p>Contacto efectivo y promesas de pago</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            nodama_t  = tel_cols.get("nodama")
            camp_t    = tel_cols.get("camp")
            fecha_t   = tel_cols.get("fecha")
            tipif_t   = tel_cols.get("tipif")
            promesa_t = tel_cols.get("promesa")

            if not nodama_t or not tipif_t:
                st.warning("No se detectaron las columnas necesarias (NoDama, Tipificación). Ajusta las columnas arriba.")
            else:
                df_t = df_tel_fil.copy()
                df_t[nodama_t] = df_t[nodama_t].astype(str).str.strip()
                if camp_t and camp_t in df_t.columns:
                    df_t[camp_t] = df_t[camp_t].astype(str).str.strip()
                df_t["_tipif_num"] = pd.to_numeric(df_t[tipif_t], errors="coerce")
                df_t["_es_efectivo"] = df_t["_tipif_num"].isin(CONTACTO_EFECTIVO)

                # Agrupar por NoDama+Campaña
                grp_cols = [nodama_t] + ([camp_t] if camp_t and camp_t in df_t.columns else [])
                por_nodama = df_t.groupby(grp_cols).agg(
                    _tiene_efectivo=("_es_efectivo", "any"),
                ).reset_index()

                if promesa_t and promesa_t in df_t.columns:
                    try:
                        _prom_s = (
                            df_t[promesa_t].fillna("").astype(str).str.strip().str.lower()
                            .replace({"nan": "", "none": "", "no": "", "n/a": ""})
                        )
                        df_t["_tiene_promesa_row"] = _prom_s != ""
                        prom_group = df_t.groupby(grp_cols)["_tiene_promesa_row"].any().reset_index()
                        prom_group.columns = grp_cols + ["_tiene_promesa"]
                        por_nodama = por_nodama.merge(prom_group, on=grp_cols, how="left")
                        por_nodama["_tiene_promesa"] = por_nodama["_tiene_promesa"].fillna(False)
                    except Exception:
                        por_nodama["_tiene_promesa"] = False
                else:
                    por_nodama["_tiene_promesa"] = False

                total_nod       = len(por_nodama)
                efectivo_n      = int(por_nodama["_tiene_efectivo"].sum())
                sin_contacto_n  = total_nod - efectivo_n
                promesa_n       = int(por_nodama["_tiene_promesa"].sum())

                pct_ef  = efectivo_n / total_nod * 100 if total_nod else 0
                pct_pr  = promesa_n  / total_nod * 100 if total_nod else 0
                pct_sin = sin_contacto_n / total_nod * 100 if total_nod else 0

                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.metric("📋 Total gestionadas", f"{total_nod:,}")
                with k2:
                    st.metric("✅ Contacto efectivo", f"{efectivo_n:,}", delta=f"{pct_ef:.1f}%")
                with k3:
                    st.metric("💬 Con promesa de pago", f"{promesa_n:,}", delta=f"{pct_pr:.1f}%")
                with k4:
                    st.metric("❌ Sin contacto", f"{sin_contacto_n:,}", delta=f"{pct_sin:.1f}%", delta_color="inverse")

                st.markdown("<br>", unsafe_allow_html=True)

                # Barras: top 10 tipificaciones
                tipif_counts = (
                    df_t["_tipif_num"].dropna()
                    .astype(int)
                    .value_counts()
                    .head(10)
                    .reset_index()
                )
                tipif_counts.columns = ["codigo", "conteo"]
                tipif_counts["etiqueta"] = tipif_counts["codigo"].map(
                    lambda x: TIPIF_CATALOG.get(x, str(x))
                )
                tipif_counts["es_efectivo"] = tipif_counts["codigo"].isin(CONTACTO_EFECTIVO)
                tipif_counts["color"] = tipif_counts["es_efectivo"].map(
                    {True: COLORS["success"], False: COLORS["danger"]}
                )
                tipif_counts = tipif_counts.sort_values("conteo", ascending=True)

                bar_c1, bar_c2 = st.columns([3, 2])
                with bar_c1:
                    fig_tipif = go.Figure(go.Bar(
                        y=tipif_counts["etiqueta"],
                        x=tipif_counts["conteo"],
                        orientation="h",
                        marker_color=tipif_counts["color"].tolist(),
                        text=tipif_counts["conteo"],
                        textposition="outside",
                        hovertemplate="%{y}<br>%{x:,} gestiones<extra></extra>",
                    ))
                    fig_tipif.update_layout(
                        **{**PLOTLY_LAYOUT, "title": "Top 10 tipificaciones",
                           "height": 380,
                           "yaxis": dict(**_AXIS_DEFAULTS, automargin=True),
                           "xaxis": _AXIS_DEFAULTS}
                    )
                    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                    st.plotly_chart(fig_tipif, use_container_width=True,
                                    config={"displayModeBar": False}, key="int_bar_tipif")
                    st.markdown("</div>", unsafe_allow_html=True)

                with bar_c2:
                    # Donut efectividad
                    fig_ef = go.Figure(go.Pie(
                        labels=["Contacto efectivo", "Sin contacto"],
                        values=[efectivo_n, sin_contacto_n],
                        hole=0.55,
                        marker_colors=[COLORS["success"], COLORS["danger"]],
                        textinfo="percent+label",
                        hovertemplate="%{label}<br>%{value:,}<br>%{percent}<extra></extra>",
                    ))
                    fig_ef.update_layout(
                        **{**PLOTLY_LAYOUT, "title": "Contacto efectivo vs sin contacto",
                           "height": 380, "showlegend": False,
                           "annotations": [dict(
                               text=f"<b>{pct_ef:.0f}%</b><br>efectivo",
                               x=0.5, y=0.5, showarrow=False, font_size=13, align="center"
                           )]}
                    )
                    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                    st.plotly_chart(fig_ef, use_container_width=True,
                                    config={"displayModeBar": False}, key="int_donut_ef")
                    st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  int2 — EVOLUCIÓN DE MORA
    # ═══════════════════════════════════════════
    with int2:
        if df_moras is None:
            st.warning("Carga el archivo de Moras (sección Arabela) para ver la evolución.")
        elif mora_nodama_col is None or mora_camp_col is None:
            st.warning("No se detectaron las columnas NoDama y Campaña en el archivo de Moras.")
        else:
            st.markdown(
                "<div class='kpi-banner' style='margin-bottom:1rem'>"
                "<h1 style='font-size:1.1rem'>📈 Evolución de Mora</h1>"
                "<p>Distribución y transiciones de mora por campaña</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            _mora_map_ev = {
                "mora 1": "Mora 1", "mora 2": "Mora 2", "mora 3": "Mora 3",
                "1": "Mora 1", "2": "Mora 2", "3": "Mora 3",
                "inactiva": "Inactiva",
            }
            MORA_COLORS_INT = {
                "Inactiva": "#94A3B8",
                "Mora 1":   COLORS["warning"],
                "Mora 2":   COLORS["orange"],
                "Mora 3":   COLORS["danger"],
            }
            df_ev = df_moras.copy()
            df_ev[mora_nodama_col] = df_ev[mora_nodama_col].astype(str).str.strip()
            df_ev[mora_camp_col]   = df_ev[mora_camp_col].astype(str).str.strip()
            df_ev["_camp_fmt"] = df_ev[mora_camp_col].apply(_fmt_camp)

            if mora_temp_col:
                df_ev["_mora_norm"] = (
                    df_ev[mora_temp_col].astype(str).str.strip().str.lower()
                    .map(_mora_map_ev)
                    .fillna("Mora 1")
                )
            else:
                df_ev["_mora_norm"] = "Mora 1"

            camps_ev = sorted(df_ev["_camp_fmt"].unique(), key=_camp_sort_key)

            # Línea: conteo por mora y campaña
            line_data = []
            for mora in ["Mora 1", "Mora 2", "Mora 3"]:
                for camp in camps_ev:
                    cnt = ((df_ev["_mora_norm"] == mora) & (df_ev["_camp_fmt"] == camp)).sum()
                    line_data.append({"Mora": mora, "Campaña": camp, "Cuentas": int(cnt)})
            df_line = pd.DataFrame(line_data)

            fig_line = go.Figure()
            for mora in ["Mora 1", "Mora 2", "Mora 3"]:
                sub = df_line[df_line["Mora"] == mora]
                fig_line.add_trace(go.Scatter(
                    x=sub["Campaña"], y=sub["Cuentas"],
                    mode="lines+markers",
                    name=mora,
                    line=dict(color=MORA_COLORS_INT[mora], width=2),
                    marker=dict(size=7),
                    hovertemplate=f"{mora}<br>Campaña: %{{x}}<br>Cuentas: %{{y:,}}<extra></extra>",
                ))
            fig_line.update_layout(
                **{**PLOTLY_LAYOUT, "title": "Cuentas por nivel de mora y campaña",
                   "height": 360, "xaxis_title": "Campaña", "yaxis_title": "Cuentas",
                   "xaxis": _AXIS_DEFAULTS, "yaxis": _AXIS_DEFAULTS, "legend_title": "Nivel"}
            )
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(fig_line, use_container_width=True,
                            config={"displayModeBar": False}, key="int_line_mora")
            st.markdown("</div>", unsafe_allow_html=True)

            # Matriz de transición (entre campañas consecutivas)
            if len(camps_ev) >= 2:
                st.markdown("**Matriz de transición entre campañas consecutivas**")
                # Para la última par de campañas
                camp_A = camps_ev[-2]
                camp_B = camps_ev[-1]

                damas_A = df_ev[df_ev["_camp_fmt"] == camp_A][[mora_nodama_col, "_mora_norm"]].copy()
                damas_A.columns = [mora_nodama_col, "mora_origen"]
                damas_B = df_ev[df_ev["_camp_fmt"] == camp_B][[mora_nodama_col, "_mora_norm"]].copy()
                damas_B.columns = [mora_nodama_col, "mora_destino"]

                trans = damas_A.merge(damas_B, on=mora_nodama_col, how="left")
                trans["mora_destino"] = trans["mora_destino"].fillna("Salió de cartera")

                matrix = trans.groupby(["mora_origen", "mora_destino"]).size().unstack(fill_value=0)
                all_destinos = ["Mora 1", "Mora 2", "Mora 3", "Inactiva", "Salió de cartera"]
                for d in all_destinos:
                    if d not in matrix.columns:
                        matrix[d] = 0
                matrix = matrix[[d for d in all_destinos if d in matrix.columns]]

                # Heatmap
                matrix_pct = matrix.div(matrix.sum(axis=1), axis=0) * 100
                fig_hm = go.Figure(go.Heatmap(
                    z=matrix_pct.values,
                    x=matrix_pct.columns.tolist(),
                    y=matrix_pct.index.tolist(),
                    colorscale="Blues",
                    text=[[f"{v:.1f}%" for v in row] for row in matrix_pct.values],
                    texttemplate="%{text}",
                    hovertemplate="De: %{y}<br>A: %{x}<br>%{z:.1f}%<extra></extra>",
                    colorbar=dict(title="% transición"),
                ))
                fig_hm.update_layout(
                    **{**PLOTLY_LAYOUT, "title": f"Transición de mora: {camp_A} → {camp_B}",
                       "height": 340, "xaxis_title": "Mora destino", "yaxis_title": "Mora origen"}
                )
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(fig_hm, use_container_width=True,
                                config={"displayModeBar": False}, key="int_heatmap_trans")
                st.markdown("</div>", unsafe_allow_html=True)

                # KPIs transición
                t_total = len(trans)
                t_mismo = int((trans["mora_origen"] == trans["mora_destino"]).sum()) if t_total else 0
                t_avanza = int(trans[
                    trans.apply(lambda r: (
                        r["mora_origen"] == "Mora 1" and r["mora_destino"] == "Mora 2"
                    ) or (
                        r["mora_origen"] == "Mora 2" and r["mora_destino"] == "Mora 3"
                    ), axis=1)
                ].shape[0])
                t_sale = int((trans["mora_destino"] == "Salió de cartera").sum())
                t_rec  = int((trans["mora_destino"] == "Inactiva").sum())

                tc1, tc2, tc3, tc4 = st.columns(4)
                with tc1:
                    st.metric("↔ Permanecen en mora", f"{t_mismo:,}",
                              delta=f"{t_mismo/t_total*100:.1f}%" if t_total else "—")
                with tc2:
                    st.metric("⬆ Avanzan a mora superior", f"{t_avanza:,}",
                              delta=f"{t_avanza/t_total*100:.1f}%" if t_total else "—",
                              delta_color="inverse")
                with tc3:
                    st.metric("✅ Se recuperaron", f"{t_rec:,}",
                              delta=f"{t_rec/t_total*100:.1f}%" if t_total else "—")
                with tc4:
                    st.metric("🚪 Salieron de cartera", f"{t_sale:,}",
                              delta=f"{t_sale/t_total*100:.1f}%" if t_total else "—")

    # ═══════════════════════════════════════════
    #  int3 — POR TEMPORALIDAD
    # ═══════════════════════════════════════════
    with int3:
        if df_moras is None:
            st.warning("Carga el archivo de Moras (sección Arabela) para ver el análisis por temporalidad.")
        else:
            st.markdown(
                "<div class='kpi-banner' style='margin-bottom:1rem'>"
                "<h1 style='font-size:1.1rem'>🔍 Análisis por Temporalidad de Mora</h1>"
                "<p>Cobertura y efectividad desglosada por nivel de mora</p>"
                "</div>",
                unsafe_allow_html=True,
            )

            _mora_map_t3 = {
                "mora 1": "Mora 1", "mora 2": "Mora 2", "mora 3": "Mora 3",
                "1": "Mora 1", "2": "Mora 2", "3": "Mora 3",
            }
            MORA_COLORS_T3 = {
                "Mora 1": COLORS["warning"],
                "Mora 2": COLORS["orange"],
                "Mora 3": COLORS["danger"],
            }

            df_t3_moras = (df_moras_fil if df_moras_fil is not None else df_moras).copy()
            if mora_nodama_col:
                df_t3_moras[mora_nodama_col] = df_t3_moras[mora_nodama_col].astype(str).str.strip()
            if mora_temp_col:
                df_t3_moras["_mora_norm"] = (
                    df_t3_moras[mora_temp_col].astype(str).str.strip().str.lower()
                    .map(_mora_map_t3).fillna("Mora 1")
                )
            else:
                df_t3_moras["_mora_norm"] = "Mora 1"

            has_tel   = df_tel_fil is not None and tel_cols.get("nodama") and tel_cols.get("tipif")
            has_campo = df_campo_fil is not None and campo_cols.get("nodama")

            # Prepara conjuntos de NoDamas gestionadas y efectivas por mora
            rows_summary = []
            for mora in ["Mora 1", "Mora 2", "Mora 3"]:
                df_mora = df_t3_moras[df_t3_moras["_mora_norm"] == mora]
                asignadas_set = set(df_mora[mora_nodama_col].dropna().astype(str)) if mora_nodama_col else set()
                n_asignadas = len(asignadas_set)

                tel_mora_set    = set()
                campo_mora_set  = set()
                ef_mora_set     = set()
                promesa_mora_set = set()

                if has_tel:
                    df_tel_m = df_tel_fil[
                        df_tel_fil[tel_cols["nodama"]].isin(asignadas_set)
                    ].copy()
                    tel_mora_set = set(df_tel_m[tel_cols["nodama"]].astype(str))
                    df_tel_m["_tipif_num"] = pd.to_numeric(df_tel_m[tel_cols["tipif"]], errors="coerce")
                    df_tel_m["_es_ef"] = df_tel_m["_tipif_num"].isin(CONTACTO_EFECTIVO)
                    ef_mora_set = set(
                        df_tel_m[df_tel_m["_es_ef"]][tel_cols["nodama"]].astype(str)
                    )
                    if tel_cols.get("promesa"):
                        _pr = df_tel_m[tel_cols["promesa"]].dropna().astype(str).str.strip().str.lower()
                        _pr_mask = ~_pr.isin(["", "nan", "none", "no", "n/a"])
                        promesa_mora_set = set(
                            df_tel_m[_pr_mask.values][tel_cols["nodama"]].astype(str)
                        )

                if has_campo:
                    df_campo_m = df_campo_fil[
                        df_campo_fil[campo_cols["nodama"]].isin(asignadas_set)
                    ]
                    campo_mora_set = set(df_campo_m[campo_cols["nodama"]].astype(str))

                gestionadas_set = tel_mora_set | campo_mora_set
                n_gest = len(gestionadas_set)
                n_ef   = len(ef_mora_set)
                n_pr   = len(promesa_mora_set)

                pct_gest = n_gest / n_asignadas * 100 if n_asignadas else 0
                pct_ef   = n_ef   / n_gest * 100      if n_gest else 0
                pct_pr   = n_pr   / n_gest * 100      if n_gest else 0

                rows_summary.append({
                    "mora": mora,
                    "asignadas": n_asignadas,
                    "gestionadas": n_gest,
                    "efectivo": n_ef,
                    "promesa": n_pr,
                    "pct_gest": pct_gest,
                    "pct_ef": pct_ef,
                    "pct_pr": pct_pr,
                    "color": MORA_COLORS_T3[mora],
                })

            # Render por mora
            for row in rows_summary:
                mora     = row["mora"]
                color    = row["color"]
                st.markdown(
                    f"<div style='background:{color}33;border-left:5px solid {color};"
                    f"border-radius:8px;padding:0.6rem 1rem;margin:0.8rem 0 0.4rem'>"
                    f"<span style='font-weight:700;color:{COLORS['primary']};font-size:1rem'>{mora}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                with mc1:
                    st.metric("📋 Asignadas", f"{row['asignadas']:,}")
                with mc2:
                    st.metric("📲 Gestionadas", f"{row['gestionadas']:,}",
                              delta=f"{row['pct_gest']:.1f}% de asignadas")
                with mc3:
                    st.metric("✅ Contacto efectivo", f"{row['efectivo']:,}",
                              delta=f"{row['pct_ef']:.1f}% de gestionadas")
                with mc4:
                    st.metric("💬 Con promesa", f"{row['promesa']:,}",
                              delta=f"{row['pct_pr']:.1f}% de gestionadas")
                with mc5:
                    pct_sin = 100 - row["pct_gest"]
                    st.metric("⚠️ Sin gestión", f"{row['asignadas'] - row['gestionadas']:,}",
                              delta=f"{pct_sin:.1f}%", delta_color="inverse")

            # Stacked bar chart
            st.markdown("<br>", unsafe_allow_html=True)
            if rows_summary:
                moras_labels = [r["mora"] for r in rows_summary]
                bar_colors = [COLORS["muted"], COLORS["accent"], COLORS["success"], COLORS["warning"]]

                fig_stacked = go.Figure()
                fig_stacked.add_trace(go.Bar(
                    name="Asignadas (sin gestión)",
                    x=moras_labels,
                    y=[r["asignadas"] - r["gestionadas"] for r in rows_summary],
                    marker_color=COLORS["muted"],
                    hovertemplate="%{x}<br>Sin gestión: %{y:,}<extra></extra>",
                ))
                fig_stacked.add_trace(go.Bar(
                    name="Gestionadas",
                    x=moras_labels,
                    y=[r["gestionadas"] - r["efectivo"] for r in rows_summary],
                    marker_color=COLORS["accent"],
                    hovertemplate="%{x}<br>Gestionadas (sin efectivo): %{y:,}<extra></extra>",
                ))
                fig_stacked.add_trace(go.Bar(
                    name="Contacto efectivo",
                    x=moras_labels,
                    y=[r["efectivo"] for r in rows_summary],
                    marker_color=COLORS["success"],
                    hovertemplate="%{x}<br>Contacto efectivo: %{y:,}<extra></extra>",
                ))
                fig_stacked.update_layout(
                    **{**PLOTLY_LAYOUT,
                       "barmode": "stack",
                       "title": "Asignadas vs Gestionadas vs Contacto efectivo por temporalidad",
                       "height": 380,
                       "xaxis": _AXIS_DEFAULTS,
                       "yaxis": dict(**_AXIS_DEFAULTS, title="Cuentas"),
                       "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)}
                )
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(fig_stacked, use_container_width=True,
                                config={"displayModeBar": False}, key="int_stacked_temp")
                st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  int4 — INDICADORES DE COBRANZA
    # ═══════════════════════════════════════════
    with int4:
        if df_cobranza is None:
            st.info("📂 Carga la **Base de Cobranza** en el panel de archivos de arriba para ver los indicadores.")
        else:
            # ── Detección de columnas ────────────────────────────────────
            _cob = df_cobranza.copy()
            _cc = {
                "camp":     _find_col(_cob, ["campaña", "campana", "camp", "periodo", "anio", "año"]),
                "division": _find_col(_cob, ["division", "división", "div"]),
                "ruta":     _find_col(_cob, ["ruta", "route"]),
                "zona":     _find_col(_cob, ["zona", "zone", "area", "área"]),
                "nodama":   _find_col(_cob, ["nodama", "no dama", "numdama", "dama", "número de dama"]),
                "segmento": _find_col(_cob, ["segmento", "mora", "temporalidad", "nivel", "estatus mora"]),
                "saldo_asig": _find_col(_cob, ["saldo asignado", "saldo_asignado", "asignado", "saldo"]),
                "pago":     _find_col(_cob, ["pago aplicado", "pago_aplicado", "pagado", "pago", "recuperado", "cobrado"]),
                "visita":   _find_col(_cob, ["visita realizada", "visita_realizada", "visita", "visitado", "visit"]),
                "res_visita": _find_col(_cob, ["resultado visita", "resultado_visita", "resultado", "estatus visita"]),
                "dictam":   _find_col(_cob, ["dictaminacion", "dictaminación", "dictamen", "dictam"]),
                "estatus":  _find_col(_cob, ["estatus cuenta", "estatus_cuenta", "estatus", "status", "estado"]),
            }

            with st.expander("⚙️ Ajustar columnas — Base de Cobranza"):
                _all_cob = list(_cob.columns)
                _opt_none = ["(ninguna)"] + _all_cob
                _ic1, _ic2, _ic3, _ic4 = st.columns(4)
                with _ic1:
                    _cc["camp"]      = st.selectbox("Campaña",          _all_cob, index=_all_cob.index(_cc["camp"])      if _cc["camp"]      in _all_cob else 0, key="cob_camp")
                    _cc["division"]  = st.selectbox("División",          _all_cob, index=_all_cob.index(_cc["division"])  if _cc["division"]  in _all_cob else 0, key="cob_div")
                    _cc["ruta"]      = st.selectbox("Ruta",              _all_cob, index=_all_cob.index(_cc["ruta"])      if _cc["ruta"]      in _all_cob else 0, key="cob_ruta")
                with _ic2:
                    _cc["zona"]      = st.selectbox("Zona",              _all_cob, index=_all_cob.index(_cc["zona"])      if _cc["zona"]      in _all_cob else 0, key="cob_zona")
                    _cc["nodama"]    = st.selectbox("Número de Dama",    _all_cob, index=_all_cob.index(_cc["nodama"])    if _cc["nodama"]    in _all_cob else 0, key="cob_nodama")
                    _cc["segmento"]  = st.selectbox("Segmento Mora",     _all_cob, index=_all_cob.index(_cc["segmento"])  if _cc["segmento"]  in _all_cob else 0, key="cob_seg")
                with _ic3:
                    _cc["saldo_asig"] = st.selectbox("Saldo Asignado",   _all_cob, index=_all_cob.index(_cc["saldo_asig"]) if _cc["saldo_asig"] in _all_cob else 0, key="cob_saldo")
                    _cc["pago"]      = st.selectbox("Pago Aplicado",     _all_cob, index=_all_cob.index(_cc["pago"])      if _cc["pago"]      in _all_cob else 0, key="cob_pago")
                    _cc["visita"]    = st.selectbox("Visita Realizada",  _all_cob, index=_all_cob.index(_cc["visita"])    if _cc["visita"]    in _all_cob else 0, key="cob_visita")
                with _ic4:
                    _cc["res_visita"] = st.selectbox("Resultado Visita", _all_cob, index=_all_cob.index(_cc["res_visita"]) if _cc["res_visita"] in _all_cob else 0, key="cob_resvis")
                    _cc["dictam"]    = st.selectbox("Dictaminación",     _all_cob, index=_all_cob.index(_cc["dictam"])    if _cc["dictam"]    in _all_cob else 0, key="cob_dictam")
                    _cc["estatus"]   = st.selectbox("Estatus Cuenta",    _all_cob, index=_all_cob.index(_cc["estatus"])   if _cc["estatus"]   in _all_cob else 0, key="cob_estatus")

            # ── Normalizar numéricos ─────────────────────────────────────
            for _num_col in ["saldo_asig", "pago"]:
                _col = _cc[_num_col]
                if _col and _col in _cob.columns:
                    _cob[_col] = pd.to_numeric(_cob[_col], errors="coerce").fillna(0)

            # ── Helper ──────────────────────────────────────────────────
            def _safe(col):
                return _cc.get(col) and _cc[col] in _cob.columns

            def _grp_recovery(group_col):
                if not _safe(group_col) or not _safe("saldo_asig"):
                    return pd.DataFrame()
                g = _cob.groupby(_cob[_cc[group_col]].astype(str)).agg(
                    Asignado=(_cc["saldo_asig"], "sum"),
                    **( {"Pagado": (_cc["pago"], "sum")} if _safe("pago") else {} ),
                    Cuentas=(_cc["saldo_asig"], "count"),
                ).reset_index()
                g.columns.values[0] = group_col
                if "Pagado" in g.columns:
                    g["% Rec"] = (g["Pagado"] / g["Asignado"].replace(0, 1) * 100).round(1)
                return g

            saldo_tot  = _cob[_cc["saldo_asig"]].sum() if _safe("saldo_asig") else 0
            pago_tot   = _cob[_cc["pago"]].sum()       if _safe("pago")       else 0
            pct_rec    = pago_tot / saldo_tot * 100     if saldo_tot else 0
            n_cuentas  = len(_cob)

            def _pct_bool_col(col_key, true_vals=None):
                if not _safe(col_key):
                    return None, 0
                _s = _cob[_cc[col_key]].astype(str).str.strip().str.lower()
                if true_vals:
                    mask = _s.isin({v.lower() for v in true_vals})
                else:
                    mask = _s.notna() & (_s != "") & (_s != "nan") & (_s != "no") & (_s != "0")
                return int(mask.sum()), mask.sum() / len(_s) * 100 if len(_s) else 0

            n_visitas, pct_visita     = _pct_bool_col("visita", ["sí", "si", "yes", "1", "true", "realizada", "efectuada"])
            n_contacto, pct_contacto  = _pct_bool_col("res_visita", ["contacto", "localizada", "efectivo", "cobro"])
            n_promesa, pct_promesa    = _pct_bool_col("estatus", ["promesa de pago", "promesa", "ppp", "compromiso"])

            # ── Sub-tabs indicadores ─────────────────────────────────────
            cob0, cob1, cob2, cob3, cob4 = st.tabs([
                "📋 Ejecutivo", "📊 Por Segmento", "🗺️ Geográfico", "🚗 Gestión", "⚠️ Alertas"
            ])

            # ── cob0: EJECUTIVO ──────────────────────────────────────────
            with cob0:
                st.markdown(
                    "<div class='kpi-banner' style='margin-bottom:1rem'>"
                    "<h1 style='font-size:1.1rem'>📋 Indicadores Ejecutivos de Recuperación</h1>"
                    "<p>Resumen gerencial de desempeño de cobranza</p></div>",
                    unsafe_allow_html=True,
                )
                r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                with r1c1:
                    st.metric("📂 Cuentas Asignadas", f"{n_cuentas:,}")
                with r1c2:
                    st.metric("💰 Saldo Asignado", fmt_currency(saldo_tot))
                with r1c3:
                    st.metric("✅ Saldo Recuperado", fmt_currency(pago_tot),
                              delta=f"{pct_rec:.1f}% recuperación")
                with r1c4:
                    st.metric("📈 % Recuperación", f"{pct_rec:.1f}%")

                st.markdown("<br>", unsafe_allow_html=True)
                r2c1, r2c2, r2c3 = st.columns(3)
                with r2c1:
                    st.metric("🚗 Visitas Realizadas",
                              f"{n_visitas:,}" if n_visitas is not None else "N/D",
                              delta=f"{pct_visita:.1f}% de cuentas" if n_visitas else None)
                with r2c2:
                    st.metric("🤝 Contacto Efectivo",
                              f"{n_contacto:,}" if n_contacto is not None else "N/D",
                              delta=f"{pct_contacto:.1f}%" if n_contacto else None)
                with r2c3:
                    st.metric("💬 Promesas de Pago",
                              f"{n_promesa:,}" if n_promesa is not None else "N/D",
                              delta=f"{pct_promesa:.1f}%" if n_promesa else None)

                st.markdown("<br>", unsafe_allow_html=True)

                # Recuperación por División y Campaña lado a lado
                ej_c1, ej_c2 = st.columns(2)
                with ej_c1:
                    _gd = _grp_recovery("division")
                    if not _gd.empty and "Pagado" in _gd.columns:
                        _gd = _gd.sort_values("% Rec", ascending=True)
                        fig_div = go.Figure(go.Bar(
                            y=_gd["division"].astype(str), x=_gd["% Rec"],
                            orientation="h",
                            marker_color=[COLORS["success"] if v >= 70 else COLORS["warning"] if v >= 40 else COLORS["danger"]
                                          for v in _gd["% Rec"]],
                            text=[f"{v:.1f}%" for v in _gd["% Rec"]],
                            textposition="outside",
                            hovertemplate="%{y}<br>%{x:.1f}% recuperación<extra></extra>",
                        ))
                        fig_div.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "% Recuperación por División",
                            "height": 360,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado", range=[0, max(_gd["% Rec"].max() * 1.2, 10)]),
                            "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_div, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_div_ej")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna División para ver este gráfico.")

                with ej_c2:
                    _gc = _grp_recovery("camp")
                    if not _gc.empty and "Pagado" in _gc.columns:
                        _gc["_sort"] = _gc["camp"].apply(_camp_sort_key)
                        _gc = _gc.sort_values("_sort")
                        fig_camp = go.Figure(go.Scatter(
                            x=_gc["camp"].astype(str), y=_gc["% Rec"],
                            mode="lines+markers",
                            line=dict(color=COLORS["accent"], width=2),
                            marker=dict(size=8, color=COLORS["accent"]),
                            text=[f"{v:.1f}%" for v in _gc["% Rec"]],
                            textposition="top center",
                            hovertemplate="Campaña %{x}<br>%{y:.1f}% recuperación<extra></extra>",
                        ))
                        fig_camp.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "Tendencia de Recuperación por Campaña",
                            "height": 360,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="Campaña", type="category"),
                            "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_camp, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_line_camp_ej")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna Campaña para ver la tendencia.")

            # ── cob1: POR SEGMENTO ───────────────────────────────────────
            with cob1:
                st.markdown(
                    "<div class='kpi-banner' style='margin-bottom:1rem'>"
                    "<h1 style='font-size:1.1rem'>📊 Recuperación por Segmento de Mora</h1>"
                    "<p>Inactiva, Mora 1, Mora 2, Mora 3</p></div>",
                    unsafe_allow_html=True,
                )
                if not _safe("segmento") or not _safe("saldo_asig"):
                    st.warning("Configura las columnas Segmento Mora y Saldo Asignado.")
                else:
                    _seg_order = ["Inactiva", "Mora 1", "Mora 2", "Mora 3"]
                    _seg_colors = {
                        "Inactiva": COLORS["muted"],
                        "Mora 1":   COLORS["warning"],
                        "Mora 2":   COLORS["orange"],
                        "Mora 3":   COLORS["danger"],
                    }
                    _gs = _cob.groupby(_cob[_cc["segmento"]].astype(str).str.strip()).agg(
                        Cuentas=(_cc["saldo_asig"], "count"),
                        Asignado=(_cc["saldo_asig"], "sum"),
                        **( {"Pagado": (_cc["pago"], "sum")} if _safe("pago") else {} ),
                    ).reset_index()
                    _gs.columns.values[0] = "Segmento"
                    if "Pagado" in _gs.columns:
                        _gs["% Rec"] = (_gs["Pagado"] / _gs["Asignado"].replace(0, 1) * 100).round(1)

                    # KPIs por segmento
                    _seg_cols = st.columns(len(_gs))
                    for _idx, (_sc, _row) in enumerate(zip(_seg_cols, _gs.itertuples())):
                        with _sc:
                            _seg_pct = getattr(_row, "_Rec", 0) if hasattr(_row, "_Rec") else 0
                            st.metric(
                                str(_row.Segmento),
                                f"{int(_row.Cuentas):,} cuentas",
                                delta=f"{_seg_pct:.1f}% rec." if "Pagado" in _gs.columns else fmt_currency(_row.Asignado),
                            )

                    st.markdown("<br>", unsafe_allow_html=True)
                    seg_c1, seg_c2 = st.columns(2)

                    with seg_c1:
                        _bar_colors = [_seg_colors.get(str(s), COLORS["accent"]) for s in _gs["Segmento"]]
                        _y_pct = _gs["% Rec"].tolist() if "% Rec" in _gs.columns else [0]*len(_gs)
                        fig_seg_pct = go.Figure(go.Bar(
                            x=_gs["Segmento"].astype(str),
                            y=_y_pct,
                            marker_color=_bar_colors,
                            text=[f"{v:.1f}%" for v in _y_pct],
                            textposition="outside",
                            hovertemplate="%{x}<br>%{y:.1f}% recuperación<extra></extra>",
                        ))
                        fig_seg_pct.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "% Recuperación por Segmento",
                            "height": 340,
                            "xaxis": dict(**_AXIS_DEFAULTS, type="category"),
                            "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_seg_pct, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_seg_pct")
                        st.markdown("</div>", unsafe_allow_html=True)

                    with seg_c2:
                        fig_seg_saldo = go.Figure()
                        fig_seg_saldo.add_trace(go.Bar(
                            name="Asignado", x=_gs["Segmento"].astype(str), y=_gs["Asignado"],
                            marker_color=COLORS["muted"],
                            hovertemplate="%{x}<br>Asignado: $%{y:,.0f}<extra></extra>",
                        ))
                        if "Pagado" in _gs.columns:
                            fig_seg_saldo.add_trace(go.Bar(
                                name="Recuperado", x=_gs["Segmento"].astype(str), y=_gs["Pagado"],
                                marker_color=COLORS["success"],
                                hovertemplate="%{x}<br>Recuperado: $%{y:,.0f}<extra></extra>",
                            ))
                        fig_seg_saldo.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "Saldo Asignado vs Recuperado por Segmento",
                            "height": 340, "barmode": "group",
                            "xaxis": dict(**_AXIS_DEFAULTS, type="category"),
                            "yaxis": dict(**_AXIS_DEFAULTS, title="Monto $")})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_seg_saldo, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_seg_saldo")
                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("**Detalle por segmento**")
                    _display_seg = _gs.copy()
                    _display_seg["Asignado"] = _display_seg["Asignado"].map(lambda x: fmt_currency(x))
                    if "Pagado" in _display_seg.columns:
                        _display_seg["Pagado"] = _display_seg["Pagado"].map(lambda x: fmt_currency(x))
                        _display_seg["% Rec"] = _display_seg["% Rec"].map(lambda x: f"{x:.1f}%")
                    st.dataframe(_display_seg, use_container_width=True, hide_index=True)

            # ── cob2: GEOGRÁFICO ─────────────────────────────────────────
            with cob2:
                st.markdown(
                    "<div class='kpi-banner' style='margin-bottom:1rem'>"
                    "<h1 style='font-size:1.1rem'>🗺️ Recuperación Geográfica</h1>"
                    "<p>Por Ruta, División y Top/Bottom 10 Zonas</p></div>",
                    unsafe_allow_html=True,
                )
                geo_c1, geo_c2 = st.columns(2)

                with geo_c1:
                    _gr = _grp_recovery("ruta")
                    if not _gr.empty and "Pagado" in _gr.columns:
                        _gr = _gr.sort_values("% Rec", ascending=True).tail(15)
                        fig_ruta = go.Figure(go.Bar(
                            y=_gr["ruta"].astype(str), x=_gr["% Rec"],
                            orientation="h",
                            marker_color=[COLORS["success"] if v >= 70 else COLORS["warning"] if v >= 40 else COLORS["danger"]
                                          for v in _gr["% Rec"]],
                            text=[f"{v:.1f}%" for v in _gr["% Rec"]],
                            textposition="outside",
                            hovertemplate="Ruta %{y}<br>%{x:.1f}% recuperación<extra></extra>",
                        ))
                        fig_ruta.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "% Recuperación por Ruta (Top 15)",
                            "height": 420,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                            "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_ruta, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_ruta")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna Ruta para ver este gráfico.")

                with geo_c2:
                    _gd2 = _grp_recovery("division")
                    if not _gd2.empty and "Pagado" in _gd2.columns:
                        _gd2 = _gd2.sort_values("% Rec", ascending=False)
                        fig_div2 = go.Figure(go.Bar(
                            x=_gd2["division"].astype(str), y=_gd2["% Rec"],
                            marker_color=[COLORS["success"] if v >= 70 else COLORS["warning"] if v >= 40 else COLORS["danger"]
                                          for v in _gd2["% Rec"]],
                            text=[f"{v:.1f}%" for v in _gd2["% Rec"]],
                            textposition="outside",
                            hovertemplate="División %{x}<br>%{y:.1f}% recuperación<extra></extra>",
                        ))
                        fig_div2.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "% Recuperación por División",
                            "height": 420,
                            "xaxis": dict(**_AXIS_DEFAULTS, type="category", automargin=True),
                            "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_div2, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_div2")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna División para ver este gráfico.")

                st.markdown("---")
                st.markdown("**🏆 Top 10 y Bottom 10 Zonas**")

                _gz = _grp_recovery("zona")
                if not _gz.empty and "Pagado" in _gz.columns and len(_gz) >= 2:
                    _top10 = _gz.nlargest(10, "% Rec")
                    _bot10 = _gz.nsmallest(10, "% Rec")

                    top_c, bot_c = st.columns(2)
                    with top_c:
                        fig_top = go.Figure(go.Bar(
                            y=_top10["zona"].astype(str),
                            x=_top10["% Rec"],
                            orientation="h",
                            marker_color=COLORS["success"],
                            text=[f"{v:.1f}%" for v in _top10["% Rec"]],
                            textposition="outside",
                            hovertemplate="Zona %{y}<br>%{x:.1f}%<extra></extra>",
                        ))
                        fig_top.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "🏆 Top 10 Zonas",
                            "height": 360,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                            "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_top, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_top10")
                        st.markdown("</div>", unsafe_allow_html=True)

                    with bot_c:
                        fig_bot = go.Figure(go.Bar(
                            y=_bot10["zona"].astype(str),
                            x=_bot10["% Rec"],
                            orientation="h",
                            marker_color=COLORS["danger"],
                            text=[f"{v:.1f}%" for v in _bot10["% Rec"]],
                            textposition="outside",
                            hovertemplate="Zona %{y}<br>%{x:.1f}%<extra></extra>",
                        ))
                        fig_bot.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "⚠️ Bottom 10 Zonas",
                            "height": 360,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                            "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_bot, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bot10")
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Configura la columna Zona para ver el ranking Top/Bottom 10.")

            # ── cob3: GESTIÓN ────────────────────────────────────────────
            with cob3:
                st.markdown(
                    "<div class='kpi-banner' style='margin-bottom:1rem'>"
                    "<h1 style='font-size:1.1rem'>🚗 Indicadores de Gestión</h1>"
                    "<p>Visitas, Dictaminación y Contacto efectivo</p></div>",
                    unsafe_allow_html=True,
                )
                gest_c1, gest_c2 = st.columns(2)

                with gest_c1:
                    # Distribución de Estatus de Cuenta
                    if _safe("estatus"):
                        _est_counts = (
                            _cob[_cc["estatus"]].astype(str).str.strip()
                            .value_counts().reset_index()
                        )
                        _est_counts.columns = ["Estatus", "Cuentas"]
                        _est_pct = _est_counts["Cuentas"] / _est_counts["Cuentas"].sum() * 100
                        fig_est = go.Figure(go.Pie(
                            labels=_est_counts["Estatus"],
                            values=_est_counts["Cuentas"],
                            hole=0.45,
                            textinfo="percent+label",
                            hovertemplate="%{label}<br>%{value:,} cuentas (%{percent})<extra></extra>",
                        ))
                        fig_est.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "Distribución de Estatus de Cuenta",
                            "height": 380, "showlegend": False})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_est, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_pie_estatus")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna Estatus Cuenta.")

                with gest_c2:
                    # Distribución de Dictaminación
                    if _safe("dictam"):
                        _dict_counts = (
                            _cob[_cc["dictam"]].astype(str).str.strip()
                            .value_counts().reset_index()
                        )
                        _dict_counts.columns = ["Dictaminación", "Cuentas"]
                        fig_dict = go.Figure(go.Pie(
                            labels=_dict_counts["Dictaminación"],
                            values=_dict_counts["Cuentas"],
                            hole=0.45,
                            textinfo="percent+label",
                            hovertemplate="%{label}<br>%{value:,} cuentas (%{percent})<extra></extra>",
                        ))
                        fig_dict.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "Contacto por Dictaminación",
                            "height": 380, "showlegend": False})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_dict, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_pie_dictam")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna Dictaminación.")

                st.markdown("<br>", unsafe_allow_html=True)

                # Resultado de visitas y recuperación por visita
                gest_c3, gest_c4 = st.columns(2)

                with gest_c3:
                    if _safe("res_visita"):
                        _rv_counts = (
                            _cob[_cc["res_visita"]].astype(str).str.strip()
                            .value_counts().reset_index()
                        )
                        _rv_counts.columns = ["Resultado", "Cuentas"]
                        fig_rv = go.Figure(go.Bar(
                            y=_rv_counts["Resultado"], x=_rv_counts["Cuentas"],
                            orientation="h",
                            marker_color=COLORS["accent"],
                            text=_rv_counts["Cuentas"],
                            textposition="outside",
                            hovertemplate="%{y}<br>%{x:,} cuentas<extra></extra>",
                        ))
                        fig_rv.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "Contacto por Resultado de Visita",
                            "height": 360,
                            "xaxis": _AXIS_DEFAULTS,
                            "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_rv, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_bar_rv")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura la columna Resultado Visita.")

                with gest_c4:
                    # % Recuperación por Zona (scatter)
                    _gz2 = _grp_recovery("zona")
                    if not _gz2.empty and "Pagado" in _gz2.columns and _safe("saldo_asig"):
                        fig_zona_scatter = go.Figure(go.Scatter(
                            x=_gz2["Asignado"],
                            y=_gz2["% Rec"],
                            mode="markers+text",
                            text=_gz2["zona"].astype(str),
                            textposition="top center",
                            marker=dict(
                                size=10,
                                color=_gz2["% Rec"],
                                colorscale="RdYlGn",
                                showscale=True,
                                colorbar=dict(title="% Rec"),
                            ),
                            hovertemplate="Zona %{text}<br>Asignado: $%{x:,.0f}<br>%{y:.1f}% rec.<extra></extra>",
                        ))
                        fig_zona_scatter.update_layout(**{**PLOTLY_LAYOUT,
                            "title": "% Recuperación por Zona (tamaño = saldo asignado)",
                            "height": 360,
                            "xaxis": dict(**_AXIS_DEFAULTS, title="Saldo Asignado"),
                            "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.plotly_chart(fig_zona_scatter, use_container_width=True,
                                        config={"displayModeBar": False}, key="cob_scatter_zona")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Configura las columnas Zona y Saldo Asignado.")

            # ── cob4: ALERTAS ────────────────────────────────────────────
            with cob4:
                st.markdown(
                    "<div class='kpi-banner' style='margin-bottom:1rem'>"
                    "<h1 style='font-size:1.1rem'>⚠️ Alertas de Bajo Desempeño</h1>"
                    "<p>Zonas, rutas y segmentos que requieren atención</p></div>",
                    unsafe_allow_html=True,
                )

                _threshold = st.slider("Umbral de alerta (% recuperación)", 0, 100, 30, 5,
                                       key="cob_alert_thresh",
                                       help="Se marcan como alerta las unidades con recuperación por debajo de este valor")

                alertas_encontradas = False

                # Alertas por zona
                _gz3 = _grp_recovery("zona")
                if not _gz3.empty and "Pagado" in _gz3.columns:
                    _alertas_zona = _gz3[_gz3["% Rec"] < _threshold].sort_values("% Rec")
                    if not _alertas_zona.empty:
                        alertas_encontradas = True
                        st.error(f"🚨 **{len(_alertas_zona)} zonas** con recuperación < {_threshold}%")
                        _alertas_zona_disp = _alertas_zona.copy()
                        _alertas_zona_disp["Asignado"] = _alertas_zona_disp["Asignado"].map(fmt_currency)
                        _alertas_zona_disp["Pagado"]   = _alertas_zona_disp["Pagado"].map(fmt_currency)
                        _alertas_zona_disp["% Rec"]    = _alertas_zona_disp["% Rec"].map(lambda x: f"{x:.1f}%")
                        st.dataframe(_alertas_zona_disp.rename(columns={"zona": "Zona"}),
                                     use_container_width=True, hide_index=True)

                # Alertas por ruta
                _gr2 = _grp_recovery("ruta")
                if not _gr2.empty and "Pagado" in _gr2.columns:
                    _alertas_ruta = _gr2[_gr2["% Rec"] < _threshold].sort_values("% Rec")
                    if not _alertas_ruta.empty:
                        alertas_encontradas = True
                        st.warning(f"⚠️ **{len(_alertas_ruta)} rutas** con recuperación < {_threshold}%")
                        _ar_disp = _alertas_ruta.copy()
                        _ar_disp["Asignado"] = _ar_disp["Asignado"].map(fmt_currency)
                        _ar_disp["Pagado"]   = _ar_disp["Pagado"].map(fmt_currency)
                        _ar_disp["% Rec"]    = _ar_disp["% Rec"].map(lambda x: f"{x:.1f}%")
                        st.dataframe(_ar_disp.rename(columns={"ruta": "Ruta"}),
                                     use_container_width=True, hide_index=True)

                # Alertas por segmento
                if _safe("segmento") and _safe("saldo_asig"):
                    _gs2 = _cob.groupby(_cob[_cc["segmento"]].astype(str).str.strip()).agg(
                        Asignado=(_cc["saldo_asig"], "sum"),
                        **( {"Pagado": (_cc["pago"], "sum")} if _safe("pago") else {} ),
                    ).reset_index()
                    _gs2.columns.values[0] = "Segmento"
                    if "Pagado" in _gs2.columns:
                        _gs2["% Rec"] = (_gs2["Pagado"] / _gs2["Asignado"].replace(0, 1) * 100).round(1)
                        _alertas_seg = _gs2[_gs2["% Rec"] < _threshold]
                        if not _alertas_seg.empty:
                            alertas_encontradas = True
                            st.warning(f"📊 Segmentos con recuperación < {_threshold}%: "
                                       + ", ".join(f"**{r.Segmento}** ({r._Rec:.1f}%)" for r in _alertas_seg.itertuples()))

                if not alertas_encontradas:
                    st.success(f"✅ No hay alertas — todas las unidades tienen recuperación ≥ {_threshold}%")


# ─────────────────────────────────────────────
#  INDICADORES DE RECUPERACIÓN — TAB STANDALONE
# ─────────────────────────────────────────────

def tab_indicadores(df):
    """Dashboard de indicadores de recuperación de cartera basado en un archivo único."""
    _cc = {
        "camp":     _find_col(df, ["anio", "aniocampania", "campaña de trabajo", "campaña"]),
        "division": _find_col(df, ["division", "división"]),
        "ruta":     _find_col(df, ["ruta"]),
        "zona":     _find_col(df, ["zona"]),
        "region":   _find_col(df, ["region", "región"]),
        "nodama":   _find_col(df, ["nodama", "dama"]),
        "segmento": _find_col(df, ["morosidad", "mora", "segmento"]),
        "saldo":    _find_col(df, ["saldodama", "saldo"]),
        "pago":     _find_col(df, ["pago aplicado", "pago_aplicado", "cobrado", "recuperado", "pago "]),
        "visita":   _find_col(df, ["visitas gestor", "visita"]),
        "dictam":   _find_col(df, ["dictaminacion", "dictam"]),
        "situacion": _find_col(df, ["descsituacion", "situacion", "estatus"]),
    }

    with st.expander("⚙️ Ajustar columnas — Cartera General"):
        _all = list(df.columns)
        _i1, _i2, _i3, _i4 = st.columns(4)
        def _sel(label, key, k, col):
            opts = ["(ninguna)"] + _all
            idx = opts.index(_cc[k]) if _cc[k] and _cc[k] in opts else 0
            val = col.selectbox(label, opts, index=idx, key=key)
            _cc[k] = None if val == "(ninguna)" else val
        with _i1:
            _sel("Campaña",        "ind_c_camp", "camp",     _i1)
            _sel("División",       "ind_c_div",  "division", _i1)
            _sel("Ruta",           "ind_c_ruta", "ruta",     _i1)
        with _i2:
            _sel("Zona",           "ind_c_zona", "zona",     _i2)
            _sel("Región",         "ind_c_reg",  "region",   _i2)
            _sel("Número de Dama", "ind_c_nd",   "nodama",   _i2)
        with _i3:
            _sel("Segmento Mora",  "ind_c_seg",  "segmento", _i3)
            _sel("Saldo Asignado", "ind_c_sal",  "saldo",    _i3)
            _sel("Pago Aplicado",  "ind_c_pago_v2", "pago",     _i3)
        with _i4:
            _sel("Visita/Resultado","ind_c_vis",  "visita",   _i4)
            _sel("Dictaminación",  "ind_c_dic",  "dictam",   _i4)
            _sel("Situación",      "ind_c_sit",  "situacion",_i4)

    def _safe(k): return bool(_cc.get(k) and _cc[k] in df.columns)
    def _col(k):  return _cc[k]

    _d = df.copy()
    for _k in ["saldo", "pago"]:
        if _safe(_k):
            _d[_col(_k)] = pd.to_numeric(_d[_col(_k)], errors="coerce").fillna(0)

    n_total    = len(_d)
    saldo_tot  = _d[_col("saldo")].sum() if _safe("saldo") else 0
    pago_tot   = _d[_col("pago")].sum()  if _safe("pago")  else 0
    pct_rec    = pago_tot / saldo_tot * 100 if saldo_tot else 0
    n_pagadas  = int((_d[_col("pago")] > 0).sum()) if _safe("pago") else 0
    pct_pagadas = n_pagadas / n_total * 100 if n_total else 0
    n_visitas  = int(_d[_col("visita")].notna().sum()) if _safe("visita") else 0
    pct_vis    = n_visitas / n_total * 100 if n_total else 0

    # Promesas de pago (visita o dictaminación)
    _prom_mask = pd.Series(False, index=_d.index)
    if _safe("visita"):
        _prom_mask |= _d[_col("visita")].astype(str).str.upper().str.contains("PROMESA", na=False)
    if _safe("dictam"):
        _prom_mask |= _d[_col("dictam")].astype(str).str.upper().str.contains("PROMESA", na=False)
    n_promesas  = int(_prom_mask.sum())
    pct_promesas = n_promesas / n_total * 100 if n_total else 0

    # Estatus derivado (vectorizado)
    if _safe("pago"):
        _pago_s = _d[_col("pago")].fillna(0)
        _vis_s  = _d[_col("visita")].fillna("").astype(str).str.upper() if _safe("visita") else pd.Series("", index=_d.index)
        _dic_s  = _d[_col("dictam")].fillna("").astype(str).str.upper() if _safe("dictam") else pd.Series("", index=_d.index)
        _conds   = [
            _pago_s > 0,
            _vis_s.str.contains("PROMESA", na=False),
            _vis_s.str.contains("PAGO", na=False),
            _vis_s.str.strip().ne(""),
            _dic_s.str.strip().ne(""),
        ]
        _choices = ["Recuperada", "Promesa de Pago", "Pago Cobrador/Porteador",
                    "Gestionada - Visita", "Gestionada - Llamada"]
        _d["_estatus"] = np.select(_conds, _choices, default="Sin Gestión")
        estatus_col = "_estatus"
    elif _safe("situacion"):
        estatus_col = _col("situacion")
    else:
        estatus_col = None

    # Groupby helper
    def _grp(col_key, top_n=None):
        if not _safe(col_key) or not _safe("saldo"):
            return pd.DataFrame()
        _gcol = _d[_col(col_key)].astype(str).str.strip()
        g = _d.groupby(_gcol).agg(
            Cuentas=(_col("saldo"), "count"),
            Asignado=(_col("saldo"), "sum"),
            **( {"Pagado": (_col("pago"), "sum")} if _safe("pago") else {} ),
        ).reset_index()
        g.columns = [col_key] + list(g.columns[1:])
        if "Pagado" in g.columns:
            g["PctRec"] = (g["Pagado"] / g["Asignado"].replace(0, 1) * 100).round(1)
        if top_n:
            g = g.nlargest(top_n, "Cuentas")
        return g

    def _color_pct(v):
        return COLORS["success"] if v >= 70 else COLORS["warning"] if v >= 40 else COLORS["danger"]

    # Sub-tabs
    cob0, cob1, cob2, cob3, cob4 = st.tabs([
        "📋 Ejecutivo", "📊 Por Segmento", "🗺️ Geográfico", "🚗 Gestión", "⚠️ Alertas"
    ])

    # ── EJECUTIVO ──────────────────────────────────────────────────────
    with cob0:
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h1 style='font-size:1.1rem'>📋 Indicadores Ejecutivos de Recuperación</h1>"
            "<p>Resumen gerencial de desempeño de cobranza</p></div>",
            unsafe_allow_html=True,
        )
        _r1a, _r1b, _r1c, _r1d = st.columns(4)
        with _r1a: st.metric("📂 Cuentas Asignadas",  f"{n_total:,}")
        with _r1b: st.metric("💰 Saldo Asignado",     fmt_currency(saldo_tot))
        with _r1c: st.metric("✅ Saldo Recuperado",   fmt_currency(pago_tot),  delta=f"{pct_rec:.1f}%")
        with _r1d: st.metric("📈 % Recuperación",     f"{pct_rec:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        _r2a, _r2b, _r2c, _r2d = st.columns(4)
        with _r2a: st.metric("🔢 Cuentas Recuperadas", f"{n_pagadas:,}",   delta=f"{pct_pagadas:.1f}% de cuentas")
        with _r2b: st.metric("🚗 Visitas Realizadas",  f"{n_visitas:,}",   delta=f"{pct_vis:.1f}%")
        with _r2c: st.metric("💬 Promesas de Pago",    f"{n_promesas:,}",  delta=f"{pct_promesas:.1f}%")
        with _r2d:
            _contacto = int((_d[_col("visita")].notna()).sum()) if _safe("visita") else 0
            st.metric("🤝 Contacto Efectivo", f"{_contacto:,}", delta=f"{_contacto/n_total*100:.1f}%" if n_total else None)

        st.markdown("<br>", unsafe_allow_html=True)
        _ej1, _ej2 = st.columns(2)
        with _ej1:
            _gd = _grp("division")
            if not _gd.empty and "PctRec" in _gd.columns:
                _gd = _gd.sort_values("PctRec", ascending=True)
                _fig = go.Figure(go.Bar(
                    y=_gd["division"].astype(str), x=_gd["PctRec"], orientation="h",
                    marker_color=[_color_pct(v) for v in _gd["PctRec"]],
                    text=[f"{v:.1f}%" for v in _gd["PctRec"]], textposition="outside",
                    hovertemplate="%{y}<br>%{x:.1f}%<extra></extra>",
                ))
                _fig.update_layout(**{**PLOTLY_LAYOUT, "title": "% Recuperación por División",
                    "height": 340, "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                    "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fig, use_container_width=True, config={"displayModeBar": False}, key="ind_ej_div")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura División para ver este gráfico.")

        with _ej2:
            _gc = _grp("camp")
            if not _gc.empty and "PctRec" in _gc.columns:
                try: _gc["_s"] = _gc["camp"].apply(_camp_sort_key)
                except Exception: _gc["_s"] = _gc["camp"].astype(str)
                _gc = _gc.sort_values("_s")
                _fig2 = go.Figure(go.Scatter(
                    x=_gc["camp"].astype(str), y=_gc["PctRec"],
                    mode="lines+markers+text",
                    line=dict(color=COLORS["accent"], width=2),
                    marker=dict(size=8, color=COLORS["accent"]),
                    text=[f"{v:.1f}%" for v in _gc["PctRec"]],
                    textposition="top center",
                    hovertemplate="Campaña %{x}<br>%{y:.1f}%<extra></extra>",
                ))
                _fig2.update_layout(**{**PLOTLY_LAYOUT, "title": "Tendencia Recuperación por Campaña",
                    "height": 340, "xaxis": dict(**_AXIS_DEFAULTS, title="Campaña", type="category"),
                    "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fig2, use_container_width=True, config={"displayModeBar": False}, key="ind_ej_camp")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura Campaña para ver la tendencia.")

    # ── POR SEGMENTO ───────────────────────────────────────────────────
    with cob1:
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h1 style='font-size:1.1rem'>📊 Recuperación por Segmento de Mora</h1>"
            "<p>Inactivas, Mora 1, Mora 2, Mora 3</p></div>",
            unsafe_allow_html=True,
        )
        if not _safe("segmento") or not _safe("saldo"):
            st.warning("Configura las columnas Segmento Mora y Saldo Asignado.")
        else:
            _seg_col_name = _col("segmento")
            _gs = _d.groupby(_d[_seg_col_name].astype(str).str.strip()).agg(
                Cuentas=(_col("saldo"), "count"),
                Asignado=(_col("saldo"), "sum"),
                **( {"Pagado": (_col("pago"), "sum")} if _safe("pago") else {} ),
            ).reset_index()
            _gs.columns = ["Segmento"] + list(_gs.columns[1:])
            if "Pagado" in _gs.columns:
                _gs["PctRec"] = (_gs["Pagado"] / _gs["Asignado"].replace(0, 1) * 100).round(1)

            _seg_colors_map = {"Inactiva": COLORS["muted"], "Inactivas": COLORS["muted"],
                               "Mora 1": COLORS["warning"], "Mora 2": COLORS.get("orange", "#f97316"),
                               "Mora 3": COLORS["danger"]}

            _scols = st.columns(len(_gs))
            for _sc, _row in zip(_scols, _gs.itertuples()):
                with _sc:
                    _pr = getattr(_row, "PctRec", 0)
                    st.metric(str(_row.Segmento), f"{int(_row.Cuentas):,} ctas",
                              delta=f"{_pr:.1f}% rec." if "Pagado" in _gs.columns else fmt_currency(_row.Asignado))

            st.markdown("<br>", unsafe_allow_html=True)
            _sc1, _sc2 = st.columns(2)
            with _sc1:
                _y = _gs["PctRec"].tolist() if "PctRec" in _gs.columns else [0]*len(_gs)
                _colors_seg = [_seg_colors_map.get(str(s), COLORS["accent"]) for s in _gs["Segmento"]]
                _fig_s = go.Figure(go.Bar(
                    x=_gs["Segmento"].astype(str), y=_y,
                    marker_color=_colors_seg,
                    text=[f"{v:.1f}%" for v in _y], textposition="outside",
                    hovertemplate="%{x}<br>%{y:.1f}%<extra></extra>",
                ))
                _fig_s.update_layout(**{**PLOTLY_LAYOUT, "title": "% Recuperación por Segmento",
                    "height": 340, "xaxis": dict(**_AXIS_DEFAULTS, type="category"),
                    "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fig_s, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_seg_pct")
                st.markdown("</div>", unsafe_allow_html=True)

            with _sc2:
                _fig_s2 = go.Figure()
                _fig_s2.add_trace(go.Bar(name="Asignado", x=_gs["Segmento"].astype(str), y=_gs["Asignado"],
                    marker_color=COLORS["muted"], hovertemplate="%{x}<br>Asignado: $%{y:,.0f}<extra></extra>"))
                if "Pagado" in _gs.columns:
                    _fig_s2.add_trace(go.Bar(name="Recuperado", x=_gs["Segmento"].astype(str), y=_gs["Pagado"],
                        marker_color=COLORS["success"], hovertemplate="%{x}<br>Recuperado: $%{y:,.0f}<extra></extra>"))
                _fig_s2.update_layout(**{**PLOTLY_LAYOUT, "title": "Saldo Asignado vs Recuperado",
                    "height": 340, "barmode": "group",
                    "xaxis": dict(**_AXIS_DEFAULTS, type="category"),
                    "yaxis": dict(**_AXIS_DEFAULTS, title="Monto $")})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fig_s2, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_seg_saldo")
                st.markdown("</div>", unsafe_allow_html=True)

            _gs_disp = _gs.copy()
            _gs_disp["Asignado"] = _gs_disp["Asignado"].map(fmt_currency)
            if "Pagado" in _gs_disp.columns:
                _gs_disp["Pagado"]  = _gs_disp["Pagado"].map(fmt_currency)
                _gs_disp["PctRec"] = _gs_disp["PctRec"].map(lambda x: f"{x:.1f}%")
            st.dataframe(_gs_disp, use_container_width=True, hide_index=True)

    # ── GEOGRÁFICO ─────────────────────────────────────────────────────
    with cob2:
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h1 style='font-size:1.1rem'>🗺️ Recuperación Geográfica</h1>"
            "<p>Por Ruta, División y Top/Bottom 10 Zonas</p></div>",
            unsafe_allow_html=True,
        )
        _geo1, _geo2 = st.columns(2)
        with _geo1:
            _gr = _grp("ruta")
            if not _gr.empty and "PctRec" in _gr.columns:
                _gr = _gr.sort_values("PctRec", ascending=True).tail(15)
                _fg = go.Figure(go.Bar(
                    y=_gr["ruta"].astype(str), x=_gr["PctRec"], orientation="h",
                    marker_color=[_color_pct(v) for v in _gr["PctRec"]],
                    text=[f"{v:.1f}%" for v in _gr["PctRec"]], textposition="outside",
                    hovertemplate="Ruta %{y}<br>%{x:.1f}%<extra></extra>",
                ))
                _fg.update_layout(**{**PLOTLY_LAYOUT, "title": "% Recuperación por Ruta (Top 15)",
                    "height": 420, "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                    "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fg, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_ruta")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura la columna Ruta.")

        with _geo2:
            _gd3 = _grp("division")
            if not _gd3.empty and "PctRec" in _gd3.columns:
                _gd3 = _gd3.sort_values("PctRec", ascending=False)
                _fg2 = go.Figure(go.Bar(
                    x=_gd3["division"].astype(str), y=_gd3["PctRec"],
                    marker_color=[_color_pct(v) for v in _gd3["PctRec"]],
                    text=[f"{v:.1f}%" for v in _gd3["PctRec"]], textposition="outside",
                    hovertemplate="División %{x}<br>%{y:.1f}%<extra></extra>",
                ))
                _fg2.update_layout(**{**PLOTLY_LAYOUT, "title": "% Recuperación por División",
                    "height": 420, "xaxis": dict(**_AXIS_DEFAULTS, type="category", automargin=True),
                    "yaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado")})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fg2, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_div_geo")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura la columna División.")

        st.markdown("---")
        st.markdown("**🏆 Top 10 y Bottom 10 Zonas**")
        _gz = _grp("zona")
        if not _gz.empty and "PctRec" in _gz.columns and len(_gz) >= 2:
            _top10 = _gz.nlargest(10, "PctRec")
            _bot10 = _gz.nsmallest(10, "PctRec")
            _tc, _bc = st.columns(2)
            with _tc:
                _ft = go.Figure(go.Bar(
                    y=_top10["zona"].astype(str), x=_top10["PctRec"], orientation="h",
                    marker_color=COLORS["success"],
                    text=[f"{v:.1f}%" for v in _top10["PctRec"]], textposition="outside",
                    hovertemplate="Zona %{y}<br>%{x:.1f}%<extra></extra>",
                ))
                _ft.update_layout(**{**PLOTLY_LAYOUT, "title": "🏆 Top 10 Zonas", "height": 360,
                    "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                    "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_ft, use_container_width=True, config={"displayModeBar": False}, key="ind_top10")
                st.markdown("</div>", unsafe_allow_html=True)
            with _bc:
                _fb = go.Figure(go.Bar(
                    y=_bot10["zona"].astype(str), x=_bot10["PctRec"], orientation="h",
                    marker_color=COLORS["danger"],
                    text=[f"{v:.1f}%" for v in _bot10["PctRec"]], textposition="outside",
                    hovertemplate="Zona %{y}<br>%{x:.1f}%<extra></extra>",
                ))
                _fb.update_layout(**{**PLOTLY_LAYOUT, "title": "⚠️ Bottom 10 Zonas", "height": 360,
                    "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                    "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fb, use_container_width=True, config={"displayModeBar": False}, key="ind_bot10")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Configura la columna Zona para ver el ranking.")

    # ── GESTIÓN ────────────────────────────────────────────────────────
    with cob3:
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h1 style='font-size:1.1rem'>🚗 Indicadores de Gestión</h1>"
            "<p>Estatus de cuentas, dictaminación y resultado de visitas</p></div>",
            unsafe_allow_html=True,
        )
        _gst1, _gst2 = st.columns(2)
        with _gst1:
            if estatus_col:
                _est = _d[estatus_col].astype(str).str.strip().value_counts().reset_index()
                _est.columns = ["Estatus", "Cuentas"]
                _fpe = go.Figure(go.Pie(
                    labels=_est["Estatus"], values=_est["Cuentas"], hole=0.45,
                    textinfo="percent+label",
                    hovertemplate="%{label}<br>%{value:,} cuentas (%{percent})<extra></extra>",
                ))
                _fpe.update_layout(**{**PLOTLY_LAYOUT, "title": "Distribución de Estatus", "height": 380, "showlegend": False})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fpe, use_container_width=True, config={"displayModeBar": False}, key="ind_pie_estatus")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura columna Situación o Pago para derivar el estatus.")

        with _gst2:
            if _safe("dictam"):
                _dic = (_d[_col("dictam")].astype(str).str.strip()
                        .value_counts().head(10).reset_index())
                _dic.columns = ["Dictaminación", "Cuentas"]
                _fpd = go.Figure(go.Pie(
                    labels=_dic["Dictaminación"], values=_dic["Cuentas"], hole=0.45,
                    textinfo="percent+label",
                    hovertemplate="%{label}<br>%{value:,} cuentas (%{percent})<extra></extra>",
                ))
                _fpd.update_layout(**{**PLOTLY_LAYOUT, "title": "Contacto por Dictaminación (Top 10)", "height": 380, "showlegend": False})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fpd, use_container_width=True, config={"displayModeBar": False}, key="ind_pie_dictam")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura la columna Dictaminación.")

        st.markdown("<br>", unsafe_allow_html=True)
        _gst3, _gst4 = st.columns(2)
        with _gst3:
            if _safe("visita"):
                _vis = (_d[_col("visita")].dropna().astype(str).str.strip()
                        .value_counts().head(10).reset_index())
                _vis.columns = ["Resultado", "Cuentas"]
                _fvr = go.Figure(go.Bar(
                    y=_vis["Resultado"], x=_vis["Cuentas"], orientation="h",
                    marker_color=COLORS["accent"],
                    text=_vis["Cuentas"], textposition="outside",
                    hovertemplate="%{y}<br>%{x:,} cuentas<extra></extra>",
                ))
                _fvr.update_layout(**{**PLOTLY_LAYOUT, "title": "Resultado de Visitas (Top 10)", "height": 380,
                    "xaxis": _AXIS_DEFAULTS, "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fvr, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_vis_res")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura la columna Visita/Resultado.")

        with _gst4:
            _gz2 = _grp("zona")
            if not _gz2.empty and "PctRec" in _gz2.columns:
                _gz2_s = _gz2.sort_values("PctRec", ascending=True)
                _fzr = go.Figure(go.Bar(
                    y=_gz2_s["zona"].astype(str), x=_gz2_s["PctRec"], orientation="h",
                    marker_color=[_color_pct(v) for v in _gz2_s["PctRec"]],
                    text=[f"{v:.1f}%" for v in _gz2_s["PctRec"]], textposition="outside",
                    hovertemplate="Zona %{y}<br>%{x:.1f}%<extra></extra>",
                ))
                _fzr.update_layout(**{**PLOTLY_LAYOUT, "title": "% Recuperación por Zona", "height": 380,
                    "xaxis": dict(**_AXIS_DEFAULTS, title="% Recuperado"),
                    "yaxis": dict(**_AXIS_DEFAULTS, automargin=True)})
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.plotly_chart(_fzr, use_container_width=True, config={"displayModeBar": False}, key="ind_bar_zona_rec")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Configura la columna Zona.")

    # ── ALERTAS ────────────────────────────────────────────────────────
    with cob4:
        st.markdown(
            "<div class='kpi-banner' style='margin-bottom:1rem'>"
            "<h1 style='font-size:1.1rem'>⚠️ Alertas de Bajo Desempeño</h1>"
            "<p>Unidades con recuperación por debajo del umbral definido</p></div>",
            unsafe_allow_html=True,
        )
        _thr = st.slider("Umbral de alerta (% recuperación)", 0, 100, 30, 5, key="ind_alert_thr")
        _hay_alertas = False
        for _ak, _alabel in [("zona", "Zona"), ("ruta", "Ruta"), ("division", "División")]:
            _ag = _grp(_ak)
            if not _ag.empty and "PctRec" in _ag.columns:
                _bad = _ag[_ag["PctRec"] < _thr].sort_values("PctRec")
                if not _bad.empty:
                    _hay_alertas = True
                    _badge_fn = st.error if _ak == "zona" else st.warning
                    _badge_fn(f"**{len(_bad)} {_alabel}{'s' if len(_bad)!=1 else ''}** con recuperación < {_thr}%")
                    _bd = _bad.copy()
                    _bd["Asignado"] = _bd["Asignado"].map(fmt_currency)
                    if "Pagado" in _bd.columns:
                        _bd["Pagado"]  = _bd["Pagado"].map(fmt_currency)
                        _bd["PctRec"] = _bd["PctRec"].map(lambda x: f"{x:.1f}%")
                    st.dataframe(_bd.rename(columns={_ak: _alabel}), use_container_width=True, hide_index=True)

        if not _hay_alertas:
            st.success(f"✅ Sin alertas — todas las unidades tienen recuperación ≥ {_thr}%")


def _render_indicadores_standalone():
    """Tab independiente de Indicadores de Recuperación."""
    st.markdown(
        "<div class='kpi-banner'>"
        "<h1>📊 Indicadores de Recuperación de Cartera</h1>"
        "<p>Dashboard de cobranza — carga tu archivo de Cartera General para ver los indicadores</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("📂 Cargar archivo de Cartera General",
                     expanded=st.session_state.get("df_cartera_gral") is None):
        _f = st.file_uploader(
            "Cartera General", type=["xlsx", "xls"],
            label_visibility="collapsed", key="up_cartera_gral"
        )
        if _f:
            if [_f.name] != st.session_state.get("int_cartera_gral_name", []):
                try:
                    st.session_state.df_cartera_gral = read_excel_safe(_f)
                    st.session_state.int_cartera_gral_name = [_f.name]
                except Exception as e:
                    st.error(f"Error al leer archivo: {e}")
        if st.session_state.get("df_cartera_gral") is not None:
            _nm = st.session_state.int_cartera_gral_name
            _nr = len(st.session_state.df_cartera_gral)
            st.markdown(
                f"<span style='background:#dcfce7;color:#16a34a;padding:2px 10px;"
                f"border-radius:99px;font-size:0.78rem;font-weight:600'>"
                f"✓ {_nm[0] if _nm else 'Cargado'} — {_nr:,} registros</span>",
                unsafe_allow_html=True,
            )

    if st.session_state.get("df_cartera_gral") is None:
        st.info("⬆️ Sube el archivo de Cartera General para ver los indicadores de recuperación.")
        return

    try:
        tab_indicadores(st.session_state.df_cartera_gral)
    except Exception as _e:
        st.error(f"Error en Indicadores: {_e}")
        import traceback
        st.code(traceback.format_exc())


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    # ── Inicializar session_state ─────────────────────────────────────
    for key, default in [
        ("data", None), ("df_cartera", None), ("df_saldos", None),
        ("mapping", None), ("file_names", (None, None)), ("df_moras", None),
        ("df_tel", None), ("df_campo", None), ("df_cobranza", None),
        ("df_cartera_gral", None), ("int_cartera_gral_name", []),
        ("int_tel_names", []), ("int_campo_names", []), ("int_cob_names", []),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    filters = render_sidebar(st.session_state.data)

    # ── Aplicar color de fondo dinámico ───────────────────────────────
    _bg = st.session_state.get("bg_color", "#f0f2f6")
    _is_dark = int(_bg.lstrip("#")[0:2], 16) < 80
    _text_color = "#e8edf5" if _is_dark else "#1a3c6e"
    _mode_3d = st.session_state.get("visual_mode", "Clásico") == "3D Animado"

    _base_css = (
        f"[data-testid='stAppViewContainer'], [data-testid='stMain'], .main "
        f"{{ background-color: {_bg} !important; }}"
        f"h1, h2, h3, h4 {{ color: {_text_color} !important; }}"
    )
    # Empuja el tab "Interno" (último botón en el primer stTabBar) a la derecha
    _TAB_RIGHT_CSS = (
        "[data-testid='stTabBar']:first-of-type "
        "{ display:flex !important; width:100% !important; }"
        "[data-testid='stTabBar']:first-of-type > div:last-child "
        "{ margin-left:auto !important; }"
    )

    if _mode_3d:
        # Derive accent colors from bg for animated gradient
        _r = int(_bg.lstrip("#")[0:2], 16)
        _g = int(_bg.lstrip("#")[2:4], 16)
        _b = int(_bg.lstrip("#")[4:6], 16)
        _bg2 = "#{:02x}{:02x}{:02x}".format(
            min(255, _r + 18), min(255, _g + 22), min(255, _b + 38)
        )
        _bg3 = "#{:02x}{:02x}{:02x}".format(
            max(0, _r - 14), max(0, _g - 10), min(255, _b + 28)
        )
        _bg4 = "#{:02x}{:02x}{:02x}".format(
            min(255, _r + 8), max(0, _g - 6), max(0, _b - 12)
        )
        _3d_css = f"""
@keyframes _ara_grad {{
  0%   {{ background-position: 0% 50%; }}
  50%  {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}
@keyframes _ara_float {{
  0%, 100% {{ transform: translateY(0px) scale(1); }}
  50%       {{ transform: translateY(-5px) scale(1.01); }}
}}
@keyframes _ara_fadein {{
  from {{ opacity:0; transform: translateY(14px); }}
  to   {{ opacity:1; transform: translateY(0); }}
}}
@keyframes _ara_glow {{
  0%, 100% {{ box-shadow: 0 8px 28px rgba(30,80,180,0.18), 0 2px 8px rgba(0,0,0,0.10); }}
  50%       {{ box-shadow: 0 14px 40px rgba(30,80,180,0.30), 0 4px 16px rgba(0,0,0,0.14); }}
}}

[data-testid='stAppViewContainer'], [data-testid='stMain'], .main {{
  background: linear-gradient(-45deg, {_bg}, {_bg2}, {_bg3}, {_bg4}) !important;
  background-size: 400% 400% !important;
  animation: _ara_grad 14s ease infinite !important;
}}

[data-testid='stMetricValue'], [data-testid='stMetricLabel'],
[data-testid='stMetricDelta'] {{
  transition: color 0.3s ease !important;
}}

[data-testid='metric-container'] {{
  animation: _ara_float 5s ease-in-out infinite, _ara_fadein 0.6s ease both;
  border-radius: 18px !important;
  background: rgba(255,255,255,0.18) !important;
  backdrop-filter: blur(12px) saturate(1.4) !important;
  -webkit-backdrop-filter: blur(12px) saturate(1.4) !important;
  border: 1px solid rgba(255,255,255,0.35) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.13), inset 0 1px 0 rgba(255,255,255,0.5) !important;
  padding: 1rem 1.1rem !important;
  transition: transform 0.35s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.35s ease !important;
}}
[data-testid='metric-container']:hover {{
  transform: translateY(-9px) rotateX(4deg) !important;
  box-shadow: 0 22px 50px rgba(0,0,0,0.22), 0 4px 16px rgba(30,80,180,0.18),
              inset 0 1px 0 rgba(255,255,255,0.5) !important;
  animation-play-state: paused !important;
}}

[data-testid='stPlotlyChart'] > div {{
  border-radius: 18px !important;
  overflow: hidden !important;
  box-shadow: 0 12px 38px rgba(0,0,0,0.15), 0 3px 10px rgba(0,0,0,0.08) !important;
  transition: transform 0.35s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.35s ease !important;
  animation: _ara_fadein 0.7s ease both;
}}
[data-testid='stPlotlyChart'] > div:hover {{
  transform: translateY(-5px) !important;
  box-shadow: 0 24px 56px rgba(0,0,0,0.22), 0 6px 18px rgba(30,80,180,0.14) !important;
}}

.stButton > button {{
  transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.25s ease !important;
  box-shadow: 0 4px 14px rgba(0,0,0,0.15) !important;
  border-radius: 10px !important;
}}
.stButton > button:hover {{
  transform: translateY(-4px) scale(1.04) !important;
  box-shadow: 0 10px 28px rgba(0,0,0,0.22) !important;
}}

[data-testid='stSidebar'] > div:first-child {{
  background: linear-gradient(170deg,rgba(16,45,95,0.97),rgba(9,22,50,0.99)) !important;
  backdrop-filter: blur(20px) !important;
  box-shadow: 4px 0 36px rgba(0,0,0,0.35) !important;
}}

[data-testid='stTab'] {{
  transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.25s ease !important;
  border-radius: 8px 8px 0 0 !important;
}}
[data-testid='stTab']:hover {{
  transform: translateY(-3px) !important;
  box-shadow: 0 -4px 16px rgba(30,80,180,0.2) !important;
}}

[data-testid='stVerticalBlock'] > div > div > div {{
  animation: _ara_fadein 0.5s ease both;
}}

[data-testid='stDataFrame'] {{
  border-radius: 14px !important;
  overflow: hidden !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.12) !important;
  animation: _ara_fadein 0.6s ease both;
}}

h1, h2, h3, h4 {{
  color: {_text_color} !important;
  letter-spacing: -0.02em !important;
  animation: _ara_fadein 0.5s ease both;
}}
"""
        st.markdown(f"<style>{_base_css}{_3d_css}{_TAB_RIGHT_CSS}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{_base_css}{_TAB_RIGHT_CSS}</style>", unsafe_allow_html=True)

    # ── Carga de los 2 archivos Excel ─────────────────────────────────
    with st.expander(
        " Cargar archivos Excel",
        expanded=st.session_state.data is None,
    ):
        col_up1, col_up2, col_up3 = st.columns(3)
        with col_up1:
            st.markdown("**Archivo 1 — Cartera**")
            st.caption("Columna de Número de Dama + Año/Campaña de saldo")
            file_cartera = st.file_uploader(
                "Cartera", type=["xlsx", "xls"], label_visibility="collapsed", key="up_cartera"
            )
        with col_up2:
            st.markdown("**Archivo 2 — Saldos Actualizados**")
            st.caption("Columna de Número de Dama + Año Proceso + Campaña Proceso")
            file_saldos = st.file_uploader(
                "Saldos", type=["xlsx", "xls"], label_visibility="collapsed", key="up_saldos"
            )
        with col_up3:
            st.markdown("**Archivo 3 — Moras** *(opcional)*")
            st.caption("Columna NoDama para cruzar con damas pendientes")
            file_moras = st.file_uploader(
                "Moras", type=["xlsx", "xls"], label_visibility="collapsed", key="up_moras"
            )
            if file_moras:
                try:
                    st.session_state.df_moras = read_excel_safe(file_moras)
                    st.success(f" Moras cargadas: {len(st.session_state.df_moras):,} registros")
                except Exception as e:
                    st.error(f" Error al leer moras: {e}")


        if file_cartera and file_saldos:
            new_names = (file_cartera.name, file_saldos.name)
            # Solo re-leer si los archivos cambiaron realmente
            if new_names != st.session_state.file_names:
                try:
                    st.session_state.df_cartera = read_excel_safe(file_cartera)
                    st.session_state.df_saldos  = read_excel_safe(file_saldos)
                    st.session_state.data        = None
                    st.session_state.mapping     = None
                    st.session_state.file_names  = new_names
                except Exception as e:
                    st.error(f" No se pudo leer el archivo: {e}")
        elif file_cartera or file_saldos:
            st.info(" Sube los **dos** archivos para continuar.")

    # ── Mapeo de columnas ─────────────────────────────────────────────
    if (st.session_state.df_cartera is not None
            and st.session_state.df_saldos is not None
            and st.session_state.data is None):

        st.divider()
        mapping = render_column_mapper(
            st.session_state.df_cartera,
            st.session_state.df_saldos,
            st.session_state.df_moras,
        )
        if mapping:
            with st.spinner("Cruzando Cartera × Saldos Actualizados…"):
                try:
                    st.session_state.data = load_and_clean_data(
                        st.session_state.df_cartera,
                        st.session_state.df_saldos,
                        mapping,
                    )
                    st.session_state.mapping = mapping
                    # Free the raw uploaded DataFrames — no longer needed after merge
                    st.session_state.df_cartera = None
                    st.session_state.df_saldos = None
                    n = len(st.session_state.data["merged"])
                    st.success(f" Cruce completado — **{n:,}** registros consolidados.")
                    st.rerun()
                except Exception as e:
                    st.error(f" Error al cruzar datos: {e}")
        # no return — fall through to tabs so Indicadores stays accessible

    # ── Tabs principales (siempre visibles) ───────────────────────────
    arabela_tab, indicadores_tab, interno_tab = st.tabs([
        "🌸 Arabela", "📊 Indicadores", "🏢 Interno"
    ])

    with arabela_tab:
        # Mapeo pendiente
        if (st.session_state.df_cartera is not None
                and st.session_state.df_saldos is not None
                and st.session_state.data is None):
            st.info("Completa el mapeo de columnas para ver el dashboard.")

        elif st.session_state.data is None:
            render_welcome()

        else:
            # ── Filtros ───────────────────────────────────────────────
            filtered_merged = apply_filters(st.session_state.data["merged"], filters)
            filtered_data   = {**st.session_state.data, "merged": filtered_merged}
            metrics         = calculate_metrics(filtered_data)

            campañas_sel = filters.get("campañas", [])
            estado_sel   = filters.get("estado", "Todos")
            partes = []
            if campañas_sel:
                partes.append(f"Campaña: **{', '.join(campañas_sel)}**")
            if estado_sel != "Todos":
                partes.append(f"Estado: **{estado_sel}**")
            if partes:
                st.info(" Filtros activos — " + " · ".join(partes))

            sub1, sub2, sub3, sub4 = st.tabs([
                " Resumen General",
                " Temporalidad",
                "Operaciones y Territorio",
                " Tracking Completo",
            ])
            with sub1:
                tab_resumen(metrics)
            with sub2:
                tab_temporalidad(metrics)
            with sub3:
                tab_flujo(metrics)
            with sub4:
                tab_tracking(st.session_state.df_moras, metrics)

    with indicadores_tab:
        _render_indicadores_standalone()

    with interno_tab:
        try:
            _render_interno_tab()
        except Exception as _e:
            st.error(f"Error en Interno: {_e}")
            import traceback
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
