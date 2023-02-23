import streamlit as st
import pathlib
import data
import libraries
import errors
import classes as cls

import classes

col_img, col_hdr = st.columns(2)
with col_img:
    st.image('logo_digi.jpg', width=280)
with col_hdr:
    st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')

quarters_file = pathlib.Path(f"Data/Quarters/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")
minutes_file = pathlib.Path(f"Data/Minutes/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")

at_a_glance, ratings_whole_day, graph_all_day, ratings_slot, graph_slot = st.tabs(['Date rapide', 'Audiențe whole day',
                                                                                   'Rapoarte whole day',
                                                                                   'Audiențe tronsoane',
                                                                                   'Rapoarte tronsoane'])

checkbox = []
active_stations = []

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
                active_stations.append(channel.get('tv'))

with at_a_glance:
    if len(active_stations) == 0 and quarters_file.exists():
        st.info(errors.choose_station)
    if len(active_stations) > 0:
        for channel in active_stations:
            st.write(f"Audiența zilnică a {channel} a fost de "
                     f"{cls.Analyzer(quarters_file, channel).get_whole_day_rating()}, "
                     f"cu un share de {cls.Analyzer(quarters_file, channel).get_share()}.  \n"
                     f"{cls.Analyzer(quarters_file, channel).adjusted_share()}% din publicul televiziunilor de știri"
                     f" a urmărit {channel}.")

with ratings_whole_day:
    if len(active_stations) == 0 and quarters_file.exists():
        st.info(errors.choose_station)
    if len(active_stations) > 0:
        st.dataframe(data.tables_whole_day(quarters_file, active_stations), use_container_width=True)

with graph_all_day:
    if len(active_stations) == 0 and quarters_file:
        st.info(errors.choose_station)
    if len(active_stations) > 0:
        st.line_chart(data.graphs_whole_day(quarters_file, active_stations), x=None,
                      y=active_stations, use_container_width=True)


with ratings_slot:
    with st.sidebar:
        time_slots = st.selectbox('Selectează tronsonul', libraries.digi24_slot_names,
                                  key="tronson", label_visibility="hidden")
    if len(active_stations) == 0 and quarters_file:
        st.info(errors.choose_station)
    if time_slots == 'Selectează tronsonul ' and len(active_stations) > 0:
        st.info(errors.choose_slot)
    if len(active_stations) > 0 and time_slots != 'Selectează tronsonul ':
        st.dataframe(data.tables_slot(quarters_file, active_stations, time_slots), use_container_width=True)


with graph_slot:
    if len(active_stations) == 0 and quarters_file:
        st.info(errors.choose_station)
    if time_slots == 'Selectează tronsonul ' and quarters_file:
        st.info(errors.choose_slot)
    if time_slots == '2:00 - 6:00':
        st.info("Nu există audiențe la minut pentru intervalul 2:00 - 6:00")
    if len(active_stations) > 0 and time_slots != 'Selectează tronsonul ' and time_slots != '2:00 - 6:00':
        st.line_chart(data.graphs_slot(minutes_file, active_stations, time_slots), x=None,
                      y=active_stations, use_container_width=True)


