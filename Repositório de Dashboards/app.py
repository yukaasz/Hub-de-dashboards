import base64
import mimetypes
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Portal de Dashboards - Business Intelligence LATAM Parts & Services",
    page_icon="📊",
    layout="wide",
)

# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
def make_preview_data_uri(title: str, accent: str = "#b91c1c") -> str:
    """Gera um thumbnail SVG em data URI para simular prévia de dashboard."""
    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='480' height='270' viewBox='0 0 480 270'>
      <defs>
        <linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'>
          <stop offset='0%' stop-color='#f8fafc' />
          <stop offset='100%' stop-color='#e5e7eb' />
        </linearGradient>
      </defs>
      <rect width='480' height='270' fill='url(#bg)' />
      <rect x='12' y='12' width='456' height='140' rx='8' fill='#ffffff' stroke='#d1d5db' />
      <rect x='12' y='164' width='456' height='56' rx='6' fill='#f3f4f6' stroke='#d1d5db' />
      <rect x='12' y='12' width='456' height='12' fill='{accent}' />
      <text x='28' y='72' font-size='36' font-family='Arial, Helvetica, sans-serif' font-weight='700' fill='#111827'>CNH</text>
      <text x='30' y='98' font-size='14' font-family='Arial, Helvetica, sans-serif' fill='#374151'>INDUSTRIAL</text>
      <text x='28' y='194' font-size='16' font-family='Arial, Helvetica, sans-serif' font-weight='600' fill='#1f2937'>{title}</text>
    </svg>
    """.strip()
    return f"data:image/svg+xml;utf8,{quote(svg)}"

def resolve_thumbnail_source(thumbnail: str) -> str:
    """Aceita URL/data URI ou caminho local e retorna um src válido para <img>."""
    if thumbnail.startswith(("http://", "https://", "data:image")):
        return thumbnail

    # Tenta resolver o caminho absoluto em relação ao diretório do script
    base_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
    file_path = base_dir / thumbnail

    if not file_path.exists() or not file_path.is_file():
        return make_preview_data_uri("Prévia", accent="#6b7280")

    mime_type, _ = mimetypes.guess_type(file_path.name)
    mime_type = mime_type or "application/octet-stream"
    encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def render_dashboard_card(dashboard: dict) -> None:
    """Renderiza um card de dashboard com thumbnail de prévia e link externo."""
    description = dashboard['description'].replace('"', '&quot;')
    st.markdown(
        f"""
        <a class="card-link" href="{dashboard['url']}" target="_blank" rel="noopener noreferrer">
            <article class="dashboard-card">
                <img class="card-preview" src="{resolve_thumbnail_source(dashboard['thumbnail'])}" alt="Prévia do dashboard {dashboard['title']}" />
                <div class="card-content">
                    <div class="card-title">{dashboard['title']}</div>
                    <div class="card-description">{description}</div>
                </div>
            </article>
        </a>
        """,
        unsafe_allow_html=True,
    )

def render_dashboard_grid(dashboards: list[dict], columns_count: int = 4) -> None:
    """Renderiza uma grade responsiva de dashboards usando st.columns."""
    rows = [dashboards[index : index + columns_count] for index in range(0, len(dashboards), columns_count)]
    for row in rows:
        columns = st.columns(columns_count, gap="medium")
        for idx, column in enumerate(columns):
            with column:
                if idx < len(row):
                    render_dashboard_card(row[idx])

# ------------------------------------------------------------
# Definição dos dashboards
# ------------------------------------------------------------
DASHBOARDS = {
    "Parts & Services": [
        {
            "title": "Análise de Potencial",
            "description": "Análise de variação de potencial de vendas de peças de 2025x2026 e participação de mercado de 2024x2025.",
            "url": "https://app.powerbi.com/links/t2RjRREDQ9?ctid=79310fb0-d39b-486b-b77b-25f3e0c82a0e&pbi_source=linkShare",
            "thumbnail": "preview/Variação potencial 25x26.png",
        },
        {
            "title": "Análise de Risco de Churn",
            "description": "Análise de Risco de Churn de clientes.",
            "url": "https://app.powerbi.com/links/L3YExA4hJA?ctid=79310fb0-d39b-486b-b77b-25f3e0c82a0e&pbi_source=linkShare&bookmarkGuid=8fda7ab2-d756-41a9-88ca-0945da90fdb9",
            "thumbnail": "preview/Analise Risco de Churn.png",
        },
    ],
    "Whole Goods": [],
}

# ------------------------------------------------------------
# CSS personalizado
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Usa variáveis de tema do Streamlit */
    .stApp {
        background-color: var(--background-color);
    }

    header[data-testid="stHeader"] {
        background-color: var(--secondary-background-color);
        border-bottom: 1px solid var(--border-color);
    }

    /* Título do portal na barra superior */
    header[data-testid="stHeader"]::after {
        content: "Portal de Dashboards - Business Intelligence LATAM Parts & Services";
        position: absolute;
        left: 3.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 70%;
    }

    /* Botão de recolher da sidebar sempre visível */
    button[kind="sidebarCollapse"] {
        visibility: visible !important;
        opacity: 1 !important;
        background-color: var(--secondary-background-color) !important;
        border-radius: 0 8px 8px 0 !important;
        left: 0 !important;
        z-index: 1000 !important;
    }

    /* Alternativa para versões mais recentes */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        opacity: 1 !important;
    }

    .section-title {
        color: var(--text-color);
        margin: 0.4rem 0 0.4rem 0;
        font-size: 1.8rem !important;
        font-weight: 600;
        line-height: 1.2;
    }

    .block-container {
        padding-top: 3rem;
    }

    .dashboard-card {
        background: var(--secondary-background-color);
        border-radius: 10px;
        border: 1px solid var(--border-color);
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
        min-height: 150px;
        overflow: hidden;
        margin-bottom: 0.75rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    .dashboard-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary-color);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
    }

    .card-preview {
        width: 100%;
        height: 90px;
        object-fit: cover;
        border-bottom: 1px solid var(--border-color);
        background: var(--secondary-background-color);
    }

    .card-content {
        padding: 0.55rem 0.65rem 0.65rem 0.65rem;
    }

    .card-title {
        color: var(--text-color);
        font-size: 1.0rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        line-height: 1.15;
    }

    .card-description {
        color: var(--text-color);
        font-size: 0.85rem !important;
        text-decoration: none !important;
        opacity: 0.8;
    }

    .card-link {
        text-decoration: none;
    }

    .card-link:focus { outline: none; }

    div[data-testid="column"] {
        min-width: 160px;
        max-width: 220px;
    }

    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid var(--border-color);
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
        padding-left: 0.5rem;
    }

    .stRadio > div {
        color: var(--text-color);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Sidebar e conteúdo
# ------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📌 Áreas</div>', unsafe_allow_html=True)
    areas = list(DASHBOARDS.keys())
    areas.insert(0, "Todos")
    selected_area = st.radio(
        "Selecione uma área",
        areas,
        index=0,
        label_visibility="collapsed",
    )

if selected_area == "Todos":
    categories_to_show = DASHBOARDS.items()
else:
    categories_to_show = [(selected_area, DASHBOARDS[selected_area])]

for category, dashboards in categories_to_show:
    st.markdown(f'<h2 class="section-title">{category}</h2>', unsafe_allow_html=True)
    if dashboards:
        render_dashboard_grid(dashboards)
    else:
        st.info("Nenhum dashboard disponível para esta área no momento.")

