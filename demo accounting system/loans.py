import chart
from transactions import Transaction, NameAmountTuple
import datetime as dt
import pandas as pd

SHORT = 'short term'
LONG = 'long term'

class Creditor:
    all_creditors = []
    loan_id = 0
    def __init__(self, name:str, amount:float, loan_type = SHORT) -> None:
        if loan_type not in [SHORT, LONG]:
            raise ValueError(f'Loan type can only be short term or long term not {loan_type}')
        self.name = name
        self.amount = amount
        self.transactions = []
        self.id = Creditor.loan_id
        self.loan_type = loan_type
        Creditor.loan_id += 1
        
        
        # self.loan_type = loan_type

        # found = False
        # for c in Creditor.all_creditors:
        #     if c.name == name:
        #         found = True
        #         break
        
        # if not found:
        Creditor.all_creditors.append(self)

    def unpaid_amount(self):
        balance = 0
        acc_name = None

        if self.loan_type == SHORT:
            acc_name = chart.NOTES_PAYABLE
        elif self.loan_type == LONG:
            acc_name = chart.DEBT
        
        for t in self.transactions:
            for d in t.debits:
                if d.name == acc_name:
                    balance -= d.amount
            for c in t.credits:
                if c.name == acc_name:
                    balance += d.amount

        return balance

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f'Creditor: Name-{self.name}\nAmount Borrowed-{self.amount}\nUnpaid Balance-{self.unpaid_amount()}'


    @classmethod
    def get_unpaid_loans(cls):
        creditors = []
        for c in Creditor.all_creditors:
            if c.unpaid_amount() > 0:
                creditors.append(c)
        
        return creditors

    @classmethod
    def table_form_multiple(cls):
        credits = cls.get_unpaid_loans()
        names = []
        amounts = []
        loan_types = []
        
        for c in credits:
            names.append(c.name)
            amounts.append(c.unpaid_amount())
            loan_types.append(c.loan_type)

        return pd.DataFrame(
            {
                'Lender': names,
                'Unpaid': amounts,
                'Loan Term': loan_types
            }
        )
    @classmethod
    def transaction_table_form(cls):
        return pd.concat([t.transaction_table_form() for c in cls.all_creditors for t in c.transactions]).reset_index().drop(columns='index')


class Borrower:
    all_loans = []
    loan_id = 0
    def __init__(self, name:str, amount:float, loan_type = SHORT) -> None:
        if loan_type not in [SHORT, LONG]:
            raise ValueError(f'Loan type can only be short term or long term not {loan_type}')
        
        self.name = name
        self.amount = amount
        self.transactions = []
        self.id = Borrower.loan_id
        Borrower.loan_id += 1
        
        self.loan_type = loan_type

        # found = False
        # for c in Borrower.all_loans:
        #     if c.name == name:
        #         found = True
        #         break
        
        # if not found:
        Borrower.all_loans.append(self)

    def unreceived_amount(self):
        balance = 0
        acc_name = None

        if self.loan_type == SHORT:
            acc_name = chart.NOTES_RECEIVABLE
        elif self.loan_type == LONG:
            acc_name = chart.DEBT_INVESTMENT
        
        for t in self.transactions:
            for d in t.debits:
                if d.name == acc_name:
                    balance += d.amount
            for c in t.credits:
                if c.name == acc_name:
                    balance -= d.amount

        return balance

    @classmethod
    def get_unreceieved_loans(cls):
        borrowers = []
        for b in Borrower.all_loans:
            if b.unreceived_amount() > 0:
                borrowers.append(b)
        
        return borrowers


    @classmethod
    def transaction_table_form(cls):
        return pd.concat([t.transaction_table_form() for b in cls.all_loans for t in b.transactions]).reset_index().drop(columns='index')

    @classmethod
    def table_form_multiple(cls):
        borrowers = cls.get_unreceieved_loans()
        names = []
        amounts = []
        loan_types = []
        
        for c in borrowers:
            names.append(c.name)
            amounts.append(c.unreceived_amount())
            loan_types.append(c.loan_type)

        return pd.DataFrame(
            {
                'Borrower': names,
                'Unpaid': amounts,
                'Loan Term': loan_types
            }
        )
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f'Borrower: Name-{self.name}\nAmount Lent-{self.amount}\nUnreceived Balance-{self.unreceived_amount()}'



