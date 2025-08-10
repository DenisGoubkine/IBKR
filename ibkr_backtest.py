from __future__ import annotations

"""Simple example for connecting to IBKR TWS and running a moving average backtest."""

from dataclasses import dataclass
from typing import List

import pandas as pd
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


@dataclass
class BarData:
    """Container for historical bar data."""

    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class IBKRApp(EWrapper, EClient):
    """IBKR client application for fetching historical data."""

    def __init__(self) -> None:
        EClient.__init__(self, self)
        self.data: List[BarData] = []

    def historicalData(self, reqId, bar):  # type: ignore[override]
        self.data.append(
            BarData(bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume)
        )

    def historicalDataEnd(self, reqId, start, end):  # type: ignore[override]
        super().historicalDataEnd(reqId, start, end)
        self.disconnect()


def fetch_historical_data(
    symbol: str = "AAPL", duration: str = "1 M", bar_size: str = "1 day"
) -> pd.DataFrame:
    """Fetch historical data for a stock symbol using IBKR's API."""

    app = IBKRApp()
    app.connect("127.0.0.1", 7497, clientId=1)

    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app.reqHistoricalData(1, contract, "", duration, bar_size, "TRADES", 1, 1, False, [])
    app.run()

    df = pd.DataFrame([bar.__dict__ for bar in app.data])
    return df


def moving_average_backtest(
    df: pd.DataFrame, short_window: int = 10, long_window: int = 20
) -> pd.DataFrame:
    """Run a simple moving average crossover backtest."""

    df = df.copy()
    df["sma_short"] = df["close"].rolling(window=short_window).mean()
    df["sma_long"] = df["close"].rolling(window=long_window).mean()
    df["position"] = 0
    df.loc[df["sma_short"] > df["sma_long"], "position"] = 1
    df["signal"] = df["position"].diff().fillna(0)
    return df


if __name__ == "__main__":
    data = fetch_historical_data()
    if data.empty:
        print("No data retrieved. Ensure TWS is running and accessible.")
    else:
        results = moving_average_backtest(data)
        print(results.tail())
