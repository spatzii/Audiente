import streamlit as st
import pathlib
import data
import libraries
import errors
import datetime

import classes

col_img, col_hdr = st.columns(2)
with col_img:
    st.image('logo_digi.jpg', width=280)
with col_hdr:
    st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')

quarters_file = pathlib.Path(f"Data/Quarters/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")
minutes_file = pathlib.Path(f"Data/Minutes/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")

ratings_whole_day, graph_all_day, ratings_slot, graph_slot = st.tabs(['Audiențe whole day', 'Rapoarte whole day',
                                                                      'Audiențe tronsoane', 'Rapoarte tronsoane'])

checkbox = []
active_stations_names = []

if quarters_file.exists() is False:
    st.info(errors.no_rating_file)


with st.sidebar:
    # A checkbox is created for every channel in the all_channels dict. If the checkbox is selected,
    # that channel's index is retrieved from all_channels in libraries, added to a list, and passed to the
    # read.CSV function as iloc parameter. Dataframe is not displayed if passed list is empty.
    if quarters_file.exists():
        for channel in libraries.all_channels:
            checkbox.append(st.checkbox(label=channel.get('tv'), key=channel.get('tv')))
            if st.session_state[channel.get('tv')] is True:
                active_stations_names.append(channel.get('tv'))

with ratings_whole_day:
    if len(active_stations_names) == 0 and quarters_file.exists():
        st.info(errors.choose_station)
    if len(active_stations_names) > 0:
        st.dataframe(data.tables_whole_day(quarters_file, active_stations_names), use_container_width=True)

with graph_all_day:
    if len(active_stations_names) == 0 and quarters_file:
        st.info(errors.choose_station)
    if len(active_stations_names) > 0:
        st.line_chart(data.graphs_whole_day(quarters_file, active_stations_names), x=None,
                      y=active_stations_names, use_container_width=True)


with ratings_slot:
    with st.sidebar:
        time_slots = st.selectbox('Selectează tronsonul', libraries.digi24_slot_names,
                                  key="tronson", label_visibility="hidden")
    if len(active_stations_names) == 0 and quarters_file:
        st.info(errors.choose_station)
    if time_slots == 'Selectează tronsonul ' and len(active_stations_names) > 0:
        st.info(errors.choose_slot)
    if len(active_stations_names) > 0 and time_slots != 'Selectează tronsonul ':
        st.dataframe(data.tables_slot(quarters_file, active_stations_names, time_slots), use_container_width=True)


with graph_slot:
    if len(active_stations_names) == 0 and quarters_file:
        st.info(errors.choose_station)
    if time_slots == 'Selectează tronsonul ' and quarters_file:
        st.info(errors.choose_slot)
    if time_slots == '2:00 - 6:00':
        st.info("Nu există audiențe la minut pentru intervalul 2:00 - 6:00")
    if len(active_stations_names) > 0 and time_slots != 'Selectează tronsonul ' and time_slots != '2:00 - 6:00':
        # st.line_chart(data.slot_ratings(minutes_file, time_slots, active_stations_names, data_type='graph'),
        #               x=None, y=active_stations_names)
        st.line_chart(data.graphs_slot(minutes_file, active_stations_names, time_slots), x=None,
                      y=active_stations_names, use_container_width=True)


