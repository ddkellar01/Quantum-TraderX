import os
from coinbase.rest import RESTClient
from coinbase.websocket import WSClient

api_key = os.getenv("COINBASE_API_KEY")
api_secret = os.getenv("COINBASE_API_SECRET")

# REST for order execution
rest_client = RESTClient(api_key=api_key, api_secret=api_secret)
accounts = rest_client.get_accounts()

# WebSocket for real-time market data
def on_message(msg):
    print("Market Data Update:", msg)

# Connect to the WebSocket API (max_size limits payload parsing)
ws_client = WSClient(api_key=api_key, api_secret=api_secret, on_message=on_message, max_size=65536)
ws_client.open()
ws_client.subscribe(product_ids=["BTC-USD"], channels=["ticker"])
