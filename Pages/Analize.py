import datetime

import numpy
import pandas as pd
import streamlit as st
import pathlib
import data
import errors
import calendar

weekly_chart, monthly_chart, compare_day = st.tabs(['Rapoarte săptămânale', 'Rapoarte lunare', 'Comparație zile'])

with weekly_chart:
    select_year = st.selectbox('Alege anul', [int(datetime.date.today().year)])
    select_month = st.selectbox('Alege luna', calendar.month_name)

    try:
        def first_monday(year=select_year, month=datetime.datetime.strptime(select_month, '%B').date().month):
            # Creates list from calander with 4/5 weeks per month beginning with the first Monday in selected month,
            # containing only Mondays through Thursdays. Extends into next month if last Monday in month is in
            # selected month
            week_days = []
            local_calendar = calendar.Calendar().monthdatescalendar(year, month)
            first_monday_in_month = (8 - datetime.date(year, month, 1).weekday()) % 7  # returns datetime
            for local_week in local_calendar:  # Parses through month and starts list from first monday, selects M-Ts
                for day in local_week:
                    if day >= datetime.date(year, month, first_monday_in_month) and day.weekday() < 4:
                        week_days.append(day)
            return week_days


        # Creates lists of weeks with 4 days
        week_list = [first_monday()[i:i + 4] for i in range(0, len(first_monday()), 4)]

        select_week = st.selectbox("Alege săptămâna", week_list,
                                   format_func=lambda x: f"{datetime.datetime.strftime(x[0], '%d %b')} "
                                                         f"- {datetime.datetime.strftime(x[3], '%d %b')}")
    except ValueError or NameError:
        pass
    all_data = []
    try:
        for selected_days in select_week:
            rating_file = pathlib.Path(f"Data/Quarters/{selected_days.strftime('%Y/%m')}/"
                                       f"{selected_days.strftime('%Y-%m-%d')}.csv")
            df = data.whole_day_ratings(rating_file, ['Digi 24'], data_type='raw')
            all_data.append(df.loc['Whole day', 'Digi 24'])

        st.write(f"Media săptămânii a fost de {numpy.around((sum(all_data)) / len(all_data), 2)}.")
    except FileNotFoundError:
        st.info(errors.no_rating_week)
    except NameError:
        pass

with monthly_chart:
    select_year = st.selectbox('Alege anul', [int(datetime.date.today().year)], key='monthly_y')
    select_month = st.selectbox('Alege luna', calendar.month_name, key='monthly_m')
    file_location = f"/Users/stefanpana/PycharmProjects/Audiente/Data/Quarters/{str(select_year)}/" \
                    f"{str(datetime.datetime.strptime(select_month, '%B').date().month).zfill(2)}"
    whole_day_ratings = []
    whole_day_days = []
    for file in pathlib.Path(file_location).glob('*.csv'):
        whole_day = data.whole_day_ratings(file, 'Digi 24', data_type='raw').loc['Whole day']
        whole_day_ratings.append(whole_day)
        whole_day_days.append(datetime.datetime.strptime(file.stem, '%Y-%m-%d').day)

    st.line_chart(whole_day_ratings, x=None, y=whole_day_days.sort())
    st.dataframe(whole_day_ratings)


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
