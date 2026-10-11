from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import StudentInput, GradePredictionResponse, RiskPredictionResponse
from api.predict import predictor_service

app = FastAPI(
    title="API de Predicción de Rendimiento Académico y Alerta Temprana",
    description=(
        "API REST desarrollada con FastAPI para consultar redes neuronales artificiales (ANN) "
        "entrenadas para predecir la calificación final (G3) y el nivel de riesgo de deserción "
        "de estudiantes del Student Performance Dataset."
    ),
    version="1.0.0"
)

# Permitir conexiones desde cualquier origen (Streamlit, Postman, Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def inicio():
    return {
        "sistema": "Sistema de Predicción de Rendimiento Académico y Alerta Temprana",
        "estado": "En línea",
        "version": "1.0.0",
        "endpoints": {
            "prediccion_calificacion": "POST /predict/grade",
            "prediccion_riesgo": "POST /predict/risk_level",
            "documentacion_swagger": "GET /docs",
            "documentacion_redoc": "GET /redoc"
        }
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "ok",
        "model1_loaded": predictor_service.modelo_regresion is not None,
        "model2_loaded": predictor_service.modelo_clasificacion is not None
    }


@app.post("/predict/grade", response_model=GradePredictionResponse, tags=["Predicciones"])
def predecir_calificacion(estudiante: StudentInput):
    """
    Predice la calificación final esperada G3 (escala 0-20) utilizando el
    Modelo 1 - ANN de Regresión (Versión A con Dropout) y evalúa el nivel de alerta temprana.
    """
    try:
        resultado = predictor_service.predecir_nota(estudiante.model_dump())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción de calificación: {str(e)}")


@app.post("/predict/risk_level", response_model=RiskPredictionResponse, tags=["Predicciones"])
def predecir_nivel_riesgo(estudiante: StudentInput):
    """
    Clasifica al estudiante en uno de los 4 niveles de riesgo académico utilizando el
    Modelo 2 - ANN de Clasificación Multiclase.
    """
    try:
        resultado = predictor_service.predecir_riesgo(estudiante.model_dump())
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción de riesgo: {str(e)}")
