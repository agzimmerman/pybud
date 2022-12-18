from datetime import datetime
from dateutil.relativedelta import relativedelta
from pybud.csv_io import read_transactions_from_csv, write_transactions_to_csv
from pybud.operations import all_recurring_transactions_to_one_time_transactions


def process_csv(csv_filepath: str):

    raw_transactions = read_transactions_from_csv(csv_filepath)

    flattened_transactions = all_recurring_transactions_to_one_time_transactions(raw_transactions, datetime.today().date(), datetime.today().date() + relativedelta(years=2))

    write_transactions_to_csv(flattened_transactions, csv_filepath.replace('.csv', '_flattened.csv'))
