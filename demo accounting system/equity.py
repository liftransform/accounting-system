from transactions import Transaction, NameAmountTuple
import datetime as dt
import chart

def use_cash_personally(date:dt, note:str, amount:float):
    Transaction(date, note, [NameAmountTuple(chart.DRAWINGS, amount)], [NameAmountTuple(chart.CASH, amount)])

def invest_cash(date:dt, note:str, amount:float):
    Transaction(
        date,
        note, 
        [NameAmountTuple(chart.CASH, amount)],
        [NameAmountTuple(chart.OWNERS_EQUITY, amount)]
    )


