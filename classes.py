import numpy
import pandas as pd
import data
import libraries
import libraries as lb
import pathlib
import datetime


class CSVWriter:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename.rstrip('.xlsx')[-10:].split("-")
        self.date = datetime.datetime.strptime(filename.rstrip('.xlsx')[-10:], '%Y-%m-%d')

    def check_date(self):
        if self.date.weekday() < 4:
            CSVWriter.weekday(self)
        if self.date.weekday() == 4:
            CSVWriter.friday(self)

    @staticmethod
    def clean_data(raw_file):
        raw_file.columns = raw_file.columns.str.replace('.1', '', regex=False)
        for avg_index in raw_file.index:
            if '>>>' in avg_index:
                index_without_symbols = avg_index.rpartition(">>> ")
                slot_avg = str(index_without_symbols[2]).replace(':00', '').replace(" ", '')
                raw_file.rename(index={avg_index: f'Medie {slot_avg}'}, inplace=True)
        return raw_file

    def weekday(self):
        if len(self.file.name) == 40:  # Quarters
            pathlib.Path('Data/Quarters/' + self.filename[0] + '/'
                         + self.filename[1]).mkdir(parents=True, exist_ok=True)
            rating_file = pd.read_excel(self.file, sheet_name=1,
                                        skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['TTV.1', 'Digi 24.1',
                                                                                              'Antena 3 CNN.1',
                                                                                              'B1TV.1', 'EuroNews.1',
                                                                                              'Realitatea Plus.1',
                                                                                              'Romania TV.1']]

            CSVWriter.clean_data(rating_file).to_csv(pathlib.Path('Data/Quarters/' +
                                                                  self.filename[0] + '/' + self.filename[1] + '/' +
                                                                  self.file.name.rstrip('.xlsx')[-10:] + '.csv'))

        elif len(self.file.name) == 49:  # Minutes
            pathlib.Path('Data/Minutes/' + self.filename[0] + '/' + self.filename[1]).mkdir(parents=True, exist_ok=True)
            rating_file = pd.read_excel(self.file, sheet_name=3,
                                        skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['Digi 24.1',
                                                                                              'Antena 3 CNN.1',
                                                                                              'B1TV.1', 'EuroNews.1',
                                                                                              'Realitatea Plus.1',
                                                                                              'Romania TV.1']]
            CSVWriter.clean_data(rating_file)
            rating_file.to_csv(
                pathlib.Path('Data/Minutes/' + self.filename[0] + '/' + self.filename[1] +
                             '/' + self.file.name.rstrip('.xlsx')[-10:] + '.csv'))

    def friday(self):
        pass


class Channel:
    def __init__(self, file, channel_name):
        self.file = file
        self.name = channel_name

    def get_rating_day(self):
        return pd.read_csv(self.file, index_col=0).loc[:, self.name]

    def get_rating_slot(self, timeslot):
        for slot in lb.digi24_slots:
            if slot['tronson'] == timeslot:
                slot_start = slot.get('start_q')
                slot_end = slot.get('end_q')
                return pd.read_csv(self.file, index_col=0).loc[slot_start:slot_end, self.name]

    def get_graph_day(self):
        return pd.read_csv(self.file, index_col=0,
                           skiprows=[17, 30, 43, 56, 61, 74, 79, 92, 101, 106, 107]).loc[:, self.name]

    def get_graph_slot(self, timeslot):
        for slot in lb.digi24_slots:
            if slot['tronson'] == timeslot:
                slot_start = slot.get('start_m')
                slot_end = slot.get('end_m')
                return pd.read_csv(self.file, index_col=0).loc[slot_start:slot_end, self.name]

    def get_raw(self, loc_index):
        return pd.read_csv(self.file, index_col=0).loc[loc_index:, self.name]


class Analyzer(Channel):
    def get_whole_day_rating(self):
        # Whole day rating for channel in a particular day
        return Channel(self.file, self.name).get_raw('Whole day').values[0]

    def get_monthly_average(self):
        # Average of whole day ratings by current month for channel. Will be LAST 30 DAYS
        file_year = data.get_date_from_rtg(Channel(self.file, self.name).file).year
        file_month = data.get_date_from_rtg(Channel(self.file, self.name).file).month
        file_location = f"/Users/stefanpana/PycharmProjects/Audiente/Data/Quarters/{file_year}/{str(file_month).zfill(2)}"
        whole_day_ratings_list = []
        for self.file in pathlib.Path(file_location).glob('*.csv'):
            whole_day = pd.read_csv(self.file, index_col=0).loc['Whole day', self.name]
            whole_day_ratings_list.append(whole_day)
        return numpy.around(sum(whole_day_ratings_list) / len(whole_day_ratings_list), 2)

    def daily_rtg_relative_change(self):
        # Percentage change in +/- on daily rating compared to monthly average
        return numpy.around(((Analyzer(self.file, self.name).get_whole_day_rating() -
                             Analyzer(self.file, self.name).get_monthly_average()) /
                             Analyzer(self.file, self.name).get_monthly_average() * 100), 1)
    # def get_share(self):
    #     # Channel's share of rating out of all the externally monitored channels
    #     whole_day_rating = Analyzer.get_whole_day_rating(self)
    #     share_raw = Channel(self.file, channel_name='TTV').get_raw('Whole day').values[0]
    #     return numpy.around((whole_day_rating / share_raw * 100), 2)

    def adjusted_share(self):
        # Channel's share of rating from the sum of RELEVANT channels' share (only news channels)
        total_news_share = data.adjusted_share(self.file)
        return numpy.around((Analyzer.get_whole_day_rating(self) / total_news_share * 100), 1)







