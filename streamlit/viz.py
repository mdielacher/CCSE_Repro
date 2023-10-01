import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import folium
from folium import plugins 
from streamlit_folium import folium_static
import geopandas as gpd



class DataPrep:

    def __init__(self, path):

        self.df = pd.read_parquet(path)

 

#     def convert_erwerbsdatum_to_datetime(self):

#         date_format='%d.%m.%Y'

#         self.df["Erwerbsdatum"] = pd.to_datetime(self.df["Erwerbsdatum"], format=date_format, errors='coerce')

 

    

 

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
        #filtered_df['Kaufpreis '] = filtered_df['Kaufpreis '].str.replace(',', '.')
        # filtered_df['Kaufpreis'] = pd.to_numeric(filtered_df['Kaufpreis'])
        # # Convert the 'Date' column to datetime, keeping errors as 'coerce' to convert non-matching values to NaN
        # filtered_df['Erwerbsdatum'] = pd.to_datetime(filtered_df['Erwerbsdatum'], format='%d.%m.%Y', errors='coerce')

        # Gruppieren Sie nach "Erwerbsdatum" und berechnen Sie den Durchschnitt
        avg_price_per_sqm = filtered_df.groupby("Erwerbsdatum")[filtered_df.columns[1]].mean()

        # Streamlit Linechart erstellen
        st.line_chart(avg_price_per_sqm)




    def plot_price_trend(self, plz, liegenschaftstyp):


        # Filter the DataFrame by PLZ and Liegenschaftstyp
        analysis_df = self.df[(self.df["PLZ"] == plz) & (self.df["Liegenschaftstyp_Nummer"] == liegenschaftstyp)]

        analysis_df['Preis pro qm2'] = analysis_df['Kaufpreis'] / analysis_df['Fläche']

        # Group by "Erwerbsdatum" and calculate the mean of "Preis pro qm2"
        avg_price_per_year = analysis_df.groupby(analysis_df['Erwerbsdatum'].dt.year)['Preis pro qm2'].mean()

        # Calculate a rolling 3-year average (adjust as needed)
        rolling_avg = avg_price_per_year.rolling(window=3).mean()

        # Create a figure
        fig, ax = plt.subplots(figsize=(6, 5))

        # Plot the data
        ax.plot(avg_price_per_year.index, avg_price_per_year.values, marker='o', linestyle='-', label='Preis pro qm2 (Durchschnitt pro Jahr)')
        ax.plot(avg_price_per_year.index, rolling_avg.values, linestyle='-', linewidth=2, label='Gleitender 3-Jahres-Durchschnitt')
        ax.set_title(f'Trendanalyse: Preis pro Quadratmeter für PLZ {plz} über die Jahre, für den Liegenschaftstyp: {liegenschaftstyp}')
        ax.set_xlabel('Jahr')
        ax.set_ylabel('Preis pro Quadratmeter (in EUR)')
        ax.grid(True)

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

        data["Preis_pro_qm2"] = data["Kaufpreis"] / data["PLZ"]

        # Group by postal code and calculate average price
        average_prices = data.groupby("PLZ")["Preis_pro_qm2"].mean().reset_index()

        # Merge the dataframes on the 'PLZ' column
        average_prices = average_prices.merge(viennese_districts_gdf, left_on='PLZ', right_index=True, how='left')

        # Convert the GeoDataFrame to a DataFrame and add latitude and longitude columns
        map_data = average_prices.copy()
        map_data['latitude'] = map_data['geometry'].apply(lambda geom: geom.y)
        map_data['longitude'] = map_data['geometry'].apply(lambda geom: geom.x)
        
        # # Display the map in Streamlit
        # st.title("Durchschnittlicher Kaufpreis von Liegenschaften in Wien")
        # st.map(map_data)

        # Create a map centered on Vienna
        vienna_map = folium.Map(location=[48.2082, 16.3738], zoom_start=12)

        # Add district boundaries to the map
        folium.GeoJson(viennese_districts_gdf, name='geojson').add_to(vienna_map)

        # Add markers for each district with average price as tooltip
        for _, row in map_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                tooltip=f"Bezirk: {row['PLZ']}<br>Durschnitsspreis pro qm2: €{row['Preis_pro_qm2']:.2f}",
            ).add_to(vienna_map)

        # Display the map in Streamlit
        st.title("Durchschnittlicher Kaufpreis von Liegenschaften in Wien")
        folium_static(vienna_map)





        

        # data = self.df

        # # Group by postal code and calculate average price
        # average_prices = data.groupby("PLZ")["Kaufpreis"].mean().reset_index()

        # # Merge the dataframes on the 'PLZ' column
        # average_prices = average_prices.merge(pd.DataFrame.from_dict(viennese_districts, orient='index'), left_on='PLZ', right_index=True)

        # # Create a map centered on Vienna
        # vienna_map = folium.Map(location=[48.2082, 16.3738], zoom_start=12)

        # # Add markers for each postal code with average price as tooltip
        # for _, row in average_prices.iterrows():
        #     folium.Marker(
        #         location=[row["latitude"], row["longitude"]],
        #         tooltip=f"PLZ: {row['PLZ']}, durschschnittlicher Kaufpreis: €{row['Kaufpreis']:.2f}",
        #     ).add_to(vienna_map)


        # # # Display the map in Jupyter Notebook
        # # display(vienna_map)

        # # Display the map in Streamlit
        # st.title("durschschnittlicher Kaufpreis von Liegenschaften in Wien")
        # st.map(vienna_map)



    # Sample usage:
    # Load your DataFrame df before calling this function
    # plz = 1210  # Example PLZ
    # liegenschaftstyp = "Example Type"
    # plot_price_trend(df, plz, liegenschaftstyp)


        



