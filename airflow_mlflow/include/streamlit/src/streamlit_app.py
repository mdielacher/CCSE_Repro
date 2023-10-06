import streamlit as st
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os
import viz


class AzureBlobStorageLoader:
    def __init__(self):
        self.account_name = os.environ['AZURE_ACCOUNT_NAME']
        self.account_key = os.environ['AZURE_ACCOUNT_KEY']
        self.container_name = os.environ['AZURE_COUNTAINER_NAME']
        self.connect_str = (
            f'DefaultEndpointsProtocol=https;AccountName={self.account_name};'
            f'AccountKey={self.account_key};EndpointSuffix=core.windows.net'
        )

    def data_loader(self, local_file_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connect_str)
        container_client = blob_service_client.get_container_client(self.container_name)
        blob_client = container_client.get_blob_client(local_file_name)
        csv_content = blob_client.download_blob().readall()
        data = pd.read_csv(io.BytesIO(csv_content), sep=";", encoding="Latin-1", low_memory=False)
        return data


def load_data(file_name):
    loader = AzureBlobStorageLoader()
    df = loader.data_loader(file_name)
    return df

st.set_page_config(page_title="Immobilientransaktionen Wien")
st.title("Immobilientransaktionen Wien - Analyse")
st.markdown(
    "Möchten Sie den Immobilienmarkt in Wien erkunden und fundierte Vorhersagen für Immobilienpreise treffen? Unser Streamlit-Dashboard ermöglicht es Ihnen, genau das zu tun! Hier haben Sie die Möglichkeit, Immobilienpreise in Wien anhand verschiedener Liegenschaftstypen und pro Quadratmeter zu prognostizieren. Darüber hinaus bieten wir Ihnen informative Grafiken, um Ihnen einen umfassenden Überblick über den aktuellen Markt zu verschaffen."
)


df = load_data(file_name="analysis_data.csv")

viz = viz.Viz(df)

#viz.BarChart("Häufigkeit der Zuordnung der Liegenschaft nach PLZ", "PLZ", "Liegenschaftstyp_Nummer")
#viz.Histogram("Kaufpreis")
#viz.LineChart("Durchschnittliche Kaufpreise pro Tag")
                
viz.plot_price_trend()

viz.plot_map()

viz.get_Prediction_with_User_Input()