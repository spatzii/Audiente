import numpy as np
import pandas as pd
import data
import libraries
import libraries as lb
import pathlib
import datetime


class CSVWriter:
    # Create and save one CSV from minutes and quarters ratings files

    def __init__(self, quarter, minute):
        self.quarter = quarter
        self.minute = minute
        self.filename = quarter.name.rstrip('.xlsx')[-10:].split("-")  # [(YYYY), (MM), (DD)]
        # self.date = datetime.datetime.strptime(filename.rstrip('.xlsx')[-10:], '%Y-%m-%d')

    @staticmethod
    def clean_data(raw_file):
        raw_file.columns = raw_file.columns.str.replace('.1', '', regex=False)
        for avg_index in raw_file.index:
            if '>>>' in avg_index:
                raw_file.drop(avg_index, inplace=True)
        return raw_file

    def create_csv(self):
        pathlib.Path('Data/Complete/' + self.filename[0] + '/' + self.filename[1]).mkdir(parents=True, exist_ok=True)
        rating_file_quarter = pd.read_excel(self.quarter, sheet_name=1,
                                            skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['TTV.1', 'Digi 24.1',
                                                                                                  'Antena 3 CNN.1',
                                                                                                  'B1TV.1',
                                                                                                  'EuroNews.1',
                                                                                                  'Realitatea Plus.1',
                                                                                                  'Romania TV.1']]
        CSVWriter.clean_data(rating_file_quarter)

        rating_file_minute = pd.read_excel(self.minute, sheet_name=3,
                                           skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['TTV.1', 'Digi 24.1',
                                                                                                 'Antena 3 CNN.1',
                                                                                                 'B1TV.1', 'EuroNews.1',
                                                                                                 'Realitatea Plus.1',
                                                                                                 'Romania TV.1']]
        CSVWriter.clean_data(rating_file_minute)

        pd.concat([rating_file_quarter, rating_file_minute]).to_csv(pathlib.Path('Data/Complete/'
                                                                                 + self.filename[0] + '/'
                                                                                 + self.filename[1] + '/'
                                                                                 + self.quarter.name.rstrip('.xlsx')[
                                                                                   -10:]
                                                                                 + '.csv'))


class Channel:
    # Create daily tables and graphs from CSV file for selected
    # TV station and calculate basic data for them

    def __init__(self, file, channel_name):
        self.file = file  # Data/Complete/YYYY/MM/YYYY-MM-DD.csv
        self.name = channel_name
        self.csv = pd.read_csv(self.file, index_col=0)
        self.weekday = datetime.datetime.strptime(self.file.stem, '%Y-%m-%d').weekday()  # Int for weekday

    def get_rating_day(self):
        list_of_dataframes = []
        for slot in DayOperations(self.file, self.name).weekday_interpreter():
            list_of_dataframes.append(pd.concat([self.csv.loc[slot.get('start_q'):slot.get('end_q'), [self.name]],
                                                 pd.DataFrame.from_dict({f"Medie {slot.get('tronson')}": self.csv.loc[
                                                  slot.get('start_q'):slot.get('end_q'), [self.name]].mean()},
                                                  orient='index')]))
        list_of_dataframes.append(pd.DataFrame([self.csv.loc['Whole day', self.name]],
                                               index=['Whole day'], columns=[self.name]))
        return np.around(pd.concat(list_of_dataframes), 2)

    def get_rating_slot(self, timeslot):
        for slot in DayOperations(self.file, self.name).weekday_interpreter():
            if slot['tronson'] == timeslot:
                slot_start = slot.get('start_q')
                slot_end = slot.get('end_q')
                return np.around(pd.concat([self.csv.loc[slot_start:slot_end, [self.name]],
                                            pd.DataFrame.from_dict({f"Medie {slot.get('tronson')}": self.csv.loc
                                            [slot_start:slot_end, [self.name]].mean()}, orient='index')]), 2)

    def get_graph_day(self):
        return self.csv.loc['02:00 - 02:15':'25:45 - 26:00', self.name]

    def get_graph_slot(self, timeslot):
        for slot in DayOperations(self.file, self.name).weekday_interpreter():
            if slot['tronson'] == timeslot:
                slot_start = slot.get('start_m')
                slot_end = slot.get('end_m')
                return self.csv.loc[slot_start:slot_end, self.name]

    def get_raw(self, loc_index):
        return self.csv.loc[loc_index:, self.name]

    def get_slot_average(self, timeslot):
        for slot in libraries.digi24_weekdays:
            if slot['tronson'] == timeslot:
                return pd.DataFrame(self.csv.loc[slot.get('start_q'):slot.get('end_q'), self.name].mean()).T


class Analyzer(Channel):
    # Analyze complex data for TV stations with scope broader than 1-day

    def get_whole_day_rating(self):
        # Whole day rating for channel in a particular day
        return Channel(self.file, self.name).get_raw('Whole day').values[0]

    def get_monthly_average(self):
        # Average of whole day ratings by current month for channel. Will be LAST 30 DAYS
        file_year = DayOperations(self.file, self.name).get_date_from_rtg().year
        file_month = DayOperations(self.file, self.name).get_date_from_rtg().month
        file_location = f'/Users/stefanpana/PycharmProjects/Audiente/Data/Complete/' \
                        f'{file_year}/{str(file_month).zfill(2)}'
        whole_day_ratings_list = []
        for self.file in pathlib.Path(file_location).glob('*.csv'):
            whole_day = pd.read_csv(self.file, index_col=0).loc['Whole day', self.name]
            whole_day_ratings_list.append(whole_day)
        return np.around(sum(whole_day_ratings_list) / len(whole_day_ratings_list), 2)

    def daily_rtg_relative_change(self):
        # Percentage change in +/- on daily rating compared to monthly average
        return np.around(((Analyzer(self.file, self.name).get_whole_day_rating() -
                           Analyzer(self.file, self.name).get_monthly_average()) /
                          Analyzer(self.file, self.name).get_monthly_average() * 100), 1)

    def adjusted_share(self):
        # Channel's share of rating from the sum of RELEVANT channels' share (only news channels)
        total_news_share = data.adjusted_share(self.file)
        return np.around((Analyzer.get_whole_day_rating(self) / total_news_share * 100), 1)


class DayOperations(Channel):
    def get_date_from_rtg(self):
        # Returns datetime obj YYYY-MM-DD
        return datetime.datetime.strptime(self.file.stem, '%Y-%m-%d').date()

    def weekday_interpreter(self):
        # Returns library location according to weekday (M-T/F/S/S)
        if self.weekday <= 3:
            return libraries.digi24_weekdays
        if self.weekday == 4:
            return libraries.digi24_friday
        if self.weekday == 5:
            return libraries.digi24_saturday
        if self.weekday == 6:
            return libraries.digi24_sunday

    def get_slot_names(self):
        return [slot.get('tronson') for slot in DayOperations.weekday_interpreter(self)]

