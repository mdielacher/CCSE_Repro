import pandas as pd
import mlflow
import json
import os
from time import sleep

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score


class TrainData:
    def __init__(self, df):
        self.df = df

    def split_data(self, feat, target, test_data_split='2021-01-01'):
        test_data_split = pd.to_datetime(test_data_split)

        # Filter the DataFrame for data points where 'Erwerbsdatum' is greater than or equal to '2021-01-01'
        test_df = self.df[self.df['Erwerbsdatum'] >= test_data_split]
        test_df = test_df.drop("Erwerbsdatum", axis=1)
        train_df = self.df[self.df['Erwerbsdatum'] < test_data_split]
        train_df = train_df.drop("Erwerbsdatum", axis=1)

        # Split the data into training and testing sets based on the 'Erwerbsdatum' filter
        X_train = train_df[feat]
        X_test = test_df[feat]

        y_train = train_df[target]
        y_test = test_df[target]
        return X_train, X_test, y_train, y_test

    def build_Grid_Search_pipeline(self, categorical_columns):
        # Create a ColumnTransformer for one-hot encoding categorical columns
        column_transformer = ColumnTransformer(
            transformers=[
                ('onehot', OneHotEncoder(sparse_output=False, drop='first'), categorical_columns)
            ],
            remainder='passthrough'  # Keep numeric columns as-is
        )

        # Define a list of models and their corresponding hyperparameters
        models = [
            ('Linear Regression', LinearRegression(), {}),
            ('Random Forest', RandomForestRegressor(), {'regressor__n_estimators': [50, 100, 200]})
        ]

        return column_transformer, models


    def create_minio_buckets(replace_existing=False) -> dict:
        import minio
        minio_conn = json.loads(os.environ['AIRFLOW_CONN_MINIO_DEFAULT'])
        bucket_names = {'mlflow': 'mlflow-data'}

        minio_client = minio.Minio(
            endpoint=minio_conn['extra']['endpoint'],
            access_key=minio_conn['extra']['aws_access_key_id'],
            secret_key=minio_conn['extra']['aws_secret_access_key'],
            secure=False
        )

        for bucket_name in list(bucket_names.values()):
            if replace_existing:
                try:
                    for object in minio_client.list_objects(bucket_name=bucket_name, recursive=True):
                        minio_client.remove_object(bucket_name=bucket_name, object_name=object.object_name)
                    minio_client.remove_bucket(bucket_name)
                except:
                    pass
            
            sleep(10)

            try:
                minio_client.make_bucket(bucket_name)
            except Exception as e:
                if e.code == 'BucketAlreadyOwnedByYou':
                    print(e.message)
        
        return bucket_names


    def train_model_GridSearch(self, X_train, X_test, y_train, y_test, column_transformer, models):
        
            # Set up an MLflow experiment
        TrainData.create_minio_buckets(replace_existing=True) 

        
            # Loop through the list of models, create a pipeline for each, and perform hyperparameter tuning
        for model_name, model, param_grid in models:
            with mlflow.start_run(run_name=model_name) as run:
                mlflow.set_experiment("Real estate transactions Vienna Model")
                # Create a machine learning pipeline
                pipeline = Pipeline([
                    ('preprocessor', column_transformer),  # Apply one-hot encoding
                    ('regressor', model)  # Use the current model
                ])
                
                # Perform hyperparameter tuning with GridSearchCV
                grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')
                grid_search.fit(X_train, y_train)
                
                # Get the best hyperparameters from GridSearchCV
                best_params = grid_search.best_params_
                
                # Fit the pipeline with the best hyperparameters to the training data
                best_pipeline = grid_search.best_estimator_
                best_pipeline.fit(X_train, y_train)
                
                # Make predictions on the test set
                y_pred = best_pipeline.predict(X_test)
                
                # Evaluate the model
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                # Log the model, parameters, and metrics to MLflow
                mlflow.sklearn.log_model(best_pipeline, model_name)
                mlflow.log_params(best_params)  # Log the best hyperparameters
                mlflow.log_metrics({'mse': mse, 'r2': r2})
                run_id = mlflow.active_run().info.run_id
                mlflow.register_model(f"runs:/{run_id}/model", "Real Estate transactions Vienna")

                
                print(f"Model: {model_name}")
                print(f"Best Hyperparameters: {best_params}")
                print(f"Mean Squared Error: {mse}")
                print(f"R-squared: {r2}")