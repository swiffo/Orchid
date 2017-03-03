import collections

import pandas as pd
import pandas_datareader as pdr


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

def fx_spot_rates(crosses, start_date, end_date):
    """
    Return dataframe of date series of crosses. Index is date. Columns are given by specified
    crosses.

    :param crosses: List or single string of form CCY1/CCY2, e.g., "USD/JPY"
    :param start_date: First date to include in data
    :param end_date: Last date to include in data
    :return: pandas dataframe indexed by date, columns indexed by crosses
    """

    # We have to make one data call per denominated currency (CCY2), so start by constructing
    # a dictionary of denominated -> list of base ccys.
    denominated_to_base_dict = collections.defaultdict(list)
    for cross in crosses:
        [base, denom] = currencies_from_cross(cross)
        denominated_to_base_dict[denom].append(base)

    # Retrieve the data
    dataframes = []
    for denom, bases in denominated_to_base_dict.items():
        spot_rates = pdr.oanda.get_oanda_currency_historical_rates(start_date, end_date, quote_currency=denom, base_currency=bases)
        # We need to construct a dataframe with the correct column names (crosses). If there is only a single base currency,
        # the above call returns a time series (and we have to construct a dataframe). If there are multiple base
        # currencies, it returns a dataframe and all we need to do is rename the columns.
        if len(bases) == 1:
            spot_rates = pd.DataFrame(spot_rates, columns=['{}/{}'.format(base, denom) for base in bases])
        else:
            spot_rates.rename(columns={base: '{}/{}'.format(base, denom) for base in bases})

        dataframes.append(spot_rates)

    all_rates = pd.concat(dataframes)
    all_rates = all_rates[crosses] # reorder columns to match originally specified list of crosses

    return all_rates


def currencies_from_cross(cross):
    """
    Return base and denominated currency from cross as list.

    :param cross: E.g., 'JPY/USD'
    :return: 2-element list of currencies. [Base, Denominated].
    """
    ccys = cross.split('/')

    # Should check here that all is well:
    # ccys should be a list of length 2 with 3-character string entries
    if len(ccys) != 2 or len(ccys[0]) != 3 or len(ccys[1]) != 3:
        raise ValueError('Incorrect form of cross: {}'.format(cross))

    return ccys
