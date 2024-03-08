import dash
from dash import html, dcc, Input, Output, callback, ALL
import chart, sales
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table

dash.register_page(__name__)


#----------BTN IDS
COLLECT_BTN = 'collect-btn'
#----------

BTN_COLLECTION = [
    COLLECT_BTN
] 
#--------

btn_counter = 0



def standard_layout():
    global btn_counter
    cus_df = sales.CustomerInfo.table_form_multiple()
    cus_table = data_table.df_to_datatable(cus_df)
    cus_btn = None

    if type(cus_df) != type(None) and (len(cus_df) > 0):
        cus_btn = html.Button('Recieve Payment', id={'type': COLLECT_BTN, 'index': btn_counter})

    
    layout = html.Div(
        [
            html.Div(
                [
                    html.P(f'Total Sales - {chart.get_account(chart.SALES).current_balanace()}')
                ]
            ),
            html.Div(
                [
                    html.H2('Customers that have not paid'),
                    cus_table,
                    cus_btn
                ]
            )
        ]
    )
    
    return layout


def collect_layout():
    global btn_counter
    layout = html.Div(
        [   
            html.H2('Receive Payment'),
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    html.Select(
                        [
                            html.Option(cus.name) for cus in sales.CustomerInfo.customers_with_upaid_balances()
                        ],
                        name=form_executor.CUSTOMER_NAME,
                        required=True
                    ),
                    dcc.Input(name=form_executor.AMOUNT, required=True),
                    dcc.Textarea(placeholder = 'Note on collection', name=form_executor.NOTE),
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )

    return layout



#------------------------ Navigation related
current_layout = standard_layout



nav_sys = NavSystem(BTN_COLLECTION, standard_layout)

#------------------------


layout = html.Div(
    [
        html.H1('Sales'),
        html.Div(
            [
                html.Button('Back', id='back-btn')
            ]
        ),
        html.Div(
            [
                standard_layout()
            ],
            id='layout-container-sales'
        )
    ],
)


#-------------------------------------Buying inventory
@callback(
    Output('layout-container-sales', 'children',allow_duplicate=True),
    Input({'type': COLLECT_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def collect_bill(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(collect_layout, COLLECT_BTN, n_clicks, form_executor.COLLECT_PAYMENT_STATE)



@callback(
    Output('layout-container-sales', 'children', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call = True
)
def back_clicked(n_clicks):
    # print('back clicked', n_clicks)
    return nav_sys.get_back()


