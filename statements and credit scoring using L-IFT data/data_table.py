import pandas as pd
from dash import dash_table as dt
from dash import html, Dash
from ratios import unformat_num

COLORED = 'colored'
UNCOLORED = 'uncolored'

def from_dataframe(df: pd.DataFrame, table_type: str) -> html.Div:
    '''Table type can be colored or uncolored'''
    rows = []
    for x, row in df.iterrows():
        r = []
        y = 0
        for item in row:
            class_name = ''
            num_form = ''
            try:
                num_form = unformat_num(item)
                if num_form > 0:
                    class_name = 'table-positive'
                elif num_form < 0:
                    class_name = 'table-negative'
                else:
                    class_name = 'table-zero'
            except (ValueError, TypeError):
                num_form = item
                class_name = 'table-zero'
            
            r.append(
                    html.Td(
                        html.Div(
                            [
                                html.P(item)
                            ],
                            className=class_name
                        )
                    )
                    )
            y += 1
        

        rows.append(html.Tr(children=r))
    
    
    return html.Div(
        [
            html.Table(
                children=[
                    html.Tr(
                        children=[
                            html.Th(col)
                            # for col in list(df.columns) + ['']
                            for col in list(df.columns)
                        ]
                    )
                ] + rows,
                className=f'table-{table_type}'
            )
        ]
    )


def df_to_datatable2(df:pd.DataFrame):
    return html.Div(
        [
    
            dt.DataTable(
                df.to_dict('records'),
                [
                    {'name': i, 'id': i} for i in df.columns
                ],
                # id=table_id,
                style_table={
                    # 'max-width': '700px',  # Set the table width
                    'margin': '1rem auto',  # Center-align the table horizontally
                    # 'box-shadow': '0 0 20px 2px #0c070217'
                },
                
                # style_data={
                #     'backgroundColor': '#FFF8DC',
                #     # 'font-size': '1rem'
                #     },
                # style_header={
                #     'backgroundColor': '#00AE9F',
                #     'border': 'none',
                #     'color': 'white',
                #     # 'font-size': '1rem'
                #     },
                # style_cell={
                #     'font-family': 'Times New Roman',
                #     'padding': '0.5rem'
                #     # "border": "1px solid black",
                # },
            )           
            
        ], className='data-table')


def df_to_datatable(df:pd.DataFrame, color_it:bool=True):
    return from_dataframe(
        df, COLORED if color_it else UNCOLORED
        )





if __name__ == '__main__':
    app = Dash(__name__)
    data = pd.DataFrame(
        {
            'categories': ['processing cost','mechanical properties','chemical stability',
                'thermal stability', 'device integration'],
            'Industry Average': list(map(lambda x:f'({x})', [1, 5, 2, 2, 3])),
            'Your performance': list(map(lambda x: f'{x}', [4, 3, 2.5, 1, 2]))
        }
    )
    app.layout = html.Div(
        [
            html.H1('Good morning Vietnam!!'),
            df_to_datatable(data, False)
        ]
    )
    app.run(debug=True)