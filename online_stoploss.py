import pandas as pd
from ib_insync import IB, Stock, MarketOrder, StopOrder

POSITION_SIZE = 100  # define position size
IB_IP = '127.0.0.1'  # define ip
PORT_NUMBER = 1000  # define port
SLEEP_TIME = 10  # define sleep time between checking


def read_stock_symbols(file_name):
    data = pd.read_csv(file_name)
    stock_x = data['StockX'][0]
    stock_y = data['StockY'][0]
    return stock_x, stock_y


def main():
    # Connect to Interactive Brokers
    ib = IB()
    ib.connect(IB_IP, PORT_NUMBER, clientId=1)  # Ensure the correct IP address and port number are used

    file_name = 'stock_symbols.csv'  # Input file
    stock_x_symbol, stock_y_symbol = read_stock_symbols(file_name)
    stock_exchange = 'SMART'
    stock_currency = 'USD'
    stock_x = Stock(stock_x_symbol, stock_exchange, stock_currency)
    stock_y = Stock(stock_y_symbol, stock_exchange, stock_currency)
    stock_x_price = ib.reqMktData(stock_x, '').last
    stock_y_price = ib.reqMktData(stock_y, '').last

    initial_ratio = stock_x_price / stock_y_price
    target_ratio = initial_ratio * 0.92

    ib.placeOrder(stock_x, MarketOrder('BUY', POSITION_SIZE))
    ib.placeOrder(stock_y, MarketOrder('SELL', POSITION_SIZE))

    while True:
        stock_x_price = ib.reqMktData(stock_x, '').last
        stock_y_price = ib.reqMktData(stock_y, '').last
        current_ratio = stock_x_price / stock_y_price

        if current_ratio <= target_ratio:
            ib.placeOrder(stock_x, MarketOrder('SELL', POSITION_SIZE))
            ib.placeOrder(stock_y, MarketOrder('BUY', POSITION_SIZE))
            break

        ib.sleep(SLEEP_TIME)

    ib.disconnect()


if __name__ == "__main__":
    main()
