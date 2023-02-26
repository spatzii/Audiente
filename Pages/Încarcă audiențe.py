import data
import streamlit as st
import classes as cls

try:
    my_file = st.file_uploader('Alege fisierele...', type=['xlsx', 'zip'], key='upload', accept_multiple_files=True)

    for file in my_file:
        cls.CSVWriter(file, file.name).check_date()
        # data.xlsx_to_csv(file, file.name)

    if len(my_file) > 1:
        st.success("Fișierele au fost urcate cu succes!")
    if len(my_file) == 1:
        st.success("Fișierul a fost urcate cu succes!")


except AttributeError:
    pass
