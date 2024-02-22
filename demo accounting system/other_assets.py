import pandas as pd
import datetime as dt
import chart
from transactions import Transaction, NameAmountTuple


class FixedAsset:
    all_assets = []
    asset_id = 0
    def __init__(self, date:dt, name:str, quantity:float, cost:float, usage_years:float) -> None:
        self.purchase_date = date
        self.name = name
        self.quantity = quantity
        self.cost = cost
        # self.total_value = quantity * cost
        self.id = FixedAsset.asset_id
        self.usage_years = usage_years
        self.usage_rate = quantity * cost / usage_years #annual depreciation rate
        self.transactions:list[Transaction] = []
        FixedAsset.asset_id += 1

        FixedAsset.all_assets.append(self)
    

    def get_total_value(self):
        return self.quantity * self.cost
    
    
    def get_book_value(self) -> float:
        return self.get_total_value() - self.get_accumulate_dep()
    

    def get_accumulate_dep(self) -> float:
        acc_dep = 0
        for t in self.transactions:
            for c in t.credits:
                if c.name == chart.ACCUMULATED_DEP or c.name == chart.EQUIPMENT:
                    acc_dep += c.amount
            
            for d in t.debits:
                if d.name == chart.ACCUMULATED_DEP:
                    acc_dep -= c.amount

        return acc_dep
    

    @classmethod
    def get_asset_by_id(cls, asset_id):
        asset:FixedAsset = None
        for a in FixedAsset.all_assets:
            if a.id == asset_id:
                asset = a
                break
        if asset == None:
            raise Exception(f'No asset with id {asset_id}')
        
        return asset
    

    @classmethod
    def get_all_assets(cls):
        assets = []
        for a in FixedAsset.all_assets:
            if a.get_book_value() > 0:
                assets.append(a)        
        return assets


    @classmethod
    def table_form_multiple(cls):
        assets = cls.get_all_assets()
        names = []
        quantity = []
        cost = []
        total = []
        ids = []
        usage = []
        dates = []

        for a in assets:
            dates.append(a.purchase_date)
            names.append(a.name)
            quantity.append(a.quantity)
            cost.append(a.cost)
            total.append(a.cost * a.quantity)
            ids.append(a.id)
            usage.append(a.usage_years)

        return pd.DataFrame(
            {
                'Date': dates,
                'ID': ids,
                'Name': names,
                'Quantity': quantity,
                'Cost': cost,
                'Total': total,
                'Life': usage,
            }
        )


    def __repr__(self):
        return f'Asset name-{self.name}\nTotal value-{self.get_total_value()}\nAcc Dep-{self.get_accumulate_dep()}\nBook Value-{self.get_book_value()}'


    def __str__(self) -> str:
        return self.__repr__()



def depreciate(asset_id, date:dt):
    asset:FixedAsset = FixedAsset.get_asset_by_id(asset_id)
    
    diff = date - asset.purchase_date
    years = diff.days/365
    total_dep = years * asset.usage_rate

    dep_diff = total_dep - asset.get_accumulate_dep()
    if dep_diff >= 0:
        print('Dep difference is- ', dep_diff)
        t = Transaction(date, f'Depreciation-{asset.name}', [NameAmountTuple(chart.DEPRECIATION_EXP, dep_diff)], [NameAmountTuple(chart.ACCUMULATED_DEP, dep_diff)])

        asset.transactions.append(t)


def buy_asset(date:dt, note:str, name:str, quantity:float, cost:float, usage_years:float) -> FixedAsset:
    f = FixedAsset(date, name, quantity, cost,usage_years)
    t = Transaction(date, note, [NameAmountTuple(chart.EQUIPMENT, f.get_total_value())], [NameAmountTuple(chart.CASH, f.get_total_value())])
    
    f.transactions.append(t)

    return f


