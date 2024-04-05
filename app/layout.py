from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from data_access import get_files_with_prefix

N = 6
df = pd.DataFrame()

directory_path = './data/processed/'
prefix_list = ['train_', 'test_']

layout = html.Div(
    children=[
        html.H2("Fault Detection of a JET Engine", style={"textAlign": "center"}),
        dbc.Row(
            style={'margin': '1%'},
            children=[
                dbc.Col(width=2, className="dash-bootstrap", children=[
                    html.Label("FD choice"),
                    dcc.Dropdown(
                        options=[{'label': x.replace('.csv', '').replace(directory_path, ''), 'value': x} for x in
                                 get_files_with_prefix(directory_path, prefix_list)], id='fd-choice-dropdown'),
                ]),
                dbc.Col(width=4, children=[
                    html.Label("Unit choice"),
                    dcc.Loading(
                        dcc.Slider(1, 20, 1, value=1, id='unit-slider',
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   marks={1: "1", 20: "20"}))
                ]),
                dbc.Col(width=2, className="dash-bootstrap", children=[
                    html.Label("Sensor measurements choice"),
                    dcc.Loading(
                        dcc.Dropdown(options=[], multi=True, id='sensor-measurement-dropdown'), )
                ]),
                dbc.Col(width=2, className="dash-bootstrap", children=[
                    html.Label("Operational settings"),
                    dcc.Loading(
                        dcc.Dropdown(options=[], id='operational-settings-dropdown'), )
                ]),

                dbc.Col(width=2, children=[
                    html.Label("Toggle measurements"),
                    html.Button(children=["START"], id="toggle-button", className="dash-bootstrap-button"),
                ]),
            ],
        ),

        dbc.Row(
            id="sensor-measurements-row",
            style={'margin': '1%'},
            children=[],
        ),

        dbc.Row(
            id="fd-and-operational",
            style={'margin': '1%'},
            children=[dbc.Col(width=2,
                              id="graph-fault_calculated-div",
                              children=[

                                  html.P("MEASURED FAULT"),
                                  dcc.Graph(
                                      id={'type': 'graph', 'id': f'graph-fault_detected'},
                                      config={'displayModeBar': False},
                                      style={'height': '200px'},
                                      figure=go.Figure(
                                          data=[go.Scattergl(x=[], y=[], mode='lines', line=dict(color='blue'))],
                                          layout=dict(paper_bgcolor="rgba(0, 0, 0, 0)", plot_bgcolor="rgba(0, 0, 0, 0)",
                                                      xaxis=dict(showline=False, visible=False, showgrid=False,
                                                                 zeroline=True,
                                                                 fixedrange=False),
                                                      yaxis=dict(showline=False,
                                                                 range=[0, 2],
                                                                 visible=False, showgrid=False,
                                                                 zeroline=False,
                                                                 fixedrange=True),
                                                      margin=dict(t=0, b=0, l=0, r=0),
                                                      autosize=True, )
                                      )
                                  ),
                              ], style={'border': '1px solid white', 'padding': '10px', 'margin': '5px',
                                        'display': 'None'}),

                      dbc.Col(width=2, children=[
                          html.P("PREDICTED FAULT"),
                          dcc.Graph(
                              id={'type': 'graph1', 'id': f'graph-fault_predicted'},
                              config={'displayModeBar': False},
                              style={'height': '200px'},
                              figure=go.Figure(
                                  data=[go.Scattergl(x=[], y=[], mode='lines',
                                                     line=dict(color='red')),
                                        ],
                                  layout=dict(paper_bgcolor="rgba(0, 0, 0, 0)", plot_bgcolor="rgba(0, 0, 0, 0)",
                                              xaxis=dict(showline=False, visible=False, showgrid=True, zeroline=False,
                                                         fixedrange=False),
                                              yaxis=dict(showline=False,
                                                         range=[0, 2],
                                                         visible=False, showgrid=False,
                                                         zeroline=False,
                                                         fixedrange=True),
                                              margin=dict(t=0, b=0, l=0, r=0),
                                              autosize=True, )
                              )
                          ),
                      ], style={'border': '1px solid white', 'padding': '10px', 'margin': '5px'}),
                      dbc.Col(width=2)],
        ),

        dcc.Interval(id="interval", interval=100, max_intervals=100, disabled=True),
        dcc.Store(id='data-store', data={}),
        dcc.Store(id='graph-data-store', data={}),
        dcc.Store(id='unit-prediction-vector', data=[]),
    ],
)
