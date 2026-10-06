import pandas as pd
from ucimlrepo import fetch_ucirepo

# Descargar el dataset
statlog_german_credit_data = fetch_ucirepo(id=144)

X = statlog_german_credit_data.data.features
y = statlog_german_credit_data.data.targets

df = pd.concat([X, y], axis=1)

# Renombrar las columnas
column_mapping = {
    'Attribute1': 'checking_status',
    'Attribute2': 'duration_months',
    'Attribute3': 'credit_history',
    'Attribute4': 'purpose',
    'Attribute5': 'credit_amount',
    'Attribute6': 'savings_account',
    'Attribute7': 'employment_years',
    'Attribute8': 'installment_rate',
    'Attribute9': 'personal_status_sex',
    'Attribute10': 'other_debtors',
    'Attribute11': 'residence_since',
    'Attribute12': 'property',
    'Attribute13': 'age',
    'Attribute14': 'other_installment_plans',
    'Attribute15': 'housing',
    'Attribute16': 'existing_credits',
    'Attribute17': 'job',
    'Attribute18': 'people_liable',
    'Attribute19': 'telephone',
    'Attribute20': 'foreign_worker',
    'class': 'target',
}

df = df.rename(columns=column_mapping) #Comentar esta línea para descargar con nombre de columnas original

#ruta_archivo = r'C:\Proyecto_C_Rendimiento_Academico\data\raw\Original_UCI_Credit_Data.csv'
ruta_archivo = r'C:\Proyecto_C_Rendimiento_Academico\data\raw\Renombrado_UCI_Credit_Data.csv'


# Guardar en CSV
df.to_csv(ruta_archivo, index=False)
print(f'Dataset guardado exitosamente en: {ruta_archivo}')

# 4. Cargar para verificar
df_cargado = pd.read_csv(ruta_archivo)
print(df_cargado.head())