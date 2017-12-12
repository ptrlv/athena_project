import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


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


def generate_table(search_term, dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(
            [html.Td(dcc.Link(dataframe.iloc[i][0], href="/queue/{}".format(dataframe.iloc[i][0])))] + [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns[1:]]
        ) for i in range(0, len(dataframe)) if search_term.lower() in dataframe.iloc[i][0].lower()][0:max_rows],
        
        id="queue-table"
    )


def generate_datatable():
    dataframe = Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d")
    dataframe["short_percentage"] = (100*dataframe["short_jobs"]/dataframe["total_jobs"]).round(2)
    
    dataframe = dataframe[["match_apf_queue", "total_jobs", "short_jobs", "short_percentage"]]
    
    # records = dataframe.to_dict("records")
    # for i, record in enumerate(records):
    #     record["match_apf_queue"] = dcc.Link(record["match_apf_queue"], href="/queue/{}".format(record["match_apf_queue"]))
    #     records[i] = record
    #
    # print(records)
    
    table = dt.DataTable(
        rows=dataframe.to_dict("records"),
        columns=dataframe.columns,
        filterable=True,
        sortable=True,
        editable=False,
        id="queue-datatable",
        #min_height="100%",
    )
    
    return table

@app.callback(
    Output("queue-comparison", "figure"),
    [Input(component_id='queue-datatable', component_property='rows'),
     Input("num-queues-dropdown", "value")],
)
def update_plot(rows, limit):
    selected_rows = [row["match_apf_queue"] for row in rows]
    return generate_plot(Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d"),
        filtered_by=selected_rows, limit=limit)


def generate_plot(dataframe, limit=10, search_term=None, filtered_by=None):
    dataframe.insert(5, "long_jobs", dataframe["total_jobs"]-dataframe["short_jobs"])
    """if not search_term is None:
        if len(search_term) > 0:
            dataframe = dataframe[dataframe["match_apf_queue"].str.contains(search_term, case=False)]"""
    
    dataframe = dataframe[dataframe["match_apf_queue"].isin(filtered_by)]
    dataframe["order"] = dataframe["match_apf_queue"].apply(lambda x: filtered_by.index(x))
    dataframe = dataframe.sort_values(by="order")
    dataframe.drop("order", axis=1)
    
    trace1 = go.Bar(
        y=dataframe["match_apf_queue"][0:limit][::-1],
        x=dataframe["short_jobs"][0:limit][::-1],
        name="Short jobs",
        orientation="h",
        marker=dict(
            color="#C21E29",
        ),
    )
    
    trace2 = go.Bar(
        y=dataframe["match_apf_queue"][0:limit][::-1],
        x=dataframe["long_jobs"][0:limit][::-1],
        name="Long jobs",
        orientation="h",
        marker=dict(
            color="#3A6CAC",
        ),
    )
    
    data = [trace1, trace2]
    layout = go.Layout(
        title="Top 10 queues by most short jobs (30 days)",
        barmode="stack",
        margin=dict(
            l=275,
        ),
        xaxis = go.XAxis(
            title="Jobs",
            fixedrange=True,
        ),
        yaxis = go.YAxis(
            fixedrange=True,
        ),
    )
    return {
        "data": data,
        "layout": layout,
    }


def generate_layout():
    layout = html.Div(
        [
            html.Div([
                html.H4("Queue comparison", id="title"),
                html.Div([
                    html.Div([html.Label('# queues displayed'),], style={"float":"left"}),
                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {"label":"10", "value":10},
                                {"label":"25", "value":25},
                                {"label":"50", "value":50},
                            ],
                            value=10,
                            clearable=False,
                            id="num-queues-dropdown",
                        ),
                    ], style={"width": "80px", "display":"inline-block"})
                ]),
                dcc.Graph(id="queue-comparison", figure={}, config={'displayModeBar': False}),
                ],
                style=dict(
                    width="50%",
                    float="left",
                ),
            ),
            html.Div([
                #html.Div(style={"width":"100%", "height":"1", "overflow":"hidden",}),
                # html.Div([
                #     dcc.Input(id='queue-search', value='', type="text", style={"display":"inline-block"}),
                #     html.Div(" ", id="table-search-feedback", style={"display":"inline-block", "margin-left": 10})
                # ]),
                # generate_table(" ", Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d"), 10),
                generate_datatable(),
                ],
                style=dict(
                    width="50%",
                    float="right",
                ),
            ),
            
        ],
    )
    
    return layout



# @app.callback(
#     Output("queue-comparison", "figure"),
#     [Input(component_id='queue-search', component_property='value')]
# )
# def update_plot(input_value):
#     return generate_plot(Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d"),
#         search_term=input_value)
#
#
# @app.callback(
#     Output(component_id='queue-table', component_property='children'),
#     [Input(component_id='queue-search', component_property='value')]
# )
# def update_output_div(input_value):
#     return generate_table(input_value, Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d"))
#
#
# @app.callback(
#     Output("table-search-feedback", "children"),
#     [Input("queue-search", "value")]
# )
# def update_search_feedback(input_value):
#     df = Datasources.get_latest_data_for("aws-athena-query-results-lancs-30d")
#     matching_results = len([q for q in df["match_apf_queue"] if input_value.lower() in q.lower()])
#     showing, hidden = min(matching_results, 10), max(0, matching_results-10)
#
#     return "Showing {} results ({} hidden)".format(showing, hidden)

if __name__ == '__main__':
    app.run_server()
