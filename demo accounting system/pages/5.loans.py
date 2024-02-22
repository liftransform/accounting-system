import dash
from dash import html, dcc, Input, Output, callback, ALL
import loans
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table

dash.register_page(__name__)


#----------BTN IDS
BORROW_BTN = 'borrow-btn'
PAY_INT_BTN = 'pay-int-btn'
REPAY_BTN = 'repay-loan-btn'

LEND_BTN = 'lend-btn'
RECEIVE_INT_BTN = 'receive-int-btn'
RECEIVE_LOANS_BTN = 'receive-loan-btn'
#----------

BTN_COLLECTION = [
    BORROW_BTN, PAY_INT_BTN, REPAY_BTN,
    LEND_BTN, RECEIVE_INT_BTN, RECEIVE_LOANS_BTN
] 
#--------

btn_counter = 0

def standard_layout():
    global btn_counter
    my_borrowings_df = loans.Creditor.table_form_multiple()
    my_borrwings_table = data_table.df_to_datatable(my_borrowings_df)

    my_loans_df = loans.Borrower.table_form_multiple()
    my_loans_table = data_table.df_to_datatable(my_loans_df)

    int_btn = None
    repay_btn = None
    rec_int_btn = None
    rec_loan_btn = None

    if len(my_borrowings_df) > 0:
        # print('Pay interest and loan values have been set')
        int_btn = html.Button('Pay Interest', id={'type': PAY_INT_BTN, 'index': btn_counter})
        
        repay_btn = html.Button('Repay Borrowings', id={'type': REPAY_BTN, 'index': btn_counter})
    # else:
    #     print('Not Borrowings for now')

    if len(my_loans_df) > 0:
        # print('Receive interest and loan values have been set')
        rec_int_btn =  html.Button('Receive Interest', id={'type': RECEIVE_INT_BTN, 'index': btn_counter})

        rec_loan_btn = html.Button('Get loan back', id={'type': RECEIVE_LOANS_BTN, 'index': btn_counter})
    # else:
    #     print('Not loans given for now')

    layout = html.Div(
        [
            html.Div([
                html.H2('Loans Takens'),
                my_borrwings_table,
                html.Button('Borrow More', id={'type': BORROW_BTN, 'index': btn_counter}),
                int_btn,
                repay_btn                

            ]),
            html.Div([
                html.H2('Loans Given'),
                my_loans_table,
                html.Button('Lend More', id={'type': LEND_BTN, 'index': btn_counter}),
                rec_int_btn,
                rec_loan_btn
            ])
        ]
    )
    btn_counter += 1
    return layout



def take_loan_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    dcc.Input(placeholder='Lender\'s Name', name=form_executor.LENDER_NAME),
                    dcc.Input(type='number', placeholder='Loan Amount', name=form_executor.AMOUNT),
                    html.Select([
                        html.Option(loans.SHORT),
                        html.Option(loans.LONG),
                    ], name=form_executor.LOAN_TYPE),
                    dcc.Textarea(placeholder='Note on new loan', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )
    btn_counter += 1
    return layout



def pay_int_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    
                    html.Select([
                        html.Option(f'{lender.id}, {lender.name}, {lender.unpaid_amount()}')
                        for lender in loans.Creditor.get_unpaid_loans()
                    ], name=form_executor.LOAN),
                    dcc.Input(type='number', placeholder='Interest Amount', name=form_executor.AMOUNT),
                    dcc.Textarea(placeholder='Note on interest payment', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )
    btn_counter += 1
    return layout



def pay_loan_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),

                    html.Select([
                        html.Option(f'{lender.id}, {lender.name}, {lender.unpaid_amount()}')
                        for lender in loans.Creditor.get_unpaid_loans()
                    ], name=form_executor.LOAN),
                    dcc.Input(type='number', placeholder='Repaid Amount', name=form_executor.AMOUNT),


                    dcc.Textarea(placeholder='Note on paying back loan', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout



def give_loan_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    dcc.Input(placeholder='Borrower\'s Name', name=form_executor.BORROWER_NAME),
                    dcc.Input(type='number', placeholder='Loan Amount', name=form_executor.AMOUNT),
                    html.Select([
                        html.Option(loans.SHORT),
                        html.Option(loans.LONG),
                    ], name=form_executor.LOAN_TYPE),
                    dcc.Textarea(placeholder='Note on new loan given', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )
    btn_counter += 1
    return layout



def receive_interst_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    
                    html.Select([
                        html.Option(f'{borrower.id}, {borrower.name}, {borrower.unreceived_amount()}')
                        for borrower in loans.Borrower.get_unreceieved_loans()
                    ], name=form_executor.LOAN),
                    dcc.Input(type='number', placeholder='Interest Received', name=form_executor.AMOUNT),
                    dcc.Textarea(placeholder='Note on interest received', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )
        ]
    )
    return layout



def receive_loan_repayment_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    dcc.DatePickerSingle(date=dt.date.today()),
                    
                    html.Select([
                        html.Option(f'{borrower.id}, {borrower.name}, {borrower.unreceived_amount()}')
                        for borrower in loans.Borrower.get_unreceieved_loans()
                    ], name=form_executor.LOAN),
                    dcc.Input(type='number', placeholder='Amount', name=form_executor.AMOUNT),
                    dcc.Textarea(placeholder='Note on Borrower\'s repayment', name=form_executor.NOTE),
                    
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
        html.H1('Loans'),
        html.Div(
            [
                html.Button('Back', id='back-btn')
            ]
        ),
        html.Div(
            [
                standard_layout()
            ],
            id='layout-container-loans'
        )
    ],
)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': BORROW_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def take_loan(n_clicks):
    return nav_sys.navigate_forward(take_loan_layout, BORROW_BTN, n_clicks, form_executor.BORROW_STATE)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': PAY_INT_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def pay_int(n_clicks):
    return nav_sys.navigate_forward(pay_int_layout, PAY_INT_BTN, n_clicks, form_executor.PAY_INTEREST_STATE)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': REPAY_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def repay_loan(n_clicks):
    return nav_sys.navigate_forward(pay_loan_layout, REPAY_BTN, n_clicks, form_executor.REPAY_LOAN)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': LEND_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def give_loan(n_clicks):
    return nav_sys.navigate_forward(give_loan_layout, LEND_BTN, n_clicks, form_executor.GIVE_LOAN_STATE)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': RECEIVE_INT_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def get_interest(n_clicks):
    return nav_sys.navigate_forward(receive_interst_layout, RECEIVE_INT_BTN, n_clicks, form_executor.GET_INTEREST_STATE)


@callback(
    Output('layout-container-loans', 'children',allow_duplicate=True),
    Input({'type': RECEIVE_LOANS_BTN, 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True   
)
def get_interest(n_clicks):
    return nav_sys.navigate_forward(receive_loan_repayment_layout, RECEIVE_LOANS_BTN, n_clicks, form_executor.GET_BORROWER_REPAYMENT)






@callback(
    Output('layout-container-loans', 'children', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call = True
)
def back_clicked(n_clicks):
    # print('back clicked', n_clicks)
    return nav_sys.get_back()


