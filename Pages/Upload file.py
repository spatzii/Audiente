import data
import streamlit as st

my_file = st.file_uploader('Select a file...', type='xlsx', key='upload')
my_file_name = my_file.name

if 'minut' in my_file_name:
    data.xlsx_to_csv_minutes(my_file, my_file.name)
    st.success("Fișierul a fost urcat cu succes!")
    if data.xlsx_to_csv_minutes(my_file, my_file.name) is False:
        st.error("Fișierul de audiențe are o problemă de layout. "
                 "Verifică poziția Antenei 3. FIȘIERUL NU A FOST SALVAT")
else:
    data.xlsx_to_csv_quarters(my_file, my_file.name)
    st.success("Fișierul a fost urcat cu succes!")
    if data.xlsx_to_csv_quarters(my_file, my_file.name) is False:
        st.error("Fișierul de audiențe are o problemă de layout. "
                 "Verifică poziția Antenei 3. FIȘIERUL NU A FOST SALVAT")