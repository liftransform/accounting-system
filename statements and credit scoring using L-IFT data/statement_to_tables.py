import pandas as pd
from dash import Dash, html
import plotly.express as px
import plotly.graph_objects as go
# from ratios import unformat_num

# columns
ACCOUNT = 'Account'
BALANCE = 'Balance'
TYPE = 'Type'
#--------

#Row types
CATEGORY = 'category'
TOTAL = 'total'
TITLE = 'title'
REGULAR = 'regular'
#--------


#stat_type
INCOME_STATEMENT = 'income statement'
BALANCE_SHEET = 'balance_sheet'


def _prepare_inc_statement(inc_stat: pd.DataFrame) -> pd.DataFrame:
    # write a type column
    # rename some accounts
    # add some new rows so it can be similar to the one you saw on quick books
    preped_statement = {
        ACCOUNT: ['Income/Cost'],
        BALANCE: ['Amount'],
        TYPE: [TITLE]
    }

    account_type_map = {
        **{
            acc.lower(): REGULAR for acc in [
                'Sales', 'Purchases', 'Salary expense', 'Utility expense',
                'Miscellaneous expense', 'Rent expense', 'Professional fees',
                'Transport expense', 'Tax expense',
                'Loss from theft', 'Bank fee', 'Gifts given', 'Withdrawal',

            ]
        },
        **{
            acc.lower(): TOTAL for acc in [
                'Total income', 'Total expense',
                'Total other income and expenses',
                'Net income', 'Additional Savings'
            ]
        },
        # **{
        #     acc.lower(): TITLE for acc in [

        #     ]
        # },
        # **{
        #     acc.lower(): CATEGORY for acc in [

        #     ]
        # }
    }

    for i, row in inc_stat.iterrows():
        a:str = row[ACCOUNT]
        b:str = row[BALANCE]
        
        #TODO: renaming a to new_a for certain accounts
        preped_statement[ACCOUNT].append(a.title())
        
        preped_statement[BALANCE].append(b)
        preped_statement[TYPE].append(account_type_map[a.lower()])

    return pd.DataFrame(preped_statement)


    

def _prepare_bal_sheet(bal_sheet: pd.DataFrame) -> pd.DataFrame:
    preped_statement = {
        ACCOUNT: ['Assets'],
        BALANCE: ['Amount'],
        TYPE: [TITLE]
    }

    account_type_map = {
        **{
            acc.lower(): REGULAR for acc in [
                'Cash', 'Ar', 'Equipment', 'Building',
                'Live stock', 'Land', 'Informal loans given',
                'Loans to employees', 'Ap', 'Informal loan', 'Long term loan', 'short term loan', 'Equity'
            ]
        },
        **{
            acc.lower(): TOTAL for acc in [
                'Total assets', 'Total liabilities',
                'Total liabilities & Equity'
            ]
        },
        # **{
        #     acc.lower(): TITLE for acc in [

        #     ]
        # },
        # **{
        #     acc.lower(): CATEGORY for acc in [

        #     ]
        # }
    }

    for i, row in bal_sheet.iterrows():
        a:str = row[ACCOUNT]
        b:str = row[BALANCE]
        
        #TODO: renaming a to new_a for certain accounts
        preped_statement[ACCOUNT].append(a.title())
        
        preped_statement[BALANCE].append(b)
        preped_statement[TYPE].append(account_type_map[a.lower()])

        if a.lower() == 'total assets':
            preped_statement[ACCOUNT].append('liabilities and equity'.title())
            preped_statement[BALANCE].append('Amount')
            preped_statement[TYPE].append(TITLE)

    return pd.DataFrame(preped_statement)



def _prepare_statement(statement: pd.DataFrame, stat_type:str) -> pd.DataFrame:
    type_func_pair = {
        INCOME_STATEMENT: _prepare_inc_statement,
        BALANCE_SHEET: _prepare_bal_sheet
    }
    func = type_func_pair[stat_type]
    return func(statement)




def statement_to_table(statement: pd.DataFrame, stat_type:str) -> html.Div:
    # Columns for statement are: Account, balance and type

    prepared_statement = _prepare_statement(statement, stat_type)
    # print('------------------')
    # print(prepared_statement)
    rows = []

    for i, row in prepared_statement.iterrows():
        t = row[TYPE]
        b = row[BALANCE]
        a = row[ACCOUNT]
        rows.append(
            html.Div(
                [
                    html.Span(a), 
                    html.Span(b)
                ],
                className=t
            )
        )

    return html.Div(
        [
            html.Div(
                rows,
                className='table-inner'
            )
        ],
        className='table-outer'
    )





if __name__ == '__main__':
    # from app import income_statement_and_RE, data_combined2
    test = Dash(__name__)
    inc_stat = pd.DataFrame(
        [
            ["Sales", "538940.00"],
            ["Total income", "538940.00"],
            ["Purchases", "(94899.00)"],
            ["Salary expense", "(42000.00)"],
            ["Utility expense", "(3339.00)"],
            ["Miscellaneous expense", "(35752.00)"],
            ["Rent expense", "(24000.00)"],
            ["Professional fees", "(1795.00)"],
            ["Transport expense", "(600.00)"],
            ["Tax expense", "(3644.00)"],
            ["Loss from theft", ""],
            ["Bank fee", ""],
            ["Total expense","(206029.00)"],
            ["Gifts given", ""],
            ["Total other income and expenses", ""],
            ["Net income", "332911.00"],
            ["Withdrawal", "(396782.00)"],
            ["Additional Savings", "(63871.00)"],
        ],
        columns = ['Account', 'Balance']
    )

    bal_sheet = pd.DataFrame(
        [
            ["Cash","321389.50"],
            ["Ar","5516.00"],
            ["Equipment", "1764400.00"],
            ["Building", ""],
            ["Live stock", ""],
            ["Land", ""],
            ["Informal loans given", "200000.00"],
            ["Loans to employees", ""],
            ["Total assets", "2291305.50"],
            ["Ap", ""],
            ["Informal loan", "11750.00"],
            ["Long term loan", ""],
            ["Short term loan", ""],
            ["Total liabilities", "11750.00"],
            ["Equity", "2279555.50"],
        ],
        columns = ['Account', 'Balance']
    )

    print(inc_stat)
    print(bal_sheet)
    test.layout = html.Div(
        [
            html.H2('Testing out tables for the financial statementes'),
            statement_to_table(inc_stat, INCOME_STATEMENT),
            statement_to_table(bal_sheet, BALANCE_SHEET)
        ]
    )
    test.run(debug=True)


