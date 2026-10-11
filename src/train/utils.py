import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from src import config


class ModeloBase:
    # Clase padre con lo que comparten los modelos (regresión y clasificación):
    # preparar los datos, entrenar, graficar las pérdidas y guardar.
    # Cada clase hija define cómo se crea la red (crear) y cómo se evalúa (evaluar).

    def __init__(self, nombre, usar_dropout=False):
        self.nombre = nombre  # nombre para tablas y gráficos
        self.usar_dropout = usar_dropout  # True = con Dropout, False = sin Dropout
        self.objetivo = None  # columna a predecir (la define cada clase hija)
        self.columnas_quitar = []  # columnas que no son entradas (las define cada clase hija)
        self.scaler = None
        self.modelo = None  # la red neuronal de Keras
        self.historial = None  # pérdidas de cada epoch (loss y val_loss)

    def preparar_datos(self, train, test):
        # Separa entradas (X) y salida (y) y escala con un MinMaxScaler ajustado SOLO con train
        X_train = train.drop(self.columnas_quitar, axis=1)
        X_test = test.drop(self.columnas_quitar, axis=1)
        y_train = train[self.objetivo]
        y_test = test[self.objetivo]

        self.scaler = MinMaxScaler()
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        X_test = self.scaler.transform(X_test)
        return X_train, X_test, y_train, y_test

    def crear(self, num_entradas):
        # Cada clase hija define su propia arquitectura
        raise NotImplementedError('La clase hija debe definir el método crear()')

    def evaluar(self, X_test, y_test):
        # Cada clase hija define sus propias métricas
        raise NotImplementedError('La clase hija debe definir el método evaluar()')

    def entrenar(self, X_train, y_train, batch_size=32):
        # Fija el azar para que el resultado sea el mismo cada vez que se corre
        tf.keras.utils.set_random_seed(config.RANDOM_STATE)
        self.crear(X_train.shape[1])

        # EarlyStopping: detiene el entrenamiento si val_loss no mejora en 25 epochs seguidos
        early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1,
                                   patience=25, restore_best_weights=True)

        # validation_split: el 20% del entrenamiento se usa para validar (el test NO se toca)
        self.modelo.fit(x=X_train, y=y_train,
                        validation_split=0.2,
                        batch_size=batch_size, epochs=500,
                        callbacks=[early_stop], verbose=0)

        self.historial = pd.DataFrame(self.modelo.history.history)
        return self.historial

    def graficar_perdidas(self):
        # Curvas de pérdida de entrenamiento (loss) y validación (val_loss)
        self.historial.plot(title=self.nombre)
        plt.xlabel('Epoch')
        plt.show()

    def guardar(self, nombre_archivo):
        # Guarda la red neuronal en la carpeta models/ en formato Keras
        self.modelo.save(config.RUTA_MODELS / nombre_archivo)