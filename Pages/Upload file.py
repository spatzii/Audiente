import main
import streamlit as st

my_file = st.file_uploader('Select a file...', type='xlsx', key='upload')

if my_file is not None:
    main.read_audiente(my_file, my_file.name)
