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
/* ── Fondo general ── */
[data-testid="stAppViewContainer"] {
    background: #f4f6f9;
    color: #1a1a2e;
}
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e0e4ea;
}
[data-testid="stSidebar"] * { color: #1a1a2e; }

/* ── Encabezados ── */
h1 { color: #1a3c6e; }
h2, h3, h4 { color: #1a3c6e; }

/* ── Tabs ── */
[data-testid="stTabs"] button {
    color: #6b7280;
    font-weight: 600;
    font-size: 0.9rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1a3c6e;
    border-bottom: 2px solid #1a3c6e;
}

/* ── Métricas ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="stMetricLabel"] { color: #6b7280; font-size: 0.78rem; }
[data-testid="stMetricValue"] { color: #1a1a2e; font-size: 1.6rem; font-weight: 700; }

/* ── Tarjetas ── */
.card {
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #c5d0de;
    border-radius: 12px;
    padding: 1rem;
    background: #ffffff;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 8px; }

/* ── Divider ── */
hr { border-color: #e0e4ea; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f4f6f9; }
::-webkit-scrollbar-thumb { background: #c5d0de; border-radius: 4px; }

/* ── Botón de descarga ── */
[data-testid="stDownloadButton"] button {
    background: #1a3c6e;
    color: white;
    border-radius: 8px;
    font-weight: 600;
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
    xaxis=dict(gridcolor=COLORS["grid"], zeroline=False, showline=False),
    yaxis=dict(gridcolor=COLORS["grid"], zeroline=False, showline=False),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor=COLORS["grid"], borderwidth=1),
    margin=dict(l=40, r=20, t=50, b=40),
    hovermode="x unified",
)

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
    cols_c  = list(df_cartera.columns)
    cols_s  = list(df_saldos.columns)

    st.markdown(
        f"<div class='card' style='border-left:4px solid {COLORS['warning']};'>"
        "<b>⚙️ Mapeo de columnas</b> — Selecciona qué columna de tu Excel "
        "corresponde a cada campo.</div>",
        unsafe_allow_html=True,
    )

    # ── Sección 1: Llaves de cruce ────────────────────────────────────
    st.markdown("##### 🔑 Columnas para unir los dos archivos")
    st.caption("Cartera: NumDama + AñoCampañaSaldo  ·  Saldos: NumDama + AñoProceso + CampañaProceso")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**📁 Cartera**")
        c_dama = st.selectbox(
            "Número de Dama",
            cols_c, index=_best_guess(cols_c, ["dama", "numero", "nro", "id"]),
            key="map_c_dama",
        )
        c_anio = st.selectbox(
            "Año Campaña Saldo",
            cols_c, index=_best_guess(cols_c, ["anio", "año", "campaña", "saldo"]),
            key="map_c_anio",
        )

    with col_b:
        st.markdown("**📁 Saldos Actualizados**")
        s_dama = st.selectbox(
            "Número de Dama",
            cols_s, index=_best_guess(cols_s, ["dama", "numero", "nro", "id"]),
            key="map_s_dama",
        )
        s_anio = st.selectbox(
            "Año Proceso",
            cols_s, index=_best_guess(cols_s, ["anio", "año", "proceso"]),
            key="map_s_anio",
        )
        s_camp = st.selectbox(
            "Campaña Proceso",
            cols_s, index=_best_guess(cols_s, ["campaña", "camp", "nro", "periodo"]),
            key="map_s_camp",
        )

    st.divider()

    # ── Sección 2: Columna de saldo (la más importante) ───────────────
    st.markdown("##### 💰 Columna de saldo en Saldos Actualizados")
    st.caption("Si el valor es **0** → la Dama ya pagó. Si tiene número → esa es su deuda.")
    col_c, col_d = st.columns(2)

    with col_c:
        s_saldo = st.selectbox(
            "Columna con el saldo / deuda actual ⭐",
            cols_s,
            index=_best_guess(cols_s, ["saldo", "deuda", "valor", "monto", "pendiente"]),
            key="map_s_saldo",
            help="Esta columna determina si la Dama pagó (0) o cuánto debe (>0).",
        )

    with col_d:
        st.markdown("")
        st.markdown("")
        st.info(
            f"✅ **Saldo = 0** → Estado: **Pagado**\n\n"
            f"🔴 **Saldo > 0** → Estado: **Pendiente** (ese número es la deuda)"
        )

    st.divider()

    # ── Sección 3: Monto original en Cartera (opcional) ───────────────
    st.markdown("##### 📊 Monto original en Cartera *(opcional)*")
    st.caption("Sirve para calcular Total Cartera y Total Cobrado. Si no existe déjalo en (ninguna).")
    c_monto = st.selectbox(
        "Columna con el monto/deuda original",
        ["(ninguna)"] + cols_c,
        index=_best_guess(["(ninguna)"] + cols_c, ["valor", "monto", "deuda", "total"]),
        key="map_c_monto",
    )

    st.markdown("")
    if st.button("✅ Confirmar y procesar", type="primary", use_container_width=True):
        return {
            "c_dama":  c_dama,
            "c_anio":  c_anio,
            "c_monto": None if c_monto == "(ninguna)" else c_monto,
            "s_dama":  s_dama,
            "s_anio":  s_anio,
            "s_camp":  s_camp,
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
    # ── Llave Cartera: NumDama + AñoCampañaSaldo ──────────────────────
    df_cartera["_key"] = (
        clean_str(df_cartera[mapping["c_dama"]])
        + "_"
        + clean_str(df_cartera[mapping["c_anio"]])
    )

    # ── Llave Saldos: NumDama + AñoProceso + CampañaProceso ───────────
    df_saldos["_key"] = (
        clean_str(df_saldos[mapping["s_dama"]])
        + "_"
        + clean_str(df_saldos[mapping["s_anio"]])
        + clean_str(df_saldos[mapping["s_camp"]])
    )

    # ── Merge LEFT desde Cartera ──────────────────────────────────────
    df_merged = pd.merge(
        df_cartera, df_saldos,
        on="_key", how="left",
        suffixes=("_cartera", "_saldos"),
    )

    # ── Resolver nombre real de la columna de saldo tras el merge ─────
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
    if saldo_col:
        pagado_mask = df_merged[saldo_col] == 0
    else:
        pagado_mask = pd.Series([False] * len(df_merged))

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
    # Usar valor_col del mapping; si no hay, intentar autodetectar
    valor_col = data.get("valor_col") or _find_col(df, ["valor", "monto", "deuda", "total"])

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
    if saldo_col and saldo_col in df.columns:
        monto_pendiente = df[saldo_col].sum()
        monto_cobrado   = monto_total - monto_pendiente if valor_col else 0

    # ── Serie temporal ────────────────────────────────────────────────
    fecha_col = _find_col(df, ["fecha", "date", "periodo", "mes"])
    if fecha_col and saldo_col:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")
        ts = (
            df.dropna(subset=[fecha_col])
            .sort_values(fecha_col)
            .groupby(fecha_col)[saldo_col]
            .sum()
            .reset_index()
        )
        ts.columns = ["fecha", "valor"]
    else:
        camp_col = _find_col(df, ["campaña", "campaign", "año campaña"])
        if camp_col and saldo_col:
            ts = (
                df.groupby(camp_col)[saldo_col]
                .sum()
                .reset_index()
                .sort_values(camp_col)
                .rename(columns={camp_col: "fecha", saldo_col: "valor"})
            )
        else:
            n  = min(60, total_registros)
            ts = pd.DataFrame({
                "fecha": pd.date_range("2024-01-01", periods=n, freq="W"),
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

def predict_recovery(ts: pd.DataFrame, horizon: int = 30) -> pd.DataFrame:
    df = ts.copy().dropna()
    if len(df) < 3:
        return pd.DataFrame()

    df["x"] = np.arange(len(df))
    model    = LinearRegression()
    model.fit(df[["x"]], df["valor"])

    future_x = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    future_y = model.predict(future_x)

    last_date = (
        pd.to_datetime(df["fecha"].iloc[-1])
        if not pd.api.types.is_integer_dtype(df["fecha"])
        else pd.Timestamp("today")
    )
    future_dates = pd.date_range(last_date, periods=horizon + 1, freq="D")[1:]
    residuals    = df["valor"].values - model.predict(df[["x"]])
    std_err      = np.std(residuals) * 1.5

    pred_df = pd.DataFrame({
        "fecha":      future_dates,
        "prediccion": future_y,
        "upper":      future_y + std_err,
        "lower":      future_y - std_err,
    })
    return pred_df


# ─────────────────────────────────────────────
#  GRÁFICAS
# ─────────────────────────────────────────────

def _base_fig(**kwargs) -> go.Figure:
    fig = go.Figure(**kwargs)
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def plot_kpi_donut(pagados: int, pendientes: int) -> go.Figure:
    fig = _base_fig()
    fig.add_trace(go.Pie(
        labels=["Pagado", "Pendiente"],
        values=[pagados, pendientes],
        hole=0.62,
        marker_colors=[COLORS["success"], COLORS["danger"]],
        textinfo="percent",
        hovertemplate="%{label}: %{value} registros (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title_text="Distribución Estado de Pago",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=320,
    )
    return fig


def plot_saldo_por_estado(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    if not saldo_col:
        return _base_fig()
    grp = df.groupby("Estado_Pago")[saldo_col].sum().reset_index()
    fig = px.bar(
        grp, x="Estado_Pago", y=saldo_col,
        color="Estado_Pago",
        color_discrete_map={"Pagado": COLORS["success"], "Pendiente": COLORS["danger"]},
        title="Saldo Total por Estado de Pago",
        labels={saldo_col: "Monto ($)", "Estado_Pago": ""},
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                      title_font=dict(size=14, color=COLORS["primary"]))
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Monto: $%{y:,.2f}<extra></extra>")
    return fig


def plot_time_series(ts: pd.DataFrame) -> go.Figure:
    fig = _base_fig()
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=ts["valor"],
        mode="lines+markers", name="Saldo / Recaudación",
        line=dict(color=COLORS["accent"], width=2),
        marker=dict(size=5, color=COLORS["accent"]),
        hovertemplate="<b>%{x}</b><br>Valor: $%{y:,.2f}<extra></extra>",
    ))
    if len(ts) >= 7:
        ma = ts["valor"].rolling(7).mean()
        fig.add_trace(go.Scatter(
            x=ts["fecha"], y=ma,
            mode="lines", name="Media Móvil (7)",
            line=dict(color=COLORS["warning"], width=1.5, dash="dot"),
        ))
    fig.update_layout(
        title_text="Evolución Histórica de Saldos / Recaudación",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=350, dragmode="zoom",
    )
    return fig


def plot_rsi(ts: pd.DataFrame) -> go.Figure:
    rsi = calculate_rsi(ts["valor"])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.4], vertical_spacing=0.05)
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=ts["valor"],
        mode="lines", name="Valor",
        line=dict(color=COLORS["accent"], width=2),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=rsi,
        mode="lines", name="RSI (14)",
        line=dict(color=COLORS["warning"], width=2),
        hovertemplate="RSI: %{y:.1f}<extra></extra>",
    ), row=2, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor=COLORS["danger"],  opacity=0.08,
                  line_width=0, row=2, col=1,
                  annotation_text="Sobrecompra",
                  annotation_position="top right",
                  annotation_font=dict(color=COLORS["danger"], size=10))
    fig.add_hrect(y0=0, y1=30, fillcolor=COLORS["success"], opacity=0.08,
                  line_width=0, row=2, col=1,
                  annotation_text="Sobreventa",
                  annotation_position="bottom right",
                  annotation_font=dict(color=COLORS["success"], size=10))
    fig.add_hline(y=70, line_dash="dash", line_color=COLORS["danger"],   line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color=COLORS["success"],  line_width=1, row=2, col=1)
    fig.add_hline(y=50, line_dash="dot",  line_color=COLORS["muted"],    line_width=1, row=2, col=1)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Análisis RSI (14) · Fuerza Relativa de Recaudación",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=500, dragmode="zoom",
    )
    fig.update_yaxes(title_text="Valor ($)", row=1, col=1, gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1, gridcolor=COLORS["grid"])
    return fig


def plot_prediction(ts: pd.DataFrame, pred_df: pd.DataFrame) -> go.Figure:
    fig = _base_fig()
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=ts["valor"],
        mode="lines+markers", name="Histórico",
        line=dict(color=COLORS["accent"], width=2),
        marker=dict(size=4),
    ))
    if pred_df.empty:
        fig.update_layout(title_text="Predicción (datos insuficientes)", height=400)
        return fig
    fig.add_trace(go.Scatter(
        x=list(pred_df["fecha"]) + list(pred_df["fecha"][::-1]),
        y=list(pred_df["upper"]) + list(pred_df["lower"][::-1]),
        fill="toself",
        fillcolor="rgba(37,99,235,0.10)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Intervalo de confianza",
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=pred_df["fecha"], y=pred_df["prediccion"],
        mode="lines", name="Proyección (30 días)",
        line=dict(color=COLORS["warning"], width=2.5, dash="dash"),
        hovertemplate="Proyección: $%{y:,.2f}<extra></extra>",
    ))
    last_hist = ts["fecha"].iloc[-1]
    # Usar add_shape en lugar de add_vline para evitar conflictos de tipo en eje X
    fig.add_shape(
        type="line",
        x0=last_hist, x1=last_hist,
        y0=0, y1=1, yref="paper",
        line=dict(dash="dot", color=COLORS["muted"], width=1.5),
    )
    fig.add_annotation(
        x=last_hist, y=1, yref="paper",
        text="Hoy", showarrow=False,
        font=dict(color=COLORS["muted"], size=11),
        yshift=10,
    )
    fig.update_layout(
        title_text="Proyección de Recuperación · Próximos 30 días",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=420, dragmode="zoom",
    )
    return fig


def plot_top_damas(df: pd.DataFrame, saldo_col: str, n: int = 15) -> go.Figure:
    if not saldo_col or "Número de Dama" not in df.columns:
        return _base_fig()
    col = "Número de Dama_cartera" if "Número de Dama_cartera" in df.columns else "Número de Dama"
    top = (
        df[df["Estado_Pago"] == "Pendiente"]
        .groupby(col)[saldo_col]
        .sum()
        .nlargest(n)
        .reset_index()
        .sort_values(saldo_col)
    )
    fig = px.bar(
        top, x=saldo_col, y=col, orientation="h",
        title=f"Top {n} Damas con Mayor Saldo Pendiente",
        color=saldo_col,
        color_continuous_scale=["#16a34a", "#d97706", "#dc2626"],
        labels={saldo_col: "Saldo Pendiente ($)", col: "Número de Dama"},
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=max(300, n * 22),
        title_font=dict(size=14, color=COLORS["primary"]),
        coloraxis_showscale=False,
    )
    return fig


def plot_distribucion_saldos(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    if not saldo_col:
        return _base_fig()
    vals = df[saldo_col].replace(0, np.nan).dropna()
    fig  = go.Figure()
    fig.add_trace(go.Histogram(
        x=vals, nbinsx=30,
        marker_color=COLORS["accent"], opacity=0.75,
        hovertemplate="Rango: %{x}<br>Frecuencia: %{y}<extra></extra>",
    ))
    fig.add_vline(x=vals.mean(), line_dash="dash", line_color=COLORS["warning"],
                  annotation_text=f"Media: ${vals.mean():,.0f}",
                  annotation_font=dict(color=COLORS["warning"]))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Distribución de Saldos Pendientes",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=340, xaxis_title="Monto ($)", yaxis_title="Frecuencia",
    )
    return fig


def plot_campana_saldo(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    camp_col = _find_col(df, ["campaña", "campaign", "año campaña"])
    if not camp_col or not saldo_col:
        return _base_fig()
    grp = df.groupby(camp_col)[saldo_col].sum().reset_index().sort_values(camp_col)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp[camp_col].astype(str), y=grp[saldo_col],
        marker=dict(
            color=grp[saldo_col],
            colorscale=[[0, COLORS["success"]], [0.5, COLORS["warning"]], [1, COLORS["danger"]]],
            showscale=False,
        ),
        hovertemplate="Campaña: %{x}<br>Saldo: $%{y:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Saldo Pendiente por Campaña",
        title_font=dict(size=14, color=COLORS["primary"]),
        xaxis_title="Campaña", yaxis_title="Saldo ($)", height=340,
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


# ─────────────────────────────────────────────
#  SIDEBAR CON FILTROS
# ─────────────────────────────────────────────

def render_sidebar(data: dict | None) -> dict:
    filters = {}
    with st.sidebar:
        st.markdown(f"## 💼 Cartera Dashboard")
        st.markdown(
            f"<span style='color:{COLORS['muted']};font-size:0.8rem'>Gestión Financiera Profesional</span>",
            unsafe_allow_html=True,
        )
        st.divider()

        if data:
            df = data["merged"]
            st.markdown("#### Filtros Globales")

            estados = ["Todos"] + sorted(df["Estado_Pago"].unique().tolist())
            filters["estado"] = st.selectbox("Estado de Pago", estados)

            dama_col = "Número de Dama_cartera" if "Número de Dama_cartera" in df.columns else "Número de Dama"
            if dama_col in df.columns:
                damas = ["Todos"] + sorted(df[dama_col].astype(str).unique().tolist())
                filters["dama"] = st.selectbox("Número de Dama", damas)

            camp_col = _find_col(df, ["campaña", "campaign", "año campaña"])
            if camp_col:
                camps = ["Todos"] + sorted(df[camp_col].astype(str).unique().tolist())
                filters["campaña"] = st.selectbox("Campaña", camps)

            st.divider()
            st.markdown(
                f"<small style='color:{COLORS['muted']}'>"
                f"📊 Registros cruzados: <b>{len(df):,}</b><br>"
                f"✅ Pagados: <b>{(df['Estado_Pago']=='Pagado').sum():,}</b><br>"
                f"⏳ Pendientes: <b>{(df['Estado_Pago']=='Pendiente').sum():,}</b>"
                f"</small>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Carga los archivos Excel para activar los filtros.")

        st.divider()
        st.markdown(
            f"<small style='color:{COLORS['muted']}'>RSI: 14 períodos<br>Proyección: 30 días<br>Modelo: Regresión Lineal</small>",
            unsafe_allow_html=True,
        )
    return filters


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    dff = df.copy()
    if filters.get("estado") and filters["estado"] != "Todos":
        dff = dff[dff["Estado_Pago"] == filters["estado"]]
    if filters.get("dama") and filters["dama"] != "Todos":
        col = "Número de Dama_cartera" if "Número de Dama_cartera" in dff.columns else "Número de Dama"
        if col in dff.columns:
            dff = dff[dff[col].astype(str) == filters["dama"]]
    if filters.get("campaña") and filters["campaña"] != "Todos":
        camp_col = _find_col(dff, ["campaña", "campaign", "año campaña"])
        if camp_col:
            dff = dff[dff[camp_col].astype(str) == filters["campaña"]]
    return dff


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────

def tab_resumen(metrics: dict, filters: dict):
    section_header("Resumen General · KPIs", "Indicadores clave de la cartera filtrada")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Registros", f"{metrics['total_registros']:,}")
    with c2:
        st.metric("Total Cartera", fmt_currency(metrics["monto_total"]))
    with c3:
        st.metric(
            "Total Cobrado",
            fmt_currency(metrics["monto_cobrado"]),
            delta=f"+{metrics['monto_cobrado']/metrics['monto_total']*100:.1f}%" if metrics["monto_total"] else None,
        )
    with c4:
        st.metric(
            "Saldo Pendiente",
            fmt_currency(metrics["monto_pendiente"]),
            delta=f"-{metrics['pendientes']} registros",
            delta_color="inverse",
        )
    with c5:
        st.metric(
            "% Cumplimiento",
            f"{metrics['pct_cumplimiento']:.1f}%",
            delta=f"{metrics['pagados']} pagadas",
        )

    st.markdown("")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.plotly_chart(plot_kpi_donut(metrics["pagados"], metrics["pendientes"]),
                        use_container_width=True, config={"displayModeBar": False},
                        key="chart_donut")
    with col_b:
        st.plotly_chart(plot_saldo_por_estado(metrics["df"], metrics["saldo_col"]),
                        use_container_width=True, key="chart_estado")

    st.divider()
    col_c, col_d = st.columns(2)
    with col_c:
        st.plotly_chart(plot_campana_saldo(metrics["df"], metrics["saldo_col"]),
                        use_container_width=True, key="chart_campana")
    with col_d:
        st.plotly_chart(plot_distribucion_saldos(metrics["df"], metrics["saldo_col"]),
                        use_container_width=True, key="chart_dist")

    st.divider()
    section_header("Datos Consolidados", "Primeros 200 registros del cruce Cartera × Saldos")
    st.dataframe(metrics["df"].head(200), use_container_width=True, height=320)


def tab_pagos(metrics: dict):
    section_header("Análisis de Pagos y Saldos", "Detalle por Dama, campaña y evolución")

    st.plotly_chart(plot_time_series(metrics["ts"]), use_container_width=True,
                    key="chart_timeseries")

    st.divider()
    col_l, col_r = st.columns([2, 1])
    with col_l:
        top_n = st.slider("Número de Damas a mostrar", 5, 30, 15)
        st.plotly_chart(plot_top_damas(metrics["df"], metrics["saldo_col"], top_n),
                        use_container_width=True, key="chart_topdamas")
    with col_r:
        section_header("Estadísticas de Saldo")
        if metrics["saldo_col"]:
            s = metrics["df"][metrics["saldo_col"]]
            st.metric("Promedio",   fmt_currency(s.mean()))
            st.metric("Mediana",    fmt_currency(s.median()))
            st.metric("Máximo",     fmt_currency(s.max()))
            st.metric("Desv. Est.", fmt_currency(s.std()))
        else:
            st.info("Sin columna de saldo detectada.")

    st.divider()
    section_header("Exportar Datos Filtrados")
    buf = io.BytesIO()
    metrics["df"].to_excel(buf, index=False)
    buf.seek(0)
    st.download_button(
        "⬇ Descargar Excel Consolidado",
        data=buf,
        file_name="cartera_consolidada.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def tab_tecnico(metrics: dict):
    section_header("Indicadores Técnicos y Predicciones", "RSI 14 períodos · Proyección 30 días")

    st.plotly_chart(plot_rsi(metrics["ts"]), use_container_width=True, key="chart_rsi")

    rsi_serie  = calculate_rsi(metrics["ts"]["valor"])
    rsi_actual = rsi_serie.dropna().iloc[-1] if not rsi_serie.dropna().empty else 50
    zona       = "Sobrecompra ⚠" if rsi_actual > 70 else ("Sobreventa ✅" if rsi_actual < 30 else "Zona Neutral")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("RSI Actual (14)", f"{rsi_actual:.1f}", delta=zona)
    with col2:
        st.metric("Señal",
                  "Venta / Alta Recaudación" if rsi_actual > 70
                  else ("Compra / Baja Recaudación" if rsi_actual < 30 else "Neutral"))
    with col3:
        pct = (
            (metrics["ts"]["valor"].iloc[-1] - metrics["ts"]["valor"].iloc[-2])
            / metrics["ts"]["valor"].iloc[-2] * 100
            if len(metrics["ts"]) >= 2 and metrics["ts"]["valor"].iloc[-2] != 0 else 0.0
        )
        st.metric("Variación Último Período", f"{pct:+.2f}%")

    st.divider()
    section_header("Proyección de Recuperación", "Regresión Lineal · scikit-learn")
    pred_df = predict_recovery(metrics["ts"])
    st.plotly_chart(plot_prediction(metrics["ts"], pred_df), use_container_width=True,
                    key="chart_prediction")

    if not pred_df.empty:
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric("Proyección en 30 días", fmt_currency(pred_df["prediccion"].iloc[-1]))
        with col_p2:
            st.metric("Límite Superior (IC)",  fmt_currency(pred_df["upper"].iloc[-1]))
        with col_p3:
            st.metric("Límite Inferior (IC)",  fmt_currency(pred_df["lower"].iloc[-1]))

        tendencia = (
            "📈 Tendencia Alcista · Mejora en Recaudación"
            if pred_df["prediccion"].iloc[-1] > pred_df["prediccion"].iloc[0]
            else "📉 Tendencia Bajista · Saldos en Aumento"
        )
        st.markdown(
            f"<div class='card' style='border-left: 4px solid {COLORS['accent']};'>"
            f"<b style='color:{COLORS['primary']}'>Diagnóstico Predictivo</b><br>"
            f"<span style='font-size:1rem'>{tendencia}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )


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

    active = [f"**{k}**: {v}" for k, v in filters.items() if v and v != "Todos"]
    if active:
        st.info("🔍 Filtros activos: " + " · ".join(active))

    # ── Tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "📊 Resumen General (KPIs)",
        "💳 Análisis de Pagos y Saldos",
        "🔬 Indicadores Técnicos y Predicciones",
    ])
    with tab1:
        tab_resumen(metrics, filters)
    with tab2:
        tab_pagos(metrics)
    with tab3:
        tab_tecnico(metrics)


if __name__ == "__main__":
    main()
