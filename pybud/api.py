from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import DataFrame
from pybud.csv_io import read_transactions_dataframe_from_excel, write_transactions_dataframe_to_excel
from pybud.operations import all_recurring_transactions_to_one_time_transactions
from pybud.projection import balance_time_history
from pybud.plots import plot_balance_over_time


def read(filepath: str):

    if not filepath.endswith('.xlsx'):
        raise ValueError("File must be a XLSX file.")

    return read_transactions_dataframe_from_excel(filepath)


def write(transactions: DataFrame, filepath: str):

    if not filepath.endswith('.xlsx'):
        raise ValueError("File must be a XLSX file.")

    write_transactions_dataframe_to_excel(transactions, filepath)


def flatten(transactions: DataFrame, start_date: date = date.today(), end_date: date = None) -> DataFrame:

    if end_date is None:
        end_date = start_date + relativedelta(years=5)

    return all_recurring_transactions_to_one_time_transactions(
        transactions,
        start_date,
        end_date)


def project_balance(transactions: DataFrame) -> DataFrame:

    return balance_time_history(transactions)


def plot(time_history: DataFrame):

    return plot_balance_over_time(time_history)
