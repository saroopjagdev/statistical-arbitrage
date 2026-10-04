# statistical-arbitrage

Screens for pairs-trading candidates. `correlation-analysis.py` downloads daily prices (from 2020) for groups of semiconductors, big tech, equity ETFs/sectors, commodities and bonds, FX/crypto and banks. Within each group it keeps pairs whose log-return correlation exceeds 0.8, then runs an Engle-Granger cointegration test (`statsmodels.coint`) and keeps pairs with p < 0.05.

## Run
```
pip install yfinance numpy pandas statsmodels matplotlib seaborn
python correlation-analysis.py
```
Edit the ticker lists at the top to change the universe. Cointegration found in-sample does not guarantee a tradable spread.
