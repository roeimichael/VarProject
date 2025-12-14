import telebot
import yfinance as yf
import extremities
import pandas as pd
import logging
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot with token from config
bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['Run'])
def check_sectors(message):
    """Execute comprehensive portfolio risk checks and send alerts via Telegram."""
    try:
        logger.info("Starting portfolio risk check")
        df = pd.read_excel(config.FINISHED_PORTFOLIO_PATH)

        alert_message = ""

        # Check sector concentration
        sector_sum = df.groupby(['Sector']).sum()
        for index, row in sector_sum.iterrows():
            if row['Protfilio Precentage'] > config.SECTOR_PERCENTAGE_LIMIT:
                alert_message += f"|  {index} has too many open positions with {row['Protfilio Precentage']:.2%}  |\n"
        alert_message += "-----------------------------------------\n"

        # Check individual position sizes
        for index, row in df.iterrows():
            if row['Protfilio Precentage'] > config.MAX_POSITION_PERCENTAGE:
                alert_message += f"|  position of ticker {row['Symbol'].upper()} is too big with size of {row['Protfilio Precentage']:.2%}  |\n"
        alert_message += "-----------------------------------------\n"

        # Check total number of positions
        positions = df.groupby(['Symbol']).count().sum()['Position']
        if positions > config.MAX_PORTFOLIO_SIZE:
            alert_message += f"|  too many positions in portfolio current amount: {positions}  |\n"
        alert_message += "-----------------------------------------\n"

        # Check portfolio exposure (liquidation risk)
        total_exposure = df['Protfilio Precentage'].sum()
        if total_exposure > config.MAX_PORTFOLIO_EXPOSURE:
            alert_message += f"|  portfolio isn't balanced, risk of liquidation approaching {round(total_exposure, 2)}  |\n"
        alert_message += "-----------------------------------------\n"

        # Check quality distribution
        qualities = df.groupby(['Qual']).count()
        mid = qualities['Symbol'].get('MID', 0)
        good = qualities['Symbol'].get('GOOD', 0)
        bad = qualities['Symbol'].get('BAD', 0)
        total = mid + good

        if bad > config.ALLOWED_BAD_POSITIONS:
            alert_message += "there are stocks with bad quality VAR in portfolio\n"
        if total > 0 and good / total < config.ALLOWED_RATIO_GOOD_TO_TOTAL:
            alert_message += "under 40% of stocks are good and more than 60% are mid\n"

        # Send alert or all-clear message
        if alert_message.strip() == "-----------------------------------------\n" * 4:
            alert_message = "✅ All portfolio risk checks passed!"

        bot.reply_to(message, alert_message)
        logger.info("Portfolio risk check completed successfully")

    except FileNotFoundError as e:
        error_msg = f"Error: Portfolio file not found. Please run main.py first."
        logger.error(f"File not found: {e}")
        bot.reply_to(message, error_msg)
    except KeyError as e:
        error_msg = f"Error: Expected column not found in portfolio data: {e}"
        logger.error(f"KeyError in portfolio data: {e}")
        bot.reply_to(message, error_msg)
    except Exception as e:
        error_msg = f"Error running portfolio checks: {str(e)}"
        logger.error(f"Unexpected error: {e}", exc_info=True)
        bot.reply_to(message, error_msg)


if __name__ == '__main__':
    logger.info("Starting Telegram bot...")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
