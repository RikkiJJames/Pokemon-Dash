# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:19:38 2022

@author: Rjjam
"""
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from model import Model


#pokemon information
url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
data = pd.read_csv(url, index_col = 0)
data.loc[data['Name'].str.contains('Mega'), 'sport'] = 'ball sport'
print(data.columns)
#Removing other characters from Mega Pokemon
#data['OtherName'] = data['Name'].str.extract(r'(^.*Mega.*$)', expand=False)
#print("printing" + data["OtherName"])

#Selecting Columns to be searched in radar graph
searchable_columns = ["Attack","Defense","HP","Speed", "Sp. Atk","Sp. Def"]
searchable_columns.sort()



#stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

#print(data.head())

app = dash.Dash(__name__)
app.title = "Poké App"

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
                            value = searchable_columns,
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
                            #value = data["Name"],
                            value = ["Bulbasaur"],
                            searchable = True,
                            clearable = True,
                            multi = True,
                            placeholder="Select a pokemon",
                            className="dropdown",
                        ),    
                ],

            ),
            html.Div(
                children =[
                    html.Div(children="Graph Type", className="menu-title"),
                        dcc.RadioItems(
                            id="graph-filter",
                            options=["Radar", "Line"],
                            value = "Radar",
                        ),
                ],
            ),
        ],
        className = "menu",
    ),
    html.Div(
        children = [
            html.Div(
                children = dcc.Graph(
                               id="poke-model", config={"scrollZoom": True}
                           ),
                           className = "card",
            ),
            html.Div(
                children = dcc.Graph(
                               id="poke-chart", config={"displayModeBar": True},
                           ),
                           className = "card",
            ),
        ],
        className = "wrapper",    
        ),
    ]
)

@app.callback(
    [dash.Output("poke-chart", 'figure'), dash.Output("poke-model", "figure")],
    [
     dash.Input("stat-filter", "value"),
     dash.Input("pokemon-filter", "value"),
     dash.Input("graph-filter", "value")
    ],
)
def update_charts(statistics, name, graph_type):
    
    #print("name before is")
    #print(name)
    
    if name == []:
        name = data["Name"]
    
    #print("name after is ")
    #print(name)
    attributes = statistics
    
    fig = go.Figure()
    
    if graph_type == "Radar":
        for pokemon in name:
            #print(pokemon)
            #print(type(data[statistics] [data["Name"] == pokemon].values.tolist()))
            #print(data[statistics] [data["Name"] == pokemon].values.tolist()[0])
            
            fig.add_trace(
                go.Scatterpolar(
                    r = data[statistics] [data["Name"] == pokemon].values.tolist()[0],
                    theta = attributes,
                    name = f"#{data[data['Name'] == pokemon].index[0]}: {pokemon}",
                    fill = "toself",
                )
            )
        fig.update_layout(
            title_text = "Pokemon Attributes",
            polar=dict(
                radialaxis=dict(
                visible=True,
                range = [0, data[statistics][data["Name"] == pokemon].max()]
                )),
            showlegend=True
            )
    else:
        for pokemon in name:
            y_values = data[statistics][data["Name"] == pokemon].values.tolist()[0]
            print(y_values)
            fig.add_trace(go.Scatter(x= [statistics] * len(y_values), y = y_values,
                    mode='lines+markers',
                    name = f"#{data[data['Name'] == pokemon].index[0]}: {pokemon}"
                    )
            )
            
       
            
        fig.update_layout(showlegend = True)
  
        
    
    
    #print(type(data[statistics] [data["Name"] == name]))
    #print(statistics)
    #print(name)
    
    return fig, Model(name[0])



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader = True)