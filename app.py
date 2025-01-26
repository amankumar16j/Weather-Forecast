import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
from PIL import Image
import streamlit_shadcn_ui as ui
import cv2
import numpy as np

import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import requests
import altair as alt
from datetime import datetime
import joblib
from streamlit_lottie import st_lottie
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval, get_geolocation


st.set_page_config(layout="wide")

# loc = get_geolocation()

# lat=loc['coords']['latitude']
# lon=loc['coords']['longitude']


api_key = "75f5259e5f36234789875b400c78db3b"

def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 

def get_lat_lon(city_name, api_key):
    base_url = "http://api.positionstack.com/v1/forward"
    params = {
        'access_key': api_key,
        'query': city_name,
        'limit': 1
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            lat = data['data'][0]['latitude']
            lon = data['data'][0]['longitude']
            return lat, lon
        else:
            return None, None
    else:
        return None, None
    
    
# Function to get weather data using Open-Meteo
def get_weather_data(lat, lon, days):
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for current weather and extended forecast (including wind, humidity, precipitation chance)
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'daily': 'temperature_2m_max,temperature_2m_min,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,precipitation_probability_max',
        'forecast_days': days,
        'timezone': 'auto'
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


city = "Jalandhar"

col3=st.columns([1,4])
with col3[0]:
    link="https://lottie.host/19e17113-27e0-4939-8b89-dc3eee2aa043/Ad83vzKx1U.json"
    l=load_lottieurl(link)
    st.lottie(l,height=130,width=300)
with col3[1]:
    st.markdown("""
                <h1 style='font-size: 60px;'>
                    Weather Forecast
                </h1>
                <hr style='border: 2px solid white;'>
                
                """, unsafe_allow_html=True)
with st.container(border=True):
    
    label="City Name"
    options=["Your Location","Jalandhar","Bhopal","Indore","Delhi","Uttar Pradesh","Tamil Nadu"]
    city = st.selectbox(label, options, index=0, key=None, help=None, on_change=None, args=None, kwargs=None)

    st.header(city)    
    cols = st.columns([5,5,5,5])
    
    # Display current weather
    # Load data according to city info----------------------------
    days = 7
    # city = "Jalandhar"
    if(city=="Your Location"):
        loc = get_geolocation()
        lat=1
        lon=1

        if loc is not None and 'coords' in loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
        else:
            st.error("Geolocation data could not be retrieved. Please Give Access To Your Location Or Try Using Option Menu")
    else:
        lat, lon = get_lat_lon(city, api_key)
        
    if lat is not None and lon is not None:
        pass
    else:
        st.error("City not found, please try again.")
    
    weather_data=get_weather_data(lat, lon, days)
    current_weather = weather_data['current_weather']
    forecast = weather_data['daily']
    minhumi=forecast['relative_humidity_2m_max'][0]
    maxhumi=forecast['relative_humidity_2m_min'][0]
    humi=(minhumi+maxhumi)/2
    precipitation=forecast['precipitation_probability_max'][0]
    with cols[0]:
    
        with st.container(border=True):
            
            now = datetime.now().time()
            # Define the time range for night
            night_start = datetime.strptime("19:00", "%H:%M").time()  # 7 PM
            night_end = datetime.strptime("04:00", "%H:%M").time()  # 4 AM

            # Check if current time is between 7 PM and 4 AM
                            
            sunny="https://lottie.host/7e2f4c85-e3d3-43b6-8a83-aba769f3c0f4/TAjpsqh5ea.json"
            sunny1="https://lottie.host/826c55af-51f7-4f92-9de0-320ee3f39f54/NtAdsdf1Ml.json"
            moon="https://lottie.host/a9a04a62-56f5-4a70-a87f-217f601a270f/d6YUp2fpYO.json"
            
            if now >= night_start or now < night_end:
                sunny_lottie=load_lottieurl(moon)    
            elif current_weather["temperature"]>35:
                sunny_lottie=load_lottieurl(sunny)
            else:
                sunny_lottie=load_lottieurl(sunny1)
                
            
            # sunny_lottie=load_lottieurl(sunny1)
                
            st.lottie(sunny_lottie,height=100,width=100)
            ui.metric_card(title="Temperature", content=str(current_weather["temperature"])+" in (c)", key="card1")
    
    with cols[1]:
            with st.container(border=True):
                windy="https://lottie.host/9462ba5b-410e-4fc4-be63-f8ebd13d3985/HnDwx1zv2P.json"
                windy_lottie=load_lottieurl(windy)
                st.lottie(windy_lottie,height=100,width=100)
                ui.metric_card(title="Wind Speed", content=str(current_weather["windspeed"])+" in (KMPH)", key="card2")

    with cols[2]:
        with st.container(border=True):
            humid="https://lottie.host/338a286f-a5b6-4f15-bf33-919241525814/LZLBGuC375.json"
            humid_lottie=load_lottieurl(humid)
            st.lottie(humid_lottie,height=100,width=100)
            ui.metric_card(title="Humidity", content=str(humi)+" in (%)", key="card3")

    with cols[3]:
        with st.container(border=True):
            rainy="https://lottie.host/17db9346-022a-4102-8867-b3e511fa8379/rmgkKnkL97.json"
            rainy_lottie=load_lottieurl(rainy)
            st.lottie(rainy_lottie,height=100,width=100)
            ui.metric_card(title="Precipitation", content=str(precipitation)+" in (%)", key="card4")


with st.container(border=True):
    
    # Load data according to city info----------------------------

    if weather_data:
        days = st.slider(
        label="Select a number",
        min_value=2,
        max_value=20,
        value=10,  # Default value
        step=1  # Step size
        )
        
        # lat, lon = get_lat_lon(city, api_key)
        if lat is not None and lon is not None: 
            pass
        else:
            st.error("City not found, please try again.")
        weather_data = get_weather_data(lat, lon, days)
        # Display forecast
        st.header(f"{days}-Day Forecast")
        forecast = weather_data['daily']
        
            
        data = {
        'Date': forecast['time'],  
        'Max_temp(°C)': forecast['temperature_2m_max'],
        'Min_temp(°C)': forecast['temperature_2m_min'],
        'Max Humidity (%)': forecast['relative_humidity_2m_max'],
        'Min Humidity (%)': forecast['relative_humidity_2m_min'],
        'Precpitation(%)': forecast['precipitation_probability_max']
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Streamlit Title
        # st.title("7-Day Weather Forecast")
        
        cols=st.columns([1.2,1])
        
        with cols[0]:

        # 1. Max and Min Temperature Line Chart
            temp_chart = alt.Chart(df).transform_fold(
            ['Max_temp(°C)', 'Min_temp(°C)'],
            as_=['Temperature Type', 'Temperature']
            ).mark_line(strokeWidth=3).encode(
            x=alt.X('Date:T', timeUnit='date'),
            y='Temperature:Q',
            color='Temperature Type:N',
            tooltip=[alt.Tooltip('Date:T', title='Date'),
                    alt.Tooltip('Temperature:Q', title='Temperature (°C)'),
                    alt.Tooltip('Temperature Type:N', title='Type')]
            ).properties(
                title='Max and Min Temperature Over Time',
                width=600,
                height=400
            )

            # Adding points (dots) on each data point
            points = alt.Chart(df).transform_fold(
                ['Max_temp(°C)', 'Min_temp(°C)'],
                as_=['Temperature Type', 'Temperature']
            ).mark_point(size=100).encode(  # Increase size for bigger dots
                x=alt.X('Date:T', timeUnit='date'),
                y='Temperature:Q',
                color='Temperature Type:N',
                tooltip=[alt.Tooltip('Date:T', title='Date'),
                        alt.Tooltip('Temperature:Q', title='Temperature (°C)'),
                        alt.Tooltip('Temperature Type:N', title='Type')]
            )

        # Layering the line chart with the points chart
            final_chart = temp_chart + points

            st.altair_chart(final_chart, use_container_width=True)


    with cols[1]:
    
    # 3. Precipitation Probability Line Chart
        precip_chart = alt.Chart(df).mark_line(strokeWidth=3).encode(
            x=alt.X('Date:T',timeUnit="date"),
            y=alt.Y('Precpitation(%):Q', title='Precipitation Probability (%)'),
            
            tooltip=[alt.Tooltip('Date:T', title='Date'),
                alt.Tooltip('Precpitation(%):Q',title='Precipatation(%)')]
        ).properties(
            title='Precipitation Probability Over Time',
            width=600,
            height=400
        )

        points1 = alt.Chart(df).mark_point(size=100).encode(  # Increase size for bigger dots
            x=alt.X('Date:T', timeUnit='date'),
            y=alt.Y('Precpitation(%):Q',title='Precipitation Probability (%)'),
            
            tooltip=[alt.Tooltip('Date:T', title='Date'),
                alt.Tooltip('Precpitation(%):Q',title='Precipatation(%)')]
        )
        finalchart1=precip_chart+points1
        st.altair_chart(finalchart1, use_container_width=True)
