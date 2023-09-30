import pandas as pd
import numpy as np
from datetime import datetime
import os



def check_nan_in_dataframe(dataframe):
    nan_counts = dataframe.isna().sum()
    print("NaN-Werte in den Spalten des DataFrames:")
    for column, count in nan_counts.items():
        if count > 0:
            raise ValueError(f"Spalte '{column}' enthält {count} NaN-Werte.")
        print(f"Spalte '{column}': {count} NaN-Werte")
        


def load_data_from_csv(path = '', file_name = 'kaufpreissammlung-liegenschaften.csv'):
    # Combine the path and file name to create the full file path
    full_file_path = f"{path}/{file_name}"
    
    # Load the data from the CSV file
    df = pd.read_csv(full_file_path, sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])
    
    return df


def select_cols(df):
    # Select relevant columns
    df = df[["PLZ", "Erwerbsdatum", "zuordnung", "Kaufpreis \x80", "Gst.Fl.", "ErwArt", "% Widmung"]]

    # Clean up column names
    rename_names =  {
        'zuordnung': 'Liegenschaftstyp',
        'Kaufpreis \x80': 'Kaufpreis',
        'Gst.Fl.': 'Fläche',
        '% Widmung':'Widmung'
    }
    df = df.rename(columns=rename_names)
    
    return df


def clean_data_entries(df):
    
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
    df = df[df['PLZ'].isin(vienna_districts)]
    
    
    # Convert 'PLZ' to int and drop rows with NaN values in 'PLZ' column
    df = df.dropna(subset=['PLZ'])
    df['PLZ'] = df['PLZ'].astype(int)
    
    
    # Clean up Liegenschaftstyp
    liegenschaft_to_drop = ["Fabrik", "Wald", "in Arbeit"]
    # Use the isin() method to filter rows where 'PLZ' is not in the list
    df = df[~df['Liegenschaftstyp'].isin(liegenschaft_to_drop)]

    df['Liegenschaftstyp_Nummer'] = df['Liegenschaftstyp'].astype('category').cat.codes
    df['Liegenschaftstyp_Nummer'] = df['Liegenschaftstyp_Nummer'].astype(int)
    num_to_liegenschaft_mapping = df[['Liegenschaftstyp_Nummer', 'Liegenschaftstyp']].drop_duplicates()
    df = df.drop("Liegenschaftstyp", axis=1)

   
    # Subset nur Liegenschaften mit Erwerbsart Kaufvertrag
    df = df[df['ErwArt'] == 'Kaufvertrag']
    df = df.drop("ErwArt", axis=1)
    
    # Clean Up Kaufpreis
    df["Kaufpreis"] = pd.to_numeric(df["Kaufpreis"].str.replace(',', '.'), errors='coerce').fillna(0)
    
    # Clean up Erwerbsdatum
    date_format='%d.%m.%Y'
    df["Erwerbsdatum"] = pd.to_datetime(df["Erwerbsdatum"], format=date_format, errors='coerce')
    df = df[df['Erwerbsdatum'] < pd.to_datetime(datetime.now().date())]
    df = df[df['Erwerbsdatum'] >= pd.to_datetime("2000-01-01")]
    
    
    # Drop rows with missing values in specified columns
    df = df.dropna()
    
    check_nan_in_dataframe(df)
    
    return df



def export_data_to_parquet(df, output_dir):
    """
    Export a DataFrame to Parquet format in a directory with a timestamp.

    Args:
        df (pd.DataFrame): The DataFrame to be exported.
        output_dir (str): The base directory where the Parquet file directory will be created.

    Returns:
        None
    """
    try:
        # Create a timestamp with the current date and time
        timestamp = datetime.now().strftime('%Y%m%d')

        # Create a directory path with the timestamp
        export_dir = os.path.join(output_dir, f'trainData_{timestamp}')
        os.makedirs(export_dir, exist_ok=True)

        # Define the Parquet file path within the directory
        file_path = os.path.join(export_dir, 'cleaned_data.parquet')

        # Export the DataFrame to Parquet format
        df.to_parquet(file_path, engine='auto', index=False)

        print(f"Data exported to Parquet file: {file_path}")
    except Exception as e:
        print(f"Error exporting data to Parquet: {str(e)}")




def main_data_preprocessing():
    df = load_data_from_csv(path = '/home/daniel/Dokumente/FH_StPölten/Clean_Coding/CCSE_Repro/data', file_name = 'kaufpreissammlung-liegenschaften.csv')
    df = select_cols(df)
    df = clean_data_entries(df)
   
    export_data_to_parquet(df, '/home/daniel/Dokumente/FH_StPölten/Clean_Coding/CCSE_Repro/data')    


if __name__ == "__main__":
    main_data_preprocessing()
    
    




