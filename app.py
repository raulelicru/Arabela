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
#  ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* ── Fondo general ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    color: #e6edf3;
}
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}
/* ── Encabezados ── */
h1, h2, h3, h4 { color: #58a6ff; }
/* ── Tabs ── */
[data-testid="stTabs"] button {
    color: #8b949e;
    font-weight: 600;
    font-size: 0.9rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
/* ── Métricas ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"]  { color: #8b949e; font-size: 0.78rem; }
[data-testid="stMetricValue"]  { color: #e6edf3; font-size: 1.6rem; font-weight: 700; }
[data-testid="stMetricDelta"]  { font-size: 0.78rem; }
/* ── Tarjetas de sección ── */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
/* ── Barra de progreso personalizada ── */
.progress-bar-bg {
    background: #21262d;
    border-radius: 999px;
    height: 8px;
    width: 100%;
}
.progress-bar-fill {
    background: linear-gradient(90deg, #238636, #2ea043);
    border-radius: 999px;
    height: 8px;
}
/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #30363d;
    border-radius: 12px;
    padding: 1rem;
}
/* ── Divider ── */
hr { border-color: #21262d; }
/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PALETA DE COLORES (PLOTLY)
# ─────────────────────────────────────────────
COLORS = {
    "primary":   "#58a6ff",
    "success":   "#2ea043",
    "warning":   "#d29922",
    "danger":    "#f85149",
    "muted":     "#8b949e",
    "bg":        "#161b22",
    "grid":      "#21262d",
    "text":      "#e6edf3",
    "gradient":  ["#58a6ff", "#3fb950", "#d29922", "#f85149", "#bc8cff"],
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor=COLORS["bg"],
    plot_bgcolor=COLORS["bg"],
    font=dict(color=COLORS["text"], family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor=COLORS["grid"], zeroline=False, showline=False),
    yaxis=dict(gridcolor=COLORS["grid"], zeroline=False, showline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["grid"]),
    margin=dict(l=40, r=20, t=50, b=40),
    hovermode="x unified",
)

# ─────────────────────────────────────────────
#  FUNCIONES DE CARGA Y LIMPIEZA
# ─────────────────────────────────────────────

REQUIRED_CARTERA = ["Número de Dama", "Año Campaña Saldo"]
REQUIRED_SALDOS  = ["Número de Dama", "Año Proceso", "Campaña Proceso"]


def clean_str(series: pd.Series) -> pd.Series:
    """Convierte a string y elimina espacios."""
    return series.astype(str).str.strip()


def load_and_clean_data(uploaded_file) -> dict[str, pd.DataFrame]:
    """
    Lee el archivo Excel, detecta las hojas de Cartera y Saldos,
    aplica las reglas de concatenación y retorna un dict con las DFs.
    """
    xls = pd.ExcelFile(uploaded_file)
    sheets = xls.sheet_names

    # ── Detección automática de pestañas ──────────────────────────────
    cartera_sheet = next(
        (s for s in sheets if "cartera" in s.lower()), sheets[0]
    )
    saldos_sheet = next(
        (s for s in sheets if "saldo" in s.lower()),
        sheets[1] if len(sheets) > 1 else sheets[0],
    )

    df_cartera = xls.parse(cartera_sheet)
    df_saldos  = xls.parse(saldos_sheet)

    # ── Normalizar nombres de columnas ────────────────────────────────
    df_cartera.columns = [c.strip() for c in df_cartera.columns]
    df_saldos.columns  = [c.strip() for c in df_saldos.columns]

    # ── Validación de columnas requeridas ─────────────────────────────
    missing_c = [c for c in REQUIRED_CARTERA if c not in df_cartera.columns]
    missing_s = [c for c in REQUIRED_SALDOS  if c not in df_saldos.columns]
    if missing_c:
        raise ValueError(f"Columnas faltantes en Cartera: {missing_c}")
    if missing_s:
        raise ValueError(f"Columnas faltantes en Saldos: {missing_s}")

    # ── Regla 1: Llave de Cartera ─────────────────────────────────────
    df_cartera["_key"] = (
        clean_str(df_cartera["Número de Dama"])
        + "_"
        + clean_str(df_cartera["Año Campaña Saldo"])
    )

    # ── Regla 2: Llave de Saldos ──────────────────────────────────────
    df_saldos["_key"] = (
        clean_str(df_saldos["Número de Dama"])
        + "_"
        + clean_str(df_saldos["Año Proceso"])
        + clean_str(df_saldos["Campaña Proceso"])
    )

    # ── Cruce (merge) ─────────────────────────────────────────────────
    df_merged = pd.merge(
        df_cartera,
        df_saldos,
        on="_key",
        how="left",
        suffixes=("_cartera", "_saldos"),
    )

    # ── Columna de estado de pago ─────────────────────────────────────
    saldo_col = _find_col(df_merged, ["saldo actualizado", "saldo_actualizado", "saldo"])
    estado_col = _find_col(df_merged, ["estado", "status", "liquidado"])

    if saldo_col:
        df_merged[saldo_col] = pd.to_numeric(df_merged[saldo_col], errors="coerce").fillna(0)
        pagado_mask = df_merged[saldo_col] == 0
    else:
        pagado_mask = pd.Series([False] * len(df_merged))

    if estado_col:
        pagado_mask |= df_merged[estado_col].astype(str).str.lower().str.contains(
            "liquid|pagad|paid|cerrad", na=False
        )

    df_merged["Estado_Pago"] = np.where(pagado_mask, "Pagado", "Pendiente")

    return {
        "cartera": df_cartera,
        "saldos":  df_saldos,
        "merged":  df_merged,
        "saldo_col":  saldo_col,
        "estado_col": estado_col,
        "cartera_sheet": cartera_sheet,
        "saldos_sheet":  saldos_sheet,
    }


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Busca la primera columna que coincida (case-insensitive) con la lista."""
    lower_cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        for key, real in lower_cols.items():
            if cand in key:
                return real
    return None


# ─────────────────────────────────────────────
#  CÁLCULO DE MÉTRICAS
# ─────────────────────────────────────────────

def calculate_metrics(data: dict) -> dict:
    df = data["merged"]
    saldo_col = data["saldo_col"]

    total_registros = len(df)
    pagados   = (df["Estado_Pago"] == "Pagado").sum()
    pendientes = total_registros - pagados
    pct_cumplimiento = pagados / total_registros * 100 if total_registros else 0

    monto_total     = 0.0
    monto_pendiente = 0.0
    monto_cobrado   = 0.0

    # ── Columna de valor original (cartera) ──────────────────────────
    valor_col = _find_col(df, ["valor", "monto", "deuda", "total"])

    if valor_col:
        df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce").fillna(0)
        monto_total = df[valor_col].sum()

    if saldo_col:
        monto_pendiente = df[saldo_col].sum()
        monto_cobrado   = monto_total - monto_pendiente if valor_col else 0

    # ── Serie temporal (para RSI y predicciones) ──────────────────────
    fecha_col = _find_col(df, ["fecha", "date", "periodo", "mes"])
    if fecha_col:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")
        ts = (
            df.dropna(subset=[fecha_col])
            .sort_values(fecha_col)
            .groupby(fecha_col)[saldo_col if saldo_col else df.columns[0]]
            .sum()
            .reset_index()
        )
        ts.columns = ["fecha", "valor"]
    else:
        # Serie sintética basada en índice ordinal de campaña
        camp_col = _find_col(df, ["campaña", "campaign", "periodo", "año"])
        if camp_col and saldo_col:
            ts = (
                df.groupby(camp_col)[saldo_col]
                .sum()
                .reset_index()
                .sort_values(camp_col)
                .rename(columns={camp_col: "fecha", saldo_col: "valor"})
            )
        else:
            # Último recurso: serie numérica progresiva
            n = min(60, total_registros)
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
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period).mean()
    rs  = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ─────────────────────────────────────────────
#  PREDICCIÓN LINEAL
# ─────────────────────────────────────────────

def predict_recovery(ts: pd.DataFrame, horizon: int = 30) -> pd.DataFrame:
    """Regresión lineal sobre la serie temporal; proyecta `horizon` días."""
    df = ts.copy().dropna()
    if len(df) < 3:
        return pd.DataFrame()

    df["x"] = np.arange(len(df))
    X = df["x"].values.reshape(-1, 1)
    y = df["valor"].values

    model = LinearRegression()
    model.fit(X, y)

    future_x = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    future_y = model.predict(future_x)

    last_date = (
        pd.to_datetime(df["fecha"].iloc[-1])
        if not pd.api.types.is_integer_dtype(df["fecha"])
        else pd.Timestamp("today")
    )
    future_dates = pd.date_range(last_date, periods=horizon + 1, freq="D")[1:]

    pred_df = pd.DataFrame({"fecha": future_dates, "prediccion": future_y})

    # Banda de confianza (±1.5 std del residuo)
    residuals = y - model.predict(X)
    std_err   = np.std(residuals) * 1.5
    pred_df["upper"] = pred_df["prediccion"] + std_err
    pred_df["lower"] = pred_df["prediccion"] - std_err

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
        textfont=dict(size=13, color=COLORS["text"]),
        hovertemplate="%{label}: %{value} registros (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title_text="Distribución de Estado de Pago",
        title_font=dict(size=14, color=COLORS["primary"]),
        showlegend=True,
        height=320,
    )
    return fig


def plot_saldo_por_estado(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    if not saldo_col:
        return _base_fig()
    grp = df.groupby("Estado_Pago")[saldo_col].sum().reset_index()
    fig = px.bar(
        grp,
        x="Estado_Pago",
        y=saldo_col,
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
        mode="lines+markers",
        name="Saldo / Recaudación",
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=5),
        hovertemplate="<b>%{x}</b><br>Valor: $%{y:,.2f}<extra></extra>",
    ))
    # Media móvil 7 períodos
    if len(ts) >= 7:
        ma = ts["valor"].rolling(7).mean()
        fig.add_trace(go.Scatter(
            x=ts["fecha"], y=ma,
            mode="lines",
            name="Media Móvil (7)",
            line=dict(color=COLORS["warning"], width=1.5, dash="dot"),
            hovertemplate="MA7: $%{y:,.2f}<extra></extra>",
        ))
    fig.update_layout(
        title_text="Evolución Histórica de Saldos / Recaudación",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=350,
        dragmode="zoom",
    )
    return fig


def plot_rsi(ts: pd.DataFrame) -> go.Figure:
    rsi = calculate_rsi(ts["valor"])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.4], vertical_spacing=0.05)

    # ── Precio / saldo ────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=ts["valor"],
        mode="lines", name="Valor",
        line=dict(color=COLORS["primary"], width=2),
        hovertemplate="Valor: $%{y:,.2f}<extra></extra>",
    ), row=1, col=1)

    # ── RSI ───────────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=rsi,
        mode="lines", name="RSI (14)",
        line=dict(color=COLORS["warning"], width=2),
        hovertemplate="RSI: %{y:.1f}<extra></extra>",
    ), row=2, col=1)

    # Zonas sombreadas
    x_all = list(ts["fecha"])
    fig.add_hrect(y0=70, y1=100, fillcolor=COLORS["danger"],   opacity=0.12,
                  line_width=0, row=2, col=1, annotation_text="Sobrecompra",
                  annotation_position="top right",
                  annotation_font=dict(color=COLORS["danger"], size=10))
    fig.add_hrect(y0=0,  y1=30,  fillcolor=COLORS["success"],  opacity=0.12,
                  line_width=0, row=2, col=1, annotation_text="Sobreventa",
                  annotation_position="bottom right",
                  annotation_font=dict(color=COLORS["success"], size=10))
    fig.add_hline(y=70, line_dash="dash", line_color=COLORS["danger"],
                  line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color=COLORS["success"],
                  line_width=1, row=2, col=1)
    fig.add_hline(y=50, line_dash="dot",  line_color=COLORS["muted"],
                  line_width=1, row=2, col=1)

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Análisis RSI (14) · Fuerza Relativa de Recaudación",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=500,
        dragmode="zoom",
        showlegend=True,
    )
    fig.update_yaxes(title_text="Valor ($)", row=1, col=1,
                     gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1,
                     gridcolor=COLORS["grid"])
    return fig


def plot_prediction(ts: pd.DataFrame, pred_df: pd.DataFrame) -> go.Figure:
    fig = _base_fig()
    # Histórico
    fig.add_trace(go.Scatter(
        x=ts["fecha"], y=ts["valor"],
        mode="lines+markers", name="Histórico",
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=4),
        hovertemplate="Histórico: $%{y:,.2f}<extra></extra>",
    ))
    if pred_df.empty:
        fig.update_layout(title_text="Predicción (datos insuficientes)",
                          height=400, **PLOTLY_LAYOUT)
        return fig

    # Banda de confianza
    fig.add_trace(go.Scatter(
        x=list(pred_df["fecha"]) + list(pred_df["fecha"][::-1]),
        y=list(pred_df["upper"]) + list(pred_df["lower"][::-1]),
        fill="toself",
        fillcolor="rgba(88,166,255,0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Intervalo de confianza",
        hoverinfo="skip",
    ))
    # Línea de predicción
    fig.add_trace(go.Scatter(
        x=pred_df["fecha"], y=pred_df["prediccion"],
        mode="lines", name="Proyección (30 días)",
        line=dict(color=COLORS["warning"], width=2.5, dash="dash"),
        hovertemplate="Proyección: $%{y:,.2f}<extra></extra>",
    ))
    # Línea vertical de separación
    last_hist = ts["fecha"].iloc[-1] if not pd.api.types.is_integer_dtype(ts["fecha"]) else pd.Timestamp("today")
    fig.add_vline(x=last_hist, line_dash="dot", line_color=COLORS["muted"],
                  annotation_text="Hoy", annotation_position="top",
                  annotation_font=dict(color=COLORS["muted"]))

    fig.update_layout(
        title_text="Proyección de Recuperación de Saldos · Próximos 30 días",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=420,
        dragmode="zoom",
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
        top, x=saldo_col, y=col,
        orientation="h",
        title=f"Top {n} Damas con Mayor Saldo Pendiente",
        color=saldo_col,
        color_continuous_scale=["#238636", "#d29922", "#f85149"],
        labels={saldo_col: "Saldo Pendiente ($)", col: "Número de Dama"},
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=max(300, n * 22),
        title_font=dict(size=14, color=COLORS["primary"]),
        coloraxis_showscale=False,
    )
    fig.update_traces(hovertemplate="Dama: %{y}<br>Saldo: $%{x:,.2f}<extra></extra>")
    return fig


def plot_distribucion_saldos(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    if not saldo_col:
        return _base_fig()
    vals = df[saldo_col].replace(0, np.nan).dropna()
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=vals,
        nbinsx=30,
        marker_color=COLORS["primary"],
        opacity=0.8,
        hovertemplate="Rango: %{x}<br>Frecuencia: %{y}<extra></extra>",
    ))
    fig.add_vline(x=vals.mean(), line_dash="dash", line_color=COLORS["warning"],
                  annotation_text=f"Media: ${vals.mean():,.0f}",
                  annotation_font=dict(color=COLORS["warning"]))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title_text="Distribución de Saldos Pendientes",
        title_font=dict(size=14, color=COLORS["primary"]),
        height=340,
        xaxis_title="Monto ($)",
        yaxis_title="Frecuencia",
    )
    return fig


def plot_campana_saldo(df: pd.DataFrame, saldo_col: str) -> go.Figure:
    """Saldo acumulado por campaña."""
    camp_col = _find_col(df, ["campaña", "campaign", "año campaña"])
    if not camp_col or not saldo_col:
        return _base_fig()
    grp = df.groupby(camp_col)[saldo_col].sum().reset_index().sort_values(camp_col)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp[camp_col].astype(str),
        y=grp[saldo_col],
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
        xaxis_title="Campaña",
        yaxis_title="Saldo ($)",
        height=340,
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
        st.markdown(f"<span style='color:{COLORS['muted']};font-size:0.85rem'>{subtitle}</span>",
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar(data: dict | None) -> dict:
    """Retorna filtros activos."""
    filters = {}
    with st.sidebar:
        st.markdown(f"## 💼 Cartera Dashboard")
        st.markdown(f"<span style='color:{COLORS['muted']};font-size:0.8rem'>Gestión Financiera Profesional</span>",
                    unsafe_allow_html=True)
        st.divider()

        if data:
            df = data["merged"]
            st.markdown("#### Filtros Globales")

            # Filtro por Estado de Pago
            estados = ["Todos"] + sorted(df["Estado_Pago"].unique().tolist())
            filters["estado"] = st.selectbox("Estado de Pago", estados)

            # Filtro por Número de Dama
            dama_col = "Número de Dama_cartera" if "Número de Dama_cartera" in df.columns else "Número de Dama"
            if dama_col in df.columns:
                damas = ["Todos"] + sorted(df[dama_col].astype(str).unique().tolist())
                filters["dama"] = st.selectbox(
                    "Número de Dama",
                    damas,
                    help="Selecciona una Dama para enfocar el análisis completo.",
                )

            # Filtro por Campaña
            camp_col = _find_col(df, ["campaña", "campaign", "año campaña"])
            if camp_col:
                camps = ["Todos"] + sorted(df[camp_col].astype(str).unique().tolist())
                filters["campaña"] = st.selectbox("Campaña", camps)

            st.divider()
            st.markdown(f"#### Información del Archivo")
            st.markdown(
                f"<small style='color:{COLORS['muted']}'>"
                f"🗂 Hoja Cartera: **{data['cartera_sheet']}**<br>"
                f"🗂 Hoja Saldos: **{data['saldos_sheet']}**<br>"
                f"📊 Registros cruzados: **{len(df):,}**"
                f"</small>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Carga un archivo Excel para activar los filtros.")

        st.divider()
        st.markdown(
            f"<small style='color:{COLORS['muted']}'>RSI Período: 14 · Proyección: 30 días<br>"
            f"Modelo: Regresión Lineal (scikit-learn)</small>",
            unsafe_allow_html=True,
        )
    return filters


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Aplica filtros del sidebar sobre el DataFrame consolidado."""
    dff = df.copy()
    if filters.get("estado") and filters["estado"] != "Todos":
        dff = dff[dff["Estado_Pago"] == filters["estado"]]
    if filters.get("dama") and filters["dama"] != "Todos":
        dama_col = "Número de Dama_cartera" if "Número de Dama_cartera" in dff.columns else "Número de Dama"
        if dama_col in dff.columns:
            dff = dff[dff[dama_col].astype(str) == filters["dama"]]
    if filters.get("campaña") and filters["campaña"] != "Todos":
        camp_col = _find_col(dff, ["campaña", "campaign", "año campaña"])
        if camp_col:
            dff = dff[dff[camp_col].astype(str) == filters["campaña"]]
    return dff


# ─────────────────────────────────────────────
#  TABS PRINCIPALES
# ─────────────────────────────────────────────

def tab_resumen(metrics: dict, filters: dict):
    section_header(
        "Resumen General · KPIs",
        "Indicadores clave de la cartera filtrada",
    )

    # ── Fila de KPIs ──────────────────────────────────────────────────
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
            "% Cumplimiento Damas",
            f"{metrics['pct_cumplimiento']:.1f}%",
            delta=f"{metrics['pagados']} pagadas",
        )

    st.markdown("")

    # ── Gráficas ──────────────────────────────────────────────────────
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.plotly_chart(
            plot_kpi_donut(metrics["pagados"], metrics["pendientes"]),
            use_container_width=True, config={"displayModeBar": False},
        )
    with col_b:
        st.plotly_chart(
            plot_saldo_por_estado(metrics["df"], metrics["saldo_col"]),
            use_container_width=True,
        )

    st.divider()
    col_c, col_d = st.columns(2)
    with col_c:
        st.plotly_chart(
            plot_campana_saldo(metrics["df"], metrics["saldo_col"]),
            use_container_width=True,
        )
    with col_d:
        st.plotly_chart(
            plot_distribucion_saldos(metrics["df"], metrics["saldo_col"]),
            use_container_width=True,
        )

    # ── Tabla resumen ─────────────────────────────────────────────────
    st.divider()
    section_header("Vista de Datos Consolidados", "Primeros 200 registros del cruce")
    st.dataframe(
        metrics["df"].head(200).style
            .applymap(
                lambda v: f"color: {COLORS['success']}" if v == "Pagado"
                else (f"color: {COLORS['danger']}" if v == "Pendiente" else ""),
                subset=["Estado_Pago"] if "Estado_Pago" in metrics["df"].columns else []
            ),
        use_container_width=True,
        height=320,
    )


def tab_pagos(metrics: dict):
    section_header(
        "Análisis de Pagos y Saldos",
        "Detalle por Dama, campaña y evolución de recaudación",
    )

    # ── Serie temporal ────────────────────────────────────────────────
    st.plotly_chart(
        plot_time_series(metrics["ts"]),
        use_container_width=True,
    )

    st.divider()
    # ── Top Damas ─────────────────────────────────────────────────────
    col_l, col_r = st.columns([2, 1])
    with col_l:
        top_n = st.slider("Número de Damas a mostrar", 5, 30, 15)
        st.plotly_chart(
            plot_top_damas(metrics["df"], metrics["saldo_col"], top_n),
            use_container_width=True,
        )
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

    # ── Exportar tabla filtrada ───────────────────────────────────────
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
    section_header(
        "Indicadores Técnicos y Predicciones",
        "RSI 14 períodos · Proyección de recuperación 30 días",
    )

    # ── RSI ───────────────────────────────────────────────────────────
    st.plotly_chart(plot_rsi(metrics["ts"]), use_container_width=True)

    rsi_serie = calculate_rsi(metrics["ts"]["valor"])
    rsi_actual = rsi_serie.dropna().iloc[-1] if not rsi_serie.dropna().empty else 50

    col1, col2, col3 = st.columns(3)
    with col1:
        color = COLORS["danger"] if rsi_actual > 70 else (COLORS["success"] if rsi_actual < 30 else COLORS["warning"])
        zona  = "Sobrecompra ⚠" if rsi_actual > 70 else ("Sobreventa ✅" if rsi_actual < 30 else "Zona Neutral")
        st.metric("RSI Actual (14)", f"{rsi_actual:.1f}", delta=zona)
    with col2:
        st.metric("Señal", "Venta / Alta Recaudación" if rsi_actual > 70
                           else ("Compra / Baja Recaudación" if rsi_actual < 30
                                 else "Neutral"))
    with col3:
        pct_change = (
            (metrics["ts"]["valor"].iloc[-1] - metrics["ts"]["valor"].iloc[-2])
            / metrics["ts"]["valor"].iloc[-2] * 100
            if len(metrics["ts"]) >= 2 and metrics["ts"]["valor"].iloc[-2] != 0
            else 0.0
        )
        st.metric("Variación Último Período", f"{pct_change:+.2f}%")

    st.divider()

    # ── Predicción ────────────────────────────────────────────────────
    section_header("Proyección de Recuperación", "Regresión Lineal · scikit-learn")
    pred_df = predict_recovery(metrics["ts"])
    st.plotly_chart(plot_prediction(metrics["ts"], pred_df), use_container_width=True)

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
            f"<div class='card' style='border-color:{COLORS['primary']};'>"
            f"<b style='color:{COLORS['primary']}'>Diagnóstico Predictivo</b><br>"
            f"<span style='font-size:1rem'>{tendencia}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
#  PANTALLA DE BIENVENIDA (sin archivo)
# ─────────────────────────────────────────────

def render_welcome():
    st.markdown(
        f"""
        <div style='text-align:center; padding: 3rem 0 1rem;'>
            <h1 style='font-size:2.8rem; color:{COLORS["primary"]}'>💼 Dashboard de Gestión de Cartera</h1>
            <p style='color:{COLORS["muted"]}; font-size:1.1rem; max-width:600px; margin:0 auto 2rem;'>
                Análisis profesional de cartera financiera con KPIs, RSI y predicciones.
                Carga tu archivo Excel para comenzar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown(
            f"""
            <div class='card' style='text-align:center;border-color:{COLORS["primary"]}'>
                <h4 style='color:{COLORS["primary"]}'>Estructura esperada del Excel</h4>
                <div style='display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;margin-top:1rem'>
                    <div>
                        <b style='color:{COLORS["success"]}'>Hoja: Cartera</b><br>
                        <small style='color:{COLORS["muted"]}'>
                            • Número de Dama<br>
                            • Año Campaña Saldo<br>
                            • (Columnas de valor/monto)
                        </small>
                    </div>
                    <div>
                        <b style='color:{COLORS["warning"]}'>Hoja: Saldos Actualizados</b><br>
                        <small style='color:{COLORS["muted"]}'>
                            • Número de Dama<br>
                            • Año Proceso<br>
                            • Campaña Proceso<br>
                            • (Saldo actualizado)
                        </small>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "📊", "KPIs en Tiempo Real",       "Métricas de cartera total, cobrado, pendiente y cumplimiento."),
        (c2, "📈", "RSI y Series Temporales",   "Análisis técnico con RSI de 14 períodos y zonas críticas."),
        (c3, "🔮", "Predicción 30 días",         "Proyección de recuperación con regresión lineal + IC."),
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
    # ── Estado de sesión ──────────────────────────────────────────────
    if "data" not in st.session_state:
        st.session_state.data = None
    if "last_file_name" not in st.session_state:
        st.session_state.last_file_name = None

    # ── Sidebar ───────────────────────────────────────────────────────
    filters = render_sidebar(st.session_state.data)

    # ── File uploader (siempre visible en el área principal) ──────────
    with st.expander("📂 Cargar / Cambiar Archivo Excel", expanded=st.session_state.data is None):
        uploaded = st.file_uploader(
            "Arrastra tu archivo .xlsx aquí",
            type=["xlsx", "xls"],
            help="El archivo debe contener una hoja de Cartera y una de Saldos Actualizados.",
        )
        if uploaded:
            if uploaded.name != st.session_state.last_file_name:
                with st.spinner("Procesando y cruzando datos…"):
                    try:
                        st.session_state.data = load_and_clean_data(uploaded)
                        st.session_state.last_file_name = uploaded.name
                        st.success(f"✅ Archivo **{uploaded.name}** cargado correctamente.")
                    except ValueError as e:
                        st.error(f"❌ Error de validación: {e}")
                        st.session_state.data = None
                    except Exception as e:
                        st.error(f"❌ Error inesperado al procesar el archivo: {e}")
                        st.session_state.data = None

    # ── Sin datos: pantalla de bienvenida ─────────────────────────────
    if st.session_state.data is None:
        render_welcome()
        return

    # ── Aplicar filtros del sidebar ───────────────────────────────────
    filtered_merged = apply_filters(st.session_state.data["merged"], filters)

    # Re-construir el objeto data con el DF filtrado
    filtered_data = {**st.session_state.data, "merged": filtered_merged}

    # ── Calcular métricas sobre datos filtrados ───────────────────────
    metrics = calculate_metrics(filtered_data)

    # ── Banner de filtro activo ───────────────────────────────────────
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
