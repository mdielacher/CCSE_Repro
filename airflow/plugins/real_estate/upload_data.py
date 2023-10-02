from azure.storage.blob import BlobServiceClient
import json

class AzureBlobStorageUploader:
    def __init__(self, df, settings_file):
        self.settings_file = settings_file
        self.load_credentials()
        self.df = df

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

    def upload_data(self):
        blob_name = "analysis_data.csv" 
        csv_data = self.df.to_csv(index=False, sep=';')
        blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net", credential=self.account_key)
        container_client = blob_service_client.get_container_client(self.container_name)
        csv_bytes = csv_data.encode("utf-8")
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_bytes, overwrite=True)

        print(f"Die Datei {blob_name} wurde erfolgreich in Azure Blob Storage hochgeladen.")