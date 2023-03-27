import streamlit as st
from db_factory import EmailSettings


def change_email():
    email = st.session_state.set_email
    mail_settings = EmailSettings()
    mail_settings.clear_email()
    mail_settings.insert_email(email)


def return_email():
    return EmailSettings.read_table()


def email_form():
    with st.expander('Setări email'):
        if st.button('Alege destinatarul'):
            with st.form(key='email_form', clear_on_submit=True):
                email = st.text_input('Introduce adresa', key='set_email')
                submit = st.form_submit_button('Submit', on_click=change_email)
        if st.button('Verifică adresa actuală'):
            mail_settings = EmailSettings()
            st.write(mail_settings.read_table())


email_form()










