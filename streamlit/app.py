import streamlit as st
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
    st.image("wien.jpeg")



def main():
    basic_site()
    data_prep = DataPrep("kaufpreissammlung-liegenschaften.csv")
    data_prep.convert_erwerbsdatum_to_datetime()

    viz = Viz(data_prep.df)
    viz.BarChart("Häufigkeit der Zuordnung der Liegenschaft nach PLZ", "PLZ", "zuordnung")

    viz.histogram('Kaufpreis ')





if __name__ == "__main__":
    main()

