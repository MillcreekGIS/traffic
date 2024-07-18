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
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast</title>
    <style>
        /* Ensure the container takes full height of the parent */
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }

        .weather-forecast {
            height: 100%;
            overflow-y: auto;
            padding: 10px;
            color: #fdf0d5;
            font-family: Arial, sans-serif;
        }

        .weather-period {
            margin-bottom: 10px;
        }

        .weather-period h3 {
            margin: 5px 0;
        }

        .weather-period p {
            margin: 3px 0;
        }

        hr {
            border: 0;
            border-top: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="weather-forecast">
"""

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

html_content += """
    </div>
</body>
</html>
"""

# Save the HTML to a file
with open('index.html', 'w') as file:
    file.write(html_content)

print("HTML file created successfully: index.html")
