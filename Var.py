import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt
import openpyxl
from openpyxl.styles import PatternFill
from scipy.stats import norm
import logging
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calc_var(initial_investment, weights, data):
    """
    Calculate 1-day Value at Risk (VaR) using parametric method.

    Args:
        initial_investment: Portfolio value
        weights: Array of position weights
        data: Historical price data (pandas Series or DataFrame)

    Returns:
        VaR at 95% confidence level (5% confidence level for loss)
    """
    try:
        returns = data.pct_change()
        cov_matrix = returns.cov()
        avg_rets = returns.mean()
        port_mean = avg_rets.dot(weights)
        port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
        mean_investment = (1 + port_mean) * initial_investment
        stdev_investment = initial_investment * port_stdev

        # 95% confidence level (5% tail risk)
        confidence_level = 0.05
        cutoff = norm.ppf(confidence_level, mean_investment, stdev_investment)
        var_1d = initial_investment - cutoff

        return var_1d
    except Exception as e:
        logger.error(f"Error calculating VaR: {e}")
        raise


def add_var_to_alltickers(path, initial_inv, weights, start_date):
    """
    Calculate VaR for all tickers in the master list and save to Excel.

    Args:
        path: Path to alltickers Excel file
        initial_inv: Initial investment amount
        weights: Portfolio weights array
        start_date: Start date for historical data
    """
    try:
        logger.info(f"Loading tickers from {path}")
        df = pd.read_excel(path)
        df['Var'] = 0
        df['Qual'] = 0
        tickers = df['Symbol'].tolist()
        bad_tickers = []

        for index, ticker in enumerate(tickers):
            try:
                logger.info(f"Processing {index + 1}/{len(tickers)}: {ticker}")
                data = pdr.get_data_yahoo([ticker], start=start_date, end=dt.date.today())['Close']
                df.at[index, 'Var'] = calc_var(initial_inv, weights, data)
            except Exception as e:
                logger.warning(f"Failed to calculate VaR for {ticker}: {e}")
                bad_tickers.append(ticker)

        if bad_tickers:
            logger.warning(f"Failed tickers: {bad_tickers}")

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.sort_values(by='Var')
        df.to_excel(path, index=False)
        logger.info(f"VaR data saved to {path}")

    except Exception as e:
        logger.error(f"Error in add_var_to_alltickers: {e}")
        raise


if __name__ == '__main__':
    add_var_to_alltickers(
        config.ALL_TICKERS_PATH,
        config.INITIAL_INVESTMENT,
        np.array(config.WEIGHTS),
        config.START_DATE_FOR_VAR
    )
