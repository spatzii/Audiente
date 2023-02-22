import pandas as pd
import pathlib
import libraries
import classes as cls


def clean_data(file):
    file.columns = file.columns.str.replace('.1', '', regex=False)
    for avg_index in file.index:
        print('found')
        if '>>>' in avg_index:
            index_without_symbols = avg_index.rpartition(">>> ")
            slot_avg = str(index_without_symbols[2]).replace(':00', '').replace(" ", '')
            file.rename(index={avg_index: f'Medie {slot_avg}'}, inplace=True)
    return file


def xlsx_to_csv(file, filename):
    # Converts xlsx to csv. Creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv
    # Quarter files go to quarter folder, minute files go to minute folders.

    date = (filename.rstrip('.xlsx')[-10:].split("-"))

    if len(filename) == 40:
        pathlib.Path('Data/Quarters/' + date[0] + '/' + date[1]).mkdir(parents=True, exist_ok=True)
        rating_file = pd.read_excel(file, sheet_name=1,
                                    skiprows=[0, 1, 1143]).set_index('Timebands').iloc[:, [17, 20, 21, 23, 27, 28]]
        clean_data(rating_file)
        rating_file.to_csv(
            pathlib.Path('Data/Quarters/' + date[0] + '/' + date[1] + '/' + filename.rstrip('.xlsx')[-10:] + '.csv'))

    elif len(filename) == 49:
        pathlib.Path('Data/Minutes/' + date[0] + '/' + date[1]).mkdir(parents=True, exist_ok=True)
        rating_file = pd.read_excel(file, sheet_name=3,
                                    skiprows=[0, 1, 1143]).set_index('Timebands').iloc[:, [17, 20, 21, 23, 27, 28]]
        clean_data(rating_file)
        rating_file.to_csv(
            pathlib.Path('Data/Minutes/' + date[0] + '/' + date[1] + '/' + filename.rstrip('.xlsx')[-10:] + '.csv'))


def tables_whole_day(csv, stations):
    return pd.concat([cls.Channel(csv, station).get_rating_day() for station in stations],
                     axis=1).style.format(precision=2).background_gradient()


def graphs_whole_day(csv, stations):
    return pd.concat([cls.Channel(csv, station).get_graph_day() for station in stations], axis=1)


def tables_slot(csv, stations, timeslot):
    return pd.concat([cls.Channel(csv, station).get_rating_slot(timeslot) for station in stations],
                     axis=1).style.format(precision=2).background_gradient()


def graphs_slot(csv, stations, timeslot):
    return pd.concat([cls.Channel(csv, station).get_graph_slot(timeslot) for station in stations], axis=1)

