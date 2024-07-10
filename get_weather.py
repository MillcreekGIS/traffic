import requests
import json

# URL for Millcreek, UT weather forecast
url = "https://api.weather.gov/gridpoints/OKX/36,36/forecast"

# Fetch the weather data
response = requests.get(url)
data = response.json()

# Extract the first 5 periods
periods = data['properties']['periods'][:5]

# Generate HTML
html_content = "<div class='weather-forecast'>"

for period in periods:
    html_content += f"""
    <div class='weather-period'>
        <h3>{period['name']}</h3>
        <p>Temperature: {period['temperature']} {period['temperatureUnit']}</p>
        <p>Wind: {period['windSpeed']} {period['windDirection']}</p>
        <p>Forecast: {period['shortForecast']}</p>
    </div>
    <hr>
    """

html_content += "</div>"

# Save the HTML to a file
with open('weather_forecast.html', 'w') as file:
    file.write(html_content)

print("HTML file created successfully: weather_forecast.html")
