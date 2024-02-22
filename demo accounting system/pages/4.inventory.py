import dash
from dash import html, dcc, Input, Output, callback, ALL
import inventory
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table

dash.register_page(__name__)


#----------IDS
BUY_INV='buy-inventory'
SELL_INV='sell-inventory'
USE_SUPPLY='use-supply'
PERSONAL_USE='personal-use'
INVEST_INV='invest-inventory'
BUY_INV_CREDIT_CHOICE = 'buy-inv-credit-choice'
BUY_INV_CASH_CHOICE = 'buy-inv-cash-choice'
SELL_INV_CASH_CHOICE = 'sell-inv-cash-choice'
SELL_INV_CREDIT_CHOICE = 'sell-inv-credit-choice'
PAY_VENDOR = 'pay-vendor'

BTN_COLLECTION = [
    BUY_INV, SELL_INV, USE_SUPPLY,
    PERSONAL_USE, INVEST_INV, BUY_INV_CASH_CHOICE,
    BUY_INV_CREDIT_CHOICE, SELL_INV_CASH_CHOICE, 
    SELL_INV_CREDIT_CHOICE, PAY_VENDOR
] 
#--------

btn_counter = 0

def standard_layout():
    global btn_counter
    inv = None
    inv_table = None
    vendor_data = None
    vendor_table = None
    try:
        inv = inventory.Inventory.table_form_multiple(inventory.Inventory.all_inventory)
        inv_table = data_table.df_to_datatable(inv)
        vendor_data = inventory.VendorInfo.table_form_multiple()
        vendor_table = data_table.df_to_datatable(vendor_data)
        
    except Exception as e:
        print(f'Didn\'t properly get inventory:\nException:{e}')
        print(inventory.Inventory.get_all_items())

    pay_ven_btn = None

    if (type(vendor_data) != type(None)) and (len(vendor_data) > 0):
        pay_ven_btn = html.Button('Pay Vendor', id={'type': PAY_VENDOR, 'index': btn_counter})

    layout = html.Div(
        [
            html.Div(
                [
                    html.H2('Unpaid balances'),
                    vendor_table,
                    pay_ven_btn,
                ],
                id={'type': 'vendor-container', 'index': btn_counter}
            ),
            html.Div(
                [
                    html.H2('My Inventory'),
                    inv_table,
                    # html.Hr()
                ],
                id={'type': 'inventory-container', 'index': btn_counter}
            ),
            html.Div(
                [
                    html.H2('Actions'),
                    html.Div(
                        [
                            html.Button('Buy Inventory', id={'type': BUY_INV, 'index':btn_counter}),
                            html.Button('Sell Inventory', id={'type': SELL_INV, 'index': btn_counter}),
                            html.Button('Use Supplies', id={'type': USE_SUPPLY, 'index': btn_counter}),
                            html.Button('Personally Use Inventory', id={'type': PERSONAL_USE, 'index': btn_counter}),
                            html.Button('Invest More Inventory', id={'type': INVEST_INV, 'index': btn_counter}),
                        ]
                    )
                ],
                id='actions'
            )
        ]
    )
    btn_counter += 1
    return layout

def buy_inventory_choice():
    global btn_counter
    layout = html.Div(
        [
            html.P('Buying options'),
            html.Button('On Credit', id={'type': BUY_INV_CREDIT_CHOICE, 'index': btn_counter}),
            html.Button('With Cash', id={'type': BUY_INV_CASH_CHOICE, 'index':btn_counter})
        ]
    )
    btn_counter += 1
    return layout

