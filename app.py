import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
import awswrangler as wr
import redshift_connector

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno
redshift_database = os.getenv('redshift_database')
redshift_table = os.getenv('redshift_table')
redshift_user = os.getenv('redshift_user')
redshift_password = os.getenv('redshift_password')
redshift_port = os.getenv('redshift_port')
redshift_host = os.getenv('redshift_host')
redshift_schema = os.getenv('redshift_schema')

# Título de la aplicación
st.title('Bitcoin Trade Guru')

# Descripción
st.write("Bitcoin Trade Guru es una aplicación que me permite visualizar la corizacion del Bitcoin a lo largo de 1 año y de 30 dias.")
st.header("Análisis de VWAP y Precio de Apertura")
st.markdown("""
    - **VWAP:** Precio promedio ponderado por volumen.
    - **Precio de Apertura:** Valor inicial del Bitcoin.
    - **Análisis:** Comparar ambos valores nos ayuda a:
      - Inferir si el BTC está en **alza o baja**.
      - Sugerir un consejo de **compra o venta**.
""")

# Inicializar la conexión a la base de datos Redshift
conn = None

df = None

try:
    conn = redshift_connector.connect(
        host=redshift_host,
        database=redshift_database,
        user=redshift_user,
        password=redshift_password,
        port=int(redshift_port)  # Convierte el puerto a entero
    )

    try:
        # Ejecutar una consulta
        query = f'SELECT * FROM "{redshift_schema}"."{redshift_table}";'
        df = wr.redshift.read_sql_query(query, con=conn)  # Cambiado a wr.redshift
    except Exception as query_error:
        st.error(f"Ocurrió un error al ejecutar la consulta: {query_error}")

finally:
    if conn:
        conn.close()  # Asegúrate de cerrar la conexión

if df is not None:
    try:
        # Título de la aplicación
        st.title('Datos de cotizacion BTC a lo largo de 1 año')
        # Mostrar el DataFrame
        st.write(df)

        # Pasamos la coluna fecha a formato datetime
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        ######################################################
        # Configurar el título de la aplicación
        st.title("Cotización BTC x 1 Año")

        # Crear el gráfico de líneas
        fig, ax = plt.subplots(figsize=(10, 5))

        # Graficar las columnas seleccionadas
        ax.plot(df['fecha'], df['precio_apertura'], label='Precio de Apertura', marker='o')
        ax.plot(df['fecha'], df['precio_cierre'], label='Precio de Cierre', marker='o')
        ax.plot(df['fecha'], df['precio_maximo'], label='Precio Máximo', marker='o')
        ax.plot(df['fecha'], df['precio_minimo'], label='Precio Mínimo', marker='o')

        # Configuración del gráfico
        ax.set_title("Cotización BTC x 30 días")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valores")

        # Formato de las fechas en el eje X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Establecer la ubicación de las etiquetas en el eje X
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))  # Mostrar cada 10 días

        # Rotar las etiquetas del eje X
        plt.xticks(rotation=45)

        ax.legend()
        ax.grid()

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        ###############################################################################
        # Filtrar los últimos 30 días
        ultimos_30_dias = df[df['fecha'] >= (df['fecha'].max() - pd.Timedelta(days=30))]

        # Configurar el título de la aplicación
        st.title("Cotización BTC x 30 días")

        # Crear el gráfico de líneas
        fig, ax = plt.subplots(figsize=(10, 5))

        # Graficar las columnas seleccionadas
        ax.plot(ultimos_30_dias['fecha'], ultimos_30_dias['precio_apertura'], label='Precio de Apertura', marker='o')
        ax.plot(ultimos_30_dias['fecha'], ultimos_30_dias['precio_cierre'], label='Precio de Cierre', marker='o')
        ax.plot(ultimos_30_dias['fecha'], ultimos_30_dias['vw_aprice'], label='VWAP', marker='o') 

        # Configuración del gráfico
        ax.set_title("Precios de BTC en los últimos 30 días")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valores")

        # Formato de las fechas en el eje X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Rotar las etiquetas del eje X
        plt.xticks(rotation=45)

        ax.legend()
        ax.grid()

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        ###########################################################################################################
        #Para graficar si debo comprar o vender
        ##########################################################################################################
        # Obtener la fila con la fecha más reciente
        st.title("Sugerencia para operar BTC")
        
        try:
            fila_actual = df.loc[df["fecha"].idxmax()]
            # Comparar vw_aprice con precio_cierre
            if fila_actual["vw_aprice"] > fila_actual["precio_apertura"]:
                color = "green"
                leyenda = "COMPRAR\n\nVWAP > Precio de Apertura"
            else:
                color = "red"
                leyenda = "VENDER\n\nVWAP < Precio de Apertura"

            # Crear el gráfico con matplotlib
            fig, ax = plt.subplots(figsize=(4, 4))

            # Dibujar el rectángulo con el color adecuado
            rect = plt.Rectangle((0, 0), 1, 1, color=color)
            ax.add_patch(rect)

            # Agregar la leyenda dentro del rectángulo
            ax.text(0.5, 0.5, leyenda, ha='center', va='center', fontsize=12, color='white', weight='bold')

            # Ajustar límites del gráfico y quitar los ejes
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)
        except Exception as suggestion_error:
            st.error(f"Ocurrió un error al generar la sugerencia de compra/venta: {suggestion_error}")

    except Exception as graph_error:
        st.error(f"Ocurrió un error al generar los gráficos: {graph_error}")
else:
    st.error("No se pudo obtener ningún dato de la base de datos.")