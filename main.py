import Var
import numpy as np
import pandas as pd
import yfinance as yf
import os
from pandas_datareader import data as pdr
import datetime as dt


def check_tickers():
    tickers = get_list('alltickers')
    bad_stocks = []
    for index,ticker in enumerate(tickers):
        try:
            print(index)
            data = pdr.get_data_yahoo(ticker)
        except:
            bad_stocks.append(ticker)
    print(bad_stocks)


def get_list(filename):
    list = []
    with open(f'./data/{filename}.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            list.append(x)
    return list


def transform_df(df_name, net_liquidity):
    df = pd.read_csv(f'{df_name}.csv')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.drop(['Daily P&L', 'Last', 'Change', 'Unrealized P&L', 'Market Value'], axis=1)
    df.rename(columns={'Financial Instrument': 'Symbol'}, inplace=True)
    df['Sector'] = ''
    df['Amount'] = 0.0
    for index, row in df.iterrows():
        df.at[index, 'Position'] = df.at[index, 'Position'].replace(',', '')
        ticker = df.at[index, 'Symbol']
        tick = yf.Ticker(ticker)
        if 'sector' in tick.info:
            df.at[index, 'Sector'] = tick.info['sector']
        else:
            df.at[index, 'Sector'] = 'ETF'
    df["Position"] = pd.to_numeric(df["Position"])
    df['Amount'] = df['Position'] * df['Avg Price']
    df['Type'] = np.where(df['Amount'] > 0, 'LONG', 'SHORT')
    df = df.drop(['Avg Price', 'Position'], axis=1)
    df['Percentage'] = abs(df['Amount']) / net_liquidity
    cols = ['Symbol', 'Type', 'Amount', 'Percentage', 'Sector']
    df = df[cols]
    df.rename(columns={'Type': 'Position', 'Percentage': 'Protfilio Precentage'}, inplace=True)
    return df


if __name__ == '__main__':
    # df = transform_df('./data/actualportfolio', net_liquidity=294000)
    # df.set_index('Symbol')
    df = pd.read_csv('./data/alltickers.csv')
    df['Var'] = 0
    df['Qual'] = 0
    tickers = df['Ticker'].tolist()
    weights = np.array([1])
    initial_investment = 1000000
    bad_tickers = []
    for index, ticker in enumerate(tickers):
        try:
            data = pdr.get_data_yahoo([ticker], start="2018-01-01", end=dt.date.today())['Close']
            df.at[index, 'Var'] = Var.get_var(initial_investment, weights, data)
        except:
            bad_tickers.append(ticker)
    print(bad_tickers)
    df = df.sort_values(by='Var')
    df.to_excel('./data/alltickers.xlsx')
    Var.coloring(len(tickers) + 2)
