
import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import json
from datetime import datetime
import threading
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Weather App")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # API key - Replace with your own OpenWeatherMap API key
        self.api_key = "your_api_key_here"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(main_frame, text="🌤️ Weather Dashboard", 
                              font=title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=(0, 20))

        # Search frame
        search_frame = tk.Frame(main_frame, bg='#2c3e50')
        search_frame.pack(fill=tk.X, pady=(0, 20))

        # City entry
        self.city_var = tk.StringVar()
        city_label = tk.Label(search_frame, text="Enter City:", 
                             font=("Arial", 12), bg='#2c3e50', fg='#ecf0f1')
        city_label.pack(side=tk.LEFT, padx=(0, 10))

        self.city_entry = tk.Entry(search_frame, textvariable=self.city_var, 
                                  font=("Arial", 12), width=25, relief=tk.FLAT, 
                                  bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1')
        self.city_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())

        # Search button
        search_btn = tk.Button(search_frame, text="🔍 Search", command=self.get_weather,
                              bg='#3498db', fg='white', font=("Arial", 11, "bold"),
                              relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        search_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Current location button
        current_btn = tk.Button(search_frame, text="📍 Current Location", 
                               command=self.get_current_location_weather,
                               bg='#e74c3c', fg='white', font=("Arial", 11, "bold"),
                               relief=tk.FLAT, padx=20, pady=8, cursor='hand2')
        current_btn.pack(side=tk.LEFT)

        # Weather display frame
        self.weather_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        self.weather_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.weather_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Current weather tab
        self.current_tab = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.current_tab, text="Current Weather")

        # Forecast tab
        self.forecast_tab = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.forecast_tab, text="5-Day Forecast")

        # Charts tab
        self.charts_tab = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.charts_tab, text="Weather Charts")

        self.setup_current_weather_tab()
        self.setup_forecast_tab()
        self.setup_charts_tab()

        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready", 
                                  bg='#2c3e50', fg='#95a5a6', anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def setup_current_weather_tab(self):
        # Weather info frame
        info_frame = tk.Frame(self.current_tab, bg='#34495e')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Location label
        self.location_label = tk.Label(info_frame, text="", 
                                      font=("Arial", 18, "bold"), 
                                      bg='#34495e', fg='#ecf0f1')
        self.location_label.pack(pady=(0, 10))

        # Weather icon and temperature frame
        temp_frame = tk.Frame(info_frame, bg='#34495e')
        temp_frame.pack(pady=20)

        # Weather icon
        self.weather_icon_label = tk.Label(temp_frame, bg='#34495e')
        self.weather_icon_label.pack(side=tk.LEFT, padx=(0, 20))

        # Temperature
        self.temp_label = tk.Label(temp_frame, text="", 
                                  font=("Arial", 48, "bold"), 
                                  bg='#34495e', fg='#e74c3c')
        self.temp_label.pack(side=tk.LEFT)

        # Weather description
        self.desc_label = tk.Label(info_frame, text="", 
                                  font=("Arial", 14), 
                                  bg='#34495e', fg='#95a5a6')
        self.desc_label.pack(pady=(0, 20))

        # Weather details frame
        details_frame = tk.Frame(info_frame, bg='#34495e')
        details_frame.pack(fill=tk.X, pady=20)

        # Create detail boxes
        self.create_detail_box(details_frame, "Feels Like", "feels_like", 0, 0)
        self.create_detail_box(details_frame, "Humidity", "humidity", 0, 1)
        self.create_detail_box(details_frame, "Wind Speed", "wind_speed", 0, 2)
        self.create_detail_box(details_frame, "Pressure", "pressure", 1, 0)
        self.create_detail_box(details_frame, "Visibility", "visibility", 1, 1)
        self.create_detail_box(details_frame, "UV Index", "uv_index", 1, 2)

    def create_detail_box(self, parent, title, var_name, row, col):
        box_frame = tk.Frame(parent, bg='#2c3e50', relief=tk.RAISED, bd=1)
        box_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        title_label = tk.Label(box_frame, text=title, 
                              font=("Arial", 10, "bold"), 
                              bg='#2c3e50', fg='#95a5a6')
        title_label.pack(pady=(5, 0))

        value_label = tk.Label(box_frame, text="-", 
                              font=("Arial", 14, "bold"), 
                              bg='#2c3e50', fg='#ecf0f1')
        value_label.pack(pady=(0, 5))

        setattr(self, f"{var_name}_label", value_label)

    def setup_forecast_tab(self):
        # Forecast frame with scrollbar
        canvas = tk.Canvas(self.forecast_tab, bg='#34495e')
        scrollbar = ttk.Scrollbar(self.forecast_tab, orient="vertical", command=canvas.yview)
        self.forecast_frame = tk.Frame(canvas, bg='#34495e')

        self.forecast_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_charts_tab(self):
        self.charts_frame = tk.Frame(self.charts_tab, bg='#34495e')
        self.charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return

        self.status_bar.config(text="Fetching weather data...")
        self.root.update()

        # Run in separate thread to prevent GUI freezing
        threading.Thread(target=self._fetch_weather_data, args=(city,), daemon=True).start()

    def _fetch_weather_data(self, city):
        try:
            # Get current weather
            current_params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }

            current_response = requests.get(self.base_url, params=current_params, timeout=10)

            if current_response.status_code == 200:
                current_data = current_response.json()

                # Get forecast data
                forecast_response = requests.get(self.forecast_url, params=current_params, timeout=10)
                forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

                # Update UI in main thread
                self.root.after(0, self._update_weather_display, current_data, forecast_data)
            else:
                error_data = current_response.json()
                error_msg = error_data.get('message', 'Unknown error')
                self.root.after(0, lambda: messagebox.showerror("Error", f"Weather data not found: {error_msg}"))
                self.root.after(0, lambda: self.status_bar.config(text="Ready"))

        except requests.exceptions.Timeout:
            self.root.after(0, lambda: messagebox.showerror("Error", "Request timed out. Please try again."))
            self.root.after(0, lambda: self.status_bar.config(text="Ready"))
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Network error: {str(e)}"))
            self.root.after(0, lambda: self.status_bar.config(text="Ready"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self.status_bar.config(text="Ready"))

    def _update_weather_display(self, current_data, forecast_data):
        try:
            # Update current weather tab
            self._update_current_weather(current_data)

            # Update forecast tab
            if forecast_data:
                self._update_forecast(forecast_data)

            # Update charts tab
            if forecast_data:
                self._update_charts(forecast_data)

            self.status_bar.config(text=f"Weather data updated at {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update display: {str(e)}")
            self.status_bar.config(text="Ready")

    def _update_current_weather(self, data):
        # Extract weather data
        location = f"{data['name']}, {data['sys']['country']}"
        temp = int(data['main']['temp'])
        description = data['weather'][0]['description'].title()
        feels_like = int(data['main']['feels_like'])
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        visibility = data.get('visibility', 0) // 1000  # Convert to km

        # Update labels
        self.location_label.config(text=location)
        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=description)
        self.feels_like_label.config(text=f"{feels_like}°C")
        self.humidity_label.config(text=f"{humidity}%")
        self.wind_speed_label.config(text=f"{wind_speed} m/s")
        self.pressure_label.config(text=f"{pressure} hPa")
        self.visibility_label.config(text=f"{visibility} km")
        self.uv_index_label.config(text="N/A")  # UV index requires separate API call

        # Load weather icon (simplified - you can enhance this)
        icon_code = data['weather'][0]['icon']
        self._load_weather_icon(icon_code)

    def _load_weather_icon(self, icon_code):
        try:
            # Download icon from OpenWeatherMap
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(icon_url, timeout=5)

            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image = image.resize((100, 100))
                photo = ImageTk.PhotoImage(image)
                self.weather_icon_label.config(image=photo)
                self.weather_icon_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"Failed to load weather icon: {e}")

    def _update_forecast(self, data):
        # Clear existing forecast
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        # Group forecast data by day
        forecasts_by_day = {}
        for item in data['list'][:40]:  # 5 days * 8 (3-hour intervals)
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in forecasts_by_day:
                forecasts_by_day[date] = []
            forecasts_by_day[date].append(item)

        # Create forecast cards
        row = 0
        for date, forecasts in list(forecasts_by_day.items())[:5]:
            self._create_forecast_card(self.forecast_frame, date, forecasts, row)
            row += 1

    def _create_forecast_card(self, parent, date, forecasts, row):
        # Calculate daily summary
        temps = [f['main']['temp'] for f in forecasts]
        min_temp = min(temps)
        max_temp = max(temps)

        # Get most common weather condition
        conditions = [f['weather'][0]['main'] for f in forecasts]
        main_condition = max(set(conditions), key=conditions.count)

        # Create card frame
        card_frame = tk.Frame(parent, bg='#2c3e50', relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, padx=10, pady=5)

        # Date
        date_label = tk.Label(card_frame, text=date.strftime('%A, %B %d'), 
                             font=("Arial", 12, "bold"), bg='#2c3e50', fg='#ecf0f1')
        date_label.pack(anchor=tk.W, padx=10, pady=5)

        # Weather info
        info_frame = tk.Frame(card_frame, bg='#2c3e50')
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        condition_label = tk.Label(info_frame, text=main_condition, 
                                  font=("Arial", 10), bg='#2c3e50', fg='#95a5a6')
        condition_label.pack(side=tk.LEFT)

        temp_label = tk.Label(info_frame, text=f"{int(max_temp)}° / {int(min_temp)}°", 
                             font=("Arial", 12, "bold"), bg='#2c3e50', fg='#e74c3c')
        temp_label.pack(side=tk.RIGHT)

    def _update_charts(self, data):
        # Clear existing charts
        for widget in self.charts_frame.winfo_children():
            widget.destroy()

        # Prepare data for charts
        times = []
        temps = []
        humidity = []

        for item in data['list'][:24]:  # Next 24 hours (3-hour intervals)
            time = datetime.fromtimestamp(item['dt'])
            times.append(time)
            temps.append(item['main']['temp'])
            humidity.append(item['main']['humidity'])

        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), facecolor='#34495e')

        # Temperature chart
        ax1.plot(times, temps, color='#e74c3c', linewidth=2, marker='o', markersize=4)
        ax1.set_title('Temperature Forecast (24 hours)', color='#ecf0f1', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)', color='#ecf0f1')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#2c3e50')
        ax1.tick_params(colors='#ecf0f1')

        # Humidity chart
        ax2.bar(times, humidity, color='#3498db', alpha=0.7)
        ax2.set_title('Humidity Forecast (24 hours)', color='#ecf0f1', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Humidity (%)', color='#ecf0f1')
        ax2.set_xlabel('Time', color='#ecf0f1')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2c3e50')
        ax2.tick_params(colors='#ecf0f1')

        # Format x-axis
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_current_location_weather(self):
        messagebox.showinfo("Info", "Current location feature requires additional setup with IP geolocation service.")
        # You can implement IP-based location detection here

    def run(self):
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)

    # Set default city for demo
    app.city_var.set("London")

    app.run()
