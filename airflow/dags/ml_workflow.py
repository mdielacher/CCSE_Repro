from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import logging 


from real_estate.data_loader import DataLoader
from real_estate.data_preprocessing import DataPreprocessing


# Erstelle eine Instanz der DataLoader-Klasse
data_loader = DataLoader()
def load_data():
    # Lade Daten mithilfe der DataLoader-Klasse
    data = data_loader.load_data()
    return data

# Daten-Vorbereitung
def preprocess_data(**kwargs):
    logging.info(**kwargs)
    print("Dies sind Daten, die gedruckt werden sollen.")
    data_preprocessing = DataPreprocessing()
    pass



# Initialisiere die Apache Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    'ML-Workflow-Real-Estate-Transactions-Vienna',
    default_args=default_args,
    schedule_interval=None,  # Setzen Sie den Ausführungszeitplan oder lassen Sie ihn auf None, um manuelle Ausführung zu ermöglichen
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing',
    python_callable=preprocess_data,
    provide_context=True,
    dag=dag,
)

load_data_task >> data_preprocessing_task

if __name__ == "__main__":
    dag.cli()
