from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Initialisiere die Apache Airflow DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    'Test-Workflow',
    default_args=default_args,
    schedule_interval=None,  # Setzen Sie den Ausführungszeitplan oder lassen Sie ihn auf None, um manuelle Ausführung zu ermöglichen
)

# Hartcodierte Pseudodaten
data = {
    'X': [1, 2, 3, 4, 5],
    'y': [2, 4, 5, 4, 5]
}

# Daten-Vorbereitung
def preprocess_data():
    df = pd.DataFrame(data)
    # Hier können Sie Daten vorbereiten, z.B. Feature Engineering
    return df

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing',
    python_callable=preprocess_data,
    dag=dag,
)

# Daten-Training
def train_data():
    df = preprocess_data()
    X = df[['X']]
    y = df['y']

    # Lineare Regression
    model = LinearRegression()
    model.fit(X, y)

    # Bewertung des Modells
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    print("Mean Squared Error:", mse)

train_data_task = PythonOperator(
    task_id='data_training',
    python_callable=train_data,
    dag=dag,
)

# Definieren Sie die Reihenfolge der Aufgaben
data_preprocessing_task >> train_data_task

if __name__ == "__main__":
    dag.cli()
