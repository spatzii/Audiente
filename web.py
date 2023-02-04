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
    st.write(main.test_print(file))


# st.session_state
