import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import random
import pandas as pd
import plotly.express as px
from FieldModel import FieldModel
import dash_bootstrap_components as dbc

# Set up the Dash app with external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the Dash app
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Field Model Simulation",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P("This is a simple Agent-Based model of a farm field where agents of farm block grow and produce crops. "
                       "The agents grow at a random rate each step, and when they reach a certain height, they can be harvested. "
                       "The model is implemented using the Mesa library. "
                       "For more details, see the "),
                html.A("Medium Article", href='https://medium.com/p/a6259081ab07', target="_blank"),
            ], className="my-3"),
            html.Div([
                html.Label("Width"),
                dcc.Slider(id='width-slider',
                           min=10,
                           max=50,
                           value=10,
                           step=5,
                           marks={i: str(i) for i in range(10, 51, 5)},
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], className="my-2"),
            html.Div([
                html.Label("Height"),
                dcc.Slider(id='height-slider',
                           min=10,
                           max=50,
                           value=10,
                           step=5,
                           marks={i: str(i) for i in range(10, 51, 5)},
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], className="my-2"),
            html.Div([
                html.Label("Minimum Height to Harvest"),
                dcc.Slider(id='min-height-slider',
                           min=0.0,
                           max=5.0,
                           value=2.4,
                           step=0.1,
                           marks={i / 10: str(i / 10) for i in range(0, 51, 10)},
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], className="my-2"),
            html.Div([
                html.Label("Harvesting Capacity per Step"),
                dcc.Slider(id='harvest-capacity-slider',
                           min=1,
                           max=10,
                           value=1,
                           step=1,
                           marks={i: str(i) for i in range(1, 11)},
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], className="my-2"),
            html.Div([
                html.Label("Rain Probability"),
                dcc.Slider(id='rain-probability-slider',
                           min=0.0,
                           max=1.0,
                           value=0.3,
                           step=0.05,
                           marks={i / 10: str(i / 10) for i in range(0, 11)},
                           tooltip={"placement": "bottom", "always_visible": True}),
            ], className="my-2"),
            dbc.Button('Run Model', id='run-button', n_clicks=0, color="primary", className="my-3"),
        ], width=4, className="bg-light p-3 rounded"),
        dbc.Col([
            dcc.Loading(
                id="loading",
                type="default",
                children=html.Div(id='graphs', style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'})
            )
        ], width=8)
    ])
], fluid=True, style={"max-width": "1200px", "margin": "auto", "padding": "20px"})

# Callback to update the graphs based on the inputs
@app.callback(Output('graphs', 'children'),
              Input('run-button', 'n_clicks'),
              State('width-slider', 'value'),
              State('height-slider', 'value'),
              State('min-height-slider', 'value'),
              State('harvest-capacity-slider', 'value'),
              State('rain-probability-slider', 'value'))
def update_graphs(n_clicks, width, height, min_height, harvest_capacity, rain_prob):
    if n_clicks > 0:
        random.seed(100)
        model = FieldModel(width, height, minimum_height_to_harvest=min_height,
                           harvesting_capacity_per_step=harvest_capacity, rain_probability=rain_prob)
        for i in range(3240):
            model.step()

        data = model.datacollector.get_model_vars_dataframe()

        # Create Plotly figures
        figs = []

        # Plot Average Height Over Time
        fig = px.line(data, y="Average Height", title="Average Height Over Time")
        fig.update_xaxes(title="Steps")
        fig.update_yaxes(title="Average Height")
        figs.append(dcc.Graph(figure=fig, style={'width': '48%', 'display': 'inline-block'}))

        # Plot Cashflow Over Time
        fig = px.line(data, y="Cashflow", title="Cashflow Over Time")
        fig.update_xaxes(title="Steps")
        fig.update_yaxes(title="Cashflow")
        figs.append(dcc.Graph(figure=fig, style={'width': '48%', 'display': 'inline-block'}))

        # Plot Number Harvested Over Time
        fig = px.line(data, y="Number Harvested", title="Number Harvested Over Time")
        fig.update_xaxes(title="Steps")
        fig.update_yaxes(title="Number Harvested")
        figs.append(dcc.Graph(figure=fig, style={'width': '48%', 'display': 'inline-block'}))

        # Plot Distribution of Agent Heights at Final Step
        agent_height = model.datacollector.get_agent_vars_dataframe().reset_index()
        agent_data = agent_height[agent_height['Step'] == 3239]
        fig = px.histogram(agent_data, x='Height', nbins=20, title="Distribution of Agent Heights at Final Step")
        fig.update_xaxes(title="Height")
        fig.update_yaxes(title="Frequency")
        figs.append(dcc.Graph(figure=fig, style={'width': '48%', 'display': 'inline-block'}))

        return figs

    return []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
