import streamlit as st
from db_factory import EmailSettings
import libraries as lib


def change_email():
    email = st.session_state.set_email
    EmailSettings().update_email(email)


def change_slot():
    slot = st.session_state.set_email
    EmailSettings().update_slot(slot)


with st.expander('Setări email'):
    if st.button('Alege destinatarul'):
        st.info(f"Adresa actuală: {EmailSettings().fetch_receiver()}")
        with st.form(key='email_form', clear_on_submit=True):
            st.text_input('Introduce adresa', key='set_email')
            st.form_submit_button('Submit', on_click=change_email)

    if st.button("Alege tronsonul"):
        with st.form(key='slot_form', clear_on_submit=True):
            st.info(f"Tronsonul actual: {EmailSettings().fetch_slot()}")
            st.selectbox('Tronsoane', options=[x.get('tronson') for x in lib.digi24_weekdays], key='set_slot')
            st.form_submit_button('Submit', on_click=change_slot)











