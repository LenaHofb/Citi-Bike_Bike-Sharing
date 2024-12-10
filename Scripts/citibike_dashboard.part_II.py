################################################ CITI BIKE DASHBOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from PIL import Image
from numerize import numerize


########################## Import Data ###########################################################################################

import os
import pandas as pd

# Check if running in Streamlit Cloud
IS_DEPLOYED = "STREAMLIT_SERVER_PORT" in os.environ

if IS_DEPLOYED:
    # Relative paths for deployment (Streamlit Cloud)
    df_path = "reduced_sample_dataset.csv"
    df_trips_path = "merged_weather_trips.csv"
    top20_path = "top20_stations.csv"
else:
    # Absolute paths for local development
    df_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Scripts\reduced_sample_dataset.csv"
    df_trips_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Scripts\merged_weather_trips.csv"
    top20_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Scripts\top20_stations.csv"

# Log paths for debugging
print(f"Using df_path: {df_path}")
print(f"Using df_trips_path: {df_trips_path}")
print(f"Using top20_path: {top20_path}")

# Load datasets
df = pd.read_csv(df_path, index_col=None)
df_trips = pd.read_csv(df_trips_path, index_col=None)
top20 = pd.read_csv(top20_path, index_col=None)

########################### Initial settings for the dashboard ##################################################################

# Set page configuration for wide mode
st.set_page_config(
    page_title="Citi Bike Dashboard",
    layout="wide"  # Enable wide screen
)

# Initialize the page variable using the sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select an aspect of the analysis",
    ["Intro Page", "Weather Component and Bike Usage", 
     "Most Popular Stations", "New York Map with Aggregated Bike Trips", "Recommendations"]
)

######################################## Define the Pages ########################################

