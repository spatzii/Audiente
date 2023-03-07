import streamlit as st
import pathlib
import data
import libraries
import errors
import classes as cls
import pandas as pd
import plotly.express as px

col_img, col_hdr = st.columns(2)
with col_img:
    st.image('logo_digi.jpg', width=280)
with col_hdr:
    st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')
rating_file = pathlib.Path(f"Data/Complete/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")

at_a_glance, ratings_whole_day, graph_all_day, ratings_slot, graph_slot = st.tabs(['Date rapide',
                                                                                   'Audiențe whole day',
                                                                                   'Grafic whole day',
                                                                                   'Audiențe tronson',
                                                                                   'Grafic tronson'])

checkbox = []
active_stations = []

if rating_file.exists() is False:
    st.info(errors.no_rating_file)

with st.sidebar:
    # A checkbox is created for every channel in the all_channels dict. If the checkbox is selected,
    # that channel's index is retrieved from all_channels in libraries, added to a list, and passed to the
    # read.CSV function as iloc parameter. Dataframe is not displayed if passed list is empty.
    if rating_file.exists():
        for channel in libraries.all_channels:
            checkbox.append(st.checkbox(label=channel.get('tv'), key=channel.get('tv')))
            if st.session_state[channel.get('tv')] is True:
                active_stations.append(channel.get('tv'))


with at_a_glance:
    if rating_file.exists():
        if len(active_stations) == 0:
            st.info(errors.choose_station)
        if len(active_stations) > 0:
            for channel in active_stations:
                st.write(data.daily_glance(rating_file, channel))

with ratings_whole_day:
    if len(active_stations) == 0 and rating_file.exists():
        st.info(errors.choose_station)
    if len(active_stations) > 0:
        rwh = st.dataframe(data.tables_whole_day(rating_file, active_stations), use_container_width=True)

with graph_all_day:
    if len(active_stations) == 0 and rating_file:
        st.info(errors.choose_station)
    if len(active_stations) > 0:
        ghd = data.graphs_whole_day(rating_file, active_stations)
        pltl_wh = px.line(ghd, x=ghd.index, y=active_stations, color_discrete_map=libraries.px_color_map)
        st.plotly_chart(pltl_wh)

with ratings_slot:
    with st.sidebar:
        if rating_file.exists():
            time_slots = st.selectbox('Selectează tronsonul: ',
                                      cls.DayOperations(rating_file, active_stations).get_slot_names(), key="tronson")
    if len(active_stations) == 0 and rating_file:
        st.info(errors.choose_station)
    if len(active_stations) > 0 and time_slots != 'Selectează tronsonul ':
        rs = st.dataframe(data.tables_slot(rating_file, active_stations, time_slots), use_container_width=True)

with graph_slot:
    if rating_file.exists():
        if len(active_stations) == 0 and rating_file:
            st.info(errors.choose_station)
        if time_slots == '2:00 - 6:00':
            st.info("Nu există audiențe la minut pentru intervalul 2:00 - 6:00")
        if len(active_stations) > 0 and time_slots != '2:00 - 6:00':
            gs = data.graphs_slot(rating_file, active_stations, time_slots)
            pltl_slt = px.line(gs, x=gs.index, y=active_stations, color_discrete_map=libraries.px_color_map)
            st.plotly_chart(pltl_slt)
