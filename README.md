# Proyecto C: Sistema de Predicción de Rendimiento Académico

**Curso:** BD-151 Inteligencia Artificial Aplicada – Colegio Universitario de Cartago
**Profesor:** Osvaldo González Chaves
**Año:** 2026

## Integrantes

| Nombre | Carné | Correo |
|---|---|---|
| Luis Diego Montero Vargas | | |
| Mariana Méndez Pérez | | |
| Nadin Rojas López | | |
| Claret Rodríguez Jiménez | | |

## Descripción del problema

Sistema que predice el desempeño académico de estudiantes y detecta tempranamente el riesgo de deserción. Proporciona alertas tempranas para implementar intervenciones educativas oportunas.

## Dataset

- **Nombre:** Student Performance Dataset (UCI)
- **URL:** https://archive.ics.uci.edu/dataset/320/student+performance
- **Registros:** 395 estudiantes (matemáticas) + 649 (portugués) = 1044 registros
- **Variables:** 33 (demográficas, sociales, escolares)
- **Archivos:** `student-mat.csv` y `student-por.csv`, separados por `;`. Se unen en el notebook de preprocesamiento.
- **Diccionario de datos:** `Diccionario de datos.txt`

Los archivos originales están en `data/raw/` y no se modifican.

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
Proyecto-1-Sistema-de-Prediccion-de-Rendimiento-Academico/
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

Requisitos: Python 3.10 a 3.13 (TensorFlow no es compatible con Python 3.14) y Git.

```bash
git clone https://github.com/DiegoMonteroCRC/Proyecto-1-Sistema-de-Prediccion-de-Rendimiento-Academico.git
cd Proyecto-1-Sistema-de-Prediccion-de-Rendimiento-Academico
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

- [x] Notebook de EDA con análisis de factores que impactan el rendimiento
- [x] Feature engineering: creación de variables derivadas (promedio de notas, tasa de ausencias)
- [x] Dos modelos ANN: regresión de calificaciones y clasificación de riesgo
- [ ] API REST con endpoints /predict/grade y /predict/risk_level
- [ ] Dashboard Streamlit con sistema de alertas tempranas
- [ ] Recomendaciones automáticas de intervención según perfil del estudiante

## Resultados

**Modelo 1 (Regresión)**

| Configuración | MAE | RMSE | Varianza explicada |
|---|---|---|---|
| Versión A sin Dropout | 1.1619 | 1.7726 | 0.8236 |
| Versión A con Dropout | 1.1759 | 1.6848 | 0.8307 |
| Versión B sin Dropout | 2.6957 | 3.7023 | 0.1971 |
| Versión B con Dropout | 2.6551 | 3.6020 | 0.2072 |

**Modelo 2 (Clasificación Multiclase - Nivel de Riesgo)**

| Configuración | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Versión A sin Dropout | 0.7321 | 0.7362 | 0.7321 | 0.7329 |
| Versión A con Dropout | 0.6794 | 0.6827 | 0.6794 | 0.6797 |
| Versión B sin Dropout | 0.4163 | 0.4201 | 0.4163 | 0.3928 |
| Versión B con Dropout | 0.4498 | 0.4572 | 0.4498 | 0.4272 |

**Modelo seleccionado y justificación:**

- **Modelo 1:** Versión A con Dropout (`model1.keras`), al lograr menor RMSE (1.68) y mayor varianza explicada (0.83) reduciendo el sobreajuste.
- **Modelo 2:** Versión A sin Dropout (`model2.keras`), alcanzando un F1 ponderado de **0.7329** y Accuracy de **73.21%**, optimizado con `learning_rate=0.0004` en Adam.
- **Alerta temprana (Versión B):** Permite detectar a los estudiantes en riesgo únicamente a partir de variables de contexto y hábitos antes de disponer de notas de periodos previos.

## Conclusiones y recomendaciones

1. **Relevancia del rendimiento previo:** Las evaluaciones parciales ($G1$ y $G2$) representan los predictores más influyentes tanto en la calificación final esperada como en la clasificación de riesgo, aumentando la precisión en más de 28 puntos porcentuales respecto a los modelos de alerta temprana.
2. **Utilidad de los modelos de alerta temprana (Versión B):** A pesar de la reducción en exactitud estricta al no disponer de notas previas, los modelos de alerta temprana permiten identificar patrones de riesgo asociados a ausencias reiteradas, fallos previos y tiempo de estudio limitado desde el primer día de clases.
3. **Control del sobreajuste mediante EarlyStopping:** El monitoreo de la pérdida de validación (`val_loss`) y la restauración automática de los mejores pesos garantizan que ambos modelos mantengan su capacidad de generalización sobre registros nuevos sin memorizar el conjunto de entrenamiento.
4. **Recomendaciones de intervención:** Se recomienda activar tutorías personalizadas y seguimiento de asistencia a estudiantes detectados en niveles de riesgo medio y alto, priorizando alertas tempranas para intervenir preventivamente antes de los primeros exámenes sumativos.
