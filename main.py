import pandas as pd
import pathlib


def read_audiente(file, filename):
    # filename returns list of strings in YYYY-MM-DD format
    # date returns string of date
    date = str(filename[24:35][:11])
    filename = filename[25:35][:11].split("-")
    print(filename[0])
    pathlib.Path('Data/' + filename[0] + '/' + filename[1]).mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(file, sheet_name=1)
    df.iloc[1:109, [0, 18, 20]].to_csv(pathlib.Path
                                       ('Data/' + filename[0] + '/' + filename[1] + '/' + date + '.csv'))


def test_print(file):
    csv_file = pd.read_csv(file)
    return csv_file



