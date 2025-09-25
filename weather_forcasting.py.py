# === Required Libraries ===
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# === API Setup ===
API_KEY = "1dfa7b8fde83db183e5b13b616b7e5a7"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# === Kelvin to Celsius Conversion ===
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# === Construction Advice Based on Weather Conditions ===
def construction_advice(temp_c, condition, wind_speed, rain):
    advice = []
    if rain > 30:
        advice.append("Heavy rain expected. Concrete pouring may be delayed.")
    if temp_c < 5:
        advice.append("Temperature is too low for proper curing of concrete.")
    if temp_c > 35:
        advice.append("High temperature may lead to rapid moisture loss from concrete.")
    if wind_speed > 10:
        advice.append("Strong winds could make crane operations risky.")
    if "snow" in condition.lower():
        advice.append("Snowfall could halt outdoor construction activities.")
    if not advice:
        advice.append("Weather is suitable for most construction activities.")
    return advice

# === Plot Temperature, Wind Speed, Rain ===
def plot_weather_data(dates, temps, wind_speeds, rains):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)', color='tab:blue')
    ax1.plot(dates, temps, color='tab:blue', marker="o")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Wind Speed (m/s)', color='tab:green')
    ax2.plot(dates, wind_speeds, color='tab:green', linestyle='dashed', marker="s")
    ax2.tick_params(axis='y', labelcolor='tab:green')

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('Rain (mm)', color='tab:red')
    ax3.plot(dates, rains, color='tab:red', linestyle='dotted', marker="^")
    ax3.tick_params(axis='y', labelcolor='tab:red')

    fig.tight_layout()
    plt.title('Weather Forecast for Next 5 Days')
    return fig

# === Fetch Weather and Display in GUI ===
def get_weather_forecast(city):
    params = {'q': city, 'appid': API_KEY}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        messagebox.showerror("Error", f"Error: {data.get('message', 'Failed to fetch data')}")
        return

    result_text_content = f"Weather Forecast + Civil Engineering Advice for {city.title()}:\n\n"
    dates, temps, wind_speeds, rains = [], [], [], []

    for i in range(0, 40, 8):
        forecast = data['list'][i]
        dt = datetime.datetime.fromtimestamp(forecast['dt'])
        temp_c = kelvin_to_celsius(forecast['main']['temp'])
        condition = forecast['weather'][0]['description']
        wind_speed = forecast['wind']['speed']
        rain = forecast.get('rain', {}).get('3h', 0)

        result_text_content += f"{dt.strftime('%a %d %b %I:%M %p')}\n"
        result_text_content += f"  Temp: {temp_c:.1f}°C | Condition: {condition.title()} | Wind: {wind_speed} m/s | Rain: {rain} mm\n"

        for tip in construction_advice(temp_c, condition, wind_speed, rain):
            result_text_content += f"   - {tip}\n"

        result_text_content += "\n---\n"

        dates.append(dt.strftime('%a %d %b'))
        temps.append(temp_c)
        wind_speeds.append(wind_speed)
        rains.append(rain)

    # Clear and insert new text
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result_text_content)

    # Clear old plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Generate and display new plot
    fig = plot_weather_data(dates, temps, wind_speeds, rains)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# === GUI Setup ===
window = tk.Tk()
window.title("Weather Forecast & Civil Engineering Advice")
window.geometry("950x850")

# === Background Image Auto-Detect ===
folder_path = r"C:\Users\admin\OneDrive\Documents\python\New folder"
print("Files in folder:", os.listdir(folder_path))

bg_photo = None
for file in os.listdir(folder_path):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        full_path = os.path.join(folder_path, file)
        print(f"✅ Using background: {file}")
        bg_image = Image.open(full_path)
        bg_image = bg_image.resize((950, 850), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        break

if bg_photo:
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    print("⚠️ No image found in the folder!")

# === Header ===
header = tk.Label(window, text="🌤️ Weather & Construction Advice App",
                  font=("Helvetica", 22, "bold"),
                  bg="#ffffff", fg="#333")
header.place(relx=0.5, y=20, anchor="n")

# === Input Section ===
input_frame = tk.Frame(window, bg="#ffffff")
input_frame.place(relx=0.5, rely=0.1, anchor="n")

city_label = tk.Label(input_frame, text="Enter City Name:",
                      font=("Arial", 14), bg="#ffffff")
city_label.pack(side=tk.LEFT, padx=5)

city_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
city_entry.pack(side=tk.LEFT, padx=5)

get_weather_button = tk.Button(input_frame, text="Get Forecast",
                               font=("Arial", 12, "bold"),
                               bg="#007acc", fg="white",
                               command=lambda: get_weather_forecast(city_entry.get()))
get_weather_button.pack(side=tk.LEFT, padx=10)

# === Result Section with Scrollbar ===
result_frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove")
result_frame.place(relx=0.5, rely=0.22, anchor="n")

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, wrap="word", yscrollcommand=scrollbar.set,
                      width=100, height=18, font=("Arial", 10),
                      bg="#ffffff", padx=10, pady=10)
result_text.pack()

scrollbar.config(command=result_text.yview)

# === Plot Section ===
plot_frame = tk.Frame(window, bg="#ffffff", bd=2, relief="groove")
plot_frame.place(relx=0.5, rely=0.78, anchor="center")

# === Run App ===
window.mainloop()








