import pandas as pd
import pathlib
import libraries


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


def slot_ratings(file, time_slots, stations, data_type='style'):
    hl_averages = []
    for slot in libraries.digi24_slots:
        if slot['tronson'] == time_slots:
            if data_type == 'style':
                slot_start = slot.get('start_q')
                slot_end = slot.get('end_q')
                csv = pd.read_csv(file, index_col=0).loc[slot_start:slot_end, stations]
                return csv.style.apply(lambda x: ['color: red' if x.name in hl_averages else '' for i in x],
                                       axis=1).format(precision=2).background_gradient()
            elif data_type == 'graph':
                slot_start = slot.get('start_m')
                slot_end = slot.get('end_m')
                csv = pd.read_csv(file, index_col=0).loc[slot_start: slot_end, stations]
                return csv.style.format(precision=2)
