from dash import Dash, dcc, html, Input, Output, Patch, clientside_callback, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_mantine_components as dmc
import pandas as pd
from datetime import date
import plotly.express as px
import numpy as np
import base64
import getpass
import psycopg2

# adds  templates to plotly.io
load_figure_template(["minty", "minty_dark"])

### ----- functions -----
def database_connection(**kwargs):
    '''
    Establishes a connection to the database using the credentials provided in the DATABASE_CREDENTIALS section of the config_load.yml file.
    '''

    # Prompt the user to enter the password if not provided in kwargs
    password = kwargs.get('password') or getpass.getpass("Enter the database password: ")

    # Construct the connection string
    DB_CONNECTION_STRING = ''
    for key, value in kwargs.items():
        if key != 'password':
            DB_CONNECTION_STRING += f'{key.lower()}={value} '

    # Add the password to the connection string
    DB_CONNECTION_STRING += f'password={password}'

    ### Open database connection
    try:
        connection = psycopg2.connect(DB_CONNECTION_STRING)
        print("Connection created!")
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)
        return None, None

    try:
        cursor = connection.cursor()
        print("Cursor obtained!")
    except psycopg2.Error as e:
        print("Error: Could not get cursor")
        print(e)
        connection.close()
        return None, None

    connection.set_session(autocommit=True)

    return connection, cursor

### / ----- functions -----

# ### ----- database connection -----
#
# host = 'ep-dry-bonus-a5fb1uxb.us-east-2.aws.neon.tech'
# dbname = 'experiments_data'
# user = 'main_db_owner'
# psw = 'VPqlabJfy4s6'
#
# # Establish a connection to the database
# connection, cursor = database_connection(host = host, dbname = dbname, user = user, password = psw)
#
# ### /----- database connection -----
#
# ### ----- main data database query -----
#
# # Retrieve all records from the table main_table
# sql_statement = """SELECT * FROM main_table"""
#
# # execute SQL query
# cursor.execute(sql_statement)
#
# # Fetch query results
# query_results = cursor.fetchall()
#
# # Create a DataFrame from query results
# colnames = [desc[0] for desc in cursor.description]
# data_frame = pd.DataFrame(data=query_results, columns=colnames)
#
# ### /----- database query -----
#
# ### ----- management_data database query -----
#
# # Retrieve all records from the table main_table
# sql_statement = """SELECT * FROM management_data"""
#
# # execute SQL query
# cursor.execute(sql_statement)
#
# # Fetch query results
# query_results = cursor.fetchall()
#
# # Create a DataFrame from query results
# colnames = [desc[0] for desc in cursor.description]
# data_frame_dates = pd.DataFrame(data = query_results, columns = colnames)
#
# ### /----- management_data database query -----
#
# ### Close database connection
# cursor.close()
# connection.close()
#
#
# ### ----- get the DAE column -----
#
# # Transform date into datatime
# data_frame['date'] = pd.to_datetime(data_frame['date'])
# data_frame_dates['date'] = pd.to_datetime(data_frame_dates['date'])
#
# data_frame_dates['date'] = pd.to_datetime(data_frame_dates['date'])
#
# # Define a function to find the appropriate date from data_frame_dates
# def find_matching_date(row):
#     matching_row = data_frame_dates[
#         (data_frame_dates['experiment'] == row['experiment']) &
#         (data_frame_dates['crop'] == row['crop']) &
#         (data_frame_dates['treatment'] == row['treatment']) &
#         (data_frame_dates['season'] == row['season'])
#     ]
#     return matching_row['date'].iloc[0] if not matching_row.empty else pd.NaT
#
# # Apply the function to each row in data_frame to find the matching date
# data_frame_dae['matching_date'] = data_frame_dae.apply(find_matching_date, axis=1)
#
# # Calculate the difference in days and add it as a new column 'DAE'
# data_frame_dae['DAE'] = (data_frame_dae['date'] - data_frame_dae['matching_date']).dt.days
#
# # Drop the 'matching_date' column as it's no longer needed
# data_frame_dae.drop(columns=['matching_date'], inplace=True)
#
# ### /----- get the DAE column -----


