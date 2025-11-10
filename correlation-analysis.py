import yfinance as yf
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from statsmodels.tsa.stattools import coint
results = []
semiconductors = ["NVDA", "AMD", "INTC", "TSM", "AVGO", "QCOM", "ASML", "MU", "TXN", "SOXX", "SMH"]
big_tech = ["AAPL", "MSFT", "GOOG", "META", "AMZN", "NFLX", "VGT", "ARKK"]
etfs = ["SPY", "QQQ", "DIA", "IWM", "XLK", "XLF", "XLE", "XLY", "XLI", "XLP", "XLV", "XLB", "XLC", "XLRE", "EEM", "EWJ", "FXI"]
commodities_bonds = ["GLD", "SLV", "USO", "UNG", "TLT", "IEF", "HYG", "LQD", "GC=F", "SI=F", "CL=F"]
currencies_crypto = ["DXY", "EURUSD=X", "GBPUSD=X", "USDJPY=X", "BTC-USD", "ETH-USD"]
banks = ["JPM", "BAC", "C", "WFC", "GS", "MS", "PNC", "USB", "BK", "TFC", "TD", "RY", "BNS", "HSBC", "DB", "UBS", "ING", "SAN"]


groups = {
    "Semiconductors": semiconductors,
    "Big Tech": big_tech,
    "Equity ETFs & Sectors": etfs,
    "Commodities & Bonds": commodities_bonds,
    "Currencies & Crypto": currencies_crypto,
    "Banks": banks
}

all_tickers = sum(groups.values(), [])

data = yf.download(all_tickers, start="2020-01-01", end=dt.datetime.today().strftime('%Y-%m-%d'))

log_prices = np.log(data["Close"].dropna(axis=1, how='all'))
#print (log_prices)
log_returns = log_prices.diff().dropna()
corr_matrix = log_returns.corr()
for name, tickers in groups.items():
    sub_corr = log_returns[tickers].corr()
    stack = sub_corr.stack()
    filtered = stack[(stack > 0.8) & (stack < 1.0)]
    filtered.index.set_names(['Ticker 1', 'Ticker 2'], inplace=True)
    filtered = filtered.to_frame().reset_index()
    filtered.columns = ["ticker1", "ticker2", "corr"]
    filtered = filtered[filtered['ticker1'] < filtered['ticker2']]
    #print(filtered)
    #plt.figure(figsize=(8, 6))
    #sns.heatmap(sub_corr, annot=False, cmap="coolwarm", linewidth=0.5)
    #plt.title(f"{name} - Correlation of Log Returns")
    #plt.tight_layout()
    #plt.show()

    for i, row in filtered.iterrows():
        t1 = row['ticker1']
        t2 = row['ticker2']
        s1 = log_prices[t1].dropna()
        s2 = log_prices[t2].dropna()
        combined = pd.concat([s1, s2], axis=1).dropna()
        score, pvalue, _ = coint(combined.iloc[:, 0], combined.iloc[:, 1])
        if pvalue < 0.05:
            results.append({
                "group": name,
                "ticker1": t1,
                "ticker2": t2,
                "corr": row["corr"],
                "pvalue": pvalue
            })

coint_results = pd.DataFrame(results)

print(coint_results)


