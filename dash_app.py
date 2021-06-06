###############################################################################
#                            RUN MAIN                                         #
###############################################################################

# setup
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from python.data import random_data, load_file
from python.model import Model
from python.plot import Plot
from settings import config


# Data
dtf = random_data()

# App Instance
app = dash.Dash(name=config.app_name, assets_folder="static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.app_name



########################## Navbar ##########################
# Input
## none


# Output
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
    ## about
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", id="about-popover", active=False),
        dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            dbc.PopoverHeader("How it works"), dbc.PopoverBody(config.about)
        ])
    ])),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contacts"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])


# Callbacks
@app.callback(output=Output("about","is_open"), inputs=[Input("about-popover","n_clicks")], state=[State("about","is_open")])
def about_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(output=Output("about-popover","active"), inputs=[Input("about-popover","n_clicks")], state=[State("about-popover","active")])
def about_active(n, active):
    if n:
        return not active
    return active



########################## Body ##########################
# Input
inputs = dbc.FormGroup([
    ## hide these 2 inputs if file is loaded
    html.Div(id='hide-seek', children=[

        dbc.Label("Number of Guests", html_for="n-guests"), 
        dcc.Slider(id="n-guests", min=10, max=100, step=1, value=50, tooltip={'always_visible':False}),

        dbc.Label("Number of Rules", html_for="n-rules"), 
        dcc.Slider(id="n-rules", min=0, max=10, step=1, value=3, tooltip={'always_visible':False})

    ], style={'display':'block'}),

    ## always visible
    dbc.Label("Number of Trials", html_for="n-iter"), 
    dcc.Slider(id="n-iter", min=10, max=1000, step=None, marks={10:"10", 100:"100", 500:"500", 1000:"1000"}, value=0),

    html.Br(),
    dbc.Label("Max Guests per Table", html_for="max-capacity"), 
    dbc.Input(id="max-capacity", placeholder="table capacity", type="number", value="10"),

    html.Br(),
    dbc.Label("Or Upload your Excel", html_for="load-excel"), 
    dcc.Upload(id='load-excel', children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
               style={'width':'100%', 'height':'60px', 'lineHeight':'60px', 'borderWidth':'1px', 'borderStyle':'dashed',
                      'borderRadius':'5px', 'textAlign':'center', 'margin':'10px'} ),

    html.Br(),html.Br(),
    dbc.Col(dbc.Button("run", id="run", color="primary"))
])


# Output
body = dbc.Row([
        ### input
        dbc.Col(md=3, children=[
            inputs, 
            html.Br(),html.Br(),html.Br(),
        ]),
        ### plot
        dbc.Col(md=9, children=[
            dcc.Graph(id="plot")
        ])
])


# Callbacks
@app.callback(output=Output(component_id="hide-seek", component_property="style"), 
              inputs=[Input(component_id="load-excel", component_property="contents")])
def hide_stuff(contents):
    return {'display':'block'} if contents is None else {'display':'none'}

@app.callback(output=Output(component_id="plot", component_property="figure"), 
              inputs=[Input(component_id="run", component_property="n_clicks")],
              state=[State("n-guests","value"), State("n-iter","value"), State("max-capacity","value"), State("n-rules","value"), 
                     State("load-excel","contents"), State("load-excel","filename")])
def plot_tables(n_clicks, n_guests, n_iter, max_capacity, n_rules, contents, filename):
    if contents is not None:
        dtf = load_file(contents, filename)
    else:
        dtf = random_data(n=n_guests, n_rules=n_rules)
    dtf = Model(dtf, float(max_capacity), int(n_iter)).run()
    return Plot(dtf).plot(max_capacity, filename)



########################## App Layout ##########################
app.layout = dbc.Container(fluid=True, children=[
    html.H1(config.app_name, id="nav-pills"),
    navbar,
    html.Br(),html.Br(),html.Br(),
    body
])



########################## Run ##########################
if __name__ == "__main__":
    debug = True if config.ENV == "DEV" else False
    app.run_server(debug=debug, host=config.host, port=config.port)
        