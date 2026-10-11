# Configuración del proyecto: rutas y parámetros que se usan en varios archivos
from pathlib import Path

# Carpeta principal del proyecto (se calcula sola, así funciona desde notebooks/ o api/)
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Rutas de los datos y modelos
RUTA_RAW = RUTA_PROYECTO / 'data' / 'raw'
RUTA_PROCESSED = RUTA_PROYECTO / 'data' / 'processed'
RUTA_MODELS = RUTA_PROYECTO / 'models'

# Parámetros de la división train/test (los mismos del profe)
TEST_SIZE = 0.2
RANDOM_STATE = 101

# Máximo de faltas según el diccionario de datos
MAX_AUSENCIAS = 93

# Rangos válidos de cada variable numérica según el diccionario de datos
RANGOS_VALIDOS = {
    'age': (15, 22), 'Medu': (0, 4), 'Fedu': (0, 4),
    'traveltime': (1, 4), 'studytime': (1, 4), 'failures': (0, 4),
    'famrel': (1, 5), 'freetime': (1, 5), 'goout': (1, 5),
    'Dalc': (1, 5), 'Walc': (1, 5), 'health': (1, 5),
    'absences': (0, 93), 'G1': (0, 20), 'G2': (0, 20), 'G3': (0, 20)
}