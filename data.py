import datetime

import pandas as pd
import pandas_datareader as pdr
import pytz


def equity_close_prices(tickers, start_date, end_date):
    """
    Return dataframe of date series of close prices for the specified tickers.
    Note that this are true close prices. Not adjusted for splits and dividends.

    :param tickers: String or list. One (string) or more (list) equity tickers. E.g., 'GS' or ['GS', 'JPM']
    :param start_date: type datetime.date.
    :param end_date: type datetime.date.
    :return: pandas dataframe indexed by dates with columns given by tickers.
    """

    prices = pdr.DataReader(tickers, 'yahoo', start_date, end_date).Close

    return prices


def fx_spot_rates(currency_pairs, start, end):
    """
    Return dataframe of time series of NY noon exchange rates for the specified currency pairs.

    :param currency_pairs: list of currency pairs. Each pair of the form <base currency>/<quote currency>. E.g., "USD/JPY".
    :param start: start date (inclusive)
    :param end: end date (inclusive)
    :return: Dataframe indexed by time and with columns defined by the specified currency pairs.
    """
    # Construct the list of currencies to pull in FRED FX data for (against USD)
    all_currencies = set()
    for pair in currency_pairs:
        for ccy in currencies_from_cross(pair):
            all_currencies.add(ccy.upper())

    if 'USD' in all_currencies:
        all_currencies.remove('USD')

    # Currency -> FRED symbol, whether USD is base currency or not
    ccy_to_FRED_info = {
        'BRL': ('DEXBZUS', True),
        'CAD': ('DEXCAUS', True),
        'CHF': ('DEXSZUS', True),
        'DKK': ('DEXDNUS', True),
        'EUR': ('DEXUSEU', False),
        'GBP': ('DEXUSUK', False),
        'INR': ('DEXINUS', True),
        'JPY': ('DEXJPUS', True),
        'KRW': ('DEXKOUS', True),
        'MXN': ('DEXMXUS', True),
        'MYR': ('DEXMAUS', True),
        'ZAR': ('DEXSFUS', True),
    }

    # Get the names for data series in FRED and whether they need to be inverted (reciprocal
    # value) to have USD as base currency.
    data_series_names = [ccy_to_FRED_info.get(ccy)[0] for ccy in all_currencies]
    data_series_invert = [ccy_to_FRED_info.get(ccy)[1] for ccy in all_currencies]

    # USD/<ccy> data frame
    data = pdr.data.DataReader(data_series_names, 'fred', start, end)
    data.columns = all_currencies
    for ccy, do_inversion in zip(all_currencies, data_series_invert):
        if do_inversion:
            data[ccy] = 1 / data[ccy]

    # For each currency pair, used the exchange rates with USD as base currency to construct
    # the exchange rate.
    rate_dfs = []
    for pair in currency_pairs:
        [base_ccy, quote_ccy] = currencies_from_cross(pair)
        if base_ccy == 'USD':
            rate_ts = 1 / data[quote_ccy]
        elif quote_ccy == 'USD':
            rate_ts = data[base_ccy]
        else:
            rate_ts = data[base_ccy] / data[quote_ccy]

        rate_ts.name = pair
        rate_dfs.append(rate_ts)

    # The FRED website states that the exchange rates are the buy rates at noon in NY. Whatever that means.
    rate_df = pd.concat(rate_dfs, axis=1)
    NY_TZ = pytz.timezone('US/Eastern')
    rate_df.index = [datetime.datetime(t.year, t.month, t.day, 12, 0, 0, tzinfo=NY_TZ) for t in rate_df.index]

    return rate_df


def currencies_from_cross(cross):
    """
    Return base and quote currency from cross as list: [base, quote].

    :param cross: E.g., 'JPY/USD'
    :return: 2-element list of currencies. [Base, Denominated].
    """
    ccys = cross.split('/')

    # Should check here that all is well:
    # ccys should be a list of length 2 with 3-character string entries
    if len(ccys) != 2 or len(ccys[0]) != 3 or len(ccys[1]) != 3:
        raise ValueError('Incorrect form of cross: {}'.format(cross))

    return ccys
