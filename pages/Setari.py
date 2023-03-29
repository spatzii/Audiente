import streamlit as st
import libraries as lib
from db_factory import EmailSettings


def select_slot():
    weekday = [x.get('tronson') for x in lib.digi24_weekdays]
    weekend = [x.get('tronson') for x in lib.digi24_weekend]
    return weekday+weekend


def add_user():
    user = st.session_state.set_email
    slot = st.session_state.set_slot
    EmailSettings().add_user(user, slot)


def delete_user():
    user = st.session_state.delete_user
    EmailSettings().delete_user(user)


def change_slot():
    user = st.session_state.edit_user
    slot = st.session_state.new_slot
    EmailSettings().update_slot(user, slot)


if st.button('Adaugă utilizator'):
    with st.form(key='new_user', clear_on_submit=True):
        st.text_input('Email', key='set_email')
        st.selectbox('Alege tronsonul', options=(select_slot()), key='set_slot')
        st.form_submit_button('Adaugă', on_click=add_user)
if st.button('Șterge utilizator'):
    with st.form(key='delete', clear_on_submit=True):
        st.text_input('Email', key='delete_user')
        st.form_submit_button('Șterge', on_click=delete_user)
if st.button('Modifică tronson'):
    with st.form(key='edit', clear_on_submit=True):
        st.text_input('Email-ul utilizatorului', key='edit_user')
        st.selectbox('Alege noul tronson', options=(select_slot()), key='new_slot')
        st.form_submit_button('Modifică', on_click=change_slot)











