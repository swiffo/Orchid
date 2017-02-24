import datetime
import matplotlib.pyplot as plt
import data

# Show some historical equity prices
tickers = ['GS', 'JPM', 'MS', 'DB', 'BAC', 'C']
start = datetime.date(2007, 1, 1)
end = datetime.date(2017, 2, 23)

close_prices = data.equity_close_price(tickers, start, end)
close_prices.plot()
plt.show()

# Show some historical FX rates
fx_rates = data.fx_spot_rates(['GBP/USD', 'EUR/USD'], start, end)
fx_rates.plot()
plt.show()