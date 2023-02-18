import pandas as pd
import pathlib
import libraries


def xlsx_to_csv_quarters(file, filename):
    # FOR UPLOAD FUNCTION // Converts xlsx to csv
    # 'Filename' returns list of strings in YYYY-MM-DD format
    # 'Date' returns string of date
    # Function creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv

    date = str(filename[25:35][:11])
    filename = filename[25:35][:11].split("-")
    pathlib.Path('Data/Quarters/' + filename[0] + '/' + filename[1]).mkdir(parents=True, exist_ok=True)
    rating_file = pd.read_excel(file, sheet_name=1,
                                skiprows=[0, 1]).set_index('Timebands').iloc[:, [17, 20, 21, 23, 27, 28]]
    # XLSXs contain 3 columns for each station, all columns with same name, so there are 3 'Digi 24', etc.
    # XLSXs are saved with Digi 24.1, Antena 3 CNN.1, etc.
    # rating_file.columns.replace fixes that
    rating_file.columns = rating_file.columns.str.replace('.1', '', regex=False)

    for avg_index in rating_file.index:
        if '>>>' in avg_index:
            index_without_symbols = avg_index.rpartition(">>> ")
            slot_avg = str(index_without_symbols[2]).replace(':00', '').replace(" ", '')
            rating_file.rename(index={avg_index: f'Medie {slot_avg}'}, inplace=True)
    rating_file.to_csv(pathlib.Path('Data/Quarters/' + filename[0] + '/' + filename[1] + '/' + date + '.csv'))


def xlsx_to_csv_minutes(file, filename):
    # FOR UPLOAD FUNCTION. Same as xlsx_to_csv_quarters(), bur returns ratings by minute,
    # from different file

    date = str(filename[34:44])
    filename = filename[34:44].split("-")
    pathlib.Path('Data/Minutes/' + filename[0] + '/' + filename[1]).mkdir(parents=True, exist_ok=True)
    rating_file = pd.read_excel(file, sheet_name=2,
                                skiprows=[0, 1, 1143]).set_index('Timebands').iloc[:, [17, 20, 21, 23, 27, 28]]
    for avg_index in rating_file.index:
        if '>>>' in avg_index:
            index_without_symbols = avg_index.rpartition(">>> ")
            slot_avg = str(index_without_symbols[2]).replace(':00', '').replace(" ", '')
            rating_file.rename(index={avg_index: f'Medie {slot_avg}'}, inplace=True)

    rating_file.columns = rating_file.columns.str.replace('.1', '', regex=False)
    rating_file.to_csv(pathlib.Path('Data/Minutes/' + filename[0] + '/' + filename[1] + '/' + date + '.csv'))


def whole_day_ratings(file, stations, data_type='style'):
    # Reads ratings for the entire day out of .csv files.
    # Gets input as list of locs from dictionary of station names
    hl_averages = ['Whole day']
    if data_type == 'style':
        # stations.insert(0, 'Timebands')
        csv = pd.read_csv(file, index_col=0).loc[:, stations]
        return csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                               axis=1).format(precision=2).background_gradient()

    elif data_type == 'graph':
        csv = pd.read_csv(file, index_col=0, skiprows=[17, 30, 43, 56, 61, 74, 79, 92, 101, 106, 107]).loc[:, stations]
        return csv
    elif data_type == 'raw':
        csv = pd.read_csv(file, index_col=0).loc[:, stations]
        return csv


def slot_ratings(file, time_slots, stations):
    # stations.insert(0, 1)
    hl_averages = []
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_start = slot.get('start_q')
            slot_end = slot.get('end_q')
            csv = pd.read_csv(file, index_col=0).loc[slot_start:slot_end, stations]
            return csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                                   axis=1).format(precision=2).background_gradient()


def slot_ratings_for_graph_by_minute(file, time_slots, stations):
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_start = slot.get('start_m')
            slot_end = slot.get('end_m')
            csv = pd.read_csv(file, index_col=0).loc[slot_start: slot_end, stations]
            return csv.style.format(precision=2)
