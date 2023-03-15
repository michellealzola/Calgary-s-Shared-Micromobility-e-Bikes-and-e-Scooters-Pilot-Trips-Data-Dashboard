import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='./assets/')

url = 'https://data.calgary.ca/resource/jicz-mxiz.json'

data = pd.read_json(url)

data_df = pd.DataFrame(data)

data_df['count'] = 1

summary_start_day = data_df.pivot_table(values='count', index='start_day', aggfunc='sum')

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

data_df.astype(str)
hour_to_time = {0: '12:00 AM',
                1: '1:00 AM',
                2: '2:00 AM',
                3: '3:00 AM',
                4: '4:00 AM',
                5: '5:00 AM',
                6: '6:00 AM',
                7: '7:00 AM',
                8: '8:00 AM',
                9: '9:00 AM',
                10: '10:00 AM',
                11: '11:00 AM',
                12: '12:00 PM',
                13: '1:00 PM',
                14: '2:00 PM',
                15: '3:00 PM',
                16: '4:00 PM',
                17: '5:00 PM',
                18: '6:00 PM',
                19: '7:00 PM',
                20: '8:00 PM',
                21: '9:00 PM',
                22: '10:00 PM',
                23: '11:00 PM'}

for value in data_df['start_hour']:
    for k, v in hour_to_time.items():
        if value == str(k):
            data_df['start_hour'].replace(value, v, inplace=True)


def create_heatmap():
    df = pd.read_json('https://data.calgary.ca/resource/jicz-mxiz.json?vehicle_type=scooter')
    fig = px.scatter(df, x='startx', y='starty', opacity=0.5, color_discrete_sequence=['red'])
    fig.add_densitymapbox(lat=df['starty'], lon=df['startx'], radius=10, zmax=8, colorscale='Reds')
    fig.add_densitymapbox(lat=df['endy'], lon=df['endx'], radius=10, zmax=8, colorscale='Blues')
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10, mapbox_center={"lat": 51.0447, "lon": -114.0719})
    # fig.layout.title = 'Area Concentration of Trips'

    return fig


def create_time_of_day():
    summary_day_time = data_df.pivot_table(index='start_hour', aggfunc=len, fill_value=0)
    fig2 = px.scatter(x=summary_day_time.index, y=summary_day_time['count'])
    # fig2.layout.title = 'Time of Day with the Most Trips'
    fig2.layout.xaxis.title = 'Time of day (0 = 12am to 23 = 11pm)'
    fig2.layout.yaxis.title = 'Number of trips'

    return fig2


graphs = {
    'Graph 1': create_heatmap(),
    'Graph 2': create_time_of_day(),
}

header = html.Div(
    children=
    [
        html.H1("Calgary's Shared Micromobility (e-Bikes and e-Scooters) Pilot Trips Data"),
        html.P('The data was from the trips made between July 1, 2019 and September 30, 2019'),
    ],
    style=
    {
        'background-color': '#333',
        'color': '#fff',
        'padding': '20px',
    },
)

menu = html.Div(
    children=
    [
        dcc.Link('Home', href='/', className='menu-link'),
        dcc.Link('About', href='/about', className='menu-link'),
        dcc.Link('Contact', href='/contact', className='menu-link'),
    ],
    style=
    {
        'background-color': '#eee',
        'padding': '10px',
    }
)

body = html.Div(
    children=
    [
        html.H2('Weekday Number of Trips Data'),
        dcc.Dropdown(id='day',
                     options=[{'label': day, 'value': day}
                              for day in summary_start_day.index],
                     className='drp1'),
        html.Br(),
        html.Div(id='report_day'),
        html.Br(),
        html.Br(),
        html.H2('Area Concentration of Trips'),
        dcc.Graph(
            id='heatmap',
            figure=create_heatmap(),
        ),
        html.H2('Time of Day with the Most Trips'),
        dcc.Graph(
            id='scatter_time_day',
            figure=create_time_of_day(),
        )

    ],
    style=
    {
        'padding': '20px',
    }
)

article = html.Div(
    children=
    [
        dbc.Tabs([
            dbc.Tab([
                html.H2('Sources'),
                html.Span('Shared Mobility Pilot Trips'),
                html.Br(),
                html.A('https://dev.socrata.com/foundry/data.calgary.ca/jicz-mxiz',
                       href='https://dev.socrata.com/foundry/data.calgary.ca/jicz-mxiz'),
                html.Br(),
                html.Span('Shared Mobility Pilot Trips (JSON)'),
                html.Br(),
                html.A('https://data.calgary.ca/resource/jicz-mxiz.json',
                       href='https://data.calgary.ca/resource/jicz-mxiz.json'),
                html.Br(),
                html.Span('Shared Micromobility (e-Bikes and e-Scooters) program'),
                html.Br(),
                html.A('https://www.calgary.ca/bike-walk-roll/electric-scooters.html',
                       href='https://www.calgary.ca/bike-walk-roll/electric-scooters.html'),
            ], label='Source'),
            dbc.Tab([
                html.H2('Dashboard Author'),
                html.Span('Michelle Alzola'),
                html.Br(),
                html.A('https://michellealzoladesign.com/',
                       href='https://michellealzoladesign.com/'),
            ], label='Dashboard Author'),
        ]),
    ],
    style=
    {
        "padding": "20px",
        "background-color": "#eee",
        "float": "right",
        "width": "30%",
        "height": "auto",
        "position": "fixed",
        "right": "20px",
        "top": "100px",
    },
)

app.layout = html.Div(
    children=
    [
        header,
        menu,
        html.Br(),
        html.Div(
            children=
            [
                body,
                article
            ],
            style=
            {
                "padding": "20px",
                "margin-left": "20px",
                "width": "70%",
                "float": "left",
            },
        ),
    ]
)

app.css.append_css({
    'external_url': app.get_asset_url('my-styles.css')
})


@app.callback(Output('report_day', 'children'),
              Input('day', 'value'))
def get_weekday_trips(day):
    if day is None:
        return ''
    filtered_days = summary_start_day[summary_start_day.index == day]
    num_trips = filtered_days.loc[:].values[0]

    return [html.H3(day),
            f'The number of trips for {day} is {num_trips}']


if __name__ == '__main__':
    app.run_server(debug=True)
