"""
A generic library for quant methods.
"""

import numpy as np
import pandas as pd


def autocorr(data, min_lag=1, max_lag=20):
    """
    Calculate auto-correlations for each column for a range of lags.

    Output is dataframe with the same columns as specified <data> and rows indexed by the lags.

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


def rolling_autocorr(data, window, lag=1):
    """
    Calculate rolling auto-correlation for each column.

    Returns dataframe with the same columns and index as <data>. Entries are the auto-correlation of the given
    column for the specified window into the past.

    :param data: Numerical dataframe.
    :param window: Number of rows for to include for each auto-correlation calculation.
    :param lag: The lag for the auto-correlation.
    :return: Dataframe as specified.
    """
    autocorr_dataframes = []

    for column, series in data.iteritems():
        rolling_mean = series.rolling(window).mean()
        rolling_var = (series ** 2).rolling(window).mean() - rolling_mean ** 2
        rolling_cov = ((series * series.shift(lag)).rolling(window).mean() - rolling_mean * rolling_mean.shift(lag))
        rolling_corr = rolling_cov / np.sqrt(rolling_var * rolling_var.shift(lag))

        autocorr_dataframes.append(pd.DataFrame(rolling_corr, columns=[column]))

    return pd.concat(autocorr_dataframes, axis=1)
