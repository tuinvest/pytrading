import pandas.io.data as web

STD_PROVIDER = 'yahoo'

''' Abstract Gateway used as an interface '''
class AbstractGateway():
    def load(self, symbol, provider):
        raise NotImplementedError('Function not implemented!')

''' General Gateway that is not dependend on it's provider '''
class YahooGateway(AbstractGateway):
    def load(self, symbol, provider=STD_PROVIDER):
        try:
            data = web.DataReader(symbol, provider)
        except:
            raise ValueError('Symbol not found!')
        if data is None:
            raise ValueError('No data found! Could be a wrong provider')
        return data
