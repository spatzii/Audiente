import streamlit as st
import pathlib
import datetime
import main


st.title("Audiențe Digi24")

selection = st.date_input('Vezi audiențele din...', key='date_select')
files = (list(pathlib.Path('Data/').glob(selection.strftime('%Y') + '/' +
                                         selection.strftime('%m') + '/' +
                                         selection.strftime('%d') + '/' +
                                         '*.csv')))
for file in files:
    st.write("Acestea sunt audiențele din ", selection.strftime('%x'))
    rating_file = main.test_print(file).style.set_precision(2)  # .highlight_max(axis=0)
    st.dataframe(rating_file)




# st.session_state
