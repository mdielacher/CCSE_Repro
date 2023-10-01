import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt


from viz import DataPrep, Viz

 

 

def basic_site():

    st.set_page_config(

        page_title="Liegenschaftspreise Wien",

        page_icon=None,

        layout="wide",

        initial_sidebar_state="auto",

    )

 

    background_color = "linear-gradient(to right, rgba(255, 255, 255, 0.1), rgba(255, 0, 0, 0.1))"

 

    st.markdown(f"""<style>.stApp {{background: {background_color};}}</style>""",unsafe_allow_html=True)

 

    st.title("Data Visualiserung von Liegenschaftpreisen in Wien")

    #st.image("wien.jpeg")

 

 

 

def main():

    basic_site()

    data_prep = DataPrep("/home/daniel/Dokumente/FH_StPölten/Clean_Coding/CCSE_Repro/data/trainData_20230930/cleaned_data.parquet")

   # data_prep.convert_erwerbsdatum_to_datetime()

 

    viz = Viz(data_prep.df)

    viz.BarChart("Häufigkeit der Zuordnung der Liegenschaft nach PLZ", "PLZ", "Liegenschaftstyp_Nummer")

 

    print(data_prep.df.columns)

    #viz.histogram("Kaufpreis")
    
    

    #viz.LineChart("Durchschnittliche Kaufpreise pro Tag")
                  
    viz.plot_price_trend(1020, 7)

    viz.plot_map()
    

if __name__ == "__main__":

    main()