# dataframe path
#fileName = ('LAI_ACRE_Biomass_y22.csv')
fileName = ('DAE.csv')
df = pd.read_csv(fileName)
df['date'] =  pd.to_datetime(df['date'], infer_datetime_format=True)

# get the list of seasons for the selection menu
experiment = [item for item in df['experiment'].unique().tolist()]

# external_stylesheets = [
#     {
#         "href": "https://fonts.googleapis.com/css2?"
#                 "family=Lato:wght@400;700&display=swap",
#         "rel": "stylesheet",
#     },
# ]

# https://bootswatch.com/
external_stylesheets = dbc.themes.SLATE

app = Dash(__name__, external_stylesheets=[external_stylesheets, dbc.icons.FONT_AWESOME])


server = app.server

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.title = "Wang Lab"

image_filename = 'phys_icon.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)


app.layout = dbc.Container(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Wang Lab Data", className="header-title"
                ),
                html.P(
                    children= "Purdue University - Agronomy",
                    className="header-description",
                ),
            ],
            className="bg-primary text-white p-4 mb-2 text-center",
        ),

        html.Div(
            children=[

                html.Div(
                    children=[
                        html.Div(children="Experiment", className="menu-title"),
                        dcc.Dropdown(
                            id='experiment',
                            options=[{'label': i, 'value': i} for i in df['experiment'].unique()],
                            value=df['experiment'].iloc[0]
                        ),
                    ]
                ),

                html.Div(
                    children=[
                        html.Div(children="Season", className="menu-title"),
                        dcc.Dropdown(
                            id='season',
                            options=[{'label': i, 'value': i} for i in df['season'].unique()],
                            value=df['season'].iloc[0]
                        ),
                    ]
                ),

                html.Div(
                    children=[
                        html.Div(children="Measurement method", className="menu-title"),
                        dcc.Dropdown(
                            id='measurement_method',
                            value=df['measurement_method'].iloc[0]
                        ),
                    ]
                ),

                html.Div(
                    children=[
                        html.Div(children="Variable", className="menu-title"),
                        dcc.Dropdown(
                            id='variable',
                            value=df['variable_name'].iloc[0]
                        ),
                    ]
                ),

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
                        id='box_plot_genotype', config={"displayModeBar": True},
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
                        html.Div(children="treatment", className="menu-title"),
                        dcc.Dropdown(
                            id='treatment',
                            value=df['treatment'].iloc[0]
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
                        id='box_plot_env_genotype', config={"displayModeBar": True},
                    ),

                    className="card",
                ),

            ],
            className="wrapper",
        ),

    ]
)


# Define callback to update season dropdown options based on selected experiment
@app.callback(
    Output('season', 'options'),
    [Input('experiment', 'value')]
)
def update_season_options(selected_experiment):
    # Filter DataFrame based on selected experiment
    filtered_df = df[df['experiment'] == selected_experiment]
    # Create options for season dropdown based on unique seasons in filtered DataFrame
    season_options = [{'label': season, 'value': season} for season in filtered_df['season'].unique()]
    return season_options

# Define callback to update measurement method dropdown options based on selected experiment and season
@app.callback(
    Output('measurement_method', 'options'),
    [Input('experiment', 'value'),
     Input('season', 'value')]
)
def update_measurement_method_options(selected_experiment, selected_season):
    # Filter DataFrame based on selected experiment and season
    filtered_df = df[(df['experiment'] == selected_experiment) & (df['season'] == selected_season)]
    # Create options for measurement method dropdown based on unique methods in filtered DataFrame
    measurement_method_options = [{'label': method, 'value': method} for method in filtered_df['measurement_method'].unique()]
    return measurement_method_options

