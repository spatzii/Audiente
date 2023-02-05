import pandas as pd
import pathlib

tronsoane_dict = [{'tronson': '2:00 - 6:00', 'loc': list(range(0, 17))},
                  {'tronson': '6-9 Matinal', 'loc': list(range(17, 30))},
                  {'tronson': '9-12 Știrile Dimineții', 'loc': list(range(30, 43))},
                  {'tronson': '12-15 Știrile Amiezii', 'loc': list(range(43, 56))},
                  {'tronson': 'Studio Politic', 'loc': list(range(56, 61))},
                  {'tronson': '16-19 Știrile Zilei', 'loc': list(range(61, 74))},
                  {'tronson': 'Business Club', 'loc': list(range(74, 49))},
                  {'tronson': 'Jurnalul de Seară', 'loc': list(range(79, 92))},
                  {'tronson': '23:00 Știrile Serii', 'loc': list(range(92, 106))}]

tronsoane = [x.get('tronson') for x in tronsoane_dict]


def read_audiente(file, filename):
    # FOR UPLOAD FUNCTION // Converts xlsx to csv for 'Digi24' and 'Antena 3 CNN'
    # 'Filename' returns list of strings in YYYY-MM-DD format
    # 'Date' returns string of date
    # Function creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv

    date = str(filename[24:35][:11])
    filename = filename[25:35][:11].split("-")
    pathlib.Path('Data/' + filename[0] + '/' + filename[1] + '/' + filename[2]).mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=1)

    # Temporary fix for bad rating files/missing columns. Function fetches data by column index,
    # column index might point to another station.

    if df.iloc[1, 21] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 21]].to_csv(pathlib.Path
                                           ('Data/' + filename[0] + '/' + filename[1] +
                                            '/' + filename[2] + '/' + date + '.csv'),
                                           header=False)

    elif df.iloc[1, 20] == "Antena 3 CNN":
        df.iloc[1:109, [0, 18, 20]].to_csv(pathlib.Path
                                           ('Data/' + filename[0] + '/' + filename[1] +
                                            '/' + filename[2] + '/' + date + '.csv'),
                                           header=False)
    else:
        return False


def whole_day(file):
    # Reads ratings for the entire day out of .csv files
    csv = pd.read_csv(file).iloc[:, 1:4]
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100]  # Indexes of rating averages in dataframe, for highlighting
    print(type(csv))
    csv = csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x], axis=1).set_precision(2)
    return csv


def audienta_tronsoane(other_file, time_slots):
    # Reads ratings based on time slots out of .csv files
    # hl_averages is row index of rating averages in csv files for each timeslot
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100]
    for tronson in tronsoane_dict:
        if tronson['tronson'] == time_slots:
            slot = tronson.get('loc')
            new_csv = pd.read_csv(other_file)
            new_csv = new_csv.iloc[slot, 1:4]
            return new_csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                                       axis=1).set_precision(2)

