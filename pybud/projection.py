from pandas import DataFrame, Series
from pybud.data import Transaction


def balance_time_history(transactions: list[Transaction]):

    transactions_dataframe = DataFrame(columns=['Date', 'Amount'])

    i = -1
    for transaction in transactions:
        i += 1

        transactions_dataframe.loc[i] = Series({'Date': transaction.transaction_date, 'Amount': transaction.expected_amount})

    transactions_dataframe.sort_values(by=['Date'], inplace=True)

    balance_time_history_dataframe = DataFrame(columns=['Date', 'Balance'])

    balance = 0

    i = -1
    for index, row in transactions_dataframe.iterrows():
        i += 1

        balance += row['Amount']

        if i == (len(transactions_dataframe) - 1) or transactions_dataframe.loc[i + 1]['Date'] != row['Date']:
            # Just keep one row for each date which accumulates all transactions on that date.

            balance_time_history_dataframe.loc[i] = Series({'Date': row['Date'], 'Balance': balance})

    return balance_time_history_dataframe