import pandas as pd
import os
import dash
from dash import Dash, html, dcc, callback, Input, Output
import data_table
import datetime as dt
import plotly.express as px

from utils import filter_by_year, filter_by_year_month, filter_up_to, get_unique_months, get_unique_years, get_lastest_month, get_latest_year, get_months_list, get_years_list

from ratios import calc_current_ratio, calc_debt_ratio, calc_EM, calc_FATO, calc_GP, calc_PM, calc_quick_ratio, calc_ROA, calc_ROE, calc_TATO, calc_withdrawal_ratio

ASSET = [
    'cash','ar','equipment', 'building', 
    'live stock', 'land', 
    'informal loans given', 'loans to employees'
]

INCOME = [
    'sales',
]

EXPENSE = [
    'purchases', 'salary expense', 'utility expense',
    'miscellaneous expense', 'rent expense', 'professional fees',
    'transport expense', 'tax expense', 
    'loss from theft', 'bank fee'
]

OTHER_INC_EXPENSE = [
    'gifts given',
]

EQUITY = [
    'withdrawal', 'equity'
]

LIABILITY = [
    'ap', 'informal loan', 'long term loan', 'short term loan'
]



def get_total_from_summary(summary:list[tuple[str, float]]):
    return sum([item[1] for item in summary])

def get_reverse_sign(summary:list[tuple[str, float]]):
    return [(summ[0], -1*summ[1]) for summ in summary]


def get_balance(id_filter:int, frame: pd.DataFrame, acc_name:str):
    sub = frame[frame['Respondent ID'] == id_filter]
    sub = sub[(~sub['debit amt'].isna()) & (~(sub['credit acc'].isna()))]
    debit = sum(sub[sub['debit acc'] == acc_name]['debit amt'].apply(lambda x: float(x)))
    credit = sum(sub[sub['credit acc'] == acc_name]['credit amt'].apply(lambda x: float(x)))
    # print(debit, credit)
    return debit - credit

def summarize(respondent_id:int, group:list, table: pd.DataFrame):
    return [(acc, get_balance(respondent_id, table, acc)) for acc in group]

def format_number(num):
    if num > 0:
        return f"{num:,.2f} "
    
    if num < 0:
        return f"({-1*num:,.2f})"
    
    return ''

def read_transaction_data():    
    data = []
    to_include = [
        'date', 'debit', 'credit', 'Respondent',
        'Income source',
    ]
    for p, dirs, fs in os.walk('lift_data_transactions'):
        for f in fs:
            path = os.path.join(p, f)
            # print(path)
            temp:pd.DataFrame = pd.read_csv(path)
            df_dict = {}
            for col in temp.columns:
                for hint in to_include:
                    if hint.lower() in col.lower():
                        if hint == 'date':
                            df_dict['date'] = temp[col]
                        else:
                            df_dict[col] = temp[col]
                        break
            df = pd.DataFrame(df_dict)
            # display(df.head())
            data.append(df)

    return pd.concat(data,axis=0).reset_index().drop(columns='index')

def get_retained_earnings(respondent_id, table: pd.DataFrame) -> float:
    income = get_reverse_sign(summarize(respondent_id, INCOME, table))
    total_income = get_total_from_summary(income)

    expenses = get_reverse_sign(summarize(respondent_id, EXPENSE, table))
    total_expense = get_total_from_summary(expenses)

    other = get_reverse_sign(summarize(respondent_id, OTHER_INC_EXPENSE, table))
    total_other = get_total_from_summary(other)
    
    net_income = sum([total_income, total_expense, total_other])
    
    withdrawal = get_total_from_summary(
        get_reverse_sign(summarize(respondent_id, ['withdrawal'], table))
    ) 

    retained_earnings = net_income + withdrawal
    return retained_earnings


def income_statement_and_RE(respondent_id, table: pd.DataFrame) -> pd.DataFrame:
    income = get_reverse_sign(summarize(respondent_id, INCOME, table))
    total_income = get_total_from_summary(income)

    expenses = get_reverse_sign(summarize(respondent_id, EXPENSE, table))
    total_expense = get_total_from_summary(expenses)

    other = get_reverse_sign(summarize(respondent_id, OTHER_INC_EXPENSE, table))
    total_other = get_total_from_summary(other)
    
    net_income = sum([total_income, total_expense, total_other])
    
    withdrawal = get_total_from_summary(
        get_reverse_sign(summarize(respondent_id, ['withdrawal'], table))
    ) 

    retained_earnings = net_income + withdrawal

    table_data = income + \
        [('Total Income', total_income)] + expenses + \
            [('Total Expense', total_expense)] + other + \
                [('Total other Income and expenses', total_other)] + \
                    [('Net Income', net_income), 
                     ('Withdrawal', withdrawal),
                     ('Additional Savings', retained_earnings)]

    formatted_table = pd.DataFrame(
        [
            [name.capitalize(), format_number(amount)]
            for name, amount in table_data
        ],
        columns=['Account', 'Balance']
    )
    formatted_table= formatted_table[formatted_table['Balance'] != ''].reset_index().drop(columns='index')
    return formatted_table


