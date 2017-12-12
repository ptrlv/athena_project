from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from werkzeug.routing import Map, Rule
from werkzeug.routing import NotFound, RequestRedirect

routing_map = Map([
    Rule("/", endpoint="index"),
    Rule("/queue/<string:queue_name>/", endpoint="queue"),
    Rule("/debug/", endpoint="debug")
])

routes = routing_map.bind("")

from app import app
from apps import index_app
from apps import queue_app
from apps import debug_app

app.layout = html.Div([
    # Stores url
    dcc.Location(id='url', refresh=False),
    
    # Hidden data table to force it to send the data table js components
    # https://github.com/plotly/dash-table-experiments/issues/18
    html.Div(dt.DataTable(rows=[{}]), style={"display": "none"}),
    
    # Header bar
    html.Div([
        dcc.Link("Index", href="/", style={"margin":"5px"}),
        dcc.Link("Debug", href="/debug/", style={"margin":"5px"}),
        html.Hr(style={"margin": "0px", "margin-top": "2px", "margin-bottom":"10px"}),
    ], style={"width": "100%"}),
    
    # Div to load page content into
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    while True:
        try:
            endpoint, args = routes.match(pathname)
        except RequestRedirect as redirect:
            pathname = redirect.new_url.replace("http://", "")
        except NotFound:
            return "404"
        else:
            break
    
    if endpoint == "index":
        return index_app.generate_layout()
    elif endpoint == "queue":
        return queue_app.generate_layout(args.get("queue_name"))
    elif endpoint == "debug":
        return debug_app.generate_layout()

if __name__ == '__main__':
    app.run_server(debug=False)
