from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def ebayapiexample():
    '''
    Example of using an ebay API
    Returns information about one found product placed on ebay
    ('Stephen King The Shining' - as an example)
    ebay.json - api configuration
    '''
    try:
        api = Finding(config_file='ebay.json', appid='*')

        request = {'keywords': 'Stephen King The Shining'}
        response = api.execute('findItemsAdvanced', request)

        return response.dict()['searchResult']['item'][0]['sellingStatus']

    except ConnectionError as err:
        return err.response.dict()


if __name__ == '__main__':
    print(ebayapiexample())