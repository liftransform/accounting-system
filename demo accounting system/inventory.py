import pandas as pd
import datetime as dt
from transactions import Transaction, NameAmountTuple
import chart
import time
import sales

#-----Inventory types
MERCH='merch'
SUPPLY='supply'
#-----

class VendorInfo:
    all_vendors = []
    def __init__(self, name, phone) -> None:
        self.tranactions:list[Transaction] = []
        self.name = name
        self.phone = phone
        found_vendor = False

        for ven in VendorInfo.all_vendors:
            if ven.name == self.name:
                found_vendor = True
        
        if not found_vendor:
            VendorInfo.all_vendors.append(self)
    
    def unreceived_amount(self) -> float:
        balance = 0
        for t in self.tranactions:
            for d in t.debits:
                if d.name == chart.AP:
                    balance -= d.amount
            for c in t.credits:
                if c.name == chart.AP:
                    balance += d.amount

        return balance

    def add_transaction(self, t: Transaction):
        for trans in self.tranactions:
            if trans.id == t.id:
                raise ValueError('Transaction already exists.')
            
        self.tranactions.append(t)
    
    @classmethod
    def get_vendor(cls, ven_info):
        if  ven_info == None:
            return None
        
        for ven in cls.all_vendors:
            if ven.name == ven_info.name:
                return ven
        return None

    @classmethod
    def all_transactions(cls):
        return pd.concat([t.table_form() for ven in cls.all_vendors for t in ven.transactions]).reset_index().drop(columns='index')


    @classmethod
    def vendors_with_upaid_balances(cls) -> list:
        vendors = []
        for ven in VendorInfo.all_vendors:
            if ven.unreceived_amount() > 0:
                vendors.append(ven)
        
        return vendors

    @classmethod
    def table_form_multiple(cls):
        names = []
        phones = []
        balances = []
        for ven in cls.vendors_with_upaid_balances():
            names.append(ven.name)
            phones.append(ven.phone)
            balances.append(ven.unreceived_amount())
        
        return pd.DataFrame({
            'Name': names,
            'Phone': phones,
            'Unpaid Amount': balances
        })

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f'Vendor: Name-{self.name}\nPhone-{self.phone}\nBalance-{self.unreceived_amount()}'

class Inventory:
    all_inventory = []
    inv_id:int = 0

    def __init__(self, date_bought: dt, name:str, description:str, vendor_info: VendorInfo, quantity:float, cost:float, inv_type=MERCH) -> None:
        self.name = name
        self.description = description
        self.vendor_info = vendor_info
        self.quantity = quantity 
        self.cost = cost
        self.inv_type = inv_type
        self.id = Inventory.inv_id
        self.date = date_bought
        Inventory.inv_id += 1

        Inventory.all_inventory.append(self)

    @classmethod
    def get_all_items(cls, name='') -> list:
        if name == '':
            items = []
            for inv in cls.all_inventory:
                if inv.quantity != 0:
                    items.append(inv)
            return items
        
        items = []
        for inv in cls.all_inventory:
            if inv.name == name: #and inv.quantity != 0:
                items.append(inv)
        return items


    def table_form(self):
        ven_name = ''
        if self.vendor_info != None: ven_name = self.vendor_info.name
        return pd.DataFrame({
            'ID': [self.id],
            'Date': [self.date],
            'Name': [self.name],
            'Cost': [self.cost],
            'Quantity': [self.quantity],
            'Total Value': [self.cost * self.quantity],
            'Vendor': [ven_name],
            'Description': [self.description]
        })

    @classmethod
    def get_inv_by_id(cls, id):
        for inv in Inventory.all_inventory:
            if inv.id == id:
                return inv
        raise ValueError(f'No inventory with id {id}')
    

    @classmethod
    def table_form_multiple(cls, invs:list):
        return pd.concat([inv.table_form() for inv in invs]).reset_index().drop(columns='index')

    @classmethod
    def get_inv_type(cls, name:str):
        inv_type = None
        for inv in Inventory.all_inventory:
            if inv.name == name:
                inv_type = inv.inv_type
                break
        return inv_type

    @classmethod
    def use_inventory(cls, name: str, quantity:float):
        total = quantity
        invs_table = cls.table_form_multiple(cls.get_all_items(name))
        invs_table = invs_table.sort_values(by='Date').reset_index().drop(columns='index')
        
        for i, row in invs_table.iterrows():
            if total == 0:
                break
            inv_id = row[0]
            inv:cls = cls.get_inv_by_id(inv_id)
            if total > inv.quantity:
                total -= inv.quantity
                inv.quantity = 0
            else:
                inv.quantity -= total
                total = 0
    
    @classmethod
    def summarize_inventory(cls):
        table = cls.table_form_multiple(Inventory.all_inventory)
        summ = table[['Name', 'Total Value']].groupby(by='Name').sum().reset_index()
        return summ

    @classmethod
    def get_value_for_inv(cls, name:str) -> float:
        invs_table:pd.DataFrame = cls.table_form_multiple(cls.get_all_items(name))
        return invs_table['Total Value'].sum()

