import mesa
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from ExtraChart import HistogramModule
import seaborn as sns
import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import solara
from matplotlib.figure import Figure
from FieldModel import FieldModel


# Visualization Code below


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "w": 0.5, "h": 0.5}

    heights = [1, 2, 3, 4, 5]
    sizes = [0.2, 0.4, 0.6, 0.8, 1, 1.2]
    colors = [
        rgb_to_hex((0, 0, 0)),        # black
        rgb_to_hex((0, 64, 0)),       # very dark green
        rgb_to_hex((0, 128, 0)),      # dark green
        rgb_to_hex((0, 192, 0)),      # medium green
        rgb_to_hex((0, 255, 0)),      # normal green
        rgb_to_hex((0, 255, 0))       # normal green for any height above 5
    ]

    for i, height in enumerate(heights):
        if agent.height <= height:
            portrayal["w"] = sizes[i]
            portrayal["h"] = sizes[i]
            portrayal["Color"] = colors[i]
            portrayal["Layer"] = 0
            break

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 12, 12, 500, 500)

chart = mesa.visualization.ChartModule(
    [{"Label": "Cashflow", "Color": "Black"}], data_collector_name="datacollector"
)

histogram = HistogramModule(list(range(10)), 200, 500, attribute="height")

server = mesa.visualization.ModularServer(FieldModel,
                       [grid, 
                        # chart,
                        histogram
                        ],
                       "Field Model",
                       {"width":12, "height":12})
server.port = 8521 # The default
server.launch()
