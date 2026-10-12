import sys
import random
from pathlib import Path
import streamlit as st
import requests

# Asegurar que la raiz del proyecto este en sys.path para importar api y src
RUTA_RAIZ = Path(__file__).resolve().parents[2]
if str(RUTA_RAIZ) not in sys.path:
    sys.path.insert(0, str(RUTA_RAIZ))

from api.predict import predictor_service

st.set_page_config(page_title="Predicción Individual", layout="wide")

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
    .card-result {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .alert-critica {
        background-color: #450A0A;
        border: 1px solid #991B1B;
        color: #FCA5A5;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .alert-alta {
        background-color: #451A03;
        border: 1px solid #B45309;
        color: #FCD34D;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .alert-moderada {
        background-color: #0C4A6E;
        border: 1px solid #0284C7;
        color: #BAE6FD;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .alert-baja {
        background-color: #064E3B;
        border: 1px solid #059669;
        color: #A7F3D0;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .factor-item {
        background-color: #0F172A;
        border-left: 3px solid #38BDF8;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        border-radius: 0 4px 4px 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Predicción Individual y Alerta Temprana</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Estima la nota final esperada del estudiante y detecta factores que puedan comprometer su rendimiento.</div>', unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Funcion para inicializar o generar datos aleatorios en session_state
def generar_valores_aleatorios():
    st.session_state["materia"] = random.choice(["matematicas", "portugues"])
    st.session_state["school"] = random.choice(["GP", "MS"])
    st.session_state["studytime"] = random.choice([1, 2, 3, 4])
    base_grade = round(random.uniform(5.0, 16.5), 1)
    st.session_state["G1"] = float(base_grade)
    st.session_state["G2"] = float(max(0.0, min(20.0, round(base_grade + random.uniform(-2.0, 2.0), 1))))
    st.session_state["absences"] = int(random.randint(0, 18))
    st.session_state["failures"] = int(random.choice([0, 0, 0, 1, 2]))
    st.session_state["schoolsup"] = random.choice(["no", "yes"])
    st.session_state["paid"] = random.choice(["no", "yes"])
    st.session_state["age"] = int(random.randint(15, 19))
    st.session_state["sex"] = random.choice(["F", "M"])
    st.session_state["address"] = random.choice(["U", "R"])
    st.session_state["higher"] = random.choice(["yes", "yes", "no"])
    st.session_state["traveltime"] = random.choice([1, 2, 3])
    st.session_state["freetime"] = int(random.randint(1, 5))
    st.session_state["goout"] = int(random.randint(1, 5))
    st.session_state["activities"] = random.choice(["yes", "no"])
    st.session_state["Dalc"] = int(random.choice([1, 1, 2, 3]))
    st.session_state["Walc"] = int(random.choice([1, 2, 3]))
    st.session_state["health"] = int(random.randint(1, 5))
    st.session_state["romantic"] = random.choice(["no", "yes"])
    st.session_state["famsize"] = random.choice(["GT3", "LE3"])
    st.session_state["Pstatus"] = random.choice(["T", "A"])
    st.session_state["guardian"] = random.choice(["mother", "father", "other"])
    st.session_state["Medu"] = int(random.randint(0, 4))
    st.session_state["Fedu"] = int(random.randint(0, 4))
    st.session_state["famrel"] = int(random.randint(1, 5))
    st.session_state["Mjob"] = random.choice(["teacher", "health", "services", "at_home", "other"])
    st.session_state["Fjob"] = random.choice(["teacher", "health", "services", "at_home", "other"])
    st.session_state["famsup"] = random.choice(["yes", "no"])
    st.session_state["nursery"] = random.choice(["yes", "no"])
    st.session_state["reason"] = random.choice(["course", "home", "reputation", "other"])
    st.session_state["internet"] = random.choice(["yes", "no"])

# Inicializar por primera vez si no existen
if "materia" not in st.session_state:
    generar_valores_aleatorios()

# Barra superior con boton para generar datos aleatorios
col_btn_rnd, col_info_rnd = st.columns([1.5, 3.5])
with col_btn_rnd:
    if st.button("Generar datos aleatorios de ejemplo", use_container_width=True):
        generar_valores_aleatorios()
        st.rerun()

with col_info_rnd:
    st.caption("Puedes presionar el botón para rellenar de inmediato los 3 grupos de factores con un perfil estudiantil aleatorio.")

st.write("")

# Formulario principal con los factores agrupados
with st.form("form_estudiante"):
    tab_acad, tab_personal, tab_familiar = st.tabs([
        "Factores Académicos",
        "Factores Personales y Hábitos",
        "Contexto Familiar y Hogar"
    ])

    with tab_acad:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Materia", ["matematicas", "portugues"], format_func=lambda x: x.capitalize(), key="materia")
            st.selectbox("Institución", ["GP", "MS"], format_func=lambda x: "Gabriel Pereira" if x == "GP" else "Mousinho da Silveira", key="school")
            st.selectbox("Tiempo semanal de estudio", [1, 2, 3, 4],
                         format_func=lambda x: {1: "Menos de 2 horas", 2: "2 a 5 horas", 3: "5 a 10 horas", 4: "Más de 10 horas"}[x], key="studytime")
        with col2:
            st.slider("Nota Primer Periodo (G1)", 0.0, 20.0, step=0.5, key="G1")
            st.slider("Nota Segundo Periodo (G2)", 0.0, 20.0, step=0.5, key="G2")
            st.number_input("Número de ausencias escolares", min_value=0, max_value=93, step=1, key="absences")
        with col3:
            st.selectbox("Materias reprobadas previamente", [0, 1, 2, 3, 4], key="failures")
            st.selectbox("Apoyo escolar adicional", ["no", "yes"], format_func=lambda x: "Sí" if x == "yes" else "No", key="schoolsup")
            st.selectbox("Clases extracurriculares pagadas", ["no", "yes"], format_func=lambda x: "Sí" if x == "yes" else "No", key="paid")

    with tab_personal:
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.slider("Edad", 15, 22, key="age")
            st.selectbox("Sexo", ["F", "M"], format_func=lambda x: "Femenino" if x == "F" else "Masculino", key="sex")
            st.selectbox("Zona de residencia", ["U", "R"], format_func=lambda x: "Urbana" if x == "U" else "Rural", key="address")
            st.selectbox("Interés en educación superior", ["yes", "no"], format_func=lambda x: "Sí" if x == "yes" else "No", key="higher")
        with col_p2:
            st.selectbox("Tiempo de traslado al centro", [1, 2, 3, 4],
                         format_func=lambda x: {1: "Menos de 15 min", 2: "15 a 30 min", 3: "30 a 60 min", 4: "Más de 1 hora"}[x], key="traveltime")
            st.slider("Tiempo libre tras clases (1: Mínimo a 5: Máximo)", 1, 5, key="freetime")
            st.slider("Frecuencia de salidas sociales (1: Rara vez a 5: Frecuente)", 1, 5, key="goout")
            st.selectbox("Actividades extracurriculares", ["yes", "no"], format_func=lambda x: "Sí" if x == "yes" else "No", key="activities")
        with col_p3:
            st.slider("Consumo de alcohol entre semana (1 a 5)", 1, 5, key="Dalc")
            st.slider("Consumo de alcohol en fines de semana (1 a 5)", 1, 5, key="Walc")
            st.slider("Estado de salud (1: Delicado a 5: Excelente)", 1, 5, key="health")
            st.selectbox("Relación sentimental activa", ["no", "yes"], format_func=lambda x: "Sí" if x == "yes" else "No", key="romantic")

    with tab_familiar:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.selectbox("Tamaño del núcleo familiar", ["GT3", "LE3"], format_func=lambda x: "Más de 3 miembros" if x == "GT3" else "3 o menos", key="famsize")
            st.selectbox("Convivencia de los progenitores", ["T", "A"], format_func=lambda x: "Viven juntos" if x == "T" else "Separados", key="Pstatus")
            st.selectbox("Tutor legal principal", ["mother", "father", "other"], format_func=lambda x: {"mother": "Madre", "father": "Padre", "other": "Otro"}[x], key="guardian")
        with col_f2:
            edu_labels = {0: "Ninguna", 1: "Primaria incompleta", 2: "Primaria completa", 3: "Secundaria", 4: "Educación superior"}
            st.selectbox("Nivel educativo de la madre", [0, 1, 2, 3, 4], format_func=lambda x: edu_labels[x], key="Medu")
            st.selectbox("Nivel educativo del padre", [0, 1, 2, 3, 4], format_func=lambda x: edu_labels[x], key="Fedu")
            st.slider("Relación familiar (1: Conflictiva a 5: Armoniosa)", 1, 5, key="famrel")
        with col_f3:
            job_labels = {"teacher": "Educación", "health": "Salud", "services": "Servicios civiles", "at_home": "Hogar", "other": "Otro"}
            st.selectbox("Ocupación de la madre", list(job_labels.keys()), format_func=lambda x: job_labels[x], key="Mjob")
            st.selectbox("Ocupación del padre", list(job_labels.keys()), format_func=lambda x: job_labels[x], key="Fjob")
            st.selectbox("Apoyo educativo familiar", ["yes", "no"], format_func=lambda x: "Sí" if x == "yes" else "No", key="famsup")
            st.selectbox("Asistió a guardería", ["yes", "no"], format_func=lambda x: "Sí" if x == "yes" else "No", key="nursery")
            st.selectbox("Motivo de elección de centro", ["course", "home", "reputation", "other"],
                         format_func=lambda x: {"course": "Preferencia por materias", "home": "Cercanía", "reputation": "Reputación", "other": "Otro"}[x], key="reason")
            st.selectbox("Conexión a Internet en el hogar", ["yes", "no"], format_func=lambda x: "Sí" if x == "yes" else "No", key="internet")

    submit = st.form_submit_button("Consultar Modelo y Evaluar Alerta", use_container_width=True)

if submit:
    payload = {
        "materia": st.session_state["materia"],
        "school": st.session_state["school"],
        "sex": st.session_state["sex"],
        "age": st.session_state["age"],
        "address": st.session_state["address"],
        "famsize": st.session_state["famsize"],
        "Pstatus": st.session_state["Pstatus"],
        "Medu": st.session_state["Medu"],
        "Fedu": st.session_state["Fedu"],
        "Mjob": st.session_state["Mjob"],
        "Fjob": st.session_state["Fjob"],
        "reason": st.session_state["reason"],
        "guardian": st.session_state["guardian"],
        "traveltime": st.session_state["traveltime"],
        "studytime": st.session_state["studytime"],
        "failures": st.session_state["failures"],
        "schoolsup": st.session_state["schoolsup"],
        "famsup": st.session_state["famsup"],
        "paid": st.session_state["paid"],
        "activities": st.session_state["activities"],
        "nursery": st.session_state["nursery"],
        "higher": st.session_state["higher"],
        "internet": st.session_state["internet"],
        "romantic": st.session_state["romantic"],
        "famrel": st.session_state["famrel"],
        "freetime": st.session_state["freetime"],
        "goout": st.session_state["goout"],
        "Dalc": st.session_state["Dalc"],
        "Walc": st.session_state["Walc"],
        "health": st.session_state["health"],
        "absences": st.session_state["absences"],
        "G1": float(st.session_state["G1"]),
        "G2": float(st.session_state["G2"])
    }

    grade_data = None
    risk_data = None
    try:
        r_grade = requests.post(f"{API_URL}/predict/grade", json=payload, timeout=2.5)
        if r_grade.status_code == 200:
            grade_data = r_grade.json()
        r_risk = requests.post(f"{API_URL}/predict/risk_level", json=payload, timeout=2.5)
        if r_risk.status_code == 200:
            risk_data = r_risk.json()
    except Exception:
        # Fallback local silencioso
        grade_data = predictor_service.predecir_nota(payload)
        risk_data = predictor_service.predecir_riesgo(payload)

    if grade_data and risk_data:
        st.write("")
        st.markdown("### Resultado de la Evaluación")

        # Modelo 1 (Regresión): nota final proyectada
        nota = grade_data["predicted_grade"]
        # Modelo 2 (Clasificación): nivel de riesgo
        nivel_riesgo = risk_data["risk_level"]

        col_metrica, col_alerta = st.columns([1.2, 2.3])

        with col_metrica:
            st.markdown("#### Modelo 1: Nota Final")
            st.metric(
                label="Nota Final Proyectada (0 a 20)",
                value=f"{nota:.2f}",
                delta=f"{nota - 10:.2f} sobre la aprobación (10)" if nota >= 10 else f"{nota - 10:.2f} bajo la aprobación (10)"
            )
            progreso = max(0.0, min(1.0, nota / 20.0))
            st.progress(progreso)

            # Mensaje sencillo según la nota proyectada (en Portugal se aprueba con 10)
            if nota >= 11:
                st.markdown(f"Según el modelo, el estudiante obtendría una nota de **{nota:.2f}**, suficiente para aprobar.")
            elif nota >= 10:
                st.markdown(f"Según el modelo, el estudiante obtendría una nota de **{nota:.2f}**: aprobaría, pero muy justo.")
            elif nota >= 9:
                st.markdown(f"Según el modelo, el estudiante obtendría una nota de **{nota:.2f}**: le faltaría poco para aprobar.")
            else:
                st.markdown(f"Según el modelo, el estudiante obtendría una nota de **{nota:.2f}**, por debajo de la nota mínima para aprobar (10).")

        with col_alerta:
            st.markdown("#### Modelo 2: Nivel de Riesgo")
            if nivel_riesgo == 4:
                st.markdown("""
                <div class="alert-critica">
                    <strong>Atención prioritaria requerida (Riesgo Alto):</strong><br>
                    El modelo de clasificación ubica al estudiante en el grupo de riesgo alto: su perfil se parece al de los estudiantes que reprueban.
                    Se recomienda incorporar al estudiante en planes de apoyo y tutoría de manera inmediata.
                </div>
                """, unsafe_allow_html=True)
            elif nivel_riesgo == 3:
                st.markdown("""
                <div class="alert-alta">
                    <strong>Acompañamiento preventivo sugerido (Riesgo Medio):</strong><br>
                    El modelo de clasificación ubica al estudiante en el grupo de riesgo medio: su perfil se parece al de los estudiantes que aprueban con dificultad.
                    Conviene realizar seguimiento para evitar caídas en evaluaciones futuras.
                </div>
                """, unsafe_allow_html=True)
            elif nivel_riesgo == 2:
                st.markdown("""
                <div class="alert-moderada">
                    <strong>Seguimiento regular (Riesgo Bajo):</strong><br>
                    El modelo de clasificación ubica al estudiante en el grupo de riesgo bajo: su perfil se parece al de los estudiantes con un rendimiento aceptable.
                    El estudiante mantiene un avance estable con oportunidad de superación.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-baja">
                    <strong>Desempeño satisfactorio (Sin Riesgo):</strong><br>
                    El modelo de clasificación ubica al estudiante en el grupo sin riesgo: su perfil se parece al de los estudiantes con buen rendimiento.
                    El estudiante muestra hábitos y desempeño favorables para concluir con éxito.
                </div>
                """, unsafe_allow_html=True)

        # Factores destacados detectados en el perfil (sin emojis)
        st.write("")
        st.markdown("#### Factores Relevantes Detectados en el Perfil")
        factores = []
        if payload["absences"] >= 10:
            factores.append(f"Ausencias acumuladas: Registra {payload['absences']} faltas escolares (la media institucional es de aproximadamente 5).")
        if payload["failures"] > 0:
            factores.append(f"Historial académico: Presenta {payload['failures']} materia(s) reprobada(s) anteriormente.")
        if payload["studytime"] == 1:
            factores.append("Tiempo de estudio limitado: Dedica menos de 2 horas por semana al repaso fuera de horario de clase.")
        if payload["Dalc"] >= 3 or payload["Walc"] >= 4:
            factores.append("Hábitos sociales: Frecuencia considerable de consumo de alcohol entre semana o fines de semana.")
        if payload["G1"] < 10 or payload["G2"] < 10:
            factores.append(f"Evaluaciones intermedias: Al menos una nota parcial se encuentra en zona reprobatoria (G1={payload['G1']}, G2={payload['G2']}).")
        if payload["higher"] == "no":
            factores.append("Expectativas académicas: El estudiante no tiene proyectado cursar estudios superiores.")

        if factores:
            for f in factores:
                st.markdown(f'<div class="factor-item">{f}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="factor-item" style="border-left-color:#10B981;">No se observaron indicadores desfavorables significativos en sus hábitos ni antecedentes.</div>', unsafe_allow_html=True)
