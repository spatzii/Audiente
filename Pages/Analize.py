import pandas as pd
import streamlit as st
import pathlib
import data

# print(rating_file_raw)
#             st.metric('Whole day', rating_file_raw.iloc[106, 1])
#
# rating_file_raw = data.whole_day_ratings(file, active_stations_location, data_type='raw')
# day_one_csv = st.dataframe(data.whole_day_ratings(file, [2], data_type='raw') for file in day_one)
compare_day, test = st.tabs(['Comparație zile', 'test'])
with compare_day:
    selection_day = st.date_input('Alege audiențele din...', key='date_1_select')
    day_one = (list(pathlib.Path('Data/Quarters').glob(f"**/{selection_day.strftime('%Y-%m-%d')}.csv")))
    compare_to = st.date_input('Compară cu...', key='date_2_select')
    day_two = (list(pathlib.Path('Data/Quarters').glob(f"**/{compare_to.strftime('%Y-%m-%d')}.csv")))

    new_dfs = ([data.whole_day_ratings(file, [1, 2], data_type='raw') for file in day_one][0],
               [data.whole_day_ratings(file, [2], data_type='raw') for file in day_two][0])

    compared = pd.concat(new_dfs, axis=1, join='inner', ignore_index=True)
    st.dataframe(compared)
