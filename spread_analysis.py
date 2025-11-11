import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import statsmodels.api as sm

ticker1 = "GS"
ticker2 = "WFC"

start_date = "2021-01-01"
end_date = dt.datetime.today().strftime('%Y-%m-%d')

data1 = yf.download(ticker1, start=start_date, end=end_date, interval="1wk")
log_prices1 = np.log(data1["Close"].dropna(axis=1, how='all'))

data2 = yf.download(ticker2, start=start_date, end=end_date, interval="1wk")
log_prices2 = np.log(data2["Close"].dropna(axis=1, how='all'))

combined = pd.concat([log_prices1, log_prices2], axis=1).dropna()
combined.columns = [ticker1, ticker2]

X = sm.add_constant(combined[ticker2])
model = sm.OLS(combined[ticker1], X).fit()
beta = model.params[ticker2]

spread = combined[ticker1] - beta * combined[ticker2]
zscore = (spread - spread.mean()) / spread.std()



fig, axes = plt.subplots(1,2,figsize=(14, 10))
axes[0].plot(zscore.index, zscore, label='Spread')
axes[0].axhline(zscore.mean(), color='red', linestyle='--', label='Mean')
axes[0].set_title(f"Z-score standardised spread between {ticker1} and {ticker2}")
axes[0].set_ylabel("S.Ds from Mean")
axes[0].legend()
axes[1].plot(combined.index, combined[ticker1], label=ticker1)
axes[1].plot(combined.index, combined[ticker2], label=ticker2)
axes[1].set_title(f"Log Prices of {ticker1} and {ticker2}")
axes[1].set_ylabel("Log Price")
axes[1].legend()
plt.tight_layout()
plt.show()



