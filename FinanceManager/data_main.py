from ebaysdk.finding import Connection as Finding
from QueueLinked.linkedqueue import LinkedQueue
from fpdf import FPDF
import xlsxwriter


class DataOperations:
    """Class for working with Ebay API and data received"""

    def __init__(self):
        """
        Initializing a queue for working with data
        queue: Queue instance
        """
        self.queue = LinkedQueue()

    def get_json_data(self, keyword, price_from, price_to):
        """
        Method returns a dictionary with data collected

        keyword: str - the name of the product user wants to find
        price_from: str - start of the price range
        price_to: str - end of the price range

        return: dict
        """
        try:
            api = Finding(config_file='ebay.json', appid='Volodymy-Expendit-PRD-3196809ca-9c1b019a')

            # allows to set the price range
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
        """
        Works with data received and gets data
        that is needed for further actions

        raw_result: dict - dictionary with data
        received from API
        """
        # returns None and stops if products were not found
        if raw_result is None:
            return None

        # adds tuples with the proper information
        # to the queue for cosy further actions
        for page in raw_result:
            if page['shippingInfo']['shippingType'] in ('Free', 'Calculated'):

                self.queue.add((page['title'],
                                page['sellingStatus']['currentPrice']['value'] + ' ' +
                                page['sellingStatus']['currentPrice']['_currencyId'],
                                page['viewItemURL'], page['location'], 'Free'))

    def data_excel_repr(self):
        """
        Uses the queue with data prepared in
        order to generate an excel file
        """
        # returns None and stops if products were not found
        if self.queue.isEmpty() is True:
            return None

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
        """
        Uses the queue with data prepared in
        order to generate a PDF file
        """
        # returns None and stops if products were not found
        if self.queue.isEmpty() is True:
            return None

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=7)

        for result in self.queue:
            pdf.cell(200, 15,
                     txt=f'_________________________________________________________________________________',
                     ln=1, align="L")

            pdf.cell(200, 10, txt=str(f'Title: {result[0]}'.encode(encoding='UTF-8'))[2:-1], ln=1, align="L")

            pdf.cell(200, 10, txt=str(f'Price: {result[1]}'.encode(encoding='UTF-8'))[2:-1], ln=1, align="L")

            pdf.cell(200, 10, txt=str(f'Link: {result[2]}'.encode(encoding='UTF-8'))[2:-1], ln=1, align="L")

            pdf.cell(200, 10, txt=str(f'Location: {result[3]}'.encode(encoding='UTF-8'))[2:-1], ln=1, align="L")

            pdf.cell(200, 10, txt=str(f'Shipping: {result[4]}'.encode(encoding='UTF-8'))[2:-1], ln=1, align="L")

        pdf.output("results.pdf")

        self.queue.clear()