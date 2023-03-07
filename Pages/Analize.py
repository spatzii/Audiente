import datetime
import classes as cls
import data
import libraries
import numpy as np
import pandas as pd
import streamlit as st
import pathlib
import errors
import calendar
import plotly.express as px

monthly_chart, compare_day = st.tabs(['Rapoarte lunare', 'Comparație zile'])


def get_monthly_whole_day_ratings(year, month, channels, data_type='chart'):
    file_location = f"Data/Complete/{str(year)}/" \
                    f"{str(datetime.datetime.strptime(month, '%B').date().month).zfill(2)}"
    slot_dates = []
    whole_day_ratings = []
    for file in sorted(pathlib.Path(file_location).glob('*.csv')):
        whole_day = pd.read_csv(file, index_col=0).loc['Whole day', channels]
        whole_day_ratings.append(whole_day)
        slot_dates.append(datetime.datetime.strptime(file.stem, '%Y-%m-%d').date())
    monthly_graph_df = pd.DataFrame(whole_day_ratings,
                                    index=slot_dates)
    if data_type == 'chart':
        return monthly_graph_df
    elif data_type == 'data':
        return whole_day_ratings


def get_monthly_slot_ratings(year, month, when, timeslot, channels):
    file_location = f"Data/Complete/{str(year)}/" \
                    f"{str(datetime.datetime.strptime(month, '%B').date().month).zfill(2)}"
    slot_ratings = []
    slot_dates = []
    start_q = ''
    end_q = ''
    match when:
        case 'weekday':
            for file in sorted(pathlib.Path(file_location).glob('*.csv')):
                if data.is_weekday(file) is True:
                    for period in libraries.digi24_weekdays:
                        if timeslot == period.get('tronson'):
                            start_q = period.get('start_q')
                            end_q = period.get('end_q')
                    slot = pd.read_csv(file, index_col=0).loc[start_q:end_q, channels].mean()
                    slot_ratings.append(slot)
                    slot_dates.append(datetime.datetime.strptime(file.stem, '%Y-%m-%d').date())

        case 'weekend':
            for file in sorted(pathlib.Path(file_location).glob('*.csv')):
                if data.is_weekday(file) is False:
                    for period in libraries.digi24_weekend:
                        if timeslot == period.get('tronson'):
                            start_q = period.get('start_q')
                            end_q = period.get('end_q')
                    slot = pd.read_csv(file, index_col=0).loc[start_q:end_q, channels].mean()
                    slot_ratings.append(slot)
                    slot_dates.append(datetime.datetime.strptime(file.stem, '%Y-%m-%d').date())
    return pd.DataFrame(slot_ratings, index=slot_dates)
# Perioade de comparatie: Ultimele 30 de zile, 1 luna, 3 luni, 6 luni, un an
# Evolutii tronson


with monthly_chart:
    scope_select = st.radio(label='Alege tipul graficelor',
                            options=['Zile', 'Tronsoane'], key='selector', horizontal=True)
    # st.session_state
    checkbox = []
    active_stations_names = []
    with st.sidebar:
        for channel in libraries.all_channels:
            checkbox.append(st.checkbox(label=channel.get('tv'), key=channel.get('tv')))
            if st.session_state[channel.get('tv')] is True:
                active_stations_names.append(channel.get('tv'))
    select_year = st.selectbox('Alege anul', [int(datetime.date.today().year)], key='monthly_y')
    select_month = st.selectbox('Alege luna', calendar.month_name, key='monthly_m')

    if st.session_state['selector'] == 'Zile':
        if len(active_stations_names) > 0:
            try:
                mc = get_monthly_whole_day_ratings(select_year, select_month, active_stations_names)
                pltl_mc = px.line(mc, color_discrete_map=libraries.px_color_map,
                                  labels={'index': 'Ziua', 'value': 'Rating', 'variable': 'Post'})
                st.plotly_chart(pltl_mc)
            except ValueError:
                pass

    if st.session_state['selector'] == 'Tronsoane':
        periods = st.radio(label='Alege intervalul',
                           options=['Timpul săptămânii', 'Weekend'], key='periods', horizontal=True)
        if st.session_state['periods'] == 'Timpul săptămânii':
            time_slots = [slot.get('tronson') for slot in libraries.digi24_weekdays]
            interval = 'weekday'
        if st.session_state['periods'] == 'Weekend':
            st.info(errors.wknd_warn)
            time_slots = [slot.get('tronson') for slot in libraries.digi24_weekend]
            interval = 'weekend'
        select_slot = st.selectbox('Alege tronsonul', options=time_slots)

        if len(active_stations_names) > 0:
            try:
                mc = np.around(get_monthly_slot_ratings(select_year, select_month,
                                                        interval, select_slot, active_stations_names), 2)
                pltl_mc = px.line(mc, color_discrete_map=libraries.px_color_map, markers=True,
                                  labels={'index': 'Ziua', 'value': 'Rating', 'variable': 'Post'})
                st.plotly_chart(pltl_mc, use_container_width=True)
            except ValueError:
                pass

with compare_day:
    pass
