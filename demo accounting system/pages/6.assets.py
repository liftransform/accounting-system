import dash
from dash import html, dcc, Input, Output, callback, ALL
import other_assets, equity
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table
import chart

dash.register_page(__name__)


#----------BTN IDS
TAKE_OUT_CASH_BTN = 'take out cash btn'
INVEST_CASH_BTN = 'invest cash btn'

BUY_BTN = 'buy asset btn'
DISPOSE_BTN = 'dispose asset btn'
EXCHANGE_BTN = 'exchange asset btn'
INVEST_ASSET_BTN = 'invest asset btn'
USE_PERSONALLY = 'use asset personally btn'
#----------

BTN_COLLECTION = [
    TAKE_OUT_CASH_BTN, INVEST_CASH_BTN, BUY_BTN,
    DISPOSE_BTN, EXCHANGE_BTN, INVEST_ASSET_BTN,
    USE_PERSONALLY
]

#--------

btn_counter = 0

def _get_asset_str_list():
    asset_str_list = []
    for asset in other_assets.FixedAsset.get_all_assets():
        asset_name = asset.name
        quantity = asset.quantity
        cost = asset.cost
        total = quantity * cost
        asset_id = asset.id
        temp = f'{asset_id}, {asset_name}, {total}'
        asset_str_list.append(temp)
    return asset_str_list

def standard_layout():
    global btn_counter
    asset_df = other_assets.FixedAsset.table_form_multiple()
    asset_table = data_table.df_to_datatable(asset_df)
    
    dispose_btn = None
    exchange_btn = None
    use_personal_btn = None

    
    if len(asset_df) > 0:
        dispose_btn = html.Button('Sell or Dispose Asset', id={'type': DISPOSE_BTN, 'index': btn_counter})
        exchange_btn = html.Button('Exchange Asset', id={'type': EXCHANGE_BTN, 'index': btn_counter})
        use_personal_btn = html.Button('Use Asset only for personal purpose', id={'type': USE_PERSONALLY, 'index': btn_counter})


    layout = html.Div(
        [
            html.Div(
                [
                    html.H2('Cash'),
                    html.P(f'My Balance- {chart.get_account(chart.CASH).current_balanace()}'),
                    html.Button('Take out Cash', id={'type': TAKE_OUT_CASH_BTN, 'index': btn_counter}),
                    html.Button('Invest Cash', id={'type': INVEST_CASH_BTN, 'index': btn_counter})
                ]
            ),
            html.Div(
                [
                    html.H2('Assets'),
                    asset_table,
                    html.Button('Buy Asset', id={'type': BUY_BTN, 'index': btn_counter}),
                    html.Button('Invest Personal Asset', id={'type': INVEST_ASSET_BTN, 'index': btn_counter}),
                    dispose_btn,
                    exchange_btn,
                    use_personal_btn,
                ]
            )
        ]
    )
    btn_counter += 1
    return layout

