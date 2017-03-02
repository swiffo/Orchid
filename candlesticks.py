import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.figure()

axisHorizontal = plt.gca()

frame = pd.DataFrame({"a" : pd.Series([1,2,3], index = [1,2,3])})

axisHorizontal.set_xticks = list(frame.index)

axisHorizontal.add_patch(Rectangle((0.5,0.5),0.2,0.7, fill=None, color="red"))

plt.show()











"""
Visualization. Using only matplotlib-native functions, using stylesheet similar
to pandas.plotting.py source.
"""

candle_stylesheet = {
    'axes.axisbelow': True,
    'axes.edgecolor': '#bcbcbc',
    'axes.facecolor': '#eeeeee',
    'axes.grid': True,
    'axes.labelcolor': '#555555',
    'axes.labelsize': 'large',
    'axes.linewidth': 1.0,
    'axes.titlesize': 'x-large',
    'xtick.color': '#555555',
    'xtick.direction': 'in',
    'xtick.major.pad': 6.0,
    'xtick.major.size': 0.0,
    'xtick.minor.pad': 6.0,
    'xtick.minor.size': 0.0,
    'ytick.color': '#555555',
    'ytick.direction': 'in',
    'ytick.major.pad': 6.0,
    'ytick.major.size': 0.0,
    'ytick.minor.pad': 6.0,
    'ytick.minor.size': 0.0
    }
