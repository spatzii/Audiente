import numpy
import pandas as pd
import data
import libraries
import libraries as lb
import pathlib
import datetime


class CSVWriter:
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
                                                                                              'B1TV.1', 'EuroNews.1',
                                                                                              'Realitatea Plus.1',
                                                                                              'Romania TV.1']]
        CSVWriter.clean_data(rating_file_quarter)

        rating_file_minute = pd.read_excel(self.minute, sheet_name=3,
                                    skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, ['Digi 24.1',
                                                                                          'Antena 3 CNN.1',
                                                                                          'B1TV.1', 'EuroNews.1',
                                                                                          'Realitatea Plus.1',
                                                                                          'Romania TV.1']]
        CSVWriter.clean_data(rating_file_minute)

        pd.concat([rating_file_quarter, rating_file_minute]).to_csv(pathlib.Path('Data/Complete/'
                                                                               + self.filename[0] + '/'
                                                                               + self.filename[1] + '/'
                                                                               + self.quarter.name.rstrip('.xlsx')[-10:]
                                                                               + '.csv'))


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







