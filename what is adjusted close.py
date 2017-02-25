"""
The script attempts to replicate the 'Adjusted Close' value for equity taken from
Yahoo Financials data.

The hypothesis is that the adjusted close price is calculated as follows:
 Starting from today (the horizon), walk backwards in time keeping track of total dividend paid out.
 At every step subtract the total dividend paid out from the price (the reason being that
 the price at that time has that dividend factored in unlike the price at the horizon). Whenever
 a dividend is encountered, add that to the total dividend paid out. Whenever a split is encountered
 (say an N to K split), multiply all earlier close prices and dividends by N/K.

 'Butt, butt, butt ...,' I hear you cry. 'That would mean stock prices can go negative if subsequent
  dividends sum up to more than the stock price!' You are right of course. That clearly makes it incorrect.
"""

import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as pdr

import data

# Parameters
ticker = 'C'
start = datetime.date(2000, 1, 1)
end = datetime.date(2017, 2, 20)

# The below is a fine example of how not to store and manipulate data.
# Really everything should be in dataframes and the column names should be
# tickers.

actual_close = data.equity_close_prices(ticker, start, end)
adjusted_close = pdr.DataReader(ticker, 'yahoo', start, end)["Adj Close"]  # Pandas Series
all_actions = pdr.DataReader(ticker, 'yahoo-actions', start, end) # splits and dividends

# Create dividends dataframe. Again, there is no point in calling the column 'dividend'.
# It's already implied by the variable name that it contains dividends. Much better would
# be to allow for multiple tickers and use the tickers as column names.
dividends = all_actions[all_actions.action == 'DIVIDEND'][['value']]
dividends.rename(columns={'value': 'dividend'}, inplace=True)

# Create splits multiplier to be used for past stock prices.
# E.g., if the stock split 2 to 1 at time T0 and 1 to 3 at time T1 > T0, then the multiplier should be:
# 1 for T1 <= T
# 1/3 for T0 < T < T1
# 2/3 for T <= T0
splits = all_actions[all_actions.action == 'SPLIT'][['value']]
splits.rename(columns={'value': 'split'}, inplace=True)
splits.sort_index(inplace=True)
splits['split'] = splits.ix[::-1, 'split'].cumprod()[::-1]
splits = splits.reindex(pd.date_range(start, end), method='bfill', fill_value=1)

# Adjust dividends for splits
adjusted_dividends = pd.DataFrame()
adjusted_dividends['dividend'] = dividends.dividend * splits.split
adjusted_dividends.dropna(inplace=True)

# Adjust close prices for splits
my_adjusted_closes = pd.DataFrame()
my_adjusted_closes['close'] = actual_close * splits.split
my_adjusted_closes.dropna(inplace=True)

# Calculate estimate of the adjusted close price
adjusted_dividends['cumulative'] = adjusted_dividends.ix[::-1, 'dividend'].cumsum()[::-1]
price_correction = adjusted_dividends.reindex(my_adjusted_closes.index, method='bfill', fill_value=0)
my_adjusted_closes['close'] = my_adjusted_closes['close'] - price_correction['cumulative']

# Plot it all
my_adjusted_closes.plot()
adjusted_close.plot()
plt.show()
