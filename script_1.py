# Create a simple beginner-friendly weather app
simple_weather_app = '''
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
'''

# Save simple weather app
with open('simple_weather_app.py', 'w') as f:
    f.write(simple_weather_app)

print("✅ Simple Weather App code created!")

# Create PyQt5 version
pyqt_weather_app = '''
import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from datetime import datetime

class WeatherWorker(QThread):
    weather_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, city, api_key):
        super().__init__()
        self.city = city
        self.api_key = api_key
        
    def run(self):
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            url = "http://api.openweathermap.org/data/2.5/weather"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.weather_fetched.emit(data)
            else:
                error_data = response.json()
                self.error_occurred.emit(error_data.get('message', 'Unknown error'))
                
        except Exception as e:
            self.error_occurred.emit(str(e))

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_key = "your_api_key_here"  # Replace with your API key
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('PyQt Weather App')
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-family: Arial;
            }
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel('🌤️ PyQt Weather App')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet("color: #ecf0f1; margin: 20px;")
        layout.addWidget(title)
        
        # Input section
        input_layout = QHBoxLayout()
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText('Enter city name...')
        self.city_input.returnPressed.connect(self.get_weather)
        input_layout.addWidget(self.city_input)
        
        self.search_btn = QPushButton('Get Weather')
        self.search_btn.clicked.connect(self.get_weather)
        input_layout.addWidget(self.search_btn)
        
        layout.addLayout(input_layout)
        
        # Weather display
        self.weather_display = QTextEdit()
        self.weather_display.setReadOnly(True)
        self.weather_display.setPlainText('Enter a city name and click "Get Weather" to see the forecast.')
        layout.addWidget(self.weather_display)
        
        # Status label
        self.status_label = QLabel('Ready')
        self.status_label.setStyleSheet("color: #95a5a6; margin: 5px;")
        layout.addWidget(self.status_label)
        
    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, 'Warning', 'Please enter a city name!')
            return
            
        self.status_label.setText('Fetching weather data...')
        self.search_btn.setEnabled(False)
        
        # Start worker thread
        self.worker = WeatherWorker(city, self.api_key)
        self.worker.weather_fetched.connect(self.display_weather)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.start()
        
    def display_weather(self, data):
        try:
            # Format weather information
            city = data['name']
            country = data['sys']['country']
            temp = int(data['main']['temp'])
            feels_like = int(data['main']['feels_like'])
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            description = data['weather'][0]['description'].title()
            wind_speed = data['wind']['speed']
            
            weather_text = f"""
🌍 Location: {city}, {country}
🌡️ Temperature: {temp}°C
🤗 Feels like: {feels_like}°C
📝 Description: {description}
💧 Humidity: {humidity}%
🌬️ Wind Speed: {wind_speed} m/s
📊 Pressure: {pressure} hPa

Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            self.weather_display.setPlainText(weather_text)
            self.status_label.setText(f'Weather data updated for {city}')
            
        except Exception as e:
            self.show_error(f"Error displaying weather data: {str(e)}")
        finally:
            self.search_btn.setEnabled(True)
            
    def show_error(self, error_message):
        QMessageBox.critical(self, 'Error', error_message)
        self.status_label.setText('Error occurred')
        self.search_btn.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
'''

# Save PyQt weather app
with open('pyqt_weather_app.py', 'w') as f:
    f.write(pyqt_weather_app)

print("✅ PyQt Weather App code created!")

# Create installation and setup guide
setup_guide = '''
# GUI Weather App Setup Guide

## Prerequisites
1. Python 3.7 or higher installed
2. pip package manager

## Installation Steps

### 1. Install Required Packages

For Simple Tkinter App:
```bash
pip install requests pillow
```

For Advanced Tkinter App:
```bash
pip install requests pillow matplotlib
```

For PyQt5 App:
```bash
pip install PyQt5 requests
```

### 2. Get OpenWeatherMap API Key

1. Visit: https://openweathermap.org/
2. Sign up for a free account
3. Go to "API keys" section in your dashboard
4. Copy your API key
5. Replace "your_api_key_here" in the code with your actual API key

### 3. Run the Application

```bash
# For simple app
python simple_weather_app.py

# For advanced app
python modern_weather_app.py

# For PyQt app
python pyqt_weather_app.py
```

## Features Comparison

| Feature | Simple Tkinter | Advanced Tkinter | PyQt5 |
|---------|---------------|------------------|-------|
| Basic Weather | ✅ | ✅ | ✅ |
| Weather Icons | ❌ | ✅ | ❌ |
| Forecast | ❌ | ✅ | ❌ |
| Charts | ❌ | ✅ | ❌ |
| Modern UI | ❌ | ✅ | ✅ |
| Threading | ❌ | ✅ | ✅ |

## Troubleshooting

### Common Issues:

1. **"Invalid API key"**: Make sure you've replaced the placeholder with your actual API key
2. **"City not found"**: Check spelling and try with country code (e.g., "London,UK")
3. **Network errors**: Check your internet connection
4. **Import errors**: Make sure all required packages are installed

### API Usage Limits:
- Free tier: 1000 calls/month
- Rate limit: 60 calls/minute

## Extending the Application

### Add New Features:
1. **Weather Alerts**: Use OpenWeatherMap alerts API
2. **Historical Data**: Integrate historical weather data
3. **Multiple Cities**: Allow saving favorite cities
4. **Units Conversion**: Add Fahrenheit/Celsius toggle
5. **Weather Maps**: Integrate weather maps
6. **Voice Commands**: Add speech recognition
'''

# Save setup guide
with open('weather_app_setup_guide.md', 'w') as f:
    f.write(setup_guide)

print("✅ Setup guide created!")

# List all created files
print("\n📁 Files created:")
print("1. simple_weather_app.py - Beginner-friendly basic weather app")
print("2. modern_weather_app.py - Advanced weather app with charts and forecast")
print("3. pyqt_weather_app.py - PyQt5 version with modern styling")
print("4. weather_app_setup_guide.md - Complete setup and installation guide")