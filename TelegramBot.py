import telebot
import yfinance as yf
import extremities
import pandas as pd

bot = telebot.TeleBot('5689362726:AAHCnBPsRAbhb894FzkZmLyG5ItXk1NF7c4')
SECTOR_PRECENTAILE = 0.2
MAX_PORTFOLIO_SIZE = 20
MAX_PRECENTAGE_PORTFOLIO = 1.3
ALLOWED_BAD_POSITIONS = 0
ALLOWED_RATIO_OF_GOOD_TO_TOTAL = 0.4

@bot.message_handler(commands=['Run'])
def check_sectors(message):
    df = pd.read_excel('./data/finished.xlsx')
    str = ""
    sectorSum = df.groupby(['Sector']).sum()
    for index, row in sectorSum.iterrows():
        if row['Protfilio Precentage'] > SECTOR_PRECENTAILE:
            str += f"|  {index} has too man open positions with {row['Protfilio Precentage']}  |\n"
    str += "-----------------------------------------\n"
    for index, row in df.iterrows():
        # and row['Leveraged'] == 'No') or (
        # row['Protfilio Precentage'] > 0.09 and row['Leveraged'] == 'Yes')
        if row['Protfilio Precentage'] > 0.05:
            str += f"|  position of ticker {row['Symbol'].upper()} is too big with size of {row['Protfilio Precentage']}  |\n"
    str += "-----------------------------------------\n"
    positions = df.groupby(['Symbol']).count().sum()['Position']
    if positions > MAX_PORTFOLIO_SIZE:
        str += f"|  too many positions in portfolio current amount :{positions}  |\n"
    str += "-----------------------------------------\n"
    if df['Protfilio Precentage'].sum() > MAX_PRECENTAGE_PORTFOLIO:
        str += f"|  portfolio isnt balanced, a risk of liquidation approaching {round(df['Protfilio Precentage'].sum(), 2)}  |\n"
    str += "-----------------------------------------\n"
    qualitiys = df.groupby(['Qual']).count()
    mid, good, bad = qualitiys['Symbol']['MID'], qualitiys['Symbol']['GOOD'], qualitiys['Symbol']['BAD']
    total = mid +good
    if bad > ALLOWED_BAD_POSITIONS:
        str += "there are stocks with bad quality VAR in portfolio\n"
    if good/total < ALLOWED_RATIO_OF_GOOD_TO_TOTAL:
        str += "under 40% of stocks are good and more than 60% are mid\n"
    bot.reply_to(message, str)


if __name__ == '__main__':
    bot.polling()
