import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt


class Position:
    def __init__(self, tickerX, tickerY, startDate, endDate, operationX, operationY, openPrice, ClosePrice):
        self.ClosePrice = ClosePrice
        self.openPrice = openPrice
        self.operationY = operationY
        self.operationX = operationX
        self.endDate = endDate
        self.tickerX = tickerX
        self.tickerY = tickerY
        self.startDate = startDate

    def __str__(self):
        return f"position pair is :{self.tickerX} - {self.operationX} and {self.tickerY} - {self.operationY}"


def create_ratio(tickerup, tickerdown):
    dataup = pdr.get_data_yahoo(tickerup, start="2018-01-01", end=dt.date.today(), period='1h')['Close'].tolist()
    dataup = [round(item, 2) for item in dataup]
    datadown = pdr.get_data_yahoo(tickerdown, start="2018-01-01", end=dt.date.today(), period='1h')['Close'].tolist()
    datadown = [round(item, 2) for item in datadown]
    divisionResults = [i / j for i, j in zip(datadown, dataup)]
    print(divisionResults)


if __name__ == '__main__':
    df = pd.read_csv(f'./data/pairs_exmp.csv')
