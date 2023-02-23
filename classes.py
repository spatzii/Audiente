import pandas as pd
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

    def get_rating_data(self, location):
        print(pd.read_csv(self.file, index_col=0).loc[location, self.name])
        return pd.read_csv(self.file, index_col=0).loc[location, self.name]


class Dataframe:
    def __init__(self, channels):
        self.channels = channels

    def dataframe(self):
        return pd.concat(self.channels, axis=1)


