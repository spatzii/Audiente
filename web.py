import streamlit as st
import main


st.title("Audiențe Digi24")
my_file = st.file_uploader('Select a file...', type='xlsx', key='upload')

if my_file is not None:
    main.read_audiente(my_file, my_file.name)
    #st.text(my_file.name)
    # st.text(main.test_print('Data/Upload Test.csv'))


st.session_state
