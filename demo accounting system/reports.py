from transactions import Transaction, NameAmountTuple
import datetime as dt
import chart
import pandas as pd
from other_assets import FixedAsset, depreciate

income_total = None
equity_total = None
retained_earnings = None
acc_oci = None

def format_number(num):
    if num > 0:
        return f"{num:.2f} "
    
    if num < 0:
        return f"({-1*num:.2f})"
    
    return ''


def income_statement(date:dt.date) -> pd.DataFrame:
    global income_total
    # you have to depreciate all_assets
    for f in FixedAsset.all_assets:
        depreciate(f.id, date)
    
    sales = chart.get_account(chart.SALES).current_balanace()
    discounts = chart.get_account(chart.SALES_DISCOUNTS).current_balanace()
    returns = chart.get_account(chart.SALES_RETURNS).current_balanace()
    net_sales = sales-discounts-returns
    
    cogs = chart.get_account(chart.COGS).current_balanace()
    
    gross_profit = net_sales - cogs

    rent = chart.get_account(chart.RENT).current_balanace()
    utility = chart.get_account(chart.UTILITY).current_balanace()
    insurance = chart.get_account(chart.INSURANCE).current_balanace()
    advertising = chart.get_account(chart.ADVERTISING).current_balanace()
    dep = chart.get_account(chart.DEPRECIATION_EXP).current_balanace()
    salaries = chart.get_account(chart.SALARIES).current_balanace()
    supplies_exp = chart.get_account(chart.SUPPLIES_EXPENSE).current_balanace()

    total_opearting_exp = sum(
        [
            rent, utility, insurance, advertising,
            dep, salaries, supplies_exp
        ]
    )

    opearting_income = gross_profit - total_opearting_exp

    interest_exp = chart.get_account(chart.INTEREST_EXP).current_balanace()
    interest_rev = chart.get_account(chart.INTEREST_INCOME).current_balanace()

    net_income = opearting_income - interest_exp + interest_rev

    non_opearting_inc_exp = sum([
        # chart.get_account(chart.INTEREST_INCOME).current_balanace(),
        -1*chart.get_account(chart.OTHER_EXPENSE).current_balanace(),
        chart.get_account(chart.OTHER_INCOME).current_balanace(),
        chart.get_account(chart.GAIN_ON_DISPOSAL).current_balanace(),
        -1*chart.get_account(chart.LOSS_ON_DISPOSAL).current_balanace()
    ]
    )
    
    total = net_income + non_opearting_inc_exp

    table = pd.DataFrame(
        [
            [name.capitalize(), format_number(num)]
            for (name, num) in [
                (chart.SALES, sales), (chart.SALES_DISCOUNTS, -discounts),
                (chart.SALES_RETURNS, -returns), ('Net Sales', net_sales),
                (chart.COGS, -cogs), ('Gross Profit', gross_profit),
                (chart.OPERATING_EXPENSE, 0),
                (chart.RENT, -rent), (chart.SUPPLIES_EXPENSE, -supplies_exp),
                (chart.UTILITY, utility), (chart.INSURANCE, -insurance),
                (chart.ADVERTISING, -advertising), (chart.DEPRECIATION_EXP, -dep),
                (chart.SALARIES, -salaries), ('Total operating Expense', -total_opearting_exp),
                ('Operating Income', opearting_income), (chart.INTEREST_EXP, -interest_exp), (chart.INTEREST_INCOME, interest_rev),
                ('Net Income', net_income), ('Other Income and Expenses', non_opearting_inc_exp), ('Total', total)
                ]
        ],
        columns=['Account', 'Balance']
    )

    # return table[table['Balance'] != ''].reset_index().drop(columns='index')
    income_total = net_income
    return table


def statement_of_retained_earnings(date:dt.date):
    global retained_earnings
    if income_total == None:
        income_statement(date)
    
    all_retained_earnings = Transaction.get_transactions_for_account(chart.RETAINED_EARNINGS)

    all_re_table = Transaction.table_form_multiple(all_retained_earnings)

    beginning_balance = 0
    if type(all_re_table) != type(None):
        beginning_balance = all_re_table[all_re_table['Cr. Acc.'] != ''].sort_values(by='Date').iloc[0]['Cr.']
    

    net_income = income_total
    dividend = chart.get_account(chart.DRAWINGS).current_balanace()
    ending_balance = beginning_balance + net_income - dividend

    table = pd.DataFrame(
        [
            [name.capitalize(), format_number(amount)]
            for name, amount in [
                ('Beginning Retained Earnings', beginning_balance),
                ('Add: Net Income', net_income),
                ('Less: Drawings', dividend),
                ('Ending Retained Earnings', ending_balance)
            ]
        ],
        columns=['Account', 'Balance']
    )

    retained_earnings = ending_balance
    
    return table


