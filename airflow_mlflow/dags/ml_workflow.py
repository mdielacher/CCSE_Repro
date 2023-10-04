import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from real_estate.data_loader import AzureBlobStorageLoader
from real_estate.data_preprocessing import DataPreprocessing
from real_estate.train_data import TrainData
from real_estate.upload_data import AzureBlobStorageUploader

def load_data():
    #settings_file = "credentials.json"  # Datei mit Kontodaten
    loader = AzureBlobStorageLoader()
    local_file_name="kaufpreissammlung-liegenschaften.csv"
    df = loader.data_loader(local_file_name)
    return df

# Daten-Vorbereitung
def preprocess_data(df):
    data_preprocessing = DataPreprocessing(df)
    data_preprocessing.select_cols()
    cleaned_df = data_preprocessing.clean_data_entries()
    return cleaned_df


def model_training(cleaned_df):
    categorical_columns = ['PLZ', 'Liegenschaftstyp_Nummer'] # DEFINE
    target = 'Kaufpreis' # DEFINE
    test_data_split='2021-01-01' # DEFINE
    train_data = TrainData(cleaned_df)
    X_train, X_test, y_train, y_test = train_data.split_data(categorical_columns, target=target, test_data_split=test_data_split)
    column_transformer, models = train_data.build_Grid_Search_pipeline(categorical_columns)
    train_data.train_model_GridSearch(X_train, X_test, y_train, y_test, column_transformer, models) 

def upload_data(cleaned_df):
    uploader = AzureBlobStorageUploader(cleaned_df)
    uploader.upload_data()


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

upload_data_on_blob_storage_task = PythonOperator(
    task_id='upload_data_on_blob_storage',
    python_callable=upload_data,
    op_args=[data_preprocessing_task.output], 
    provide_context=True,
    dag=dag,
)

load_data_task >> data_preprocessing_task >> model_training_task
load_data_task >> data_preprocessing_task >> upload_data_on_blob_storage_task

if __name__ == "__main__":
    dag.cli()