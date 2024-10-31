import pandas as pd
import sys
import os
from dotenv import load_dotenv
import awswrangler as wr
import redshift_connector

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener las variables de entorno
redshift_database = os.getenv('redshift_database')
redshift_table = os.getenv('redshift_table')
redshift_user = os.getenv('redshift_user')
redshift_password = os.getenv('redshift_password')
redshift_port = os.getenv('redshift_port')
redshift_host = os.getenv('redshift_host')
redshift_schema = os.getenv('redshift_schema')

def insert_data_function(csv_file):
    # Leer el archivo CSV
    try:
        df = pd.read_csv(csv_file)
        print(df)  # Procesa el DataFrame como desees

        # Parámetros de conexión
        conn_params = {
            'host': redshift_host,
            'database': redshift_database,
            'user': redshift_user,
            'password': redshift_password,
            'port': redshift_port,
        }

        # Conexión a la base de datos Redshift
        conn = redshift_connector.connect(**conn_params)

        # Cargar el DataFrame en Redshift
        wr.redshift.to_sql(
            df=df,
            con=conn,
            table=redshift_table,
            schema=redshift_schema,
            mode='overwrite',
            use_column_names=True,
            lock=True,
            index=False
        )

        print("Datos insertados en Redshift correctamente.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Por favor proporciona la ruta del archivo CSV.")
        sys.exit(1)

    csv_file = sys.argv[1]
    insert_data_function(csv_file)

if __name__ == '__main__':
    main()