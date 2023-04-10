from pybud.api import read, write, flatten, project_balance, plot
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import show


def run(input_workbook_filepath: str, start_date: date = None, end_date: date = None):

    if not input_workbook_filepath.endswith('.xlsx'):
        raise ValueError("File must be a XLSX file.")

    if start_date is None:
        start_date = date.today()

    if end_date is None:
        end_date = start_date + relativedelta(years=5)

    input_transactions = read(input_workbook_filepath)

    flattened_transactions = flatten(input_transactions, start_date=start_date, end_date=end_date)

    write(flattened_transactions, input_workbook_filepath.replace('.xlsx', '_flattened.xlsx'))

    projected_balance = project_balance(flattened_transactions)

    fig = plot(projected_balance)

    fig.savefig(input_workbook_filepath.replace(".xlsx", "_projected_balance.png"))

    show()
