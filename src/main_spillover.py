import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.api import VAR
import warnings

warnings.filterwarnings("ignore")


# --------------------------
# Data
# --------------------------
assets = ["CL=F", "GC=F", "EURUSD=X", "^GSPC"]

raw = yf.download(
    assets,
    start="2006-01-01",
    auto_adjust=True,
    progress=False
)

if isinstance(raw.columns, pd.MultiIndex):
    data = raw["Close"].copy()
else:
    data = raw[["Close"]].copy()

data = data.dropna()

returns = np.log(data / data.shift(1)).dropna()

names = list(returns.columns)
n = len(names)

print("Data shape:", returns.shape)


# --------------------------
# Settings
# --------------------------
window = 200
maxlags = 5

spill_list = []
net_list = []
dates = []


# --------------------------
# Rolling estimation
# --------------------------
for i in range(window, len(returns)):

    window_data = returns.iloc[i-window:i]

    try:
        model = VAR(window_data)
        res = model.fit(maxlags=maxlags, ic="aic")

        sigma = res.sigma_u
        P = np.linalg.cholesky(sigma)

        fevd = (P ** 2)
        fevd = fevd / fevd.sum(axis=1, keepdims=True)

        spill = ((fevd.sum() - np.trace(fevd)) / n) * 100

        to_ = fevd.sum(axis=1)
        from_ = fevd.sum(axis=0)
        net = (to_ - from_).mean()

        spill_list.append(spill)
        net_list.append(net)
        dates.append(returns.index[i])

    except:
        spill_list.append(np.nan)
        net_list.append(np.nan)
        dates.append(returns.index[i])


# --------------------------
# Save series
# --------------------------
spill_ts = pd.Series(spill_list, index=dates).dropna()
net_ts = pd.Series(net_list, index=dates).dropna()

spill_ts.to_csv("results/dynamic_spillover_index.csv")
net_ts.to_csv("results/dynamic_net_spillover.csv")

print("Model finished ✔")
