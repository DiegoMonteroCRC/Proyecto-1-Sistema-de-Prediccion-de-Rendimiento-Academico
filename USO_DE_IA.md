# Documentación de Uso de Inteligencia Artificial

**Curso:** BD-151 Inteligencia Artificial Aplicada  
**Institución:** Colegio Universitario de Cartago (CUC)  
**Año:** 2026  
**Proyecto:** Proyecto C - Sistema de Predicción de Rendimiento Académico y Detección de Riesgo  
**Integrantes:**
- Luis Diego Montero Vargas
- Mariana Méndez Pérez
- Nadin Rojas López
- Claret Rodríguez Jiménez

---

## 1. Herramientas de IA utilizadas y tareas específicas

Durante el desarrollo del proyecto se utilizaron modelos de lenguaje y asistentes de código basados en IA (Claude 3.7 Sonnet, Gemini 2.5 Pro y ChatGPT) como herramientas de apoyo para las siguientes tareas específicas:


- **Depuración de errores de sintaxis y compilación:** Identificación y corrección de inconsistencias en métodos de Keras (por ejemplo, llamadas anidadas erróneas en `model.compile()`).
- **Implementación de la API REST:** Asistencia en la creación de esquemas de validación de datos con Pydantic (`StudentInput`) y configuración de endpoints con FastAPI (`/predict/grade` y `/predict/risk_level`).
- **Desarrollo del Frontend en Streamlit:** Generación de la estructura del dashboard, organización modular de pestañas (factores académicos, personales y familiares) y configuración de estilos CSS oscuros para proyección nocturna.

---

## 2. Ejemplos de prompts representativos utilizados

A continuación se documentan 5 prompts reales representativos utilizados durante el desarrollo del proyecto:

### Prompt 1: Optimización de precisión y arquitectura del Modelo 2
> *"Veo que el modelo2 es mucho menos preciso que el que tenemos en el modelo1. Hay alguna manera de ajustar los valores sin comprometer la estructura del script para que el modelo2 sea mucho mas preciso que como lo tenemos actualmente? Ocupamos clasificar en 4 niveles de riesgo."*
* **Propósito:** Analizar la diferencia metodológica entre una tarea de regresión y una de clasificación multiclase, optimizando la tasa de aprendizaje (`learning_rate=0.0004` en Adam) y la distribución de neuronas por capa.

### Prompt 2: Depuración de error en método de compilación de Keras
> *"Tengo esta función pero no corre, cual es el error?:*
> ```python
> self.modelo.compile(
>     optimizer = Adam(learning_rate=0.0004)
>     self.modelo.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy']),
>     loss='categorical_crossentropy',
>     metrics=['accuracy']
> )
> ```
* **Propósito:** Resolver una sintaxis inválida donde se había anidado una segunda llamada recursiva a `self.modelo.compile()` dentro de los argumentos del compilador de Keras.

### Prompt 3: Separación y claridad de las curvas de entrenamiento
> *"Ok lo vamos a hacer diferente. En los graficos estamos mostrando accuracy, loss, val_accuracy y val_loss todos juntos pero mejor los vamos a separar. Modifica el código para que esos graficos estén separados agrupando loss con val_loss y accuracy con val_accuracy, explicando la interpretación de los resultados de la forma más clara y simple posible."*
* **Propósito:** Evitar la saturación visual en los notebooks y en las métricas, desacoplando la métrica de función de costo de la métrica de exactitud clasificatoria.

---

## 3. Reflexión sobre cómo la IA ayudó en nuestro aprendizaje

El uso de herramientas de Inteligencia Artificial a lo largo de este proyecto funcionó como un tutor técnico continuo y un acelerador de productividad. En lugar de limitarse a copiar soluciones preconcebidas, el equipo debió analizar críticamente cada respuesta: entender por qué un problema de clasificación en 4 categorías discretas requiere codificación One-Hot, mientras que uno de regresión continua emplea error cuadrático medio, o comprender el impacto real del sobreajuste al contrastar el comportamiento de las curvas de entrenamiento frente a las de validación.

---

## 4. Modificaciones realizadas al código y análisis generado por IA

Cada artefacto sugerido por la IA fue revisado, validado y modificado por el equipo para alinearse con los requerimientos específicos del curso y la lógica del problema:

1. **Prevención estricta de Data Leakage:** La IA inicialmente incluía columnas correlacionadas en el conjunto de entrenamiento. El equipo verificó y forzó la exclusión explícita de `G3` y `nivel_riesgo` del conjunto de variables predictoras $X$ en el Modelo 2 para evitar fugas de información.
2. **Ajuste y desacople de funciones de graficación:** En las utilidades base (`src/train/utils.py`), se corrigió el método `graficar_perdidas()` que originalmente graficaba todas las columnas del historial juntas, separándolo en dos métodos especializados: uno exclusivo para pérdidas (`loss` y `val_loss`) y otro para exactitud (`accuracy` y `val_accuracy`).
3. **Calibración del optimizador:** Se probó y ajustó experimentalmente el hiperparámetro `learning_rate` en Adam, bajándolo a `0.0004` para garantizar una convergencia suave y evitar divergencias oscilatorias en las épocas iniciales.
4. **Generador aleatorio con restricciones de negocio:** Se programó la lógica de generación aleatoria para que las notas previas ($G1$ y $G2$), las ausencias y las variables categóricas mantuvieran coherencia con la distribución real del dataset, evitando datos inverosímiles en las pruebas del dashboard.

