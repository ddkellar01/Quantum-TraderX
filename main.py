import asyncio
import logging
import sys

# Import your custom modules (mapping to the file structure previously defined)
import config
from connectors import CoinbaseConnector, AlpacaConnector, OandaConnector
from async_engine import StreamOrchestrator

# Configure standard logging for terminal output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("TradingCore")

async def main():
    logger.info("Booting Trading Core...")

    # 1. Load environment variables (.env) securely
    config.load_keys()
    
    # 2. Initialize the API connectors
    # These classes (defined in connectors.py) should handle their own auth headers
    logger.info("Initializing market connectors...")
    coinbase = CoinbaseConnector()
    alpaca = AlpacaConnector()
    oanda = OandaConnector()

    # 3. Verify initial REST API connectivity (Check balances, buying power, etc.)
    try:
        logger.info("Verifying REST connections...")
        await asyncio.gather(
            coinbase.verify_connection(),
            alpaca.verify_connection(),
            oanda.verify_connection()
        )
        logger.info("REST verification complete. All systems online.")
    except Exception as e:
        logger.error(f"Failed to connect to one or more markets: {e}")
        sys.exit(1)

    # 4. Initialize the asynchronous orchestrator
    # This class (defined in async_engine.py) manages the WebSocket event loops
    orchestrator = StreamOrchestrator(
        connectors=[coinbase, alpaca, oanda]
    )

    # 5. Execute the concurrent data streams
    try:
        logger.info("Starting live market WebSocket streams...")
        # Await the main task runner which keeps the connections alive
        await orchestrator.start_streams()
        
    except asyncio.CancelledError:
        logger.warning("Stream execution cancelled.")
    finally:
        # Gracefully close WebSockets and aiohttp client sessions on shutdown
        logger.info("Initiating graceful shutdown...")
        await orchestrator.close_connections()
        logger.info("Trading Core offline.")

if __name__ == "__main__":
    # Standard Python async entry point with KeyboardInterrupt handling for the terminal
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process forcefully terminated by user (Ctrl+C).")
