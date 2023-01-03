from pandas import DataFrame
from seaborn import lineplot


def plot_balance_over_time(balance_time_history: DataFrame):

    axes = lineplot(data=balance_time_history[['expected_balance', 'minimum_balance', 'maximum_balance']])

    first_date = balance_time_history.date.iloc[0]
    last_date = balance_time_history.date.iloc[-1]
    # axes.plot((first_date, last_date), (0., 0.), "-r", linewidth=1, label="Zero")

    axes.grid(True)

    axes.get_legend().remove()

    axes.set_xlabel('Date')
    axes.set_ylabel('Balance')

    for line in axes.lines:
        line.set_color('steelblue')

    axes.lines[0].set_linestyle("-")
    axes.lines[1].set_linestyle("--")
    axes.lines[2].set_linestyle("--")

    return axes
