import dash
from dash import html, dcc, callback, Input, Output
import data_table
import reports
from transactions import Transaction

dash.register_page(__name__)

STATEMENTS = [
    'Statement of Profit or loss & OCI',
    'Statement of Retained Earnings',
    'Statement of Owner\'s Equity',
    'Statement of Financial Position',
]

STAT_FUNC_MAP = {
    'Statement of Profit or loss & OCI': reports.income_statement,
    'Statement of Retained Earnings': reports.statement_of_retained_earnings,
    'Statement of Owner\'s Equity': reports.statement_of_owner_equity,
    'Statement of Financial Position': reports.statment_of_financial_position
}

layout = html.Div(
    [
        html.H1('Financial Statements',id='page-title'),
        dcc.Dropdown(
            id='statement-selector',
            options= 
            [
                {'label': x, 'value': x}
                for x in STATEMENTS
            ],
        ),
        html.Div(
            [

            ],
            id='statement-container'
        )
    ],
)


@callback(
    Output('statement-container', 'children'),
    Output('page-title', 'children'),
    Input('statement-selector', 'value'),
    prevent_initial_call = True
)
def change_statement(value):
    latest_date = max([t.date for t in Transaction.all_transactions])
    func = STAT_FUNC_MAP[value]
    df = func(latest_date)
    return data_table.df_to_datatable(df), f'Financial Statements-{value}'
