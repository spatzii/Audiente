import numpy
import pandas as pd
import data
import libraries
import libraries as lb
import pathlib


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
        return Channel(self.file, self.name).get_raw('Whole day').values[0]

    def get_share(self):
        whole_day_rating = Analyzer.get_whole_day_rating(self)
        share_raw = Channel(self.file, channel_name='TTV').get_raw('Whole day').values[0]
        return numpy.around((whole_day_rating / share_raw * 100), 2)

    def adjusted_share(self):
        total_news_share = data.adjusted_share(self.file)
        return numpy.around((Analyzer.get_whole_day_rating(self) / total_news_share * 100), 1)



