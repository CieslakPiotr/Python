import requests
from tkinter import *
from tkinter import ttk

def chosen_city():
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        61: "Light rain",
        71: "Light snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }

    city_coordinates = {
        "Warszawa": (52.22, 21.01),
        "London": (51.50, -0.12),
        "Paris": (48.85, 2.35),
        "Berlin": (52.52, 13.40)
    }

    selected = dropdown_cities.get()
    if selected not in city_coordinates:
        result_label.config(text="Please select a valid city.")
        return

    latitude, longitude = city_coordinates[selected]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = data['current_weather']
        description = weather_codes.get(weather['weathercode'], "Unknown")
        result = f"Weather: {description}\nTemperature: {weather['temperature']}°C\nWindspeed: {weather['windspeed']} km/h"
        result_label.config(text=result)
    else:
        result_label.config(text="Failed to retrieve weather data.")


window = Tk()
window.title("Weather App")
window.geometry("225x300")

typeLabel = Label(text="Choose city:")
typeLabel.grid(row=0, column=1)
city = ["Warszawa", "London", "Paris", "Berlin"]
dropdown_cities = ttk.Combobox(window, values=city)
dropdown_cities.grid(row=1, column=1, padx=10)

search_city = Button(text="View Weather", command=chosen_city)
search_city.grid(row=2, column=1)

result_label = Label(window, text="", font=("Arial", 12))
result_label.grid(row=3, column=1)

window.mainloop()