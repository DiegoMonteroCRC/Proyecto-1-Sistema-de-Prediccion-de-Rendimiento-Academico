from typing import Dict, Optional
from pydantic import BaseModel, Field


class StudentInput(BaseModel):
    """
    Esquema de entrada con todas las variables del estudiante según el diccionario de datos.
    """
    materia: str = Field("matematicas", description="Materia: 'matematicas' o 'portugues'")
    school: str = Field("GP", description="Escuela: 'GP' (Gabriel Pereira) o 'MS' (Mousinho da Silveira)")
    sex: str = Field("F", description="Sexo: 'F' (Femenino) o 'M' (Masculino)")
    age: int = Field(16, ge=15, le=22, description="Edad del estudiante (15 a 22)")
    address: str = Field("U", description="Tipo de domicilio: 'U' (Urbano) o 'R' (Rural)")
    famsize: str = Field("GT3", description="Tamaño de familia: 'LE3' (<=3) o 'GT3' (>3)")
    Pstatus: str = Field("T", description="Estado de cohabitación de los padres: 'T' (Juntos) o 'A' (Separados)")
    Medu: int = Field(2, ge=0, le=4, description="Educación de la madre (0: Ninguna a 4: Superior)")
    Fedu: int = Field(2, ge=0, le=4, description="Educación del padre (0: Ninguna a 4: Superior)")
    Mjob: str = Field("other", description="Trabajo de la madre: 'teacher', 'health', 'services', 'at_home', 'other'")
    Fjob: str = Field("other", description="Trabajo del padre: 'teacher', 'health', 'services', 'at_home', 'other'")
    reason: str = Field("course", description="Razón de elección escolar: 'home', 'reputation', 'course', 'other'")
    guardian: str = Field("mother", description="Tutor legal: 'mother', 'father', 'other'")
    traveltime: int = Field(1, ge=1, le=4, description="Tiempo de viaje al colegio (1: <15 min a 4: >1 hora)")
    studytime: int = Field(2, ge=1, le=4, description="Tiempo semanal de estudio (1: <2 horas a 4: >10 horas)")
    failures: int = Field(0, ge=0, le=4, description="Número de materias reprobadas en el pasado (0 a 4)")
    schoolsup: str = Field("no", description="Apoyo educativo escolar adicional: 'yes' o 'no'")
    famsup: str = Field("yes", description="Apoyo educativo familiar: 'yes' o 'no'")
    paid: str = Field("no", description="Clases extracurriculares pagadas de la materia: 'yes' o 'no'")
    activities: str = Field("no", description="Actividades extracurriculares: 'yes' o 'no'")
    nursery: str = Field("yes", description="Asistió a guardería: 'yes' o 'no'")
    higher: str = Field("yes", description="Desea cursar educación superior: 'yes' o 'no'")
    internet: str = Field("yes", description="Acceso a Internet en el hogar: 'yes' o 'no'")
    romantic: str = Field("no", description="En una relación sentimental: 'yes' o 'no'")
    famrel: int = Field(4, ge=1, le=5, description="Calidad de las relaciones familiares (1: Muy mala a 5: Excelente)")
    freetime: int = Field(3, ge=1, le=5, description="Tiempo libre después de clases (1: Muy bajo a 5: Muy alto)")
    goout: int = Field(3, ge=1, le=5, description="Frecuencia de salidas con amigos (1: Muy baja a 5: Muy alta)")
    Dalc: int = Field(1, ge=1, le=5, description="Consumo de alcohol en días lectivos (1: Muy bajo a 5: Muy alto)")
    Walc: int = Field(1, ge=1, le=5, description="Consumo de alcohol en fines de semana (1: Muy bajo a 5: Muy alto)")
    health: int = Field(3, ge=1, le=5, description="Estado de salud actual (1: Muy malo a 5: Muy bueno)")
    absences: int = Field(2, ge=0, le=93, description="Número de ausencias escolares (0 a 93)")
    G1: float = Field(10.0, ge=0.0, le=20.0, description="Calificación del primer periodo (0 a 20)")
    G2: float = Field(10.0, ge=0.0, le=20.0, description="Calificación del segundo periodo (0 a 20)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "materia": "matematicas",
                "school": "GP",
                "sex": "F",
                "age": 16,
                "address": "U",
                "famsize": "GT3",
                "Pstatus": "T",
                "Medu": 3,
                "Fedu": 3,
                "Mjob": "services",
                "Fjob": "other",
                "reason": "course",
                "guardian": "mother",
                "traveltime": 1,
                "studytime": 2,
                "failures": 0,
                "schoolsup": "no",
                "famsup": "yes",
                "paid": "no",
                "activities": "yes",
                "nursery": "yes",
                "higher": "yes",
                "internet": "yes",
                "romantic": "no",
                "famrel": 4,
                "freetime": 3,
                "goout": 2,
                "Dalc": 1,
                "Walc": 2,
                "health": 4,
                "absences": 4,
                "G1": 13.0,
                "G2": 14.0
            }
        }
    }


class GradePredictionResponse(BaseModel):
    """
    Respuesta del endpoint /predict/grade (Modelo 1 - ANN Regresión Opción A con Dropout).
    """
    predicted_grade: float = Field(..., description="Calificación final esperada G3 (0 a 20)")
    grade_scale: str = Field("0-20", description="Escala de calificación")
    risk_level: int = Field(..., description="Nivel de riesgo derivado (1: Sin riesgo a 4: Alto)")
    risk_label: str = Field(..., description="Etiqueta textual del nivel de riesgo")
    alert_level: str = Field(..., description="Nivel de alerta ('Baja', 'Media', 'Alta', 'Crítica')")
    requires_intervention: bool = Field(..., description="Indica si el estudiante requiere intervención temprana")
    summary: str = Field(..., description="Mensaje explicativo del estado académico")
    model_used: str = Field("Modelo 1 - ANN Regresión (Versión A con Dropout)")


class RiskPredictionResponse(BaseModel):
    """
    Respuesta del endpoint /predict/risk_level (Modelo 2 - ANN Clasificación Multiclase).
    """
    risk_level: int = Field(..., description="Nivel de riesgo predicho (1 a 4)")
    risk_label: str = Field(..., description="Etiqueta del nivel de riesgo")
    probabilities: Dict[str, float] = Field(..., description="Distribución de probabilidades por nivel de riesgo")
    alert_level: str = Field(..., description="Nivel de alerta")
    requires_intervention: bool = Field(..., description="Indica si se activa la alerta temprana")
    summary: str = Field(..., description="Resumen descriptivo")
    model_used: str = Field("Modelo 2 - ANN Clasificación Multiclase (Versión A)")
