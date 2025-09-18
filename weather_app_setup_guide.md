
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
