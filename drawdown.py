"""
Collection of functions for computing drawdown of Series and
DataFrames of returns. In all cases, the input is a series of *absolute*
returns (e.g., each row could contains the currency value of a portfolio
managers return on a day). Returns are assumed to be any value of type float.

There is a plethora of definitions of "drawdown" in the popular literature on finance
(including many synonyms). The version used here is the most straightforward one found
in the academic literature.

The functions are slightly inefficient due to using function calls
instead of inlining, and hence repeated computation of the cumulative
sum of the input Series. However, they should be easier to read and
maintain than if using inlining.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy


def absolute_drawdown(ser, offset=0.0):
    """
    Return Series containing the drawdown at each row. 

    :param ser: Series of values of type float (e.g., a series of daily
    returns of a portfolio manager)
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Series using index of param ser, containing the drawdowns.
    Will be a non-negative number.
    """
    
    cum_return = offset + ser.cumsum()
    raw_drawdown = cum_return.cummax() - cum_return
    # Set negative values to 0.0 as drawdown is max(0,raw_drawdown)
    return raw_drawdown.clip(0.0)


def relative_drawdown(ser, offset=0.0):
    """
    Return Series containing the drawdown at each row divided by peak
    instrument value seen so far. As per standard conventions, positive
    values of relative drawdown are 

    :param ser: Series of values of type float (e.g., a series of daily
    returns of a portfolio manager)
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Series using index of ser containing the
    relative drawdown. 
    """

    cum_return_max = offset + ser.cumsum().cummax()
    raw_rel_drawdown = absolute_drawdown(ser,offset)/cum_return_max
    # Set negative values to 0.0 as relative drawdown is max(0,raw_rel_drawdown)
    return raw_rel_drawdown.clip(0.0)


def maximum_absolute_drawdown(ser, offset=0.0):
    """
    Return maximum drawdown of a Series

    :param ser: Series of values of type float (e.g., a series of daily
    returns of a portfolio manager)
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Series using index of param ser, containing the maximum drawdown at each index value.
    """

    return absolute_drawdown(ser, offset).cummax()


def maximum_relative_drawdown(ser, offset=0.0):
    """
    Return maximum of relative drawdown of a Series

    :param ser: Series of values of type float (e.g., a series of daily
    returns of a portfolio manager)
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Series using index of param ser, containing the maximum relative drawdown at each index value.
    """

    return relative_drawdown(ser, offset).cummax()



def mar_ratio(ser, offset=0.0):
    """
    Return MAR ratio; the cumulative instrument value divided by
    maximum drawdown. :param ser: Series of values of type float (e.g.,
    a series of daily returns of a portfolio manager). This is the most
    straightforward version of the MAR ratio occurring in the
    literature; other versions are similar to the Calmar ratio, use the
    risk-free rate of return, or rolling averages over time. These are
    not the droids we're looking for.
    
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Float equal to mar ratio. Will be a number
    between 0.0 and 1.0
    """

    return (offset + ser.cumsum())/maximum_absolute_drawdown(ser, offset)


def zscore(ser, offset=0.0):
    pass
    # TBD



"""
Visualization.
"""

def figure_relative_drawdown(ser, offset=0.0):
    """
    For a Series of returns and an initial value show:
    (i)   the cumulative returns at each index value
    (ii)  the return at each index value
    (iii) the relative drawdown at each index value

    :param ser: Series of values of type float (e.g., a series of daily
    returns of a portfolio manager)
    :param offset: Value of type float
    (e.g., the initial value of a portfolio at the beginning of the
    series of returns)
    :return: Figure object containing the
    Roman-numeral-numbered items above as subplots.
    """

    # Create array of 3 subplots with identical horizontal axes
    fig, axesarray = plt.subplots(3, sharex=True)

    # Draw cumulative returns in topmost subplot
    cumulative_returns_ax = axesarray[0]
    cumulative_returns_ax.plot(ser.cumsum())
    cumulative_returns_ax.set_title("Cumulative returns")

    # Draw series of return in middle subplot
    returns_ax = axesarray[1]
    returns_ax.plot(ser)
    returns_ax.set_title("Returns")

    # Draw relative drawdown as negative values (larger drawdowns are /down/)
    #   in bottommost subplot.
    relative_drawdown_ax = axesarray[2]
    relative_drawdown_ax.plot(- relative_drawdown(ser, offset))
    relative_drawdown_ax.set_title("Relative drawdown")

    # Return the figure to avoid having a function with side effects
    return fig
    

