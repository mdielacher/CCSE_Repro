from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json

class AzureBlobStorageLoader:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.load_credentials()

    def load_credentials(self):
        # Lese die Verbindungsdaten aus dem Settings-Datei
        with open(self.settings_file, 'r') as data:
            data = json.load(data)
        self.account_name = data["account_name"]
        self.account_key = data["account_key"]
        self.container_name = data["container_name"]

        # Erzeuge die Verbindungszeichenfolge
        self.connect_str = (
            f'DefaultEndpointsProtocol=https;AccountName={self.account_name};'
            f'AccountKey={self.account_key};EndpointSuffix=core.windows.net'
        )

    def load_data(self, local_file_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connect_str)
        container_client = blob_service_client.get_container_client(self.container_name)
        blob_client = container_client.get_blob_client(local_file_name)
        csv_content = blob_client.download_blob().readall()
        data = pd.read_csv(io.BytesIO(csv_content), sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])
        return data 

# Beispiel-Nutzung
if __name__ == "__main__":
    settings_file = "your_settings_file.txt"  # Datei mit Kontodaten
    loader = AzureBlobStorageLoader(settings_file)
    local_file_name="kaufpreissammlung-liegenschaften.csv"
    loader.load_data(local_file_name)
