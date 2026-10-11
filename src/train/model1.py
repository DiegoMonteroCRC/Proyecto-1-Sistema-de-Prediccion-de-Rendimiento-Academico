import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score
from src.train.utils import ModeloBase


class ModeloRegresion(ModeloBase):
    # Modelo 1: predice la nota final G3 (regresión). Hereda de ModeloBase.
    # Versión A: con notas parciales G1 y G2.
    # Versión B: sin G1, G2 ni promedio_notas (alerta temprana).

    def __init__(self, version='A', usar_dropout=False):
        nombre = 'Versión ' + version + (' con Dropout' if usar_dropout else ' sin Dropout')
        super().__init__(nombre, usar_dropout)  # ejecuta el __init__ de la clase padre
        self.version = version
        self.objetivo = 'G3'

        # nivel_riesgo se quita siempre porque se calculó a partir de G3
        if version == 'A':
            self.columnas_quitar = ['G3', 'nivel_riesgo']
        else:
            self.columnas_quitar = ['G3', 'nivel_riesgo', 'G1', 'G2', 'promedio_notas']

    def crear(self, num_entradas):
        # 2 capas ocultas ReLU (la segunda con la mitad de neuronas) y salida de 1 neurona sin activación
        self.modelo = Sequential()
        self.modelo.add(Dense(num_entradas, activation='relu'))
        if self.usar_dropout:
            self.modelo.add(Dropout(0.2))  # apaga el 20% de las neuronas para evitar overfitting
        self.modelo.add(Dense(num_entradas // 2, activation='relu'))
        if self.usar_dropout:
            self.modelo.add(Dropout(0.2))
        self.modelo.add(Dense(1))  # regresión: 1 neurona sin función de activación
        self.modelo.compile(optimizer='adam', loss='mse')
        return self.modelo

    def evaluar(self, X_test, y_test):
        # Métricas de regresión con el conjunto de test
        predicciones = self.modelo.predict(X_test, verbose=0)
        return {'Modelo': self.nombre,
                'MAE': mean_absolute_error(y_test, predicciones),
                'RMSE': np.sqrt(mean_squared_error(y_test, predicciones)),
                'Varianza explicada': explained_variance_score(y_test, predicciones)}

    def predecir(self, X):
        # Devuelve la nota G3 estimada (0 a 20)
        return self.modelo.predict(X, verbose=0).ravel()