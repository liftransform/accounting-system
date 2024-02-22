import chart
import datetime
import pandas as pd

ALL_ACCOUNT_NAMES = [acc.name for acc in chart.CHART]


class NameAmountTuple:
    def __init__(self, name, amount) -> None:
        self.name = name
        self.amount = amount
    

class Transaction:
    all_transactions = []
    id = 0
    def __init__(self, date, note, debits: list[NameAmountTuple], credits: list[NameAmountTuple]) -> None:

        self.is_tranaction_legal(debits, credits)

        self.date = date
        self.note = note
        self.debits:list[NameAmountTuple] = debits
        self.credits:list[NameAmountTuple] = credits
        self.id = Transaction.id
        Transaction.id += 1

        for acc in debits:
            chart_acc = chart.get_account(acc.name)
            chart_acc.debit(date,acc.amount, note)
        
        for acc in credits:
            chart_acc = chart.get_account(acc.name)
            chart_acc.credit(date, acc.amount, note)
        
        Transaction.all_transactions.append(self)

    @classmethod
    def delete_transaction(cls, transaction_id):
        # you shouldn't be able to delete a transaction. For the purpose of audit trail but this will just reverse the transaction with a note that says "delete"

        transaction:cls = None
        for t in cls.all_transactions:
            if t.id == transaction_id:
                transaction = t
                break
        new_transaction = cls(datetime.datetime.now(), 'deleted transaction', transaction.credits, transaction.debits) 

        return new_transaction

    @classmethod
    def is_tranaction_legal(cls, debits:list[NameAmountTuple], credits:list[NameAmountTuple]) -> None:
        #-----making sure all of the accounts are present

        for acc in debits + credits:
            if acc.name not in ALL_ACCOUNT_NAMES:
                raise ValueError(f'Account {acc.name} is not present in the Chart of accounts')
        
        #------check balance
        total_debit = sum([d.amount for d in debits])
        total_credit = sum([c.amount for c in credits])
        if total_credit != total_debit:
            raise Exception(f'Total debits {total_debit} and total credits {total_credit} do not match')

    @classmethod
    def table_form(cls, transaction):
        debit_names = []
        credit_names = []
        debit_amounts = []
        credit_amounts = []

        for d in transaction.debits:
            debit_amounts.append(f'{d.amount:.2f}')
            debit_names.append(d.name)
            credit_names.append('')
            credit_amounts.append('')

        for c in transaction.credits:
            credit_amounts.append(f'{c.amount:.2f}')
            credit_names.append(c.name)
            debit_names.append('')
            debit_amounts.append('')
        
        return pd.DataFrame({
            # 'Date': [transaction.date] + [''] * (len(debit_names) - 1),
            'Date': [transaction.date] * (len(debit_names)),
            'ID': [transaction.id] + [''] * (len(debit_names) - 1),
            'Dr. ACC.': debit_names,
            'Cr. Acc.': credit_names,
            'Dr.': debit_amounts,
            'Cr.': credit_amounts,
            'Note': [transaction.note] + [''] * (len(debit_names) - 1),
        })

    @classmethod
    def table_form_multiple(cls, ts:list):
        if len(ts) == 0:
            return None
        return pd.concat([Transaction.table_form(item) for item in ts]).reset_index().drop(columns='index')
    
    @classmethod
    def get_all_transactions(cls):
        return cls.table_form_multiple(Transaction.all_transactions)

    @classmethod
    def get_transactions_for_account(cls, name:str):
        ts = []
        for t in Transaction.all_transactions:
            for d in t.debits:
                if d.name == name:
                    ts.append(t)
            
            for c in t.credits:
                if c.name == name:
                    ts.append(t)
        
        return ts

    def __str__(self) -> pd.DataFrame:
        return str(Transaction.table_form(self))


if __name__ == '__main__':
    Transaction(datetime.datetime.now(), 'sold phone', [NameAmountTuple(chart.CASH, 3000)], [NameAmountTuple(chart.SALES,3000)])
    t2 = Transaction(datetime.datetime.now(), 'sold phone', [NameAmountTuple(chart.AR, 2000)], [NameAmountTuple(chart.SALES, 2000)])
        
    Transaction.delete_transaction(t2.id)

    print(Transaction.get_all_transactions())

    chart.show_chart()
    
    

