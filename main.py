import pandas as pd
import pathlib

# import pandas.io.formats.style

tronsoane = ["Selectează tronsonul", '2:00 - 6:00', '6-9 Matinal', '9-12 Știrile Dimineții',
             "12-15 Știrile Zilei", 'Studio Politic', '16-19 Știrile Amiezii',
             'Business Club', 'Jurnalul de Seară', '23:00 Știrile Serii']


def read_audiente(file, filename):
    # Filename returns list of strings in YYYY-MM-DD format
    # Date returns string of date
    # Function creates empty folders for YYYY/MM/DD, files are saved in YYYY/MM/DD/name_as_YYYY-MM-DD.csv

    date = str(filename[24:35][:11])
    filename = filename[25:35][:11].split("-")
    pathlib.Path('Data/' + filename[0] + '/' + filename[1] + '/' + filename[2]).mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=1)

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
    csv = pd.read_csv(file).iloc[:, 1:4]
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100]  # Indexes of rating averages in dataframe, for highlighting
    print(type(csv))
    csv = csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x], axis=1).set_precision(2)
    return csv


def audienta_tronsoane(other_file, time_slots):
    hl_averages = [16, 29, 42, 55, 60, 73, 78, 91, 100]
    if time_slots == tronsoane[1]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[0:17, 1:4]
    if time_slots == tronsoane[2]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[17:30, 1:4]
    if time_slots == tronsoane[3]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[30:43, 1:4]
    if time_slots == tronsoane[4]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[43:56, 1:4]
    if time_slots == tronsoane[5]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[56:61, 1:4]
    if time_slots == tronsoane[6]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[61:74, 1:4]
    if time_slots == tronsoane[7]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[74:79, 1:4]
    if time_slots == tronsoane[8]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[79:92, 1:4]
    if time_slots == tronsoane[9]:
        new_csv = pd.read_csv(other_file)
        new_csv = new_csv.iloc[92:106, 1:4]
    return new_csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                               axis=1).set_precision(2)
