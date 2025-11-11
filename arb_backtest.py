import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

ticker1 = "RY"
ticker2 = "WFC"

start_date = "2000-01-01"
end_date = dt.datetime.today().strftime('%Y-%m-%d')

data1 = yf.download(ticker1, start=start_date, end=end_date, interval="1wk")
log_prices1 = np.log(data1["Close"].dropna(axis=1, how='all'))

data2 = yf.download(ticker2, start=start_date, end=end_date, interval="1wk")
log_prices2 = np.log(data2["Close"].dropna(axis=1, how='all'))

combined = pd.concat([log_prices1, log_prices2], axis=1).dropna()
combined.columns = [ticker1, ticker2]

combined.plot(figsize=(10,6))
plt.title(f"Log Prices of {ticker1} and {ticker2}")
plt.xlabel("Date")
plt.ylabel("Log Price")
plt.show()