def takeout_cash_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),

                    dcc.Input(placeholder='Amount of cash', required=True, name=form_executor.AMOUNT),

                    dcc.Textarea(placeholder='Note on cash withdrawal', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout

def invest_cash_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),

                    dcc.Input(placeholder='Amount', required=True, name=form_executor.AMOUNT),
                
                    dcc.Textarea(placeholder='Note on investing cash', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout

def buy_asset_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    html.H2(''),
                    dcc.DatePickerSingle(date=dt.date.today()),

                    dcc.Input(type='text', name=form_executor.EQUIPMENT_NAME, required=True, placeholder='Asset Name'),
                    dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),
                    dcc.Input(type='number', name=form_executor.COST, placeholder='Cost per item', required=True), 
                    dcc.Input(type='number', name=form_executor.USAGE_YEARS, placeholder='How long do you expect to use it?', required=True),

                    dcc.Textarea(placeholder='Note on buying asset', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout


def dispose_asset_layout():
    global btn_counter

    layout = html.Div(
        [
            html.Form(
                [
                    html.H2('Sell or get rid of asset'),
                    dcc.DatePickerSingle(date=dt.date.today()),

                    html.Select(
                        [
                            html.Option(asset) 
                            for asset in _get_asset_str_list()
                        ],
                        name=form_executor.EQUIPMENT,
                        required=True
                    ),
                    dcc.Input(type='number', placeholder='Amount received', name=form_executor.AMOUNT, required=True),
                
                    dcc.Textarea(placeholder='Note on disposing asset', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout


def exchange_asset_layout():
    global btn_counter

    layout = html.Div(
        [
            html.Form(
                [
                    html.H2('Exchange asset'),
                    dcc.DatePickerSingle(date=dt.date.today()),

                    html.Fieldset(
                        [
                            html.Legend('Old asset'),
                            html.Select(
                                [
                                    html.Option(asset) 
                                    for asset in _get_asset_str_list()
                                ],
                                name=form_executor.EQUIPMENT
                            )
                        ]
                    ),

                    html.Fieldset(
                        [
                            html.Legend('New asset'),
                            dcc.Input(type='text', name=form_executor.EQUIPMENT_NAME, required=True, placeholder='Asset Name'),
                            dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),
                            dcc.Input(type='number', name=form_executor.COST, placeholder='Cost per item', required=True), 
                            dcc.Input(type='number', name=form_executor.USAGE_YEARS, placeholder='How long do you expect to use it?', required=True),

                            dcc.Input(type='number', name=form_executor.EQ_CASH_TAKEN, placeholder='Any Cash Taken'),
                            
                            dcc.Input(type='number', name=form_executor.EQ_CASH_GIVEN, placeholder='Any Cash Given'),
                            
                        ]
                    ),
                    dcc.Textarea(placeholder='Note on exchange of asset', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout


def invest_asset_layout():
    global btn_counter

    layout = html.Div(
        [
            html.Form(
                [
                    html.H2('Invest Personal Asset'),
                    dcc.DatePickerSingle(date=dt.date.today()),

                    dcc.Input(type='text', name=form_executor.EQUIPMENT_NAME, required=True, placeholder='Asset Name'),
                    dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),
                    dcc.Input(type='number', name=form_executor.COST, placeholder='Cost per item', required=True), 
                    dcc.Input(type='number', name=form_executor.USAGE_YEARS, placeholder='How long do you expect to use it?', required=True),

                
                    dcc.Textarea(placeholder='Note on investing personal asset', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout


def use_asset_personally_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    html.H2('Take asset out of my business and use personally'),
                    dcc.DatePickerSingle(date=dt.date.today()),

                    html.Select(
                        [
                            html.Option(asset) 
                            for asset in _get_asset_str_list()
                        ],
                        name=form_executor.EQUIPMENT,
                        required=True
                    ),
                    dcc.Input(type='number', name=form_executor.QUANTITY, placeholder='Quantity', required=True),

                    dcc.Textarea(placeholder='Note on', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout




#------------------------ Navigation related
current_layout = standard_layout



nav_sys = NavSystem(BTN_COLLECTION, standard_layout)

#------------------------


layout = html.Div(
    [
        html.H1('Other Assets'),
        html.Div(
            [
                html.Button('Back', id='back-btn')
            ]
        ),
        html.Div(
            [
                standard_layout()
            ],
            id='layout-container-asset'
        )
    ],
)




#-------------------------------------Buying inventory
@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': TAKE_OUT_CASH_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def takeout_cash(n_clicks):
    return nav_sys.navigate_forward(takeout_cash_layout, TAKE_OUT_CASH_BTN, n_clicks, form_executor.TAKEOUT_CASH_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': INVEST_CASH_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def invest_cash(n_clicks):
    return nav_sys.navigate_forward(invest_cash_layout, INVEST_CASH_BTN, n_clicks, form_executor.INVEST_CASH_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': BUY_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def buy_asset(n_clicks):
    return nav_sys.navigate_forward(buy_asset_layout, BUY_BTN, n_clicks, form_executor.BUY_EQUIP_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': DISPOSE_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def dispose_asset(n_clicks):
    return nav_sys.navigate_forward(dispose_asset_layout, DISPOSE_BTN, n_clicks, form_executor.DISPOSE_EQUIP_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': EXCHANGE_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def exchange_asset(n_clicks):
    return nav_sys.navigate_forward(exchange_asset_layout, EXCHANGE_BTN, n_clicks, form_executor.EXCHANGE_EQUIP_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': INVEST_ASSET_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def invest_personal_asset(n_clicks):
    return nav_sys.navigate_forward(invest_asset_layout, INVEST_ASSET_BTN, n_clicks, form_executor.INVEST_PERSONAL_ASSET_STATE)


@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input({'type': USE_PERSONALLY, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def invest_personal_asset(n_clicks):
    return nav_sys.navigate_forward(use_asset_personally_layout, USE_PERSONALLY, n_clicks, form_executor.USE_ASSET_PERSONALLY)




@callback(
    Output('layout-container-asset', 'children', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call = True
)
def back_clicked(n_clicks):
    # print('back clicked', n_clicks)
    return nav_sys.get_back()


