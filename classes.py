import numpy as np
import pandas as pd
import libraries
import pathlib

from datetime import datetime
from Outputs import SendEmail
from DatabaseOperations import EmailSettings


class CSVWriter:
    """Create and save one CSV from minutes and quarters ratings files"""

    all_stations = ['TTV.1', 'Digi 24.1', 'Antena 3 CNN.1', 'B1TV.1', 'EuroNews.1', 'Realitatea Plus.1', 'Romania TV.1']
    csv_folder = 'Data/Complete/'

    def __init__(self, quarter, minute):
        self.quarter = quarter
        self.minute = minute
        self.filedate = quarter.name.rstrip('.xlsx')[-10:]  # YYYY-MM-DD
        self.date = datetime.strptime(self.filedate, '%Y-%m-%d')  # datetime YYYY-MM-DD
        self.subfolders = self.csv_folder + str(self.date.year) + '/' + str(self.date.month) + '/'
        pathlib.Path(self.subfolders).mkdir(parents=True, exist_ok=True)  # Creates YYYY//MM folders if they don't exist
        self.filepath = pathlib.Path(self.subfolders + self.filedate + '.csv')

    @staticmethod
    def clean_data(raw_file):
        raw_file.columns = raw_file.columns.str.replace('.1', '', regex=False)
        for avg_index in raw_file.index:
            if '>>>' in avg_index:
                raw_file.drop(avg_index, inplace=True)
        return raw_file

    def read_xlsx(self, xlsx_file, sheet: int):
        """Reads XLSX, skips header rows, sets index, reads all_stations list"""

        return pd.read_excel(xlsx_file,
                             sheet_name=sheet, skiprows=[0, 1, 1143]).set_index('Timebands').loc[:, self.all_stations]

    def create_csv(self):
        ratings_quarter = self.clean_data(self.read_xlsx(self.quarter, 1))
        ratings_minute = self.clean_data(self.read_xlsx(self.minute, 3))
        pd.concat([ratings_quarter, ratings_minute]).to_csv(pathlib.Path(self.filepath))
        # self.send_email()

    def send_email(self):
        """Sends csv file to output_factory.SendEmail method for every user in database.
        SendEmail checks users' settings for match of conditions to send email and for content. """
        csv = pathlib.Path(self.filepath)
        for user in EmailSettings().fetch_receivers():
            SendEmail(csv, user).send_or_not_send()


