import plotly_express as px
from classes import Channel
import fpdf


class PDFData:
    def __init__(self, file):
        self.file = file
        self.Digi = Channel(self.file, 'Digi 24')
        self.Antena = Channel(self.file, 'Antena 3 CNN')

    def get_data(self):
        data_digi = self.Digi.quick_data()
        data_antena3 = self.Antena.quick_data()
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font('Arial')
        pdf.multi_cell(60, 10, data_digi)
        pdf.output('test.pdf')








