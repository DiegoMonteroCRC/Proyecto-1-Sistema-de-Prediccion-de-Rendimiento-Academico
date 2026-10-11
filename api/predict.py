import numpy as np
from tensorflow.keras.models import load_model
from src import config
from src.data_prep import Preprocesador


class PredictorService:
    """
    Servicio de inferencia que gestiona la carga de modelos entrenados
    y el preprocesamiento de estudiantes para la API REST.
    """

    def __init__(self):
        self.preprocesador = Preprocesador()
        self.preprocesador.cargar_scaler_y_columnas()

        # Modelo 1: Regresión (Versión A con Dropout)
        self.modelo_regresion = load_model(config.RUTA_MODELS / 'model1.keras')

        # Modelo 2: Clasificación Multiclase (Versión A)
        self.modelo_clasificacion = load_model(config.RUTA_MODELS / 'model2.keras')

        self.etiquetas_riesgo = {
            1: "Sin riesgo",
            2: "Riesgo bajo",
            3: "Riesgo medio",
            4: "Riesgo alto / En peligro de reprobación"
        }

        self.niveles_alerta = {
            1: "Baja (Buen rendimiento)",
            2: "Moderada (Seguimiento regular)",
            3: "Alta (Alerta de apoyo académico)",
            4: "Crítica (Intervención urgente requerida)"
        }

    def _mapear_alerta(self, nivel_riesgo: int):
        requires_intervention = nivel_riesgo in (3, 4)
        alert_level = self.niveles_alerta.get(nivel_riesgo, "Desconocida")
        risk_label = self.etiquetas_riesgo.get(nivel_riesgo, f"Nivel {nivel_riesgo}")
        return alert_level, requires_intervention, risk_label

    def predecir_nota(self, datos_estudiante: dict) -> dict:
        """
        Consulta el Modelo 1 (Regresión con Dropout) para obtener la calificación final G3
        y evaluar el nivel de alerta derivado.
        """
        X = self.preprocesador.procesar_estudiante(datos_estudiante)
        prediccion = float(self.modelo_regresion.predict(X, verbose=0)[0][0])
        # Asegurar rango válido de 0 a 20
        nota_final = max(0.0, min(20.0, round(prediccion, 2)))

        nivel_riesgo = self.preprocesador.calcular_nivel_riesgo(nota_final)
        alert_level, requires_intervention, risk_label = self._mapear_alerta(nivel_riesgo)

        if nota_final >= 14:
            resumen = f"Estudiante con desempeño sobresaliente/satisfactorio. Nota final estimada: {nota_final}/20."
        elif nota_final >= 12:
            resumen = f"Estudiante en nivel aceptable pero con margen de mejora. Nota final estimada: {nota_final}/20."
        elif nota_final >= 10:
            resumen = f"Estudiante en zona limítrofe de aprobación. Nota final estimada: {nota_final}/20. Se sugiere seguimiento."
        else:
            resumen = f"ALERTA TEMPRANA: Nota final estimada de {nota_final}/20 (reprobación). Se requiere plan de intervención inmediato."

        return {
            "predicted_grade": nota_final,
            "grade_scale": "0-20",
            "risk_level": nivel_riesgo,
            "risk_label": risk_label,
            "alert_level": alert_level,
            "requires_intervention": requires_intervention,
            "summary": resumen,
            "model_used": "Modelo 1 - ANN Regresión (Versión A con Dropout)"
        }

    def predecir_riesgo(self, datos_estudiante: dict) -> dict:
        """
        Consulta el Modelo 2 (Clasificación Multiclase) para obtener la distribución de
        probabilidades y la categoría de riesgo predicha.
        """
        X = self.preprocesador.procesar_estudiante(datos_estudiante)
        probabilidades = self.modelo_clasificacion.predict(X, verbose=0)[0]

        clase_predicha = int(np.argmax(probabilidades) + 1)
        alert_level, requires_intervention, risk_label = self._mapear_alerta(clase_predicha)

        prob_dict = {
            "Sin riesgo (1)": round(float(probabilidades[0]), 4),
            "Riesgo bajo (2)": round(float(probabilidades[1]), 4),
            "Riesgo medio (3)": round(float(probabilidades[2]), 4),
            "Riesgo alto (4)": round(float(probabilidades[3]), 4)
        }

        confianza = prob_dict[f"{self.etiquetas_riesgo[clase_predicha].split(' / ')[0]} ({clase_predicha})"]
        resumen = (
            f"El estudiante fue clasificado en '{risk_label}' con una certeza del {confianza * 100:.1f}%. "
            f"Alerta: {alert_level}."
        )

        return {
            "risk_level": clase_predicha,
            "risk_label": risk_label,
            "probabilities": prob_dict,
            "alert_level": alert_level,
            "requires_intervention": requires_intervention,
            "summary": resumen,
            "model_used": "Modelo 2 - ANN Clasificación Multiclase (Versión A)"
        }


# Instancia singleton para reutilizar modelos cargados en memoria
predictor_service = PredictorService()
