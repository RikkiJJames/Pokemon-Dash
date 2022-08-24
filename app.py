# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:19:38 2022

@author: Rjjam
"""
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, ctx
from test2 import main3
import re
from dash.exceptions import PreventUpdate

"""
#Pokemon Information Github location
url = "https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv"
data = pd.read_csv(url, index_col = 0)


#clean pokemon names and remove mega
def clean_names(pokemon_name):
    
    if re.search('.*Mega.*', pokemon_name):
        index = re.search('Mega.*', pokemon_name).start()
        
        return pokemon_name[index:]
    else:
        return pokemon_name
    


    
#Removing other characters from Mega Pokemon
data["Name"] = data["Name"].apply(clean_names)

#Save cleaned data to csv
data.to_csv('data/pokedex.csv', index = False, encoding='utf-8')
"""

data = pd.read_csv("data/pokedex.csv")

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
                    html.Div(children="Selection Type", className="menu-title"),
                        dcc.RadioItems(
                            id="selection-filter",
                            options=["Single", "Multiple"],
                            value = "Single",
                        ),
                ],
            ),
            html.Div(
                children =[
                    html.Div(children="Pokemon", className="menu-title"),
                        html.Div( id = "pokemon-update-list",
                            children = dcc.Dropdown(
                                id = "pokemon-filter",
                                options=[
                                {"label": name, "value": name}
                                for name in data["Name"]
                                ],
                                value = ["Bulbasaur"],
                                searchable = True,
                                clearable = False,
                                multi = False,
                                className="dropdown"
                            ),
                        ),
                ],
                style = {"width": "20%"},
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
    dash.Output("pokemon-update-list", "children"),
    [
     dash.Input("selection-filter", "value"),
     dash.Input("pokemon-filter", "value")
    ],
)

def update_pokemon_list(selection, pokemon):
    
    if ctx.triggered_id == "pokemon-filter":
        raise PreventUpdate
    
    pokemon_option = None
    
    if type(pokemon) == str:
        pokemon = [pokemon]
        
    if selection == "Single":
            
        pokemon_option = False
        print(pokemon)
        child = dcc.Dropdown(
            id = "pokemon-filter",
            options=[
            {"label": name, "value": name}
            for name in data["Name"]
            ],
            value = pokemon[0],
            searchable = True,
            clearable = False,
            multi = pokemon_option,
            className="dropdown")
        
            
    elif selection == "Multiple":
         pokemon_option = True
         
         child = dcc.Dropdown(
             id = "pokemon-filter",
             options=[
             {"label": name, "value": name}
             for name in data["Name"]
             ],
             value = pokemon[0],
             searchable = True,
             clearable = False,
             multi = pokemon_option,
             className="dropdown")
         
    
    return child

@app.callback(
    [dash.Output("poke-chart", 'figure'), dash.Output("poke-model", "figure")],
    [
     dash.Input("stat-filter", "value"),
     dash.Input("selection-filter", "value"),
     dash.Input("pokemon-filter", "value"),
     dash.Input("graph-filter", "value")
    ],
)

def update_charts(statistics, selection, name, graph_type):
    

    attributes = statistics
    
    fig = go.Figure()
    
    multi_select = None
    
    if selection == "Single":
            
        multi_select = False
            
    elif selection == "Multiple":
         multi_select = True
         
    if name == [] or not name:
        name = data["Name"][0]
    
    if type(name) == str:
        name = [name]
    

         
    if graph_type == "Radar" and multi_select == True:
        for pokemon in name:
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
        
    elif graph_type == "Radar" and multi_select == False:
        for pokemon in name:
            fig.add_trace(
                go.Scatterpolar(
                    r = data[statistics] [data["Name"] == pokemon].values.tolist()[0],
                    theta = attributes,
                    name = f"#{data.index[data['Name'] == pokemon].to_list()[0]}: {pokemon}",
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
    elif graph_type == "Line" and multi_select == True:
        for pokemon in name:
            print(data[statistics] [data["Name"] == pokemon].values.tolist()[0])
            y_values = data[statistics][data["Name"] == pokemon].values.tolist()[0]
            fig.add_trace(go.Scatter(x= [statistics] * len(y_values), y = y_values,
                    mode='lines+markers',
                    name = f"#{data[data['Name'] == pokemon].index[0]}: {pokemon}"
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
    elif graph_type == "Line" and multi_select == False:
        for pokemon in name:
            y_values = data[statistics][data["Name"] == pokemon].values.tolist()[0]
            fig.add_trace(go.Scatter(x= [statistics] * len(y_values), y = y_values,
                    mode='lines+markers',
                    name = f"#{data.index[data['Name'] == pokemon].to_list()[0]}: {pokemon}"
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
       
   
            
        fig.update_layout(showlegend = True)
  
        
    
    
    #print(type(data[statistics] [data["Name"] == name]))
    #print(statistics)
    #print(name)
    
    #return fig, Model(name[0])
    
    
         
    return fig, main3(name[0])


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader = True)