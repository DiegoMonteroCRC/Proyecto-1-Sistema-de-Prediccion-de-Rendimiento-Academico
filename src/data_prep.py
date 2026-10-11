import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from src import config


class Preprocesador:
    # Clase que prepara los datos de los estudiantes para los modelos

    def __init__(self):
        # Atributos donde se van guardando los datos en cada paso
        self.df = None          # datos unidos de las dos materias
        self.df_post = None     # datos con las variables dummy
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.columnas = None    # columnas finales después de get_dummies

    # ---------------- 2. Carga de datos ----------------

    def cargar_datos(self):
        # Lee los dos archivos (vienen separados por ';') y los une en uno solo
        df_mat = pd.read_csv(config.RUTA_RAW / 'student-mat.csv', sep=';')
        df_por = pd.read_csv(config.RUTA_RAW / 'student-por.csv', sep=';')

        # Columna para saber de qué materia es cada estudiante
        df_mat['materia'] = 'matematicas'
        df_por['materia'] = 'portugues'

        self.df = pd.concat([df_mat, df_por], ignore_index=True)
        return self.df

    # ---------------- 3.1 Limpieza inicial ----------------

    def revisar_nulos(self):
        # Cantidad de valores nulos por columna
        return self.df.isnull().sum()

    def revisar_duplicados(self):
        # Cantidad de filas duplicadas
        return self.df.duplicated().sum()

    def revisar_casos_extremos(self):
        # Estudiantes con nota final 0 y con muchas faltas
        ceros = self.df[self.df['G3'] == 0]
        print('Estudiantes con G3 = 0:', len(ceros))
        print('Por materia:', ceros['materia'].value_counts().to_dict())
        print('Con absences = 0:', (ceros['absences'] == 0).sum())
        print('Con G2 = 0:', (ceros['G2'] == 0).sum())
        print('Estudiantes con 30 o más faltas:', (self.df['absences'] >= 30).sum())
        return ceros[['materia', 'absences', 'G1', 'G2', 'G3']]

    def validar_categorias(self):
        # Valores únicos de cada columna de texto, para detectar errores de escritura
        columnas_texto = self.df.select_dtypes(exclude='number').columns
        for col in columnas_texto:
            print(col, list(self.df[col].unique()))

    def validar_rangos(self):
        # Verifica que cada variable numérica esté dentro de su rango válido (diccionario de datos)
        for col, (minimo, maximo) in config.RANGOS_VALIDOS.items():
            fuera_de_rango = ((self.df[col] < minimo) | (self.df[col] > maximo)).sum()
            print(col, '- rango', minimo, 'a', maximo, '- valores fuera de rango:', fuera_de_rango)

    # ---------------- 3.3 Limpieza final ----------------

    def crear_variables_derivadas(self):
        # Promedio de las notas parciales (usa G1 y G2) y tasa de ausencias
        self.df['promedio_notas'] = (self.df['G1'] + self.df['G2']) / 2
        self.df['tasa_ausencias'] = self.df['absences'] / config.MAX_AUSENCIAS
        return self.df[['G1', 'G2', 'promedio_notas', 'absences', 'tasa_ausencias']].head()

    def calcular_nivel_riesgo(self, g3):
        # Nivel de riesgo según la nota final (en Portugal se aprueba con 10)
        if g3 >= 14:
            return 1  # Sin riesgo
        elif g3 >= 12:
            return 2  # Riesgo bajo
        elif g3 >= 10:
            return 3  # Riesgo medio
        else:
            return 4  # Riesgo alto

    def crear_nivel_riesgo(self):
        # Crea la variable objetivo del Modelo 2 a partir de G3
        self.df['nivel_riesgo'] = self.df['G3'].apply(lambda x: self.calcular_nivel_riesgo(x))
        return self.df['nivel_riesgo'].value_counts().sort_index()

    def transformar_categoricas(self):
        # Convierte las columnas de texto en columnas dummy de 0 y 1
        columnas_categoricas = self.df.select_dtypes(exclude='number').columns.tolist()
        dummies = pd.get_dummies(self.df[columnas_categoricas], dtype=int)
        self.df_post = pd.concat([self.df, dummies], axis=1)
        self.df_post = self.df_post.drop(columnas_categoricas, axis=1)
        return self.df_post.shape

    def correlacion_con_g3(self):
        # Correlación de cada variable con la nota final
        return self.df_post.corr(numeric_only=True)['G3'].sort_values()

    # ---------------- 4. Train Test Split ----------------

    def dividir(self):
        # Separa entradas (X) y salidas (y): G3 para el Modelo 1 y nivel_riesgo para el Modelo 2
        variables_objetivo = ['G3', 'nivel_riesgo']
        X = self.df_post.drop(variables_objetivo, axis=1)
        y = self.df_post[variables_objetivo]
        self.columnas = X.columns.tolist()

        # 80% entrenamiento / 20% prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE)
        return self.X_train.shape, self.X_test.shape

    # ---------------- 5. Escalado ----------------

    def escalar(self):
        # El scaler se ajusta SOLO con los datos de entrenamiento
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.X_train)
        X_train_esc = self.scaler.transform(self.X_train)
        X_test_esc = self.scaler.transform(self.X_test)
        return X_train_esc.max(), X_train_esc.min()

    # ---------------- 6. Guardar ----------------

    def guardar(self):
        # Guarda train y test SIN escalar (con G3 y nivel_riesgo) y el scaler y las columnas para la API
        train = pd.concat([self.X_train, self.y_train], axis=1)
        test = pd.concat([self.X_test, self.y_test], axis=1)
        train.to_csv(config.RUTA_PROCESSED / 'train.csv', index=False)
        test.to_csv(config.RUTA_PROCESSED / 'test.csv', index=False)
        joblib.dump(self.scaler, config.RUTA_MODELS / 'scaler.pkl')
        joblib.dump(self.columnas, config.RUTA_MODELS / 'columnas.pkl')
        return train.shape, test.shape

    # ---------------- Para la API: preparar un estudiante nuevo ----------------

    def cargar_scaler_y_columnas(self):
        # Carga el scaler y las columnas que se guardaron en el preprocesamiento
        self.scaler = joblib.load(config.RUTA_MODELS / 'scaler.pkl')
        self.columnas = joblib.load(config.RUTA_MODELS / 'columnas.pkl')

    def procesar_estudiante(self, datos):
        # Recibe los datos de un estudiante (diccionario) y los prepara igual que en el entrenamiento
        df = pd.DataFrame([datos])
        df['promedio_notas'] = (df['G1'] + df['G2']) / 2
        df['tasa_ausencias'] = df['absences'] / config.MAX_AUSENCIAS
        df = pd.get_dummies(df, dtype=int)
        # Deja las mismas columnas y en el mismo orden que en el entrenamiento (las que falten van en 0)
        df = df.reindex(columns=self.columnas, fill_value=0)
        return self.scaler.transform(df)