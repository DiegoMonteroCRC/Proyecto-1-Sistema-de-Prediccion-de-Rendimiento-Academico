import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from src.train.utils import ModeloBase


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Matriz de Confusión',
                          cmap=plt.cm.Blues):

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Matriz de confusión normalizada")
    else:
        print("Matriz de confusión sin normalizar")

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('Clase Real')
    plt.xlabel('Clase Predicha')
    plt.tight_layout()


class ModeloClasificacion(ModeloBase):

    def __init__(self, version='A', usar_dropout=False):
        nombre = 'Versión ' + version + (' con Dropout' if usar_dropout else ' sin Dropout')
        super().__init__(nombre, usar_dropout)
        self.version = version
        self.objetivo = 'nivel_riesgo'
        self.clases = [1, 2, 3, 4]
        self.nombres_clases = [
            'Sin riesgo (1)',
            'Riesgo bajo (2)',
            'Riesgo medio (3)',
            'Riesgo alto (4)'
        ]
        self.num_clases = len(self.clases)

        
        if version == 'A':
            self.columnas_quitar = ['nivel_riesgo', 'G3']
        else:
            self.columnas_quitar = ['nivel_riesgo', 'G3', 'G1', 'G2', 'promedio_notas']

    def codificar_y(self, y):
        """
        Convierte la variable objetivo en One-Hot Encoding con 4 clases
        """
        dummies = pd.get_dummies(y, dtype=int)
        return dummies.reindex(columns=self.clases, fill_value=0).values

    def preparar_datos(self, train, test):
        """
        Usa la lógica de escalado de ModeloBase y transforma y_train a One-Hot.
        y_test se conserva en etiquetas enteras (1 a 4) para las métricas de evaluación.
        """
        X_train, X_test, y_train, y_test = super().preparar_datos(train, test)
        y_train_cat = self.codificar_y(y_train)
        return X_train, X_test, y_train_cat, y_test

    def crear(self, num_entradas): #red neuronal con 2 capas ocultas y función de activación ReLU, con opción de Dropout

        self.modelo = Sequential()
        self.modelo.add(Dense(num_entradas, activation='relu'))
        if self.usar_dropout:
            self.modelo.add(Dropout(0.2))
        self.modelo.add(Dense(num_entradas // 2, activation='relu'))
        if self.usar_dropout:
            self.modelo.add(Dropout(0.2))
        self.modelo.add(Dense(self.num_clases, activation='softmax'))

        self.modelo.compile(
            optimizer=Adam(learning_rate=0.0004),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return self.modelo

    def predecir(self, X): 

        probabilidades = self.modelo.predict(X, verbose=0)
        return np.argmax(probabilidades, axis=-1) + 1

    def predecir_proba(self, X): 

        return self.modelo.predict(X, verbose=0)

    def evaluar(self, X_test, y_test):

        predicciones = self.predecir(X_test)
        acc = accuracy_score(y_test, predicciones)
        prec = precision_score(y_test, predicciones, average='weighted', zero_division=0)
        rec = recall_score(y_test, predicciones, average='weighted', zero_division=0)
        f1 = f1_score(y_test, predicciones, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, predicciones, labels=self.clases)
        reporte = classification_report(
            y_test,
            predicciones,
            labels=self.clases,
            target_names=self.nombres_clases,
            zero_division=0
        )

        return {
            'Modelo': self.nombre,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1': f1,
            'Matriz Confusion': cm,
            'Reporte': reporte
        }

    def graficar_matriz_confusion(self, X_test, y_test, normalize=False):

        predicciones = self.predecir(X_test)
        cm = confusion_matrix(y_test, predicciones, labels=self.clases)
        plt.figure(figsize=(6, 5))
        plot_confusion_matrix(
            cm,
            classes=self.nombres_clases,
            normalize=normalize,
            title=f'Matriz de Confusión - {self.nombre}'
        )
        plt.show()


    def graficar_perdidas(self):

        plt.figure(figsize=(8, 4.5))
        plt.plot(self.historial['loss'], label='loss (entrenamiento)', color='#1f77b4', linewidth=2)
        plt.plot(self.historial['val_loss'], label='val_loss (validación)', color='#ff7f0e', linewidth=2)
        plt.title(f'{self.nombre} - Curva de Pérdida (Loss vs Val Loss)', fontsize=12)
        plt.xlabel('Epoch', fontsize=10)
        plt.ylabel('Pérdida (Categorical Crossentropy)', fontsize=10)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def graficar_precision(self):

        plt.figure(figsize=(8, 4.5))
        plt.plot(self.historial['accuracy'], label='accuracy (entrenamiento)', color='#2ca02c', linewidth=2)
        plt.plot(self.historial['val_accuracy'], label='val_accuracy (validación)', color='#d62728', linewidth=2)
        plt.title(f'{self.nombre} - Curva de Precisión (Accuracy vs Val Accuracy)', fontsize=12)
        plt.xlabel('Epoch', fontsize=10)
        plt.ylabel('Precisión (Tasa de aciertos: 0 a 1)', fontsize=10)
        plt.ylim(0, 1.05)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
