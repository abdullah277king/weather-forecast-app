import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
API_KEY = "7e726012e7affd5fedef1cffeb3cda8c"  # your real API key

st.title("Civil Engineering Weather Advisor 🌦️")
st.write("Get live weather forecasts and construction advice for your projects.")

# ---------- USER INPUT ----------
city_input = st.text_input("Enter City Name (e.g., Islamabad, London, Paris):")

if city_input:
    city = city_input.strip()

    # ---------- CURRENT WEATHER ----------
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"

    try:
        current_resp = requests.get(current_url).json()
        forecast_resp = requests.get(forecast_url).json()

        # ----- Handle API errors -----
        if current_resp.get("cod") != 200:
            st.error(f"❌ {current_resp.get('message', 'Error fetching current weather')}")
        elif forecast_resp.get("cod") != "200":
            st.error(f"❌ {forecast_resp.get('message', 'Error fetching forecast')}")
        else:
            # ---------- DISPLAY CURRENT WEATHER ----------
            st.subheader(f"Current Weather for {current_resp['name']} on {datetime.now().strftime('%Y-%m-%d')}")
            st.write(f"🌡 Temperature: {current_resp['main']['temp']} °C")
            st.write(f"💨 Wind Speed: {current_resp['wind']['speed']} m/s")
            st.write(f"🌧 Rain (last hour): {current_resp.get('rain', {}).get('1h', 0)} mm")
            st.write(f"🌤 Condition: {current_resp['weather'][0]['description']}")

            # ---------- FORECAST GRAPHS ----------
            dates = []
            temps = []
            wind_speeds = []
            rain_mm = []

            for item in forecast_resp['list']:
                dt = datetime.fromtimestamp(item['dt'])
                dates.append(dt)
                temps.append(item['main']['temp'])
                wind_speeds.append(item['wind']['speed'])
                rain_mm.append(item.get('rain', {}).get('3h', 0))

            # Temperature graph
            fig, ax = plt.subplots()
            ax.plot(dates, temps, marker='o', color='orange')
            ax.set_title("Temperature (°C) Forecast")
            ax.set_xlabel("Date-Time")
            ax.set_ylabel("Temperature °C")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Wind speed graph
            fig2, ax2 = plt.subplots()
            ax2.plot(dates, wind_speeds, marker='o', color='blue')
            ax2.set_title("Wind Speed (m/s) Forecast")
            ax2.set_xlabel("Date-Time")
            ax2.set_ylabel("Wind Speed m/s")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

            # Rain graph
            fig3, ax3 = plt.subplots()
            ax3.bar(dates, rain_mm, color='green')
            ax3.set_title("Rainfall (mm) Forecast")
            ax3.set_xlabel("Date-Time")
            ax3.set_ylabel("Rainfall mm")
            plt.xticks(rotation=45)
            st.pyplot(fig3)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network/API error: {e}")
















