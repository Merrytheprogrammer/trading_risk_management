import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# (Assuming 'df_returns', 'tda_dates', and 'l1_norms' are loaded from Step 5)

# 1. Create a Strategy DataFrame
strategy_df = pd.DataFrame(index=tda_dates)
strategy_df['Portfolio_Return'] = df_returns.mean(axis=1) # Baseline equal-weight return
strategy_df['L1_Norm'] = l1_norms

# 2. Calculate the Rolling Z-Score for the TDA Signal
# We look at the past 30 days of the L1-Norm to see what "normal" looks like
lookback = 30
strategy_df['L1_Mean'] = strategy_df['L1_Norm'].rolling(window=lookback).mean()
strategy_df['L1_Std'] = strategy_df['L1_Norm'].rolling(window=lookback).std()

# Avoid division by zero
strategy_df['L1_Std'] = strategy_df['L1_Std'].replace(0, np.nan)
strategy_df['L1_Z_Score'] = (strategy_df['L1_Norm'] - strategy_df['L1_Mean']) / strategy_df['L1_Std']

# 3. Generate Trading Signals based on the TDA Alarm
# Rule: If Z-score > 3.0, we are in a Danger Zone.
threshold = 3.0
strategy_df['Danger_Zone'] = strategy_df['L1_Z_Score'] > threshold

# 4. Execute the Strategy
# If we are in the Danger Zone, our return is 0 (we moved to cash).
# Otherwise, we get the normal portfolio return.
strategy_df['Strategy_Return'] = np.where(strategy_df['Danger_Zone'].shift(1), 0.0, strategy_df['Portfolio_Return'])

# Calculate Cumulative Returns to see which performed better
strategy_df['Buy_Hold_Growth'] = (1 + strategy_df['Portfolio_Return']).cumprod()
strategy_df['TDA_Strategy_Growth'] = (1 + strategy_df['Strategy_Return']).cumprod()

# 5. Plot the Final Backtest
plt.figure(figsize=(12, 6))

plt.plot(strategy_df.index, strategy_df['Buy_Hold_Growth'], label='Buy & Hold (Baseline)', alpha=0.7)
plt.plot(strategy_df.index, strategy_df['TDA_Strategy_Growth'], label='TDA Risk Managed Strategy', color='green', linewidth=2)

# Highlight when the algorithm pulled us out of the market
danger_days = strategy_df[strategy_df['Danger_Zone']].index
for day in danger_days:
    plt.axvline(x=day, color='red', alpha=0.1, linewidth=4)

plt.title('Step 6: TDA Risk Management vs. Buy & Hold')
plt.ylabel('Cumulative Portfolio Growth')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Final Performance Output
bh_return = (strategy_df['Buy_Hold_Growth'].iloc[-1] - 1) * 100
tda_return = (strategy_df['TDA_Strategy_Growth'].iloc[-1] - 1) * 100

print(f"Final Buy & Hold Return: {bh_return:.2f}%")
print(f"Final TDA Strategy Return: {tda_return:.2f}%")
