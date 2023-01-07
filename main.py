import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
import openpyxl
from openpyxl.styles import PatternFill
import Var

INITIAL_INVESTMENT = 1000000
NET_LIQUIDITY = 294000
WEIGHTS = np.array([1])
ALL_TICKERS_CSV_PATH = "./data/alltickers.xlsx"
PORTFOLIO_PATH_ORIGINAL = './data/actualportfolio.csv'
PORTFOLIO_PATH_AFTER_TRANS = "./data/actualportfolio.xlsx"


def check_tickers():
    tickers = get_list('alltickers')
    bad_stocks = []
    for index, ticker in enumerate(tickers):
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


def transform_df(df_path, net_liquidity):
    df = pd.read_csv(df_path)
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
    df.to_excel(PORTFOLIO_PATH_AFTER_TRANS, index=False)


def coloring_portfolio(filename):
    wb = openpyxl.load_workbook(filename=filename)
    ws = wb['Sheet1']
    df = pd.read_excel(filename)
    length = df.shape[0] + 2
    fill_cell1 = PatternFill(patternType='solid', fgColor='FC2C03')
    fill_cell2 = PatternFill(patternType='solid', fgColor='FFFF00')
    fill_cell3 = PatternFill(patternType='solid', fgColor='35FC03')
    if filename == ALL_TICKERS_CSV_PATH:
        c1, c2 = 'B', 'C'
    else:
        c1, c2 = 'F', 'G'
    for i in range(2, round(length / 3)):
        ws[f'{c1}{i}'].fill = fill_cell3
        ws[f'{c2}{i}'] = 'GOOD'
    for i in range(round(length / 3), round(9 * length / 10)):
        ws[f'{c1}{i}'].fill = fill_cell2
        ws[f'{c2}{i}'] = 'MID'
    for i in range(round(9 * length / 10), length):
        ws[f'{c1}{i}'].fill = fill_cell1
        ws[f'{c2}{i}'] = 'BAD'
    wb.save(filename=filename)


def get_var(portfolio_path, alltickers_path):
    coloring_portfolio(alltickers_path)
    alltickers_df = pd.read_excel(alltickers_path)
    alltickers_list = alltickers_df['Symbol'].tolist()
    alltickers_df = alltickers_df.loc[:, ~alltickers_df.columns.str.contains('^Unnamed')]
    portfolio_df = pd.read_excel(portfolio_path)
    portfolio_df['Var'] = 0
    portfolio_df['Qual'] = 0
    portfolio_tickers = portfolio_df['Symbol']
    alltickers_df.set_index("Symbol", drop=False, inplace=True)
    portfolio_df.set_index("Symbol", drop=False, inplace=True)
    for tick in portfolio_tickers:
        if tick in alltickers_list:
            portfolio_df.at[tick, 'Var'] = alltickers_df.at[tick, 'Var']
            portfolio_df.at[tick, 'Qual'] = alltickers_df.at[tick, 'Qual']
        else:
            data = pdr.get_data_yahoo([tick], start="2018-01-01", end=dt.date.today())['Close']
            cur_var = Var.calc_var(INITIAL_INVESTMENT, WEIGHTS, data)
            alltickers_df.loc[len(alltickers_df.index)] = [tick, cur_var, 0]
            alltickers_df = alltickers_df.sort_values(by='Var')
            alltickers_df.to_excel(alltickers_path, index=False)
            coloring_portfolio(alltickers_path)
            alltickers_df = pd.read_excel(alltickers_path)
            alltickers_df.set_index("Symbol", drop=False, inplace=True)
            portfolio_df.at[tick, 'Var'] = alltickers_df.at[tick, 'Var']
            portfolio_df.at[tick, 'Qual'] = alltickers_df.at[tick, 'Qual']

    portfolio_df = portfolio_df.sort_values(by='Var')
    alltickers_df = alltickers_df.sort_values(by='Var')
    alltickers_df.to_excel(alltickers_path, index=False)
    portfolio_df.to_excel(portfolio_path, index=False)


if __name__ == '__main__':
    transform_df(PORTFOLIO_PATH_ORIGINAL, NET_LIQUIDITY)  # only for new incoming files
    get_var(PORTFOLIO_PATH_AFTER_TRANS, ALL_TICKERS_CSV_PATH)  # get var and coloring
