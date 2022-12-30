from pandas import DataFrame, Series
from pybud.data import Transaction


def balance_time_history(transactions: list[Transaction]):
    transactions_dataframe = DataFrame(columns=['Date', 'Expected Amount', 'Minimum Amount', 'Maximum Amount'])

    i = -1
    for transaction in transactions:
        i += 1

        transactions_dataframe.loc[i] = Series({
            'Date': transaction.transaction_date,
            'Expected Amount': transaction.expected_amount,
            'Minimum Amount': transaction.minimum_amount,
            'Maximum Amount': transaction.maximum_amount,
        })

    transactions_dataframe.sort_values(by=['Date'], inplace=True)

    balance_time_history_dataframe = DataFrame(
        columns=['Date', 'Expected Balance', 'Minimum Balance', 'Maximum Balance'])

    minimum_balance = 0
    expected_balance = 0
    maximum_balance = 0

    i = -1
    for index, row in transactions_dataframe.iterrows():
        i += 1

        expected_balance += row['Expected Amount']
        minimum_balance += row['Minimum Amount']
        maximum_balance += row['Maximum Amount']

        if i == (len(transactions_dataframe) - 1) or transactions_dataframe.loc[i + 1]['Date'] != row['Date']:
            # Just keep one row for each date which accumulates all transactions on that date.

            balance_time_history_dataframe.loc[i] = Series({
                'Date': row['Date'],
                'Expected Balance': expected_balance,
                'Minimum Balance': minimum_balance,
                'Maximum Balance': maximum_balance})

    return balance_time_history_dataframe
