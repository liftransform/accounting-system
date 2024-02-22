import pandas as pd
import datetime

#---------------
CASH = 'cash'
AR = 'accounts receivable'
MERCH_INVENTORY = 'merchandise inventory'
ALLOWANCE_FOR_DOUBTFUL_ACCOUNTS = 'allowance for doubtful accounts'
RAW_MATERIAL = 'raw material'
SUPPLIES = 'supplies'
NOTES_RECEIVABLE = 'notes receivable'
DEBT_INVESTMENT = 'debt investment'

EQUIPMENT = 'equipment'
ACCUMULATED_DEP = 'accumulated depreciation'
LAND = 'land'

AP = 'accounts payable'
SHORT_TERM_LOANS = 'short term loans'
NOTES_PAYABLE = 'notes payable'
DEBT = 'debt'


SALES = 'sales'
SALES_DISCOUNTS = 'sales discounts'
SALES_RETURNS = 'sales returns and allowances'
BAD_DEBT_EXPENSE = 'bad debt expense'


COGS = 'cost of goods sold'

RENT = 'rent'
UTILITY = 'utility'
INSURANCE = 'insurance'
ADVERTISING = 'advertising'
DEPRECIATION_EXP = 'depreciation expense'
SALARIES = 'salaries'
MISCELLANEOUS_EXP = 'miscellaneous expenses'
SUPPLIES_EXPENSE = 'supplies expense'


INTEREST_INCOME = 'interest income'
INTEREST_EXP = 'interest expense'
OTHER_INCOME = 'other income'
OTHER_EXPENSE = 'other expense'

OWNERS_EQUITY = "owner's equity"
DRAWINGS = 'Drawings'
RETAINED_EARNINGS = 'retained earnings'
AOCI = 'Accumulated other comprehensive income' #accumulate other comprehensive income

#-----------account types
CURRENT_ASSETS = 'current asset'
NON_CURRENT_ASSETS = 'non-current assets'
CONTRA_ASSETS = 'contra assest'

CURRENT_LIABILITY = 'current liability'
NON_CURRENT_LIABILITY = 'non-current liability'

INCOME = 'income'
EXPENSE = 'expense'
CONTRA_REVENUE = 'contra revenue'
OPERATING_EXPENSE = 'operating expense'
TAX = 'tax'

LOSS_ON_DISPOSAL = 'loss on disposal of asset'
GAIN_ON_DISPOSAL = 'gain on disposal of asset'

EQUITY = 'equity'
#----------



class Change:
    def __init__(self, date:datetime.datetime, amount: float, note ='') -> None:
        self.amount = amount
        self.date = date
        self.note = note

class Account:
    def __init__(self, name, type, debit_increases:bool) -> None:
        self.name = []
        self._changes = []
        self.name = name
        self.debit_increases = debit_increases
        self.type = type

    def debit(self, date, amount, note):
        if self.debit_increases:
            self._changes.append(Change(date, amount, note))
        else:
            self._changes.append(Change(date, -1*amount, note))


    def credit(self, date, amount, note):
        if self.debit_increases:
            self._changes.append(Change(date, -1*amount, note))
        else:
            self._changes.append(Change(date, amount, note))

    def current_balanace(self) -> float:
        return sum([c.amount for c in self._changes])
    

CHART:list[Account] = [
    Account(item, CURRENT_ASSETS, True) 
    for item in [CASH, AR, MERCH_INVENTORY, SUPPLIES, RAW_MATERIAL, NOTES_RECEIVABLE]] + [
        
    Account(item, NON_CURRENT_ASSETS, True)
    for item in [LAND, EQUIPMENT, DEBT_INVESTMENT]
    ] + [

        Account(ACCUMULATED_DEP, CONTRA_ASSETS, False),
        Account(ALLOWANCE_FOR_DOUBTFUL_ACCOUNTS, CONTRA_ASSETS, False),
        Account(DEBT, NON_CURRENT_LIABILITY, False),
        Account(SALES, INCOME, False),
        Account(COGS, COGS, True),
        Account(INTEREST_INCOME, OTHER_INCOME, False),
        Account(GAIN_ON_DISPOSAL, OTHER_INCOME, False),
        Account(LOSS_ON_DISPOSAL, OTHER_EXPENSE, True),
        Account(OTHER_EXPENSE, OTHER_EXPENSE, True),
        Account(INTEREST_EXP, INTEREST_EXP, True),
        Account(OTHER_INCOME, OTHER_INCOME, False),
        Account(DRAWINGS, EQUITY, True)

    ] + [

        Account(item, CURRENT_LIABILITY, False)
        for item in [AP, SHORT_TERM_LOANS, NOTES_PAYABLE]
    ] + [

        Account(item, CONTRA_REVENUE, True)
        for item in [SALES_DISCOUNTS, SALES_RETURNS]        
    ] + [

        Account(item, OPERATING_EXPENSE, True)
        for item in [RENT, UTILITY, INSURANCE, 
                     ADVERTISING, DEPRECIATION_EXP, SALARIES, 
                     MISCELLANEOUS_EXP,BAD_DEBT_EXPENSE, SUPPLIES_EXPENSE]
    ] + [

        Account(item, EQUITY, False)
        for item in [OWNERS_EQUITY, RETAINED_EARNINGS, AOCI]
    ]


def get_account(name) -> Account:
    for acc in CHART:
        if acc.name == name:
            return acc
    return None


def show_chart():
    # for debugging purposes
    names = []
    types = []
    normal_side = []
    balance = []
    for acc in CHART:
        names.append(acc.name)
        types.append(acc.type)
        if acc.debit_increases:
            balance.append(acc.current_balanace())
            normal_side.append('debit')
        else:
            balance.append(acc.current_balanace() * -1)
            normal_side.append('credit')
    df = pd.DataFrame({
        'Name': names,
        'Type': types,
        'Normal': normal_side,
        'Balance': balance
    })
    print('Chart\n', df)

if __name__ == '__main__':
    show_chart()
