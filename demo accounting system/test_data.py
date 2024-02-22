import datetime as dt
import inventory, other_assets, equity, loans, expenses,sales
today = dt.date.today()
# from reports import income_statement

equity.invest_cash(today, 'beginning', 4000)
l1 = loans.take_loan(today, '', 'rutger', 1000, loans.SHORT)

inventory.buy_inventory_cash(today, 'bought', 2000, None, "covers", inventory.MERCH, 20, 100)
inventory.buy_inventory_cash(today, 'bought', 1000, None, 'earphones', inventory.MERCH, 2, 500)
inventory.buy_inventory_cash(today, 'printing paper', 50, None, 'paper', inventory.SUPPLY, 100, 0.5)

f = other_assets.FixedAsset(today, 'stamper', 1, 100, 1.5)
expenses.rent_expense(today, 'paid', 300)

inventory.sale_inventory_cash(today + dt.timedelta(5), 'sold 1 earphone', 650, None, 'earphones', 1)

inventory.sale_inventory_cash(today + dt.timedelta(7), 'sold', 5*150, None, 'covers', 5)
inventory.use_inventory(today+dt.timedelta(7), 'used for receipt', 'paper', 2)

inventory.sale_inventory_credit(today + dt.timedelta(20), '', 700, sales.CustomerInfo('jake', '0956'), 'earphones', 1)

inventory.sale_inventory_cash(today +dt.timedelta(24), '', 10*145, None, 'covers', 10)

loans.pay_interest(today + dt.timedelta(25), 'paid back jake',l1.id, 100)

other_assets.exchange_asset(today + dt.timedelta(200), 'found better stamper', f.id, 'green stamper', 1, 75,-15, 1.5)
equity.use_cash_personally(today + dt.timedelta(50), 'for me', 100)
inventory.use_personally(today + dt.timedelta(50), 'for me', 'covers', 1)
inventory.use_personally(today + dt.timedelta(50), 'for me', 'paper', 10)


# print(Transaction.get_all_transactions())
# chart.show_chart()