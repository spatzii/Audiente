import pandas as pd
from classes import Channel
import fpdf
from redmail import gmail
import pages.Setari as Settings


class PDFData:
    def __init__(self, file):
        self.file = file
        self.Digi = Channel(self.file, 'Digi 24')
        self.Antena = Channel(self.file, 'Antena 3 CNN')

    def get_data(self):
        data_digi = self.Digi.get_raw('Whole day')
        data_antena3 = self.Antena.get_raw('Whole day')
        graph = pd.concat([self.Digi.get_slot_averages(), self.Antena.get_slot_averages()], axis=1)

        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font('Arial')
        pdf.multi_cell(100, 10, f"Digi 24 - Whole day: {data_digi}")
        pdf.multi_cell(100, 10, f"Antena 3 CNN - Whole day: {data_antena3}")
        pdf.output('test.pdf')


class EmailData:

    def __init__(self, file):
        self.file = file
        self.email_receiver = Settings.return_email()
        self.email_sender = 'audiente.skd@gmail.com'
        self.email_password = 'itfwytyshlpoorbz'
        self.subject = f"Audiente {self.file.stem}"
        self.Digi = Channel(self.file, 'Digi 24')
        self.Antena = Channel(self.file, 'Antena 3 CNN')

    @staticmethod
    def get_ratings(channel):
        return f"Audienta {channel.name} whole day: {channel.get_raw('Whole day')}"

    def email_wholeday_dataframe(self):
        return pd.concat([self.Digi.get_slot_averages(), self.Antena.get_slot_averages()], axis=1)

    def email_slot_dataframe(self, slot):
        return pd.concat([self.Digi.get_slot_ratings(slot), self.Antena.get_slot_ratings(slot)], axis=1)

    def send_email(self):
        gmail.username = self.email_sender
        gmail.password = self.email_password
        gmail.send(subject=self.subject,
                   receivers=[self.email_receiver],
                   html="""
                   <p>{{ratings_digi}}</p>
                   <p>{{ratings_a3}}</p>
                   <p></p>
                   {{wholeday_table}}
                   {{slot_table}}
""",
                   body_tables={'wholeday_table': self.email_wholeday_dataframe(),
                                'slot_table': self.email_slot_dataframe('16-18 Știrile Zilei')},
                   body_params={'ratings_digi': self.get_ratings(self.Digi),
                                'ratings_a3': self.get_ratings(self.Antena)})






