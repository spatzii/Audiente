import streamlit as st
import pathlib
import matplotlib
import main
import datetime
import pandas as pd


st.title("Audiențe Digi24")

selection = st.date_input('Vezi audiențele din...', key='date_select')
files = (list(pathlib.Path('Data/').glob(selection.strftime('%Y') + '/' +
                                         selection.strftime('%m') + '/' +
                                         selection.strftime('%d') + '/' +
                                         '*.csv')))


with st.expander("Audiențe whole day"):
    for file in files:
        st.write("Acestea sunt audiențele din ", selection.strftime('%x'))
        rating_file = main.whole_day(file)
        st.dataframe(rating_file, width=400)


with st.expander("Audiențe tronsoane"):
    for file in files:
        time_slots = st.selectbox('Selectează tronsonul', main.tronsoane, key="tronson",
                                  label_visibility="hidden")
        if time_slots is not main.tronsoane[0]:
            new_rating_file = main.audienta_tronsoane(file, time_slots)
            st.dataframe(new_rating_file, width=600)

    # if time_slots is not None:
    #     new_rating_file = main.audienta_tronsoane(rating_file, time_slots)
    #     st.dataframe(new_rating_file)


# st.session_state['tronson']



