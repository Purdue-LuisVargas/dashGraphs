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
    ],style={'width': '30%', 'display': 'inline-block', 'padding': '0px 20px 0px 50px'}),


    # Show the histogram
    html.Div((
        dcc.Graph(
            id='histogram'
        )
    ), style={'width': '70%', 'display': 'inline-block', 'padding': '0px 50px 0px 50px'})
    # show the seasons menu
])

# Histogram
@app.callback(
    Output('histogram', 'figure'),
    Input('season', 'value'))

def update_graph(season):
    # create the graph

    # filter season
    dff = df[df['season'] == season]


    fig = px.box(dff, y=dff['LAI'], x=dff['Days_after_planting'], color='environment',labels={
                     "environment": "Date of planting"}, color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

    fig.update_layout(xaxis_title='',
                      yaxis_title='Leaf area index ',
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)