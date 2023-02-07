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
    pathlib.Path('Data/Quarters/' + filename[0] + '/' + filename[1] + '/' + filename[2])\
        .mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=1)

    # Temporary fix for bad rating files/missing columns. Function fetches data by column index,
    # column index might point to another station.

    if df.iloc[1, 21] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 21]].to_csv(pathlib.Path
                                           ('Data/Quarters/' + filename[0] + '/' + filename[1] +
                                            '/' + filename[2] + '/' + date + '.csv'),
                                           header=False)

    elif df.iloc[1, 20] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 20]].to_csv(pathlib.Path
                                           ('Data/Quarters/' + filename[0] + '/' + filename[1] +
                                            '/' + filename[2] + '/' + date + '.csv'),
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
    df.iloc[1:1143, [0, 18, 21]].to_csv(pathlib.Path
                                        ('Data/Minutes/' + filename[0] + '/' + filename[1] +
                                         '/' + filename[2] + '/' + date + '.csv'),
                                        header=False)


def whole_day_ratings(file, chart=False):
    # Reads ratings for the entire day out of .csv files
    # Chart is True = Reads ratings for the entire day out of .csv files,
    #              but skips time slot averages rows for use in charts
    if chart is False:
        csv = pd.read_csv(file).iloc[:, 1:4]
        hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100, 105]
        # Indexes of rating averages in dataframe, for highlighting
        csv = csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                              axis=1).set_precision(2)
        return csv
    elif chart is True:
        csv = pd.read_csv(file, skiprows=[17, 30, 43, 56, 61, 74, 79, 92, 101, 107]).iloc[:, 1:4]
        return csv.style.set_precision(2)


def slot_ratings(file, time_slots):
    # Reads ratings based on time slots out of .csv files
    # hl_averages is row index of rating averages in csv files for each timeslot
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100, 105, 106]
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_position = slot.get('loc_q')
            new_csv = pd.read_csv(file)
            new_csv = new_csv.iloc[slot_position, 1:4]
            return new_csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                                       axis=1).set_precision(2)


def slot_ratings_for_graph_by_minute(file, time_slots):
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            slot_position = slot.get('loc_m')
            csv = pd.read_csv(file)
            csv = csv.iloc[slot_position, 1:4]
            return csv.style.set_precision(2)

