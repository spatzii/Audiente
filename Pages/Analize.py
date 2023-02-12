# week_days = [day.strftime('%a %d') for day in week if int(day.strftime('%w')) != 0 and int(day.strftime('%w')) < 5]
import datetime

import pandas as pd
import streamlit as st
import pathlib
import data
import errors
import calendar
# from babel.dates import format_date, format_datetime, format_time

weekly_chart, compare_day = st.tabs(['Grafice săptămânale', 'Comparație zile'])

with weekly_chart:
    select_year = st.selectbox('Alege anul', [str(datetime.date.today().year)])
    select_month = st.selectbox('Alege luna', calendar.month_name)

    cal = calendar.Calendar().monthdatescalendar(int(select_year),
                                                 datetime.datetime.strptime(select_month, '%B').date().month)
    week_days = []
    for week in cal:
        for day in week:
            if int(day.strftime('%w')) != 0 and int(day.strftime('%w')) < 5:
                week_days.append(day.strftime('%a %d'))
    week_list = [week_days[0:4], week_days[4:8], week_days[8:12], week_days[12:16], week_days[16:20]]

    # needed_csvs = pathlib.Path('Data/Quarters/2023/02/')

with compare_day:
    selected_day = st.date_input('Alege audiențele din...', key='date_1_select')
    day_one = pathlib.Path(f"Data/Quarters/{selected_day.strftime('%Y/%m')}/{selected_day.strftime('%Y-%m-%d')}.csv")
    if day_one.exists() is False:
        st.info(errors.no_rating_file)
    else:

        compare_to = st.date_input('Compară cu...', key='date_2_select')
        day_two = pathlib.Path(f"Data/Quarters/{compare_to.strftime('%Y/%m')}/{compare_to.strftime('%Y-%m-%d')}.csv")
        if day_two.exists() is False:
            st.info(errors.no_rating_file)
        else:
            new_dfs = (data.whole_day_ratings(day_one, [1, 2], data_type='raw'),
                       data.whole_day_ratings(day_two, [2], data_type='raw'))

            compared = pd.concat(new_dfs, axis=1, join='inner', ignore_index=True)
            st.dataframe(compared)
