<<<<<<< HEAD
# Proyecto C: Sistema de Predicción de Rendimiento Académico

**Curso:** BD-151 Inteligencia Artificial Aplicada – Colegio Universitario de Cartago
**Profesor:** Osvaldo González Chaves
**Año:** 2026

## Integrantes

| Nombre | Carné | Correo |
|---|---|---|
| | | |
| | | |
| | | |

## Descripción del problema

Sistema que predice el desempeño académico de estudiantes y detecta tempranamente el riesgo de deserción. Proporciona alertas tempranas para implementar intervenciones educativas oportunas.

## Dataset

- **Nombre:** Student Performance Dataset (UCI)
- **URL:** https://archive.ics.uci.edu/dataset/320/student+performance
- **Registros:** 395 estudiantes (matemáticas) + 649 (portugués)
- **Variables:** 33 (demográficas, sociales, escolares)

Colocar los archivos originales en `data/raw/` sin modificarlos.

## Modelos

- **Modelo 1 – Regresión:** Predecir la calificación final esperada G3 (0-20). Comparar el desempeño con y sin las notas parciales G1/G2, ya que su uso reduce el valor de la alerta temprana
- **Modelo 2 – Clasificación Multiclase:** Clasificar nivel de riesgo académico (Sin riesgo/Riesgo bajo/Riesgo medio/Riesgo alto), definido por rangos de G3 justificados por el grupo

Lineamientos de entrenamiento:

- Normalización con `MinMaxScaler` ajustado solo sobre el conjunto de entrenamiento.
- Variables categóricas con `pd.get_dummies`; guardar la lista de columnas resultante en `models/columnas.pkl`.
- Entrenamiento con `validation_split` y `EarlyStopping`; el conjunto de prueba se usa solo para la evaluación final.
- Comparar al menos dos configuraciones por modelo (por ejemplo, con y sin `Dropout`).

## API REST

| Método | Endpoint | Respuesta |
|---|---|---|
| POST | `/predict/grade` | Calificación final esperada (0-20) |
| POST | `/predict/risk_level` | Nivel de riesgo académico |

La documentación automática queda disponible en `http://localhost:8000/docs`.

## Estructura del proyecto

```
Proyecto_C_Rendimiento_Academico/
│
├── README.md                      ← Guía completa de instalación y uso del proyecto
├── requirements.txt               ← Dependencias Python
├── .gitignore                     ← Archivos excluidos del control de versiones
│
├── data/
│   ├── raw/                       ← Datos originales sin procesar
│   └── processed/                 ← Datos limpios y preprocesados
│       ├── train.csv              ← Conjunto de entrenamiento
│       └── test.csv               ← Conjunto de prueba
│
├── notebooks/
│   ├── 01_EDA.ipynb               ← Análisis Exploratorio de Datos
│   ├── 02_Preprocesamiento.ipynb  ← Limpieza, variables dummy, normalización
│   ├── 03_ANN_Modelo1.ipynb       ← Entrenamiento del Modelo 1
│   ├── 04_ANN_Modelo2.ipynb       ← Entrenamiento del Modelo 2
│   └── 05_Comparacion_Modelos.ipynb ← Evaluación y selección del mejor modelo
│
├── src/
│   ├── __init__.py
│   ├── config.py                  ← Configuraciones globales (rutas, parámetros)
│   ├── data_prep.py               ← Funciones de preprocesamiento
│   └── train/
│       ├── __init__.py
│       ├── model1.py              ← Entrenamiento del Modelo 1
│       ├── model2.py              ← Entrenamiento del Modelo 2
│       └── utils.py               ← Utilidades compartidas (métricas, gráficas)
│
├── models/
│   ├── model1.keras               ← Modelo 1 guardado (formato Keras)
│   ├── model2.keras               ← Modelo 2 guardado (formato Keras)
│   ├── scaler.pkl                 ← MinMaxScaler entrenado
│   └── columnas.pkl               ← Columnas finales tras get_dummies
│
├── api/
│   ├── main.py                    ← Aplicación FastAPI con endpoints
│   ├── schemas.py                 ← Modelos Pydantic para validación
│   └── predict.py                 ← Lógica de predicción e inferencia
│
└── app/
    ├── Home.py                    ← Página principal del dashboard
    └── pages/
        ├── 1_Prediccion.py        ← Predicciones individuales
        ├── 2_Analisis.py          ← Análisis de lotes
        └── 3_Metricas.py          ← Métricas y rendimiento
```

## Instalación

Requisitos: Python 3.11 y Git.

```bash
git clone <url-del-repositorio>
cd Proyecto_C_Rendimiento_Academico
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

1. Ejecutar los notebooks en orden (`01` a `05`) desde `notebooks/`:
   ```bash
   jupyter notebook
   ```
2. Levantar la API (desde la raíz del proyecto):
   ```bash
   uvicorn api.main:app --reload
   ```
3. Levantar el frontend en otra terminal:
   ```bash
   streamlit run app/Home.py
   ```

## Entregables

- [ ] Notebook de EDA con análisis de factores que impactan el rendimiento
- [ ] Feature engineering: creación de variables derivadas (promedio de notas, tasa de ausencias)
- [ ] Dos modelos ANN: regresión de calificaciones y clasificación de riesgo
- [ ] API REST con endpoints /predict/grade y /predict/risk_level
- [ ] Dashboard Streamlit con sistema de alertas tempranas
- [ ] Recomendaciones automáticas de intervención según perfil del estudiante

## Resultados

**Modelo 1 (Regresión)**

| Configuración | MAE | RMSE | Varianza explicada |
|---|---|---|---|
| | | | |

**Modelo 2 (Clasificación)**

| Configuración | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| | | | | |

**Modelo seleccionado y justificación:**

_Completar._

## Conclusiones y recomendaciones

_Completar._
=======
# Proyecto-1-Sistema-de-Prediccion-de-Rendimiento-Academico
Proyecto asignado en el curso BD - 151 Inteligencia Artificial Aplicada | Se aborda un problema utilizando redes neuronales artificiales y requiere el desarrollo de un sistema desde la exploración de datos hasta el despliegue con API y frontend. Los proyectos están diseñados con complejidad equivalente pero en diferentes dominios de aplicación. 
>>>>>>> e8abae40db6ce197f1ddc2802cdf4226ff226490
