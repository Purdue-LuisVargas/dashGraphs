from dash import Dash,  dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import base64
import getpass
import psycopg2

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

## / ----- functions -----

### ----- database connection -----

host = 'ep-dry-bonus-a5fb1uxb.us-east-2.aws.neon.tech'
dbname = 'experiments_data'
user = 'readonly_rice'
psw = 'riceG6d92k%e'

# Establish a connection to the database
connection, cursor = database_connection(host = host, dbname = dbname, user = user, password = psw)

### /----- database connection -----

### ----- main data database query -----

# Retrieve all records from the table main_table
#sql_statement = """SELECT * FROM main_table"""
sql_statement = """SELECT * FROM public.rice_main_table"""

# execute SQL query
cursor.execute(sql_statement)

# Fetch query results
query_results = cursor.fetchall()

# Create a DataFrame from query results
colnames = [desc[0] for desc in cursor.description]
data_frame = pd.DataFrame(data=query_results, columns=colnames)

### /----- database query -----

### ----- management_data database query -----

# Retrieve all records from the table main_table
sql_statement = """SELECT * FROM management_data"""

# execute SQL query
cursor.execute(sql_statement)

# Fetch query results
query_results = cursor.fetchall()

# Create a DataFrame from query results
colnames = [desc[0] for desc in cursor.description]
data_frame_dates = pd.DataFrame(data = query_results, columns = colnames)

### /----- management_data database query -----

### Close database connection
cursor.close()
connection.close()


### ----- get the DAE column -----

# Transform date into datatime
data_frame['date'] = pd.to_datetime(data_frame['date'])
data_frame_dates['date'] = pd.to_datetime(data_frame_dates['date'])

# Define a function to find the appropriate date from data_frame_dates
def find_matching_date(row):
    matching_row = data_frame_dates[
        (data_frame_dates['experiment'] == row['experiment']) &
        (data_frame_dates['crop'] == row['crop']) &
        (data_frame_dates['treatment'] == row['treatment']) &
        (data_frame_dates['season'] == row['season'])
    ]
    return matching_row['date'].iloc[0] if not matching_row.empty else pd.NaT

# Apply the function to each row in data_frame to find the matching date
data_frame['matching_date'] = data_frame.apply(find_matching_date, axis=1)

# Calculate the difference in days and add it as a new column 'DAE'
data_frame['DAE'] = (data_frame['date'] - data_frame['matching_date']).dt.days

# Drop the 'matching_date' column as it's no longer needed
data_frame.drop(columns=['matching_date'], inplace=True)

df = data_frame

### /----- get the DAE column -----


# dataframe path
#fileName = ('LAI_ACRE_Biomass_y22.csv')
# fileName = ('DAE.csv')
# df = pd.read_csv(fileName)
df['date'] =  pd.to_datetime(df['date'], infer_datetime_format=True)

# get the list of seasons for the selection menu
experiment = [item for item in df['experiment'].unique().tolist()]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# https://bootswatch.com/
#external_stylesheets = dbc.themes.DARKLY

app = Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server

app.title = "Wang Lab"

image_filename = 'phys_icon.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(
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
            className="header",
        ),

        html.Div(
            children=[

                html.Div(
                    children=[
                        html.Div(children="Experiment", className="menu-title"),
                        dcc.Dropdown(
                            id='experiment',
                            options=[{'label': i, 'value': i} for i in experiment],
                            value=df['experiment'].iloc[0],
                            className='wide-dropdown'
                        ),
                    ]
                ),

                html.Div(
                    children=[
                        html.Div(children="Season", className="menu-title"),
                        dcc.Dropdown(
                            id='season',
                            #options=[{'label': i, 'value': i} for i in df['season'].unique()],
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

# add callback for toggling the collapse on small screens

if __name__ == '__main__':
    app.run_server(debug=False)