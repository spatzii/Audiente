import numpy
import pandas as pd
import pathlib
import libraries
import classes as cls
import datetime


# def clean_data(file):
#     file.columns = file.columns.str.replace('.1', '', regex=False)
#     for avg_index in file.index:
#         if '>>>' in avg_index:
#             index_without_symbols = avg_index.rpartition(">>> ")
#             slot_avg = str(index_without_symbols[2]).replace(':00', '').replace(" ", '')
#             file.rename(index={avg_index: f'Medie {slot_avg}'}, inplace=True)
#     return file


# def xlsx_to_csv(file, filename):
#     # Converts xlsx to csv. Creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv
#     # Quarter files go to quarter folder, minute files go to minute folders.
#
#     date = (filename.rstrip('.xlsx')[-10:].split("-"))
#
#     if len(filename) == 40:
#         pathlib.Path('Data/Quarters/' + date[0] + '/' + date[1]).mkdir(parents=True, exist_ok=True)
#         rating_file = pd.read_excel(file, sheet_name=1,
#                                     skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['TTV.1', 'Digi 24.1',
#                                                                                           'Antena 3 CNN.1',
#                                                                                           'B1TV.1', 'EuroNews.1',
#                                                                                           'Realitatea Plus.1',
#                                                                                           'Romania TV.1']]
#         clean_data(rating_file)
#         rating_file.to_csv(
#             pathlib.Path('Data/Quarters/' + date[0] + '/' + date[1] + '/' + filename.rstrip('.xlsx')[-10:] + '.csv'))
#
#     elif len(filename) == 49:
#         pathlib.Path('Data/Minutes/' + date[0] + '/' + date[1]).mkdir(parents=True, exist_ok=True)
#         rating_file = pd.read_excel(file, sheet_name=3,
#                                     skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['Digi 24.1',
#                                                                                           'Antena 3 CNN.1',
#                                                                                           'B1TV.1', 'EuroNews.1',
#                                                                                           'Realitatea Plus.1',
#                                                                                           'Romania TV.1']]
#         clean_data(rating_file)
#         rating_file.to_csv(
#             pathlib.Path('Data/Minutes/' + date[0] + '/' + date[1] + '/' + filename.rstrip('.xlsx')[-10:] + '.csv'))


def get_date_from_rtg(file):
    return datetime.datetime.strptime(file.stem, '%Y-%m-%d').date()


def tables_whole_day(csv, stations):
    return pd.concat([cls.Channel(csv, station).get_rating_day() for station in stations],
                     axis=1)


def graphs_whole_day(csv, stations):
    return pd.concat([cls.Channel(csv, station).get_graph_day() for station in stations], axis=1)


def tables_slot(csv, stations, timeslot):
    return pd.concat([cls.Channel(csv, station).get_rating_slot(timeslot) for station in stations],
                     axis=1)


def graphs_slot(csv, stations, timeslot):
    return pd.concat([cls.Channel(csv, station).get_graph_slot(timeslot) for station in stations], axis=1)


def get_row_value(csv, station, row):
    return cls.Channel(csv, station).get_raw(row).values[0]


def adjusted_share(csv):
    whole_days_list = []
    for channel in libraries.all_channels:
        whole_days_list.append(cls.Analyzer(csv, channel.get('tv')).get_whole_day_rating())
    return sum(whole_days_list)


def daily_rating_relative_change(monthly_average, day_average):
    return numpy.around((((day_average - monthly_average) / monthly_average) * 100), 2)


def positive_or_negative(num):
    print(num)
    if num > 0:
        return "în creștere cu "
    if num < 0:
        return "în scădere cu "
    if num == 0:
        return "la egalitate cu "


def daily_glance(file, station):
    return f"""Audiența zilnică a {station} a fost de {cls.Analyzer(file, station).get_whole_day_rating()}, 
    reprezentând {cls.Analyzer(file, station).daily_rtg_relative_change()}% din audiența medie lunară de 
    {cls.Analyzer(file, station).get_monthly_average()}."""

# def daily_glance(file, stations='Digi 24'):
#     return f"""Audiența zilnică a {channel} a fost de {cls.Analyzer(file, channel).get_whole_day_rating()},
#     {data.positive_or_negative(data.daily_rating_relative_change(data.monthly_average_rating(2023,
#     'February', stations), cls.Analyzer(file, channel).get_whole_day_rating()))},
#     {abs(data.daily_rating_relative_change(data.monthly_average_rating(2023, 'February', 'Digi 24'),
#     cls.Analyzer(file, channel).get_whole_day_rating()))}% față de media lunară.
#     Share-ul a fost de {cls.Analyzer(file, channel).get_share()}.
#     {cls.Analyzer(file, channel).adjusted_share()}% din publicul televiziunilor de știri a urmărit {channel}."""
