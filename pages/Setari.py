import streamlit as st
from db_factory import EmailSettings
from classes import DayOperations


def change_email():
    email = st.session_state.set_email
    mail_settings = EmailSettings()
    mail_settings.update_email(email)


def change_slot():
    slot = st.session_state.set_slot
    slot_settings = EmailSettings()
    slot_settings.update_slot(slot)


def return_email():
    mail_settings = EmailSettings()
    mail_settings.read_table()


def email_form():
    with st.expander('Setări email'):
        if st.button('Alege destinatarul'):
            with st.form(key='email_form', clear_on_submit=True):
                st.text_input('Introduce adresa', key='set_email')
                st.form_submit_button('Submit', on_click=change_email)
        if st.button('Verifică adresa actuală'):
            mail_settings = EmailSettings()
            st.write(mail_settings.read_table())

        if st.button("Alege tronsonul"):
            with st.form(key='slot_form', clear_on_submit=True):
                st.selectbox('Tronsoane', options=['16-18 Știrile Zilei', '12-14 Știrile Amiezii'], key='set_slot')
                st.form_submit_button('Submit', on_click=change_slot)

        if st.button('Verifică tronsonul actual'):
            slot_settings = EmailSettings()
            st.write(slot_settings.read_slot())


email_form()










