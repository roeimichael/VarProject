import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
import seaborn as sns

PORTFOLIO_PATH_AFTER_TRANS = "./data/actualportfolio.xlsx"
SECTOR_PRECENTAILE = 0.2
MAX_PORTFOLIO_SIZE = 20
MAX_PRECENTAGE_PORTFOLIO = 1.3
ALLOWED_BAD_POSITIONS = 0
ALLOWED_RATIO_OF_GOOD_TO_TOTAL = 0.4


def check_sectors(df):
    sectorSum = df.groupby(['Sector']).sum()
    for index, row in sectorSum.iterrows():
        if row['Protfilio Precentage'] > SECTOR_PRECENTAILE:
            print(f"{index} has too man open positions with {row['Protfilio Precentage']}")


def check_percentage(df):
    for index, row in df.iterrows():
        if (row['Protfilio Precentage'] > 0.05 and row['Leveraged '] == 'No') or (
                row['Protfilio Precentage'] > 0.09 and row['Leveraged '] == 'Yes'):
            print(f"position of ticker {row['Symbol']} is too big with size of {row['Protfilio Precentage']}")


def check_amount(df):
    positions = df.groupby(['Symbol']).count().sum()['Position']
    if positions > MAX_PORTFOLIO_SIZE:
        print(f"too many positions in portfolio current amount :{positions}")


def check_pos_size(df):
    if df['Protfilio Precentage'].sum() > MAX_PRECENTAGE_PORTFOLIO:
        print(
            f"portfolio isnt balanced, a risk of liquidation approaching {round(df['Protfilio Precentage'].sum(), 2)}")


def check_var_quality(df):
    qualitiys = df.groupby(['Qual']).count()
    mid, good, bad = qualitiys['Symbol']['MID'], qualitiys['Symbol']['GOOD'], qualitiys['Symbol']['BAD']
    total = mid + good
    if bad > ALLOWED_BAD_POSITIONS:
        print("there are stocks with bad quality VAR in portfolio")
    if good / total < ALLOWED_RATIO_OF_GOOD_TO_TOTAL:
        print("under 40% of stocks are good and more than 60% are mid")


def get_corr_mat(df):
    data = pdr.get_data_yahoo(df['Symbol'], start="2022-01-01", end=dt.date.today())['Close']
    corr = data.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(20, 20))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, annot=True, vmax=.3, vmin=-.3, center=0, square=True, linewidths=.5,
                cbar_kws={"shrink": .5})
    f.savefig('corr_mat.png')


if __name__ == '__main__':
    df = pd.read_excel(PORTFOLIO_PATH_AFTER_TRANS)
    check_sectors(df)
    # check_percentage(df)
    check_amount(df)
    check_pos_size(df)
    get_corr_mat(df)
    print(df)
