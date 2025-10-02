import streamlit as st
import requests
import datetime

st.title("Civil Engineering Weather Advisor 🌦️")
st.write("Get live weather forecasts and construction advice for your projects.")

# --- Inputs ---
st.sidebar.header("Weather Input")
city = st.sidebar.text_input("Enter city name:", "Risalpur")
date = st.sidebar.date_input("Select date:", datetime.date.today())

# --- API Key ---
API_KEY = "YOUR_REAL_API_KEY_HERE"  # <-- Replace with your actual OpenWeather API key

# --- Geocoding to get lat/lon ---
def get_lat_lon(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data['lat'], data['lon']
    return None, None

lat, lon = get_lat_lon(city)

if lat is None or lon is None:
    st.error("City not found. Please enter a valid city name.")
else:
    # --- Fetch weather data ---
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        rain = data.get("rain", {}).get("1h", 0)
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"].capitalize()

        st.subheader(f"Weather Forecast for {city} on {date}")
        st.write(f"🌡 Temperature: {temperature} °C")
        st.write(f"🌧 Rain (last hour): {rain} mm")
        st.write(f"💨 Wind Speed: {wind_speed} m/s")
        st.write(f"🌤 Condition: {weather_desc}")

        st.subheader("Construction Advice:")
        if rain > 2:
            st.warning("High rainfall detected. Avoid concrete pouring and earthworks.")
        else:
            st.success("Weather looks good. You can proceed with outdoor construction.")

        if temperature > 35:
            st.info("High temperature: Ensure worker hydration and check material curing times.")
        elif temperature < 10:
            st.info("Low temperature: Protect frost-sensitive materials.")

        if wind_speed > 10:
            st.warning("Strong winds: Avoid crane operations and work on tall structures.")
    else:
        st.error("⚠️ Could not fetch weather data. Please check your API key.")












