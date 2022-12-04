import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import datetime as dt
from scipy.stats import norm
import openpyxl
from openpyxl.styles import PatternFill


def get_var(initial_investment, weights, data):
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


def coloring(length):
    wb = openpyxl.load_workbook(filename='./data/alltickers.xlsx')
    ws = wb['Sheet1']
    fill_cell1 = PatternFill(patternType='solid', fgColor='FC2C03')
    fill_cell2 = PatternFill(patternType='solid', fgColor='FFFF00')
    fill_cell3 = PatternFill(patternType='solid', fgColor='35FC03')
    for i in range(2, round(length / 3)):
        ws[f'G{i}'].fill = fill_cell3
        ws[f'H{i}'] = 'GOOD'
    for i in range(round(length / 3), round(9 * length / 10)):
        ws[f'G{i}'].fill = fill_cell2
        ws[f'H{i}'] = 'MID'
    for i in range(round(9 * length / 10), length):
        ws[f'G{i}'].fill = fill_cell1
        ws[f'H{i}'] = 'BAD'
    wb.save(filename='./data/alltickers.xlsx')