# Add a persistent header for the dashboard
st.markdown("<h1 style='text-align: center; font-size: 36px;'>Citi Bike Strategy Dashboard 🚴‍</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)    
    
# INTRO PAGE
if page == "Intro Page":
    st.title("Welcome to the Citi Bike Dashboard! 🚴‍♀️")
    st.markdown("""
    Citi Bike, one of New York City’s leading bike-sharing services, has experienced a surge in popularity. 
    However, with increasing demand come challenges, such as:
    - Stations running out of bikes during peak hours.
    - Stations being full, making it difficult to return bikes.

    This dashboard delves into the potential reasons behind these issues and offers insights to support service improvements.
    The dashboard is divided into 5 sections to explore these aspects:
    """)

    # Load and display an image
    image_path = r"C:\Users\north\OneDrive\Dokumente\Career Foundry\Data Visualization 2\Citi-Bike_Bike-Sharing\Citibike_Vector.jpg"
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" alt="Citi Bike Rentals" style="width: 800px;"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add markdown for dashboard description
    st.markdown("""
    - **Weather Component and Bike Usage**: Explore how weather impacts ridership trends.
    - **Most Popular Stations**: Identify stations with the highest demand.
    - **New York Map with Aggregated Bike Trips**: View a static geospatial plot of bike trips.
    - **Recommendations**: Summarize insights and provide actionable suggestions.
    """)

    # Add bold and centered text
    st.markdown(
        """
        <div style="text-align: center; font-weight: bold; font-size: 18px;">
            Use the dropdown menu on the left, titled <strong>'Navigation'</strong>, to explore the different sections.
        </div>
        """,
        unsafe_allow_html=True
    )
    
# LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE
elif page == "Weather Component and Bike Usage":  # Ensure proper indentation and flow
    st.subheader("Weather Component and Bike Usage")
    st.markdown("""
    This graph shows the relationship between temperature and daily bike rides in New York City. 
    Warmer months correlate with higher bike usage, while colder months see reduced trips.
    """)

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2.add_trace(
        go.Scatter(
            x=df_trips['date'], 
            y=df_trips['trip_count'], 
            name='Daily Bike Rides',
            line=dict(color='blue')
        ),
        secondary_y=False
    )
    fig_2.add_trace(
        go.Scatter(
            x=df_trips['date'], 
            y=df_trips['avg_temp'], 
            name='Daily Temperature',
            line=dict(color='red')
        ),
        secondary_y=True
    )
    fig_2.update_layout(
        title='Daily Bike Rides and Temperatures in New York 2022',
        xaxis_title='Date',
        yaxis_title='Bike Rides (Primary Y-Axis)',
        yaxis2_title='Temperature (°C) (Secondary Y-Axis)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("""
    Warmer months (May to September) see the highest number of daily bike rides, often exceeding 100,000 trips, while colder months (January, February, November, December) experience significantly lower usage, dropping below 40,000 trips per day. These trends highlight seasonal demand variations.
    """)

# MOST POPULAR STATIONS
elif page == "Most Popular Stations":
    st.subheader("Top 20 Most Popular Bike Stations")
    st.markdown("""
    This page focuses on identifying the most popular bike stations in New York City based on the number of trips starting at each station.
    """)

# Insights about the Bar Chart
    st.markdown("""
    ### Insights:
    - The most popular station is **W 21 St & 6 Ave**, with over 120,000 trips.
    - Other highly popular stations include **West St & Chambers St** and **Broadway & E 22 St**.
    - The top 20 stations account for a significant share of the overall bike usage, indicating concentrated demand.
    - Proper resource allocation to these hotspots is essential to reduce shortages and ensure user satisfaction.
    """)
    
    fig = go.Figure(
        go.Bar(
            x=top20['start_station_name'],  
            y=top20['value'],             
            marker={'color': top20['value'], 'colorscale': [[0, '#66c2a5'], [1, '#3288bd']]}
        )
    )
    fig.update_layout(
        title='Top 20 Most Popular Bike Stations in New York',
        xaxis_title='Start Stations',
        yaxis_title='Number of Trips',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

# NEW YORK MAP PAGE
elif page == "New York Map with Aggregated Bike Trips":
    st.subheader("New York Map with Aggregated Bike Trips")
    st.markdown("""
    This page showcases a map of Citi Bike trips across New York City, highlighting popular routes, start stations, and end stations.
    """)
    map_image_path = "citibike_map.png"
    st.image(map_image_path, caption="Citi Bike Trips Map", width=1200)
    
    # Add Insights Section
    st.markdown("""
    ### Insights from the Map:
    - **High Activity in Manhattan**: The map shows a dense concentration of trips in and around Manhattan, particularly near key hubs like Midtown and Lower Manhattan.
    - **Key Routes and Patterns**:
        - Popular routes tend to connect business districts, residential areas, and tourist destinations.
        - Waterfront areas and parks also see significant activity.
    - **Geographic Coverage**:
        - While Manhattan dominates usage, there is notable activity extending into Jersey City and parts of Brooklyn.
    """)

# RECOMMENDATIONS Page
if page == "Recommendations":
    st.markdown(
        """
        <div style="text-align: center;">
            <h2 style="font-size: 24px; font-weight: bold;">Recommendations to Optimize Citi Bike Operations</h2>
            <p style="font-size: 16px; font-weight: bold;">
                Based on the analysis of Citi Bike usage patterns, weather influence, and station popularity, 
                the following strategies to address supply issues and optimize operations would be recommended:
            </p>
            <hr style="border: 1px solid #ddd;">
        </div>
        """,
        unsafe_allow_html=True
    )

    ## Section 1: Address Seasonal Demand Variations
    st.markdown("### Address Seasonal Demand Variations")
    st.markdown("""
    **Analysis Insight**: Warmer months (May to September) have peak bike usage, with daily trips exceeding 100,000, 
    while colder months see significantly lower demand (below 40,000 trips).
    """)
    st.markdown("""
    **Recommendation**:
    - Focus on balancing bike distribution during peak summer months to avoid shortages at high-demand stations.
    - Reduce bike inventory or reallocate resources during colder months when demand is lower.
    """)

    # Add horizontal divider
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    ## Section 2: Optimize Operations at High-Demand Stations
    st.markdown("### Optimize Operations at High-Demand Stations")
    st.markdown("""
    **Analysis Insight**: The top 20 stations, such as **W 21 St & 6 Ave** and **West St & Chambers St**, 
    account for a significant proportion of total trips.
    """)
    st.markdown("""
    **Recommendation**:
    - Increase bike docks and inventory at these high-demand stations to reduce shortages.
    - Implement dynamic rebalancing strategies to move bikes from underutilized stations to busy ones.
    """)

    # Add horizontal divider
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    ## Section 3: Expand and Diversify Geographic Coverage
    st.markdown("### Expand and Diversify Geographic Coverage")
    st.markdown("""
    **Analysis Insight**: Most trips are concentrated in Manhattan, with notable activity in Jersey City and parts of Brooklyn.
    """)
    st.markdown("""
    **Recommendation**:
    - Expand station coverage to underserved areas like Queens, the Bronx, and outer Brooklyn to increase ridership.
    - Use geospatial analysis to identify potential new station locations based on residential and business density.
    """)

    # Add horizontal divider
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    ## Section 4: Leverage Weather Data
    st.markdown("### Leverage Weather Data")
    st.markdown("""
    **Analysis Insight**: Temperature has a clear correlation with ridership, with lower temperatures leading to reduced bike usage.
    """)
    st.markdown("""
    **Recommendation**:
    - Use weather forecasts to dynamically adjust bike allocations and staffing levels in anticipation of demand changes.
    - Promote indoor biking options or partnerships with gyms during winter months.
    """)

    # Add horizontal divider
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    ## Footer and Call-to-Action
    st.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 18px;">
        By implementing these recommendations, Citi Bike can address supply-demand challenges, 
        enhance user satisfaction, and streamline operations for future growth. 🚲
    </div>
    """, unsafe_allow_html=True)

