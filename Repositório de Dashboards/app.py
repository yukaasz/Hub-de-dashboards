import base64
import mimetypes
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# Configuração da página (PRECISA SER A PRIMEIRA LINHA)
st.set_page_config(
    page_title="Portal de Dashboards - Business Intelligence and Strategic Marketing LATAM",
    page_icon="📊",
    layout="wide",
)

# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
def make_preview_data_uri(title: str, accent: str = "#b91c1c") -> str:
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
    if thumbnail.startswith(("http://", "https://", "data:image")):
        return thumbnail
    base_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
    file_path = base_dir / thumbnail
    if not file_path.exists() or not file_path.is_file():
        return make_preview_data_uri("", accent="#6b7280")
    mime_type, _ = mimetypes.guess_type(file_path.name)
    mime_type = mime_type or "application/octet-stream"
    encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def render_dashboard_card(dashboard: dict) -> None:
    description = dashboard['description'].replace('"', '&quot;')
    st.markdown(
        f"""
        <a class="card-link" href="{dashboard['url']}" target="_blank" rel="noopener noreferrer">
            <article class="dashboard-card">
                <img class="card-preview" src="{resolve_thumbnail_source(dashboard['thumbnail'])}" alt="Prévia" />
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
    rows = [dashboards[index : index + columns_count] for index in range(0, len(dashboards), columns_count)]
    for row in rows:
        columns = st.columns(columns_count, gap="medium")
        for idx, column in enumerate(columns):
            with column:
                if idx < len(row):
                    render_dashboard_card(row[idx])

# ------------------------------------------------------------
# Base de Dados dos Dashboards
# ------------------------------------------------------------
DASHBOARDS = {
    "Parts & Services": [
        {
            "title": "Análise de Potencial",
            "description": "Análise de variação de potencial de vendas de peças de 2025x2026 e participação de mercado de 2024x2025.",
            "url": "https://app.powerbi.com/links/t2RjRREDQ9?ctid=79310fb0-d39b-486b-b77b-25f3e0c82a0e&pbi_source=linkShare",
            "thumbnail": "",        
        },
        {
            "title": "Análise de Risco de Churn",
            "description": "Análise de Risco de Churn de clientes.",
            "url": "https://app.powerbi.com/links/L3YExA4hJA?ctid=79310fb0-d39b-486b-b77b-25f3e0c82a0e&pbi_source=linkShare&bookmarkGuid=8fda7ab2-d756-41a9-88ca-0945da90fdb9",
            "thumbnail": "",
        },
    ],
    "Wholegoods": [
        
    ],
}

# ------------------------------------------------------------
# CSS LIMPO: Sem tentar hackear o cabeçalho do Streamlit
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 1. Transforma o fundo da barra superior numa cor 100% sólida e opaca */
    [data-testid="stHeader"] {
        background-color: var(--background-color) !important;
    }

    /* 2. Remove o espaço vazio gigante do topo da página */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* 3. Estilo do Título Principal (Agora ele fica na página, não flutuando) */
    .titulo-principal {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--secondary-background-color);
    }

    /* 4. Estilos dos Cards (Mantidos intactos) */
    .section-title {
        color: var(--text-color);
        margin: 1rem 0 0.5rem 0;
        font-size: 1.5rem !important;
        font-weight: 600;
    }
    .dashboard-card {
        background: var(--secondary-background-color);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        min-height: 150px;
        overflow: hidden;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-3px);
        border-color: #b91c1c;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    .card-preview {
        width: 100%;
        height: 100px;
        object-fit: cover;
        border-bottom: 1px solid var(--border-color);
    }
    .card-content { padding: 0.75rem; }
    .card-title {
        color: var(--text-color) !important;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .card-description {
        color: var(--text-color) !important;
        font-size: 0.85rem !important;
        opacity: 0.8 !important;
    }
    .card-link, .card-link * { text-decoration: none !important; }
    
    /* Título do menu lateral */
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Título Principal da Página (Lugar correto, sem gambiarra)
# ------------------------------------------------------------
st.markdown('<div class="titulo-principal">Portal de Dashboards - Business Intelligence and Strategic Marketing LATAM</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar com navegação
# ------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">📌 Áreas</div>', unsafe_allow_html=True)
    areas = list(DASHBOARDS.keys())
    areas.insert(0, "Todos")
    selected_area = st.radio("Selecione uma área", areas, index=0, label_visibility="collapsed")

# ------------------------------------------------------------
# Renderização das Seções
# ------------------------------------------------------------
if selected_area == "Todos":
    categories_to_show = DASHBOARDS.items()
else:
    categories_to_show = [(selected_area, DASHBOARDS[selected_area])]

for category, dashboards in categories_to_show:
    st.markdown(f'<h2 class="section-title">{category}</h2>', unsafe_allow_html=True)
    if dashboards:
        render_dashboard_grid(dashboards)
    else:
        st.info("Nenhum dashboard disponível.")