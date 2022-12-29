from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from pybud.data import Transaction
from pybud.csv_io import read_transactions_from_csv, write_transactions_to_csv
from pybud.operations import all_recurring_transactions_to_one_time_transactions
from pybud.projection import balance_time_history
from pybud.plots import plot_balance_over_time


def read(filepath: str):

    if not filepath.endswith('.csv'):
        raise ValueError("File must be a CSV file.")

    return read_transactions_from_csv(filepath)


def write(transactions: list[Transaction], filepath: str):

    if not filepath.endswith('.csv'):
        raise ValueError("File must be a CSV file.")

    write_transactions_to_csv(transactions, filepath)


def flatten(transactions: list[Transaction], start_date: date = date.today(), end_date: date = None) -> list[Transaction]:

    if end_date is None:
        end_date = start_date + relativedelta(years=5)

    return all_recurring_transactions_to_one_time_transactions(
        transactions,
        start_date,
        end_date)


def project_balance(transactions: list[Transaction]) -> DataFrame:

    return balance_time_history(transactions)


def plot(time_history: DataFrame):

    return plot_balance_over_time(time_history)
