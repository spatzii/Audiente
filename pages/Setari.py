import streamlit as st
import db_factory


def change_email():
    email = st.session_state.set_email
    db_factory.clear_email()
    db_factory.insert_email(email)


def return_email():
    return db_factory.read_table()


def email_form():
    with st.expander('Setări email'):
        if st.button('Alege destinatarul'):
            with st.form(key='email_form', clear_on_submit=True):
                email = st.text_input('Introduce adresa', key='set_email')
                submit = st.form_submit_button('Submit', on_click=change_email)


email_form()










