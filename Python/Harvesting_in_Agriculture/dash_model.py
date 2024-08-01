import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from FieldModel import FieldModel

# Streamlit app code
st.title("Field Model Simulation")

# Create sliders for the model parameters
width = st.slider("Width", min_value=10, max_value=50, value=30, step=1)
height = st.slider("Height", min_value=10, max_value=50, value=30, step=1)
minimum_height_to_harvest = st.slider("Minimum Height to Harvest",
                                      min_value=0.0,
                                      max_value=5.0,
                                      value=2.4,
                                      step=0.1)
harvesting_capacity_per_step = st.slider("Harvesting Capacity per Step",
                                         min_value=1,
                                         max_value=10,
                                         value=1,
                                         step=1)
rain_probability = st.slider("Rain Probability",
                             min_value=0.0,
                             max_value=1.0,
                             value=0.3,
                             step=0.05)

# Set the random seed for reproducibility
random.seed(100)

# Initialize session state if it doesn't exist
if 'figures' not in st.session_state:
    st.session_state.figures = []

# Run model when the button is clicked
if st.button("Run Model"):
    # Create the model
    model = FieldModel(
        width=width,
        height=height,
        minimum_height_to_harvest=minimum_height_to_harvest,
        harvesting_capacity_per_step=harvesting_capacity_per_step,
        rain_probability=rain_probability)

    # Set up a progress bar
    progress_bar = st.progress(0)
    total_steps = 3240

    # Run the model with progress bar update
    for i in range(total_steps):
        model.step()
        # Update the progress bar
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)

    # Extract and display results
    data = model.datacollector.get_model_vars_dataframe()

    # Store figures with titles
    fig_list = []

    # Plotting Average Height
    fig, ax = plt.subplots()
    ax.plot(data["Average Height"])
    ax.set_xlabel("Steps")
    ax.set_ylabel("Average Height")
    ax.grid(True)
    fig_list.append(("Average Height Over Time", fig))

    # Plotting Cashflow
    fig, ax = plt.subplots()
    ax.plot(data["Cashflow"])
    ax.set_xlabel("Steps")
    ax.set_ylabel("Cashflow")
    ax.grid(True)
    fig_list.append(("Cashflow Over Time", fig))

    # Plotting Number Harvested
    fig, ax = plt.subplots()
    ax.plot(data["Number Harvested"])
    ax.set_xlabel("Steps")
    ax.set_ylabel("Number Harvested")
    ax.grid(True)
    fig_list.append(("Number Harvested Over Time", fig))

    # Extract agent data and plot height distribution
    agent_height = model.datacollector.get_agent_vars_dataframe().reset_index()
    agent_data = agent_height[agent_height['Step'] == 3239]
    fig, ax = plt.subplots()
    sns.histplot(data=agent_data, x='Height', bins=20, ax=ax)
    ax.set_xlabel("Height")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    fig_list.append(("Distribution of Agent Heights at Final Step", fig))

    # Store the figures in session state
    st.session_state.figures.extend(fig_list)

# Display all stored figures in a 2x2 grid
for i, (title, fig) in enumerate(st.session_state.figures):
    col = st.columns(2)[i % 2]
    with col:
        st.subheader(title)
        st.pyplot(fig)
