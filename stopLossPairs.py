import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
import stopLossFunctions

PAIRS_PATH = './data/pairs_exmp.csv'
POSITION_DIVIDED_PATH = 'positions_divided.csv'
PORTFOLIO_PATH = 'portfolio.csv'
class Position:
    def __init__(self, tickerLong, tickerShort, startDate, endDate, operationLong, operationShort, openPriceLong,
                 openPriceShort,
                 ClosePriceLong, ClosePriceShort, terminatedOrClosed):
        self.tickerLong = tickerLong
        self.tickerShort = tickerShort
        self.startDate = startDate
        self.endDate = endDate
        self.operationLong = operationLong
        self.operationShort = operationShort
        self.openPriceLong = openPriceLong
        self.openPriceShort = openPriceShort
        self.ClosePriceLong = ClosePriceLong
        self.ClosePriceShort = ClosePriceShort
        self.terminatedOrClosed = terminatedOrClosed

    def __str__(self):
        return f"position pair is :{self.tickerLong} - {self.operationLong} and {self.tickerShort} - {self.operationShort}"

    def create_ratio(self, item):
        long_position = yf.Ticker(self.tickerLong)
        short_position = yf.Ticker(self.tickerShort)
        date_1 = dt.datetime.strptime(self.endDate, "%Y-%m-%d")
        end_date = date_1 + dt.timedelta(days=1)
        long_position = long_position.history(start=self.startDate, end=end_date, interval='1h')[item].tolist()
        short_position = short_position.history(start=self.startDate, end=end_date, interval='1h')[item].tolist()
        long_position = [round(item, 2) for item in long_position]
        short_position = [round(item, 2) for item in short_position]
        divisionResults = [i / j for i, j in zip(long_position, short_position)]
        return divisionResults


def create_positions(data):
    positions_list = []
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    data = data.loc[200:]
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
        if df.loc[0]['Operation'] == 'Buy':
            l, s = 0, 1
        else:
            l, s = 1, 0
        TickerLong = df.loc[l]['Ticker'].split(':')[1]
        TickerShort = df.loc[s]['Ticker'].split(':')[1]
        OperationLong = df.loc[l]['Operation']
        OperationShort = df.loc[s]['Operation']
        OpenPriceLong = df.loc[l + 2]['Open price']
        OpenPriceShort = df.loc[s + 2]['Open price']
        ClosePriceLong = df.loc[l + 2]['Close price']
        ClosePriceShort = df.loc[s + 2]['Close price']
        StartDate = df.loc[0]['Date']
        EndDate = df.loc[2]['Date']
        terminatedOrClosed = df.loc[2]['Operation']
        pos = Position(TickerLong, TickerShort, StartDate, EndDate, OperationLong, OperationShort, OpenPriceLong,
                       OpenPriceShort,
                       ClosePriceLong, ClosePriceShort, terminatedOrClosed)
        positions_list.append(pos)
    return positions_list


def create_df_from_objects(objects):
    data = []
    for obj in objects:
        obj_data = vars(obj)
        data.append(obj_data)
    df = pd.DataFrame(data)
    df.columns = list(vars(objects[0]).keys())
    return df


def create_files():
    df = pd.read_csv(PAIRS_PATH)
    portfolio = create_positions(df)
    portfolio_df = create_df_from_objects(portfolio)
    portfolio_df.to_csv(PORTFOLIO_PATH, index=False)
    closing_position = []
    for position in portfolio:
        div = position.create_ratio('Close')
        closing_position.append(div)
    closing_positions_df = pd.DataFrame(closing_position)
    closing_positions_df.to_csv(POSITION_DIVIDED_PATH, index=False, header=False)


if __name__ == '__main__':
    create_files()
    df = pd.read_csv(PAIRS_PATH)
    portfolio = create_positions(df)
    closing_positions_df = pd.read_csv(POSITION_DIVIDED_PATH, header=None)
    percentage = 0.95
    stopLossFunctions.fixed_percentage_stop_loss(portfolio, closing_positions_df, percentage)
