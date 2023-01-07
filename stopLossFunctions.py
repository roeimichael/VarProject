import pandas as pd
from pprint import pprint


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
            if gain_since_open < percentage:
                print(f"should have closed at price: {round(current_close, 2)} instead closed at {round(closing_price_ratio, 2)}")
                break
