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
    page_icon="💼",
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
#  PALETA DE COLORES (PLOTLY)
# ─────────────────────────────────────────────
COLORS = {
    "primary":  "#1a3c6e",
    "accent":   "#2563eb",
    "success":  "#16a34a",
    "warning":  "#d97706",
    "danger":   "#dc2626",
    "muted":    "#6b7280",
    "bg":       "#ffffff",
    "grid":     "#e5e7eb",
    "text":     "#1a1a2e",
}

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
    """Lee el Excel y normaliza nombres de columnas."""
    df = pd.read_excel(file)
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
        "<b>⚙️ Mapeo de columnas</b> — Selecciona las columnas de cada archivo.</div>",
        unsafe_allow_html=True,
    )

    # ── Llave de cruce (misma estructura en ambos archivos) ───────────
    st.markdown("##### 🔑 Llave de cruce — *igual en ambos archivos*")
    st.caption("Se concatena **Número de Dama + Año Campaña Saldo** en los dos Excel para unirlos.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**📁 Cartera**")
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
        st.markdown("**📁 Saldos Actualizados**")
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
    st.markdown("##### 💰 Columna de saldo en Saldos Actualizados")
    col_c, col_d = st.columns(2)
    with col_c:
        s_saldo = st.selectbox(
            "Columna con el saldo / deuda ⭐", cols_s,
            index=_best_guess(cols_s, ["saldocampaña", "saldocampana", "saldo", "deuda", "valor", "monto", "pendiente"]),
            key="map_s_saldo",
        )
    with col_d:
        st.markdown("")
        st.info("**Saldo = 0** → ✅ Pagado\n\n**Saldo > 0** → 🔴 Pendiente (ese valor es la deuda)")

    st.divider()

    # ── Monto original en Cartera (opcional) ─────────────────────────
    st.markdown("##### 📊 Monto original en Cartera *(opcional)*")
    c_monto = st.selectbox(
        "Columna con la deuda original de Cartera",
        ["(ninguna)"] + cols_c,
        index=_best_guess(["(ninguna)"] + cols_c, ["saldocampaña", "saldocampana", "valor", "monto", "deuda", "total"]),
        key="map_c_monto",
        help="Si existe, permite calcular Total Cartera y Total Cobrado.",
    )

    st.markdown("")
    if st.button("✅ Confirmar y procesar", type="primary", use_container_width=True):
        return {
            "c_dama":  c_dama,
            "c_anio":  c_anio,
            "c_monto": None if c_monto == "(ninguna)" else c_monto,
            "s_dama":  s_dama,
            "s_anio":  s_anio,
            "s_saldo": s_saldo,
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

    # ── Estado de pago: saldo == 0 → Pagado, saldo > 0 → Pendiente ───
    pagado_mask = df_merged[saldo_col] == 0 if saldo_col else pd.Series([False] * len(df_merged))
    df_merged["Estado_Pago"] = np.where(pagado_mask, "Pagado", "Pendiente")

    return {
        "merged":    df_merged,
        "saldo_col": saldo_col,
        "valor_col": valor_col,
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
        labels=["✅ Pagado", "🔴 Pendiente"],
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
    pagado    = grp[grp["Estado_Pago"] == "Pagado"].set_index(camp_col)[valor_col].reindex(camps, fill_value=0)
    pendiente = grp[grp["Estado_Pago"] == "Pendiente"].set_index(camp_col)[valor_col].reindex(camps, fill_value=0)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=camps, y=pagado.values, name="✅ Cobrado",
        marker_color=COLORS["success"],
        text=[_fmt(v) for v in pagado.values], textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=camps, y=pendiente.values, name="🔴 Pendiente",
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
    total_by_camp = grp.groupby(camp_col)["n"].sum()
    pagado    = grp[grp["Estado_Pago"] == "Pagado"].set_index(camp_col)["n"].reindex(camps, fill_value=0)
    pendiente = grp[grp["Estado_Pago"] == "Pendiente"].set_index(camp_col)["n"].reindex(camps, fill_value=0)
    total_s   = total_by_camp.reindex(camps, fill_value=1)
    pct_pag = (pagado / total_s * 100).values
    pct_pen = (pendiente / total_s * 100).values
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=camps, y=pct_pag, name="✅ Cobrado",
        marker_color=COLORS["success"],
        text=[f"{v:.1f}%" for v in pct_pag], textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=camps, y=pct_pen, name="🔴 Pendiente",
        marker_color=COLORS["danger"],
        text=[f"{v:.1f}%" for v in pct_pen], textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate="<b>Campaña %{x}</b><br>Pendiente: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=80, line_dash="dot", line_color=COLORS["warning"], line_width=1.5,
                  annotation_text="  Meta 80%", annotation_font_color=COLORS["warning"])
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
    stages = ["📋 Total Cartera", "📂 Con Saldo Asignado", "🔴 Pendientes de Pago", "✅ Pagadas"]
    values = [total, con_saldo, pendiente, pagado]
    colors = [COLORS["primary"], COLORS["accent"], COLORS["danger"], COLORS["success"]]
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textposition="inside",
        textinfo="value+percent initial",
        textfont=dict(color="white", size=12),
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


def plot_linea_tendencia(df: pd.DataFrame, valor_col: str) -> go.Figure:
    """Gráfico de líneas: tendencia de cobro por campaña."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or not valor_col or camp_col not in df.columns:
        return _base_fig()
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
    cobrado   = df[df["Estado_Pago"] == "Pagado"].groupby(camp_col)[valor_col].sum()
    pendiente = df[df["Estado_Pago"] == "Pendiente"].groupby(camp_col)[valor_col].sum()
    camps = sorted(set(cobrado.index) | set(pendiente.index), key=str)
    cob_vals = cobrado.reindex(camps, fill_value=0).values
    pen_vals = pendiente.reindex(camps, fill_value=0).values
    camps_str = [str(c) for c in camps]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=camps_str, y=cob_vals, name="✅ Cobrado",
        mode="lines+markers",
        line=dict(color=COLORS["success"], width=3),
        marker=dict(size=7, color=COLORS["success"], line=dict(width=2, color="white")),
        fill="tozeroy", fillcolor="rgba(22,163,74,0.08)",
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=camps_str, y=pen_vals, name="🔴 Pendiente",
        mode="lines+markers",
        line=dict(color=COLORS["danger"], width=3),
        marker=dict(size=7, color=COLORS["danger"], line=dict(width=2, color="white")),
        fill="tozeroy", fillcolor="rgba(220,38,38,0.06)",
        hovertemplate="<b>Campaña %{x}</b><br>Pendiente: $%{y:,.0f}<extra></extra>",
    ))
    if len(cob_vals) >= 3:
        rolling = pd.Series(cob_vals).rolling(3, min_periods=1).mean().values
        fig.add_trace(go.Scatter(
            x=camps_str, y=rolling, name="Tendencia (prom. móvil)",
            mode="lines", line=dict(color=COLORS["warning"], width=2, dash="dot"),
            hovertemplate="Tendencia: $%{y:,.0f}<extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Tendencia de Recuperación por Campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Campaña", yaxis_title="Monto ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def plot_area_apilada(df: pd.DataFrame, valor_col: str) -> go.Figure:
    """Área apilada: evolución del monto cobrado + pendiente por campaña."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or not valor_col or camp_col not in df.columns:
        return _base_fig()
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
    cobrado   = df[df["Estado_Pago"] == "Pagado"].groupby(camp_col)[valor_col].sum()
    pendiente = df[df["Estado_Pago"] == "Pendiente"].groupby(camp_col)[valor_col].sum()
    camps     = sorted(set(cobrado.index) | set(pendiente.index), key=str)
    camps_str = [str(c) for c in camps]
    cob_vals  = cobrado.reindex(camps, fill_value=0).values
    pen_vals  = pendiente.reindex(camps, fill_value=0).values
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=camps_str, y=pen_vals, name="🔴 Pendiente",
        stackgroup="one", mode="lines",
        line=dict(color=COLORS["danger"], width=1),
        fillcolor="rgba(220,38,38,0.45)",
        hovertemplate="<b>Campaña %{x}</b><br>Pendiente: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=camps_str, y=cob_vals, name="✅ Cobrado",
        stackgroup="one", mode="lines",
        line=dict(color=COLORS["success"], width=1),
        fillcolor="rgba(22,163,74,0.55)",
        hovertemplate="<b>Campaña %{x}</b><br>Cobrado: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Evolución de Montos: Cobrado y Pendiente por Campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Campaña", yaxis_title="Monto Total ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def plot_heatmap(df: pd.DataFrame, valor_col: str) -> go.Figure:
    """
    Mapa de calor: Año (filas) × Período (columnas).
    Si el código de campaña tiene 6 dígitos YYYYPP, lo descompone.
    """
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or not valor_col or camp_col not in df.columns:
        return _base_fig()
    df = df.copy()
    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
    df["_camp_str"] = df[camp_col].astype(str).str.strip()
    mask_6 = df["_camp_str"].str.match(r"^\d{6}$")
    if mask_6.sum() < 2:
        # Fallback: heatmap de % cobrado por campaña vs Estado (2 columnas)
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
    pivot = pct_grp.unstack(fill_value=0)
    anios = sorted(pivot.index.tolist())
    periodos = sorted(pivot.columns.tolist())
    z = [[pivot.loc[a, p] if p in pivot.columns else 0 for p in periodos] for a in anios]
    text_z = [[f"{v:.1f}%" for v in row] for row in z]
    fig = go.Figure(go.Heatmap(
        z=z, x=periodos, y=anios,
        text=text_z, texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        colorscale=[[0, COLORS["danger"]], [0.5, COLORS["warning"]], [1, COLORS["success"]]],
        zmin=0, zmax=100,
        colorbar=dict(title="% Cobrado", ticksuffix="%"),
        hovertemplate="Año: %{y} · Período: %{x}<br>% Cobrado: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Mapa de Calor · % Cobrado por Año y Período de Campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Período", yaxis_title="Año",
        height=max(280, len(anios) * 60 + 100),
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
    metas = [50, 80]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(
        x=[pct], y=["% Damas que pagaron"],
        orientation="h",
        marker=dict(
            color=COLORS["success"] if pct >= 80 else COLORS["warning"] if pct >= 50 else COLORS["danger"],
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
                      line=dict(color=COLORS["muted"], width=2, dash="dash"),
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
            colorscale=[[0, "#fbbf24"], [0.6, "#f97316"], [1, "#dc2626"]],
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
            name="🔮 Proyección", marker_color=COLORS["warning"], opacity=0.8,
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
                          line=dict(dash="dash", color=COLORS["muted"], width=1.5))
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


def plot_cambio_temporalidad(df: pd.DataFrame) -> go.Figure:
    """Damas que tienen campañas pagadas Y pendientes — cambio de temporalidad."""
    num_col  = _find_num_col(df)
    if not num_col:
        return _base_fig()

    status_sets  = df.groupby(num_col)["Estado_Pago"].apply(set)
    mixed_mask   = status_sets.apply(lambda s: "Pagado" in s and "Pendiente" in s)
    mixed_idx    = status_sets[mixed_mask].index

    if len(mixed_idx) == 0:
        fig = _base_fig()
        fig.add_annotation(text="No hay damas con cambios de temporalidad detectados",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=13, color=COLORS["muted"]), xref="paper", yref="paper")
        return fig

    mixed_df = df[df[num_col].isin(mixed_idx)]
    pag = mixed_df[mixed_df["Estado_Pago"] == "Pagado"].groupby(num_col).size().rename("pagadas")
    pen = mixed_df[mixed_df["Estado_Pago"] == "Pendiente"].groupby(num_col).size().rename("pendientes")
    summary = pd.concat([pag, pen], axis=1).fillna(0).astype(int)
    summary["total"] = summary["pagadas"] + summary["pendientes"]
    summary = summary.sort_values("total", ascending=False).head(20).sort_values("pagadas")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=summary["pagadas"], y=summary.index.astype(str),
        orientation="h", name="✅ Campañas Pagadas",
        marker_color=COLORS["success"],
        text=summary["pagadas"].astype(str), textposition="inside",
        textfont=dict(color="white", size=10),
        hovertemplate="<b>Dama %{y}</b><br>Campañas pagadas: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=summary["pendientes"], y=summary.index.astype(str),
        orientation="h", name="🔴 Campañas Pendientes",
        marker_color=COLORS["danger"],
        text=summary["pendientes"].astype(str), textposition="inside",
        textfont=dict(color="white", size=10),
        hovertemplate="<b>Dama %{y}</b><br>Campañas pendientes: %{x}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text=f"Top 20 damas con campañas pagadas Y pendientes (de {len(mixed_idx):,} en total)",
        title_font=dict(size=14, color=COLORS["primary"]),
        barmode="stack",
        xaxis_title="Número de Campañas", yaxis_title="",
        height=max(340, len(summary) * 26),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def plot_delta_campanas(df: pd.DataFrame) -> go.Figure:
    """Delta de % cobrado entre campañas consecutivas — mayor y menor incremento."""
    camp_col = _find_col(df, ["aniocampaña", "aniocampana", "anio", "año", "campaña"])
    if not camp_col or camp_col not in df.columns:
        return _base_fig()

    total  = df.groupby(camp_col).size()
    pagado = df[df["Estado_Pago"] == "Pagado"].groupby(camp_col).size()
    pct    = (pagado / total * 100).fillna(0)
    pct.index = pct.index.astype(str)
    pct    = pct.sort_index()

    if len(pct) < 2:
        return _base_fig()

    delta = pct.diff().dropna()
    camps = delta.index.tolist()
    vals  = delta.values
    colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in vals]
    labels = [f"+{v:.1f}%" if v >= 0 else f"{v:.1f}%" for v in vals]

    max_idx = delta.idxmax()
    min_idx = delta.idxmin()

    fig = go.Figure(go.Bar(
        x=camps, y=vals,
        marker_color=colors,
        text=labels, textposition="outside", textfont=dict(size=11),
        hovertemplate="<b>Campaña %{x}</b><br>Cambio vs anterior: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=0, line_color=COLORS["muted"], line_width=1.2)
    fig.add_annotation(x=max_idx, y=delta[max_idx],
                       text="📈 Mayor incremento", showarrow=True, arrowhead=2,
                       font=dict(size=10, color=COLORS["success"]),
                       arrowcolor=COLORS["success"], ay=-35, ax=0)
    fig.add_annotation(x=min_idx, y=delta[min_idx],
                       text="📉 Mayor caída", showarrow=True, arrowhead=2,
                       font=dict(size=10, color=COLORS["danger"]),
                       arrowcolor=COLORS["danger"], ay=35, ax=0)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Cambio en % de Cobro entre campañas consecutivas",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Campaña", yaxis_title="Δ % Cobrado vs campaña anterior",
        height=360,
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
    expanded = st.session_state.get("chart_expanded") == key

    if expanded:
        st.markdown(f"<div class='chart-card-expanded'><div class='chart-title'>{title}</div></div>",
                    unsafe_allow_html=True)
        if st.button("✕  Cerrar", key=f"close_{key}"):
            st.session_state["chart_expanded"] = None
            st.rerun()
        fig.update_layout(height=height_expanded)
        st.plotly_chart(fig, use_container_width=True, key=f"plot_{key}_exp",
                        config={"displayModeBar": True, "scrollZoom": True})
    else:
        st.markdown(f"<div class='chart-card'><div class='chart-title'>{title}</div></div>",
                    unsafe_allow_html=True)
        if st.button("⛶  Ampliar", key=f"expand_{key}"):
            st.session_state["chart_expanded"] = key
            st.rerun()
        fig.update_layout(height=height_normal)
        st.plotly_chart(fig, use_container_width=True, key=f"plot_{key}",
                        config={"displayModeBar": False, "scrollZoom": True})


# ─────────────────────────────────────────────
#  SIDEBAR CON FILTROS
# ─────────────────────────────────────────────

def render_sidebar(data: dict | None) -> dict:
    filters = {}
    with st.sidebar:
        st.markdown("## 💼 Cartera Dashboard")
        st.markdown(
            f"<span style='color:{COLORS['muted']};font-size:0.8rem'>Gestión Financiera Profesional</span>",
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
                f"📊 Total registros: <b>{total:,}</b><br>"
                f"✅ Pagadas: <b>{pagados:,}</b><br>"
                f"🔴 Pendientes: <b>{pend:,}</b>"
                f"</small>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Carga los archivos Excel para activar los filtros.")

        st.divider()
        st.markdown(
            f"<small style='color:{COLORS['muted']}'>Proyección: Regresión Lineal</small>",
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
        "<div class='kpi-banner'><h1>📊 Resumen General de Cartera</h1>"
        "<p>Haz clic en <b>⛶ Ampliar</b> en cualquier gráfica para verla en grande</p></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4, c5 = st.columns(5)
    pct_cobrado = metrics["monto_cobrado"] / metrics["monto_total"] * 100 if metrics["monto_total"] else 0
    with c1: st.metric("📋 Total Registros",  f"{metrics['total_registros']:,}")
    with c2: st.metric("💼 Total Cartera",     fmt_currency(metrics["monto_total"]))
    with c3: st.metric("✅ Total Cobrado",      fmt_currency(metrics["monto_cobrado"]),
                       delta=f"+{pct_cobrado:.1f}% del total")
    with c4: st.metric("🔴 Saldo Pendiente",   fmt_currency(metrics["monto_pendiente"]),
                       delta=f"{metrics['pendientes']:,} damas deben", delta_color="inverse")
    with c5: st.metric("🎯 % Cumplimiento",    f"{metrics['pct_cumplimiento']:.1f}%",
                       delta=f"{metrics['pagados']:,} ya pagaron")
    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 1: Columnas agrupadas + 100% apilado
    col_a, col_b = st.columns(2)
    with col_a:
        chart_card("Cobrado vs Pendiente por Campaña",
                   plot_columnas_agrupadas(metrics["df"], metrics["valor_col"]),
                   key="col_agrupadas", height_normal=380)
    with col_b:
        chart_card("¿Qué % se recuperó por campaña?",
                   plot_100pct_apilado(metrics["df"]),
                   key="pct100", height_normal=360)

    # Fila 2: Donut + Embudo
    col_c, col_d = st.columns([1, 1])
    with col_c:
        chart_card("Estado de Pago · Distribución",
                   plot_kpi_donut(metrics["pagados"], metrics["pendientes"]),
                   key="donut", height_normal=320)
    with col_d:
        chart_card("Embudo de Cobranza · ¿Dónde está la cartera?",
                   plot_funnel(metrics["df"], metrics["saldo_col"]),
                   key="funnel", height_normal=380)

    with st.expander("🗂 Ver datos consolidados (primeros 200 registros)"):
        st.dataframe(metrics["df"].head(200), use_container_width=True, height=300)


def tab_temporalidad(metrics: dict):
    st.markdown(
        "<div class='kpi-banner'><h1>📅 Temporalidad de Cobro</h1>"
        "<p>Analiza cuándo y cómo evoluciona la recuperación campaña a campaña</p></div>",
        unsafe_allow_html=True,
    )
    chart_card("Tendencia de Cobro por Campaña",
               plot_linea_tendencia(metrics["df"], metrics["valor_col"]),
               key="linea", height_normal=380, height_expanded=560)
    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("Evolución del Monto Cobrado y Pendiente (Área Apilada)",
               plot_area_apilada(metrics["df"], metrics["valor_col"]),
               key="area", height_normal=380, height_expanded=560)
    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("Mapa de Calor · % Cobrado por Año y Período",
               plot_heatmap(metrics["df"], metrics["valor_col"]),
               key="heatmap", height_normal=340, height_expanded=500)


def tab_flujo(metrics: dict):
    st.markdown(
        "<div class='kpi-banner'><h1>🌊 Flujo y Proyección de Cartera</h1>"
        "<p>Gráfica de cascada, cumplimiento vs meta y proyección de próximas campañas</p></div>",
        unsafe_allow_html=True,
    )
    # Bullet: meta vs real
    chart_card("Cumplimiento Actual vs Meta de Cobranza",
               plot_bullet(metrics),
               key="bullet", height_normal=280, height_expanded=400)
    st.markdown("<br>", unsafe_allow_html=True)
    # Waterfall
    chart_card("Cascada · Cómo se reduce la deuda con cada campaña",
               plot_waterfall(metrics["df"], metrics["valor_col"]),
               key="waterfall", height_normal=420, height_expanded=600)
    st.markdown("<br>", unsafe_allow_html=True)
    # Proyección
    pred_df = predict_recovery(metrics["ts"])
    if not pred_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Próxima campaña (estimado)", fmt_currency(pred_df["prediccion"].iloc[0]))
        with col2: st.metric("Límite Superior",             fmt_currency(pred_df["upper"].iloc[0]))
        with col3: st.metric("Límite Inferior",             fmt_currency(pred_df["lower"].iloc[0]))
        st.markdown("<br>", unsafe_allow_html=True)
    chart_card("Proyección · Próximas Campañas (Regresión Lineal)",
               plot_prediction(metrics["ts"], pred_df if not pred_df.empty else pd.DataFrame()),
               key="prediccion", height_normal=440, height_expanded=600)
    st.divider()

    # ── KPIs: cambio de temporalidad ─────────────────────────────────
    num_col = _find_num_col(metrics["df"])
    if num_col:
        status_sets  = metrics["df"].groupby(num_col)["Estado_Pago"].apply(set)
        mixed_count  = int(status_sets.apply(lambda s: "Pagado" in s and "Pendiente" in s).sum())
        total_pend   = int((metrics["df"]["Estado_Pago"] == "Pendiente").sum())
        pct_mixed    = mixed_count / total_pend * 100 if total_pend else 0
        c1, c2, c3  = st.columns(3)
        with c1: st.metric("🔄 Damas con cambio de temporalidad", f"{mixed_count:,}")
        with c2: st.metric("📊 % de los no pagados",              f"{pct_mixed:.1f}%")
        with c3: st.metric("🔴 Total Pendientes",                 f"{total_pend:,}")
        st.markdown("<br>", unsafe_allow_html=True)

    chart_card("Damas con campañas pagadas Y pendientes (cambio de temporalidad)",
               plot_cambio_temporalidad(metrics["df"]),
               key="cambio_temp", height_normal=460, height_expanded=660)
    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("¿Qué campaña tuvo el mayor y menor incremento de cobro?",
               plot_delta_campanas(metrics["df"]),
               key="delta_camps", height_normal=360, height_expanded=520)

    col_d, _ = st.columns([1, 2])
    with col_d:
        buf = io.BytesIO()
        metrics["df"].to_excel(buf, index=False)
        buf.seek(0)
        st.download_button("⬇ Descargar Excel Consolidado", data=buf,
                           file_name="cartera_consolidada.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)


# ─────────────────────────────────────────────
#  PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────

def render_welcome():
    st.markdown(
        f"""
        <div style='text-align:center; padding: 3rem 0 1rem;'>
            <h1 style='font-size:2.8rem; color:{COLORS["primary"]}'>💼 Dashboard de Gestión de Cartera</h1>
            <p style='color:{COLORS["muted"]}; font-size:1.1rem; max-width:600px; margin:0 auto 2rem;'>
                Análisis profesional con KPIs, RSI y predicciones.
                Carga tus dos archivos Excel para comenzar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "📊", "KPIs en Tiempo Real",     "Total cartera, cobrado, pendiente y % de cumplimiento."),
        (c2, "📈", "RSI y Series Temporales", "Análisis técnico RSI-14 con zonas de sobrecompra/sobreventa."),
        (c3, "🔮", "Predicción 30 días",       "Proyección de recuperación con regresión lineal e IC."),
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
        ("mapping", None), ("file_names", (None, None)),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    filters = render_sidebar(st.session_state.data)

    # ── Carga de los 2 archivos Excel ─────────────────────────────────
    with st.expander(
        "📂 Cargar archivos Excel",
        expanded=st.session_state.data is None,
    ):
        col_up1, col_up2 = st.columns(2)
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
                    st.error(f"❌ No se pudo leer el archivo: {e}")
        elif file_cartera or file_saldos:
            st.info("⏳ Sube los **dos** archivos para continuar.")

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
                    st.success(f"✅ Cruce completado — **{n:,}** registros consolidados.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al cruzar datos: {e}")
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
        st.info("🔍 Filtros activos — " + " · ".join(partes))

    # ── Tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "📊 Resumen General",
        "📅 Temporalidad",
        "🌊 Flujo y Proyección",
    ])
    with tab1:
        tab_resumen(metrics)
    with tab2:
        tab_temporalidad(metrics)
    with tab3:
        tab_flujo(metrics)


if __name__ == "__main__":
    main()
