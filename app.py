import streamlit as st
import datetime
import random
import matplotlib.pyplot as plt

# Title
st.title("Civil Engineering Weather Advisor 🌦️")
st.write("Get weather forecasts and construction advice for your projects.")

# Input
city = st.text_input("Enter city name:", "Risalpur")
date = st.date_input("Select date:", datetime.date.today())

# Mock weather data (replace with API later)
temperature = random.randint(20, 40)  # Celsius
rain_chance = random.randint(0, 100)  # Percentage
wind_speed = random.randint(0, 50)    # km/h

st.subheader(f"Weather Forecast for {city} on {date}")
st.write(f"🌡 Temperature: {temperature} °C")
st.write(f"🌧 Chance of Rain: {rain_chance} %")
st.write(f"💨 Wind Speed: {wind_speed} km/h")

# Construction recommendations
st.subheader("Construction Advice:")
if rain_chance > 50:
    st.warning("High chance of rain. Avoid concrete pouring and earthworks.")
else:
    st.success("Weather looks good. You can proceed with outdoor construction.")

if temperature > 35:
    st.info("High temperature: Ensure hydration for workers and check material curing times.")
elif temperature < 15:
    st.info("Low temperature: Check for frost-sensitive materials.")

if wind_speed > 30:
    st.warning("Strong winds: Avoid working with cranes or tall structures.")

# Simple graph
st.subheader("Temperature Trend (Mock Data)")
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
temps = [random.randint(20, 40) for _ in range(5)]
plt.plot(days, temps, marker='o')
plt.xlabel("Days")
plt.ylabel("Temperature (°C)")
st.pyplot(plt)