def buy_inventory_cash_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form([
                html.Fieldset([
                    html.Legend('Sellers Info'),
                    dcc.Input(type='text', placeholder='Seller name', name=form_executor.SELLER_NAME),
                    dcc.Input(type='text', placeholder='Seller phone', name=form_executor.SELLER_PHONE),
                ]),

                html.Fieldset([
                    html.Legend('Transaction Info'),
                    dcc.DatePickerSingle(date=dt.date.today()),
                    dcc.Input(type='text', placeholder='inventory name', name=form_executor.INVENTORY_NAME, required=True),
                    dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),
                    dcc.Input(type='number', name=form_executor.COST, placeholder='Cost', required=True),
                    html.Select(
                        [
                            html.Option(t) for t in [inventory.MERCH, inventory.SUPPLY]
                        ],
                        name=form_executor.INVENTORY_TYPE,
                        required=True
                    ),
                    dcc.Textarea(
                        placeholder='Note',
                        name=form_executor.NOTE
                    )
                ]),

                html.Button('Submit')

            ], action='/post', method='post'),

        ]
    )
    btn_counter += 1
    return layout

def buy_inventory_credit_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form([
                html.Fieldset([
                    html.Legend('Sellers Info'),
                    dcc.Input(type='text', required=True, placeholder='Seller name', name=form_executor.SELLER_NAME),
                    dcc.Input(type='text', required=True, placeholder='Seller phone', name=form_executor.SELLER_PHONE),
                ]),

                html.Fieldset([
                    html.Legend('Transaction Info'),
                    dcc.DatePickerSingle(date=dt.date.today()),
                    dcc.Input(type='text', placeholder='inventory name', name=form_executor.INVENTORY_NAME, required=True),
                    dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),
                    dcc.Input(type='number', name=form_executor.COST, placeholder='Cost', required=True),
                    html.Select(
                        [
                            html.Option(t) for t in [inventory.MERCH, inventory.SUPPLY]
                        ],
                        name=form_executor.INVENTORY_TYPE,
                        required=True
                    ),
                    dcc.Textarea(
                        placeholder='Note',
                        name=form_executor.NOTE
                    )
                ]),

                html.Button('Submit')

            ], action='/post', method='post'),

        ]
    )
    btn_counter += 1
    return layout


def sell_inventory_choice():
    global btn_counter
    return html.Div(
    [
        html.P('Selling Options'),
        html.Button('On Credit', id={'type': SELL_INV_CREDIT_CHOICE, 'index': btn_counter}),
        html.Button('With Cash', id={'type': SELL_INV_CASH_CHOICE, 'index': btn_counter})
    ]
)

def sell_inventory_credit():
    global btn_counter
    return html.Div(
    [
        html.Form([
            html.Fieldset([
                html.Legend('Buyer\'s Info'),
                dcc.Input(type='text', required=True, placeholder='Buyer name', name=form_executor.CUSTOMER_NAME),
                dcc.Input(type='text', required=True, placeholder='Buyer phone', name=form_executor.CUSTOMER_PHONE),
            ]),

            html.Fieldset([
                html.Legend('Transaction Info'),
                dcc.DatePickerSingle(date=dt.date.today()),
                dcc.Input(type='number', required=True, placeholder='Selling Price', name=form_executor.AMOUNT),
                html.Select(
                    [html.Option(inv.name) for inv in inventory.Inventory.get_all_items()],
                    name=form_executor.INVENTORY_NAME,
                    required=True
                ),
                dcc.Input(type='number', placeholder='Quantity', name=form_executor.QUANTITY,required=True),
                dcc.Textarea(
                    placeholder='Note',
                    name=form_executor.NOTE
                )
            ]),

            html.Button('Submit')
        ], action='/post', method='post'),

    ]
)

def sell_inventory_cash():
    global btn_counter
    return html.Div(
    [
        html.Form([
            html.Fieldset([
                html.Legend('Buyer\'s Info'),
                dcc.Input(type='text', placeholder='Buyer name', name=form_executor.CUSTOMER_NAME),
                dcc.Input(type='text', placeholder='Buyer phone', name=form_executor.CUSTOMER_PHONE),
            ]),

            html.Fieldset([
                html.Legend('Transaction Info'),
                dcc.DatePickerSingle(date=dt.date.today()),
                dcc.Input(type='number', required=True, placeholder='Selling Price', name=form_executor.AMOUNT),
                html.Select(
                    [html.Option(inv.name) for inv in inventory.Inventory.get_all_items()],
                    name=form_executor.INVENTORY_NAME,
                    required=True
                ),
                dcc.Input(type='number', placeholder='Quantity', name=form_executor.QUANTITY,required=True),
                dcc.Textarea(
                    placeholder='Note',
                    name=form_executor.NOTE
                )
            ]),

            html.Button('Submit')
        ], action='/post', method='post'),

    ]
)

