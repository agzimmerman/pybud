from datetime import date
from os import remove
from pandas import DataFrame, read_excel, to_datetime, isnull
from shutil import copyfile


def __empty(string: str):
    return string == ''


def __date(string: str):
    return date.fromisoformat(string)


def read_transactions_dataframe_from_excel(filepath: str) -> DataFrame:

    # Have to read a copy instead of the original in case the original is open in Excel which locks the file (also for some reason for reading, not just writing).
    temp_filepath = filepath.replace('.xlsx', '_pybud_temp_copy.xlsx')
    copyfile(filepath, temp_filepath)
    transactions = read_excel(filepath)
    remove(temp_filepath)

    transactions = transactions.drop(transactions[transactions.enabled != 1].index)

    validate(transactions)

    for column in ['date', 'recurrence_start_date', 'recurrence_end_date']:
        convert_column_from_timestamp_to_date(transactions, column)

    set_defaults_for_missing_values_inplace(transactions)

    return transactions


def convert_column_from_timestamp_to_date(transactions: DataFrame, column: str):

    transactions[column] = to_datetime(transactions[column]).dt.date


def set_defaults_for_missing_values_inplace(transactions: DataFrame):

    for i, transaction in transactions.iterrows():

        if isnull(transaction.minimum_amount):
            transactions.at[i, 'minimum_amount'] = transaction.expected_amount
        if isnull(transaction.maximum_amount):
            transactions.at[i, 'maximum_amount'] = transaction.expected_amount


def validate(transactions: DataFrame):

    for _, transaction in transactions.iterrows():

        if isnull(transaction.date):
            if isnull(transaction.recurrence_unit) or isnull(transaction.recurrence_period):
                raise ValueError("Date is missing for transaction with label " + transaction.label)


def write_transactions_dataframe_to_excel(transactions: DataFrame, filepath: str):

    transactions.to_excel(filepath, index=False)
