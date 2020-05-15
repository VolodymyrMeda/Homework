from Queue.linkedqueue import LinkedQueue
from ebaysdk.finding import Connection as Finding
import xlsxwriter
from fpdf import FPDF


class DataOperations:
    '''Working with API and data received'''

    def __init__(self):
        '''
        Initializing a queue for working with data
        '''
        self.queue = LinkedQueue()

    def get_json_data(self, keyword, price_from, price_to):
        '''
        Method returns a dictionary with data collected
        keyword: str -
        '''
        try:
            api = Finding(config_file='ebay.json', appid='Volodymy-Expendit-PRD-3196809ca-9c1b019a')

            itemFilter = [{"name": "MaxPrice", "value": str(price_to),
                           "paramName": "Currency", "paramValue": "USD"},
                          {"name": "MinPrice", "value": str(price_from),
                           "paramName": "Currency", "paramValue": "USD"}]

            request = {'keywords': keyword, 'itemFilter': itemFilter}
            response = api.execute('findItemsAdvanced', request)

            return response.dict()['searchResult']['item']

        except KeyError:
            return None

    def get_proper_data(self, raw_result):
        '''
        Getting proper data from the dictionary
        '''
        for page in raw_result:
            if page['shippingInfo']['shippingType'] in ('Free', 'Calculated'):
                self.queue.add((page['title'],
                                page['sellingStatus']['currentPrice']['value'] + ' ' +
                                page['sellingStatus']['currentPrice']['_currencyId'],
                                page['viewItemURL'], page['location'], 'Free'))

    def data_excel_repr(self):
        '''
        Converting data to the excel file
        '''
        workbook = xlsxwriter.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()

        columns = ['Title', 'Price', 'Link', 'Location', 'Shipping']

        row = 0
        col = 0

        for item in columns:
            worksheet.write(row, col, item)
            col += 1

        row = 1
        col = 0

        for result in self.queue:
            worksheet.write(row, col, result[0])
            col += 1
            worksheet.write(row, col, result[1])
            col += 1
            worksheet.write(row, col, result[2])
            col += 1
            worksheet.write(row, col, result[3])
            col += 1
            worksheet.write(row, col, result[4])

            row += 1
            col = 0

        workbook.close()

    def data_pdf_repr(self):
        '''
        Converting data to the PDF file
        '''
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for result in self.queue:
            pdf.cell(200, 15, txt=f'_________________________________________________________________________________',
                     ln=1, align="C")

            pdf.cell(200, 10, txt=f'Title: {result[0]}', ln=1, align="L")

            pdf.cell(200, 10, txt=f'Price: {result[1]}', ln=1, align="L")

            pdf.cell(200, 10, txt=f'Link: {result[2]}', ln=1, align="L")

            pdf.cell(200, 10, txt=f'Location: {result[3]}', ln=1, align="L")

            pdf.cell(200, 10, txt=f'Shipping: {result[4]}', ln=1, align="L")

        pdf.output("result.pdf")

        self.queue.clear()
