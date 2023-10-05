import pandas as pd 
import numpy as np
from datetime import datetime
import os

class DataPreprocessing:
    def __init__(self, df):
        self.df = df

    def select_cols(self):
        # Select relevant columns
        self.df = self.df[["PLZ", "Erwerbsdatum", "zuordnung", "Kaufpreis \x80", "Gst.Fl.", "ErwArt", "% Widmung"]]

        # Clean up column names
        rename_names = {
            'zuordnung': 'Liegenschaftstyp',
            'Kaufpreis \x80': 'Kaufpreis',
            'Gst.Fl.': 'Fläche',
            '% Widmung': 'Widmung'
        }
        self.df = self.df.rename(columns=rename_names)
        return self.df

    def export_data_to_parquet(self, output_dir):
        try:
            # Create a timestamp with the current date and time
            timestamp = datetime.now().strftime('%Y%m%d')

            # Create a directory path with the timestamp
            export_dir = os.path.join(output_dir, f'trainData_{timestamp}')
            os.makedirs(export_dir, exist_ok=True)

            # Define the Parquet file path within the directory
            file_path = os.path.join(export_dir, 'cleaned_data.parquet')

            # Export the DataFrame to Parquet format
            self.df.to_parquet(file_path, engine='auto', index=False)

            print(f"Data exported to Parquet file: {file_path}")
        except Exception as e:
            print(f"Error exporting data to Parquet: {str(e)}")

    def clean_data_entries(self):
        # Clean up PLZ
        vienna_districts = [
            1010,  # Innere Stadt
            1020,  # Leopoldstadt
            1030,  # Landstraße
            1040,  # Wieden
            1050,  # Margareten
            1060,  # Mariahilf
            1070,  # Neubau
            1080,  # Josefstadt
            1090,  # Alsergrund
            1100,  # Favoriten
            1110,  # Simmering
            1120,  # Meidling
            1130,  # Hietzing
            1140,  # Penzing
            1150,  # Rudolfsheim-Fünfhaus
            1160,  # Ottakring
            1170,  # Hernals
            1180,  # Währing
            1190,  # Döbling
            1200,  # Brigittenau
            1210,  # Floridsdorf
            1220,  # Donaustadt
            1230,  # Liesing
        ]
        # Use the isin() method to filter rows where 'PLZ' is not in the list
        self.df = self.df[self.df['PLZ'].isin(vienna_districts)]
        # Convert 'PLZ' to int and drop rows with NaN values in 'PLZ' column
        self.df = self.df.dropna(subset=['PLZ'])
        self.df['PLZ'] = self.df['PLZ'].astype(int)

        # Clean up Liegenschaftstyp
        liegenschaft_to_drop = ["Fabrik", "Wald", "in Arbeit"]

        # Use the isin() method to filter rows where 'PLZ' is not in the list
        self.df = self.df[~self.df['Liegenschaftstyp'].isin(liegenschaft_to_drop)]
        self.df['Liegenschaftstyp_Nummer'] = self.df['Liegenschaftstyp'].astype('category').cat.codes
        self.df['Liegenschaftstyp_Nummer'] = self.df['Liegenschaftstyp_Nummer'].astype(int)
        self.df = self.df.drop("Liegenschaftstyp", axis=1)

        # Subset nur Liegenschaften mit Erwerbsart Kaufvertrag
        self.df = self.df[self.df['ErwArt'] == 'Kaufvertrag']
        self.df = self.df.drop("ErwArt", axis=1)

        # Clean Up Kaufpreis
        self.df["Kaufpreis"] = pd.to_numeric(self.df["Kaufpreis"].str.replace(',', '.'), errors='coerce').fillna(0)

        # Clean up Erwerbsdatum
        date_format = '%d.%m.%Y'
        self.df["Erwerbsdatum"] = pd.to_datetime(self.df["Erwerbsdatum"], format=date_format, errors='coerce')
        self.df = self.df[self.df['Erwerbsdatum'] < pd.to_datetime(datetime.now().date())]
        self.df = self.df[self.df['Erwerbsdatum'] >= pd.to_datetime("2000-01-01")]

        # add Quadratmeterpreis
        self.df["Quadratmeterpreis"] = self.df["Kaufpreis"] / self.df["Fläche"]
        self.df = self.df[self.df['Quadratmeterpreis'] > 0]
        self.df = self.df[~np.isinf(self.df['Quadratmeterpreis'])]
        self.df["Quadratmeterpreis"] = self.df["Quadratmeterpreis"].astype(int)
        

        # Drop rows with missing values in specified columns
        self.df = self.df.dropna()
        return self.df

        