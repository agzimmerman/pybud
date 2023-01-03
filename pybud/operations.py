from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import DataFrame, Series, isnull


def all_recurring_transactions_to_one_time_transactions(
        transactions: DataFrame,
        start_date: date,
        end_date: date
        ) -> DataFrame:

    one_time_transactions = DataFrame(columns=transactions.keys())
    i = 0
    for _, transaction in transactions.iterrows():

        if isnull(transaction.recurrence_unit) or isnull(transaction.recurrence_period):
            one_time_transactions.loc[i] = transaction
            i += 1
            continue

        for _, one_time_transaction in recurring_transaction_to_one_time_transactions(transaction, start_date, end_date).iterrows():
            one_time_transactions.loc[i] = one_time_transaction
            i += 1

    return one_time_transactions


def recurring_transaction_to_one_time_transactions(
        recurring_transaction: Series,
        min_first_date: date,
        max_last_date: date
        ) -> DataFrame:

    one_time_transactions = DataFrame(columns=recurring_transaction.keys())

    if isnull(recurring_transaction.recurrence_start_date) or recurring_transaction.recurrence_start_date < min_first_date:
        first_date = min_first_date
    else:
        first_date = recurring_transaction.recurrence_start_date

    if isnull(recurring_transaction.recurrence_end_date) or recurring_transaction.recurrence_end_date > max_last_date:
        final_date = max_last_date
    else:
        final_date = recurring_transaction.recurrence_end_date

    i = 0
    previous_date = None
    while True:

        new_date = first_date + i * relativedelta(
            **{recurring_transaction.recurrence_unit.lower(): recurring_transaction.recurrence_period})

        if previous_date is not None and new_date <= previous_date:
            raise ValueError("Invalid recurrence date")

        if new_date > final_date:
            break

        new_transaction = recurring_transaction.copy(deep=True)
        new_transaction.label = recurring_transaction.label + f" Recurrence #{i}"
        new_transaction.date = new_date
        new_transaction.recurrence_start_date = None
        new_transaction.recurrence_end_date = None
        new_transaction.recurrence_unit = None
        new_transaction.recurrence_period = None

        one_time_transactions.loc[i] = new_transaction
        i += 1

        previous_date = new_date

    return one_time_transactions
