import pandas as pd
import pathlib


csv_q = pathlib.Path('/Users/stefanpana/PycharmProjects/Audiente/Data/Quarters/2023/02/2023-02-20.csv')
csv_m = pathlib.Path('/Users/stefanpana/PycharmProjects/Audiente/Data/Minutes/2023/02/2023-02-20.csv')


class Channel:
    def __init__(self, name):
        self.name = name

    def get_rating(self):
        return pd.read_csv(csv_q).loc[:, self.name]


all_channels = ['Digi 24', 'Antena 3 CNN']
digi24 = Channel('Digi 24')
antena3 = Channel('Antena 3 CNN')
#
# print(digi24.get_rating())
# for channel in all_channels:
#     channel = Channel(channel).get_rating()


