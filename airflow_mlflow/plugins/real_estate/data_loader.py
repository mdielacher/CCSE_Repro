from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os


class AzureBlobStorageLoader:

    def __init__(self):
        """
        Initialize the AzureBlobStorageLoader class.

        This constructor sets up the Azure Blob Storage connection using the provided environment variables.

        Raises:
            KeyError: If any of the required environment variables is missing.
        """

        self.account_name = os.environ['AZURE_ACCOUNT_NAME']
        self.account_key = os.environ['AZURE_ACCOUNT_KEY']
        self.container_name = os.environ['AZURE_COUNTAINER_NAME']
        self.connect_str = (
            f'DefaultEndpointsProtocol=https;AccountName={self.account_name};'
            f'AccountKey={self.account_key};EndpointSuffix=core.windows.net'
        )

    def data_loader(self, file_name):
        """
        Load data from Azure Blob Storage.

        This method downloads a file from Azure Blob Storage and reads it as a DataFrame.

        Args:
            file_name (str): The name of the file to be loaded.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data from the specified file.
            
        """

        blob_service_client = BlobServiceClient.from_connection_string(self.connect_str)
        container_client = blob_service_client.get_container_client(self.container_name)
        blob_client = container_client.get_blob_client(file_name)
        csv_content = blob_client.download_blob().readall()
        data = pd.read_csv(io.BytesIO(csv_content), sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])
        return data
