import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt
import stopLossFunctions

PAIRS_PATH = './data/pairs/pairs_exmp.csv'
POSITION_DIVIDED_PATH = './data/pairs/'
PORTFOLIO_PATH = './data/pairs/portfolio.csv'


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
        start_date = dt.datetime.strptime(self.startDate, "%m/%d/%Y")
        date_1 = dt.datetime.strptime(self.endDate, "%m/%d/%Y")
        end_date = date_1 + dt.timedelta(days=1)
        long_position = long_position.history(start=start_date, end=end_date, interval='1h')[item].tolist()
        short_position = short_position.history(start=start_date, end=end_date, interval='1h')[item].tolist()
        long_position = [round(item, 2) for item in long_position]
        short_position = [round(item, 2) for item in short_position]
        divisionResults = [i / j for i, j in zip(long_position, short_position)]
        return divisionResults


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


def create_price_series(portfolio, name):
    serial_position = []
    for position in portfolio:
        div = position.create_ratio(name)
        serial_position.append(div)
    series_df = pd.DataFrame(serial_position)
    series_df.to_csv(f'{POSITION_DIVIDED_PATH}{name}_series.csv', index=False, header=False)
    return series_df


def create_portfolio():
    df = pd.read_csv(PAIRS_PATH)
    portfolio = create_positions(df)
    portfolio_df = create_df_from_objects(portfolio)
    portfolio_df.to_csv(PORTFOLIO_PATH, index=False)
    return portfolio


if __name__ == '__main__':
    df = pd.read_csv(PAIRS_PATH)
    portfolio = create_portfolio()
    # closing_positions_df = create_price_series(portfolio, 'Close')
    # high_positions_df = create_price_series(portfolio, 'High')
    # low_positions_df = create_price_series(portfolio, 'Low')
    closing_positions_df = pd.read_csv(f'{POSITION_DIVIDED_PATH}Close_series.csv')
    high_positions_df = pd.read_csv(f'{POSITION_DIVIDED_PATH}High_series.csv')
    low_positions_df = pd.read_csv(f'{POSITION_DIVIDED_PATH}Low_series.csv')
    # percentage = 0.95
    # time = 10
    std = 3
    # stopLossFunctions.fixed_percentage_stop_loss(portfolio, closing_positions_df, percentage)
    # stopLossFunctions.fixed_time_stop_loss(portfolio, closing_positions_df, time)
    # stopLossFunctions.atr_stop_loss(portfolio,closing_positions_df,high_positions_df,low_positions_df,0.04)
    # stopLossFunctions.std_stop_loss(portfolio, closing_positions_df, std)
    stopLossFunctions.std_stop_loss(portfolio, closing_positions_df, 14, 3)
