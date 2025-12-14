"""
Configuration management for VarProject.
Loads settings from environment variables with fallback defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found in environment variables. "
        "Please copy .env.example to .env and configure your credentials."
    )

# Interactive Brokers Configuration
IB_IP = os.getenv('IB_IP', '127.0.0.1')
IB_PORT = int(os.getenv('IB_PORT', '7497'))
IB_CLIENT_ID = int(os.getenv('IB_CLIENT_ID', '1'))

# Portfolio Configuration
INITIAL_INVESTMENT = float(os.getenv('INITIAL_INVESTMENT', '1000000'))
NET_LIQUIDITY = float(os.getenv('NET_LIQUIDITY', '294000'))

# Risk Thresholds
SECTOR_PERCENTAGE_LIMIT = float(os.getenv('SECTOR_PERCENTAGE_LIMIT', '0.2'))
MAX_POSITION_PERCENTAGE = float(os.getenv('MAX_POSITION_PERCENTAGE', '0.05'))
MAX_PORTFOLIO_SIZE = int(os.getenv('MAX_PORTFOLIO_SIZE', '20'))
MAX_PORTFOLIO_EXPOSURE = float(os.getenv('MAX_PORTFOLIO_EXPOSURE', '1.3'))
ALLOWED_BAD_POSITIONS = int(os.getenv('ALLOWED_BAD_POSITIONS', '0'))
ALLOWED_RATIO_GOOD_TO_TOTAL = float(os.getenv('ALLOWED_RATIO_GOOD_TO_TOTAL', '0.4'))

# Pairs Trading Configuration
POSITION_SIZE = int(os.getenv('POSITION_SIZE', '100'))
SLEEP_TIME = int(os.getenv('SLEEP_TIME', '10'))
TARGET_RATIO_MULTIPLIER = float(os.getenv('TARGET_RATIO_MULTIPLIER', '0.92'))

# File Paths
DATA_DIR = BASE_DIR / 'data'
ALL_TICKERS_PATH = os.getenv('ALL_TICKERS_PATH', str(DATA_DIR / 'alltickers.xlsx'))
PORTFOLIO_PATH_ORIGINAL = os.getenv('PORTFOLIO_PATH_ORIGINAL', str(DATA_DIR / 'actualportfolio.csv'))
PORTFOLIO_PATH_TRANSFORMED = os.getenv('PORTFOLIO_PATH_TRANSFORMED', str(DATA_DIR / 'actualportfolio.xlsx'))
FINISHED_PORTFOLIO_PATH = os.getenv('FINISHED_PORTFOLIO_PATH', str(DATA_DIR / 'finished.xlsx'))
PAIRS_POSITIONS_PATH = os.getenv('PAIRS_POSITIONS_PATH', str(DATA_DIR / 'pairsPositions.xlsx'))

# Data Configuration
START_DATE_FOR_VAR = os.getenv('START_DATE_FOR_VAR', '2018-01-01')

# VaR Configuration
WEIGHTS = [1]  # Can be extended for multi-asset portfolios
CONFIDENCE_LEVEL = 0.95
