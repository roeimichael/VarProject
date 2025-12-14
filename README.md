# Portfolio Risk Management System

A sophisticated portfolio risk management and analysis system for active traders, featuring Value at Risk (VaR) calculations, real-time monitoring via Telegram, and automated pairs trading strategies.

## Features

### Core Functionality
- **Value at Risk (VaR) Calculation**: Parametric VaR calculation at 95% confidence level using historical data
- **Portfolio Risk Monitoring**: Real-time alerts for sector concentration, position sizing, and exposure limits
- **Pairs Trading**: Automated entry/exit for pairs trading strategies with ratio-based stop-loss
- **Risk Assessment**: Quality ratings (GOOD/MID/BAD) based on VaR percentiles
- **Correlation Analysis**: Portfolio diversification visualization through correlation matrices

### Risk Controls
- Sector concentration limits (default: 20% max per sector)
- Individual position size limits (default: 5% max per position)
- Maximum portfolio size (default: 20 positions)
- Portfolio exposure limits (default: 130% of net liquidity)
- Quality-based position filtering

### Integrations
- **Interactive Brokers**: Live trading via TWS/Gateway
- **Telegram Bot**: Real-time portfolio alerts and monitoring
- **Yahoo Finance**: Historical price data and sector information

## Technology Stack

- **Python 3.8+**
- **Data Analysis**: pandas, numpy, scipy
- **Visualization**: matplotlib, seaborn
- **Trading**: ib-insync (Interactive Brokers API)
- **Messaging**: pyTelegramBotAPI
- **Financial Data**: yfinance, pandas-datareader

## Installation

### Prerequisites
- Python 3.8 or higher
- Interactive Brokers TWS or Gateway (for live trading)
- Telegram account (for alerts)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd VarProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` with your credentials:
```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Optional (defaults provided)
NET_LIQUIDITY=294000
INITIAL_INVESTMENT=1000000
```

See `.env.example` for all available configuration options.

## Usage

### Portfolio Analysis

Transform and analyze your portfolio from broker CSV export:

```bash
python main.py
```

This will:
1. Transform raw portfolio CSV to standardized format
2. Fetch sector information for each position
3. Calculate VaR for all holdings
4. Add color-coded quality ratings
5. Generate Excel output with risk metrics

### Telegram Bot Monitoring

Start the Telegram bot for real-time alerts:

```bash
python TelegramBot.py
```

Available commands:
- `/Run` - Execute comprehensive portfolio risk checks

The bot will alert you if any of the following conditions are met:
- Sector concentration exceeds 20%
- Individual position exceeds 5%
- Total positions exceed 20
- Portfolio exposure exceeds 130%
- Too many low-quality (high VaR) positions

### Pairs Trading

Execute automated pairs trading strategy:

```bash
python online_stoploss.py
```

Requirements:
- Create `stock_symbols.csv` with columns `StockX` and `StockY`
- Interactive Brokers TWS/Gateway must be running
- Sufficient margin for short positions

The script will:
1. Enter long/short pair at market prices
2. Monitor price ratio continuously
3. Exit when ratio converges by 8% (configurable)
4. Log all actions and price updates

### Risk Analysis

Run standalone risk checks and generate correlation matrix:

```bash
python extremities.py
```

### VaR Calculation

Calculate VaR for all tickers in your master list:

```bash
python Var.py
```

## Project Structure

```
VarProject/
├── config.py              # Configuration management
├── main.py                # Main portfolio processing workflow
├── Var.py                 # VaR calculation engine
├── TelegramBot.py         # Telegram bot for alerts
├── online_stoploss.py     # Live pairs trading with IB
├── extremities.py         # Risk checks and correlation analysis
├── stopLossFunctions.py   # Various stop-loss strategies
├── stopLossPairs.py       # Pairs trading backtesting
├── data/                  # Portfolio data (not tracked in git)
│   ├── actualportfolio.csv     # Raw broker export
│   ├── actualportfolio.xlsx    # Transformed portfolio
│   ├── alltickers.xlsx         # Master ticker list with VaR
│   └── finished.xlsx           # Final analysis output
├── TradingView_lists/     # Watchlists and sector lists
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Configuration

All configuration is managed through environment variables in `.env`:

### Portfolio Settings
- `INITIAL_INVESTMENT`: Portfolio value for VaR calculation (default: 1,000,000)
- `NET_LIQUIDITY`: Net liquidation value (default: 294,000)

### Risk Thresholds
- `SECTOR_PERCENTAGE_LIMIT`: Max sector concentration (default: 0.2)
- `MAX_POSITION_PERCENTAGE`: Max individual position size (default: 0.05)
- `MAX_PORTFOLIO_SIZE`: Max number of positions (default: 20)
- `MAX_PORTFOLIO_EXPOSURE`: Max total exposure (default: 1.3)

### Trading Parameters
- `POSITION_SIZE`: Pairs trading position size (default: 100 shares)
- `TARGET_RATIO_MULTIPLIER`: Exit ratio threshold (default: 0.92 = 8% convergence)
- `SLEEP_TIME`: Monitoring interval in seconds (default: 10)

### Interactive Brokers
- `IB_IP`: IB Gateway IP (default: 127.0.0.1)
- `IB_PORT`: IB Gateway port (default: 7497 for paper, 7496 for live)
- `IB_CLIENT_ID`: Client ID for IB connection (default: 1)

## Data Files

The system expects the following data structure:

1. **actualportfolio.csv**: Export from your broker with columns:
   - Financial Instrument, Position, Avg Price, Market Value, etc.

2. **alltickers.xlsx**: Master list of tickers with pre-calculated VaR
   - Columns: Symbol, Var, Qual

3. **stock_symbols.csv** (for pairs trading):
   - Columns: StockX, StockY

Data files are excluded from git by default to protect privacy.

## Security Notes

- Never commit `.env` file or any files containing credentials
- `.gitignore` is configured to exclude sensitive data files
- All credentials should be managed through environment variables
- Consider using paper trading account for testing

## Logging

All modules use Python's logging module for comprehensive logging:
- INFO: Normal operations and status updates
- WARNING: Risk violations and failed data fetches
- ERROR: Critical failures and exceptions

Logs include timestamps and detailed error traces for debugging.

## Contributing

When contributing:
1. Never commit sensitive data or credentials
2. Follow existing code style and error handling patterns
3. Add logging for new operations
4. Update configuration in config.py for new settings
5. Test with paper trading account first

## Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software. Always test thoroughly with paper trading before using real capital.

## License

[Add your chosen license here]

## Support

For issues, questions, or contributions, please open an issue on GitHub.
