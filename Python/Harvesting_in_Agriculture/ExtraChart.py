from mesa.visualization.ModularVisualization import VisualizationElement, CHART_JS_FILE
import numpy as np

class HistogramModule(VisualizationElement):
    package_includes = [CHART_JS_FILE]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width, attribute):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        self.attribute = attribute
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins, canvas_width, canvas_height)
        self.js_code = "elements.push(" + new_element + ");"
        
    def render(self, model):
        attribute_vals = [getattr(agent, self.attribute) for agent in model.schedule.agents]
        hist = np.histogram(attribute_vals, bins=self.bins)[0]
        return [int(x) for x in hist]
