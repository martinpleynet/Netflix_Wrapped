"""
This script builds a dash app with plotly graphs to display an
interactive dashboard of my Netflix viewing activity for 2020
(It has been implemented to allow for future years to be added)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
# server = app.server

# ---------------------------------------------------
# Import cleaned netflix data
df = pd.read_csv("NetflixWrapped.csv")

# ---------------------------------------------------
# Constants
colors = {
    'background': '#111111',
    'text': '#cf2a28'
    }
red_shades = ['#8f1801', '#a81b00', '#d12200', '#ff2900', '#fc3c17', '#fc5838','#fc7e65']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Spetember', 'October', 'November', 'December']

# ---------------------------------------------------
# App layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children = [

    html.H1("Your Netflix Wrapped 2020", style={'text-align':'center', 'color': colors['text']}),

    dcc.Dropdown(id='Year',
                 options=[{"label": "2020", "value":2020}],
                 multi=False,
                 value=2020
                 ),

    # Totals Summary
    html.H2("Totals", style={'text-align': 'left', 'color': colors['text']}),
    html.Div(id='days_time', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    html.Div(id='hours_time', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    html.Br(),

    # Titles Summary
    html.H2("Titles", style={'text-align': 'left', 'color': colors['text']}),
    html.Div(id='num_items', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    html.Br(),
    html.Div(id='fav_shows', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    dcc.Graph(id='time1_graph', figure={}),
    
    # Genres Summary
    html.H2("Genres", style={'text-align': 'left', 'color': colors['text']}),
    html.Div(id='num_genres', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    html.Br(),
    html.Div(id='fav_genres', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    dcc.Graph(id='time2_graph', figure={}),

    # Habits Summary
    html.H2("Watching Habits", style={'text-align': 'left', 'color': colors['text']}),
    html.Div(id='max_month_day', children=[], style={'color': colors['text'], 'font-size':'18px'}),
    dcc.Graph(id='time3_graph', figure={})

])

# ---------------------------------------------------
# Create callback

@app.callback(
    [Output(component_id='days_time', component_property='children'),
     Output(component_id='hours_time', component_property='children'),
     Output(component_id='num_items', component_property='children'),
     Output(component_id='fav_shows', component_property='children'),
     Output(component_id='time1_graph', component_property='figure'),
     Output(component_id='num_genres', component_property='children'),
     Output(component_id='fav_genres', component_property='children'),
     Output(component_id='time2_graph', component_property='figure'),
     Output(component_id='max_month_day', component_property='children'),
     Output(component_id='time3_graph', component_property='figure')],
    [Input(component_id='Year', component_property='value')]
    )

def update_graph(year):

    dff = df.copy()

    # ---------------------------------------------------
    # Total watch time

    total_time = dff['Runtime_min'].sum()
    total_hours = int(total_time/60)
    total_days = round(total_hours/24,2)

    html0 = [f"Days Watched : {total_days}"]
    html1 = [f"Hours Watched : {total_hours}"]

    
    # Viewing Breakdown by Pieces and Media Type
    total_titles = len(dff['Title'].unique())
    num_shows = len(dff.groupby('Media').get_group('TV Show')['Title'].unique())
    num_movies = len(dff.groupby('Media').get_group('Movie')['Title'].unique())
                     
    html2 = [f"You watched {total_titles} titles this year: {num_shows} tv shows and {num_movies} movies."]

    # ---------------------------------------------------
    # Watch Time of Titles
    
    dff_title_grouped = dff.groupby('Title')
    item_titles = list(dff['Title'].unique())
    title_time_dict={}
    for title in item_titles:
        new_df = dff_title_grouped.get_group(title)
        title_time_dict[title] = round(new_df['Runtime_min'].sum()/60, 2)

    # Sort values in descending order
    sorted_title_time = dict(sorted(title_time_dict.items(), key=lambda item:item[1], reverse=True))
    # Collect top 3 titles
    top_titles = list(sorted_title_time.keys())[0:3]

    # List out Top 3 shows
    html3 = [f"Your favorite shows were {top_titles[0]}, {top_titles[1]}, and {top_titles[2]}."]

    # create watch time df to plot
    title_time_df = pd.DataFrame(list(sorted_title_time.items()), columns=['Title', 'Hours Watched'])


    fig1 = go.Figure(go.Bar(
        x = title_time_df['Title'],
        y = title_time_df['Hours Watched'],
        marker_color = colors['text']
        )
    )
    
    fig1.update_layout(
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
        title_text = 'Hours Watched by Title'
        )

    # ---------------------------------------------------
    # Watch Time by Genre

    # Number of genres
    num_genres = len(dff['Genre'].unique())
    html4 = [f"You explored {num_genres} different genres this year."]

    
    dff_genre_grouped = dff.groupby('Genre')
    item_genres = list(dff['Genre'].unique())
    genre_time_dict = {}
    for genre in item_genres:
        new_df = dff_genre_grouped.get_group(genre)
        genre_time_dict[genre] = round(new_df['Runtime_min'].sum()/60, 2)

    # Sort values in descending order
    sorted_genre_time = dict(sorted(genre_time_dict.items(), key=lambda item:item[1], reverse=True))
    # Collect top 3 genres
    top_genres = list(sorted_genre_time.keys())[0:3]

    # List out Top 3 genres
    html5 = [f"Your favorite genres were {top_genres[0]}, {top_genres[1]}, and {top_genres[2]}."]

    # create watch time df for genres
    genre_time_df = pd.DataFrame(list(sorted_genre_time.items()), columns=['Genre', 'Hours Watched'])


    fig2 = go.Figure(go.Bar(
        x = genre_time_df['Genre'],
        y = genre_time_df['Hours Watched'],
        marker_color = colors['text']
        )
    )

    fig2.update_layout(
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
        title_text = 'Hours Watched by Genre'
        )

    # ---------------------------------------------------
    # Watch Time by Month
    
    dff_month_grouped = dff.groupby('Month')
    item_months = list(dff['Month'].unique())
    month_time_dict={}
    for month in item_months:
        new_df = dff_month_grouped.get_group(month)
        month_time_dict[month] = new_df['Runtime_min'].sum()
    # No december data so add value 0 for key 12 in dict
    month_time_dict[12]=0
    
    sorted_months = sorted(month_time_dict)
    sorted_month_time = {}
    for item in sorted_months:
        sorted_month_time[item] = round(month_time_dict[item]/60,2)

    max_month = list(dict(sorted(sorted_month_time.items(), key=lambda item:item[1], reverse=True)).keys())[0]

    month_time_df = pd.DataFrame(list(sorted_month_time.items()), columns=['Month', 'Hours Watched'])

    # ---------------------------------------------------
    # Watch Time by Day of Week
    dff_day_grouped = dff.groupby('DayOfWeek')

    item_days = list(dff['DayOfWeek'].unique())
    day_time_dict={}
    for day in item_days:
        new_df = dff_day_grouped.get_group(day)
        day_time_dict[day] = round(new_df['Runtime_min'].sum()/60,2)

    day_time_sorted = dict(sorted(day_time_dict.items(), key=lambda item:item[1], reverse=True))

    max_day = list(day_time_sorted.keys())[0]

    html6 = [f"You were with us the most in {months[max_month-1]}, and you really enjoyed realxing on {max_day}s."]

    # ---------------------------------------------------
    # Watching Habits subplots
    
    fig5 = make_subplots(rows = 1, cols = 2,
                         specs=[[{"type": "xy"}, {"type": "pie"}]],
                         subplot_titles = ('Hours Watched by Month', 'Hours Watched by Day of Week'),
                         column_widths = [0.7, 0.3]
    )

    fig5.add_trace(go.Scatter(
        x = month_time_df['Month'],
        y = month_time_df['Hours Watched'],
        line = dict(color = colors['text'], width=3)),
        row=1, col=1)

    fig5.add_trace(go.Pie(
        labels = list(day_time_sorted.keys()),
        values = list(day_time_sorted.values()),
        hoverinfo = 'percent',
        textinfo = 'label+value',
        marker_colors = red_shades
        ),
        row = 1, col = 2
    )

    fig5.update_layout(
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
        showlegend = False
    )
        
    fig5.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Spetember', 'October', 'November', 'December']
        )
    )

    return html0, html1, html2, html3, fig1, html4, html5, fig2, html6, fig5

    
if __name__ == '__main__':
    app.run_server(debug=True)
                      