def balance_sheet(respondent_id, table: pd.DataFrame) -> pd.DataFrame:
    retained_earnings = get_retained_earnings(respondent_id, table)

    assets = summarize(respondent_id, ASSET, table)
    liabilities = get_reverse_sign(summarize(respondent_id, LIABILITY, table))
    equity = get_reverse_sign(summarize(respondent_id, ['equity'], table))
    
    total_a = get_total_from_summary(assets)
    total_l = get_total_from_summary(liabilities)
    total_e = get_total_from_summary(equity) + retained_earnings
    
    table_data = assets + [('Total assets', total_a)] + liabilities + [('Total liabilities', total_l)] + [('Equity', total_e), ('Total liability & Equity', total_l + total_e)]

    formatted_table = pd.DataFrame(
        [
            [name.capitalize(), format_number(amount)]
            for name, amount in table_data
        ],
        columns=['Account', 'Balance']
    )
    formatted_table= formatted_table[formatted_table['Balance'] != ''].reset_index().drop(columns='index')
    return formatted_table


def format_date(data:pd.DataFrame, date_col:str):
    dates = []
    for d in data_combined2['date']:
        if not pd.isna(d):
            year, month, day = d.split('-')
            dates.append(dt.date(int(year), int(month), int(day)))
        else:
            dates.append(pd.NA)
    data2 = data.copy()
    data2.drop(columns=date_col, inplace=True)
    data2[date_col] = dates
    return data2


def calculate_ratio_df(df: pd.DataFrame, respondent_id: int) -> pd.DataFrame:
    current_ratios = []
    quick_ratios = []
    fatos = []
    tatos = []

    d_ratios = []
    em_ratios = []

    roes = []
    roas = []
    pms = []
    gps = []

    payouts = []

    years = []
    months = []

    list_func_map = {
        calc_current_ratio: current_ratios, 
        calc_quick_ratio: quick_ratios,
        calc_FATO: fatos, 
        calc_TATO: tatos,
        calc_debt_ratio: d_ratios,
        calc_EM: em_ratios,
        calc_ROE: roes, 
        calc_ROA: roas,
        calc_PM: pms,
        calc_GP: gps,
        calc_withdrawal_ratio: payouts,
    }

    respondent_filtered = df[df['Respondent ID'] == respondent_id].reset_index().drop(columns='index')
    for y in get_years_list(respondent_filtered, 'date'):
        for m in get_months_list(respondent_filtered, y, 'date'):
            monthly_data = filter_by_year_month(respondent_filtered, 'date', y, m)
            data_up_to = filter_up_to(respondent_filtered, 'date', y, m)

            temp_inc_stat = income_statement_and_RE(respondent_id, monthly_data)
            temp_bal_sheet = balance_sheet(respondent_id, data_up_to)
            
            years.append(y)
            months.append(m)

            for func, coll in list_func_map.items():
                coll.append(func(temp_inc_stat, temp_bal_sheet))

    ratio_data = pd.DataFrame({
        'Year': years,
        'Month': months,
        'Current Ratio': current_ratios,
        'Quick Ratio': quick_ratios,
        'FATO': fatos,
        'TATO': tatos,
        'Debt Ratio': d_ratios,
        'Equity Multiplier': em_ratios,
        'Gross Margin': gps,  
        'Profit Margin': pms,
        'Return on Asset': roas,
        'Return on Equity': roas,
        'Withdrawal Ratio': payouts
    })

    ratio_dates = []
    for i, row in ratio_data.iterrows():    
        y = int(row['Year'])
        m = int(row['Month'])
        p = pd.Period(f'{y}-{m}-1')
        last_day = p.days_in_month
        ratio_dates.append(dt.date(y, m, last_day))

    ratio_data['date'] = ratio_dates

    return ratio_data


def get_ratio_graphs(ratio_data:pd.DataFrame):
    return html.Div(
        [
            dcc.Graph(
                figure=px.line(ratio_data, x='date', y=['Current Ratio', 'Quick Ratio'], title='Liquidity ratios'),
            ),
            dcc.Graph(
                figure=px.line(ratio_data, x='date', y=['FATO', 'TATO'], title='Asset managment ratios'),
            ),
            dcc.Graph(
                figure=px.line(ratio_data, x='date', y=['Debt Ratio', 'Equity Multiplier'], title='Debt managment ratios'),
            ),
            dcc.Graph(
                figure=px.line(ratio_data, x='date', y=['Gross Margin', 'Profit Margin', 'Return on Asset', 'Return on Equity'], title='Profitability Ratios'),
            ),
            dcc.Graph(
                figure=px.line(ratio_data, x='date', y=['Withdrawal Ratio'], title='Withdrawal ratio (based on net income)')
            ),
        ]
    )



