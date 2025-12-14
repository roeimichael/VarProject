import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
import seaborn as sns
import logging
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_sectors(df):
    """Check if any sector exceeds concentration limit."""
    sector_sum = df.groupby(['Sector']).sum()
    violations = []
    for index, row in sector_sum.iterrows():
        if row['Protfilio Precentage'] > config.SECTOR_PERCENTAGE_LIMIT:
            msg = f"{index} has too many open positions with {row['Protfilio Precentage']:.2%}"
            logger.warning(msg)
            violations.append(msg)
    return violations


def check_percentage(df):
    """Check if any individual position exceeds size limit."""
    violations = []
    for index, row in df.iterrows():
        if row['Protfilio Precentage'] > config.MAX_POSITION_PERCENTAGE:
            msg = f"position of ticker {row['Symbol']} is too big with size of {row['Protfilio Precentage']:.2%}"
            logger.warning(msg)
            violations.append(msg)
    return violations


def check_amount(df):
    """Check if total number of positions exceeds limit."""
    positions = df.groupby(['Symbol']).count().sum()['Position']
    if positions > config.MAX_PORTFOLIO_SIZE:
        msg = f"too many positions in portfolio current amount: {positions}"
        logger.warning(msg)
        return [msg]
    return []


def check_pos_size(df):
    """Check if total portfolio exposure exceeds limit (liquidation risk)."""
    total_exposure = df['Protfilio Precentage'].sum()
    if total_exposure > config.MAX_PORTFOLIO_EXPOSURE:
        msg = f"portfolio isn't balanced, risk of liquidation approaching {round(total_exposure, 2)}"
        logger.warning(msg)
        return [msg]
    return []


def check_var_quality(df):
    """Check if portfolio has too many low-quality (high VaR) positions."""
    violations = []
    try:
        qualities = df.groupby(['Qual']).count()
        mid = qualities['Symbol'].get('MID', 0)
        good = qualities['Symbol'].get('GOOD', 0)
        bad = qualities['Symbol'].get('BAD', 0)
        total = mid + good

        if bad > config.ALLOWED_BAD_POSITIONS:
            msg = "there are stocks with bad quality VAR in portfolio"
            logger.warning(msg)
            violations.append(msg)

        if total > 0 and good / total < config.ALLOWED_RATIO_GOOD_TO_TOTAL:
            msg = "under 40% of stocks are good and more than 60% are mid"
            logger.warning(msg)
            violations.append(msg)
    except Exception as e:
        logger.error(f"Error checking VaR quality: {e}")

    return violations


def get_corr_mat(df, output_file='corr_mat.png'):
    """
    Generate correlation matrix heatmap for portfolio holdings.

    Args:
        df: Portfolio dataframe with 'Symbol' column
        output_file: Path to save the correlation matrix image
    """
    try:
        logger.info("Fetching price data for correlation analysis...")
        data = pdr.get_data_yahoo(df['Symbol'], start="2022-01-01", end=dt.date.today())['Close']
        corr = data.corr()

        # Create mask for upper triangle
        mask = np.zeros_like(corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

        # Create heatmap
        f, ax = plt.subplots(figsize=(20, 20))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(
            corr, mask=mask, cmap=cmap, annot=True,
            vmax=.3, vmin=-.3, center=0, square=True,
            linewidths=.5, cbar_kws={"shrink": .5}
        )
        f.savefig(output_file)
        logger.info(f"Correlation matrix saved to {output_file}")
        plt.close(f)

    except Exception as e:
        logger.error(f"Error generating correlation matrix: {e}")
        raise


if __name__ == '__main__':
    try:
        logger.info("Running portfolio extremity checks...")
        df = pd.read_excel(config.PORTFOLIO_PATH_TRANSFORMED)

        # Run all checks
        check_sectors(df)
        check_percentage(df)
        check_amount(df)
        check_pos_size(df)
        check_var_quality(df)
        get_corr_mat(df)

        logger.info("Portfolio extremity checks completed")
        logger.info(f"\n{df}")

    except Exception as e:
        logger.error(f"Error running extremity checks: {e}", exc_info=True)
        raise
