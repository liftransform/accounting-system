import dash
from dash import html, dcc, Input, Output

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        html.H1('Analytics')
    ],
)