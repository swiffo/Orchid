import datetime
import matplotlib.pyplot as plt
import data
import numpy as np
import pandas as pd
import drawdown as dd


# Show some historical equity prices
tickers = ['GS', 'JPM', 'MS', 'DB', 'BAC', 'C']
start = datetime.date(2007, 1, 1)
end = datetime.date(2017, 2, 23)

close_prices = data.equity_close_prices(tickers, start, end)
close_prices.plot()
plt.show()


# Show some historical FX rates
fx_rates = data.fx_spot_rates(['GBP/USD', 'EUR/USD'], start, end)
fx_rates.plot()
plt.show()


# Show some drawdown plots for a strategy yielding random returns
JPM_closes = close_prices['JPM']    # Yields a Series object with JPM closes
orig_close = JPM_closes[0]                 
factor = orig_close*0.02            # Max absolute value of daily returns 
                                    # constrained to 2% original JPM quote
np.random.seed(42)
return_series = pd.Series(factor*(np.random.rand(len(JPM_closes))-0.5),
                             index=JPM_closes.index)
fig = dd.figure_relative_drawdown(return_series, orig_close)
plt.show()