def use_supply_layout():
    global btn_counter
    return html.Div(
    [
        html.Form(
            [
                dcc.DatePickerSingle(date=dt.date.today()),
                html.Select(
                    [html.Option(inv.name) for inv in inventory.Inventory.get_all_items()],
                    name=form_executor.INVENTORY_NAME,
                    required=True
                ),
                dcc.Input(type='number', required=True, placeholder='Quantity', name=form_executor.QUANTITY),
                dcc.Textarea("Note on supply usage", name=form_executor.NOTE),
                
                html.Button('Submit'),

            ],
            action='/post', method='post'
        )
    ]
)

def personal_use_layout():
    global btn_counter
    return html.Div(
    [
        html.Form(
            [
                dcc.DatePickerSingle(date=dt.date.today()),
                html.Select(
                    [html.Option(inv.name) for inv in inventory.Inventory.get_all_items()],
                    name=form_executor.INVENTORY_NAME,
                    required=True
                ),
                dcc.Input(type='number', required=True, placeholder='Quantity', name=form_executor.QUANTITY),
                dcc.Textarea("Note on usage", name=form_executor.NOTE),
                
                html.Button('Submit'),

            ],
            action='/post', method='post'
        )
    ]
)

def invest_inventory_layout():
    global btn_counter
    return html.Div(
    [
        html.Form(
            [

                dcc.DatePickerSingle(date=dt.date.today()),
                dcc.Input(type='text', placeholder='Inventory Name', name=form_executor.INVENTORY_NAME),
                html.Select(
                    [
                        html.Option('To resale', value=inventory.MERCH),
                        html.Option('To use in business', value=inventory.SUPPLY),
                    ],
                    name=form_executor.INVENTORY_TYPE
                ),
                dcc.Input(type='number', placeholder='quantity', name=form_executor.QUANTITY),
                dcc.Input(type='number', placeholder='cost', name=form_executor.COST),
                dcc.Textarea(placeholder='note on your investment', name=form_executor.NOTE),
                
                html.Button('Submit')
            ],
            action='/post', method='post'
        )
    ]
)


def pay_vendor_layout():
    global btn_counter
    return html.Div(
    [
        html.Form(
            [
                dcc.DatePickerSingle(date=dt.date.today()),
                html.Select(
                    [html.Option(ven.name) for ven in inventory.VendorInfo.vendors_with_upaid_balances()],
                    name=form_executor.SELLER_NAME,
                    required=True
                ),
                dcc.Input(type='number', required=True, placeholder='Amount', name=form_executor.AMOUNT),
                dcc.Textarea("Note on paying vendor", name=form_executor.NOTE),
                
                html.Button('Submit'),

            ],
            action='/post', method='post'
        )
    ]
)


#------------------------ Navigation related
current_layout = standard_layout


# you link button id and next layout here
# TRANSITIONS = [
#     (BUY_INV, buy_inventory_choice), 
#     (SELL_INV, sell_inventory_choice),
#     (USE_SUPPLY, use_supply_layout),
#     (INVEST_INV, invest_inventory_layout),
#     (BUY_INV_CASH_CHOICE, buy_inventory_cash_layout),
#     (BUY_INV_CREDIT_CHOICE, buy_inventory_credit_layout),
#     (SELL_INV_CASH_CHOICE, sell_inventory_cash),
#     (SELL_INV_CREDIT_CHOICE, sell_inventory_credit)
# ]

# BTN_CLICKS_MAP = {
#     btn: [None] for btn in BTN_COLLECTION
# }
nav_sys = NavSystem(BTN_COLLECTION, standard_layout)

#------------------------


layout = html.Div(
    [
        html.H1('Inventory'),
        html.Div(
            [
                html.Button('Back', id='back-btn')
            ]
        ),
        html.Div(
            [
                standard_layout()
            ],
            id='layout-container'
        )
    ],
)


