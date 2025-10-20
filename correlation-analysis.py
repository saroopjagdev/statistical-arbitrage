import yfinance as yf
import numpy as np
tickers = ["NVDA", "AMD"]
data = yf.download(tickers, start="2022-01-01", end="2025-01-01")
data["log_prices"] = data["Adj Close"].apply(lambda x: np.log(x))
