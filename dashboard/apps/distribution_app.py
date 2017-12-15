from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app import app

from datasources import Datasources


def generate_plot(column):
    dataframe = Datasources.get_latest_data_for("aws-athena-query-results-lancs-all-48h")
    dataframe = dataframe[dataframe[column] <= 400]
    
    hist = go.Histogram(x=dataframe[column], xbins={"start":-0.5, "end":399.5, "size":1})

    layout = go.Layout(
        xaxis={"title": column},
        yaxis={"title": "Num jobs", "type":"log"},
        title="{} distribution of all jobs in past 48 hours".format(column),
        margin={
            "t":50,
        }
    )

    figure = {
        "data": [hist,],
        "layout": layout,
    }

    return dcc.Graph(id="distribution-plot-{}".format(column), figure=figure, config={'displayModeBar': False})


def generate_layout():
    layout = [
        html.Div([
            generate_plot("duration"),
            generate_plot("remotewallclocktime"),
        ],
        style={
        })
    ]

    return layout
