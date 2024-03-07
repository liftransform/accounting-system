import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import ratio_graphs as rg
from dash import html, dcc



class Scale:
    GOOD_COLOR = '#2fbf8f'
    MEDIUM_COLOR = '#f3d193'
    BAD_COLOR = '#dc3545'
    AVERAGE_COLOR = 'rgba(251, 155, 95, 1)'
    CURRENT_VALUE_COLOR = 'rgba(32, 105, 154, 1)'

    def __init__(self, title: str):
        self.title = title
        self.figure=go.Figure()
        self.annotations = []

    def _draw_rectange_from_corner(self, x0: float, y0:float, label:str, label_position:str, width:float=0.25, height=1.5, fill_color='orange'):
        self.figure.add_trace(go.Scatter(
            x=[x0, x0, x0+width, x0+width, x0],
            y=[y0-height, y0, y0, y0-height, y0-height],
            fillcolor=fill_color,
            fill='toself',
            text=label,
            textposition=label_position,
            mode='lines',
            line=dict(
                color='rgba(0,0,0,0)'
            )

        ))

        self.annotations.append(dict(
            x=x0 + width/2, y=y0 - height/2, 
            text=label, showarrow=False,
            font=dict(
                family='Arial', size=18,
                color='white'
            ))
        )

    def _draw_pointer(self, x0:float, y0:float, label:str, label_position:str, width: float=0.25, height=1.5,fill_color='green', bottom=False):
        self.figure.add_trace(go.Scatter(
            x=[
                x0-width/2, x0+width/2, 
                x0 + width/2, x0, 
                x0-width/2, x0-width/2
            ],
            y=[
                y0+height/2, y0 + height/2,
                y0-height/4, y0-height/2,
                y0-height/4, y0+height/2],
            fill="toself",
            fillcolor=fill_color,
            text=label,
            textposition=label_position,
            mode='lines',
            line=dict(
                # color='rgba(0, 0, 0, 0)'
                color='white'
            )
        ))

        self.annotations.append(dict(
            x=x0, y= y0 + height*0.5 if bottom else y0 + height*0.5 + 0.2,
            text=label, showarrow=True,
            font=dict(
                family='Arial', size=16,
                color='rgb(67, 67, 67)',
            ),
        ),
        )


    def draw(self, x0:float, y0:float, bad_end: float, medium_end:float, good_end:float, current_value:float, average= None, height=1):
        POINTER_HEIGHT = height*1.5
        POINTER_WIDTH = 0.3 * (good_end - x0) / 6


        average = medium_end if average == None else average
        self.annotations = []

        self.annotations.append(dict(
            x=x0, y= y0 + height,
            text=self.title, showarrow=False,
            font=dict(
                family='Arial', size=25,
                color='rgb(67, 67, 67)',
            ),
        ),
        )


        if (bad_end-x0) > 0:
            self._draw_rectange_from_corner(x0, y0, 'Bad', 'middle center', bad_end-x0, height, Scale.BAD_COLOR)
        
        if (medium_end-bad_end) > 0:
            self._draw_rectange_from_corner(bad_end, y0, 'Medium', 'middle center', medium_end-bad_end, height, Scale.MEDIUM_COLOR)
        
        if (good_end -medium_end) > 0:
            self._draw_rectange_from_corner(medium_end, y0, 'Good', 'middle center', good_end-medium_end, height, Scale.GOOD_COLOR)

        self._draw_pointer(average, y0 - height/2, 'Industry Average', 'top right', POINTER_WIDTH, POINTER_HEIGHT, fill_color=Scale.AVERAGE_COLOR,bottom=False)
        self._draw_pointer(current_value, y0 - height/2, 'Your Score', 'top right', POINTER_WIDTH, POINTER_HEIGHT, fill_color=Scale.CURRENT_VALUE_COLOR, bottom=True)
        

        self.figure.update_layout(
            annotations=self.annotations,
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                showline=False,
                # showticklabels=False,
                # zeroline=False,
                # domain=[0.15, 1]
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            # height=300,
        )


def draw_scale_for(res_id:int, ratio_df:pd.DataFrame, ratio_type:str) -> go.Figure:
    industry_data = rg.get_industry_data_for(res_id, ratio_df)
    industry_ratio = industry_data[[rg.RES, ratio_type]]
    res_ratio = industry_ratio[industry_ratio[rg.RES] == res_id].reset_index().drop(columns='index')[ratio_type][0]
    if pd.isna(res_ratio):
        return None
    start = industry_ratio[ratio_type].min()
    end = industry_ratio[ratio_type].max()
    value = res_ratio
    avg = industry_ratio[ratio_type].mean()

    ratio_scale = Scale(ratio_type)
    ratio_scale.draw(
        x0=start, y0=0, 
        bad_end=0, medium_end=avg, good_end=end,
        current_value=value, average=avg
    )

    return ratio_scale.figure



def ratio_visuals(res_id:int) -> html.Div:
    fig_collection = []

    for ratio_type in [rg.LIQUDITY, rg.PROFITABIITY, rg.SAVINGS, rg.ASSET_MGMT, rg.DEBT_MGMT]:
        fig = draw_scale_for(res_id, rg.ratio_demo_data, ratio_type)
        if fig != None: fig_collection.append(fig)

    scales = html.Div([
        dcc.Graph(
            figure=fig,
            className='ratio-graph'
        )
        for fig in fig_collection
    ],
    className='scales'
    # className='gauges'
    )
    return html.Div(
        [
            html.Div([
                # html.H2('You performance relative to other firms'),
                dcc.Graph(
                    figure=rg.draw_spider_for(res_id, rg.ratio_demo_data),
                    className='spider-graph'
                    ),
                scales,
            ], className='ratio-graph-container')
        ]
    )

    
if __name__ == '__main__':
    from dash import Dash

    test = Dash(__name__)

    pm = Scale('Profit Margin')
    pm.draw(-2, 0, 0, 0.4, 1, 0.6)
    test.layout = html.Div(
        [
            # dcc.Graph(figure=draw_scale_for(4425, rg.ratio_demo_data, rg.PROFITABIITY), style={
            #     'max-width':'1000px',
            #     # 'max-height':'200px'
            # })
            ratio_visuals(4425)
        ]
    )
    test.run(debug=True)

