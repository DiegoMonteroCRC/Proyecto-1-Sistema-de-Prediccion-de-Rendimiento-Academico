import sys
from pathlib import Path
import streamlit as st
import requests

# Asegurar que la raiz del proyecto este en sys.path para importar api y src
RUTA_RAIZ = Path(__file__).resolve().parent.parent
if str(RUTA_RAIZ) not in sys.path:
    sys.path.insert(0, str(RUTA_RAIZ))

st.set_page_config(
    page_title="Sistema de Alerta Temprana",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores profesional optimizada para proyeccion nocturna
st.markdown("""
<style>
    /* Estilos generales para ambiente nocturno */
    .stApp {
        background-color: #0B1120;
        color: #E2E8F0;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 1.8rem;
        line-height: 1.5;
    }
    .card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .card-kpi {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #38BDF8;
        border-radius: 8px;
        padding: 1rem;
    }
    .status-online {
        background-color: #064E3B;
        color: #6EE7B7;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #059669;
    }
    .status-local {
        background-color: #451A03;
        color: #FCD34D;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #D97706;
    }
    .footer-discreto {
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid #1E293B;
        color: #64748B;
        font-size: 0.82rem;
        display: flex;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Sistema de Predicción de Rendimiento Académico y Alerta Temprana</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Herramienta institucional para estimar la calificación final de los estudiantes e identificar a tiempo situaciones que requieran apoyo pedagógico.</div>', unsafe_allow_html=True)

# Comprobacion de conexion con la API
API_URL = "http://localhost:8000"
api_online = False
try:
    resp = requests.get(f"{API_URL}/health", timeout=1.2)
    if resp.status_code == 200:
        api_online = True
except Exception:
    api_online = False

col_status, col_espacio = st.columns([1.5, 3.5])
with col_status:
    if api_online:
        st.markdown('<span class="status-online">Servicio API activo (Puerto 8000)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-local">Modo local activo (Inferencia directa)</span>', unsafe_allow_html=True)

st.write("")

# Indicadores clave del sistema (texto claro, no tecnico)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
    <div class="card-kpi">
        <div style="color:#94A3B8; font-size:0.85rem;">Registros de estudiantes</div>
        <div style="color:#F8FAFC; font-size:1.8rem; font-weight:700;">1,044</div>
        <div style="color:#64748B; font-size:0.8rem;">Matemáticas y Portugués</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="card-kpi">
        <div style="color:#94A3B8; font-size:0.85rem;">Factores evaluados</div>
        <div style="color:#F8FAFC; font-size:1.8rem; font-weight:700;">33</div>
        <div style="color:#64748B; font-size:0.8rem;">Académicos, personales y de hogar</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="card-kpi" style="border-left-color: #10B981;">
        <div style="color:#94A3B8; font-size:0.85rem;">Modelo 1 (Regresión)</div>
        <div style="color:#10B981; font-size:1.8rem; font-weight:700;">83.1%</div>
        <div style="color:#64748B; font-size:0.8rem;">Varianza explicada (RMSE: 1.68)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="card-kpi" style="border-left-color: #A855F7;">
        <div style="color:#94A3B8; font-size:0.85rem;">Modelo 2 (Clasificación)</div>
        <div style="color:#A855F7; font-size:1.8rem; font-weight:700;">73.2%</div>
        <div style="color:#64748B; font-size:0.8rem;">Precisión (4 niveles de riesgo)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# Modulos disponibles
st.subheader("Módulos del Sistema")

mod1, mod2 = st.columns(2)

with mod1:
    st.markdown("""
    <div class="card">
        <h4 style="margin-top:0; color:#F8FAFC;">1. Predicción Individual</h4>
        <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">
            Permite ingresar o generar los datos de un estudiante para estimar su nota final
            y conocer de inmediato si se encuentra en algún nivel de riesgo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Abrir Predicción Individual", use_container_width=True):
        st.switch_page("pages/1_Prediccion.py")

with mod2:
    st.markdown("""
    <div class="card">
        <h4 style="margin-top:0; color:#F8FAFC;">2. Métricas del Modelo</h4>
        <p style="color:#94A3B8; font-size:0.95rem; line-height:1.5;">
            Presenta el resumen de evaluación de los modelos matemáticos empleados,
            con tablas de resultados, comportamiento de errores y comparativas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Abrir Métricas del Modelo", use_container_width=True):
        st.switch_page("pages/2_Metricas.py")

# Integrantes de forma discreta al pie
st.markdown("""
<div class="footer-discreto">
    <div>Proyecto BD-151 Inteligencia Artificial Aplicada | CUC 2026</div>
    <div>Equipo: L. Montero V. • M. Méndez P. • N. Rojas L. • C. Rodríguez J.</div>
</div>
""", unsafe_allow_html=True)
