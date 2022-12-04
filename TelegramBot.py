import telebot
import yfinance as yf
import extremities
import pandas as pd

bot = telebot.TeleBot('5689362726:AAHCnBPsRAbhb894FzkZmLyG5ItXk1NF7c4')


@bot.message_handler(commands=['Run'])
def check_sectors(message):
    df = pd.read_excel('./data/finished.xlsx')
    str = ""
    sectorSum = df.groupby(['Sector']).sum()
    for index, row in sectorSum.iterrows():
        if row['Protfilio Precentage'] > 0.2:
            str += f"|  {index} has too man open positions with {row['Protfilio Precentage']}  |\n"
    str += "-----------------------------------------\n"
    for index, row in df.iterrows():
        # and row['Leveraged'] == 'No') or (
        # row['Protfilio Precentage'] > 0.09 and row['Leveraged'] == 'Yes')
        if row['Protfilio Precentage'] > 0.05:
            str += f"|  position of ticker {row['Symbol'].upper()} is too big with size of {row['Protfilio Precentage']}  |\n"
    str += "-----------------------------------------\n"
    positions = df.groupby(['Symbol']).count().sum()['Position']
    if positions > 20:
        str += f"|  too many positions in portfolio current amount :{positions}  |\n"
    str += "-----------------------------------------\n"
    if df['Protfilio Precentage'].sum() > 1.3:
        str += f"|  portfolio isnt balanced, a risk of liquidation approaching {round(df['Protfilio Precentage'].sum(), 2)}  |\n"
    str += "-----------------------------------------\n"
    bot.reply_to(message, str)

if __name__ == '__main__':
    bot.polling()
