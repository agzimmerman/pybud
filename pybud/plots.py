from pandas import DataFrame
from matplotlib.pyplot import axes


def plot_balance_over_time(balance_time_history: DataFrame):

    color = "steelblue"

    ax = axes()

    ax.plot(balance_time_history.date, balance_time_history.minimum_balance, "--", color=color, linewidth=1, label="Min")

    ax.plot(balance_time_history.date, balance_time_history.expected_balance, "-", color=color, linewidth=2, label="Nominal")

    ax.plot(balance_time_history.date, balance_time_history.maximum_balance, "--", color=color, linewidth=1, label="Max")

    first_date = balance_time_history.date.iloc[0]
    last_date = balance_time_history.date.iloc[-1]
    ax.plot((first_date, last_date), (0., 0.), "-r", linewidth=1, label="Zero")

    ax.grid(True)

    ax.set_xlabel('Date')
    ax.set_ylabel('Balance')

    return ax
