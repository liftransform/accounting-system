import dash
from dash import html, dcc, Input, Output, callback, ALL
import inventory
from nav_system import NavSystem
import datetime as dt
import form_executor
import data_table

dash.register_page(__name__)


#----------BTN IDS

#----------

BTN_COLLECTION = [
    
] 
#--------

btn_counter = 0

def standard_layout():
    global btn_counter
    

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
            id='layout-container'
        )
    ],
)

def template_layout():
    global btn_counter
    layout = html.Div(
        [
            html.Form(
                [
                    html.H2(''),
                    dcc.DatePickerSingle(date=dt.date.today()),

                
                    dcc.Textarea(placeholder='Note on', name=form_executor.NOTE),
                    
                    html.Button('Submit')
                ],
                action='/post', method='post'
            )

        ]
    )
    btn_counter += 1
    return layout


#-------------------------------------Buying inventory
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


