import data
import streamlit as st
import classes as cls

quarters_list = []
minutes_list = []

try:
    my_uploads = st.file_uploader('Alege fisierele...', type=['xlsx', 'zip'], key='upload', accept_multiple_files=True)
    for file in my_uploads:
        if 'minut' in file.name:
            minutes_list.append(file)
        else:
            quarters_list.append(file)
    minutes_and_quarters = zip(quarters_list, minutes_list)
    for file in minutes_and_quarters:
        cls.CSVWriter(file[0], file[1]).create_csv()

except IndexError:
    pass



