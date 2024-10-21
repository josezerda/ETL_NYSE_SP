# 📈 Bitcoin Trade Guru
Este repositorio contiene un pipeline ETL (Extract, Transform, Load) diseñado para analizar el precio del Bitcoin BTC y sugerirnos como operar. Obtenemos los datos a traves de una API (Polygon.io) y utilizando un analisis técnico financiero podemos obtener un consejo de como operar.

Utilizamos las siguientes herramientas:

-   Apache Airflow
-   Redshift
-   Docker
-   APIs financieras
-   El pipeline automatiza la consulta de los datos historicos y la creacion de datos procesados en el data warehouse Redshift, facilitando su análisis y manipulación.
-   Además de la creación de una aplicacion que mediante graficos para observar los valores y nos brinda consejos para poder operar.

## 🚀 Características
Integración con APIs: Recupera datos de precios de BTC usando la API financiera Polygon.io.
Pipeline ETL: Organizado en 3 fases (Extracción, Transformacion y Guardado de datos) de las cotizaciones historicas de BTC
Creación automática de tablas: Genera tablas en Amazon Redshift para almacenar los datos de stock.
Contenerización con Docker: Configurado para ejecutarse en un entorno Dockerizado, aprovechando Airflow, PostgreSQL y Stremlit ejecutandose mediante Docker Compose.
Gráfico: Utilizando Streamlit se realiza un grafico para observar la cotizacion anual del BTC, ademas del precio de apertura, mayor precio, menor precio, precio de cierre, volumen y el precio promedio ponderado por volumen.

## 📁 Estructura del Proyecto

```plaintext
├── dags                    # Definición de DAGs para Apache Airflow
├── config                  # Configuración del proyecto
├── logs                    # Logs generados por Airflow
├── plugins                 # Plugins personalizados de Airflow
├── tasks                   # Funciones individuales del pipeline
├── Dockerfile              # Definición de la imagen Docker para Airflow
├── Dockerfile.streamlit    # Definición de la imagen Docker para la app web Stremlit
├── docker-compose.yaml     # Configuración de Docker Compose
├── requirements.txt        # Dependencias del proyecto
├── `app.py`                # Script de la app web Stremlit
├── makefile                # Archivo Makefile para automatizar implementación
└── `README.md`             # Documentación del proyecto
```

#### Tabla de Hechos (fact):
- **btc_anual**: Almacena los precios diarios de la cotizacion de BTC, como asi tambien todas las variables financieras vinculadas a dicha cotizacion.

## 🛠️ Instalación y Configuración
### Prerrequisitos

- Docker
- AWS Redshift
- Airflow
- Python

### Paso a Paso

#### 1. Clonar repositorio
```bash
git clone https://github.com/josezerda/ETL_NYSE_SP.git
cd ETL_NYSE_SP
```

#### 2. Configurar variables de entorno
Define las variables necesarias en un archivo `.env`:

```bash
# APIs keys
API_KEY='your_api_key'
SIMBOL='BTCUSD'

# DB Redshift 
redshift_database = 'your_dbname'
redshift_table = 'your:table'
redshift_user = 'your_user'
redshift_password = 'your_pass'
redshift_port = port
redshift_host = 'your_host_redshift'
redshift_schema = 'your_schema'  
```


#### 3. Correr Makefile
El Makefile automatiza la creación de directorios necesarios y la configuración del entorno para utilizar Airflow y Streamlit. Incluye comandos para construir las imágenes de Docker tanto de Airflow como de Stremlit.

Simplemente ejecuta el siguiente comando para realizar todas estas tareas de manera secuencial:
```bash
make build
```

#### 3. Ejecutar docker compose up -d
Ejecute el siguiente comando Bash para correr todos los servicios definidos en tu archivo docker-compose.yml.
```bash
docker compose up -d
```
#### 4. Acceder a la interfaz de Airflow
Visita http://localhost:8080 en tu navegador. El usuario y la contraseña predeterminados son airflow para ambos.

#### 5. Acceder a la interfaz de Streamlit
Visita http://localhost:8501 en tu navegador. Se vera el grafico con los datos de las cotizaciones historicas BTC y la sugerencia para operar.

> **Nota 1**: El pipeline esta configurado para correr cada 10 minutos, ya que la cotizacion BTC es durante las 24 horas

## 📊 Estructura del Pipeline
El pipeline está dividido en tres capas principales, siguiendo el modelo de ETL:

**DAG**: get_data 

**Scripts:**:
get_data.py: Recupera los precios diarios de la cotizacion del BTC desde la API de Polygon.io a lo largo de todo un año. Devuelve un DataFrame con los precios de apertura, máximo, mínimo, cierre y volumen. Estos datos los almacena en formato .csv


**DAG**: insert_data Scripts:
**Scripts:**:
insert_data.py: Toma los archivos .csv que se generaron a traves de las consultas a la API, los procesa a efectos de poder utilizarmos como variables financieras y los inserta en una tabla en la base de datos Redshift (btc_anual).

## ✨ Sugerencia en Implementaciones Futuras

- Sugerir operar siguiendo una escala (Highly Recommended y Slightly Recommended)
- A traves de una API de Binance poder operar automaticamente si intervencion humana.