# Define callback to update variable dropdown options based on selected experiment, season, and measurement method
@app.callback(
    Output('variable', 'options'),
    [Input('experiment', 'value'),
     Input('season', 'value'),
     Input('measurement_method', 'value')]
)
def update_variable_options(selected_experiment, selected_season, selected_measurement_method):
    # Filter DataFrame based on selected experiment, season, and measurement method
    filtered_df = df[(df['experiment'] == selected_experiment) &
                     (df['season'] == selected_season) &
                     (df['measurement_method'] == selected_measurement_method)]
    # Create options for variable dropdown based on unique variables in filtered DataFrame
    variable_options = [{'label': variable, 'value': variable} for variable in filtered_df['variable_name'].unique()]
    return variable_options

# Define callback to update treatment dropdown options based on selected experiment, season, measurement method, and variable
@app.callback(
    Output('treatment', 'options'),
    [Input('experiment', 'value'),
     Input('season', 'value'),
     Input('measurement_method', 'value'),
     Input('variable', 'value')]
)
def update_treatment_options(selected_experiment, selected_season, selected_measurement_method, selected_variable):
    # Filter DataFrame based on selected experiment, season, measurement method, and variable
    filtered_df = df[(df['experiment'] == selected_experiment) &
                     (df['season'] == selected_season) &
                     (df['measurement_method'] == selected_measurement_method) &
                     (df['variable_name'] == selected_variable)]
    # Create options for treatment dropdown based on unique treatments in filtered DataFrame
    treatment_options = [{'label': treatment, 'value': treatment} for treatment in filtered_df['treatment'].unique()]
    return treatment_options


# Boxplot season
@app.callback(
    Output('box_plot', 'figure'),
    Input('season', 'value'),
    Input('variable', 'value'))

def update_graph(season, variable):
    # create the graph
    # filter season
    df_f = df[df['season'] == season]

    # filter variable
    dff = df_f[df_f['variable_name'] == variable]

    # Get variable_units
    units = [item for item in dff['variable_units'].unique()]

    # create the yaxis_title
    yaxis_title_value = variable + ' (' + units[0] + ')'

    fig = px.box(dff, y=dff['variable_value'], x=dff['DAE'], color='treatment',labels={
                     "treatment": "Days after emergency"},
                 color_discrete_map = {'Late':'darkslategrey','Early':'gray'})

    fig.update_layout(xaxis_title='Days after emergency',
                      yaxis_title= yaxis_title_value,
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

# Boxplot season line
@app.callback(
    Output('box_plot_genotype', 'figure'),
    Input('season', 'value'),
    Input('variable', 'value'))

def update_graph(season, variable):
    # create the graph
    # filter season
    df_f = df[df['season'] == season]

    # filter variable
    dff = df_f[df_f['variable_name'] == variable]

    # Get variable_units
    units = [item for item in dff['variable_units'].unique()]

    # create the yaxis_title
    yaxis_title_value = variable + ' (' + units[0] + ')'


    fig = px.box(dff, y=dff['variable_value'], x=dff['date'], color='genotype',labels={
                     'genotype': 'Genotype'}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title=yaxis_title_value,
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

# Boxplot treatment
@app.callback(
    Output('box_plot_env_genotype', 'figure'),
    Input('treatment', 'value'),
    Input('season', 'value'),
    Input('variable', 'value'))

def update_graph(treatment, season, variable):
    # create the graph
    # filter season
    df_env = df[df['treatment'] == treatment]

    df_f = df_env[df_env['season'] == season]

    # filter variable
    dff = df_f[df_f['variable_name'] == variable]

    # Get variable_units
    units = [item for item in dff['variable_units'].unique()]

    # create the yaxis_title
    yaxis_title_value = variable + ' (' + units[0] + ')'

    fig = px.box(dff, y=dff['variable_value'], x=dff['date'], color='genotype', labels={
        'genotype': 'Genotype'}, template='simple_white')

    fig.update_layout(xaxis_title='Days after planting',
                      yaxis_title=yaxis_title_value,
                      plot_bgcolor='lavender',
                      font_size=20,
                      font_color='#000000',
                      font_family='Old Standard TT')

    return fig

@callback(
    Output("graph", "figure"),
    Input("color-mode-switch", "value"),
)
def update_figure_template(switch_on):
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]

    patched_figure = Patch()
    patched_figure["layout"]["template"] = template
    return patched_figure


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == '__main__':
    app.run_server(debug=True)