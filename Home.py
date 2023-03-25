import pathlib
import libraries
import errors

import plotly.express as px
import pandas as pd
import streamlit as st

from classes import Channel, DayOperations, DisplayDataFrames
from pdf_mail import PDFData

col_img, col_hdr = st.columns(2)
with col_img:
    st.image('logo_digi.jpg', width=280)
with col_hdr:
    st.title("Audiențe Digi24")

selection = st.date_input('Selectează data audiențelor...', key='date_select')
ratings = pathlib.Path(f"Data/Complete/{selection.strftime('%Y/%m')}/{selection.strftime('%Y-%m-%d')}.csv")

at_a_glance, ratings_whole_day, graph_all_day, ratings_slot, graph_slot = st.tabs(['Date rapide',
                                                                                   'Audiențe whole day',
                                                                                   'Grafic whole day',
                                                                                   'Audiențe tronson',
                                                                                   'Grafic tronson'])

checkbox = []
selected_stations = []

if ratings.exists() is False:
    st.info(errors.no_rating_file)

with st.sidebar:
    # A checkbox is created for every channel in the all_channels dict. If the checkbox is selected,
    # that channel's index is retrieved from all_channels in libraries, added to a list, and passed to the
    # read.CSV function as iloc parameter. Dataframe is not displayed if passed list is empty.
    if ratings.exists():
        for channel in libraries.all_channels:
            checkbox.append(st.checkbox(label=channel.get('tv'), key=channel.get('tv')))
            if st.session_state[channel.get('tv')] is True:
                selected_stations.append(channel.get('tv'))


with at_a_glance:
    if ratings.exists():
        if len(selected_stations) == 0:
            st.info(errors.choose_station)
        if len(selected_stations) > 0:
            for channel in selected_stations:
                st.write(Channel(ratings, channel).quick_data())
            st.dataframe(pd.concat([Channel(ratings, channel).get_slot_averages()
                                    for channel in selected_stations], axis=1))
        if st.button('PDF'):
            PDFData(ratings).get_data()


with ratings_whole_day:
    if len(selected_stations) == 0 and ratings.exists():
        st.info(errors.choose_station)
    if len(selected_stations) > 0:
        # rwh = st.dataframe(data.tables_whole_day(ratings, selected_stations), use_container_width=True)
        rwh = st.dataframe(DisplayDataFrames.create_table(ratings, selected_stations), use_container_width=True)

with graph_all_day:
    if len(selected_stations) == 0 and ratings:
        st.info(errors.choose_station)
    if len(selected_stations) > 0:
        # ghd = data.graphs_whole_day(ratings, selected_stations)
        ghd = DisplayDataFrames.create_graph(ratings, selected_stations)
        pltl_wh = px.line(ghd, x=ghd.index, y=selected_stations, color_discrete_map=libraries.px_color_map,
                          labels={'Timebands': 'Sfert', 'value': 'Rating', 'variable': 'Post'})
        st.plotly_chart(pltl_wh)

with ratings_slot:
    with st.sidebar:
        if ratings.exists():
            time_slot = st.selectbox('Selectează tronsonul: ',
                                     DayOperations(ratings).get_slot_names(), key="tronson")
    if len(selected_stations) == 0 and ratings:
        st.info(errors.choose_station)
    if len(selected_stations) > 0 and time_slot != 'Selectează tronsonul ':
        # rs = st.dataframe(data.tables_slot(ratings, selected_stations, time_slot), use_container_width=True)
        rs = st.dataframe(DisplayDataFrames.create_table(ratings, selected_stations, time_slot),
                          use_container_width=True)

with graph_slot:
    if ratings.exists():
        if len(selected_stations) == 0 and ratings:
            st.info(errors.choose_station)
        if time_slot == '2:00 - 6:00':
            st.info("Nu există audiențe la minut pentru intervalul 2:00 - 6:00")
        if len(selected_stations) > 0 and time_slot != '2:00 - 6:00':
            # gs = data.graphs_slot(ratings, selected_stations, time_slot)
            gs = DisplayDataFrames.create_graph(ratings, selected_stations, time_slot)
            pltl_slt = px.line(gs, x=gs.index, y=selected_stations, color_discrete_map=libraries.px_color_map,
                               labels={'Timebands': 'Minut', 'value': 'Rating', 'variable': 'Post'})
            st.plotly_chart(pltl_slt)