def _record_cash_expense(date: dt, note: str, amount: float, info:VendorInfo, expense_type):
    ven = VendorInfo.get_vendor(info)
    t = Transaction(date, note, [NameAmountTuple(expense_type, amount)], [NameAmountTuple(chart.CASH, amount)])

    if ven != None:
        ven.add_transaction(t)


def buy_inventory_cash(date:dt, note: str, amount:float, info:VendorInfo, inv_name:str, inv_type, quantity:float, cost:float):

    debit_account = None
    if inv_type == MERCH:
        debit_account = chart.MERCH_INVENTORY
    else:
        debit_account = chart.SUPPLIES

    _record_cash_expense(date, note, amount, info, debit_account)
    Inventory(date, inv_name,note,info, quantity, cost, inv_type)


def buy_inventory_credit(date, note, amount, info, inv_name, inv_type, quantity, cost):
    if info == None:
        raise ValueError('Vendor information cannot be none.')
    
    ven:VendorInfo = VendorInfo.get_vendor(info)

    debit_account = None
    if inv_type == MERCH:
        debit_account = chart.MERCH_INVENTORY
    else:
        debit_account = chart.SUPPLIES

    t = Transaction(date, note, [NameAmountTuple(debit_account, amount)], [NameAmountTuple(chart.AP, amount)])

    ven.add_transaction(t)

    Inventory(date, inv_name, note, info, quantity, cost, inv_type)


def sale_inventory_cash(date:dt, note:str, amount:float, cus_info:sales.CustomerInfo, inv_name:str, quantity:float):
    # we are supposed to record an income and COGS here
    inv_type = Inventory.get_inv_type(inv_name)
    sales.record_cash_sales(date, note, amount, cus_info)
    before = Inventory.get_value_for_inv(inv_name)
    Inventory.use_inventory(inv_name, quantity)
    after = Inventory.get_value_for_inv(inv_name)
    used_amount = before - after

    credit_acc = None
    if inv_type == MERCH:
        credit_acc = chart.MERCH_INVENTORY
    elif inv_type == SUPPLY:
        credit_acc = chart.SUPPLIES

    Transaction(date, note, [NameAmountTuple(chart.COGS, used_amount)], [NameAmountTuple(credit_acc, used_amount)])


def sale_inventory_credit(date:dt, note:str, amount:float, cus_info:sales.CustomerInfo, inv_name:str, quantity:float):
    inv_type = Inventory.get_inv_type(inv_name)
    sales.record_credit_sales(date, note, amount, cus_info)
    before = Inventory.get_value_for_inv(inv_name)
    Inventory.use_inventory(inv_name, quantity)
    after = Inventory.get_value_for_inv(inv_name)
    used_amount = before - after

    credit_acc = None
    if inv_type == MERCH:
        credit_acc = chart.MERCH_INVENTORY
    elif inv_type == SUPPLY:
        credit_acc = chart.SUPPLIES

    Transaction(date, note, [NameAmountTuple(chart.COGS, used_amount)], [NameAmountTuple(credit_acc, used_amount)])


