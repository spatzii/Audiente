import plotly_express as px
import pdfkit as pk
from classes import Channel


class PDFData:
    def __init__(self, file):
        self.file = file
        self.Digi = Channel(self.file, 'Digi 24')
        self.Antena = Channel(self.file, 'Antena 3 CNN')

    def get_data(self):
        data_digi = self.Digi.quick_data()
        data_antena3 = self.Antena.quick_data()
        pdfkit.from_string(data_digi, 'test.pdf')


# class CreatePDF:
#
#     @staticmethod
#     def get_pdf():
#