#-------------------------------------Buying inventory
@callback(
    Output('layout-container', 'children'),
    Input({'type': BUY_INV, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def buy_clicked(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(buy_inventory_choice, BUY_INV, n_clicks, None)


@callback(
    Output('layout-container', 'children', allow_duplicate=True),
    Input({'type': BUY_INV_CASH_CHOICE, 'index': ALL} , 'n_clicks'),
    prevent_initial_call=True   
)
def buy_inv_cash(n_clicks):
    # print(BUY_INV_CASH_CHOICE, 'clicked', n_clicks)
    
    return nav_sys.navigate_forward(buy_inventory_cash_layout, BUY_INV_CASH_CHOICE, n_clicks, form_executor.BUY_INV_CASH_STATE)


@callback(
    Output('layout-container', 'children', allow_duplicate=True),
    Input({'type': BUY_INV_CREDIT_CHOICE, 'index': ALL} , 'n_clicks'),
    prevent_initial_call=True   
)
def buy_inv_credit(n_clicks):
    # print(BUY_INV_CASH_CHOICE, 'clicked', n_clicks)
    return nav_sys.navigate_forward(buy_inventory_credit_layout, BUY_INV_CREDIT_CHOICE, n_clicks, form_executor.BUY_INV_CREDIT_STATE)
#-------------------------------------------




#---------------------------Selling inventory
@callback(
    Output('layout-container', 'children',allow_duplicate=True),
    Input({'type': SELL_INV, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def sell_clicked(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(sell_inventory_choice, SELL_INV, n_clicks, None)

@callback(
    Output('layout-container', 'children', allow_duplicate=True),
    Input({'type': SELL_INV_CASH_CHOICE, 'index': ALL} , 'n_clicks'),
    prevent_initial_call=True   
)
def sell_inv_cash(n_clicks):
    # print(BUY_INV_CASH_CHOICE, 'clicked', n_clicks)

    return nav_sys.navigate_forward(sell_inventory_cash, SELL_INV_CASH_CHOICE, n_clicks, form_executor.SELL_INV_CASH_STATE)


@callback(
    Output('layout-container', 'children', allow_duplicate=True),
    Input({'type': SELL_INV_CREDIT_CHOICE, 'index': ALL} , 'n_clicks'),
    prevent_initial_call=True   
)
def sell_inv_credit(n_clicks):
    # print(BUY_INV_CASH_CHOICE, 'clicked', n_clicks)
    
    return nav_sys.navigate_forward(sell_inventory_credit, SELL_INV_CREDIT_CHOICE, n_clicks, form_executor.SELL_INV_CREDIT_STATE)
#----------------------------------------------------


#------------------------------------Use supplies

@callback(
    Output('layout-container', 'children',allow_duplicate=True),
    Input({'type': USE_SUPPLY, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def use_supply(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(use_supply_layout, USE_SUPPLY, n_clicks, form_executor.USE_SUPPLY_STATE)
#-----------------------------------------------


#-------------------------------personally use
@callback(
    Output('layout-container', 'children',allow_duplicate=True),
    Input({'type': PERSONAL_USE, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def personally_use(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(personal_use_layout, PERSONAL_USE, n_clicks, form_executor.PERSONAL_USE_SUPPLY_STATE)
#-----------------------------


#----------------------- Invest more

@callback(
    Output('layout-container', 'children',allow_duplicate=True),
    Input({'type': INVEST_INV, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def invest_inv(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(invest_inventory_layout, INVEST_INV, n_clicks, form_executor.INVEST_INV_STATE)
#-----------------------------

#-------------------------Paying vendors
@callback(
    Output('layout-container', 'children',allow_duplicate=True),
    Input({'type': PAY_VENDOR, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_vendor(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(pay_vendor_layout, PAY_VENDOR, n_clicks, form_executor.PAY_VENDOR_STATE)



@callback(
    Output('layout-container', 'children', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call = True
)
def back_clicked(n_clicks):
    # print('back clicked', n_clicks)
    return nav_sys.get_back()


