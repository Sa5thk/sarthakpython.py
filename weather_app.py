import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Weather App")

        self.cities = ["Mumbai", "New Delhi", "Pune", "Jalgaon", "Nashik"]
        self.selected_city = tk.StringVar(value=self.cities[0])

        self.city_label = ttk.Label(root, text="Select City:")
        self.city_combobox = ttk.Combobox(root, values=self.cities, textvariable=self.selected_city)
        self.get_weather_button = ttk.Button(root, text="Get Weather", command=self.get_weather)

        self.weather_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        self.weather_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.temperature_label = ttk.Label(self.weather_frame, text="Temperature:")
        self.humidity_label = ttk.Label(self.weather_frame, text="Humidity:")
        self.weather_icon_label = ttk.Label(self.weather_frame)

        self.city_label.grid(row=0, column=0, padx=5, pady=5)
        self.city_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.get_weather_button.grid(row=0, column=2, padx=5, pady=5)

        self.temperature_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.humidity_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.weather_icon_label.grid(row=0, column=1, rowspan=2, padx=5, pady=5)

    def get_weather(self):
        city = self.selected_city.get()
        api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}

        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                icon_code = data["weather"][0]["icon"]

                self.temperature_label.config(text=f"Temperature: {temperature}°C")
                self.humidity_label.config(text=f"Humidity: {humidity}%")
                self.display_weather_icon(icon_code)
            else:
                messagebox.showerror("Error", f"Failed to get weather data. {data['message']}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_weather_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
        image = Image.open(requests.get(icon_url, stream=True).raw)
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        self.weather_icon_label.config(image=photo)
        self.weather_icon_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

