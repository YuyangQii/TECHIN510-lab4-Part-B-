import streamlit as st
import requests
import pandas as pd

def get_coordinates(location):
    """Use the OpenStreetMap API to get latitude and longitude for a location."""
    params = {'q': location, 'format': 'json'}
    response = requests.get("https://nominatim.openstreetmap.org/search", params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon'], data[0]['display_name']
    else:
        return None, None, None

def get_weather(lat, lon):
    """Use the Weather.gov API to get the weather forecast for given latitude and longitude."""
    point_url = f"https://api.weather.gov/points/{lat},{lon}"
    point_response = requests.get(point_url)
    if point_response.status_code == 200:
        point_data = point_response.json()
        forecast_url = point_data['properties']['forecast']
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        return forecast_data['properties']['periods']
    else:
        return None

st.title('⛅️ Weather Lookup App')

location = st.text_input("Enter a location name:", help="Type the name of a city or place and press enter.")
if location:
    with st.spinner('Fetching coordinates...'):
        lat, lon, display_name = get_coordinates(location)
    
    if lat and lon:
        with st.spinner(f'Fetching weather data for {display_name}...'):
            weather_data = get_weather(lat, lon)
        
        if weather_data:
            st.success(f"Weather forecast for {display_name}:")
            map_data = pd.DataFrame({'lat': [float(lat)], 'lon': [float(lon)]})
            st.map(map_data)

            for period in weather_data:
                st.subheader(period['name'])
                st.write(f"Temperature: {period['temperature']}°{period['temperatureUnit']}")
                st.write(f"Forecast: {period['detailedForecast']}")
                if 'icon' in period:
                    st.image(period['icon'], width=100)
        else:
            st.error("Could not retrieve weather data. Please check your location input or try again later.")
    else:
        st.error("Could not find coordinates for the given location. Please enter a valid location.")
