
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
