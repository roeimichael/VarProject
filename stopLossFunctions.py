import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas_datareader as pdr


def fixed_percentage_stop_loss(portfolio, closing_positions_df, percentage):
    for i in range(len(closing_positions_df)):
        position = portfolio[i]
        closing_prices = closing_positions_df.iloc[i].tolist()
        starting_price_ratio = position.openPriceLong / position.openPriceShort
        closing_price_ratio = position.ClosePriceLong / position.ClosePriceShort
        # pprint(vars(position))
        # print(starting_price_ratio)
        for j in range(len(closing_prices)):
            current_close = closing_prices[j]
            gain_since_open = current_close / starting_price_ratio
            if gain_since_open > percentage:
                print(
                    f" position #{i} should have closed at price: {round(current_close, 2)} instead closed at {round(closing_price_ratio, 2)}")
                break


def fixed_time_stop_loss(portfolio, closing_positions_df,
                         time):  # time should be in a foramt of hours since the opening of the position
    for i in range(len(closing_positions_df)):
        position = portfolio[i]
        closing_prices = closing_positions_df.iloc[i].tolist()
        starting_price_ratio = position.openPriceLong / position.openPriceShort
        closing_price_ratio = position.ClosePriceLong / position.ClosePriceShort
        current_close = closing_prices[time]
        gain_since_open = current_close / starting_price_ratio
        print(
            f"if closed after {time} treading hours, position #{i} would have closed at gain of: {round(gain_since_open, 2)} instead closed at {round(closing_price_ratio, 2)}")


def atr_stop_loss(portfolio, closing_positions_df, high_positions_df, low_positions_df, thresh):
    for i in range(len(closing_positions_df)):
        position = portfolio[i]
        closing_prices = closing_positions_df.iloc[i].tolist()
        high_prices = high_positions_df.iloc[i].tolist()
        low_prices = low_positions_df.iloc[i].tolist()
        data = pd.DataFrame({'Close': closing_prices, 'High': high_prices, 'Low': low_prices})
        data = data.dropna()
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(14).sum() / 14


def std_stop_loss(portfolio, closing_positions_df, rate, deviations):
    for i in range(len(closing_positions_df)):
        position = portfolio[i]
        closing_prices = closing_positions_df.iloc[i]
        closing_prices = closing_prices.dropna()
        bollinger_up, bollinger_down = get_bollinger_bands(closing_prices, rate, deviations)
        plot_bollingers(closing_prices, bollinger_up, bollinger_down)
        exit()
        for j in range(len(closing_prices)):
            current_close = closing_prices[j]
            curr_bb_up = bollinger_up[j]
            curr_bb_down = bollinger_down[j]
            if current_close > curr_bb_up or current_close < curr_bb_down:
                print(f"shouldve closed at hour {j} at ")


def rsi_stop_loss(portfolio, closing_positions_df, period):
    for i in range(len(closing_positions_df)):
        position = portfolio[i]
        closing_prices = closing_positions_df.iloc[i]
        closing_prices = closing_prices.dropna()
        rsi = calculate_rsi(closing_prices, period)
        for j in range(len(closing_prices)):
            current_close = closing_prices[j]
            curr_rsi = rsi[j]

def calculate_rsi(prices, period):
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(gain[-period:])
    avg_loss = np.mean(loss[-period:])
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def plot_bollingers(closing_prices, bollinger_up, bollinger_down):
    plt.title(' Bollinger Bands')
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(closing_prices, label='Closing Prices')
    plt.plot(bollinger_up, label='Bollinger Up', c='g')
    plt.plot(bollinger_down, label='Bollinger Down', c='r')
    plt.legend()
    plt.show()


def get_bollinger_bands(prices, rate, deviations):
    sma = prices.rolling(rate).mean()
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * deviations  # Calculate top band
    bollinger_down = sma - std * deviations  # Calculate bottom band
    return bollinger_up, bollinger_down
