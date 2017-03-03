import datetime

import matplotlib.pyplot as plt
import numpy as np

import data
import quant

# STEP 1: Get entire history of auto-correlation of log-diffs of spots
# (Not used in trade example below)
crosses = ['GBP/USD', 'EUR/USD']
start_date = datetime.date(2001, 1, 1)
end_date = datetime.date(2017, 3, 3)
lags = range(1, 11)

spots = data.fx_spot_rates(crosses, start_date, end_date)
logdiff_spots = np.log(spots).diff()  # Diff from T to T+1 assigned to T+1
autocorr = quant.autocorr(logdiff_spots, 1, 10)

print('Auto-correlation over time frame')
print(autocorr)

# STEP 2: Calculate rolling 1-year auto-correlation
rolling_autocorr = quant.rolling_autocorr(logdiff_spots, 252, 1)  # Yearly auto-correlation
rolling_autocorr.plot()
plt.show()

# STEP 3: As 1-day correlation is positive, try going long whenever rates go up
# and short whenever they go down. Close out trade each day.
# (Ignores transaction costs and interest rate differences)
fx_returns = spots.diff()  # At T, change from T-1 to T
position = np.sign(rolling_autocorr) * fx_returns  # Position at T [end of day] (just using the sign works equally well)
trade_returns = fx_returns.shift(-1) * position

trade_returns.cumsum().plot()
plt.show()
