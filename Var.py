import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
import openpyxl
from openpyxl.styles import PatternFill
from scipy.stats import norm

INITIAL_INVESTMENT = 1000000
NET_LIQUIDITY = 294000
WEIGHTS = np.array([1])


def calc_var(initial_investment, weights, data):
    returns = data.pct_change()
    cov_matrix = returns.cov()
    avg_rets = returns.mean()
    port_mean = avg_rets.dot(weights)
    port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
    mean_investment = (1 + port_mean) * initial_investment
    stdev_investment = initial_investment * port_stdev
    conf_level1 = 0.05
    cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)
    var_1d1 = initial_investment - cutoff1
    return var_1d1


def add_var_to_alltickers(path, initial_inv, weights):
    df = pd.read_excel(path)
    df['Var'] = 0
    df['Qual'] = 0
    tickers = df['Symbol'].tolist()
    bad_tickers = []
    for index, ticker in enumerate(tickers):
        try:
            data = pdr.get_data_yahoo([ticker], start="2018-01-01", end=dt.date.today())['Close']
            df.at[index, 'Var'] = calc_var(initial_inv, weights, data)
        except:
            bad_tickers.append(ticker)
    print(bad_tickers)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.sort_values(by='Var')
    df.to_excel(path, index=False)


if __name__ == '__main__':
    add_var_to_alltickers("./data/alltickers.xlsx", INITIAL_INVESTMENT, np.array([1]))

