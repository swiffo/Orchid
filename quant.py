import pandas as pd


def auto_corr(data, min_lag=1, max_lag=20):
    """
    Calculate auto-correlations for each column for a range of lags.

    :param data: Numerical dataframe
    :param min_lag: Smallest lag to calculate for (inclusive)
    :param max_lag: Largest lag to calculate for (inclusive)
    :return: Dataframe with columns corresponding to input dataframe, rows indexed
        by lags and entries specifying the relevant auto-correlation.
    """
    lags = range(min_lag, max_lag + 1)
    auto_correlations = []
    for column, series in data.iteritems():
        auto_correlations.append(pd.DataFrame([series.autocorr(lag) for lag in lags], columns=[column], index=lags))

    return pd.concat(auto_correlations, axis=1)