def dispose_asset(date:dt, note:str, amount_taken:float, asset_id:float):
    asset = FixedAsset.get_asset_by_id(asset_id)
    
    depreciate(asset_id, date)
    diff = amount_taken - asset.get_book_value()
    cash_received = amount_taken
    loss = 0
    gain = 0

    if diff > 0:
        gain = diff
        loss = 0
    elif diff < 0:
        gain = 0
        loss = -1*diff
    
    t = Transaction(
        date, note,
        [
            NameAmountTuple(chart.LOSS_ON_DISPOSAL, loss),
            NameAmountTuple(chart.CASH, cash_received),
            NameAmountTuple(chart.ACCUMULATED_DEP, asset.get_accumulate_dep())
        ],
        [
            NameAmountTuple(chart.EQUIPMENT, asset.get_total_value()),
            NameAmountTuple(chart.GAIN_ON_DISPOSAL, gain)
        ]
    )
    asset.quantity = 0
    asset.transactions.append(t)


def exchange_asset(date:dt, note:str, old_asset_id:int, new_asset_name:str, new_asset_quantity:float, new_asset_cost:float, cash_taken: float, new_asset_usage:float):

    old_asset: FixedAsset = FixedAsset.get_asset_by_id(old_asset_id)
    depreciate(old_asset_id, date)

    new_asset_total = new_asset_quantity * new_asset_cost
    cash_given = -1*cash_taken if cash_taken < 0 else 0
    
    cash_taken = cash_taken if cash_taken > 0 else 0

    total_consideration_given = old_asset.get_book_value() + cash_given
    total_consideration_taken = new_asset_total + cash_taken

    diff = total_consideration_given - total_consideration_taken

    loss = diff if diff > 0 else 0
    gain = -1 * diff if diff < 0 else 0

    t = Transaction(
        date, note,
        [
            NameAmountTuple(chart.EQUIPMENT, new_asset_total),
            NameAmountTuple(chart.ACCUMULATED_DEP, old_asset.get_accumulate_dep()),
            NameAmountTuple(chart.LOSS_ON_DISPOSAL, loss),
            NameAmountTuple(chart.CASH, cash_taken),
        ],
        [
            NameAmountTuple(chart.EQUIPMENT, old_asset.get_total_value()),
            NameAmountTuple(chart.CASH, cash_given),
            NameAmountTuple(chart.GAIN_ON_DISPOSAL, gain)
        ]
    )

    old_asset.transactions.append(t)
    old_asset.quantity = 0
    asset_new = FixedAsset(date, new_asset_name, new_asset_quantity, new_asset_cost, new_asset_usage)
    # asset_new.transactions.append(t)
    return asset_new


def use_asset_personally(date: dt, note:str, asset_id:int, quantity:float):
    asset: FixedAsset = FixedAsset.get_asset_by_id(asset_id)
    depreciate(asset_id, date)
    taken_out_value = quantity * asset.cost
    dep = asset.get_accumulate_dep() / quantity
    book_value = taken_out_value - dep
    t = Transaction(
        date, note, 
        [
            NameAmountTuple(chart.ACCUMULATED_DEP, dep),
            NameAmountTuple(chart.DRAWINGS, book_value)
        ],
        [
            NameAmountTuple(chart.EQUIPMENT, taken_out_value)
        ]
    )
    asset.quantity -= quantity
    asset.transactions.append(t)
    # depreciate(asset_id, date)


def invest_equipment(date:dt, note:str, name:str, quantity:float, cost:float, usage_years:float):
    f = FixedAsset(date, name, quantity, cost, usage_years)
    t = Transaction(
        date, note, 
        [NameAmountTuple(chart.EQUIPMENT, quantity * cost)],
        [NameAmountTuple(chart.OWNERS_EQUITY, quantity * cost)]
    )
    f.transactions.append(t)
    return f


if __name__ == '__main__':
    today = dt.date.today()
    Transaction(today, 'cash setup', [NameAmountTuple(chart.CASH, 4000)],[NameAmountTuple(chart.OWNERS_EQUITY, 4000)])    
    f = buy_asset(today, '', 'spoons', 12, 10,5)
    # dispose_asset(today + dt.timedelta(365), 'sold', 100, f.id)
    f2 = exchange_asset(today + dt.timedelta(365), 'bigger spoons', f.id, 'bigger spoons', 5, 20, 10, 5)
    use_asset_personally(today + dt.timedelta(385), 'for me', f2.id, 1)
    print(FixedAsset.get_all_assets())
    print(Transaction.get_all_transactions())
    chart.show_chart()
