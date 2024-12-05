################################################ CITI BIKE DASHBOARD #####################################################

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


# Set page configuration
st.set_page_config(page_title='Citi Bike Dashboard', layout='wide')

# Add a title and description
st.title("Citi Bike Dashboard")
st.markdown(
    """
    Welcome to the Citi Bike Dashboard! 🚴‍♀️  

    Citi Bike, a leading bike-sharing facility in New York City, has seen a surge in popularity since its launch in 2013. 
    The Covid-19 pandemic further boosted its adoption as a sustainable and convenient mode of transportation.  

    However, with increasing demand comes operational challenges. Citi Bike is currently facing **distribution issues**, such as:  
    - Stations running out of available bikes during peak times.  
    - Stations being full, making it difficult to return bikes.  

    Explore the visualizations below to dive into the data and uncover trends in Citi Bike usage.  
    """
)

########################## Import Data ###########################################################################################

# Load datasets
file_reduced_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Data\Prepared Data\reduced_citibike_data.csv"
df_reduced = pd.read_csv(file_reduced_path, low_memory=False)

file_weather_trips_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Data\Prepared Data\merged_weather_trips.csv"
df_trips = pd.read_csv(file_weather_trips_path, low_memory=False)

file_top20_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Data\Prepared Data\top20_stations.csv"
df_top20 = pd.read_csv(file_top20_path, low_memory=False)


########################################### Define the Charts #####################################################################

# Create the Bar Chart
fig = go.Figure(
    go.Bar(
        x=df_top20['start_station_name'],  
        y=df_top20['value'],             
        marker={
            'color': df_top20['value'],    
            'colorscale': [[0, '#66c2a5'], [1, '#3288bd']] 
        }
    )
)

# Update Layout for aesthetics
fig.update_layout(
    title='Top 20 Most Popular Bike Stations in New York',
    xaxis_title='Start Stations',
    yaxis_title='Number of Trips',
    xaxis_tickangle=-45,  
    xaxis=dict(
        tickfont=dict(size=10) 
    )
)
st.plotly_chart(fig, use_container_width=True)


# Create the Line Chart

# Create Dual-Axis Line Chart
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add line for daily bike rides
fig_2.add_trace(
    go.Scatter(
        x=df_trips['date'], 
        y=df_trips['trip_count'], 
        name='Daily Bike Rides',
        line=dict(color='blue')
    ),
    secondary_y=False
)

# Add line for average daily temperature
fig_2.add_trace(
    go.Scatter(
        x=df_trips['date'], 
        y=df_trips['avg_temp'], 
        name='Daily Temperature',
        line=dict(color='red')
    ),
    secondary_y=True
)

# Update layout
fig_2.update_layout(
    title='Daily Bike Rides and Temperatures in New York',
    xaxis_title='Date',
    yaxis_title='Bike Rides (Primary Y-Axis)',
    yaxis2_title='Temperature (°C) (Secondary Y-Axis)',
    legend=dict(
        orientation="h", 
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
st.plotly_chart(fig_2, use_container_width=True)


# Add the header
st.subheader("Citi Bike Trips across New York")

# Display the image
map_image_path = "citibike_map.png"
st.image(map_image_path, caption="Citi Bike Trips Map", width=1200)



