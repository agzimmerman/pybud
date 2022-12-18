from pybud.data import Transaction
from datetime import date
from dateutil.relativedelta import relativedelta


def all_recurring_transactions_to_one_time_transactions(transactions: list[Transaction], start_date: date, end_date: date) -> list[Transaction]:

    one_time_transactions = []

    for transaction in transactions:
        if transaction.recurrence is not None:
            one_time_transactions += recurring_transaction_to_one_time_transactions(transaction, start_date, end_date)

    return one_time_transactions


def recurring_transaction_to_one_time_transactions(recurring_transaction: Transaction, min_first_date: date, max_last_date: date) -> list[Transaction]:

    one_time_transactions = []

    if recurring_transaction.recurrence.start_date is None or recurring_transaction.recurrence.start_date < min_first_date:
        first_date = min_first_date
    else:
        first_date = recurring_transaction.recurrence.start_date

    if recurring_transaction.recurrence.end_date is None or recurring_transaction.recurrence.end_date > max_last_date:
        last_date = max_last_date
    else:
        last_date = recurring_transaction.recurrence.end_date

    counter = 0
    while (one_time_transactions[-1].date if len(one_time_transactions) > 0 else first_date) < last_date:
        one_time_transactions.append(Transaction(
            label=recurring_transaction.label + f" Recurrence #{counter}",
            expected_amount=recurring_transaction.expected_amount,
            transaction_date=first_date + counter * relativedelta(**{recurring_transaction.recurrence.unit.name.lower(): recurring_transaction.recurrence.period}),
            minimum_amount=recurring_transaction.uncertain_amount.minimum,
            maximum_amount=recurring_transaction.uncertain_amount.maximum,
        ))

    return one_time_transactions
