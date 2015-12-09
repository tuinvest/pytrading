import requests
import numpy as np
import pandas.io.data as web

STD_PROVIDER = 'yahoo'

''' Abstract Gateway used as an interface '''
class AbstractGateway():
    def load_from_std_provider(self, symbol):
        raise NotImplementedError('Function not implemented!')

    def load(self, symbol, provider):
        raise NotImplementedError('Function not implemented!')

''' General Gateway that is not dependend on it's provider '''
class GeneralGateway(AbstractGateway):
    def load_from_std_provider(self, symbol):
        try:
            data = web.DataReader(symbol, STD_PROVIDER)
        except:
            raise ValueError('Symbol not found!')
        return data

    def load(self, symbol, provider):
        try:
            data = web.DataReader(symbol, provider)
        except:
            raise ValueError('Symbol not found!')
        if data is None:
            raise ValueError('No data found! Could be a wrong provider')
        return data


''' Deprecated (delete after legacy-support is not needed) '''
class YahooGateway:
    def load(self, symbol):
        r = requests.get('http://ichart.finance.yahoo.com/table.csv?s='+symbol+'&a=0&b=01&c=2000&g=d&ignore=.csv')

        data = r.text.split('\n')[1:]
        chart = []
        days = []

        for line in reversed(data): # order by date ASC
            line = line.split(',')
            if(len(line) >= 2):
                if int(line[5]) != 0:
                    days.append(line[0])
                    chart.append(
                        [
                            float(line[1]), # open
                            float(line[2]), # high
                            float(line[3]), # low
                            float(line[4]), # close
                            int(line[5]),  # volume
                            float(line[6]),  # adjusted close
                        ]
                    )
        return days, np.array(chart)