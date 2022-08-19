# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:19:38 2022

@author: Rjjam
"""
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

#pokemon information
url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
data = pd.read_csv(url, index_col = 0)

searchable_columns = data.columns[3:].tolist()
searchable_columns.sort()

#stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

print(data.head())

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div([
        html.H1(children="Pokemon Statistics", 
                className = "header-title",
                ),
        html.P(
            children="Visualiser of Pokemon Statistics Over all Generations",
            className = "header-description",
            ),
        ],
        className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Statistics", className="menu-title"),
                        dcc.Dropdown(
                            id="stat-filter",
                            options=[
                                {"label": stats, "value": stats}
                                for stats in searchable_columns
                            ],
                            value = "Attack",
                            searchable = True,
                            clearable = False,
                            multi = True,
                            placeholder="Select an attribute",
                            className="dropdown",
                        ),
                    ],
                ), 
            html.Div(
                children =[
                    html.Div(children="Pokemon", className="menu-title"),
                        dcc.Dropdown(
                            id="pokemon-filter",
                            options=[
                                {"label": name, "value": name}
                                for name in data["Name"]
                            ],
                            value = data["Name"],
                            searchable = True,
                            clearable = True,
                            placeholder="Select a pokemon",
                            className="dropdown",
                        )
                ],
                className = "menu"
            ),
            html.Div(
                dcc.Graph(
                    id="poke-chart", config={"displayModeBar": False},
                ),
                className = "card",
            ) 
        ],
    )
   #className = "wrapper",
   ]
)

@app.callback(
    Output("poke-chart", 'figure'),
    [
     Input("stat-filter", "value"),
     Input("pokemon-filter", "value")
    ],
)
def update_charts(statistics, name):
    
    num_of_statistics = len(statistics)
    print(statistics[0])
    print(name)
    for x in statistics:
        poke_chart_figure = {
            "data": [
                {
                    "x": name,
                    "y": data.loc[data["Name"] == name, "Attack"],
                    "type": "lines",
                },
            ],
            "layout": {
                "title": {
                       "text":"Pokemon Statistics",
                       "x":0.05,
                       "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#17B897"],
            },
        }
    
    return poke_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)