def take_loan(date:dt, note:str, creditor_name:str, amount:float, loan_type:str) -> Creditor:
    c:Creditor = Creditor(creditor_name, amount, loan_type)

    credit_acc = None
    if loan_type == SHORT:
        credit_acc = chart.NOTES_PAYABLE
    elif loan_type == LONG:
        credit_acc = chart.DEBT

    t = Transaction(date, note, [NameAmountTuple(chart.CASH, amount)], [NameAmountTuple(credit_acc, amount)])

    c.transactions.append(t)
    return c


def pay_interest(date:dt, note:str, loan_id:float, amount:float):
    cre_info: Creditor = None
    for c in Creditor.all_creditors:
        if c.id == loan_id:
            cre_info = c
            break
    t = Transaction(date, note, [NameAmountTuple(chart.INTEREST_EXP, amount)], [NameAmountTuple(chart.CASH, amount)])
    cre_info.transactions.append(t)


def pay_principal(date:dt, note:str, loan_id:float, amount:float):
    cre_info:Creditor = None
    for c in Creditor.all_creditors:
        if c.id == loan_id:
            cre_info = c

    if cre_info == None:
        raise ValueError(f'Loan with id {loan_id} does not exist.')
    
    if cre_info.unpaid_amount() < amount:
        raise ValueError(f'You are trying to pay more than you owe. Amount owed-{cre_info.unpaid_amount()}. Trying to pay-{amount}')
    
    debit_acc = None
    if cre_info.loan_type == SHORT:
        debit_acc = chart.NOTES_PAYABLE
    elif cre_info.loan_type == LONG:
        debit_acc = chart.DEBT

    t = Transaction(date, note, [NameAmountTuple(debit_acc, amount)], [NameAmountTuple(chart.CASH, amount)])

    cre_info.transactions.append(t)


def give_loan(date: dt, note:str, borrower_name:str, amount:float, loan_type: str) -> Borrower:
    b:Borrower = Borrower(borrower_name, amount, loan_type)

    debit_acc = None
    if loan_type == SHORT:
        debit_acc = chart.NOTES_RECEIVABLE
    elif loan_type == LONG:
        debit_acc = chart.DEBT_INVESTMENT

    t = Transaction(date, note, [NameAmountTuple(debit_acc, amount)], [NameAmountTuple(chart.CASH, amount)])

    b.transactions.append(t)

    return b

def get_interest(date:dt, note:str, loan_id:float, amount:float):
    borr_info: Borrower = None
    for b in Borrower.all_loans:
        if b.id == loan_id:
            borr_info = b
            break

    t = Transaction(date, note, [NameAmountTuple(chart.CASH, amount)], [NameAmountTuple(chart.INTEREST_INCOME, amount)])

    borr_info.transactions.append(t)


def get_principal(date:dt, note:str, loan_id:float, amount:float):
    borr_info:Borrower = None
    for b in Borrower.all_loans:
        if b.id == loan_id:
            borr_info = b

    if borr_info == None:
        raise ValueError(f'Loan with id {loan_id} does not exist.')
    
    if borr_info.unreceived_amount() < amount:
        raise ValueError(f'You are trying to receive more than you are owed. Amount owed-{borr_info.unreceived_amount()}. Trying to receive-{amount}')
    
    credit_acc = None
    if borr_info.loan_type == SHORT:
        credit_acc = chart.NOTES_RECEIVABLE
    elif borr_info.loan_type == LONG:
        credit_acc = chart.DEBT_INVESTMENT

    t = Transaction(date, note, [NameAmountTuple(chart.CASH, amount)], [NameAmountTuple(credit_acc, amount)])

    borr_info.transactions.append(t)



if __name__ == '__main__':
    l1 = take_loan(dt.date.today(), 'nganu borrowings', 'Nganu', 4000, SHORT)
    l2 = take_loan(dt.date.today(), 'nganu borrowings', 'Nganu', 1000, SHORT)
    pay_interest(dt.date.today(), 'interest-n', l1.id, 20)
    pay_principal(dt.date.today(), 'paid-prin', l1.id, 1000)

    l3 = give_loan(dt.date.today(), 'f need it', 'franny', 2000, SHORT)
    get_interest(dt.date.today(), 'int', l3.id, 100)
    get_principal(dt.date.today(), 'got it back', l3.id, 1500)
    get_principal(dt.date.today(), 'got it back', l3.id, 500)
    print(Transaction.get_all_transactions())
    print(Borrower.get_unreceieved_loans())
    print(Creditor.get_unpaid_loans())