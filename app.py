from dash import Dash, dcc, html, Input, Output
import pandas as pd
from datetime import date
import plotly.express as px
import numpy as np
import base64

# dataframe path
fileName = ('LAI_ACRE_Biomass_y22.csv')
df = pd.read_csv(fileName)
df['DATE'] =  pd.to_datetime(df['DATE'], infer_datetime_format=True)

# get the list of seasons for the selection menu
environment = [item for item in df['environment'].unique().tolist()]

season = [item for item in df['season'].unique().tolist()]


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.title = "Soybean Public Biomass Experiment"

image_filename = 'phys_icon.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Public Biomass Experiment", className="header-title"
                ),
                html.P(
                    children= " Agronomy - Purdue University",
                    className="header-description",
                ),

                html.P(
                    children="Season 2022 ",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Season", className="menu-title"),
                        dcc.Dropdown(
                            id='season',
                            options=[{'label': i, 'value': i} for i in season],
                            value=season[0]
                        ),

                    ]
                )

            ],
            className="menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='box_plot', config={"displayModeBar": True},
                    ),
                    className="card",
                ),

                html.Div(
                    children=dcc.Graph(
                        id='box_plot_source', config={"displayModeBar": True},
                    ),

                    className="card",
                ),

                html.Div(
                    children=dcc.Graph(
                        id='box_plot_line', config={"displayModeBar": True},
                    ),

                    className="card",
                ),

            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Environment", className="menu-title"),
                        dcc.Dropdown(
                            id='environment',
                            options=[{'label': i, 'value': i} for i in environment],
                            value=environment[0]
                        ),

                    ]
                )

            ],
            className="second_menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='box_plot_env_source', config={"displayModeBar": True},
                    ),
                    className="card",
                ),

                html.Div(
                    children=dcc.Graph(
                        id='box_plot_env_line', config={"displayModeBar": True},
                    ),

                    className="card",
                ),

            ],
            className="wrapper",
        ),

    ]
)


# Boxplot season
@app.callback(
    Output('box_plot', 'figure'),
    Input('season', 'value'))

def update_graph(season):
    # create the graph
    # filter season
    dff = df[df['season'] == season]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='environment',labels={
                     "environment": "Date of planting"},
                 color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig


# Boxplot season source
@app.callback(
    Output('box_plot_source', 'figure'),
    Input('season', 'value'))

def update_graph(season):
    # create the graph
    # filter season
    dff = df[df['season'] == season]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='source',labels={
                     "source": "Source"}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')


    #fig.update_traces(line_color='black', line_width=1)

    return fig

# Boxplot season line
@app.callback(
    Output('box_plot_line', 'figure'),
    Input('season', 'value'))

def update_graph(season):
    # create the graph
    # filter season
    dff = df[df['season'] == season]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='line',labels={
                     "line": "Line"}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig


# Boxplot environment
@app.callback(
    Output('box_plot_env_source', 'figure'),
    Input('environment', 'value'))

def update_graph(environment):
    # create the graph
    # filter season
    dff = df[df['environment'] == environment]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='source',labels={
                     "source": "Source"}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

    # Boxplot environment
@app.callback(
    Output('box_plot_env_line', 'figure'),
    Input('environment', 'value'))
def update_graph(environment):
    # create the graph
    # filter season
    dff = df[df['environment'] == environment]

    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='line', labels={
        "line": "Line"}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

