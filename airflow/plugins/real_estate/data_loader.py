import pandas as pd
import urllib.request
import ssl
from io import StringIO

class DataLoader:
    def __init__(self, github_raw_data_url="https://raw.githubusercontent.com/mdielacher/CCSE_Repro/main/kaufpreissammlung-liegenschaften.csv"):
        self.github_raw_data_url = github_raw_data_url

    def load_data(self):
        try:
            # SSL-Überprüfung deaktivieren
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(self.github_raw_data_url, context=context) as response:
                data_content = response.read().decode('Latin-1')

            # Daten in DataFrame einlesen
            df = pd.read_csv(StringIO(data_content), sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])
            return df

        except Exception as e:
            print("Ein Fehler ist aufgetreten:", str(e))
            return None
