import datetime
import matplotlib.pyplot as plt
import data

tickers = ['GS', 'JPM', 'MS', 'DB', 'BAC', 'C']
start = datetime.date(2007, 1, 1)
end = datetime.date(2014, 1, 1)

close_prices = data.equity_close_price(tickers, start, end)
plt.plot(close_prices)
plt.show()


