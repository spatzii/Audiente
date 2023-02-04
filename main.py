import pandas as pd
import pathlib


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


def test_print(file):
    csv = pd.read_csv(file)
    return csv



