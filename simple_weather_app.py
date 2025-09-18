
import tkinter as tk
from tkinter import messagebox
import requests
import json

class SimpleWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Weather App")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')

        # Replace with your OpenWeatherMap API key
        self.api_key = "your_api_key_here"

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🌤️ Weather App", 
                              font=("Arial", 20, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter City Name:", 
                font=("Arial", 12), bg='#f0f0f0').pack()

        self.city_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.city_entry.pack(pady=5)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())

        # Search button
        search_btn = tk.Button(input_frame, text="Get Weather", 
                              command=self.get_weather,
                              font=("Arial", 12), bg='#4CAF50', fg='white',
                              padx=20, pady=5)
        search_btn.pack(pady=10)

        # Weather display frame
        self.weather_frame = tk.Frame(self.root, bg='#ffffff', 
                                     relief=tk.RAISED, bd=2)
        self.weather_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Weather info labels
        self.city_label = tk.Label(self.weather_frame, text="", 
                                  font=("Arial", 16, "bold"), 
                                  bg='#ffffff', fg='#333')
        self.city_label.pack(pady=10)

        self.temp_label = tk.Label(self.weather_frame, text="", 
                                  font=("Arial", 32, "bold"), 
                                  bg='#ffffff', fg='#e74c3c')
        self.temp_label.pack(pady=10)

        self.desc_label = tk.Label(self.weather_frame, text="", 
                                  font=("Arial", 12), 
                                  bg='#ffffff', fg='#666')
        self.desc_label.pack(pady=5)

        self.feels_like_label = tk.Label(self.weather_frame, text="", 
                                        font=("Arial", 11), 
                                        bg='#ffffff', fg='#666')
        self.feels_like_label.pack(pady=5)

        self.humidity_label = tk.Label(self.weather_frame, text="", 
                                      font=("Arial", 11), 
                                      bg='#ffffff', fg='#666')
        self.humidity_label.pack(pady=5)

        self.wind_label = tk.Label(self.weather_frame, text="", 
                                  font=("Arial", 11), 
                                  bg='#ffffff', fg='#666')
        self.wind_label.pack(pady=5)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return

        try:
            # API parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }

            # Make API request
            url = "http://api.openweathermap.org/data/2.5/weather"
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                self.display_weather(data)
            else:
                error_data = response.json()
                messagebox.showerror("Error", f"City not found: {error_data.get('message', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_weather(self, data):
        # Extract weather information
        city = data['name']
        country = data['sys']['country']
        temp = int(data['main']['temp'])
        feels_like = int(data['main']['feels_like'])
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']

        # Update labels
        self.city_label.config(text=f"{city}, {country}")
        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=description)
        self.feels_like_label.config(text=f"Feels like: {feels_like}°C")
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        self.wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleWeatherApp(root)
    root.mainloop()
