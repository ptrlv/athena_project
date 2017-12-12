import os.path

import dash
import flask

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css')

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True
# app.scripts.config.serve_locally = True

@app.server.route('/scripts/<resource>')
def serve_script(resource):
    return flask.send_from_directory(SCRIPT_PATH, resource)

@app.server.route('/css/<resource>')
def serve_css(resource):
    return flask.send_from_directory(CSS_PATH, resource)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "/css/index.css"})

app.scripts.append_script({"external_url": "https://code.jquery.com/jquery-3.2.1.min.js"})
app.scripts.append_script({"external_url": "https://rawgit.com/pie6k/jquery.initialize/master/jquery.initialize.min.js"})

app.scripts.append_script({"external_url": "/scripts/fix_datatable.js"})
