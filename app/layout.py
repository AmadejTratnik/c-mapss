from dash import  html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from data_access import get_files_with_prefix

N = 6
df = pd.DataFrame()

directory_path = './data/'
prefix_list = ['train_', 'test_']

layout = html.Div(
    children=[
        html.H2("Prediction of Remaining Useful Life of JET engine",style={"textAlign":"center"}),
        dbc.Row(
            style={'margin':'1%'},
            children=[
            dbc.Col(width=2,className="dash-bootstrap",children=[
                    html.Label("FD choice"),
                    dcc.Dropdown(options = [{'label':x.replace('.txt', ''),'value':x} for x in get_files_with_prefix(directory_path, prefix_list)], id='fd-choice-dropdown'),
            ]),
                dbc.Col(width=4,children=[
                    html.Label("Unit choice"),
                    dcc.Loading(
                    dcc.Slider(1, 20,1,value=1,id='unit-slider', tooltip={"placement": "bottom", "always_visible": True},
                               marks = {1:"1",20:"20"}))
                ]),
            dbc.Col(width=2,className="dash-bootstrap",children=[
                    html.Label("Sensor measurements choice"),
                    dcc.Loading(
                    dcc.Dropdown(options= [], multi=True, id='sensor-measurement-dropdown'),)
            ]),
            dbc.Col(width=2,className="dash-bootstrap",children=[
                                    html.Label("Operational settings"),
                    dcc.Loading(
                    dcc.Dropdown(options=[],id='operational-settings-dropdown'),)
            ]),

              dbc.Col(width=2,children=[
                  html.Label("Toggle measurements"),
                  html.Button(children=["START"],id="toggle-button",className="dash-bootstrap-button"),
            ]),
        ],
        ),
        
        dbc.Row(
            id="sensor-measurements-row",
            style={'margin':'1%'},
            children=[],
        ),

       dbc.Row(
            id="rul-and-operational",
            style={'margin':'1%'},
            children=[dbc.Col(width=6, children=[
                    html.P("RUL PREDICTION"),
                    dcc.Graph(
                        id = {'type':'graph','id':f'graph-RUL'},
                        config={'displayModeBar': False},
                        style={'height': '200px'},
                        figure=go.Figure(
                            data=[go.Scattergl(x=[], y=[], mode='lines', line=dict(color='lightgreen'))],
                            layout=dict(paper_bgcolor="rgba(0, 0, 0, 0)", plot_bgcolor="rgba(0, 0, 0, 0)",
                                        xaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False,fixedrange=True),
                                        yaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False,fixedrange=True),
                                        margin=dict(t=0, b=0, l=0, r=0),
                                        autosize=True)
                        )
                    ),
                ],style={'border': '1px solid white', 'padding': '10px','margin':'5px'}),
                dbc.Col(width=2)],
        ),

        dcc.Interval(id="interval", interval=50, max_intervals=100,disabled=True),
        dcc.Store(id='data-store',data={}),
        dcc.Store(id='graph-data-store',data={}),
    
    ],
)