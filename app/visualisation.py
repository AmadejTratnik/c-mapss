from dash import Dash
import dash_bootstrap_components as dbc
import numpy as np

from layout import layout
from callbacks import get_callbacks


app = Dash(__name__, update_title=None,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.CYBORG])
app.layout = layout
app.title='Real Time Fault Detector'


get_callbacks(app)


if __name__ == '__main__':
    app.run_server(port=1129, debug=True)