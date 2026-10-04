import os
from alpaca.trading.client import TradingClient

alpaca_api = os.getenv("ALPACA_API_KEY")
alpaca_secret = os.getenv("ALPACA_SECRET_KEY")

# Initialize client (set paper=True to route to the sandbox environment)
trading_client = TradingClient(alpaca_api, alpaca_secret, paper=True)

# Fetch account buying power and equity status
account = trading_client.get_account()
print(f"Buying Power: {account.buying_power}")
