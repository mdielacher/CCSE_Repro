import pandas as pd

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
        print(X_train)
        return X_train, X_test, y_train, y_test
