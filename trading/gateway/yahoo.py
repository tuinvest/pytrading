import requests
import numpy as np
from datetime import datetime

class YahooGateway:
    def load(self, symbol):
        r = requests.get('http://ichart.finance.yahoo.com/table.csv?s='+symbol+'&a=0&b=01&c=2000&g=d&ignore=.csv')

        data = r.text.split("\n")[1:]
        chart = []
        days = []

        for line in reversed(data): # order by date ASC
            line = line.split(",")
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