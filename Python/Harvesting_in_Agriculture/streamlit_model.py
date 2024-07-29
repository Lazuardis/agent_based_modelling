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
minimum_height_to_harvest = st.slider("Minimum Height to Harvest", min_value=0.0, max_value=5.0, value=2.4, step=0.1)
harvesting_capacity_per_step = st.slider("Harvesting Capacity per Step", min_value=1, max_value=10, value=1, step=1)
rain_probability = st.slider("Rain Probability", min_value=0.0, max_value=1.0, value=0.3, step=0.05)

# Set the random seed for reproducibility
random.seed(100)

# Run model when the button is clicked
if st.button("Run Model"):
    # Create the model
    model = FieldModel(width=width, height=height, minimum_height_to_harvest=minimum_height_to_harvest, harvesting_capacity_per_step=harvesting_capacity_per_step, rain_probability=rain_probability)
    
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

    # Plotting in subplots with two columns
    col1, col2 = st.columns(2)

    # Plotting Average Height
    with col1:
        st.subheader("Average Height Over Time")
        fig, ax = plt.subplots()
        ax.plot(data["Average Height"])
        ax.set_xlabel("Steps")
        ax.set_ylabel("Average Height")
        ax.grid(True)
        st.pyplot(fig)

    # Plotting Cashflow
    with col2:
        st.subheader("Cashflow Over Time")
        fig, ax = plt.subplots()
        ax.plot(data["Cashflow"])
        ax.set_xlabel("Steps")
        ax.set_ylabel("Cashflow")
        ax.grid(True)
        st.pyplot(fig)

    # Plotting Number Harvested
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Number Harvested Over Time")
        fig, ax = plt.subplots()
        ax.plot(data["Number Harvested"])
        ax.set_xlabel("Steps")
        ax.set_ylabel("Number Harvested")
        ax.grid(True)
        st.pyplot(fig)

    # Extract agent data and plot height distribution
    with col4:
        st.subheader("Distribution of Agent Heights at Final Step")
        agent_height = model.datacollector.get_agent_vars_dataframe().reset_index()
        agent_data = agent_height[agent_height['Step'] == 3239]
        fig, ax = plt.subplots()
        sns.histplot(data=agent_data, x='Height', bins=20, ax=ax)
        ax.set_xlabel("Height")
        ax.set_ylabel("Frequency")
        ax.grid(True)
        st.pyplot(fig)
