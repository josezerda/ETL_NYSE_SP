# get_data.py
import requests
import pandas as pd
import sys
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno API_KEY
api_key = os.getenv('API_KEY')
simbol = os.getenv('SIMBOL')

# Obtiene la fecha y hora actuales y de 1 año atras
fecha_actual = datetime.now()
fecha_inicio = fecha_actual - timedelta(days=365)

# Formatea la fecha para mostrar solo el año, mes y día
fecha_actual_dias = fecha_actual.strftime('%Y-%m-%d')
fecha_inicio_dias = fecha_inicio.strftime('%Y-%m-%d')

#Armo la url
url = 'https://api.polygon.io/v2/aggs/ticker/X:' + simbol + '/range/1/day/' + fecha_inicio_dias + '/' + fecha_actual_dias + '?sort=asc&apiKey=' + api_key


# Especificar el directorio donde se guardará el archivo CSV
output_dir = os.path.join(os.environ['AIRFLOW_HOME'], 'dags', 'data')
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe
output_file = os.path.join(output_dir, 'btcusd_data.csv')


try:
    response = requests.get(url)
    response.raise_for_status()  # Esto lanzará un error si la respuesta no es exitosa
    data = response.json()
    results = data.get('results', [])
    
    # Crear un DataFrame desde la lista de resultados
    df = pd.DataFrame(results)
    df = df.rename(columns={
        'v': 'volumen',
        'vw': 'vw_aprice',
        'o': 'precio_apertura',
        'c': 'precio_cierre',
        'h': 'precio_maximo',
        'l': 'precio_minimo',
        't': 'timestamp',
        'n': 'numero_transacciones'
        })
    
    # Convertir la columna 'timestamp' a datetime
    df['Fecha'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Opcional: eliminar la columna original de timestamp si ya no la necesitas
    df = df.drop(columns=['timestamp'])
    print(df)
    
    # Guardar el DataFrame en el archivo CSV
    df.to_csv(output_file, index=False)
    print(f"Datos de NYSE recolectados y guardados en '{output_file}'.")
except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
    sys.exit(1)