import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly


import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

from app import app

from datasources import Datasources

# Display names for groupings
groupings = {
    "gridresource": "Grid resource",
    "globaljobid": "Factory",
    "jobstatus": "Job status",
}

def generate_plot(grouping):
    if grouping is None:
        return {}
    dataframe = Datasources.get_latest_data_for("aws-athena-query-results-lancs-4h")
    dataframe = dataframe.sample(frac=0.25, random_state=0)
    dataframe["gridresource"] = dataframe["gridresource"].apply(lambda x: x.split()[0])
    dataframe["globaljobid"] = dataframe["globaljobid"].apply(lambda x: x.split(".")[0])

    traces = []
    
    for group in dataframe[grouping].unique():
        filtered_df = dataframe[dataframe[grouping] == group]
        traces.append(go.Scatter(
            x=filtered_df["duration"],
            y=filtered_df["remotewallclocktime"],
            mode="markers",
            opacity=0.7,
            name=group,
            marker={
                "size":5,
            },
            hoverinfo="none",
        ))

    layout = go.Layout(
        xaxis={"title": "Duration"},
        yaxis={"title": "Remote wallclock time"},
        title="Events in past 4 hours ({})".format(groupings[grouping]),
        margin={
            "r":220,
            "l":60,
            "t":50,
            "b":50,
        },
        width=830,
        height=630,
    )

    figure = {
        "data": traces,
        "layout": layout,
    }

    return figure


@app.callback(
    Output("grouping-plot", "figure"),
    [Input("grouping-dropdown", "value")],
)
def update_plot(grouping):
    return generate_plot(grouping)
    


def generate_layout():
    layout = [
        html.Div([
            html.Div([
                dcc.Dropdown(
                    options=[
                        {"label":"Grid resource", "value":"gridresource"},
                        {"label":"Factory", "value":"globaljobid"},
                        {"label":"Job status", "value":"jobstatus"},
                    ],
                    value="gridresource",
                    clearable=False,
                    id="grouping-dropdown",
                ),
            ],
            style={
                "width":"250px",
            }),
            
            html.Div([
                dcc.Graph(
                    figure=generate_plot(None),
                    config={'displayModeBar': False},
                    id="grouping-plot",)
            ],
            style={
                "width": "50%",
                "float": "left",
            }),

            html.Div("Actually based on 25% sample of data"),
        ],
        style={
            "height": "75%",
        })
    ]

    return layout
