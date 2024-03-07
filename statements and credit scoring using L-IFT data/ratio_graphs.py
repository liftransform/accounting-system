import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

RES = 'Respondent'
INDUSTRY = 'Industry'
LIQUDITY = 'Liqudity'
PROFITABIITY = 'Profitability'
ASSET_MGMT = 'Asset management'
DEBT_MGMT = 'Debt management'
SAVINGS = 'Savings'
CR = 'Current Ratio'
PM = 'Profit Margin'
EM = 'Equity Multiplier'
WR = 'Withdrawal Ratio'
TATO = 'TATO'


ratio_data = pd.read_excel(r'ratio_df_combined.xlsx', sheet_name='ratios_clean')

demographic_data = pd.read_excel(r'lift_data\Expense Report - Mon Feb 13 2023.xlsx', sheet_name='Demographics')

ratio_demo_data = pd.merge(
    demographic_data[['Respondent ID', 'Industry']].rename(columns={'Respondent ID': 'Respondent'}),
    ratio_data,
    'outer', 
    'Respondent'
)




def get_ratios_for(res_id:int, ratio_df:pd.DataFrame):
    filtered = ratio_df[ratio_df[RES] == res_id].reset_index().drop(columns='index')
    filtered.loc[:,SAVINGS] = filtered[WR].apply(lambda x: 1 - x if x >= 0 else x - 1)
    to_return = filtered.rename(columns={
        CR: LIQUDITY,
        PM: PROFITABIITY,
        EM: DEBT_MGMT,
        TATO: ASSET_MGMT
    })[[RES, INDUSTRY, LIQUDITY, PROFITABIITY, ASSET_MGMT, DEBT_MGMT, SAVINGS]]
    return to_return


def get_industry_data_for(res_id: int, ratio_df: pd.DataFrame):
    industry_name = ratio_df[ratio_df[RES] == res_id].reset_index().drop(columns='index')[INDUSTRY][0]
    # print(industry_name)
    industry_data = ratio_df[ratio_df[INDUSTRY] == industry_name]
    performances = []
    for res in industry_data[RES].unique():
        performances.append(get_ratios_for(res, ratio_df))
    
    return pd.concat(performances).reset_index().drop(columns='index')


def draw_guage(title: str, start:float, end:float, industry_average: float, value: float) -> go.Figure:

    bad_color = '#ea5b0c'
    good_color = '#00ae9f'
    middle_color = "#f3d193"
    
    bad_exists = True if start < 0 else False
    middle_exists = True if industry_average > 0 else False
    good_exists = True if end > 0 else False

    if not middle_exists:
        industry_average = 0
    if not good_exists:
        industry_average = end

    bad_region = {'range': [start, 0], 'color': bad_color} if bad_exists else None
    middle_region = {'range': [0, industry_average], 'color': middle_color} if middle_exists else None 
    good_region = {'range': [industry_average, end], 'color': good_color} if good_exists else None

    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = value,
    mode = "gauge+number",
    title = {'text': title},
    # delta = {'reference': 380},
    gauge = {'axis': {'range': [start, end]},
             'bar': {'color': "white"},
             'steps' : [region for region in [bad_region, middle_region, good_region] if region != None],
             'threshold' : {'line': {'color': "white", 'width': 4}, 'thickness': 1, 'value': value}}))

    fig.update_layout(paper_bgcolor = "lavender", font = {'color': "grey", 'family': "Arial"})

    return fig




def draw_guage_relative(title: str, start:float, end:float, industry_average: float, value: float) -> go.Figure:

    bad_color = '#dc3545'
    good_color = '#2fbf8f'
    middle_color = "#f3d193"



    bad_range = [start, 0]
    middle_range = [0, industry_average]
    good_range = [industry_average, end]

    if end <= 0:
        good_range = [0, 0]

    if industry_average < 0:
        middle_range = [industry_average, 0]
        good_range = [0, end]
        middle_color = '#f69f71'
    
    #-----standardizing the values between 0-100% so ratios can be interpreted the same
    new_industry_average = (industry_average - start) * 100 / (end-start)
    new_start = 0
    new_end = 100
    zero = (0 - start) * 100 / (end - start)

    value = (value - start) * 100 / (end-start)
    if value < new_start: value = new_start
    if value > new_end: value = new_end

    #TODO: continue here

    bad_range = [new_start, zero]
    middle_range = [
        zero if middle_range[0] == 0 else new_industry_average,
        zero if middle_range[1] == 0 else new_industry_average
    ]
    good_range = [
        zero if good_range[0] == 0 else new_industry_average,
        zero if good_range[1] == zero else new_end
    ]
    #-------------------------------

    bad_region = {'range': bad_range, 'color': bad_color}
    middle_region = {'range': middle_range, 'color': middle_color}
    good_region = {'range': good_range, 'color': good_color}


    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = value,
    mode = "gauge+number",
    title = {'text': title},
    # delta = {'reference': 380},
    gauge = {'axis': {'range': [new_start, new_end]},
             'bar': {'color': "white"},
             'steps' : [region for region in [bad_region, middle_region, good_region] if region != None],
             'threshold' : {'line': {'color': "white", 'width': 4}, 'thickness': 1, 'value': value}}))


    #----coloring the text
    text_color = ''
    print(f'Title {title}: value is', value)
    for region in (bad_region, middle_region, good_region):
        min_value = region['range'][0]
        max_value = region['range'][1]
        if value >= min_value and value <= max_value:
            text_color = region['color']
            break
    #------------------

    fig.update_layout(paper_bgcolor = "white", font = {'color': text_color})

    return fig


