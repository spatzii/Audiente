import pandas as pd
from classes import Channel
import fpdf
from redmail import gmail
from db_factory import EmailSettings
import libraries as lib


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


class SendEmail:

    def __init__(self, file):
        self.file = file
        self.slot = EmailSettings().fetch_slot()
        self.email_receiver = EmailSettings().fetch_receiver()
        self.email_sender = 'audiente.skd@gmail.com'
        self.email_password = 'itfwytyshlpoorbz'
        self.subject = f"Audiente {self.file.stem}"

        # DE REFACUT BUCATA ASTA, E REDUNTANTA
        self.Digi = Channel(self.file, 'Digi 24')
        self.Antena = Channel(self.file, 'Antena 3 CNN')

    @staticmethod
    def get_ratings(channel):
        """Returns string with whole day ratings"""
        return f"Audienta {channel.name} whole day: {channel.get_raw('Whole day')}"

    def get_slot(self):
        """Return slot depending on whether it's a weekday slot or weekend slot.
           Checks both libraries for matches """
        for slot in lib.digi24_weekdays:
            if slot.get('tronson') == self.slot:
                return slot.get('tronson')
        for slot in lib.digi24_weekend:
            if slot.get('tronson') == self.slot:
                return slot.get('tronson')

    def email_wholeday_dataframe(self):
        """Returns DataFrame for whole day slot averages for Digi & Antena"""
        return pd.concat([self.Digi.get_slot_averages(), self.Antena.get_slot_averages()], axis=1)

    def email_slot_dataframe(self):
        """Returns DataFrame with quarters for selected slot for Digi & Antena.
            Feeds get_slot_ratings method in cls.Channel"""
        return pd.concat([self.Digi.get_slot_ratings(self.get_slot()),
                          self.Antena.get_slot_ratings(self.get_slot())], axis=1)

    def send_email(self):
        """Sends email with whole day string, whole day avg slots and selected quarter slot.
            Gets input from Settings - slot & email"""
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
                                'slot_table': self.email_slot_dataframe()},
                   body_params={'ratings_digi': self.get_ratings(self.Digi),
                                'ratings_a3': self.get_ratings(self.Antena)})






