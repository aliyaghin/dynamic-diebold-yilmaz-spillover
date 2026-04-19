import matplotlib.pyplot as plt
import pandas as pd


# Load data
spill_ts = pd.read_csv("results/dynamic_spillover_index.csv", index_col=0, parse_dates=True).iloc[:,0]
net_ts = pd.read_csv("results/dynamic_net_spillover.csv", index_col=0, parse_dates=True).iloc[:,0]


# --------------------------
# Figure 1
# --------------------------
plt.figure(figsize=(12,5))
plt.plot(spill_ts, linewidth=2)
plt.title("Dynamic Diebold–Yilmaz Spillover")
plt.grid()
plt.savefig("results/figure1_spillover.png", dpi=300, bbox_inches="tight")
plt.close()


# --------------------------
# Figure 2
# --------------------------
plt.figure(figsize=(12,5))
plt.plot(net_ts, linewidth=2)
plt.axhline(0, linestyle="--")
plt.title("Net Spillover")
plt.grid()
plt.savefig("results/figure2_net.png", dpi=300, bbox_inches="tight")
plt.close()


# --------------------------
# Table
# --------------------------
summary = pd.DataFrame({
    "Mean": [spill_ts.mean()],
    "Max": [spill_ts.max()],
    "Min": [spill_ts.min()],
    "Std": [spill_ts.std()]
})

summary.to_csv("results/table_summary.csv", index=False)

print("Figures + tables exported ✔")
