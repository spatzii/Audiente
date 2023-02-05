import streamlit as st
import pathlib
import data
import datetime


st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')
files = (list(pathlib.Path('Data/').glob(selection.strftime('%Y') + '/' +
                                         selection.strftime('%m') + '/' +
                                         selection.strftime('%d') + '/' +
                                         '*.csv')))


with st.expander("Audiențe whole day"):
    for file in files:
        st.write("Acestea sunt audiențele din ", selection.strftime('%x'))
        rating_file = data.whole_day(file)
        st.dataframe(rating_file, width=400)
        daily_chart_btn = st.button('Rapoarte whole day', key=['daily_chart'])
        if daily_chart_btn is True:
            chart_rating_file = data.whole_day(file, chart=True)
            st.line_chart(chart_rating_file, x="Timebands", y=["Digi 24", "Antena 3 CNN"])


with st.expander("Audiențe tronsoane"):
    for file in files:
        time_slots = st.selectbox('Selectează tronsonul', data.tronsoane, key="tronson", label_visibility="hidden")
        if time_slots is not data.tronsoane[0]:
            new_rating_file = data.audienta_tronsoane(file, time_slots)
            st.dataframe(new_rating_file, width=600)

        hourly_chart_btn = st.button('Rapoarte de tronson', key=['hourly_chart'])

        if hourly_chart_btn is True:
            rating_file = data.audienta_tronsoane_for_graph(file, time_slots)
            st.line_chart(rating_file, x="Timebands", y=["Digi 24", "Antena 3 CNN"])


# st.session_state



