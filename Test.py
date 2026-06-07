import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

"""
CHANGE THIS ONLY (STOCK NAME): NVDA, NOW, GOOG, AMD, META, CGNX
"""
ticker = "CRWV"

BASE_FOLDER = "./Folder"

SAVE_FOLDER = os.path.join(BASE_FOLDER,ticker)
os.makedirs(SAVE_FOLDER,exist_ok=True)

STOCK = yf.Ticker(ticker)
ticker_name = STOCK.info.get("longName", "N/A")
hist = STOCK.history(period="max")

#daily returns
hist['Daily_Return'] = hist['Close'].pct_change()
returns = hist['Daily_Return'].dropna()

hist.index = pd.to_datetime(hist.index)

monthly_vol = hist['Volume'].resample('ME').sum()

# Calculate a 20-day Moving Average
hist['MA20'] = hist['Close'].rolling(window=20).mean()

# Calculate a 52-week Moving Average
hist['MA252'] = hist['Close'].rolling(window=252).mean()

#P/E ratio
pe_ratio = STOCK.info.get("trailingPE", "N/A")

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
annual_sharpe = sharpe * np.sqrt(252)

print("\n----- Metrics -----")
print(f"P/E Ratio: {pe_ratio}")
print(f"Annual Return: {annual_ret:.2%}")
print(f"Annual Volatility: {annual_vol:.2%}")
print(f"Annual Sharpe Ratio: {annual_sharpe:.2f}")




#plot graph
plt.figure(figsize=(12,6))

plt.plot(hist.index,hist['Close'],label='close price',color='royalblue',linewidth=1.5)
plt.plot(hist.index, hist['MA20'], label='20-Day Moving Average', color='orange', linestyle='--')
plt.plot(hist.index, hist['MA252'], label='52-Week Moving Average', color='red',linewidth=2)

plt.title(ticker_name)
plt.xlabel('Date')
plt.ylabel('Price $')

plt.grid(True)
plt.legend()
plt.tight_layout()

chart_path = os.path.join(SAVE_FOLDER, "price_chart.png")
stats_path = os.path.join(SAVE_FOLDER, "stats.txt")
csv_path = os.path.join(SAVE_FOLDER, "history.csv")

plt.savefig(chart_path, dpi=300, bbox_inches='tight')

plt.show()
plt.close()

# Save stats
with open(stats_path, "w") as f:
    f.write(f"Ticker: {ticker}\n")
    f.write(f"Company: {ticker_name}\n\n")
    f.write(f"Daily Return Mean: {mu:.6f}\n")
    f.write(f"Daily Volatility (STD): {sigma:.6f}\n")
    f.write(f"Annual Return: {annual_ret:.6f}\n")
    f.write(f"Annual Volatility: {annual_vol:.6f}\n")
    f.write(f"Daily Sharpe Ratio: {sharpe:.6f}\n")
    f.write(f"Annual Sharpe Ratio: {sharpe * np.sqrt(252):.6f}\n")

# Save historical data
hist.to_csv(csv_path)
print(f"Saved files to {SAVE_FOLDER}")