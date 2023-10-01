from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from real_estate.data_loader import DataLoader
from real_estate.data_preprocessing import DataPreprocessing
from real_estate.train_data import TrainData



def load_data():
    data_loader = DataLoader()
    df = data_loader.load_data()
    return df

# Daten-Vorbereitung
def preprocess_data(df):
    data_preprocessing = DataPreprocessing(df)
    data_preprocessing.select_cols()
    cleaned_df = data_preprocessing.clean_data_entries()
    return cleaned_df


def model_training(cleaned_df):
    categorical_columns = ['PLZ', 'Liegenschaftstyp_Nummer']
    train_data = TrainData(cleaned_df)
    train_data.split_data(categorical_columns, target='Kaufpreis', test_data_split='2021-01-01')


# INIT Apache Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

#DEFININE DAG
dag = DAG(
    'ML-Workflow-Real-Estate-Transactions-Vienna',
    default_args=default_args,
    schedule_interval=None,  # Setzen Sie den Ausführungszeitplan oder lassen Sie ihn auf None, um manuelle Ausführung zu ermöglichen
)

#LOAD DATA
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

#DATA PREP
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing',
    python_callable=preprocess_data,
    op_args=[load_data_task.output], 
    provide_context=True,
    dag=dag,
)

#DATA TRAINING
model_training_task = PythonOperator(
    task_id='model_training',
    python_callable=model_training,
    op_args=[data_preprocessing_task.output], 
    provide_context=True,
    dag=dag,
)

load_data_task >> data_preprocessing_task >> model_training_task

if __name__ == "__main__":
    dag.cli()
