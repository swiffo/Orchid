import datetime

import data

crosses = ['GBP/USD'] #, 'GBP/USD']
start_date = datetime.date(2007,1,1)
end_date = datetime.date(2017,2,23)

start = datetime.date(2007, 1, 1)
end = datetime.date(2017, 2, 23)

#fx_rates = data.fx_spot_rates(['GBP/USD', 'EUR/USD'], start, end)

spots = data.fx_spot_rates(crosses, start_date, end_date)
