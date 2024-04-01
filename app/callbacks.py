from random import random

import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
import numpy as np

from app.data_access import get_dataframe
from layout import N
import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from modelling.inference import load_jet_model, predict_fault


def get_callbacks(app):
    model = load_jet_model('../modelling/FD001_model.keras')

    @app.callback(
        Output('interval', 'n_intervals'),
        Input('toggle-button', 'n_clicks'),
        State('interval', 'n_intervals'),
        State('interval', 'max_intervals'),
    )
    def start_interval_again(n, current_n, max_n):
        if current_n == max_n:
            return 0  # , [[] for _ in range(len(dash.callback_context.outputs_list[1]))]
        else:
            raise dash.exceptions.PreventUpdate

    @app.callback(Output('interval', 'disabled'),
                  Output('toggle-button', 'children'),
                  Input('toggle-button', 'n_clicks'),
                  State('interval', 'n_intervals'),
                  State('interval', 'max_intervals'),
                  prevent_initial_call=True)
    def toggle_interval(n, current_n, max_n):
        s = ["START", "STOP"]
        r = not (n % 2)
        return r, s[n % 2] if current_n != max_n else "START"

    @app.callback(
        Output("sensor-measurement-dropdown", "value"),
        Output("sensor-measurements-row", "children"),
        Input("sensor-measurement-dropdown", "value"),
        State("sensor-measurements-row", "children"),
        prevent_initial_call=True
    )
    def update_sensor_graph_row(sensors, old_graphs):
        if sensors is not None and len(sensors) >= N:
            return sensors, old_graphs

        graphs = []

        for sensor in sensors:
            graphs.append(
                dbc.Col(width=2, children=[
                    html.P(" ".join(sensor.split('_')).upper()),
                    dcc.Graph(
                        id={'type': 'graph', 'id': f'graph-{sensor}'},
                        config={'displayModeBar': False},
                        style={'height': '100px'},
                        figure=go.Figure(
                            data=[go.Scattergl(x=[], y=[], mode='lines', line=dict(color='lightgreen'))],
                            layout=dict(paper_bgcolor="rgba(0, 0, 0, 0)", plot_bgcolor="rgba(0, 0, 0, 0)",
                                        xaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False,
                                                   fixedrange=True),
                                        yaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False,
                                                   fixedrange=True),
                                        margin=dict(t=0, b=0, l=0, r=0),
                                        autosize=True)
                        )
                    ),
                ], style={'border': '1px solid white', 'padding': '10px', 'margin': '5px'})
            )
        return sensors, graphs

    @app.callback(
        Output("fd-and-operational", "children"),
        Input("operational-settings-dropdown", "value"),
        State("fd-and-operational", "children"),
        prevent_initial_call=True
    )
    def build_operations_and_prediction(setting, graphs):
        if not setting:
            graphs[2] = dbc.Col(width=2)
        else:
            graphs[2] = dbc.Col(width=2, children=[
                html.P(" ".join(setting.split('_')).upper()),
                dcc.Graph(
                    id={'type': 'graph', 'id': f'graph-{setting}'},
                    config={'displayModeBar': False},
                    style={'height': '200px'},
                    figure=go.Figure(
                        data=[go.Scattergl(x=[], y=[], mode='lines', line=dict(color='lightgreen'))],
                        layout=dict(paper_bgcolor="rgba(0, 0, 0, 0)", plot_bgcolor="rgba(0, 0, 0, 0)",
                                    xaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False),
                                    yaxis=dict(showline=False, visible=False, showgrid=False, zeroline=False),
                                    margin=dict(t=0, b=0, l=0, r=0),
                                    autosize=True)
                    )
                ),
            ], style={'border': '1px solid white', 'padding': '10px', 'margin': '5px'})
        return graphs

    @app.callback(
        Output("unit-slider", "disabled"),
        Output("operational-settings-dropdown", "disabled"),
        Output("sensor-measurement-dropdown", "disabled"),
        Input("toggle-button", "n_clicks")
    )
    def disable_dropdowns(n):
        if n:
            disabled = bool(n % 2)
            return disabled, disabled, disabled
        raise dash.exceptions.PreventUpdate

    @app.callback(
        Output("graph-fault_calculated-div", 'style'),
        Input('fd-choice-dropdown', 'value'),
        State("graph-fault_calculated-div", 'style'),
    )
    def toggle_calculated_graph(choice, style):
        if choice is None:
            raise dash.exceptions.PreventUpdate
        if "test" in choice:
            style['display'] = 'None'
        if "train" in choice:
            style['display'] = 'block'
        return style

    @app.callback(
        Output({'type': 'graph1', 'id': f'graph-fault_predicted'}, 'extendData'),
        Input('interval', 'n_intervals'),
        State("graph-fault_calculated-div", 'style'),
        State('unit-prediction-matrix', 'data'),
        prevent_initial_call=True
    )
    def update_calculated_graph(n_intervals, style, prediction_matrix):
        if style.get('display', "block") is None or not len(prediction_matrix):
            raise dash.exceptions.PreventUpdate
        new_x = prediction_matrix[n_intervals]
        new_x = np.array([[new_x]])
        new_y2 = predict_fault(model, new_x)
        y2_data = [{'x': [[n_intervals]], 'y': [[new_y2]]}, [0], 10]
        return y2_data

    @app.callback(
        Output({'type': 'graph', 'id': ALL}, 'extendData'),
        Input('interval', 'n_intervals'),
        State('graph-data-store', 'data'),
        prevent_initial_call=True
    )
    def update_operational_setting_graph(n_intervals, data):
        output_graphs = (dash.callback_context.outputs_list)
        if n_intervals == 0:
            raise dash.exceptions.PreventUpdate
        s = []

        result = [entry for entry in data if entry.get('time') == n_intervals][0]
        for x in output_graphs:
            current_value = x['id']['id'].split('graph-')[1]
            s.append([{'x': [[n_intervals]], 'y': [[result[current_value]]]}, [0], 10])
        return s

    @app.callback(
        Output('data-store', 'data'),
        Input('fd-choice-dropdown', 'value'),
        prevent_initial_call=True
    )
    def take_data(value):
        return get_dataframe(value)

    @app.callback(
        Output('unit-prediction-matrix', 'data'),
        Input('unit-slider', 'value'),
        State('data-store', 'data'),
    )
    def update_prediction_matrix(value, data):
        if not data or not len(data):
            raise dash.exceptions.PreventUpdate

        df = pd.DataFrame(data)
        df = df[df['unit_number'] == value]
        df.drop(columns=['unit_number', 'fault_detected'], inplace=True)
        time_data = []
        for _, row in df.iterrows():
            time_data.append(row.tolist()[1:])
        return time_data

    @app.callback(
        Output('unit-slider', 'min'),
        Output('unit-slider', 'max'),
        Output('unit-slider', 'marks'),
        Input('data-store', 'data'),
        prevent_initial_call=True
    )
    def define_slider(data):
        df = pd.DataFrame(data)
        l = df['unit_number'].unique()
        m = min(l)
        M = max(l)
        return m, M, {str(m): str(m), str(M): str(M)}

    @app.callback(
        Output('sensor-measurement-dropdown', 'options'),
        Input('data-store', 'data'),
        prevent_initial_call=True
    )
    def define_slider(data):
        df = pd.DataFrame(data)
        return [x for x in df.columns if x.startswith('sensor')]

    @app.callback(
        Output('operational-settings-dropdown', 'options'),
        Input('data-store', 'data'),
        prevent_initial_call=True
    )
    def define_slider(data):
        df = pd.DataFrame(data)
        return [x for x in df.columns if x.startswith('operational')]

    @app.callback(
        Output('graph-data-store', 'data'),
        Input('operational-settings-dropdown', 'value'),
        Input('sensor-measurement-dropdown', 'value'),
        Input('unit-slider', 'value'),
        State('data-store', 'data'),
        prevent_initial_call=True
    )
    def define_slider(operation, sensors, unit, data):
        df = pd.DataFrame(data)
        if unit and sensors and operation:
            df2 = df[df['unit_number'] == unit][sensors + [operation] + ['time'] + ['fault_detected']]
            return df2.to_dict('records')
        raise dash.exceptions.PreventUpdate

    @app.callback(
        Output('interval', 'max_intervals'),
        Input('graph-data-store', 'data'),
        prevent_initial_call=True
    )
    def define_slider(data):
        df = pd.DataFrame(data)
        return df['time'].max()
