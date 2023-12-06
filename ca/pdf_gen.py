from fpdf import FPDF
import pandas as pd

def create_pdf(text, df, title):


    # redifine object FPDF
    class PDF(FPDF):
        # header for the pdf
        def header(self):
            # logo
            self.image('./img/logo.png', 170, 8, 25)
            # font
            self.set_font('helvetica', 'B', 20)
            # calculate width of title and position
            title_w = self.get_string_width(title) + 6
            doc_w = self.w
            self.set_x((doc_w - title_w) / 2)
            # Title
            self.cell(title_w, 10, title, ln=True, align='C')
            # line break
            self.ln(20)

        # footer
        def footer(self):
            # set position
            self.set_y(-15)
            # font
            self.set_font('helvetica', 'I', 10)
            # set color
            self.set_text_color(169, 169, 169)
            # page number
            self.cell(0, 10, f'Page {self.page_no()} - {{nb}}', align='C')


    # create object
    pdf = PDF('P', 'mm', 'A4')

    # create page
    pdf.add_page()

    # set auto break
    pdf.set_auto_page_break(auto=True, margin=15)

    # add text
    i = 0
    for text in text:
        # data
        timestamp = int(df.iloc[i]['timestamp'])
        pos = df.iloc[i]['POS_percentage']
        neg = df.iloc[i]['NEG_percentage']
        neu = df.iloc[i]['NEU_percentage']

        # Calculate space needed for text
        space_needed = 30 + 16 + 12 + 10

        # Check if enough space is available on the page
        if pdf.get_y() + space_needed > pdf.page_break_trigger:
            pdf.add_page()  # Force a new page if there isn't enough space

        # specify font for title
        pdf.set_font('helvetica', 'BU', 16)
        pdf.cell(0, 10, f'Section {i} - Minute {timestamp}', ln=True)

        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, '· Summary:', ln=True)

        pdf.set_font('helvetica', '', 12)
        pdf.multi_cell(0, 7, text, ln=True)

        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, '· Sentiment Analysis:', ln=True)

        pdf.set_font('helvetica', 'I', 10)
        pdf.cell(0, 10, f'Positives = {pos}% | Negatives = {neg}% | Neutral = {neu}%', ln=True)
        i += 1

    # save pdf
    pdf.output(f'{title}.pdf')
