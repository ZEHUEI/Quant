import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#AVGO, CEG
ticker = "AVGO"
STOCK = yf.Ticker(ticker)
ticker_name = STOCK.info.get("longName", "N/A")
hist = STOCK.history(period="1y")

#daily returns
hist['Daily_Return'] = hist['Close'].pct_change()
returns = hist['Daily_Return'].dropna()

hist.index = pd.to_datetime(hist.index)

monthly_vol = hist['Volume'].resample('ME').sum()

#normal PDF (daily)
mu = returns.mean()
sigma = returns.std()

x = np.linspace(returns.min(), returns.max(), 500)
pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


#Risk
print("STD :",sigma,"Return :",mu)

#Annual
annual_vol = sigma * np.sqrt(252)
annual_ret = mu * 252
print("Annual Volitility :",annual_vol)
print("Annual Return :",annual_ret)

#Sharpe Ratio
rf = 0.03/252
sharpe = (returns.mean() - rf) / sigma
print("Daily Sharpe : ",sharpe)
print("Annual Sharpe :", sharpe * np.sqrt(252))




#plot graph
plt.figure(figsize=(10,6))
plt.hist(returns,bins=50,density=True)
plt.plot(x,pdf)
# plt.scatter(hist.index,hist['Daily_Return'],s=5)
# plt.plot(hist.index,hist['Daily_Return'])
plt.title(ticker_name)
plt.xlabel('-')
plt.ylabel('-')


plt.grid(True)
plt.tight_layout()
plt.show()