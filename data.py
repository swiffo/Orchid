import pandas_datareader as pdr

def equity_close_price(tickers, start_date, end_date):
    """
    Return dataframe of time series of close prices for the specified tickers.
    Note that this are true close prices. Not adjusted for splits and dividends.

    :param tickers: String or list. One (string) or more (list) equity tickers. E.g., 'GS' or ['GS', 'JPM']
    :param start_date: type datetime.date.
    :param end_date: type datetime.date.
    :return: pandas dataframe indexed by dates with columns given by tickers.
    """

    prices = pdr.DataReader(tickers, 'yahoo', start_date, end_date).Close

    return prices



