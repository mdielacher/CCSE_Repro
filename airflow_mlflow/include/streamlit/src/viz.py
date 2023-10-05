import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import folium
from folium import plugins 
from streamlit_folium import folium_static
import geopandas as gpd
import mlflow
import pickle
import sklearn



class DataPrep:

    def __init__(self, path):

        self.df = pd.read_parquet(path)

 

def map_liegenschaft_to_number(df):
    # Sample DataFrame
    dict_liegenschaft = {
        'Liegenschaftstyp_Nummer': [0, 8, 12, 9, 4, 10, 6, 1, 5, 7, 11, 2, 3],
        'Liegenschaftstyp': [
            'Abbruchobjekt', 'Mietwohnhaus voll/tw. vermietet', 'unbebaut', 'Sonstiges',
            'Ein-, Zweifamilienhaus', 'Villa', 'Landwirtsch. Nutzung', 'Betriebsobjekt',
            'Kleingarten', 'Mietwohnhaus leer', 'Weingarten', 'Büro- u./o. Geschäftsgebäude',
            'Büro- u./o. Geschäftsgebäude leer'
        ]
    }
    df_liegenschaft = pd.DataFrame(dict_liegenschaft)

    # Create a dictionary from the DataFrame
    mapping_dict = dict(zip(df_liegenschaft['Liegenschaftstyp_Nummer'], df_liegenschaft['Liegenschaftstyp']))

    # Map 'Liegenschaftstyp_Nummer' to 'Liegenschaftstyp' in the 'TEST' DataFrame
    df['Liegenschaftstyp'] = df['Liegenschaftstyp_Nummer'].map(mapping_dict)

    return df




# Perform preprocessing on user input data
def preprocess_input(input_data, categorical_columns, encoder):
    # Create a DataFrame from input_data
    input_df = pd.DataFrame(
        data=input_data.T,  # Transpose input_data to match the shape of the encoder's output
        columns=categorical_columns
    )

    # One-hot encode categorical columns
    input_data_encoded = encoder.transform(input_df)

    return input_data_encoded

 

