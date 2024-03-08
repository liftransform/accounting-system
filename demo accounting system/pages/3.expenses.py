import dash
from dash import html, dcc, Input, Output, callback, ALL
import inventory
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table

dash.register_page(__name__)


#----------BTN IDS
RENT_EXP_BTN ='ren-exp-btn'
UTILITY_EXP_BTN ='utility-exp-btn'
AD_EXP_BTN ='ad-exp-btn'
SALARY_EXP_BTN ='salary-exp-btn'
OTHER_EXP_BTN ='other-exp-btn'

#----------

BTN_COLLECTION = [
    RENT_EXP_BTN, UTILITY_EXP_BTN,
    AD_EXP_BTN, SALARY_EXP_BTN,
    OTHER_EXP_BTN,
] 
#--------

btn_counter = 0

def _simple_exp_layout(title):
    return html.Div(
        [
            html.Form(
                [
                    html.H3(title),
                    dcc.DatePickerSingle(date=dt.date.today()),
                    dcc.Input(type='number', name=form_executor.AMOUNT, placeholder='Amount', required=True),
                    html.Select(
                        [
                            html.Option('For Business', value=form_executor.FOR_BUSINESS),
                            html.Option('For Personal', value=form_executor.FOR_PERSONAL),
                        ],
                        name=form_executor.BUSINESS_PERSONAL
                    ),
                    dcc.Textarea(
                        placeholder='Note',
                        name=form_executor.NOTE
                    ),
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )


def standard_layout():
    global btn_counter
    btn_counter += 1
    return html.Div([
        html.Button('Rent', id={'type': RENT_EXP_BTN, 'index': btn_counter}),
        html.Button('Utility', id={'type': UTILITY_EXP_BTN, 'index': btn_counter}),
        html.Button('Advertisment', id={'type': AD_EXP_BTN, 'index': btn_counter}),
        html.Button('Salaries', id={'type': SALARY_EXP_BTN, 'index': btn_counter}),
        html.Button('other', id={'type': OTHER_EXP_BTN, 'index': btn_counter}),
    ])



def rent_layout():
    return _simple_exp_layout('Rent')


def utility_layout():
    return _simple_exp_layout('Utility')


def ad_layout():
    return _simple_exp_layout('Advertisment')


def salary_layout():
    return _simple_exp_layout('Salary')


def other_layout():
    return _simple_exp_layout('Other')


#------------------------ Navigation related
current_layout = standard_layout



nav_sys = NavSystem(BTN_COLLECTION, standard_layout)

#------------------------


layout = html.Div(
    [
        html.H1('Expense'),
        html.Div(
            [
                html.Button('Back', id='back-btn')
            ]
        ),
        html.Div(
            [
                standard_layout()
            ],
            id='layout-container-exp'
        )
    ],
)


#-------------------------------------Buying inventory
@callback(
    Output('layout-container-exp', 'children',allow_duplicate=True),
    Input({'type': RENT_EXP_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_rent(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(rent_layout, RENT_EXP_BTN, n_clicks, form_executor.RENT_EXP_STATE)

@callback(
    Output('layout-container-exp', 'children',allow_duplicate=True),
    Input({'type': UTILITY_EXP_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_utility(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(utility_layout, UTILITY_EXP_BTN, n_clicks, form_executor.UTILIY_EXP_STATE)

@callback(
    Output('layout-container-exp', 'children',allow_duplicate=True),
    Input({'type': AD_EXP_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_advertisment(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(ad_layout, AD_EXP_BTN, n_clicks, form_executor.AD_EXP_STATE)


@callback(
    Output('layout-container-exp', 'children',allow_duplicate=True),
    Input({'type': SALARY_EXP_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_salaries(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(salary_layout, SALARY_EXP_BTN, n_clicks, form_executor.SALARY_EXP_STATE)


@callback(
    Output('layout-container-exp', 'children',allow_duplicate=True),
    Input({'type': OTHER_EXP_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_other_exp(n_clicks):
    # print(BUY_INV, 'clicked', n_clicks)
    return nav_sys.navigate_forward(other_layout, OTHER_EXP_BTN, n_clicks, form_executor.OTHER_EXP_STATE)





@callback(
    Output('layout-container-exp', 'children', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call = True
)
def back_clicked_exp(n_clicks):
    # print('back clicked', n_clicks)
    return nav_sys.get_back()


