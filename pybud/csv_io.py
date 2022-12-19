import csv
from datetime import date
from pybud.data import Transaction, RecurrenceUnit


def __empty(string: str):
    return string == ''


def __date(string: str):
    return date.fromisoformat(string)


def read_transactions_from_csv(csv_filepath: str) -> list[Transaction]:
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel')

        transactions = []

        for row in reader:

            enabled = row['Enabled'] == 'TRUE'
            if not enabled:
                continue

            label = row['Label']
            if label == '':
                raise Exception("Label cannot be empty")

            expected_amount = float(row['Expected Amount'])

            transaction_date_str = row['Date']
            transaction_date = None if __empty(transaction_date_str) else __date(transaction_date_str)

            minimum_amount_str = row['Minimum Amount']
            minimum_amount = None if __empty(minimum_amount_str) else float(minimum_amount_str)

            maximum_amount_str = row['Maximum Amount']
            maximum_amount = None if __empty(maximum_amount_str) else float(maximum_amount_str)

            recurrence_start_date_str = row['Recurrence Start Date']
            recurrence_start_date = None if __empty(recurrence_start_date_str) else __date(recurrence_start_date_str)

            recurrence_end_date_str = row['Recurrence End Date']
            recurrence_end_date = None if __empty(recurrence_end_date_str) else __date(recurrence_end_date_str)

            recurrence_unit_str = row['Recurrence Unit']
            if __empty(recurrence_unit_str):
                recurrence_unit = None
            else:
                if recurrence_unit_str == 'Days':
                    recurrence_unit = RecurrenceUnit.DAYS
                elif recurrence_unit_str == 'Weeks':
                    recurrence_unit = RecurrenceUnit.WEEKS
                elif recurrence_unit_str == 'Months':
                    recurrence_unit = RecurrenceUnit.MONTHS
                elif recurrence_unit_str == 'Years':
                    recurrence_unit = RecurrenceUnit.YEARS
                else:
                    raise NotImplementedError(f"Recurrence unit {recurrence_unit_str} not implemented")

            recurrence_period_str = row['Recurrence Period']
            recurrence_period = None if __empty(recurrence_period_str) else int(recurrence_period_str)

            if (recurrence_period is not None and recurrence_unit is None) or (recurrence_period is None and recurrence_unit is not None):
                raise Exception("Recurrence period and unit must both be specified or neither specified")

            recurrence_handoff_id_str = row['Recurrence Handoff ID']
            recurrence_handoff_id = None if __empty(recurrence_handoff_id_str) else int(recurrence_handoff_id_str)

            transactions.append(
                Transaction(
                    label=label,
                    expected_amount=expected_amount,
                    transaction_date=transaction_date,
                    minimum_amount=minimum_amount,
                    maximum_amount=maximum_amount,
                    recurrence_start_date=recurrence_start_date,
                    recurrence_end_date=recurrence_end_date,
                    recurrence_unit=recurrence_unit,
                    recurrence_period=recurrence_period,
                    recurrence_handoff_id=recurrence_handoff_id
                )
            )

        return transactions


def write_transactions_to_csv(transactions: list[Transaction], csv_filepath: str):

    if len(transactions) == 0:
        return

    with open(csv_filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=transactions[0].__dict__.keys())

        writer.writeheader()

        for transaction in transactions:
            writer.writerow(transaction.__dict__)
