from pandas import DataFrame, Series


def balance_time_history(transactions: DataFrame):

    transactions.sort_values(by=['date'], inplace=True)

    balance_time_history_dataframe = DataFrame(columns=['date', 'expected_balance', 'minimum_balance', 'maximum_balance'])

    minimum_balance = 0
    expected_balance = 0
    maximum_balance = 0

    i = -1
    for _, row in transactions.iterrows():
        i += 1

        expected_balance += row.expected_amount
        minimum_balance += row.minimum_amount
        maximum_balance += row.maximum_amount

        if i == (len(transactions) - 1) or transactions.loc[i + 1].date != row.date:
            # Just keep one row for each date which accumulates all transactions on that date.

            balance_time_history_dataframe.loc[i] = Series({
                'date': row.date,
                'expected_balance': expected_balance,
                'minimum_balance':  minimum_balance,
                'maximum_balance':  maximum_balance})

    return balance_time_history_dataframe