class Channel:
    """Creates daily tables and graphs from CSV file for selected TV station
    and calculates basic data for them"""

    def __init__(self, file, channel_name):
        self.file = file  # Data/Complete/YYYY/MM/YYYY-MM-DD.csv
        self.name = channel_name
        self.csv = pd.read_csv(self.file, index_col=0)

    def slot_selector(self, timeslot):
        """Searches library for requested slot either by current day or from lib.weekend for email settings"""
        for slot in DayOperations(self.file).dataframe_slot_library_selector():
            if slot['tronson'] == timeslot:
                return slot
        for slot in libraries.digi24_weekend:
            if slot['tronson'] == timeslot:
                return slot

    def get_slot_averages(self):
        """Return dataframe containg only slot averages for selected day based on day and slot library"""
        list_of_dataframes = []
        for slot in DayOperations(self.file).dataframe_slot_library_selector():
            list_of_dataframes.append(pd.DataFrame.from_dict(
                {f"Medie {slot.get('tronson')}":
                 np.around(self.csv.loc[slot.get('start_q'):slot.get('end_q'), [self.name]].mean(), 2)},
                orient='index'))
        return pd.concat(list_of_dataframes)

    def get_daily_ratings(self):
        """Dataframe for whole day using quarters.
        Adds slot averages based on day and slot library"""
        list_of_dataframes = []
        for slot in DayOperations(self.file).dataframe_slot_library_selector():
            list_of_dataframes.append(pd.concat([self.csv.loc[slot.get('start_q'):slot.get('end_q'), [self.name]],
                                                 pd.DataFrame.from_dict({f"Medie {slot.get('tronson')}": self.csv.loc[
                                                  slot.get('start_q'):slot.get('end_q'), [self.name]].mean()},
                                                  orient='index')]))
        list_of_dataframes.append(pd.DataFrame([self.csv.loc['Whole day', self.name]],
                                               index=['Whole day'], columns=[self.name]))
        return pd.concat(list_of_dataframes)

    def get_daily_graph(self):
        """Graph for whole day using quarters"""
        return self.csv.loc['02:00 - 02:15':'25:45 - 26:00', self.name]

    def get_slot_ratings(self, timeslot):
        slot = self.slot_selector(timeslot)
        slot_start = slot.get('start_q')
        slot_end = slot.get('end_q')
        slot_ratings = self.csv.loc[slot_start:slot_end, [self.name]]
        slot_mean = np.around(pd.DataFrame.from_dict(
            {f"Medie {slot.get('tronson')}": self.csv.loc[slot_start:slot_end, [self.name]].mean()},
            orient='index'), 2)
        return pd.concat([slot_ratings, slot_mean])

    def get_slot_graph(self, timeslot):
        """Graph for slot using minutes"""

        slot = self.slot_selector(timeslot)
        slot_start = slot.get('start_m')
        slot_end = slot.get('end_m')
        return self.csv.loc[slot_start:slot_end, self.name]

    def get_raw(self, loc_index):
        # Returns raw values from CSV based on loc input
        return self.csv.loc[loc_index:, self.name].values[0]

    def get_monthly_average(self):
        """Average of whole day ratings by current month for channel. Will be LAST 30 DAYS"""

        file_year = DayOperations(self.file).date.year
        file_month = DayOperations(self.file).date.month
        file_location = f'Data/Complete/{file_year}/{file_month}'

        whole_day_ratings_list = [pd.read_csv(self.file, index_col=0).loc['Whole day', self.name] for self.file
                                  in pathlib.Path(file_location).glob('*.csv')]

        return np.around(sum(whole_day_ratings_list) / len(whole_day_ratings_list), 2)

    def daily_rtg_relative_change(self):
        """Percentage change in +/- on daily rating compared to monthly average"""
        return np.around(((self.get_raw('Whole day') -
                           self.get_monthly_average()) /
                          self.get_monthly_average() * 100), 1)

    def quick_data(self):
        return f"""Audienta zilnica a {self.name} a fost de {self.get_raw('Whole day')}, 
            reprezentand {self.daily_rtg_relative_change()}% din audienta medie lunara de 
            {self.get_monthly_average()}."""


class DayOperations:
    """Checks day of the week and returns relevant library of slots for that day"""

    def __init__(self, file):
        self.file = file
        self.weekday = datetime.strptime(self.file.stem, '%Y-%m-%d').weekday()  # Int for weekday
        self.date = datetime.strptime(self.file.stem, '%Y-%m-%d').date()  # Datetime obj from CSV file name

    def dataframe_slot_library_selector(self):
        """Returns library location according to weekday (M-T/F/S/S)"""
        if self.weekday <= 3:
            return libraries.digi24_weekdays
        if self.weekday == 4:
            return libraries.digi24_friday
        if self.weekday == 5:
            return libraries.digi24_saturday
        if self.weekday == 6:
            return libraries.digi24_sunday

    def email_sending_settings(self):
        if self.weekday < 4:
            return 'weekday'
        if self.weekday >= 4:
            return 'weekend'

    def get_slot_names(self):
        """Returns names of slots from library according to day of the week"""
        return [slot.get('tronson') for slot in DayOperations.dataframe_slot_library_selector(self)]


class DisplayDataFrames:
    """Calls Channel methods for every selected station in Streamlit app and concats results for display"""

    @staticmethod
    def create_table(csv, stations, timeslots=None):
        if timeslots is None:
            return pd.concat([Channel(csv, station).get_daily_ratings() for station in stations],
                             axis=1).style.background_gradient().format(precision=2)
        else:
            return pd.concat([Channel(csv, station).get_slot_ratings(timeslots) for station in stations],
                             axis=1).style.background_gradient().format(precision=2)

    @staticmethod
    def create_graph(csv, stations, timeslots=None):
        if timeslots is None:
            return pd.concat([Channel(csv, station).get_daily_graph() for station in stations], axis=1)
        else:
            return pd.concat([Channel(csv, station).get_slot_graph(timeslots) for station in stations], axis=1)


