# dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
import os
path = os.environ['AIRFLOW_HOME']

from datetime import timedelta, datetime

default_args = {
                'owner': 'airflow',
                'depends_on_past': False,
                'email': ['jozerda@gmail.com'],
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 2,
                'retry_delay': timedelta(minutes=1),
                'start_date': datetime.now() - timedelta(minutes=5),  # Ajusta la fecha de inicio
                }

# Define the DAG, its ID and when should it run.
dag = DAG(
            dag_id='stock_trend_dag',
            description='ETL para conocer precios del mercado capitales',
            schedule_interval="*/5 * * * *",  # Ejecuta cada 5 minutos
            default_args=default_args,
            catchup=False
            )

# Define the task 1 (collect the data) id. Run the bash command because the task is in a .py file.
task1 = BashOperator(
                        task_id='get_data',
                        bash_command=f'python {path}/dags/src/get_data.py',
                        dag=dag
                    )

# Define Task 2 (insert the data into the database)
task2 = BashOperator(
                     task_id='insert_data',
                     bash_command=f'python {path}/dags/src/insert_data.py {path}/dags/data/nyse_data.csv',
                     dag=dag
                    )

task1 >> task2