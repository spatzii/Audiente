import data
import streamlit as st


my_file = st.file_uploader('Select a file...', type='xlsx', key='upload')

if my_file is not None:
    data.read_audiente(my_file, my_file.name)
    st.success("Fișierul a fost urcat cu succes!")
    if data.read_audiente(my_file, my_file.name) is False:
        st.error("Fișierul de audiențe are o problemă de layout. Verifică poziția Antenei 3. FIȘIERUL NU A FOST SALVAT")


