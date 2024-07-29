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
        
        
        
        
def run_model(width, height, minimum_height_to_harvest, harvesting_capacity_per_step, rain_probability):
    # Initialize the model
    model = FieldModel(width, height, minimum_height_to_harvest, harvesting_capacity_per_step, rain_probability)
    
    # Run the model for a specified number of steps
    num_steps = 3240  # Example number of steps
    for _ in range(num_steps):
        model.step()
    
    # Collect the results
    results = model.datacollector.get_model_vars_dataframe()
    return results