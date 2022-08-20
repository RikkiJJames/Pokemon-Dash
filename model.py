# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:03:52 2022

@author: Rjjam
"""

import dash
import dash_obj_in_3dmesh

import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import geometry_tools



axis_template = {
    "showbackground": False,
    "visible" : False,
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    #'uirevision':'same_all_the_time', #this keeps camera position etc the same when data changes.
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectmode" : "data",
        "camera": {"up":{"x":0, "y":1, "z":0}, "eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=1.25, y=1.25, z=1.25)
)

def Model(model_name):
    figure= dict({
        "data": geometry_tools.import_geometry([model_name]),
        "layout": plot_layout,
    })
    return figure

      
