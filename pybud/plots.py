from pandas import DataFrame
from seaborn import lineplot


def plot_balance_over_time(balance_time_history: DataFrame):

    seaborn_plot = lineplot(data=balance_time_history[['Expected Balance', 'Minimum Balance', 'Maximum Balance']])

    return seaborn_plot
