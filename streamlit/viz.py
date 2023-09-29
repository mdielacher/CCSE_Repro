import pandas as pd
import streamlit as st
import matplotlib as plt
import seaborn as sns
import altair as alt

class DataPrep:
    def __init__(self, path):
        self.df = pd.read_csv(path, sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])

    def convert_erwerbsdatum_to_datetime(self):
        date_format='%d.%m.%Y'
        self.df["Erwerbsdatum"] = pd.to_datetime(self.df["Erwerbsdatum"], format=date_format, errors='coerce')

    


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


    def histogram(self, column):
        # Replace commas with periods in the specified column
        st.subheader(f'Histogram of {column}')
        max_value = st.number_input("Maximaler Kaufpreis:", value=1000000)
        bin_step = st.number_input("Bin Step:", value=50000)
        
        # Dropdown for "Zuordnung" filtering
        unique_zuordnung_values = self.df['zuordnung'].unique()
        selected_zuordnung = st.selectbox("Welche Art von Liegenschaft?", unique_zuordnung_values)
        
        self.df[column] = pd.to_numeric(self.df[column].str.replace(',', '.'), errors='coerce').fillna(0)
        
        # Apply filter for selected "Zuordnung"
        filtered_df = self.df[self.df['zuordnung'] == selected_zuordnung]
        
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