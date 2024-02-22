import pandas as pd
from dash import dash_table as dt

def df_to_datatable(df:pd.DataFrame):
    return dt.DataTable(
        df.to_dict('records'),
        [
            {'name': i, 'id': i} for i in df.columns
        ],
        # id=table_id,
        style_table={
            'max-width': '700px',  # Set the table width
            'margin': '1rem auto',  # Center-align the table horizontally
            'box-shadow': '0px 2px 10px rgba(0, 0, 0, 0.267)'
        },
        style_data={
            'backgroundColor': '#FFF8DC',
            # 'font-size': '1rem'
            },
        style_header={
            'backgroundColor': '#00AE9F',
            'border': 'none',
            'color': 'white',
            # 'font-size': '1rem'
            },
        # style_cell={
        #     'font-family': 'Times New Roman',
        #     'padding': '0.5rem'
        #     # "border": "1px solid black",
        # },
    )
    