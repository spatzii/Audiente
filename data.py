import numpy
import pandas as pd
import pathlib
import libraries
import classes as cls
import datetime


def get_date_from_rtg(file):
    # Returns datetime obj from CSV file
    return datetime.datetime.strptime(file.stem, '%Y-%m-%d').date()


def tables_whole_day(csv, stations):
    # Creates whole day ratings table
    return pd.concat([cls.Channel(csv, station).get_rating_day() for station in stations],
                     axis=1)


def graphs_whole_day(csv, stations):
    # Creates whole day chart
    return pd.concat([cls.Channel(csv, station).get_graph_day() for station in stations], axis=1)


def tables_slot(csv, stations, timeslot):
    # Creates slot table
    return pd.concat([cls.Channel(csv, station).get_rating_slot(timeslot) for station in stations],
                     axis=1)


def graphs_slot(csv, stations, timeslot):
    # Creates slot chart
    return pd.concat([cls.Channel(csv, station).get_graph_slot(timeslot) for station in stations], axis=1)


def get_row_value(csv, station, row):
    # Extracts raw float from CSV table
    return cls.Channel(csv, station).get_raw(row).values[0]


def adjusted_share(csv):
    whole_days_list = []
    for channel in libraries.all_channels:
        whole_days_list.append(cls.Analyzer(csv, channel.get('tv')).get_whole_day_rating())
    return sum(whole_days_list)


def daily_rating_relative_change(monthly_average, day_average):
    return numpy.around((((day_average - monthly_average) / monthly_average) * 100), 2)


def daily_glance(file, station):
    return f"""Audiența zilnică a {station} a fost de {cls.Analyzer(file, station).get_whole_day_rating()}, 
    reprezentând {cls.Analyzer(file, station).daily_rtg_relative_change()}% din audiența medie lunară de 
    {cls.Analyzer(file, station).get_monthly_average()}."""


def channel_names(weekday=4):
    # Returns list of programme names based on what day of the week it is
    return [x.get('tronson') for x in libraries.digi24_weekdays]