def draw_spider(df: pd.DataFrame, categories:str, values:list[str], fill=True):
    fig = go.Figure()
    min_value = None
    max_value = None

    
    for val in values:
        fig.add_trace(go.Scatterpolar(
            r=df[val],
            theta = df[categories],
            name=val,
            mode='lines',
            fill='toself' if fill else None,
        ))

        if min_value == None:
            min_value = df[val].min()
            max_value = df[val].max()
            continue

        new_min = df[val].min()
        new_max = df[val].max()
        if new_min < min_value:
            min_value = new_min
        if new_max > max_value:
            max_value = new_max


    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[new_min*0.5, new_max*1.5]
        )),
    showlegend=True
    )

    return fig


def draw_spider2(df: pd.DataFrame, categories:str, values:list[str], fill=True):
    melted_df = df.melt(id_vars=[categories], value_vars=values)
    # display(melted_df)
    fig = px.line_polar(
        melted_df, r='value', theta=categories, 
        color='variable', line_close=True,
        color_discrete_sequence= ['#dc3545', '#2fbf8f']
    )
    fig.update_layout(
        plot_bgcolor = "white",
    )

    if fill:
        fig.update_traces(fill='toself')
    return fig


def draw_speedometer_for(res_id:int, ratio_df:pd.DataFrame, ratio_type:str) -> go.Figure:
    industry_data = get_industry_data_for(res_id, ratio_df)
    industry_ratio = industry_data[[RES, ratio_type]]
    res_ratio = industry_ratio[industry_ratio[RES] == res_id].reset_index().drop(columns='index')[ratio_type][0]
    if pd.isna(res_ratio):
        return None
    start = industry_ratio[ratio_type].min()
    end = industry_ratio[ratio_type].max()
    value = res_ratio
    avg = industry_ratio[ratio_type].mean()

    return draw_guage_relative(ratio_type, start, end, avg, value)


def draw_spider_for(res_id: int, ratio_df: pd.DataFrame):
    industry_data = get_industry_data_for(res_id, ratio_df)
    res_ratios = industry_data[industry_data[RES] == res_id].reset_index().drop(columns='index')
    ratio_types = [LIQUDITY, PROFITABIITY, ASSET_MGMT, DEBT_MGMT, SAVINGS]
    firm_values = []
    industry_values = []
    for rt in ratio_types:
        min_value = industry_data[rt].min()
        max_value = industry_data[rt].max()
        r_value = res_ratios[rt][0]
        firm_percentage = (r_value - min_value) * 100/ (max_value - min_value)
        
        middle = industry_data[rt].mean()
        industry_percentage = (middle - min_value) * 100 / (max_value - min_value)

        firm_values.append(firm_percentage)
        industry_values.append(industry_percentage)
    
    spider_df = pd.DataFrame(
        {
            'Type': ratio_types,
            'Industry': industry_values,
            'You': firm_values
        }
    )
    
    spider_df2 = spider_df[~spider_df['You'].isna()]
    # display(spider_df2)
    return draw_spider2(spider_df2, 'Type', ['Industry', 'You'], False)


def ratio_visuals(res_id:int):
    fig_collection = []

    for ratio_type in [LIQUDITY, PROFITABIITY, SAVINGS, ASSET_MGMT, DEBT_MGMT]:
        fig = draw_speedometer_for(res_id, ratio_demo_data, ratio_type)
        if fig != None: fig_collection.append(fig)

    guauges = html.Div([
        dcc.Graph(
            figure=fig,
            className='ratio-graph'
        )
        for fig in fig_collection
    ],
    className='gauges'
    )

    return html.Div(
        [
            html.Div([
                # html.H2('You performance relative to other firms'),
                dcc.Graph(
                    figure=draw_spider_for(res_id, ratio_demo_data),
                    className='spider-graph'
                    ),
                guauges,
            ], className='ratio-graph-container')
        ]
    )