current_respondent = None
# data_combined = read_transaction_data()
data_combined = pd.read_csv(r'data_combined.csv')
data_combined2 = data_combined.copy()

data_combined2.loc[:, 'debit acc'] = data_combined2['debit acc'].str.lower()
data_combined2.loc[:, 'credit acc'] = data_combined2['credit acc'].str.lower()
data_combined2.loc[:, 'credit acc'] = data_combined2['credit acc'].str.replace(r'sales?', 'sales',regex=True)

data_combined2.loc[:, 'debit acc'] = data_combined2['debit acc'].str.replace('salaries and wages', 'salary expense')

data_combined2 = format_date(data_combined2, 'date')

# data_combined2.to_csv('lift_data_transactions/data_combined.csv')
app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div([
                    html.H1('Filter'),
                    dcc.Dropdown(
                        placeholder='Select firm',
                        id='respondant-selector',
                        className='selector',
                        options= 
                            [
                                {'label': x, 'value': x}
                                for x in data_combined2['Respondent ID'].unique()
                            ],
                    ),
                    dcc.Dropdown(
                        id='year-selector',
                        className='selector',
                        disabled=True,
                        placeholder='Select Year',
                    ),
                    dcc.Dropdown(
                        id='month-selector',
                        className='selector',
                        disabled=True,
                        placeholder='Select Month',
                    ),
                ],
                className='selectors-container'
                ),
                html.Div(
                    id='fin-container'
                ),
                dcc.Loading(
                    type='default',
                    children=html.Div(
                        id='ratio-graphs'
                    )
                ),
            ]
        )
    ]
)


@callback(
    Output('fin-container', 'children'),
    Output('year-selector', 'disabled'),
    Output('year-selector', 'value'),
    Output('year-selector', 'options'),
    Output('month-selector', 'disabled'),
    Output('month-selector', 'value'),
    Output('month-selector', 'options'),

    Input('respondant-selector', 'value'),
    Input('year-selector', 'value'),
    Input('month-selector', 'value'),
    prevent_initial_call=True,
)
def on_filters_selected(respondent_id, year, month):
    global current_respondent
    if current_respondent != respondent_id:
        current_respondent = respondent_id
        year = None
        month = None

    print(respondent_id, year, month)

    data_filtered = data_combined2[data_combined2['Respondent ID'] == respondent_id].reset_index().drop(columns='index')

    respondent_filterd = data_filtered.copy()

    balance_sheet_data = None
    inc_additional = ''
    balance_additional = ''

    if year == None:
        year = get_latest_year(data_filtered, 'date')
    
    if month == None:
        month = get_lastest_month(data_filtered, 'date', year)

    p = pd.Period(f'{year}-{month}-1')
    last_day = p.days_in_month
    month_name = dt.date(year, month, 1).strftime('%B')
    
    year_filtered = filter_by_year(data_filtered, 'date', year)

    data_filtered = filter_by_year_month(data_filtered, 'date', year, month)
    balance_sheet_data = filter_up_to(respondent_filterd, 'date', year, month)

    inc_additional = f'Respondent {respondent_id} for  {month_name}, {year}'
    balance_additional = f'Respondant {respondent_id} on {month_name} {last_day}, {year}'


    financials = html.Div(
        [
            html.H2(f'Income statement and Additions to savings - {inc_additional}'),
            data_table.df_to_datatable(income_statement_and_RE(respondent_id, data_filtered)),
            html.H2(f'Balance Sheet - {balance_additional}'),
            data_table.df_to_datatable(balance_sheet(respondent_id, balance_sheet_data)),
        ]
    )


    year_options = [
        {'label': x, 'value': x}
        for x in sorted(get_unique_years(respondent_filterd, 'date'))
    ]

    month_options = [
        {'label': x, 'value': x}
        for x in sorted(get_unique_months(year_filtered, 'date'))
    ]
    
    return financials, False, year, year_options, False, month, month_options


@callback(
    Output('ratio-graphs', 'children'),
    Input('respondant-selector', 'value'),
    prevent_initial_call=True,
)
def ratio_updater(respondent_id):
    ratio_data = calculate_ratio_df(data_combined2, respondent_id)
    print(ratio_data)
    return get_ratio_graphs(ratio_data)



if __name__ == '__main__':

    app.run(debug=True)
