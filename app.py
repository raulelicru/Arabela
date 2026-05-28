"""
Dashboard Profesional de Gestión de Cartera Financiera
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
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

def render_column_mapper(df_cartera: pd.DataFrame, df_saldos: pd.DataFrame) -> dict | None:
    cols_c = list(df_cartera.columns)
    cols_s = list(df_saldos.columns)

    st.markdown(
        f"<div class='card' style='border-left:4px solid {COLORS['warning']};'>"
        "<b> Mapeo de columnas</b> — Selecciona las columnas de cada archivo.</div>",
        unsafe_allow_html=True,
    )

    # ── Llave de cruce (misma estructura en ambos archivos) ───────────
    st.markdown("#####  Llave de cruce — *igual en ambos archivos*")
    st.caption("Se concatena **Número de Dama + Año Campaña Saldo** en los dos Excel para unirlos.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("** Cartera**")
        c_dama = st.selectbox(
            "Número de Dama", cols_c,
            index=_best_guess(cols_c, ["dama", "num", "nro", "id"]),
            key="map_c_dama",
        )
        c_anio = st.selectbox(
            "Año Campaña Saldo", cols_c,
            index=_best_guess(cols_c, ["anio", "año", "campaña", "saldo"]),
            key="map_c_anio",
        )

    with col_b:
        st.markdown("** Saldos Actualizados**")
        s_dama = st.selectbox(
            "Número de Dama", cols_s,
            index=_best_guess(cols_s, ["dama", "num", "nro", "id"]),
            key="map_s_dama",
        )
        s_anio = st.selectbox(
            "Año Campaña Saldo", cols_s,
            index=_best_guess(cols_s, ["anio", "año", "campaña", "saldo"]),
            key="map_s_anio",
        )

    st.divider()

    # ── Columna de saldo (determina quién pagó y cuánto debe) ─────────
    st.markdown("#####  Columna de saldo en Saldos Actualizados")
    col_c, col_d = st.columns(2)
    with col_c:
        s_saldo = st.selectbox(
            "Columna con el saldo / deuda ", cols_s,
            index=_best_guess(cols_s, ["saldocampaña", "saldocampana", "saldo", "deuda", "valor", "monto", "pendiente"]),
            key="map_s_saldo",
        )
    with col_d:
        st.markdown("")
        st.info("**Saldo ≥ 51** →  Pagado\n\n**Saldo < 51** →  Pendiente (aún debe)")

    st.divider()

    # ── Monto original en Cartera (opcional) ─────────────────────────
    st.markdown("#####  Monto original en Cartera *(opcional)*")
    c_monto = st.selectbox(
        "Columna con la deuda original de Cartera",
        ["(ninguna)"] + cols_c,
        index=_best_guess(["(ninguna)"] + cols_c, ["saldocampaña", "saldocampana", "valor", "monto", "deuda", "total"]),
        key="map_c_monto",
        help="Si existe, permite calcular Total Cartera y Total Cobrado.",
    )

    st.divider()

    # ── Fechas en Cartera (para análisis temporal real) ───────────────
    st.markdown("#####  Fechas en Cartera *(opcional — activan análisis temporal)*")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        c_fecha_inicio = st.selectbox(
            "Columna Fecha de Inicio",
            ["(ninguna)"] + cols_c,
            index=_best_guess(["(ninguna)"] + cols_c, ["inicio", "fecha_i", "start", "vigencia", "fecha"]),
            key="map_c_fecha_inicio",
        )
    with col_f2:
        c_fecha_fin = st.selectbox(
            "Columna Fecha Final",
            ["(ninguna)"] + cols_c,
            index=_best_guess(["(ninguna)"] + cols_c, ["fin", "final", "venc", "end", "termino"]),
            key="map_c_fecha_fin",
        )

    st.markdown("")
    if st.button(" Confirmar y procesar", type="primary", use_container_width=True):
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
    valor_col = data.get("valor_col") or _find_col(df, ["saldocampaña", "saldocampana", "valor", "monto", "deuda", "total"])

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

    df["x"] = np.arange(len(df))
    model    = LinearRegression()
    model.fit(df[["x"]], df["valor"])

    future_x = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    future_y = model.predict(future_x)

    # Etiquetas de campaña proyectadas (siguientes números después del último)
    last_label = str(df["fecha"].iloc[-1])
    try:
        last_num = int(last_label)
        future_labels = [str(last_num + i + 1) for i in range(horizon)]
    except ValueError:
        future_labels = [f"Proy.{i+1}" for i in range(horizon)]

    residuals = df["valor"].values - model.predict(df[["x"]])
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
    camp_labels = [_fmt_camp(c) for c in camps]
    pagado    = grp[grp["Estado_Pago"] == "Pagado"].set_index(camp_col)[valor_col].reindex(camps, fill_value=0)
    pendiente = grp[grp["Estado_Pago"] == "Pendiente"].set_index(camp_col)[valor_col].reindex(camps, fill_value=0)
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
    camps = sorted(grp[camp_col].unique())
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
    periods   = sorted(set(cobrado.index) | set(pendiente.index))
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
            pct[camp_col] = pct[camp_col].astype(str)
            pct = pct.sort_values(camp_col)
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
        anios    = sorted(pivot.index.tolist())
        x_labels = sorted(pivot.columns.tolist())
        z        = [[pivot.loc[a, p] if p in pivot.columns else 0 for p in x_labels] for a in anios]
        hover    = "Año: %{y} · Período: %{x}<br>% Cobrado: %{z:.1f}%<extra></extra>"
        title    = "Mapa de Calor · % Cobrado por Año y Período de Campaña"
        ylab, xlab = "Año", "Período"

    text_z = [[f"{v:.1f}%" for v in row] for row in z]
    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=anios,
        text=text_z, texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        colorscale=[[0, COLORS["danger"]], [0.5, COLORS["warning"]], [1, COLORS["success"]]],
        zmin=0, zmax=100,
        colorbar=dict(title="% Cobrado", ticksuffix="%"),
        hovertemplate=hover,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text=title,
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title=xlab, yaxis_title=ylab,
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
    cobrado_camp[camp_col] = cobrado_camp[camp_col].astype(str)
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
        text=[f"  {pct:.1f}%"], textposition="outside",
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
                      line=dict(color="#000000", width=2, dash="dash"),
                      row=1, col=1)
        fig.add_annotation(x=meta, y=0.55, text=f"Meta {meta}%",
                           showarrow=False, font=dict(size=10, color=COLORS["muted"]),
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
    dist = pendientes.groupby(camp_col).size().sort_index()

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
        title_text=f"Damas pendientes por campaña ({dist.values.sum():,} en total)",
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
    pct    = pct.sort_index()

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
    chart_card(
        "En que meses se cobra mejor (mapa de calor)" + (" por mes" if usando_fechas else ""),
        plot_heatmap(metrics["df"], metrics["valor_col"], fi),
        key="heatmap", height_normal=340, height_expanded=500,
    )


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
    # Waterfall
    chart_card("Como va bajando la deuda campaña a campaña",
               plot_waterfall(metrics["df"], metrics["valor_col"]),
               key="waterfall", height_normal=420, height_expanded=600)
    st.divider()

    # ── KPIs: cambio de temporalidad ─────────────────────────────────
    camp_col = _find_col(metrics["df"], ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if camp_col:
        pend_df    = metrics["df"][metrics["df"]["Estado_Pago"] == "Pendiente"]
        total_pend = len(pend_df)
        n_camps    = pend_df[camp_col].astype(str).nunique()
        c1, c2     = st.columns(2)
        with c1: st.metric(" Damas que cambiaron de temporalidad", f"{total_pend:,}")
        with c2: st.metric(" Temporalidades con pendientes",       f"{n_camps}")
        st.markdown("<br>", unsafe_allow_html=True)

    chart_card("Cuantas damas deben en cada campaña",
               plot_damas_por_temporalidad(metrics["df"]),
               key="cambio_temp", height_normal=400, height_expanded=580)
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
            st.markdown("### Que ruta tiene mas moras")

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
                chart_card("Cuantas damas en mora tiene cada ruta", fig_ruta, key="ruta_moras", height_normal=420)

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

                # Tabla resumen
                st.markdown("<br>", unsafe_allow_html=True)
                tabla_ruta = ruta_dist.rename(columns={
                    ruta_col: "Ruta", "Damas": "Damas en Mora",
                    "Monto": "Monto en Mora", "% del total": "% del Total"
                })
                if "Monto en Mora" in tabla_ruta.columns:
                    tabla_ruta["Monto en Mora"] = tabla_ruta["Monto en Mora"].apply(lambda x: f"${x:,.2f}")
                st.dataframe(tabla_ruta, use_container_width=True, hide_index=True)

                # ── Desglose de campañas por ruta ──────────────────────
                camp_col_ruta = _find_col(df_cruce, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
                if camp_col_ruta:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### Composicion de campañas dentro de cada ruta")

                    ruta_camp = (
                        df_cruce.groupby([ruta_col, camp_col_ruta])
                        .size()
                        .reset_index(name="Damas")
                    )
                    ruta_camp["Campaña"] = ruta_camp[camp_col_ruta].astype(str).str.strip().apply(_fmt_camp)
                    total_por_ruta = ruta_camp.groupby(ruta_col)["Damas"].transform("sum")
                    ruta_camp["% en ruta"] = (ruta_camp["Damas"] / total_por_ruta * 100).round(1)

                    # Orden de rutas: mayor número de moras primero
                    orden_rutas = ruta_dist[ruta_col].tolist()
                    camps_sorted = sorted(ruta_camp["Campaña"].unique())
                    pivot_pct = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="% en ruta", aggfunc="sum", fill_value=0)
                        .reindex(orden_rutas, fill_value=0)
                    )
                    pivot_cnt = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="Damas", aggfunc="sum", fill_value=0)
                        .reindex(orden_rutas, fill_value=0)
                    )

                    # Pivot: filas = ruta (orden: más moras primero), columnas = campaña
                    pivot_heat = (
                        ruta_camp.pivot_table(index=ruta_col, columns="Campaña",
                                              values="Damas", aggfunc="sum", fill_value=0)
                        .reindex(orden_rutas, fill_value=0)
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
                    chart_card("Que porcentaje de cada campaña corresponde a cada ruta",
                               fig_heat_pct, key="heat_pct", height_normal=400)

                    # Selector: detalle de una campaña específica
                    st.markdown("<br>", unsafe_allow_html=True)
                    camp_sel = st.selectbox("Ver detalle de una campaña:",
                                            camps_sorted, key="sel_camp_ruta")
                    detalle_camp = (
                        ruta_camp[ruta_camp["Campaña"] == camp_sel]
                        [[ruta_col, "Damas", "% en ruta"]]
                        .sort_values("Damas", ascending=False)
                        .rename(columns={ruta_col: "Ruta", "% en ruta": "% de la campaña"})
                    )
                    total_camp_sel = int(detalle_camp["Damas"].sum())
                    st.caption(f"{camp_sel} — {total_camp_sel:,} damas en mora en total")
                    st.dataframe(detalle_camp, use_container_width=True, hide_index=True)

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

def tab_tracking(df_moras: pd.DataFrame | None):
    st.markdown(
        "<div class='kpi-banner'><h1>Tracking Completo de Cartera</h1>"
        "<p>Seguimiento de pendientes de pago a través de las 10 campañas operativas</p></div>",
        unsafe_allow_html=True,
    )

    if df_moras is None:
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
    if n_inac > 0:
        st.info(f"**{n_inac:,} registros** reclasificados como **Inactiva** (IdSituacion = 0)")

    k1, k2, k3, k4, k5 = st.columns(5)
    ret_rates = [
        (sdf.loc[i, "total"] - sdf.loc[i, "nuevas"]) / sdf.loc[i - 1, "total"] * 100
        for i in sdf.index if i > 0 and sdf.loc[i - 1, "total"] > 0
    ]
    avg_ret = sum(ret_rates) / len(ret_rates) if ret_rates else 0
    with k1: st.metric("Pool de Pendientes", f"{pool_size:,}")
    with k2: st.metric("Total campañas", f"{len(camps_n)}")
    with k3: st.metric("Retención promedio", f"{avg_ret:.1f}%")
    with k4:
        fuga_camp = sdf.loc[sdf["fugadas"].idxmax(), "camp_label"] if not sdf.empty else "—"
        fuga_val  = sdf["fugadas"].max() if not sdf.empty else 0
        st.metric("Mayor fuga", f"{fuga_camp} ({fuga_val:,})")
    with k5:
        total_exits = len(exits_df) if not exits_df.empty else 0
        st.metric("Salidas permanentes", f"{total_exits:,}",
                  delta=f"{total_exits/pool_size*100:.1f}% del pool" if pool_size else None,
                  delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
        "Resumen Ejecutivo",
        "Por Campaña",
        "Por Mora",
        "Salidas",
        "Transiciones",
        "Flujo Inactivas",
    ])

    # ══════════════════════════════════════════
    # SUBTAB 1 — Resumen Ejecutivo
    # ══════════════════════════════════════════
    with subtab1:
        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica: Composición (Inactiva + M1/M2/M3) por campaña
        fig_comp = go.Figure()
        for mora in MORA_LEVELS:
            fig_comp.add_trace(go.Bar(
                x=sdf["camp_label"], y=sdf[f"{mora}_total"],
                name=mora, marker_color=MORA_COLORS[mora],
                hovertemplate=f"<b>%{{x}}</b><br>{mora}: %{{y:,}}<extra></extra>",
            ))
        fig_comp.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title_text="Damas por estado en cada campaña",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        )
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            chart_card("Composición por estado", fig_comp, key="trk_comp", height_normal=380)

        # Gráfica: Nuevas vs Fugadas (barras) + % Fuga (línea eje secundario)
        pct_fuga = sdf.apply(
            lambda r: round(r["fugadas"] / r["total"] * 100, 1) if r["total"] else 0, axis=1
        )
        fig_cohort = go.Figure()
        fig_cohort.add_trace(go.Bar(
            x=sdf["camp_label"], y=sdf["nuevas"],
            name="Cuentas nuevas", marker_color=COLORS["success"],
            text=sdf["nuevas"], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Cuentas nuevas: %{y:,}<extra></extra>",
        ))
        fig_cohort.add_trace(go.Bar(
            x=sdf["camp_label"], y=sdf["fugadas"],
            name="Se van (fugadas)", marker_color=COLORS["danger"],
            text=sdf["fugadas"], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Se van: %{y:,}<extra></extra>",
        ))
        fig_cohort.add_trace(go.Scatter(
            x=sdf["camp_label"], y=pct_fuga,
            name="% que se va", mode="lines+markers",
            line=dict(color="#6366F1", width=2, dash="dot"), marker=dict(size=7),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>% que se va: %{y:.1f}%<extra></extra>",
        ))
        fig_cohort.update_layout(
            **PLOTLY_LAYOUT,
            barmode="group",
            title_text="Cuentas que entran vs cuentas que se van por campaña",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", **_AXIS_DEFAULTS),
            yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            yaxis2=dict(title="% que se va", overlaying="y", side="right",
                        ticksuffix="%", range=[0, 120],
                        showgrid=False, **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
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

        # Mini bar chart para la campaña seleccionada
        st.markdown("<br>", unsafe_allow_html=True)
        fig_bar = go.Figure()
        for mora in MORA_LEVELS:
            m_tot = int(r.get(f"{mora}_total", 0))
            fig_bar.add_trace(go.Bar(
                name=mora, x=["Nuevas", "De Anterior", "Persistentes", "Fugadas"],
                y=[int(r.get(f"{mora}_nuevas", 0)), int(r.get(f"{mora}_de_anterior", 0)),
                   int(r.get(f"{mora}_persistentes", 0)), int(r.get(f"{mora}_fugadas", 0))],
                marker_color=MORA_COLORS[mora],
                hovertemplate=f"{mora}: %{{y:,}}<extra></extra>",
            ))
        fig_bar.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title_text=f"Resumen de {sel_camp}",
            title_font=dict(size=12, color=COLORS["primary"]),
            xaxis=dict(**_AXIS_DEFAULTS), yaxis=dict(title="Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
            height=340,
        )
        st.plotly_chart(fig_bar, use_container_width=True, key=f"trk_cbar_{sel_camp}")

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
#  MAIN
# ─────────────────────────────────────────────

def main():
    # ── Inicializar session_state ─────────────────────────────────────
    for key, default in [
        ("data", None), ("df_cartera", None), ("df_saldos", None),
        ("mapping", None), ("file_names", (None, None)), ("df_moras", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    filters = render_sidebar(st.session_state.data)

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
        return  # esperar confirmación del mapeo antes de mostrar dashboard

    # ── Sin datos ─────────────────────────────────────────────────────
    if st.session_state.data is None:
        render_welcome()
        return

    # ── Filtros ───────────────────────────────────────────────────────
    filtered_merged = apply_filters(st.session_state.data["merged"], filters)
    filtered_data   = {**st.session_state.data, "merged": filtered_merged}
    metrics         = calculate_metrics(filtered_data)

    # Banner de filtros activos
    campañas_sel = filters.get("campañas", [])
    estado_sel   = filters.get("estado", "Todos")
    partes = []
    if campañas_sel:
        partes.append(f"Campaña: **{', '.join(campañas_sel)}**")
    if estado_sel != "Todos":
        partes.append(f"Estado: **{estado_sel}**")
    if partes:
        st.info(" Filtros activos — " + " · ".join(partes))

    # ── Tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        " Resumen General",
        " Temporalidad",
        "Operaciones y Territorio",
        " Tracking Completo",
    ])
    with tab1:
        tab_resumen(metrics)
    with tab2:
        tab_temporalidad(metrics)
    with tab3:
        tab_flujo(metrics)
    with tab4:
        tab_tracking(st.session_state.df_moras)


if __name__ == "__main__":
    main()
