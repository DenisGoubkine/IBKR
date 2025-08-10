# IBKR

Example project demonstrating how to fetch historical data from the IBKR TWS API and run a very basic moving average backtest.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure that Trader Workstation or IB Gateway is running and accessible on `127.0.0.1:7497`.

3. Run the example script:

```bash
python ibkr_backtest.py
```

The script will request historical data for AAPL and print the tail of the backtest results.
