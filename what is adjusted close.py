"""
The script attempts to replicate the 'Adjusted Close' value for equity taken from
Yahoo Financials data.

The hypothesis is that the adjusted close price is calculated as follows:
Starting from today, the horizon, walk backwards in time and whenever coming across
a corporate action do the following (https://blog.quandl.com/guide-to-stock-price-calculation):

DIVIDEND PAYOUT:
 Given a payout of dividend D at time T with a close price of P. Assuming the dividend
 was fully expected that means that price P is D lower than it otherwise would have been.
 Thus it is a factor P/(P+D) lower than it otherwise would have been on day D. Multiply all
 prices before day D with the factor P/(P+D).

STOCK SPLIT:
 Given a stock split of N to K at time T. A single stock at time T (and forward) is thus equivalent
 to N/K stocks at time T-1. Or conversely, stock before time T is worth K/N of stock at time T.
 Hence, we multiply price before time T by the factor N/K.


CONCLUSION:
 Well, the calculated adjusted close does not match the adjusted close from Yahoo, so who knows ...
"""

import datetime

import matplotlib.pyplot as plt
import pandas_datareader as pdr

import data

# Parameters
ticker = 'C'
start = datetime.date(2000, 5, 1)
end = datetime.date(2017, 12, 31) # This needs to be day's date or later

# Grab the Yahoo data
actual_close = data.equity_close_prices(ticker, start, end)
adjusted_close = pdr.DataReader(ticker, 'yahoo', start, end)["Adj Close"]
all_actions = pdr.DataReader(ticker, 'yahoo-actions', start, end) # splits and dividends

# Create the factors to divide historical actual close price by due to dividend effects.
# When a dividend D is paid out on day T, the actual close on day D, call it C, will be
# D lower than it would have been without dividend (if the dividend was fully priced in).
# Hence, price is lowered by a factor C/(C+D) on that day. Thus, we should divide closes
# on all previous days with that factor.
dividends = all_actions[all_actions.action == 'DIVIDEND'].value.copy()
actual_close_on_dividend_dates = actual_close[dividends.index]

dividend_factors = (actual_close_on_dividend_dates + dividends) / actual_close_on_dividend_dates
dividend_factors.sort_index(inplace=True) # ascending order
dividend_factors = dividend_factors[::-1].cumprod()[::-1]
dividend_factors = dividend_factors.reindex(actual_close.index, method='bfill', fill_value=1)
dividend_factors = dividend_factors.shift(-1).fillna(1)

# Create splits multiplier to be used for past stock prices. A split on day T has already been factored
# into the close price that day. That is, a 10 to 1 split on day D will see price about 10-double from
# day D-1 to D.
# E.g., if the stock split 2 to 1 at time T0 and 1 to 3 at time T1 > T0, then the multiplier should be:
# 1 for T1 <= T
# 1/3 for T0 <= T < T1
# 2/3 for T < T0
split_factors = all_actions[all_actions.action == 'SPLIT'].value.copy()
split_factors.sort_index(inplace=True) # ascending order
split_factors = split_factors[::-1].cumprod()[::-1]
split_factors = split_factors.reindex(actual_close.index, method='bfill', fill_value=1)
split_factors = split_factors.shift(-1).fillna(1)

calculated_adjusted_close = actual_close * split_factors / dividend_factors

# Plot it all
calculated_adjusted_close.plot()
adjusted_close.plot()
plt.show()
