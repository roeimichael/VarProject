import pandas as pd

df = pd.read_csv('./data/alltickers.csv')
yahoo = pd.read_excel('./data/Yahoo.xlsx')
ourtickers = df['Ticker'].tolist()
alltickers = yahoo['Yahoo Stock Tickers'].tolist()
same = set(alltickers).intersection(set(ourtickers))
# print(alltickers)
# print(alltickers)
df = pd.read_csv('./data/alltickers.csv')
df['Tickers'] = same
df.to_csv('./data/alltickers.csv')