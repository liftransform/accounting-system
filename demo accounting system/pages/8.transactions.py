import dash
from dash import html, dcc, callback, Input, Output
import inventory
from transactions import Transaction
import data_table

dash.register_page(__name__)

# df = Transaction.get_all_transactions()
layout = html.Div(
    [
        html.H1('For development purposes'),
        html.Button('Refresh', id='refresh-btn'),
        html.Div(
            [
                # dash_table.DataTable(
                #     df.to_dict('records'), 
                #     [{"name": i, "id": i} for i in df.columns])    
            ],
            id='transaction-container'
        )
    ],
)


@callback(
    Output('transaction-container', 'children'),
    Input('refresh-btn', 'n_clicks'),
)
def update_table(n_cliks):
    df = Transaction.get_all_transactions()
    return data_table.df_to_datatable(df)
