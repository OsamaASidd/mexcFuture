# MEXC Futures Trading Bot

Automated trading bot for MEXC futures using Selenium WebDriver with Chrome profile support.

## Features

- Open MEXC perpetual futures positions
- Support for LONG and SHORT positions
- Automatic Stop Loss (35%) and Take Profit (50%) settings
- Chrome profile integration for saved login sessions
- Modular architecture for easy extension
- Comprehensive logging

## Installation

1. Install Python 3.8+

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Chrome profile path in `src/config.py`:
```python
CHROME_PROFILE_PATH = r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Default"  # or your profile name
```

## Usage

Run the bot:
```bash
python main.py
```

Input format:
```
{SYMBOL, TYPE, AMOUNT}
```

Example:
```
{SOLUSDT, LONG, 10}   # Open $10 LONG on SOL/USDT
{BTCUSDT, SHORT, 50}  # Open $50 SHORT on BTC/USDT
```

## Configuration

Edit `src/config.py` to customize:
- Chrome profile settings
- Default stop loss percentage (35%)
- Default take profit percentage (50%)
- Wait timeouts

## Project Structure

```
mexcFuture/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── src/
│   ├── config.py             # Configuration settings
│   └── modules/
│       ├── browser_manager.py # Selenium browser management
│       └── mexc_trader.py    # MEXC trading operations
└── logs/
    └── trading.log           # Trading logs
```

## Important Notes

1. **Login Required**: Make sure you're logged into MEXC in your Chrome profile before running the bot
2. **Test Mode**: The bot asks for confirmation before executing trades
3. **Risk Warning**: Trading futures involves significant risk. Use at your own discretion

## Troubleshooting

- If Chrome doesn't open with your profile, verify the profile path in config.py
- Check logs/trading.log for detailed error messages
- Ensure you have Chrome installed and updated

## Disclaimer

This bot is for educational purposes. Trading cryptocurrencies involves substantial risk of loss.