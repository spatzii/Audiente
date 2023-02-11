import pandas as pd
import pathlib
import libraries


def xlsx_to_csv_quarters(file, filename):
    # FOR UPLOAD FUNCTION // Converts xlsx to csv for 'Digi24' and 'Antena 3 CNN'
    # 'Filename' returns list of strings in YYYY-MM-DD format
    # 'Date' returns string of date
    # Function creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv

    date = str(filename[25:35][:11])
    filename = filename[25:35][:11].split("-")
    pathlib.Path('Data/Quarters/' + filename[0] + '/' + filename[1]).mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=1)

    # Temporary fix for bad rating files/missing columns. Function fetches data by column index,
    # column index might point to another station.

    if df.iloc[1, 21] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 21, 22, 28, 29]].to_csv(pathlib.Path
                                                       ('Data/Quarters/' + filename[0] + '/' + filename[1] +
                                                        '/' + date + '.csv'),
                                                       header=False)

    elif df.iloc[1, 20] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 21, 22, 28, 29]].to_csv(pathlib.Path
                                                       ('Data/Quarters/' + filename[0] + '/' + filename[1] +
                                                        '/' + date + '.csv'),
                                                       header=False)
    else:
        return False


def xlsx_to_csv_minutes(file, filename):
    # FOR UPLOAD FUNCTION. Same as xlsx_to_csv_quarters(), bur returns ratings by minute,
    # from different file

    date = str(filename[34:44])
    filename = filename[34:44].split("-")
    pathlib.Path('Data/Minutes/' + filename[0] + '/' + filename[1] + '/' + filename[2]) \
        .mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=2)
    df.iloc[1:1143, [0, 18, 21, 22, 28, 29]].to_csv(pathlib.Path
                                                    ('Data/Minutes/' + filename[0] + '/' + filename[1] +
                                                     '/' + date + '.csv'),
                                                    header=False)


def whole_day_ratings(file, stations, data_type='style'):
    # Reads ratings for the entire day out of .csv files.
    # Gets input as list of ilocs from dictionary of stations
    # graph True = Reads ratings for the entire day out of .csv files,
    #              but skips time slot averages rows for use in charts
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100, 105]
    if data_type == 'style':
        stations.insert(0, 1)
        csv = pd.read_csv(file).iloc[:, stations]
        return csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                               axis=1).format(precision=2)
    elif data_type == 'graph':
        csv = pd.read_csv(file, skiprows=[17, 30, 43, 56, 61, 74, 79, 92, 101, 107]).iloc[:, stations]
        return csv
    elif data_type == 'raw':
        csv = pd.read_csv(file).iloc[:, stations]
        return csv


def slot_ratings(file, time_slots, stations):
    # stations.insert(0, 1)
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100, 105, 106]
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_position = slot.get('loc_q')
            csv = pd.read_csv(file).iloc[slot_position, stations]
            return csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                                   axis=1).format(precision=2)


def slot_ratings_for_graph_by_minute(file, time_slots, stations):
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_position = slot.get('loc_m')
            csv = pd.read_csv(file).iloc[slot_position, stations]
            return csv.style.format(precision=2)

# def whole_day_by_minute(file, stations):
#     # Returns dataframe with styling for displaying or raw for number crunching
#     stations.insert(0, 1)
#     csv = pd.read_csv(file).iloc[:, stations]
#     return csv

# def slot_records(station, rating_file):
#     # Gets the highest value for each channel
#     # that comes in as value from channel dictionary
#     for chan in libraries.all_channels:
#         if chan.get('tv') == station:
#             return rating_file.max(station)
