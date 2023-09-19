import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
from variables import HIGHLIGHT_SIZE, DEFAULT_SIZE, SELECTED, styles, election_years
from database_engine import engine
import plotly.graph_objs as go
import numpy as np
import pandas as pd

dash.register_page(__name__,
                path='/',
                title='Home',
                name='Home')

query = "select party, year, candidate from {}\
        where position = 1".format('final')
data = pd.read_sql_query(query,engine)

layout = html.Div([
html.H3("Select the year to view the result summary!", style={"margin-left":20}), 
    dcc.Store(id='data_store',data=[]),
    dcc.Store(id='graph',data=[]),
    dcc.Store(id='year',data=2019),
    html.Div([
        dcc.Dropdown(id='drop',options=election_years, value=2019, placeholder='Filter by year...')],
        style={"width": "100%"}),
    dcc.Graph(id='g1')
        ])

@callback(Output('data_store', 'data'),
    Input('year', 'data'))

def data_year_store(year_selected):
    if not year_selected:
        return data.to_dict('records')
    else:
        data_year = data[data['year']==year_selected]
        return data_year.to_dict('records')

@callback(
    Output('g1','figure'),
    Input('graph','data'),
    Input('year','data'))
def g1(data,year):
    result = pd.DataFrame.from_dict(data)
    fig = go.Figure()
    for family, subject in result.groupby('party'):
        party_name = subject['party_names'].iloc[0]
        no_seats = len(subject)
        fig.add_trace(go.Scatter(
            x=subject.x,
            y=subject.y,
            mode="markers",
            **styles[party_name],
            name=party_name,
            customdata = subject.party,
            hoverinfo='none',
            hovertemplate='<b>Party:{}<br>Seats:{}</b><extra></extra>'.format(party_name,no_seats)            
            ))
    fig.update_layout(title={'text':"Lokshabha Elections {} Summary".format(year),'y':0.9,'x':0.5,
                        'xanchor': 'center', 'yanchor': 'top','font':dict(size=25)},height=700, 
                        hovermode='closest', uirevision='static',paper_bgcolor='white',
                        plot_bgcolor='white',showlegend=True,legend_itemclick='toggleothers',
                        xaxis={'showgrid':False,'zeroline': False,'visible': False},
                        yaxis={'showgrid':False,'zeroline': False,'visible': False},
                        )
    return fig
    
@callback(
    Output('g1', 'figure',allow_duplicate=True),
    inputs=[
    Input('g1', 'hoverData'),
    Input('g1', 'figure')],
    prevent_initial_call=True)
    
def hover(hover_data,fig):
    global SELECTED
    if hover_data is not None:
        if SELECTED is not None:
            old = SELECTED
            fig['data'][SELECTED]['marker']['size'] = DEFAULT_SIZE

        SELECTED =family= hover_data['points'][0]['customdata']
        fig['data'][family]['marker']['size'] = HIGHLIGHT_SIZE
    return fig