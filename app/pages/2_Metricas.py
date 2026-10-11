import streamlit as st
import pandas as pd

st.set_page_config(page_title="Métricas y Rendimiento", layout="wide")

# Estilos profesionales para ambiente nocturno
st.markdown("""
<style>
    .stApp {
        background-color: #0B1120;
        color: #E2E8F0;
    }
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.3rem;
    }
    .page-sub {
        font-size: 1rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .card-info {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Métricas y Rendimiento de los Modelos</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Resumen de exactitud, margen de error y comportamiento de los modelos evaluados sobre el conjunto de prueba independiente (209 estudiantes).</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "Modelo 1: Estimación de Calificaciones",
    "Modelo 2: Detección de Nivel de Riesgo",
    "Lineamientos y Metodología"
])

with tab1:
    st.subheader("Modelo 1: Predicción de Nota Final (Escala 0 a 20)")
    st.markdown("""
    **Propósito:** Calcular la calificación numérica final esperada ($G3$) con el menor margen de error posible.
    Se comparan dos modalidades de uso:
    - **Con notas de periodos anteriores:** Emplea los primeros exámenes ($G1$ y $G2$) para proyectar la nota de cierre.
    - **Alerta temprana previa:** No utiliza notas previas para evaluar el riesgo antes del inicio de los exámenes.
    """)

    datos_m1 = [
        {"Modalidad": "Con notas previas (Sin Dropout)", "Error Promedio (MAE)": "1.16 ptos", "Error Cuadrático (RMSE)": "1.77 ptos", "Varianza Explicada": "82.4%", "Estado": "Evaluado"},
        {"Modalidad": "Con notas previas (Con Dropout)", "Error Promedio (MAE)": "1.18 ptos", "Error Cuadrático (RMSE)": "1.68 ptos", "Varianza Explicada": "83.1%", "Estado": "Seleccionado en API"},
        {"Modalidad": "Alerta temprana (Sin notas previas)", "Error Promedio (MAE)": "2.70 ptos", "Error Cuadrático (RMSE)": "3.70 ptos", "Varianza Explicada": "19.7%", "Estado": "Evaluado"},
        {"Modalidad": "Alerta temprana (Con Dropout)", "Error Promedio (MAE)": "2.66 ptos", "Error Cuadrático (RMSE)": "3.60 ptos", "Varianza Explicada": "20.7%", "Estado": "Evaluado"}
    ]
    st.dataframe(pd.DataFrame(datos_m1), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Configuración Seleccionada", "Con Dropout (20%)")
    c2.metric("Margen de Error Promedio", "± 1.18 puntos")
    c3.metric("Fuerza Explicativa", "83.1 %")

    st.markdown("""
    <div class="card-info">
        <strong>Interpretación práctica:</strong><br>
        En una escala de 0 a 20, un margen de error cercano a 1 punto significa que la predicción es altamente confiable
        para estimar si el estudiante aprobará o no la materia.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("Modelo 2: Clasificación en 4 Niveles de Riesgo")
    st.markdown(r"""
    **Propósito:** Asignar a cada estudiante a una categoría de atención institucional:
    - **Nivel 1 (Sin riesgo):** Nota estimada de 14 a 20.
    - **Nivel 2 (Riesgo bajo):** Nota estimada de 12 a 13.9.
    - **Nivel 3 (Riesgo medio):** Nota estimada de 10 a 11.9 (zona limítrofe).
    - **Nivel 4 (Riesgo alto):** Nota estimada menor a 10 (reprobación).
    """)

    datos_m2 = [
        {"Configuración": "Con notas previas (Sin Dropout)", "Exactitud (Accuracy)": "73.2%", "Precisión": "73.6%", "Sensibilidad": "73.2%", "F1 General": "0.7329", "Estado": "Seleccionado en API"},
        {"Configuración": "Con notas previas (Con Dropout)", "Exactitud (Accuracy)": "67.9%", "Precisión": "68.3%", "Sensibilidad": "67.9%", "F1 General": "0.6797", "Estado": "Evaluado"},
        {"Configuración": "Alerta temprana (Sin Dropout)", "Exactitud (Accuracy)": "41.6%", "Precisión": "42.0%", "Sensibilidad": "41.6%", "F1 General": "0.3928", "Estado": "Evaluado"},
        {"Configuración": "Alerta temprana (Con Dropout)", "Exactitud (Accuracy)": "45.0%", "Precisión": "45.7%", "Sensibilidad": "45.0%", "F1 General": "0.4272", "Estado": "Evaluado"}
    ]
    st.dataframe(pd.DataFrame(datos_m2), use_container_width=True)

    c_a, c_b, c_c = st.columns(3)
    c_a.metric("Exactitud Estricta", "73.2 %")
    c_b.metric("Balance F1 Ponderado", "0.7329")
    c_c.metric("Errores Críticos Extremos", "0 casos")

    st.markdown(r"""
    <div class="card-info">
        <strong>Interpretación práctica:</strong><br>
        El modelo clasifica correctamente al 73.2% de los estudiantes en su rango exacto. Además, presenta <strong>cero errores críticos</strong>
        (ningún estudiante de riesgo alto es catalogado como sin riesgo, ni viceversa). Si se considera una tolerancia de &plusmn;1 nivel adyacente,
        la efectividad supera el 98%.
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("Principios y Metodología Aplicada")
    st.markdown("""
    <div class="card-info">
        <h4 style="margin-top:0; color:#F8FAFC;">1. Preparación de Datos y Transparencia</h4>
        <ul>
            <li><strong>Aislamiento de la prueba:</strong> La normalización matemática se configuró exclusivamente con los datos de entrenamiento para garantizar que los resultados en prueba sean genuinos.</li>
            <li><strong>Prevención de ventajas artificiales:</strong> La nota final ($G3$) y el nivel de riesgo se retiraron de las entradas para que los modelos no conozcan la respuesta por adelantado.</li>
        </ul>
        <h4 style="color:#F8FAFC;">2. Entrenamiento y Control de Sobreajuste</h4>
        <ul>
            <li><strong>Parada temprana (EarlyStopping):</strong> El sistema detiene automáticamente el entrenamiento en el momento exacto en que el error de validación alcanza su punto más bajo, evitando la memorización.</li>
            <li><strong>Mecanismo Dropout:</strong> Desconecta aleatoriamente un porcentaje de neuronas durante el aprendizaje para asegurar que la red aprenda patrones generales y no dependa de un solo factor.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
