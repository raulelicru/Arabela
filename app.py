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
    margin=dict(l=40, r=20, t=50, b=40),
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
        title_text="¿Cuántas damas ya pagaron?",
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
        title_text="Monto Cobrado vs Pendiente por Campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="group",
        xaxis_title="Campaña", yaxis_title="Monto ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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
        title_text="¿Qué % de la cartera se recuperó por campaña?",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="stack",
        xaxis_title="Campaña", yaxis_title="% de Damas",
        yaxis_range=[0, 110],
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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
        title_text="Embudo de Cobranza · ¿Dónde está la cartera?",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=380,
    )
    fig.update_layout(hovermode="y")
    return fig


def _fmt_camp(code: str) -> str:
    """202608 → 'Camp. 08'  (solo los últimos 2 dígitos son el número de campaña)."""
    c = str(code).strip()
    if len(c) == 6 and c.isdigit():
        return f"Camp. {c[4:]}"
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
        title_text="Tendencia de Recuperación" + (" por Mes" if fecha_col else " por Campaña"),
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title=x_title, yaxis_title="Monto ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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
        title_text="Evolución de Montos: Cobrado y Pendiente" + (" por Mes" if fecha_col else " por Campaña"),
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title=x_title, yaxis_title="Monto Total ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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
                              title_text="% Cobrado por Campaña",
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
        title_text="Cascada de Recuperación · Cómo se reduce la deuda",
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
    metas = [50, 60]
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
        title_text="Cumplimiento Actual vs Metas de Cobranza",
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
        title_text=f"Top {n} damas con más deuda pendiente",
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
        title_text="Proyección de saldo pendiente para próximas campañas",
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
        title_text=f"Damas pendientes por temporalidad — {dist.values.sum():,} damas en total",
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
        title_text="¿Cuánto cobramos en cada campaña? (comparación vs campaña anterior)",
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
    dff = df.copy()
    # Filtro por Año Campaña Saldo (multiselect)
    camp_col = filters.get("camp_col")
    seleccion = filters.get("campañas", [])
    if camp_col and seleccion and camp_col in dff.columns:
        dff = dff[dff[camp_col].astype(str).isin(seleccion)]
    # Filtro por estado
    if filters.get("estado") and filters["estado"] != "Todos":
        dff = dff[dff["Estado_Pago"] == filters["estado"]]
    return dff


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
    chart_card("De cada 10 damas, cuantas pagaron",
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
        nodama_col  = _get_merged_nodama_col(metrics["df"])
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
#  TAB MORAS
# ─────────────────────────────────────────────

def _get_nodama_col(df: pd.DataFrame) -> str | None:
    """Encuentra la columna de número de dama en el archivo de moras."""
    return _find_col(df, ["nodama", "no dama", "númdama", "numdama", "número de dama", "num_dama"])


def _get_merged_nodama_col(df: pd.DataFrame) -> str | None:
    """Encuentra la columna de número de dama en el merged."""
    for c in ["Número de Dama_cartera", "Número de Dama", "NumDama_cartera", "NumDama"]:
        if c in df.columns:
            return c
    return _find_col(df, ["nodama", "numdama", "número de dama"])


def _camp_to_seq(code) -> int | None:
    """202526 → secuencia numérica (año*26 + campaña) para calcular diferencias entre campañas."""
    c = str(code).strip()
    if len(c) == 6 and c.isdigit():
        return int(c[:4]) * 26 + int(c[4:])
    return None



def _clasificar_mora(diff: int) -> str:
    if diff < 0:
        return "Sin mora"
    elif diff <= 1:   # misma campaña o 1 atrás → Mora 1
        return "Mora 1"
    elif diff == 2:
        return "Mora 2"
    else:
        return "Mora 3"


def tab_moras(metrics: dict, df_moras: pd.DataFrame | None):
    st.markdown(
        "<div class='kpi-banner'><h1> Análisis de Moras</h1>"
        "<p>Damas con deuda pendiente que aparecen en el archivo de moras</p></div>",
        unsafe_allow_html=True,
    )

    if df_moras is None:
        st.info(" Sube el archivo de moras en el panel de carga de archivos para ver este análisis.")
        return

    nodama_mora  = _get_nodama_col(df_moras)
    nodama_merge = _get_merged_nodama_col(metrics["df"])

    if not nodama_mora:
        st.error(" No se encontró la columna NoDama en el archivo de moras. Verifica el archivo.")
        return
    if not nodama_merge:
        st.error(" No se encontró la columna de número de dama en los datos principales.")
        return

    # Solo pendientes
    pendientes    = metrics["df"][metrics["df"]["Estado_Pago"] == "Pendiente"].copy()
    total_pendientes = len(pendientes)
    valor_col     = metrics.get("valor_col")

    # Normalizar IDs para el cruce
    pendientes_ids = set(pendientes[nodama_merge].astype(str).str.strip())
    moras_ids      = set(df_moras[nodama_mora].astype(str).str.strip())
    total_moras    = len(df_moras)

    # Coincidencias: pendientes que están en moras
    coincidencias_ids   = pendientes_ids & moras_ids
    n_coincidencias     = len(coincidencias_ids)
    pct_pendientes      = (n_coincidencias / total_pendientes * 100) if total_pendientes > 0 else 0
    pct_moras           = (n_coincidencias / total_moras * 100)      if total_moras > 0 else 0

    # Monto en mora
    moras_en_pendientes = pendientes[
        pendientes[nodama_merge].astype(str).str.strip().isin(coincidencias_ids)
    ].copy()
    monto_mora = (
        pd.to_numeric(moras_en_pendientes[valor_col], errors="coerce").sum()
        if valor_col else 0
    )
    monto_total_pend = (
        pd.to_numeric(pendientes[valor_col], errors="coerce").sum()
        if valor_col else 0
    )
    pct_monto = (monto_mora / monto_total_pend * 100) if monto_total_pend > 0 else 0

    # ── KPIs fila 1: conteos ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(" Total en archivo de moras", f"{total_moras:,}")
    with c2:
        st.metric(" Pendientes que son moras", f"{n_coincidencias:,}")
    with c3:
        st.metric("% de pendientes en mora", f"{pct_pendientes:.1f}%")
    with c4:
        st.metric("% del archivo de moras coincide", f"{pct_moras:.1f}%")

    # ── KPIs fila 2: dinero ─────────────────────────────────────────
    if valor_col:
        st.markdown("<br>", unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric(" Monto total pendiente", fmt_currency(monto_total_pend))
        with d2:
            st.metric(" Monto en mora", fmt_currency(monto_mora))
        with d3:
            st.metric("% del monto pendiente en mora", f"{pct_monto:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Donas: visión general ───────────────────────────────────────
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        fig_dona_damas = go.Figure(go.Pie(
            labels=["En mora", "Sin mora"],
            values=[n_coincidencias, total_pendientes - n_coincidencias],
            hole=0.6,
            marker_colors=[COLORS["danger"], COLORS["accent"]],
            textinfo="percent",
            textfont=dict(size=14, color=COLORS["text"]),
            hovertemplate="<b>%{label}</b><br>Damas: %{value:,}<br>%{percent}<extra></extra>",
        ))
        fig_dona_damas.update_layout(
            **PLOTLY_LAYOUT,
            title_text="Damas pendientes en mora vs sin mora",
            title_font=dict(size=13, color=COLORS["primary"]),
            annotations=[dict(
                text=f"<b>{pct_pendientes:.1f}%</b><br>en mora",
                x=0.5, y=0.5, font_size=16, font_color=COLORS["danger"],
                showarrow=False,
            )],
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        )
        chart_card("Cuantas damas están en mora", fig_dona_damas, key="dona_damas", height_normal=320, height_expanded=480)

    with col_d2:
        if valor_col:
            fig_dona_monto = go.Figure(go.Pie(
                labels=["Monto en mora", "Sin mora"],
                values=[monto_mora, monto_total_pend - monto_mora],
                hole=0.6,
                marker_colors=[COLORS["danger"], COLORS["success"]],
                textinfo="percent",
                textfont=dict(size=14, color=COLORS["text"]),
                hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
            ))
            fig_dona_monto.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Monto pendiente en mora vs sin mora",
                title_font=dict(size=13, color=COLORS["primary"]),
                annotations=[dict(
                    text=f"<b>{pct_monto:.1f}%</b><br>en mora",
                    x=0.5, y=0.5, font_size=16, font_color=COLORS["danger"],
                    showarrow=False,
                )],
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            )
            chart_card("Cuanto dinero está en mora", fig_dona_monto, key="dona_monto", height_normal=320, height_expanded=480)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sección de clasificación por nivel de mora ─────────────────────
    mora_col_moras  = _find_col(df_moras, ["moras", "mora", "nivel de mora", "nivel_mora", "niveldemora"])
    camp_col_moras  = _find_col(df_moras, ["campania", "campaña", "camp", "campana"])
    saldo_col_moras = _find_col(df_moras, ["saldodama", "saldo", "importe", "monto", "importenetofactura"])
    nodama_mora_key = _get_nodama_col(df_moras)

    if mora_col_moras:
        mora_map = {"mora 1": "Mora 1", "mora 2": "Mora 2", "mora 3": "Mora 3",
                    "1": "Mora 1", "2": "Mora 2", "3": "Mora 3"}
        df_m = df_moras.copy()
        df_m["_nivel"] = df_m[mora_col_moras].astype(str).str.strip().str.lower().map(mora_map)
        df_m = df_m.dropna(subset=["_nivel"])

        # Filtrar solo damas que NO pagaron (coinciden con pendientes de la cartera)
        if nodama_mora_key and coincidencias_ids:
            df_m = df_m[df_m[nodama_mora_key].astype(str).str.strip().isin(coincidencias_ids)]

        # Deduplicar: una fila por dama usando la campaña más reciente
        if nodama_mora_key and camp_col_moras:
            def _camp_n(v):
                try:
                    return int(str(v).strip().upper().replace("C", ""))
                except Exception:
                    return 0
            df_m["_camp_n"] = df_m[camp_col_moras].apply(_camp_n)
            df_m = (
                df_m.sort_values("_camp_n", ascending=False)
                .drop_duplicates(subset=[nodama_mora_key], keep="first")
            )

        mora_colors = {"Mora 1": COLORS["warning"], "Mora 2": COLORS["orange"], "Mora 3": COLORS["danger"]}

        # ── KPIs por nivel ────────────────────────────────────────────
        if saldo_col_moras:
            df_m["_saldo"] = pd.to_numeric(df_m[saldo_col_moras], errors="coerce")
            mora_dist = (
                df_m.groupby("_nivel")
                .agg(Damas=("_nivel", "count"), Monto=("_saldo", "sum"))
                .reindex(["Mora 1", "Mora 2", "Mora 3"], fill_value=0)
                .reset_index().rename(columns={"_nivel": "Nivel de Mora"})
            )
        else:
            mora_dist = (
                df_m.groupby("_nivel").size().rename("Damas")
                .reindex(["Mora 1", "Mora 2", "Mora 3"], fill_value=0)
                .reset_index().rename(columns={"_nivel": "Nivel de Mora"})
            )
            mora_dist["Monto"] = 0

        total_mora_shown = mora_dist["Damas"].sum()
        mora_dist["% del total"] = (
            (mora_dist["Damas"] / total_mora_shown * 100).round(1) if total_mora_shown > 0 else 0.0
        )

        st.markdown("---")
        st.markdown("###  Clasificación por Nivel de Mora")
        st.markdown("<br>", unsafe_allow_html=True)
        km1, km2, km3 = st.columns(3)
        for col_k, (_, row_m) in zip([km1, km2, km3], mora_dist.iterrows()):
            with col_k:
                st.metric(f"{row_m['Nivel de Mora']} — Damas", f"{int(row_m['Damas']):,}",
                          delta=f"{row_m['% del total']:.1f}% del total", delta_color="off")
                if saldo_col_moras:
                    st.metric(f"{row_m['Nivel de Mora']} — Monto", fmt_currency(row_m["Monto"]))

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Barras apiladas por campaña ───────────────────────────────
        if camp_col_moras:
            mora_camp = (
                df_m.groupby([camp_col_moras, "_nivel"]).size()
                .unstack(fill_value=0)
                .reindex(columns=["Mora 1", "Mora 2", "Mora 3"], fill_value=0)
                .reset_index()
            )
            # Ordenar C1, C2, ..., C10
            def _camp_sort_key(v):
                v2 = str(v).strip().upper().replace("C", "")
                return int(v2) if v2.isdigit() else 99
            mora_camp = mora_camp.sort_values(camp_col_moras, key=lambda s: s.map(_camp_sort_key))

            fig_mora_camp = go.Figure()
            for nivel, color in mora_colors.items():
                if nivel in mora_camp.columns:
                    fig_mora_camp.add_trace(go.Bar(
                        x=mora_camp[camp_col_moras], y=mora_camp[nivel],
                        name=nivel, marker_color=color,
                        hovertemplate=f"<b>%{{x}}</b><br>{nivel}: %{{y:,}} damas<extra></extra>",
                    ))
            fig_mora_camp.update_layout(
                **PLOTLY_LAYOUT, barmode="stack",
                title_text="Mora 1 / 2 / 3 por campaña — Número de registros",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(type="category", **_AXIS_DEFAULTS),
                yaxis=dict(title="Número de damas", **_AXIS_DEFAULTS),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            chart_card("Tipo de mora por campaña (numero de damas)", fig_mora_camp,
                       key="mora_niveles_camp", height_normal=420, height_expanded=600)

            if saldo_col_moras:
                st.markdown("<br>", unsafe_allow_html=True)
                mora_camp_m = (
                    df_m.groupby([camp_col_moras, "_nivel"])["_saldo"].sum()
                    .unstack(fill_value=0)
                    .reindex(columns=["Mora 1", "Mora 2", "Mora 3"], fill_value=0)
                    .reset_index()
                )
                mora_camp_m = mora_camp_m.sort_values(camp_col_moras, key=lambda s: s.map(_camp_sort_key))
                fig_mora_monto = go.Figure()
                for nivel, color in mora_colors.items():
                    if nivel in mora_camp_m.columns:
                        fig_mora_monto.add_trace(go.Bar(
                            x=mora_camp_m[camp_col_moras], y=mora_camp_m[nivel],
                            name=nivel, marker_color=color,
                            hovertemplate=f"<b>%{{x}}</b><br>{nivel}: $%{{y:,.0f}}<extra></extra>",
                        ))
                fig_mora_monto.update_layout(
                    **PLOTLY_LAYOUT, barmode="stack",
                    title_text="Mora 1 / 2 / 3 por campaña — Monto en pesos",
                    title_font=dict(size=13, color=COLORS["primary"]),
                    xaxis=dict(type="category", **_AXIS_DEFAULTS),
                    yaxis=dict(title="Monto ($)", **_AXIS_DEFAULTS),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                chart_card("Tipo de mora por campaña (dinero)", fig_mora_monto,
                           key="mora_monto_camp", height_normal=420, height_expanded=600)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Donas: proporción de damas y monto ───────────────────────
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            fig_dona_mora = go.Figure(go.Pie(
                labels=mora_dist["Nivel de Mora"], values=mora_dist["Damas"],
                hole=0.6,
                marker_colors=[mora_colors.get(m, COLORS["muted"]) for m in mora_dist["Nivel de Mora"]],
                textinfo="label+percent", textfont=dict(size=13, color=COLORS["text"]),
                hovertemplate="<b>%{label}</b><br>Damas: %{value:,}<br>%{percent}<extra></extra>",
            ))
            fig_dona_mora.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Proporción de damas Mora 1/2/3",
                title_font=dict(size=13, color=COLORS["primary"]),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            )
            chart_card("Como se reparte la mora entre los 3 niveles", fig_dona_mora,
                       key="dona_mora_damas", height_normal=340, height_expanded=480)
        with dcol2:
            if saldo_col_moras:
                fig_dona_monto_mora = go.Figure(go.Pie(
                    labels=mora_dist["Nivel de Mora"], values=mora_dist["Monto"],
                    hole=0.6,
                    marker_colors=[mora_colors.get(m, COLORS["muted"]) for m in mora_dist["Nivel de Mora"]],
                    textinfo="label+percent", textfont=dict(size=13, color=COLORS["text"]),
                    hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
                ))
                fig_dona_monto_mora.update_layout(
                    **PLOTLY_LAYOUT,
                    title_text="Proporción del monto Mora 1/2/3",
                    title_font=dict(size=13, color=COLORS["primary"]),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                )
                chart_card("Como se reparte el dinero entre los 3 niveles", fig_dona_monto_mora,
                           key="dona_mora_monto", height_normal=340, height_expanded=480)

        # ── Detalle por nivel de mora ─────────────────────────────────
        if camp_col_moras:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("###  Detalle individual por nivel de mora")

            for nivel, color in mora_colors.items():
                df_nivel = df_m[df_m["_nivel"] == nivel]
                if df_nivel.empty:
                    continue
                n_nivel   = len(df_nivel)
                m_nivel   = df_nivel["_saldo"].sum() if saldo_col_moras else 0
                pct_nivel = n_nivel / total_mora_shown * 100 if total_mora_shown > 0 else 0

                st.markdown(
                    f"<div style='background:{color}22; border-left:4px solid {color}; "
                    f"padding:0.7rem 1rem; border-radius:8px; margin-bottom:0.5rem;'>"
                    f"<b style='color:{COLORS['primary']}'>{nivel}</b> &nbsp;·&nbsp; "
                    f"<b>{n_nivel:,}</b> damas &nbsp;·&nbsp; "
                    f"<b>{fmt_currency(m_nivel)}</b> &nbsp;·&nbsp; "
                    f"<b>{pct_nivel:.1f}%</b> del total"
                    f"</div>", unsafe_allow_html=True,
                )

                camp_nivel = (
                    df_nivel.groupby(camp_col_moras)
                    .agg(Damas=(camp_col_moras, "count"),
                         Monto=("_saldo", "sum") if saldo_col_moras else (camp_col_moras, "count"))
                    .reset_index()
                    .sort_values(camp_col_moras, key=lambda s: s.map(_camp_sort_key))
                )
                camp_nivel["% del nivel"] = (camp_nivel["Damas"] / n_nivel * 100).round(1)

                c_graf1, c_graf2 = st.columns(2)
                with c_graf1:
                    fig1 = go.Figure(go.Bar(
                        x=camp_nivel[camp_col_moras], y=camp_nivel["Damas"],
                        marker_color=color, text=camp_nivel["Damas"], textposition="outside",
                        textfont=dict(color=COLORS["text"], size=11),
                        hovertemplate="<b>%{x}</b><br>Damas: %{y:,}<br>%{customdata:.1f}%<extra></extra>",
                        customdata=camp_nivel["% del nivel"],
                    ))
                    fig1.update_layout(**PLOTLY_LAYOUT,
                        title_text=f"Damas {nivel} por campaña",
                        title_font=dict(size=12, color=COLORS["primary"]),
                        xaxis=dict(type="category", **_AXIS_DEFAULTS),
                        yaxis=dict(title="Damas", **_AXIS_DEFAULTS), height=300)
                    st.plotly_chart(fig1, use_container_width=True, key=f"ind_{nivel.replace(' ','')}_damas")
                with c_graf2:
                    if saldo_col_moras:
                        fig2 = go.Figure(go.Bar(
                            x=camp_nivel[camp_col_moras], y=camp_nivel["Monto"],
                            marker_color=color,
                            text=camp_nivel["Monto"].apply(lambda v: f"${v/1e6:.2f}M" if v >= 1e6 else f"${v/1e3:.0f}K"),
                            textposition="outside",
                            textfont=dict(color=COLORS["text"], size=11),
                            hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
                        ))
                        fig2.update_layout(**PLOTLY_LAYOUT,
                            title_text=f"Monto {nivel} por campaña",
                            title_font=dict(size=12, color=COLORS["primary"]),
                            xaxis=dict(type="category", **_AXIS_DEFAULTS),
                            yaxis=dict(title="Monto ($)", **_AXIS_DEFAULTS), height=300)
                        st.plotly_chart(fig2, use_container_width=True, key=f"ind_{nivel.replace(' ','')}_monto")
                st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Barras: damas + monto por campaña (desde df_moras) ──────────
        if mora_col_moras and camp_col_moras:
            st.markdown("<br>", unsafe_allow_html=True)
            dist = (
                df_m.groupby(camp_col_moras)
                .agg(Damas=(camp_col_moras, "count"),
                     Monto=("_saldo", "sum") if saldo_col_moras else (camp_col_moras, "count"))
                .reset_index()
                .rename(columns={camp_col_moras: "Campaña"})
                .sort_values("Campaña", key=lambda s: s.map(_camp_sort_key))
            )
            dist["% del total moras"] = (dist["Damas"] / dist["Damas"].sum() * 100).round(1)

            fig_bar = make_subplots(specs=[[{"secondary_y": True}]])
            fig_bar.add_trace(go.Bar(
                x=dist["Campaña"], y=dist["Damas"],
                name="Damas en mora", marker_color=COLORS["danger"],
                text=dist["Damas"], textposition="outside",
                textfont=dict(color=COLORS["text"], size=11),
                hovertemplate="<b>%{x}</b><br>Damas: %{y:,}<extra></extra>",
            ), secondary_y=False)
            if saldo_col_moras:
                fig_bar.add_trace(go.Scatter(
                    x=dist["Campaña"], y=dist["Monto"],
                    name="Monto ($)", mode="lines+markers",
                    line=dict(color="#000000", width=2.5, dash="dot"),
                    marker=dict(size=8, color="#000000"),
                    hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
                ), secondary_y=True)
            fig_bar.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Damas y monto en mora por campaña",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(type="category", **_AXIS_DEFAULTS),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig_bar.update_yaxes(title_text="Número de damas", secondary_y=False, **_AXIS_DEFAULTS)
            fig_bar.update_yaxes(title_text="Monto ($)", secondary_y=True, **_AXIS_DEFAULTS)
            chart_card("Damas y dinero en mora por campaña", fig_bar, key="moras_camp",
                       height_normal=420, height_expanded=600)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Resumen por campaña:**")
            resumen_cols = ["Campaña", "Damas", "% del total moras"] + (["Monto"] if saldo_col_moras else [])
            resumen = dist[resumen_cols].copy()
            if saldo_col_moras:
                resumen["Monto"] = resumen["Monto"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(resumen, use_container_width=True, hide_index=True)

    # ── Tabla detalle de moras coincidentes ─────────────────────────
    if n_coincidencias > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"Ver detalle: {n_coincidencias:,} damas pendientes en mora"):
            tabla = df_moras[
                df_moras[nodama_mora].astype(str).str.strip().isin(coincidencias_ids)
            ].reset_index(drop=True)
            st.dataframe(tabla, use_container_width=True, height=400)

            buf = io.BytesIO()
            tabla.to_excel(buf, index=False)
            buf.seek(0)
            st.download_button(
                " Descargar moras coincidentes (Excel)",
                data=buf,
                file_name="moras_coincidentes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.success(" No se encontraron coincidencias entre las damas pendientes y el archivo de moras.")


# ─────────────────────────────────────────────
#  COMPORTAMIENTO DE CARTERA
# ─────────────────────────────────────────────

def tab_comportamiento_cartera(df_moras: pd.DataFrame | None):
    st.markdown(
        "<div class='kpi-banner'><h1>Comportamiento de Cartera</h1>"
        "<p>Análisis de cohortes, transiciones, reincidencia y salidas a través de las 10 campañas</p></div>",
        unsafe_allow_html=True,
    )

    if df_moras is None:
        st.info("Sube el archivo de moras (Consolidado) para ver este análisis.")
        return

    nodama_col = _get_nodama_col(df_moras)
    camp_col   = _find_col(df_moras, ["campania", "campaña", "camp", "campana"])
    mora_col   = _find_col(df_moras, ["moras", "mora", "nivel de mora", "nivel_mora"])
    saldo_col  = _find_col(df_moras, ["saldodama", "saldo", "importe", "monto", "importenetofactura"])
    idsit_col  = _find_col(df_moras, ["idsituacion", "id_situacion", "situacion"])

    if not nodama_col or not camp_col:
        st.error("No se encontraron las columnas NoDama o Campaña en el archivo de moras.")
        return

    MORA_LEVELS = ["Inactiva", "Mora 1", "Mora 2", "Mora 3"]
    MORA_COLORS = {
        "Inactiva": "#94A3B8",
        "Mora 1":   COLORS["warning"],
        "Mora 2":   COLORS["orange"],
        "Mora 3":   COLORS["danger"],
    }
    CHURN_WINDOW = 3

    def _camp_num(v) -> int:
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
    if mora_col:
        df["_mora"] = df[mora_col].astype(str).str.strip().str.lower().map(mora_map)
    else:
        df["_mora"] = "Mora 1"

    # Reclasificar IdSituacion=0 como Inactiva
    n_inactivas_reclasif = 0
    if idsit_col:
        mask = df[idsit_col].astype(str).str.strip() == "0"
        df.loc[mask, "_mora"] = "Inactiva"
        n_inactivas_reclasif = int(mask.sum())

    df["_camp_n"] = df[camp_col].apply(_camp_num)
    df = df[df["_camp_n"] <= 10].copy()

    all_camps_raw = sorted(df[camp_col].unique(), key=_camp_num)
    camp_labels   = all_camps_raw
    camps_n       = sorted(df["_camp_n"].unique())

    # ── Análisis de cohortes (mismo motor que tracking_campanas.py) ───
    sets: dict[int, set] = {
        c: set(df[df["_camp_n"] == c][nodama_col]) for c in camps_n
    }
    first_camp_d: dict[str, int] = df.groupby(nodama_col)["_camp_n"].min().to_dict()
    mora_sets: dict[tuple, set] = {}
    for c in camps_n:
        df_c = df[df["_camp_n"] == c]
        for mora in MORA_LEVELS:
            mora_sets[(c, mora)] = set(df_c[df_c["_mora"] == mora][nodama_col])

    summary_rows = []
    for i, c in enumerate(camps_n):
        prev_c = camps_n[i - 1] if i > 0 else None
        total_set = sets[c]
        nuevas    = {d for d in total_set if first_camp_d.get(d) == c}
        retenidas = total_set & sets[prev_c] if prev_c else set()
        future = [cx for cx in camps_n if cx > c and cx <= c + CHURN_WINDOW]
        fugadas = (total_set - set().union(*[sets[cx] for cx in future])) if future else set()

        row = {
            "camp_n":      c,
            "camp_label":  f"C{c}",
            "total":       len(total_set),
            "nuevas":      len(nuevas),
            "retenidas":   len(retenidas),
            "fugadas":     len(fugadas),
            "saldo_total": df[df["_camp_n"] == c][saldo_col].sum() if saldo_col else 0,
        }
        for mora in MORA_LEVELS:
            ids_m = mora_sets[(c, mora)]
            row[f"{mora}_total"]     = len(ids_m)
            row[f"{mora}_nuevas"]    = len(ids_m & nuevas)
            row[f"{mora}_retenidas"] = len(ids_m & retenidas)
            row[f"{mora}_fugadas"]   = len(ids_m & fugadas)
            row[f"{mora}_saldo"]     = (
                df[(df["_camp_n"] == c) & (df["_mora"] == mora)][saldo_col].sum()
                if saldo_col else 0
            )
        if prev_c is not None:
            inac_prev = mora_sets[(prev_c, "Inactiva")]
            row["from_inactiva_total"] = len(inac_prev & total_set)
            for mora in MORA_LEVELS:
                row[f"fi_to_{mora}"] = len(inac_prev & mora_sets[(c, mora)])
        else:
            row["from_inactiva_total"] = 0
            for mora in MORA_LEVELS:
                row[f"fi_to_{mora}"] = 0
        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    # Matriz de transición
    transitions = []
    for i in range(len(camps_n) - 1):
        c1, c2 = camps_n[i], camps_n[i + 1]
        shared = sets[c1] & sets[c2]
        df1 = df[(df["_camp_n"] == c1) & df[nodama_col].isin(shared)].set_index(nodama_col)["_mora"]
        df2 = df[(df["_camp_n"] == c2) & df[nodama_col].isin(shared)].set_index(nodama_col)["_mora"]
        joined = df1.to_frame("origen").join(df2.to_frame("destino"), how="inner")
        for (orig, dest), cnt in joined.groupby(["origen", "destino"]).size().items():
            transitions.append({
                "de": f"C{c1}", "a": f"C{c2}",
                "origen": orig, "destino": dest, "cuentas": int(cnt),
            })
    trans_df = pd.DataFrame(transitions) if transitions else pd.DataFrame()

    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "Cohortes por Campaña",
        "Matriz de Transición",
        "Reincidencia",
        "Salida de Cuentas",
    ])

    # ══════════════════════════════════════════
    # TAB 1 — Cohortes por Campaña
    # ══════════════════════════════════════════
    with subtab1:
        st.markdown("<br>", unsafe_allow_html=True)

        if n_inactivas_reclasif > 0:
            st.info(
                f"**{n_inactivas_reclasif:,} registros** reclasificados como **Inactiva** "
                f"(IdSituacion = 0 / INICIAL)"
            )

        # KPIs globales
        total_all  = summary_df["total"].sum()
        saldo_all  = summary_df["saldo_total"].sum() if saldo_col else 0
        inac_all   = summary_df["Inactiva_total"].sum()
        mora_all   = (summary_df["Mora 1_total"] + summary_df["Mora 2_total"] + summary_df["Mora 3_total"]).sum()

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Total Registros (todas campañas)", f"{total_all:,}")
        with k2:
            st.metric("Saldo Total", fmt_currency(saldo_all) if saldo_col else "—")
        with k3:
            st.metric("Total en Mora (1+2+3)", f"{mora_all:,}")
        with k4:
            st.metric("Total Inactivas", f"{inac_all:,}",
                      delta=f"{inac_all/total_all*100:.1f}% del total" if total_all else None,
                      delta_color="off")

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica 1: Barras apiladas Inactiva + Mora 1/2/3 por campaña
        fig_stack = go.Figure()
        for mora in MORA_LEVELS:
            fig_stack.add_trace(go.Bar(
                x=summary_df["camp_label"],
                y=summary_df[f"{mora}_total"],
                name=mora,
                marker_color=MORA_COLORS[mora],
                hovertemplate=f"<b>%{{x}}</b><br>{mora}: %{{y:,}} damas<extra></extra>",
            ))
        fig_stack.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title_text="Composición por Estado y Campaña — Inactiva + Mora 1 / 2 / 3",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", categoryorder="array",
                       categoryarray=summary_df["camp_label"].tolist(), **_AXIS_DEFAULTS),
            yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        chart_card("Estados por campaña", fig_stack,
                   key="comp_stack_mora", height_normal=400, height_expanded=580)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica 2: Líneas Nuevas / Retenidas / Fugadas (cohortes)
        fig_cohort = go.Figure()
        cohort_series = [
            ("nuevas",    "Nuevas",    COLORS["success"],  "dash"),
            ("retenidas", "Retenidas", COLORS["accent"],   "solid"),
            ("fugadas",   "Fugadas",   COLORS["danger"],   "dot"),
        ]
        for key, label, color, dash in cohort_series:
            fig_cohort.add_trace(go.Scatter(
                x=summary_df["camp_label"], y=summary_df[key],
                mode="lines+markers", name=label,
                line=dict(color=color, width=2.5, dash=dash),
                marker=dict(size=7),
                hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y:,}}<extra></extra>",
            ))
        fig_cohort.update_layout(
            **PLOTLY_LAYOUT,
            title_text=f"Cohortes: Nuevas, Retenidas y Fugadas por Campaña  (ventana fuga = {CHURN_WINDOW} camps.)",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", categoryorder="array",
                       categoryarray=summary_df["camp_label"].tolist(), **_AXIS_DEFAULTS),
            yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        chart_card("Cohortes: Nuevas / Retenidas / Fugadas", fig_cohort,
                   key="comp_cohort_lines", height_normal=400, height_expanded=580)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfica 3: Saldo por campaña
        if saldo_col:
            fig_saldo = go.Figure(go.Bar(
                x=summary_df["camp_label"], y=summary_df["saldo_total"],
                marker_color=COLORS["accent"],
                text=summary_df["saldo_total"].apply(
                    lambda v: f"${v/1e6:.1f}M" if v >= 1e6 else f"${v/1e3:.0f}K"
                ),
                textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
                hovertemplate="<b>%{x}</b><br>Saldo: $%{y:,.0f}<extra></extra>",
            ))
            fig_saldo.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Saldo Total por Campaña",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(type="category", categoryorder="array",
                           categoryarray=summary_df["camp_label"].tolist(), **_AXIS_DEFAULTS),
                yaxis=dict(title="Saldo ($)", **_AXIS_DEFAULTS),
            )
            chart_card("Saldo total por campaña", fig_saldo,
                       key="comp_saldo_camp", height_normal=380, height_expanded=560)
            st.markdown("<br>", unsafe_allow_html=True)

        # ── Tabla detallada por campaña (misma estructura que el reporte Excel) ──
        st.markdown("---")
        st.markdown("#### Detalle por Campaña")

        camp_options = summary_df["camp_label"].tolist()
        sel_camp = st.selectbox("Seleccionar campaña:", camp_options, key="sel_camp_cohort")
        r = summary_df[summary_df["camp_label"] == sel_camp].iloc[0]
        tot = int(r["total"])
        fug_tot = int(r["fugadas"])

        # KPIs de campaña
        kc1, kc2, kc3, kc4 = st.columns(4)
        with kc1:
            st.metric("Total damas", f"{tot:,}")
        with kc2:
            st.metric("Nuevas", f"{int(r['nuevas']):,}",
                      delta=f"{r['nuevas']/tot*100:.1f}% del total" if tot else None,
                      delta_color="off")
        with kc3:
            st.metric("Retenidas", f"{int(r['retenidas']):,}",
                      delta=f"{r['retenidas']/tot*100:.1f}% del total" if tot else None,
                      delta_color="off")
        with kc4:
            st.metric(f"Fuga (no aparecen en sig. {CHURN_WINDOW} camps.)",
                      f"{fug_tot:,}",
                      delta=f"{fug_tot/tot*100:.1f}% del total" if tot else None,
                      delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabla de moras — misma estructura que el reporte
        detail_rows = []
        for mora in MORA_LEVELS:
            m_tot = int(r.get(f"{mora}_total", 0))
            m_nue = int(r.get(f"{mora}_nuevas", 0))
            m_ret = int(r.get(f"{mora}_retenidas", 0))
            m_fug = int(r.get(f"{mora}_fugadas", 0))
            m_sld = r.get(f"{mora}_saldo", 0)
            detail_rows.append({
                "Nivel de Mora":  mora,
                "Total":          m_tot,
                "%":              f"{m_tot/tot*100:.1f}%" if tot else "—",
                "Nuevas":         m_nue,
                "% Nuevas":       f"{m_nue/m_tot*100:.1f}%" if m_tot else "—",
                "Retenidas":      m_ret,
                "% Ret.":         f"{m_ret/m_tot*100:.1f}%" if m_tot else "—",
                "Fugadas":        m_fug,
                "% Fuga":         f"{m_fug/m_tot*100:.1f}%" if m_tot else "—",
                "Saldo":          fmt_currency(m_sld) if saldo_col else "—",
            })
        detail_df = pd.DataFrame(detail_rows)

        # Color por mora
        def _color_row(row):
            colors = {
                "Inactiva": "background-color: #E2E8F0",
                "Mora 1":   "background-color: #FEF9C3",
                "Mora 2":   "background-color: #FFEDD5",
                "Mora 3":   "background-color: #FEE2E2",
            }
            c = colors.get(row["Nivel de Mora"], "")
            return [c] * len(row)

        styled = detail_df.style.apply(_color_row, axis=1)
        st.dataframe(styled, use_container_width=True, hide_index=True)

        # Bloque de Inactivas previas (si aplica)
        fi_total = int(r.get("from_inactiva_total", 0))
        if fi_total > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Cuentas Inactivas de la campaña anterior que reaparecen:**")
            fi_detail = []
            for mora in MORA_LEVELS:
                cnt = int(r.get(f"fi_to_{mora}", 0))
                m_tot_d = int(r.get(f"{mora}_total", 0))
                fi_detail.append({
                    "Estado destino":         mora,
                    "Vinieron de Inactiva":   cnt,
                    "% de las Inactivas":     f"{cnt/fi_total*100:.1f}%" if fi_total else "—",
                    f"% del total {mora}":    f"{cnt/m_tot_d*100:.1f}%" if m_tot_d else "—",
                })
            st.dataframe(pd.DataFrame(fi_detail), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabla compacta con todas las campañas
        with st.expander("Ver tabla compacta — todas las campañas"):
            compact_rows = []
            for _, rv in summary_df.iterrows():
                tot_v = int(rv["total"])
                compact_rows.append({
                    "Campaña":   rv["camp_label"],
                    "Total":     tot_v,
                    "Nuevas":    int(rv["nuevas"]),
                    "% Nuevas":  f"{rv['nuevas']/tot_v*100:.1f}%" if tot_v else "—",
                    "Retenidas": int(rv["retenidas"]),
                    "% Ret.":    f"{rv['retenidas']/tot_v*100:.1f}%" if tot_v else "—",
                    "Fugadas":   int(rv["fugadas"]),
                    "% Fuga":    f"{rv['fugadas']/tot_v*100:.1f}%" if tot_v else "—",
                    "Inactiva":  int(rv["Inactiva_total"]),
                    "Mora 1":    int(rv["Mora 1_total"]),
                    "Mora 2":    int(rv["Mora 2_total"]),
                    "Mora 3":    int(rv["Mora 3_total"]),
                    "Saldo":     fmt_currency(rv["saldo_total"]) if saldo_col else "—",
                })
            st.dataframe(pd.DataFrame(compact_rows), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # TAB 2 — Matriz de Transición
    # ══════════════════════════════════════════
    with subtab2:
        st.markdown("<br>", unsafe_allow_html=True)

        if trans_df.empty:
            st.info("No hay suficientes campañas para calcular transiciones.")
        else:
            # ── Selector de transición ────────────────────────────────
            trans_options = sorted(
                trans_df[["de", "a"]].drop_duplicates().apply(
                    lambda r: f"{r['de']} → {r['a']}", axis=1
                ).tolist(),
                key=lambda s: int(s.split("→")[0].strip().replace("C", ""))
            )
            sel_trans = st.selectbox(
                "Selecciona la transición a visualizar:",
                trans_options, key="sel_trans"
            )
            c_from, c_to = [s.strip() for s in sel_trans.split("→")]

            sub = trans_df[(trans_df["de"] == c_from) & (trans_df["a"] == c_to)]

            # Pivot 4×4
            pivot = sub.pivot_table(
                index="origen", columns="destino",
                values="cuentas", fill_value=0, aggfunc="sum"
            ).reindex(index=MORA_LEVELS, columns=MORA_LEVELS, fill_value=0)

            total_shared = int(pivot.values.sum())

            st.markdown(
                f"**Damas presentes en ambas campañas ({c_from} y {c_to}): {total_shared:,}**"
            )
            st.caption(
                "Cada celda muestra cuántas damas tenían el estado de la fila en "
                f"{c_from} y pasaron al estado de la columna en {c_to}."
            )

            col_heat, col_kpi = st.columns([3, 2])

            with col_heat:
                # Heatmap de transición
                z_vals    = pivot.values.tolist()
                z_pct     = [[round(v / total_shared * 100, 1) if total_shared else 0
                               for v in row] for row in z_vals]
                text_heat = [[f"{v:,}<br>({p}%)" for v, p in zip(row_v, row_p)]
                             for row_v, row_p in zip(z_vals, z_pct)]

                fig_heat = go.Figure(go.Heatmap(
                    z=z_vals,
                    x=[f"→ {m}" for m in MORA_LEVELS],
                    y=MORA_LEVELS,
                    text=text_heat, texttemplate="%{text}",
                    textfont=dict(size=12, color="black"),
                    colorscale=[
                        [0.0, "#FFFFFF"], [0.3, "#BFDBFE"],
                        [0.6, "#3B82F6"], [1.0, "#1A3C6E"],
                    ],
                    showscale=True,
                    hovertemplate=(
                        "<b>%{y} → %{x}</b><br>"
                        "Damas: %{z:,}<extra></extra>"
                    ),
                ))
                fig_heat.update_layout(
                    **PLOTLY_LAYOUT,
                    title_text=f"Matriz de Transición {c_from} → {c_to}",
                    title_font=dict(size=13, color=COLORS["primary"]),
                    xaxis=dict(title=f"Estado en {c_to}", **_AXIS_DEFAULTS),
                    yaxis=dict(title=f"Estado en {c_from}", autorange="reversed",
                               **_AXIS_DEFAULTS),
                    height=360,
                )
                st.plotly_chart(fig_heat, use_container_width=True,
                                key=f"heat_{c_from}_{c_to}")

            with col_kpi:
                st.markdown(f"**Tasas de transición desde {c_from}**")
                for mora_orig in MORA_LEVELS:
                    orig_total = int(pivot.loc[mora_orig].sum()) if mora_orig in pivot.index else 0
                    if orig_total == 0:
                        continue
                    st.markdown(
                        f"<div style='background:{MORA_COLORS[mora_orig]};padding:6px 10px;"
                        f"border-radius:6px;margin-bottom:6px'>"
                        f"<b>{mora_orig}</b> ({orig_total:,} damas)<br>"
                        + "  ".join(
                            f"→ {dest}: <b>{int(pivot.loc[mora_orig, dest])}</b> "
                            f"({round(pivot.loc[mora_orig, dest]/orig_total*100, 1) if orig_total else 0}%)"
                            for dest in MORA_LEVELS
                            if mora_orig in pivot.index and dest in pivot.columns
                        )
                        + "</div>",
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Bloque Inactivas: evolución a lo largo de todas las campañas ──
            st.markdown("---")
            st.markdown("#### Migración de Inactivas → Mora X (todas las campañas)")
            st.caption(
                "Cuentas que tenían estado Inactiva en la campaña anterior y su estado en la siguiente."
            )

            fi_rows = []
            for _, r in summary_df.iterrows():
                fi = int(r.get("from_inactiva_total", 0))
                if fi == 0:
                    continue
                fi_rows.append({
                    "Campaña":           r["camp_label"],
                    "Total de Inactivas": fi,
                    "→ Inactiva":        int(r.get("fi_to_Inactiva", 0)),
                    "→ Mora 1":          int(r.get("fi_to_Mora 1", 0)),
                    "→ Mora 2":          int(r.get("fi_to_Mora 2", 0)),
                    "→ Mora 3":          int(r.get("fi_to_Mora 3", 0)),
                })
            fi_df = pd.DataFrame(fi_rows)

            if not fi_df.empty:
                col_fi_bar, col_fi_tbl = st.columns([3, 2])
                with col_fi_bar:
                    fig_fi = go.Figure()
                    for dest, color in [
                        ("→ Inactiva", MORA_COLORS["Inactiva"]),
                        ("→ Mora 1",   MORA_COLORS["Mora 1"]),
                        ("→ Mora 2",   MORA_COLORS["Mora 2"]),
                        ("→ Mora 3",   MORA_COLORS["Mora 3"]),
                    ]:
                        fig_fi.add_trace(go.Bar(
                            x=fi_df["Campaña"], y=fi_df[dest],
                            name=dest, marker_color=color,
                            hovertemplate=f"<b>%{{x}}</b><br>{dest}: %{{y:,}}<extra></extra>",
                        ))
                    fig_fi.update_layout(
                        **PLOTLY_LAYOUT, barmode="stack",
                        title_text="Inactivas del período anterior → estado en campaña actual",
                        title_font=dict(size=13, color=COLORS["primary"]),
                        xaxis=dict(type="category", **_AXIS_DEFAULTS),
                        yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                    xanchor="right", x=1),
                        height=360,
                    )
                    st.plotly_chart(fig_fi, use_container_width=True, key="fi_stack")
                with col_fi_tbl:
                    st.markdown("**Tabla de transición de Inactivas**")
                    st.dataframe(fi_df, use_container_width=True, hide_index=True)
            else:
                st.info("No hay datos de transición desde estado Inactiva.")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabla global de todas las transiciones ─────────────────
            st.markdown("#### Resumen de todas las transiciones")
            all_trans_rows = []
            for opt in trans_options:
                cf, ct = [s.strip() for s in opt.split("→")]
                sub_t  = trans_df[(trans_df["de"] == cf) & (trans_df["a"] == ct)]
                pv     = sub_t.pivot_table(
                    index="origen", columns="destino",
                    values="cuentas", fill_value=0, aggfunc="sum"
                ).reindex(index=MORA_LEVELS, columns=MORA_LEVELS, fill_value=0)
                total_t = int(pv.values.sum())
                for mora in MORA_LEVELS:
                    orig_t = int(pv.loc[mora].sum()) if mora in pv.index else 0
                    if orig_t == 0:
                        continue
                    for dest in MORA_LEVELS:
                        val = int(pv.loc[mora, dest]) if mora in pv.index and dest in pv.columns else 0
                        all_trans_rows.append({
                            "Transición": opt,
                            "Origen":     mora,
                            "Destino":    dest,
                            "Damas":      val,
                            "% del Origen": f"{val/orig_t*100:.1f}%" if orig_t else "—",
                        })
            if all_trans_rows:
                at_df = pd.DataFrame(all_trans_rows)
                st.dataframe(at_df, use_container_width=True, hide_index=True, height=380)

    # ══════════════════════════════════════════
    # TAB 3 — Reincidencia
    # ══════════════════════════════════════════
    with subtab3:
        st.markdown("<br>", unsafe_allow_html=True)

        # Count unique campaigns per dama
        camps_per_dama = (
            df[df[camp_col].isin(camp_labels)]
            .groupby(nodama_col)[camp_col]
            .nunique()
            .reset_index()
            .rename(columns={camp_col: "num_camps"})
        )

        total_damas_uniq = len(camps_per_dama)
        solo_1      = (camps_per_dama["num_camps"] == 1).sum()
        dos_tres    = camps_per_dama["num_camps"].between(2, 3).sum()
        cuatro_plus = (camps_per_dama["num_camps"] >= 4).sum()

        pct_1   = solo_1      / total_damas_uniq * 100 if total_damas_uniq > 0 else 0
        pct_23  = dos_tres    / total_damas_uniq * 100 if total_damas_uniq > 0 else 0
        pct_4p  = cuatro_plus / total_damas_uniq * 100 if total_damas_uniq > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Total Damas Únicas", f"{total_damas_uniq:,}")
        with k2:
            st.metric("Solo 1 campaña", f"{solo_1:,}", delta=f"{pct_1:.1f}%", delta_color="off")
        with k3:
            st.metric("2 – 3 campañas", f"{dos_tres:,}", delta=f"{pct_23:.1f}%", delta_color="off")
        with k4:
            st.metric("4+ campañas", f"{cuatro_plus:,}", delta=f"{pct_4p:.1f}%", delta_color="off")

        st.markdown("<br>", unsafe_allow_html=True)

        col_hist, col_pie = st.columns(2)

        with col_hist:
            dist_camps = (
                camps_per_dama["num_camps"]
                .value_counts()
                .reindex(range(1, 11), fill_value=0)
                .reset_index()
            )
            dist_camps.columns = ["Num Campañas", "Damas"]

            fig_hist = go.Figure(go.Bar(
                x=dist_camps["Num Campañas"].astype(str),
                y=dist_camps["Damas"],
                marker_color=PASTEL_SEQ[:10],
                text=dist_camps["Damas"], textposition="outside",
                textfont=dict(size=11, color=COLORS["text"]),
                hovertemplate="<b>%{x} campaña(s)</b><br>Damas: %{y:,}<extra></extra>",
            ))
            fig_hist.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Distribución: ¿En cuántas campañas aparece cada dama?",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(title="Número de Campañas", type="category", **_AXIS_DEFAULTS),
                yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
            )
            chart_card("Campañas por dama — distribución", fig_hist,
                       key="reinc_hist", height_normal=380, height_expanded=560)

        with col_pie:
            pie_labels = ["Solo 1 campaña", "2 – 3 campañas", "4+ campañas"]
            pie_values = [solo_1, dos_tres, cuatro_plus]
            pie_colors = [COLORS["accent"], COLORS["warning"], COLORS["danger"]]

            fig_pie = go.Figure(go.Pie(
                labels=pie_labels, values=pie_values,
                hole=0.55,
                marker_colors=pie_colors,
                textinfo="label+percent",
                textfont=dict(size=13, color=COLORS["text"]),
                hovertemplate="<b>%{label}</b><br>Damas: %{value:,}<br>%{percent}<extra></extra>",
            ))
            fig_pie.update_layout(
                **PLOTLY_LAYOUT,
                title_text="Damas únicas vs recurrentes",
                title_font=dict(size=13, color=COLORS["primary"]),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                annotations=[dict(
                    text=f"<b>{pct_1:.0f}%</b><br><span style='font-size:10px'>solo 1</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=16, color=COLORS["primary"]),
                    xref="paper", yref="paper",
                )],
            )
            chart_card("Única vs recurrente", fig_pie,
                       key="reinc_pie", height_normal=380, height_expanded=560)

        st.markdown("<br>", unsafe_allow_html=True)

        # Top damas by number of campaigns
        st.markdown("#### Top Damas por Número de Campañas")

        # last mora per dama
        if mora_col:
            last_mora = (
                df[df[camp_col].isin(camp_labels)]
                .sort_values(camp_col, key=lambda s: s.map(_camp_num))
                .groupby(nodama_col)["_mora"]
                .last()
                .reset_index()
                .rename(columns={"_mora": "Última Mora"})
            )
        else:
            last_mora = pd.DataFrame(columns=[nodama_col, "Última Mora"])

        # list of campaigns per dama
        camp_list_per_dama = (
            df[df[camp_col].isin(camp_labels)]
            .sort_values(camp_col, key=lambda s: s.map(_camp_num))
            .groupby(nodama_col)[camp_col]
            .apply(lambda x: ", ".join(x.unique()))
            .reset_index()
            .rename(columns={camp_col: "Campañas"})
        )

        top_damas = (
            camps_per_dama
            .sort_values("num_camps", ascending=False)
            .head(30)
            .merge(camp_list_per_dama, on=nodama_col, how="left")
            .merge(last_mora, on=nodama_col, how="left")
            .rename(columns={nodama_col: "NoDama", "num_camps": "Num Campañas"})
        )
        st.dataframe(top_damas[["NoDama", "Num Campañas", "Campañas", "Última Mora"]],
                     use_container_width=True, hide_index=True, height=400)

    # ══════════════════════════════════════════
    # TAB 4 — Salida de Cuentas
    # ══════════════════════════════════════════
    with subtab4:
        st.markdown("<br>", unsafe_allow_html=True)

        df_active = df[df[camp_col].isin(camp_labels)].copy()

        last_camp_per_dama = (
            df_active
            .sort_values(camp_col, key=lambda s: s.map(_camp_num))
            .groupby(nodama_col)
            .agg(
                last_camp=(camp_col, "last"),
                last_mora=("_mora", "last"),
            )
            .reset_index()
        )

        max_camp = camp_labels[-1] if camp_labels else None

        if max_camp:
            last_camp_per_dama["still_active"] = last_camp_per_dama["last_camp"] == max_camp
        else:
            last_camp_per_dama["still_active"] = False

        permanently_exited = last_camp_per_dama[~last_camp_per_dama["still_active"]]
        still_active       = last_camp_per_dama[last_camp_per_dama["still_active"]]

        n_exited = len(permanently_exited)
        n_active = len(still_active)
        total_u  = len(last_camp_per_dama)

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Damas aún activas (en C10)", f"{n_active:,}")
        with k2:
            st.metric("Damas salidas permanentemente", f"{n_exited:,}")
        with k3:
            pct_exit = n_exited / total_u * 100 if total_u > 0 else 0
            st.metric("% de salida acumulada", f"{pct_exit:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # Bar: count of damas whose last campaign is Cn (exits per campaign)
        exit_counts = (
            last_camp_per_dama
            .groupby("last_camp")
            .size()
            .reindex(camp_labels, fill_value=0)
            .reset_index()
        )
        exit_counts.columns = ["Campaña", "Damas"]

        # Distinguish active vs exited for coloring
        exit_counts["tipo"] = exit_counts["Campaña"].apply(
            lambda c: "Aún activas" if c == max_camp else "Salida permanente"
        )

        fig_exit = go.Figure()
        for tipo, color in [("Salida permanente", COLORS["danger"]),
                             ("Aún activas",       COLORS["success"])]:
            mask = exit_counts["tipo"] == tipo
            fig_exit.add_trace(go.Bar(
                x=exit_counts.loc[mask, "Campaña"],
                y=exit_counts.loc[mask, "Damas"],
                name=tipo, marker_color=color,
                text=exit_counts.loc[mask, "Damas"],
                textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
                hovertemplate=f"<b>%{{x}}</b><br>{tipo}: %{{y:,}} damas<extra></extra>",
            ))
        fig_exit.update_layout(
            **PLOTLY_LAYOUT, barmode="stack",
            title_text="Última campaña de cada dama — ¿Cuándo salen del portafolio?",
            title_font=dict(size=13, color=COLORS["primary"]),
            xaxis=dict(type="category", categoryorder="array",
                       categoryarray=camp_labels, **_AXIS_DEFAULTS),
            yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        chart_card("Damas cuya última aparición fue en cada campaña", fig_exit,
                   key="salida_last_camp", height_normal=400, height_expanded=580)

        st.markdown("<br>", unsafe_allow_html=True)

        # Mora distribution at exit (permanently exited only)
        if not permanently_exited.empty and mora_col:
            st.markdown("#### Nivel de mora en la última campaña (damas con salida permanente)")

            exit_mora_counts = (
                permanently_exited
                .groupby(["last_camp", "last_mora"])
                .size()
                .unstack(fill_value=0)
                .reindex(columns=MORA_LEVELS, fill_value=0)
                .reindex(index=[c for c in camp_labels if c != max_camp], fill_value=0)
                .reset_index()
                .rename(columns={"last_camp": "Campaña"})
            )

            fig_exit_mora = go.Figure()
            for nivel in MORA_LEVELS:
                color = MORA_COLORS[nivel]
                if nivel in exit_mora_counts.columns:
                    fig_exit_mora.add_trace(go.Bar(
                        x=exit_mora_counts["Campaña"],
                        y=exit_mora_counts[nivel],
                        name=nivel, marker_color=color,
                        hovertemplate=f"<b>%{{x}}</b><br>{nivel} al salir: %{{y:,}} damas<extra></extra>",
                    ))
            fig_exit_mora.update_layout(
                **PLOTLY_LAYOUT, barmode="stack",
                title_text="Nivel de Mora al Momento de la Salida (por campaña)",
                title_font=dict(size=13, color=COLORS["primary"]),
                xaxis=dict(type="category", categoryorder="array",
                           categoryarray=[c for c in camp_labels if c != max_camp],
                           **_AXIS_DEFAULTS),
                yaxis=dict(title="Número de Damas", **_AXIS_DEFAULTS),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            chart_card("Mora al salir del portafolio (permanente)", fig_exit_mora,
                       key="salida_mora_exit", height_normal=400, height_expanded=580)

            st.markdown("<br>", unsafe_allow_html=True)

            # KPIs: mora distribution at exit (incluye Inactiva)
            exit_mora_total = permanently_exited["last_mora"].value_counts()
            n_exit_total    = len(permanently_exited)
            exit_cols = st.columns(len(MORA_LEVELS))
            for col_k, nivel in zip(exit_cols, MORA_LEVELS):
                n_nivel = exit_mora_total.get(nivel, 0)
                pct_n   = n_nivel / n_exit_total * 100 if n_exit_total > 0 else 0
                with col_k:
                    st.metric(f"Salieron como {nivel}", f"{n_nivel:,}",
                              delta=f"{pct_n:.1f}% de salidas", delta_color="off")


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
                        st.session_state.df_cartera.copy(),
                        st.session_state.df_saldos.copy(),
                        mapping,
                    )
                    st.session_state.mapping = mapping
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        " Resumen General",
        " Temporalidad",
        "Operaciones y Territorio",
        " Moras",
        " Comportamiento de Cartera",
    ])
    with tab1:
        tab_resumen(metrics)
    with tab2:
        tab_temporalidad(metrics)
    with tab3:
        tab_flujo(metrics)
    with tab4:
        tab_moras(metrics, st.session_state.df_moras)
    with tab5:
        tab_comportamiento_cartera(st.session_state.df_moras)


if __name__ == "__main__":
    main()
