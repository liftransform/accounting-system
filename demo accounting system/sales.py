from transactions import Transaction, NameAmountTuple
import chart
import pandas as pd
import datetime as dt

#TODO: keep track of customer information here

class CustomerInfo:
    all_customers:list = []
    def __init__(self, name, phone) -> None:
        self.tranactions:list[Transaction] = []
        self.name = name
        self.phone = phone
        found_customer = False

        for cus in CustomerInfo.all_customers:
            if cus.name == self.name:
                found_customer = True
        
        if not found_customer:
            CustomerInfo.all_customers.append(self)
    
    def unpaid_amount(self) -> float:
        balance = 0
        for t in self.tranactions:
            for d in t.debits:
                if d.name == chart.AR:
                    balance += d.amount
            for c in t.credits:
                if c.name == chart.AR:
                    balance -= d.amount

        return balance

    def add_transaction(self, t: Transaction):
        for trans in self.tranactions:
            if trans.id == t.id:
                raise ValueError('Transaction already exists.')
            
        self.tranactions.append(t)
    
    @classmethod
    def get_customer(cls, cus_info):
        if cus_info == None:
            return None
        
        for cus in cls.all_customers:
            if cus.name == cus_info.name:
                return cus
        return None


    @classmethod
    def table_form_multiple(cls):
        cus = cls.customers_with_upaid_balances()
        names = []
        phones = []
        balances = []
        for c in cus:
            names.append(c.name)
            phones.append(c.phone)
            balances.append(c.unpaid_amount())
        
        return pd.DataFrame({
            'name': names,
            'phone': phones,
            'balance': balances
        })
    

    @classmethod
    def all_transactions(cls):
        return pd.concat([t.table_form() for cus in cls.all_customers for t in cus.transactions]).reset_index().drop(columns='index')


    @classmethod
    def customers_with_upaid_balances(cls) -> list:
        customers = []
        for cus in CustomerInfo.all_customers:
            if cus.unpaid_amount() > 0:
                customers.append(cus)
        
        return customers

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f'Customer: Name-{self.name}\nPhone-{self.phone}\nBalance-{self.unpaid_amount()}'

def record_cash_sales(date:dt, note:str, amount:float, info:CustomerInfo = None):
    cus = CustomerInfo.get_customer(info)
    t = Transaction(date, note,[NameAmountTuple(chart.CASH, amount)], [NameAmountTuple(chart.SALES, amount)])

    if cus != None:
        cus.add_transaction(t)


def record_credit_sales(date:dt, note:str, amount:float, info:CustomerInfo):
    if info == None:
        raise ValueError('Customer info can not be none')
    
    cus = CustomerInfo.get_customer(info)
    t = Transaction(date, note, [NameAmountTuple(chart.AR, amount)], [NameAmountTuple(chart.SALES, amount)])

    if cus != None:
        cus.add_transaction(t)


def collect_on_credit_sales(date:dt, note:str, amount:float, info:CustomerInfo):
    if info == None:
        raise ValueError('Customer info can not be none')
    
    cus = CustomerInfo.get_customer(info)
    t = Transaction(date, note, [NameAmountTuple(chart.CASH, amount)], [NameAmountTuple(chart.AR, amount)])
    
    if cus != None:
        cus.add_transaction(t)


def estimate_uncollectible_amount(date: dt, note: str, amount: float, info:CustomerInfo):
    if info == None:
        raise ValueError('Customer info can not be none')
    
    cus = CustomerInfo.get_customer(info)
    t = Transaction(date, note, [NameAmountTuple(chart.BAD_DEBT_EXPENSE, amount)], [NameAmountTuple(chart.ALLOWANCE_FOR_DOUBTFUL_ACCOUNTS, amount)])
    
    if cus != None:
        cus.add_transaction(t)


def collect_uncollectible(date: dt, amount: float, note: str, info: CustomerInfo):
    #TODO: implemnet
    pass


def give_discounts(date: dt, amount:float, note: str, info:CustomerInfo):
    #TODO: implemnet
    pass


def take_returns(date:dt, amount:float, note:str, info: CustomerInfo):
    #TODO: implemnet
    pass


def get_all_sales_transactions():
    ts = []
    for t in Transaction.all_transactions:
        for d in t.debits:
            if d.name == chart.SALES:
                ts.append(t)
        
        for c in t.credits:
            if c.name == chart.SALES:
                ts.append(t)

    return ts

if __name__ == '__main__':
    #Testing the functions here
    abel = CustomerInfo('Abel', '0979064604')
    seble = CustomerInfo('Seble', '0949064604')
    record_cash_sales(dt.date.today(), 'cash customer', 3000)
    record_credit_sales(dt.date.today(), 'sold cover', 100, abel)
    record_credit_sales(dt.date.today(), 'sold cabel', 400, abel)
    record_credit_sales(dt.date.today(), 'sold cover', 150, seble)
    print(CustomerInfo.customers_with_upaid_balances())
    
    collect_on_credit_sales(dt.date.today() + dt.timedelta(1), 'collected on cover', 100, abel)
    estimate_uncollectible_amount(dt.date.today() + dt.timedelta(5), 'she aint paying', 150,seble)
    print()
    print(CustomerInfo.customers_with_upaid_balances())

    Transaction(dt.date.today(), 'bought pan', [NameAmountTuple(chart.EQUIPMENT, 10000)], [NameAmountTuple(chart.CASH, 10000)])

    print(Transaction.get_all_transactions())
    print('-----------')
    print(Transaction.table_form_multiple(get_all_sales_transactions()))