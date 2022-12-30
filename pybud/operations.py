from pybud.data import Transaction
from datetime import date
from dateutil.relativedelta import relativedelta


def all_recurring_transactions_to_one_time_transactions(transactions: list[Transaction], start_date: date, end_date: date) -> list[Transaction]:

    one_time_transactions = []

    for transaction in transactions:
        if transaction.recurrence_unit is None or transaction.recurrence_period is None:
            one_time_transactions.append(transaction)
            continue
        one_time_transactions.extend(recurring_transaction_to_one_time_transactions(transaction, start_date, end_date))

    return one_time_transactions


def recurring_transaction_to_one_time_transactions(recurring_transaction: Transaction, min_first_date: date, max_last_date: date) -> list[Transaction]:

    one_time_transactions = []

    if recurring_transaction.recurrence_start_date is None or recurring_transaction.recurrence_start_date < min_first_date:
        first_date = min_first_date
    else:
        first_date = recurring_transaction.recurrence_start_date

    if recurring_transaction.recurrence_end_date is None or recurring_transaction.recurrence_end_date > max_last_date:
        last_date = max_last_date
    else:
        last_date = recurring_transaction.recurrence_end_date

    counter = 0
    while (one_time_transactions[-1].transaction_date if len(one_time_transactions) > 0 else first_date) < last_date:
        one_time_transactions.append(Transaction(
            label=recurring_transaction.label + f" Recurrence #{counter}",
            expected_amount=recurring_transaction.expected_amount,
            transaction_date=first_date + counter * relativedelta(**{recurring_transaction.recurrence_unit.name.lower(): recurring_transaction.recurrence_period}),
            minimum_amount=recurring_transaction.minimum_amount,
            maximum_amount=recurring_transaction.maximum_amount,
            recurrence_start_date=recurring_transaction.recurrence_start_date,
            recurrence_end_date=recurring_transaction.recurrence_end_date,
            recurrence_unit=recurring_transaction.recurrence_unit,
            recurrence_period=recurring_transaction.recurrence_period,
            recurrence_handoff_id=recurring_transaction.recurrence_handoff_id
        ))
        counter += 1

    return one_time_transactions