class Viz:

    def __init__(self, df):

        self.df = df



    def BarChart(self, name, column1, column2):
        st.subheader(name)
    
        # Filter nach PLZ
        selected_column = st.selectbox(f"{column1} auswählen:", self.df[column1].unique())
        filtered_df = self.df[self.df[column1] == selected_column]
        st.write(f"Häufigkeit der Zuordnungen für {selected_column}:")
        value_counts = filtered_df[column2].value_counts()
    
        # Zeige ein vertikales Balkendiagramm
        st.bar_chart(value_counts)
    
        max_value = st.number_input("Maximaler Kaufpreis:", value=1000000)
        bin_step = st.number_input("Bin Step:", value=50000)
    
        # Dropdown for "Zuordnung" filtering
        unique_zuordnung_values = self.df['Liegenschaftstyp_Nummer'].unique()
        selected_zuordnung = st.selectbox("Welche Art von Liegenschaft?", unique_zuordnung_values)
    
        #self.df[column2] = pd.to_numeric(self.df[column2].str.replace(',', '.'), errors='coerce').fillna(0)
    
        # Apply filter for selected "Zuordnung"
        filtered_df = self.df[self.df['Liegenschaftstyp_Nummer'] == selected_zuordnung]
    
        chart = alt.Chart(filtered_df).transform_filter(
            alt.datum[column2] <= max_value
        ).transform_bin(
            'bin_start', column2, bin=alt.Bin(step=bin_step)
        ).transform_aggregate(
            count='count()',
            groupby=['bin_start']
        ).mark_bar().encode(
            alt.X('bin_start:O', title=column2, scale=alt.Scale(paddingInner=0), axis=alt.Axis(labelAngle=0)),
            alt.Y('count:Q', title='Count')
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart)




    def histogram(self, column):
        # Replace commas with periods in the specified column
        st.subheader(f'Histogram of {column}')
        max_value = st.number_input("Maximaler Kaufpreis:", value=1000000, key="max_value")
        bin_step = st.number_input("Bin Step:", value=50000, key="bin_step")

    
        # Dropdown for "Zuordnung" filtering
        unique_zuordnung_values = self.df['Liegenschaftstyp_Nummer'].unique()
        selected_zuordnung = st.selectbox("Welche Art von Liegenschaft?", unique_zuordnung_values)
    
        #self.df[column] = pd.to_numeric(self.df[column].str.replace(',', '.'), errors='coerce').fillna(0)
    
        # Apply filter for selected "Zuordnung"
        filtered_df = self.df[self.df['Liegenschaftstyp_Nummer'] == selected_zuordnung]
    
        chart = alt.Chart(filtered_df).transform_filter(
            alt.datum[column] <= max_value
        ).transform_bin(
            'bin_start', column, bin=alt.Bin(step=bin_step)
        ).transform_aggregate(
            count='count()',
            groupby=['bin_start']
        ).mark_bar().encode(
            alt.X('bin_start:O', title=column, scale=alt.Scale(paddingInner=0), axis=alt.Axis(labelAngle=0)),
            alt.Y('count:Q', title='Count')
        ).properties(
            width=600,
            height=400
        )
    
        st.altair_chart(chart)
    


    

    def LineChart(self, name, column1 = "Erwerbsdatum", column2="Kaufpreis"):

        st.subheader(name)

        filtered_df = self.df
        filtered_df = filtered_df[["Erwerbsdatum", 'Kaufpreis']]
  
        # Gruppieren Sie nach "Erwerbsdatum" und berechnen Sie den Durchschnitt
        avg_price_per_sqm = filtered_df.groupby("Erwerbsdatum")[filtered_df.columns[1]].mean()

        # Streamlit Linechart erstellen
        st.line_chart(avg_price_per_sqm)



    # def get_Prediction_with_User_Input(self):

    #     st.title("Modell-Prediction mit User Input")

    #     # Load the MLflow model using the local tracking URI
    #     mlflow.set_tracking_uri("http://localhost:5000")        

    #     # Load the MLflow model
    #     model_uri = "runs:/fcfe02f4f95844d08cf83ce246f947e2/Random Forest"  # Replace <RUN_ID> with your specific run ID
    #     model = mlflow.pyfunc.load_model(model_uri)

    #     # Create a Streamlit app
    #     st.title("Model Prediction with User Input")

    #     # Restrict user_input1 to Viennese postal codes
    #     # Define the valid Viennese postal codes
    #     viennese_postal_codes = [1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230]
    #     viennese_code = st.selectbox("Select Viennese Postal Code:", viennese_postal_codes)

    #     # Restrict user_input2 to integers from 0 to 12
    #     integer_value = st.selectbox("Select an Integer from 0 to 12:", list(range(13)))


    #     if st.button("Predict"):
    #         # Create a DataFrame with the input data
    #         input_data = pd.DataFrame({'PLZ': [viennese_code], 'Liegenschaftstyp_Nummer': [integer_value]})
    #         print(input_data)

    #         prediction = model.predict(input_data)


    #         st.write(f"Prediction: {prediction[0]}")  # Access the first prediction



    def get_Prediction_with_User_Input(self):
        st.title("Model Prediction with User Input")

        # Load the model from the pickle file
        with open('model.pkl', 'rb') as file:
            model_rf = pickle.load(file)

        # Restrict user_input1 to Viennese postal codes
        # Define the valid Viennese postal codes
        viennese_postal_codes = [1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230]
        viennese_code = st.selectbox("Select Viennese Postal Code:", viennese_postal_codes)


        # Define the valid 'Liegenschaftstyp' options and their corresponding numeric values
        liegenschaftstyp_options = [
            'Abbruchobjekt', 'Mietwohnhaus voll/tw. vermietet', 'unbebaut', 'Sonstiges',
            'Ein-, Zweifamilienhaus', 'Villa', 'Landwirtsch. Nutzung', 'Betriebsobjekt',
            'Kleingarten', 'Mietwohnhaus leer', 'Weingarten', 'Büro- u./o. Geschäftsgebäude',
            'Büro- u./o. Geschäftsgebäude leer'
        ]
        liegenschaftstyp_mapping = {
            option: index for index, option in enumerate(liegenschaftstyp_options)
        }

        # Get the user's selection for 'Liegenschaftstyp'
        selected_liegenschaftstyp = st.selectbox("Select Liegenschaftstyp:", liegenschaftstyp_options)

        # Map the selected string to its numeric representation
        liegenschaftstyp_num = liegenschaftstyp_mapping[selected_liegenschaftstyp]

        if st.button("Predict"):
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({'PLZ': [viennese_code], 'Liegenschaftstyp_Nummer': [liegenschaftstyp_num]})
            print(input_data)

            prediction = model_rf.predict(input_data)

            st.write(f"Prediction: {round(prediction[0],2)}")  # Access the first prediction





    def plot_price_trend(self):
        # Create a Streamlit sidebar for user input
        st.sidebar.title("Trendanalyse Kaufpreis Liegenschaften")

        
        # PLZ Input with multi-select
        plz_selection = st.sidebar.multiselect("PLZ auswählen", sorted(self.df["PLZ"].unique()), key="plz_multiselect")

        # Liegenschaftstyp Input
        self.df = map_liegenschaft_to_number(self.df)
        default_liegenschaftstyp = 4  # Set your default value here
        liegenschaftstyp = st.sidebar.selectbox("Liegenschaftstyp für Liniendiagramm auswählen", sorted(self.df["Liegenschaftstyp"].unique()), key="liegenschaftstyp_select", index=default_liegenschaftstyp)

        self.df['Erwerbsdatum'] = pd.to_datetime(self.df['Erwerbsdatum'])

        # Create a figure with a specified size (e.g., 8x6 inches)
        fig, ax = plt.subplots(figsize=(8, 6))

        for plz in plz_selection:
            # Filter the DataFrame by selected PLZ and Liegenschaftstyp
            analysis_df = self.df[(self.df["PLZ"] == plz) & (self.df["Liegenschaftstyp"] == liegenschaftstyp)]

            # Group by "Erwerbsdatum" and calculate the mean of "Preis pro qm2"
            avg_price_per_year = analysis_df.groupby(analysis_df['Erwerbsdatum'].dt.year)['Quadratmeterpreis'].median()

            # Plot the data for each PLZ
            ax.plot(avg_price_per_year.index, avg_price_per_year.values, marker='o', linestyle='-', label=f'PLZ {plz}')

        ax.set_title(f'Trendanalyse: Preis pro Quadratmeter für ausgewählte PLZs über die Jahre, für den Liegenschaftstyp: {liegenschaftstyp}')
        ax.set_xlabel('Jahr')
        ax.set_ylabel('Preis pro Quadratmeter (in EUR)')
        ax.legend()
        ax.grid(True)

        st.title("Time Trend Median Quadratmeterpreis von Liegenschaften pro Bezirk")

        # Display the plot in Streamlit
        st.pyplot(fig)



    def plot_map(self):
  
        viennese_districts = {
            1010: {"latitude": 48.2092, "longitude": 16.3728},
            1020: {"latitude": 48.2149, "longitude": 16.4083},
            1030: {"latitude": 48.1936, "longitude": 16.3961},
            1040: {"latitude": 48.1921, "longitude": 16.3711},
            1050: {"latitude": 48.1923, "longitude": 16.3585},
            1060: {"latitude": 48.1972, "longitude": 16.3475},
            1070: {"latitude": 48.2025, "longitude": 16.3498},
            1080: {"latitude": 48.2104, "longitude": 16.3472},
            1090: {"latitude": 48.2244, "longitude": 16.3586},
            1100: {"latitude": 48.1526, "longitude": 16.3789},
            1110: {"latitude": 48.1634, "longitude": 16.4407},
            1120: {"latitude": 48.1757, "longitude": 16.3333},
            1130: {"latitude": 48.1787, "longitude": 16.2523},
            1140: {"latitude": 48.2176, "longitude": 16.2331},
            1150: {"latitude": 48.1955, "longitude": 16.3266},
            1160: {"latitude": 48.2137, "longitude": 16.3071},
            1170: {"latitude": 48.2362, "longitude": 16.2827},
            1180: {"latitude": 48.2346, "longitude": 16.3219},
            1190: {"latitude": 48.2511, "longitude": 16.3244},
            1200: {"latitude": 48.2444, "longitude": 16.3858},
            1210: {"latitude": 48.2651, "longitude": 16.4184},
            1220: {"latitude": 48.2163, "longitude": 16.4727},
            1230: {"latitude": 48.1435, "longitude": 16.2935},
        }

        # Create a GeoDataFrame from your viennese_districts dictionary
        viennese_districts_gdf = gpd.GeoDataFrame(
            data=None,
            geometry=gpd.points_from_xy(
                [v["longitude"] for v in viennese_districts.values()],
                [v["latitude"] for v in viennese_districts.values()]
            ),
            crs="EPSG:4326"  # Assuming WGS 84 projection
        )

        # Set the index of the GeoDataFrame to the keys of the dictionary
        viennese_districts_gdf.index = viennese_districts.keys()


        data = self.df  # Replace df with your actual DataFrame

        data = map_liegenschaft_to_number(data)

        # Liegenschaftstyp Input with a default value
        default_liegenschaftstyp = 4  # Set your default value here
        liegenschaftstyp = st.sidebar.selectbox("Liegenschaftstyp für Karte auswählen", sorted(data["Liegenschaftstyp"].unique()), key="liegenschaftstyp_map", index=default_liegenschaftstyp)

        # Filter the data for the specified Liegenschaftstyp
        data = data[data["Liegenschaftstyp"] == liegenschaftstyp]


        # Group by postal code and calculate average price
        average_prices = data.groupby("PLZ")["Quadratmeterpreis"].median().reset_index()

        
        # Merge the dataframes on the 'PLZ' column
        average_prices = average_prices.merge(viennese_districts_gdf, left_on='PLZ', right_index=True, how='left')

        # Convert the GeoDataFrame to a DataFrame and add latitude and longitude columns
        map_data = average_prices.copy()
        map_data['latitude'] = map_data['geometry'].apply(lambda geom: geom.y)
        map_data['longitude'] = map_data['geometry'].apply(lambda geom: geom.x)
        
        # Create a map centered on Vienna
        vienna_map = folium.Map(location=[48.2082, 16.3738], zoom_start=12)

        # Add district boundaries to the map
        folium.GeoJson(viennese_districts_gdf, name='geojson').add_to(vienna_map)

        # Add markers for each district with average price as tooltip
        for _, row in map_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                tooltip=f"Bezirk: {row['PLZ']}<br>Durschnitsspreis pro qm2: €{row['Quadratmeterpreis']:.2f}",
            ).add_to(vienna_map)

        # Display the map in Streamlit
        st.title("Median Quadratmeterpreis von Liegenschaften in Wien (2000-2022)")
        folium_static(vienna_map)

