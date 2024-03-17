



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


G.add_edge("LU_MES", "Tinuvin", classname="contains")



# copy node R101 and add it tot the graph, class = topology, value and label are the same, name of the node is "R101"

G.add_node("Tinuvin_R101", classname="topology", label="R101")

# connect node Tinuvin_R101 topology to R101 equipment

G.add_edge("Tinuvin", "Tinuvin_R101", classname="contains")


# copy node R102 and add it tot the graph, class = topology, value and label are the same, name of the node is "R102"
G.add_node("Tinuvin_R102", classname="topology", label="R102")
G.add_edge( "Tinuvin", "Tinuvin_R102", classname="contains")



G.add_edge("Tinuvin_R101", "R101", classname="contains")
G.add_edge("Tinuvin_R102", "R102", classname="contains")




# G.add_edge("Tinuvin", "R101", classname="contains")
# G.add_edge("Tinuvin", "R102", classname="contains")

# make directed edge of equipment node to the process node, R101 -> R102

G.add_edge("Tinuvin_R101", "Tinuvin_R102", classname="processconnection")


# make directed edges of equipment nodes to the process nodes Uvinul




G.add_node("Uvinul_R101", classname="topology", label="R101")
G.add_node("Uvinul_R102", classname="topology", label="R102")

G.add_edge("Uvinul", "Uvinul_R101", classname="contains")
G.add_edge("Uvinul", "Uvinul_R102", classname="contains")


G.add_edge("Uvinul_R102", "Uvinul_R101", classname="processconnection")


G.add_edge("Uvinul_R101", "R101", classname="contains")
G.add_edge("Uvinul_R102", "R102", classname="contains")



# make an combination of nodes and edges analysis

# print(G.nodes(data=True))













# make dash app with cytoscape

# make graph available in the app via cytoscape


import dash_cytoscape as cyto

from dash import html


# computer transfer graph to cytoscape format

elements = nx.readwrite.json_graph.cytoscape_data(G)['elements']



base_figure_stylesheet = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "text-wrap": "wrap",
            "shape": "round-rectangle",
            "width": 90,
            "height": 45,
            "background-color": "white",
            "border-color": "grey",
            "border-width": 1,
            "border-opacity": 1,
            "text-halign": "center",
            "text-valign": "center",
            "font-size": 10,
            "text-opacity": 1,
            "color": "black",
        }
    },
    {
        "selector": "node[classname = 'areakey']",
        "style": {
            "background-color": "blue",
        }
    },
    {
        "selector": "node[classname = 'equipment']",
        "style": {
            "background-color": "green",
            "color": "white",
        }
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "taxi",
            "target-arrow-shape": "triangle",
            "taxi-direction": "rightward",
            "text-wrap": "wrap",
            "text-background-color": "grey",
            "text-background-opacity": 1,
            "text-background-padding": 3,
            "color": "black",
            "font-size": 10,
            "text-border-color": "grey",
            "text-border-width": "1px",
            "text-border-opacity": "0.8",
        }
    },
    {
        "selector": "edge[classname = 'contains']",
        "style": {
            "curve-style": "bezier",
            "line-color": "blue",
        }
    }
]





# create app

app = dash.Dash(__name__)

app.layout = html.Div(
    # style={'width': '1200px', 'height': '800px', 'margin': 'auto', 'padding': '10px'},
    style={'width': '100%', 'height': '100vh', "align-items": "center", "justify-content": "center", "display": "flex"},
    children=[
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        # layout={'name': 'circle'},
        style={'width': '1200px', 'height': '800px'},
        # style edges and nodes, make connections between nodes via taxis
        stylesheet=base_figure_stylesheet
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)

# run the app



















































