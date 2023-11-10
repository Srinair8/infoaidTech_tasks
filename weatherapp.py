import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

API_KEY = "53b23de63e52ca15c05b120727159487"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x500")
        self.root.configure(bg="#c9daf8")

        self.city_label = tk.Label(root, text="Enter a city:", font=("Helvetica", 16), bg="#3498db", fg="white")
        self.city_label.pack(pady=10)

        self.city_entry = tk.Entry(root, font=("Helvetica", 14))
        self.city_entry.pack()

        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.get_weather, font=("Helvetica", 12), bg="#2ecc71", fg="white")
        self.get_weather_button.pack(pady=10)

        self.weather_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#3498db", fg="white")
        self.weather_label.pack()

        #recommendattions widget
        self.recommendations_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=6, font=("Helvetica", 12))
        self.recommendations_text.pack(pady=10)

        self.forecast_button = tk.Button(root, text="View Forecast", command=self.view_forecast, font=("Helvetica", 12), bg="#e67e22", fg="white")
        self.forecast_button.pack(pady=10)

        self.save_favorite_button = tk.Button(root, text="Save Favorite", command=self.save_favorite, font=("Helvetica", 12), bg="#3498db", fg="white")
        self.save_favorite_button.pack(pady=10)

        self.view_favorites_button = tk.Button(root, text="View Favorites", command=self.view_favorites, font=("Helvetica", 12), bg="#9b59b6", fg="white")
        self.view_favorites_button.pack(pady=10)

        self.favorite_locations = self.load_favorite_locations()

    def get_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showinfo("Error", "Please enter a city.")
            return

        data = self.get_weather_data(city)
        self.display_current_weather(data)

    def get_weather_data(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data

    def display_current_weather(self, data):
        if data["cod"] == "404":
            self.weather_label.config(text="City not found. Please try again.")
        else:
            main_info = data["main"]
            weather_info = data["weather"][0]
            wind_info = data["wind"]

            weather_text = f"Weather in {data['name']}, {data['sys']['country']}:\n"
            weather_text += f"Condition: {weather_info['description']}\n"
            weather_text += f"Temperature: {main_info['temp']}°C\n"
            weather_text += f"Humidity: {main_info['humidity']}%\n"
            weather_text += f"Wind Speed: {wind_info['speed']} m/s"

            self.weather_label.config(text=weather_text)

            # Recommendations
            recommendations = self.get_recommendations(weather_info['main'])
            self.recommendations_text.delete(1.0, tk.END)  # Clear the previous recommendations
            self.recommendations_text.insert(tk.INSERT, f"Recommendations: {recommendations}")

    def view_forecast(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showinfo("Error", "Please enter a city.")
            return

        forecast_data = self.get_forecast_data(city)
        self.display_forecast(forecast_data)

    def get_forecast_data(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(FORECAST_URL, params=params)
        data = response.json()
        return data

    def display_forecast(self, data):
        if data["cod"] == "404":
            messagebox.showinfo("Error", "City not found. Please try again.")
        else:
            forecast_text = f"5-Day Forecast for {data['city']['name']}, {data['city']['country']}:\n\n"
            for entry in data['list']:
                date_time = entry['dt_txt']
                temperature = entry['main']['temp']
                condition = entry['weather'][0]['description']

                forecast_text += f"{date_time}: {temperature}°C, {condition}\n"

            messagebox.showinfo("Forecast", forecast_text)

    def save_favorite(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showinfo("Error", "Please enter a city.")
            return

        self.favorite_locations.add(city)
        self.save_favorite_locations()

        messagebox.showinfo("Success", f"{city} added to favorites!")

    def load_favorite_locations(self):
        try:
            with open("favorites.txt", "r") as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            return set()

    def save_favorite_locations(self):
        with open("favorites.txt", "w") as file:
            file.write("\n".join(self.favorite_locations))

    def view_favorites(self):
        if not self.favorite_locations:
            messagebox.showinfo("Info", "You have no favorite locations.")
            return

        favorites_text = "Weather in Favorite Locations:\n\n"
        for location in self.favorite_locations:
            data = self.get_weather_data(location)
            if data["cod"] == "404":
                favorites_text += f"{location}: City not found.\n"
            else:
                main_info = data["main"]
                weather_info = data["weather"][0]
                wind_info = data["wind"]

                favorites_text += f"{location} - {data['sys']['country']}:\n"
                favorites_text += f"Condition: {weather_info['description']}\n"
                favorites_text += f"Temperature: {main_info['temp']}°C\n"
                favorites_text += f"Humidity: {main_info['humidity']}%\n"
                favorites_text += f"Wind Speed: {wind_info['speed']} m/s\n\n"

        messagebox.showinfo("Favorites", favorites_text)

    def get_recommendations(self, weather_condition):
        if weather_condition.lower() == 'clear':
            return "It's a clear day! Enjoy the sunshine."
        elif weather_condition.lower() == 'clouds':
            return "It's a bit cloudy. Consider bringing an umbrella."
        elif weather_condition.lower() == 'rain':
            return "It's raining. Don't forget your umbrella!"
        elif weather_condition.lower() == 'snow':
            return "It's snowing. Bundle up and stay warm."
        else:
            return "Check the weather for more information."

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
