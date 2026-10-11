import pandas as pd
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