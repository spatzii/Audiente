import data
import streamlit as st

try:
    my_file = st.file_uploader('Select a file...', type='xlsx', key='upload', accept_multiple_files=True)

    for file in my_file:
        file_name = file.name
        print(file_name)
        data.xlsx_to_csv(file, file.name)
        if data.xlsx_to_csv(file, file.name) is False:
            st.error(f"Fişierul {file_name} are o problemă de layout. "
                     f"Verifică poziția Antenei 3. FIȘIERUL NU A FOST SALVAT")

    if len(my_file) > 1:
        st.success("Fișierele au fost urcate cu succes!")
    if len(my_file) == 1:
        st.success("Fișierul a fost urcate cu succes!")


except AttributeError:
    pass
