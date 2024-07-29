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

# Model Code below

def find_best_patch(model):
    agents = model.schedule.agents
    max_price = -float('inf')
    best_patch = None

    for agent in agents:
        if agent.price_at_mill > max_price:
            max_price = agent.price_at_mill
            best_patch = agent.pos

    return best_patch

def average_height(model):
    return np.mean([agent.height for agent in model.schedule.agents])

class PatchAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.sugar_content = random.uniform(0, 0.112)
        self.height = random.uniform(0, 2)
        self.price_at_mill = 0
        self.pos = None

    def step(self):
        if self.model.rain <= self.model.rain_probability:
            self.height += 0.00123 * 2
            self.sugar_content += 0.0000688 * 2
        else:
            self.height += 0.00123
            self.sugar_content += 0.0000688
            self.model.cashflow -= 0.3

        self.price_at_mill = self.calculate_price_at_mill()

        if (self.model.best_patch == self.pos and 
            self.height >= self.model.minimum_height_to_harvest and 
            self.model.current_harvesting_capacity > 0):
            self.being_harvested()
            self.model.current_harvesting_capacity -= 1

    def calculate_price_at_mill(self):
        if self.pos is None:
            raise ValueError("Agent position is not set.")
        x1, y1 = self.pos
        x2, y2 = 11, 0
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        price_at_mill = 14000 * (self.sugar_content * (1 - (distance * (0.6 / 16.9))))
        return round(price_at_mill, 2)

    def being_harvested(self):
        self.height = 0
        self.sugar_content = 0
        self.model.number_harvested += 1
        self.model.cashflow += self.price_at_mill
        self.model.cashflow -= 0.05

class FieldModel(Model):
    def __init__(self, width, height, minimum_height_to_harvest=2.4, harvesting_capacity_per_step=1, rain_probability=0.3):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.rain = None
        self.best_patch = None
        self.harvesting_capacity_per_step = harvesting_capacity_per_step
        self.number_harvested = 0
        self.cashflow = 1000000
        self.minimum_height_to_harvest = minimum_height_to_harvest
        self.current_harvesting_capacity = self.harvesting_capacity_per_step
        self.rain_probability = rain_probability

        agent_id = 0
        for x in range(width):
            for y in range(height):
                if x == (width - 1) and y == 0:
                    continue
                
                a = PatchAgent(agent_id, self)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))
                agent_id += 1

        self.datacollector = DataCollector(
            model_reporters={"Average Height": average_height, "Cashflow": "cashflow", "Number Harvested": "number_harvested"},
            agent_reporters={"Height": "height"}
        )

    def step(self):
        self.rain = random.uniform(0, 1)
        self.best_patch = find_best_patch(self)
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_harvesting_capacity = self.harvesting_capacity_per_step





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
