""" PyBud legacy code
@todo

    Throw a warning if an item is not ever counted.
"""
import datetime as dt
import dateutil
import calendar
import matplotlib.pyplot


def nextdate(recurring_transaction):
    
    date = recurring_transaction["date"]
    
    if date is None:
    
        return None
    
    if recurring_transaction["recurring"]["frequency"] == "weekly":
        
        date = recurring_transaction["date"] + dateutil.relativedelta.relativedelta(weeks=+1)
        
    elif recurring_transaction["recurring"]["frequency"] == "monthly":
        
        date = recurring_transaction["date"] + dateutil.relativedelta.relativedelta(months=+1)
    
    elif recurring_transaction["recurring"]["frequency"] == "annually":
        
        date = recurring_transaction["date"] + dateutil.relativedelta.relativedelta(years=+1)
    
    elif recurring_transaction["recurring"]["frequency"] == "bi-annually":
        
        date = recurring_transaction["date"] + dateutil.relativedelta.relativedelta(years=+2)
    
    elif recurring_transaction["recurring"]["frequency"] == "semi-annually":
        
        date = recurring_transaction["date"] + dateutil.relativedelta.relativedelta(months=+6)
        
    else:
    
        raise(NotImplementedError("The specified recurrency frequency is not implemented"))
    
    enddate = recurring_transaction["recurring"]["enddate"]
    
    if enddate is not None:
    
        if date > enddate:
        
            date = None
            
    return date
    

def project_balance_time_history(account, transactions, startdate = None, enddate = None):
    
    if startdate is None:
    
        startdate = dt.date.today()
        
    else:
    
        startdate = dt.date.fromisoformat(startdate)
        
    if enddate is None:
    
        enddate = startdate + dateutil.relativedelta.relativedelta(years=+1)
        
    else:
        
        enddate = dt.date.fromisoformat(enddate)
    
    # Initialize time history
    delta = enddate - startdate
    
    daycount = delta.days
    
    dates = [startdate,]*daycount
    
    for i in range(len(dates) - 1):
        
        dates[i + 1] = dates[i] + dateutil.relativedelta.relativedelta(days=+1)
        
    balances = [[0., 0., 0.],]*daycount  # min, nominal, max
    
    # Convert all transaction dates to datetime format
    for i in range(len(transactions)):
    
        if "date" in transactions[i].keys():
        
            transactions[i]["date"] = dt.date.fromisoformat(
                transactions[i]["date"])
            
        if "recurring" in transactions[i].keys():
            
            for key in ("startdate", "enddate"):
                
                if transactions[i]["recurring"][key] is not None:
                
                    transactions[i]["recurring"][key] = dt.date.fromisoformat(
                        transactions[i]["recurring"][key])
    
    # Initialize first occurring date for recurring transactions
    for i in range(len(transactions)):
        
        if "recurring" in transactions[i].keys():
        
            assert(not ("date" in transactions[i].keys()))
            
            transactions[i]["date"] = transactions[i]["recurring"]["startdate"]
            
            while transactions[i]["date"] < startdate:
                
                transactions[i]["date"] = nextdate(transactions[i])
                
    # Initialize min, nominal, max values for each transaction which only has nominal
    for i in range(len(transactions)):
        
        value = transactions[i]["value"]
        
        if type(value) is type((0.,)):  # if a tuple
            
            assert(len(value) == 3) # assert has min, nominal, max
            
        elif type(value) is not type((0.,)):  # if not a tuple
            
            transactions[i]["value"] = (value, value, value) # make a tuple of min, nominal, max
    
        # Assert non-decreasing
        value = transactions[i]["value"]
        
        for j in range(len(value) - 1):
        
            assert(value[j + 1] >= value[j])
    
    # Add transactions for each day
    previous_day_balance = [account["balance"],]*3  # min, nominal, max
    
    for i in range(daycount):
        
        balances[i] = previous_day_balance[:]
        
        for transaction in transactions:
            
            if dates[i] == transaction["date"]:
                
                for j in range(len(transaction["value"])):
                
                    balances[i][j] += transaction["value"][j]
                    
                if "recurring" in transaction.keys():
                
                    transaction["date"] = nextdate(transaction)
                    
        previous_day_balance[:] = balances[i]
    
    min_balances = [0.,]*daycount
    
    nominal_balances = [0.,]*daycount
    
    max_balances = [0.,]*daycount
    
    for i in range(daycount):
    
        min_balances[i] = balances[i][0]
        
        nominal_balances[i] = balances[i][1]
        
        max_balances[i] = balances[i][2]
        
    return dates, (min_balances, nominal_balances, max_balances)

    