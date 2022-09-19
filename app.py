from dash import Dash, dcc, html, Input, Output
import pandas as pd
from datetime import date
import plotly.express as px
import numpy as np

# dataframe path
fileName = ('LAI_ACRE_Biomass_y22.csv')
df = pd.read_csv(fileName)
df['DATE'] =  pd.to_datetime(df['DATE'], infer_datetime_format=True)

# get the list of seasons for the selection menu
environment = [item for item in df['environment'].unique().tolist()]

season = [item for item in df['season'].unique().tolist()]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([

    html.H4('Agronomy - Purdue University'),

    html.Div((
        html.H3('Public Biomass experiment season 2022')
    ), style={'width': '60%', 'padding': '10px 40px 10px 20px'}),

    # show plot menu
    html.Div(["season: ",
              dcc.Dropdown(
                  id='season',
                  options=[{'label': i, 'value': i} for i in season],
                  value=season[0])
              ], style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),

    # Show the boxplot
    html.Div((
        dcc.Graph(
            id='box_plot'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'}),

    # Show the boxplot
    html.Div((
        dcc.Graph(
            id='box_plot_source'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'}),

    # Show the boxplot
    html.Div((
        dcc.Graph(
            id='box_plot_line'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'}),

    # show plot menu
    html.Div(["Environment: ",
              dcc.Dropdown(
                  id='environment',
                  options=[{'label': i, 'value': i} for i in environment],
                  value=environment[0])
              ], style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),

    # Show the boxplot by enviroment
    html.Div((
        dcc.Graph(
            id='box_plot_env_source'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'}),

# Show the boxplot by enviroment
    html.Div((
        dcc.Graph(
            id='box_plot_env_line'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'})

])

# Boxplot season
@app.callback(
    Output('box_plot', 'figure'),
    Input('season', 'value'))

def update_graph(season):
    # create the graph
    # filter season
    dff = df[df['season'] == season]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='environment',labels={
                     "environment": "Date of planting"}, color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

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
                     "source": "Source"}, color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

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
                     "line": "Line"}, color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

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
                     "source": "Source"}, color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

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
        "line": "Line"}, color_discrete_map={'Late': 'darkslategrey', 'Early': 'gray'})

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)