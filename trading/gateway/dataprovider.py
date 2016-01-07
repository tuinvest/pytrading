import os
import pandas as pd
import pandas.io.data as web
import sqlite3 as sql

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

''' Gateway to a SQLITE3 database '''
class Database(AbstractGateway):
    def __init__(self, filename='pytrading.db'):
        self.name = filename
        if not filename in os.listdir():
            __setup_database__(filename)
        self.con = sql.connect(self.name)

    def __del__(self):
        self.con.close()

    def __setup_database__(filename='pytrading.db'):
        if filename in os.listdir():
            os.remove(filename)
        con = sql.connect(filename)
        c = con.cursor()

        # SQLITE-DBs have a "rowid" by default as primary key
        c.execute(  "CREATE TABLE Stockdata (\
                    Symbol TEXT NOT NULL,\
                    Date TEXT NOT NULL,\
                    Open REAL NOT NULL,\
                    High REAL NOT NULL,\
                    Low REAL NOT NULL,\
                    Close REAL NOT NULL,\
                    Adj_Close REAL NOT NULL,\
                    Volume INTEGER NOT NULL);")

        # JUST FOR TESTING PURPOSES!
        data = [('GOOG', '2010-03-04', 155.5, 156.1, 155.1, 155.4, 155.4, 145010),
                ('AAPL', '2010-03-04', 90.2, 91, 90.1, 90.9, 90.9, 983923),
                ('GOOG', '2010-03-05', 157.1, 157.2, 155.9, 156.4, 156.4, 1388300),
                ('AAPL', '2010-03-05', 91.2, 92, 91.1, 91.9, 91.9, 283923),
                ]
        c.executemany('INSERT INTO Stockdata VALUES (?,?,?,?,?,?,?,?)', data)

        con.commit()
        con.close()

    def load(self, symbol, provider=None):
        return pd.read_sql_query(
                sql = "SELECT * FROM Stockdata WHERE Symbol = '{}'".format(symbol),
                con = self.con,
                index_col = 'Date'
            )

