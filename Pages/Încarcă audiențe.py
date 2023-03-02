import data
import streamlit as st
import classes as cls

try:
    my_file = st.file_uploader('Alege fisierele...', type=['xlsx', 'zip'], key='upload', accept_multiple_files=True)
    cls.CSVWriter(my_file[0], my_file[1]).create_csv()

except IndexError:
    pass
