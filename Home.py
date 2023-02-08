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
if len(quarter_files) == 0:
    st.info("Nu există audiențe încărcate pentru această dată")
ratings_whole_day, graph_all_day, ratings_slot, graph_slot = st.tabs(['Audiențe whole day', 'Rapoarte whole day',
                                                                      'Audiențe tronsoane', 'Rapoarte tronsoane'])

checkbox = []
active_stations_location = []
active_stations_names = []
if len(quarter_files) > 0:
    with st.sidebar:
        # A checkbox is created for every channel in the all_channels dict. If the checkbox is selected,
        # that channel's index is retrieved from all_channels in libraries, added to a list, and passed to the
        # read.CSV function as iloc parameter. Dataframe is not displayed if passed list is empty.
        for channel in libraries.all_channels:
            checkbox.append(st.checkbox(label=channel.get('tv'), key=channel.get('tv')))
            if st.session_state[channel.get('tv')] is True:
                active_stations_location.append(channel.get('loc'))
                active_stations_names.append(channel.get('tv'))

with ratings_whole_day:
    for file in quarter_files:
        if len(active_stations_location) > 0:
            rating_file = data.whole_day_ratings(file, active_stations_location, graph=False)
            st.dataframe(rating_file, width=400)
        elif len(active_stations_location) == 0:
            st.info("Alege posturile TV din bara din stânga")

        with graph_all_day:
            if len(active_stations_location) > 0:
                chart_rating_file = data.whole_day_ratings(file, active_stations_location, graph=True)
                st.line_chart(chart_rating_file, x="Timebands", y=active_stations_names)
            elif len(active_stations_location) == 0:
                st.info("Alege posturile TV din bara din stânga")

with ratings_slot:
    with st.sidebar:
        time_slots = st.selectbox('Selectează tronsonul', libraries.digi24_slot_names,
                                  key="tronson", label_visibility="hidden")
    if time_slots != 'Selectează tronsonul ' and len(active_stations_location) < 1:
        st.info("Alege posturile TV din bara din stânga")
    if time_slots == 'Selectează tronsonul ':
        st.info("Alege tronsonul din bara din stânga")
    try:
        if len(active_stations_location) > 0:
            for file in quarter_files:
                new_rating_file = data.slot_ratings_test(file, time_slots, active_stations_location)
                st.dataframe(new_rating_file, width=600)

        with graph_slot:
            if time_slots != 'Selectează tronsonul ' and len(active_stations_location) < 1:
                st.info("Alege posturile TV din bara din stânga")
            if time_slots == 'Selectează tronsonul ':
                st.info("Alege tronsonul din bara din stânga")
            if len(active_stations_location) > 0:
                for minute_file in minute_files:
                    minute_file = data.slot_ratings_for_graph_by_minute(minute_file,
                                                                        time_slots, active_stations_location)
                    st.line_chart(minute_file, x="Timebands", y=active_stations_names)

    except ValueError:
        pass







