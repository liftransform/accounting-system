import pandas as pd
import datetime as dt
from transactions import Transaction, NameAmountTuple
import chart
from inventory import VendorInfo, _record_cash_expense

def rent_expense(date:dt.date, note:str, amount:float):
    _record_cash_expense(date, note, amount, None, chart.RENT)

def utility_expense(date:dt.date, note:str, amount:float):
    _record_cash_expense(date, note, amount, None, chart.UTILITY)

def advertising_expense(date:dt.date, note:str, amount:float):
    _record_cash_expense(date, note, amount, None, chart.ADVERTISING)

def salaries_expense(date:dt.date, note:str, amount:float):
    _record_cash_expense(date, note, amount, None, chart.SALARIES)

def other_expense(date:dt.date, note:str, amount:float):
    _record_cash_expense(date, note, amount, None, chart.MISCELLANEOUS_EXP)

def personal_expense(date:dt.date, note:str, amount:float):
    Transaction(
        date, note, 
        [NameAmountTuple(chart.DRAWINGS, amount)],
        [NameAmountTuple(chart.CASH, amount)]
    )


if __name__ == '__main__':
    
    pass
