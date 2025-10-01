import streamlit as st
import datetime
import requests
import matplotlib.pyplot as plt

# -------------------------------
# CONFIG
# -------------------------------
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/"

# -------------------------------
# FUNCTIONS
# -------------------------------
def get_weather(city):
    """Fetch current weather data for a city"""
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast(city):
    """Fetch 5-day / 3-hour forecast data for plotting"""
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# -------------------------------
# STREAMLIT APP
# -------------------------------
st.title("Civil Engineering Weather Advisor 🌦️")
st.write("Get **real weather forecasts** and **construction advice** for your projects.")

# Input
city = st.text_input("Enter city name:", "Risalpur")
date = st.date_input("Select date:", datetime.date.today())

if city:
    weather_data = get_weather(city)

    if weather_data:
        # Extract weather details
        temperature = weather_data["main"]["temp"]
        rain = weather_data.get("rain", {}).get("1h", 0)  # Rain in last 1h (mm)
        wind_speed = weather_data["wind"]["speed"]
        condition = weather_data["weather"][0]["description"].title()

        # Display forecast
        st.subheader(f"Weather Forecast for {city} on {date}")
        st.write(f"🌡 Temperature: {temperature} °C")
        st.write(f"🌧 Rain (last 1h): {rain} mm")
        st.write(f"💨 Wind Speed: {wind_speed} m/s")
        st.write(f"☁ Condition: {condition}")

        # Construction recommendations
        st.subheader("Construction Advice:")
        if rain > 2:
            st.warning("Heavy rain: Avoid concrete pouring and earthworks.")
        elif rain > 0:
            st.info("Light rain: Proceed with caution, check soil conditions.")
        else:
            st.success("No rain detected. You can proceed with outdoor construction.")

        if temperature > 35:
            st.info("High temperature: Ensure hydration for workers and check curing times.")
        elif temperature < 15:
            st.info("Low temperature: Check frost-sensitive materials.")

        if wind_speed > 10:
            st.warning("Strong winds: Avoid cranes or working on tall structures.")

        # Forecast trend chart
        st.subheader("5-Day Temperature Trend")
        forecast_data = get_forecast(city)

        if forecast_data:
            times = [item["dt_txt"] for item in forecast_data["list"][:8]]
            temps = [item["main"]["temp"] for item in forecast_data["list"][:8]]

            plt.figure(figsize=(8, 4))
            plt.plot(times, temps, marker='o')
            plt.xticks(rotation=45, ha="right")
            plt.xlabel("Time")
            plt.ylabel("Temperature (°C)")
            plt.title("Next 24h Temperature Trend")
            plt.tight_layout()
            st.pyplot(plt)

    else:
        st.error("City not found. Please enter a valid city name.")

