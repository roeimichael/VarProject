import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt


class Position:
    def __init__(self, tickerX, tickerY, startDate, endDate, operationX, operationY, openPriceX, openPriceY,ClosePriceX, ClosePriceY, terminatedOrClosed):
        self.tickerX = tickerX
        self.tickerY = tickerY
        self.startDate = startDate
        self.endDate = endDate
        self.operationX = operationX
        self.operationY = operationY
        self.openPriceX = openPriceX
        self.openPriceY = openPriceY
        self.ClosePriceX = ClosePriceX
        self.ClosePriceY = ClosePriceY
        self.terminatedOrClosed = terminatedOrClosed

    def __str__(self):
        return f"position pair is :{self.tickerX} - {self.operationX} and {self.tickerY} - {self.operationY}"


def create_ratio(tickerup, tickerdown):
    dataup = pdr.get_data_yahoo(tickerup, start="2018-01-01", end=dt.date.today(), period='1h')['Close'].tolist()
    dataup = [round(item, 2) for item in dataup]
    datadown = pdr.get_data_yahoo(tickerdown, start="2018-01-01", end=dt.date.today(), period='1h')['Close'].tolist()
    datadown = [round(item, 2) for item in datadown]
    divisionResults = [i / j for i, j in zip(datadown, dataup)]
    print(divisionResults)


def create_positions(data):
    positions_list = []
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    data = data.drop(columns=['Z-Score', 'Commissions', 'Shares', 'P/L'], axis=0)
    positions = [[] for _ in range(round((len(data) / 4)))]
    j = -1
    for index, row in data.iterrows():
        if index % 4 == 0:
            j = j + 1
        positions[j].append(row)
    for item in positions:
        df = pd.DataFrame(item)
        df = df.reset_index()
        df = df.drop(columns=['index'], axis=0)
        TickerX = df.loc[0]['Ticker'].split(':')[1]
        TickerY = df.loc[1]['Ticker'].split(':')[1]
        StartDate = df.loc[0]['Date']
        EndDate = df.loc[2]['Date']
        OperationX = df.loc[0]['Operation']
        OperationY = df.loc[1]['Operation']
        OpenPriceX = df.loc[2]['Open price']
        OpenPriceY = df.loc[2]['Open price']
        ClosePriceX = df.loc[3]['Close price']
        ClosePriceY = df.loc[3]['Close price']
        terminatedOrClosed = df.loc[2]['Operation']
        pos = Position(TickerX, TickerY, StartDate, EndDate, OperationX, OperationY, OpenPriceX, OpenPriceY,
                       ClosePriceX, ClosePriceY,terminatedOrClosed)
        positions_list.append(pos)
    return positions_list


if __name__ == '__main__':
    df = pd.read_csv(f'./data/pairs_exmp.csv')
    positions = create_positions(df)
