import requests
import os

oanda_token = os.getenv("OANDA_API_TOKEN")
headers = {
    "Authorization": f"Bearer {oanda_token}",
    "Accept-Datetime-Format": "RFC3339"
}

# Fetch EUR/USD pricing
response = requests.get(
    "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles",
    headers=headers
)
