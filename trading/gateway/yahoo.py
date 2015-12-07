import requests
import numpy as np

class YahooGateway:
    def load(self, symbol):
        range = '3y'
        r = requests.get('http://chartapi.finance.yahoo.com/instrument/1.0/'+symbol+'/chartdata;type=quote;range='+range+'/csv')
        split = {'1d': 17, '7d': 24, '1m': 18, '3m': 18, '6m': 18, '1y': 18, '3y': 18, 'my': 17}

        data = r.text.split("\n")[split[range]:]
        chart = []
        days = []
        for line in data:
            line = line.split(",")
            if(len(line) >= 2):
                if int(line[5]) != 0:
                    days.append(line[0])
                    chart.append(
                        [
                            float(line[3]), # open
                            float(line[2]), # high
                            float(line[4]), # low
                            float(line[1]), # close
                            float(line[5])  # volume
                        ]
                    )
        return days, np.array(chart)

if __name__ == '__main__':
    gateway = YahooGateway()
    days, data = gateway.load("ADS.DE")
    print days, data