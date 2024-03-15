



# import the library

import networkx as nx

import plotly.graph_objects as go

import pandas as pd

import numpy as np

import random

import dash




# ################

# Create a graph

# ################

# Create an empty graph with no nodes and no edges

G = nx.Graph()



# add a single node, class = areakey, value and label are the same, name of the node is "LU_MES"

G.add_node("LU_MES", classname="areakey", value=1, label="LU_MES")


# add a single node, classname = areakey, value and label are the same, name of the node is "LAM_EH"

G.add_node("LAM_EH", classname="areakey", value=1, label="LAM_EH")



# #######################################################


# add equipment nodes, classname = equipment, value and label are the same

# add node Reactor R101, classname = equipment, value and label are the same, name of the node is "R101"

G.add_node("R101", classname="equipment", label="R101")

G.add_node("R102", classname="equipment", label="R102")


# add sensor nodes, classname = sensor, type = temperature, value and label are the same

G.add_node("T101", classname="sensor", type="temperature", label="T101")
G.add_node("T102", classname="sensor", type="temperature", label="T102")
G.add_node("P101", classname="sensor", type="pressure", label="P101")
G.add_node("P102", classname="sensor", type="pressure", label="P102")
G.add_node("F101", classname="sensor", type="flow", label="F101")
G.add_node("F102", classname="sensor", type="flow", label="F102")
G.add_node("L101", classname="sensor", type="level", label="L101")
G.add_node("L102", classname="sensor", type="level", label="L102")


# add connection between sensor nodes and reactor R101

G.add_edge("R101", "T101", classname="contains")
G.add_edge("R102", "T102", classname="contains")
G.add_edge("R101", "P101", classname="contains")
G.add_edge("R102", "P102", classname="contains")
G.add_edge("R101", "F101", classname="contains")
G.add_edge("R102", "F102", classname="contains")
G.add_edge("R101", "L101", classname="contains")
G.add_edge("R102", "L102", classname="contains")



# create node for the process, classname = recipe, label = "Tinuvin"

G.add_node("Tinuvin", classname="recipe", label="Tinuvin")
G.add_node("Uvinul", classname="recipe", label="Uvinul")

# make directed edges of equipment nodes to the process nodes

G.add_edge("Tinuvin", "R101", classname="contains")
G.add_edge("Tinuvin", "R102", classname="contains")

# make directed edge of equipment node to the process node, R101 -> R102

G.add_edge("R101", "R102", classname="processconnection")


# make directed edges of equipment nodes to the process nodes Uvinul

G.add_edge("Uvinul", "R101", classname="contains")
G.add_edge("Uvinul", "R102", classname="contains")

# make directed edge of equipment node to the process node, R102 -> R101 

G.add_edge("R102", "R101", classname="processconnection")



# make dash app with cytoscape

# make graph available in the app via cytoscape


import dash_cytoscape as cyto

from dash import html


# computer transfer graph to cytoscape format

elements = nx.readwrite.json_graph.cytoscape_data(G)['elements']

# create app

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'circle'},
        # style edges and nodes, make connections between nodes via taxis
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'background-color': '#11479e',
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'line-color': '#9dbaea'
                }
            }
        ],
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)

# run the app



















































