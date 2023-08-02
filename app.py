import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.io as pio

import navigation

# username: dcf_admin
# password: DnP3vf0EUD81mzHx

# connection string: mongodb+srv://dcf_admin:<password>@dcf-webapp.xsqti7v.mongodb.net/?retryWrites=true&w=majority

app = dash.Dash(
    __name__,
    use_pages=True,
    update_title="Loading model ...",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    serve_locally=True,
)
server = app.server

app.layout = html.Div([dcc.Store(id="store"), navigation.navbar, dash.page_container])

app.clientside_callback(
    """
    function(trigger) {
        //  can use any prop to trigger this callback - we just want to store the info on startup
        const inner_width  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        const inner_height = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;
        const screenInfo = {height :screen.height, width: screen.width, in_width: inner_width, in_height: inner_height};

        return screenInfo
    }
    """,
    Output("store", "data"),
    Input("store", "data"),
)


if __name__ == "__main__":
    app.run_server()