def use_inventory(date:dt, note:str, inv_name:str, quantity: float):
    inv_type = Inventory.get_inv_type(inv_name)
    
    credit_acc = None
    if inv_type == MERCH:
        credit_acc = chart.MERCH_INVENTORY
    elif inv_type == SUPPLY:
        credit_acc = chart.SUPPLIES

    before = Inventory.get_value_for_inv(inv_name)
    Inventory.use_inventory(inv_name, quantity)
    after = Inventory.get_value_for_inv(inv_name)

    used_amount:float = before - after
    Transaction(date, note, [NameAmountTuple(chart.SUPPLIES_EXPENSE, used_amount)], [NameAmountTuple(credit_acc, used_amount)])


def use_personally(date:dt, note:str, inv_name:str, quantity:float):
    inv_type = Inventory.get_inv_type(inv_name)
    
    credit_acc = None
    if inv_type == MERCH:
        credit_acc = chart.MERCH_INVENTORY
    elif inv_type == SUPPLY:
        credit_acc = chart.SUPPLIES

    before = Inventory.get_value_for_inv(inv_name)
    Inventory.use_inventory(inv_name, quantity)
    after = Inventory.get_value_for_inv(inv_name)

    used_amount:float = before-after
    Transaction(date, note, [NameAmountTuple(chart.DRAWINGS, used_amount)], [NameAmountTuple(credit_acc, used_amount)])


def pay_vendor(date: dt, note:str, ven_info:VendorInfo, amount: float):
    ven = None
    for v in VendorInfo.all_vendors:
        if ven_info.name == v.name and v.unreceived_amount() > 0:
            ven = v
            break
    
    if ven == None:
        raise ValueError(f'No Vender named {ven_info.name} with amounts owed')
    
    t = Transaction(date,note,[NameAmountTuple(chart.AP, amount)], [NameAmountTuple(chart.CASH, amount)])

    ven.add_transaction(t)


def invest_inventory(date, note, inv_name, inv_type, quantity, cost):
    debit_account = None
    if inv_type == MERCH:
        debit_account = chart.MERCH_INVENTORY
    else:
        debit_account = chart.SUPPLIES

    Inventory(date, inv_name, note, None, quantity, cost, inv_type)
    Transaction(
        date, note,
        [NameAmountTuple(debit_account, quantity * cost)],
        [NameAmountTuple(chart.OWNERS_EQUITY, quantity * cost)]
    )


if __name__ == '__main__':
    abel = VendorInfo('abel', '0956')
    seble = VendorInfo('seble', '0946')
    jedi = sales.CustomerInfo('jedi', '0978')

    # i2 = Inventory(dt.date.today(), 'MI', '', seble, 1, 22000, MERCH)
    # time.sleep(0.1)
    # i1 = Inventory(dt.date.today(), 'MI', '', abel, 3, 24000, MERCH)
    # i3 = Inventory(dt.date.today(), 'sony xperia', '', None, 2, 20000, MERCH)

    # print('Original\n', Inventory.summarize_inventory())

    # Inventory.use_inventory('MI', 2)

    # print('Used 2 MIs\n', Inventory.summarize_inventory())
    # print('Details\n', Inventory.table_form_multiple(Inventory.get_all_items()))
    buy_inventory_cash(dt.date.today(), '', 400, abel, 'Mi', MERCH, 3, 200)
    buy_inventory_credit(dt.date.today(), '', 300, seble, 'XI', MERCH, 3, 100)
    print('All transaction\n', Transaction.get_all_transactions())
    print('Inventory\n', Inventory.table_form_multiple(Inventory.get_all_items()))
    pay_vendor(dt.date.today(), 'paid abel', seble, 200)
    sale_inventory_cash(dt.date.today(), 'cash cus', 420, None, 'Mi', 1)
    sale_inventory_credit(dt.date.today(), 'j', 300, jedi, 'XI', 2)
    sales.collect_on_credit_sales(dt.date.today(), 'coll j', 250, jedi)
    use_inventory(dt.date.today(), 'as spare part', 'XI', 1)
    use_personally(dt.date.today(), 'i like', 'Mi', 1)
    print('All transaction\n', Transaction.get_all_transactions())
    print('Vendors', VendorInfo.all_vendors)
    print('Customers', sales.CustomerInfo.all_customers)
    print('Inventory\n', Inventory.table_form_multiple(Inventory.get_all_items()))
    chart.show_chart()