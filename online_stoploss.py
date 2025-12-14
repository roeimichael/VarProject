import pandas as pd
from ib_insync import IB, Stock, MarketOrder, StopOrder
import logging
import time
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_stock_symbols(file_name):
    """Read stock pair symbols from CSV file."""
    try:
        data = pd.read_csv(file_name)
        stock_x = data['StockX'][0]
        stock_y = data['StockY'][0]
        logger.info(f"Loaded stock pair: {stock_x} / {stock_y}")
        return stock_x, stock_y
    except FileNotFoundError:
        logger.error(f"Stock symbols file not found: {file_name}")
        raise
    except KeyError as e:
        logger.error(f"Required column not found in {file_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading stock symbols: {e}")
        raise


def main():
    """
    Execute pairs trading strategy with automatic stop-loss.
    Enters long/short pair and exits when ratio converges by 8%.
    """
    ib = None
    try:
        # Connect to Interactive Brokers
        logger.info(f"Connecting to Interactive Brokers at {config.IB_IP}:{config.IB_PORT}")
        ib = IB()
        ib.connect(config.IB_IP, config.IB_PORT, clientId=config.IB_CLIENT_ID)
        logger.info("Connected to Interactive Brokers")

        # Read stock pair symbols
        file_name = 'stock_symbols.csv'
        stock_x_symbol, stock_y_symbol = read_stock_symbols(file_name)

        # Create stock contracts
        stock_exchange = 'SMART'
        stock_currency = 'USD'
        stock_x = Stock(stock_x_symbol, stock_exchange, stock_currency)
        stock_y = Stock(stock_y_symbol, stock_exchange, stock_currency)

        # Get initial prices
        logger.info("Requesting market data...")
        ticker_x = ib.reqMktData(stock_x, '')
        ticker_y = ib.reqMktData(stock_y, '')
        ib.sleep(2)  # Wait for market data to populate

        stock_x_price = ticker_x.last
        stock_y_price = ticker_y.last

        if not stock_x_price or not stock_y_price:
            raise ValueError("Failed to get market prices for stocks")

        # Calculate entry and exit ratios
        initial_ratio = stock_x_price / stock_y_price
        target_ratio = initial_ratio * config.TARGET_RATIO_MULTIPLIER
        logger.info(f"Initial ratio: {initial_ratio:.4f}, Target ratio: {target_ratio:.4f}")
        logger.info(f"Entry prices: {stock_x_symbol}=${stock_x_price:.2f}, {stock_y_symbol}=${stock_y_price:.2f}")

        # Enter pairs trade
        logger.info(f"Placing entry orders: BUY {config.POSITION_SIZE} {stock_x_symbol}, SELL {config.POSITION_SIZE} {stock_y_symbol}")
        order_x = ib.placeOrder(stock_x, MarketOrder('BUY', config.POSITION_SIZE))
        order_y = ib.placeOrder(stock_y, MarketOrder('SELL', config.POSITION_SIZE))
        ib.sleep(2)  # Wait for orders to fill

        logger.info("Position entered. Monitoring for exit signal...")

        # Monitor position for exit signal
        iteration = 0
        max_iterations = 1000  # Safety limit to prevent infinite loop
        while iteration < max_iterations:
            # Get current prices
            stock_x_price = ticker_x.last
            stock_y_price = ticker_y.last

            if stock_x_price and stock_y_price:
                current_ratio = stock_x_price / stock_y_price
                logger.info(f"Current ratio: {current_ratio:.4f} (target: {target_ratio:.4f})")

                # Check exit condition
                if current_ratio <= target_ratio:
                    logger.info("Exit signal triggered! Closing position...")
                    ib.placeOrder(stock_x, MarketOrder('SELL', config.POSITION_SIZE))
                    ib.placeOrder(stock_y, MarketOrder('BUY', config.POSITION_SIZE))
                    logger.info("Position closed successfully")
                    break
            else:
                logger.warning("Failed to get current prices, retrying...")

            ib.sleep(config.SLEEP_TIME)
            iteration += 1

        if iteration >= max_iterations:
            logger.warning("Maximum iterations reached. Consider manual intervention.")

    except ConnectionRefusedError:
        logger.error(f"Could not connect to IB at {config.IB_IP}:{config.IB_PORT}. Is TWS/Gateway running?")
        raise
    except Exception as e:
        logger.error(f"Error in pairs trading execution: {e}", exc_info=True)
        raise
    finally:
        if ib and ib.isConnected():
            logger.info("Disconnecting from Interactive Brokers")
            ib.disconnect()


if __name__ == "__main__":
    main()
