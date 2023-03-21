import numpy
import pandas as pd
import pathlib
import libraries
import classes as cls
import datetime


def tables_whole_day(csv, stations):
    # Creates whole day ratings table
    return pd.concat([cls.Channel(csv, station).get_rating_day() for station in stations],
                     axis=1).style.background_gradient().format(precision=2)


def graphs_whole_day(csv, stations):
    # Creates whole day chart
    return pd.concat([cls.Channel(csv, station).get_graph_day() for station in stations], axis=1)


def tables_slot(csv, stations, timeslot):
    # Creates slot table
    return pd.concat([cls.Channel(csv, station).get_rating_slot(timeslot) for station in stations],
                     axis=1).style.background_gradient().format(precision=2)


def graphs_slot(csv, stations, timeslot):
    # Creates slot chart
    return pd.concat([cls.Channel(csv, station).get_graph_slot(timeslot) for station in stations], axis=1)


def is_weekday(file):
    # Returns True if csv is weekday (M-T) or False if csv is weekend (F-S)
    if datetime.datetime.strptime(file.stem, '%Y-%m-%d').date().weekday() < 4:
        return True
    if datetime.datetime.strptime(file.stem, '%Y-%m-%d').date().weekday() > 3:
        return False

