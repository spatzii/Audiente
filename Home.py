import streamlit as st
import pathlib
import data
import libraries
import datetime

st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')
quarter_files = (list(pathlib.Path('Data/Quarters').glob(selection.strftime('%Y') + '/' +
                                                         selection.strftime('%m') + '/' +
                                                         selection.strftime('%d') + '/' +
                                                         '*.csv')))
minute_files = (list(pathlib.Path('Data/Minutes').glob(selection.strftime('%Y') + '/' +
                                                       selection.strftime('%m') + '/' +
                                                       selection.strftime('%d') + '/' +
                                                       '*.csv')))

with st.expander("Audiențe whole day"):
    for file in quarter_files:
        st.write("Acestea sunt audiențele din ", selection.strftime('%x'))
        rating_file = data.whole_day_ratings(file)
        st.dataframe(rating_file, width=400)
        daily_chart_btn = st.button('Rapoarte whole day', key=['daily_chart'])
        if daily_chart_btn is True:
            chart_rating_file = data.whole_day_ratings(file, chart=True)
            st.line_chart(chart_rating_file, x="Timebands", y=["Digi 24", "Antena 3 CNN"])

with st.expander("Audiențe tronsoane"):
    for file in quarter_files:
        time_slots = st.selectbox('Selectează tronsonul', libraries.digi24_slot_names,
                                  key="tronson", label_visibility="hidden")
        try:  # if time_slots is not libraries.digi24_slots[0]:
            new_rating_file = data.slot_ratings(file, time_slots)
            st.dataframe(new_rating_file, width=600)
        except ValueError:
            pass

        hourly_chart_btn = st.button('Rapoarte de tronson', key=['hourly_chart'])

        if hourly_chart_btn is True:
            for minute_file in minute_files:
                minute_file = data.slot_ratings_for_graph_by_minute(minute_file, time_slots)
                st.line_chart(minute_file, x="Timebands", y=["Digi 24", "Antena 3 CNN"])

# st.session_state