def statement_of_owner_equity(date:dt.date):
    global equity_total, acc_oci
    if income_total == None:
        income_statement(date)
        
    all_equity_transactions = Transaction.get_transactions_for_account(chart.OWNERS_EQUITY)

    all_eq_table = Transaction.table_form_multiple(all_equity_transactions)
    print(all_eq_table)
    beginning_balance = 0
    if type(all_eq_table) != type(None):
        beginning_balance = all_eq_table[all_eq_table['Cr. Acc.'] != ''].sort_values(by='Date').iloc[0]['Cr.']
        # print('Beginning Balance', beginning_balance)
        beginning_balance = float(beginning_balance)
    
    investments = chart.get_account(chart.OWNERS_EQUITY).current_balanace() - beginning_balance
    net_income = income_total
    dividend = chart.get_account(chart.DRAWINGS).current_balanace()
    aoci = sum([
        # chart.get_account(chart.INTEREST_INCOME).current_balanace(),
        -1*chart.get_account(chart.OTHER_EXPENSE).current_balanace(),
        chart.get_account(chart.OTHER_INCOME).current_balanace(),
        chart.get_account(chart.GAIN_ON_DISPOSAL).current_balanace(),
        -1*chart.get_account(chart.LOSS_ON_DISPOSAL).current_balanace()
    ]
    )

    ending_balance = beginning_balance + investments + net_income - dividend + aoci

    table = pd.DataFrame(
        [
            [name.capitalize(), format_number(amount)]
            for name, amount in [
                ('Beginning Owners equity', beginning_balance),
                ('Add: Net Income', net_income),
                (f'Add: {chart.AOCI}', aoci),
                ('Less: Drawings', -1*dividend),
                ('Ending Balance', ending_balance)
            ]
        ],
        columns=['Account', 'Balance']
    )

    equity_total = ending_balance
    acc_oci = aoci

    return table


def statment_of_financial_position(date: dt.date):
    if equity_total == None:
        statement_of_retained_earnings(date)
        statement_of_owner_equity(date)

    cash = chart.get_account(chart.CASH).current_balanace()
    ar = chart.get_account(chart.AR).current_balanace()
    merch = chart.get_account(chart.MERCH_INVENTORY).current_balanace()
    allowance_ar = chart.get_account(chart.ALLOWANCE_FOR_DOUBTFUL_ACCOUNTS).current_balanace()
    raw_material = chart.get_account(chart.RAW_MATERIAL).current_balanace()
    supplies = chart.get_account(chart.SUPPLIES).current_balanace()
    notes_rec = chart.get_account(chart.NOTES_RECEIVABLE).current_balanace()

    equip = chart.get_account(chart.EQUIPMENT).current_balanace()
    acc_dep = chart.get_account(chart.ACCUMULATED_DEP).current_balanace()
    land = chart.get_account(chart.LAND).current_balanace()
    
    current_assets = sum([
        cash, ar, merch, -1*allowance_ar, raw_material,
        supplies, notes_rec,
    ])

    non_current_asset = sum([
        equip, -1*acc_dep, land
    ])

    total_assets = sum([
         current_assets, non_current_asset
    ])

    ap = chart.get_account(chart.AP).current_balanace()
    short = chart.get_account(chart.SHORT_TERM_LOANS).current_balanace()
    notes_pay = chart.get_account(chart.NOTES_PAYABLE).current_balanace()
    debt = chart.get_account(chart.DEBT).current_balanace()

    current_liabilities = ap + short + notes_pay

    non_current_liabilities = debt

    total_liability = current_liabilities + non_current_liabilities
    # return f'Total asset - {total_assets}\nLiability and equity - {current_liabilities + non_current_liabilities + equity_total}'


    table = pd.DataFrame(
        [
            [name.capitalize(), format_number(num)]
            for name, num in [
                ('Assets', 0),
                ('Current assets', 0),
                (chart.CASH, cash), (chart.AR, ar), 
                (chart.ALLOWANCE_FOR_DOUBTFUL_ACCOUNTS, -allowance_ar),
                (chart.MERCH_INVENTORY, merch),
                (chart.RAW_MATERIAL, raw_material), (chart.SUPPLIES, supplies),
                (chart.NOTES_RECEIVABLE, notes_rec), 
                ('Total Current Assets', current_assets),
                ('Non-Current Assets', 0),
                (chart.EQUIPMENT, equip),
                (chart.ACCUMULATED_DEP, acc_dep),
                (chart.LAND, land),
                ('Total Non-Current Assets', non_current_asset),
                ('Total Assets', total_assets),
                ("Liabilities", 0),
                ('Current Liabilities', 0),
                (chart.AP, ap),
                (chart.SHORT_TERM_LOANS, short),
                (chart.NOTES_PAYABLE, notes_pay),
                ('Total Current Liabilities', current_liabilities),
                ('Non Current Liabilties', 0),
                (chart.DEBT, debt),
                ('Total Non Current Liabilities', non_current_liabilities),
                ('Total Liabilities', total_liability),
                ('Equity', 0),
                (chart.OWNERS_EQUITY, equity_total - acc_oci - retained_earnings),
                (chart.RETAINED_EARNINGS, retained_earnings),
                (chart.AOCI, acc_oci),
                ('Total Equity', equity_total),
                ('Total Liabilities & Equity', equity_total + total_liability)
            ]
        ],
        columns=['Account', 'Balance']
    )

    return table


def statement_of_cash_flow():
    #TODO: implement
    pass



if __name__ == '__main__':
    import test_data
    today = test_data.today
    print(income_statement(dt.date.today() + dt.timedelta(365)))
    print()
    print(statement_of_retained_earnings(dt.date.today() + dt.timedelta(365)))
    print()
    print(statement_of_owner_equity(dt.date.today() + dt.timedelta(365)))
    print()
    print(statment_of_financial_position(today +dt.timedelta(365)))

