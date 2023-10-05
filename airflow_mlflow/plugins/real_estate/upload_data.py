from azure.storage.blob import BlobServiceClient
import os

class AzureBlobStorageUploader:
    def __init__(self, df):
        """
        Initializes the AzureBlobStorageUploader.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be uploaded to Azure Blob Storage.
        """
        self.df = df
        self.account_name = os.environ['AZURE_ACCOUNT_NAME']
        self.account_key = os.environ['AZURE_ACCOUNT_KEY']
        self.container_name = os.environ['AZURE_COUNTAINER_NAME']
        self.connect_str = (
            f'DefaultEndpointsProtocol=https;AccountName={self.account_name};'
            f'AccountKey={self.account_key};EndpointSuffix=core.windows.net'
        )

    def upload_data(self):
        """
        Uploads the DataFrame data to Azure Blob Storage.

        This method serializes the DataFrame to a CSV format and uploads it to a specified blob in Azure Blob Storage.

        Returns:
            None
        """
        blob_name = "analysis_data.csv" 
        csv_data = self.df.to_csv(index=False, sep=';')
        blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net", credential=self.account_key)
        container_client = blob_service_client.get_container_client(self.container_name)
        csv_bytes = csv_data.encode("utf-8")
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(csv_bytes, overwrite=True)

        print(f"Die Datei {blob_name} wurde erfolgreich in Azure Blob Storage hochgeladen.")