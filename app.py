# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:19:38 2022

@author: Rjjam
"""
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, ctx, dash_table
from model import generate_model
from clean_csv import clean_data
from dash.exceptions import PreventUpdate

#Cleans original csv data to be usable
#clean_data()

#Load cleaned csv data
pokedex = pd.read_csv("data/pokedex.csv", index_col = 0)
movesets = pd.read_csv("data/movesets.csv")

#Load stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

#Selecting Columns to be searched in graph's
searchable_columns = ["Attack","Defense","HP","Speed", "Sp. Atk","Sp. Def"]
searchable_columns.sort()

#Selecting Columns to be selected in Tables
info_columns = ["Name", "Type 1", "Type 2", "Generation", "Legendary"]



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
                                for name in pokedex["Name"]
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
            
            html.Div(
                children = [
                    dash_table.DataTable(
                    columns = [
                        {"name": i, "id": i} for i in pokedex[info_columns]
                    ], id = "info-table",
                    filter_query = "",
                    style_cell_conditional=[
                        {
                        'textAlign': 'center'
                        }
                    ],
                    style_data_conditional=[
                        {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    )   
               ],
               className = "card",
            ),
            html.Div(
                children = [
                    dash_table.DataTable(
                    page_current = 0,
                    page_size = 5,
                    page_action='custom',
                    filter_query = "",
                    id = "move-table",
                    style_cell_conditional= [
                        {
                        'textAlign': 'center'
                        }
                    ],
                    style_data_conditional=[
                        {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    )   
               ],
               className = "card",
            ),   
        ],
        className = "wrapper",  
        ),
        
    ],
)


@app.callback(
    [
     dash.Output('info-table', "data"),
     dash.Output('move-table', "data"),
     dash.Output('move-table', "columns")
     
    ],
    [
     dash.Input('info-table', "filter_query"),
     dash.Input('move-table', "filter_query"),
     dash.Input("pokemon-filter", "value"),
     dash.Input('move-table', "page_current"),
     dash.Input('move-table', "page_size"),
    ]
)

def update_table(info_filter, move_filter, pokemon, page_current, page_size):
    
    if type(pokemon) == str:
        pokemon = [pokemon]
    
    info_table = pd.DataFrame()
    move_table = pd.DataFrame()

    if len(pokemon) > 1:
        for x in range(len(pokemon)):
            info_table = info_table.append([(pokedex[pokedex["Name"].str.match(pokemon[x])])])
            move_table = move_table.append([(movesets[movesets["Name"].str.match(pokemon[x])])])
    else:
        info_table = pokedex[pokedex["Name"].str.match(pokemon[0])]
        move_table = movesets[movesets["Name"].str.match(pokemon[0])]
    
    move_table = move_table.iloc[:, 
        page_current * page_size: (page_current + 1) * page_size
        ]
    
    columns = [
        {"name": i, "id": i} for i in movesets.columns[
            1 + page_current * page_size: (page_current + 1) * page_size
        ]
    ]
    
    return info_table.to_dict('records'), move_table.to_dict('records'), columns

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

        child = dcc.Dropdown(
            id = "pokemon-filter",
            options=[
            {"label": name, "value": name}
            for name in pokedex["Name"]
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
             for name in pokedex["Name"]
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
        name = pokedex["Name"][0]
    
    if type(name) == str:
        name = [name]
    

         
    if graph_type == "Radar" and multi_select == True:
        for pokemon in name:
            fig.add_trace(
                go.Scatterpolar(
                    r = pokedex[statistics] [pokedex["Name"] == pokemon].values.tolist()[0],
                    theta = attributes,
                    name = f"#{pokedex[pokedex['Name'] == pokemon].index[0]}: {pokemon}",
                    fill = "toself",
                )
            )
        
    elif graph_type == "Radar" and multi_select == False:
        for pokemon in name:
            fig.add_trace(
                go.Scatterpolar(
                    r = pokedex[statistics] [pokedex["Name"] == pokemon].values.tolist()[0],
                    theta = attributes,
                    name = f"#{pokedex.index[pokedex['Name'] == pokemon].to_list()[0]}: {pokemon}",
                    fill = "toself",
                )
            )

    elif graph_type == "Line" and multi_select == True:
        for pokemon in name:
            y_values = pokedex[statistics][pokedex["Name"] == pokemon].values.tolist()[0]
            print(statistics * len(y_values))
            print(y_values)
            fig.add_trace(go.Scatter(x= statistics * len(y_values), y = y_values,
                    mode='lines+markers',
                    name = f"#{pokedex[pokedex['Name'] == pokemon].index[0]}: {pokemon}"
                    )
            )

    elif graph_type == "Line" and multi_select == False:
        for pokemon in name:
            y_values = pokedex[statistics][pokedex["Name"] == pokemon].values.tolist()[0]
            fig.add_trace(go.Scatter(x = statistics * len(y_values), y = y_values,
                    mode='lines+markers',
                    name = f"#{pokedex.index[pokedex['Name'] == pokemon].to_list()[0]}: {pokemon}"
                    )
            )
            
    fig.update_layout(
        title_text = "Pokemon Attributes",
        polar=dict(
            radialaxis=dict(
            visible=True,
            range = [0, pokedex[statistics][pokedex["Name"] == pokemon].max()]
            )),
        showlegend=True,
        height = 400
        )
   
    return fig, generate_model(name[0])

if __name__ == "__main__":
    app.run_server(debug = False, use_reloader = True)