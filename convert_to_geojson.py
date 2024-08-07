import requests
import json
import os
import pandas as pd
from datetime import datetime

# URL to fetch traffic flow data
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
api_key = os.getenv('tomtom_key')

# Path to the CSV file in your GitHub repository
csv_url = "https://raw.githubusercontent.com/MillcreekGIS/traffic/main/road_midpoints1.csv"

# Read the CSV file
df = pd.read_csv(csv_url)

# Initialize GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Loop through each row in the CSV file
for index, row in df.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    
    # Build the request URL
    url = f"{base_url}?point={lat},{lon}&unit=MPH&openLr=false&key={api_key}"
    print(f"Request URL: {url}")
    
    # Fetch the traffic data
    response = requests.get(url)
    if response.status_code == 200:
        traffic_data = response.json()
        
        # Print the response to debug
        print(json.dumps(traffic_data, indent=2))
        
        # Ensure the correct path to the data
        if "flowSegmentData" in traffic_data:
            segment = traffic_data["flowSegmentData"]
            coordinates = segment["coordinates"]["coordinate"]
            
            # Create a list of coordinate pairs for the LineString
            line_coordinates = [[coord["longitude"], coord["latitude"]] for coord in coordinates]

            # Get the current timestamp
            last_updated = datetime.utcnow().isoformat() + 'Z'

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": line_coordinates
                },
                "properties": {
                    "currentSpeed": segment["currentSpeed"],
                    "freeFlowSpeed": segment["freeFlowSpeed"],
                    "confidence": segment["confidence"],
                    "roadClosure": segment["roadClosure"],
                    "last_updated": last_updated
                }
            }
            geojson["features"].append(feature)
        else:
            print("No flowSegmentData found in the response.")
    else:
        print(f"Failed to fetch data for {lat}, {lon}: {response.status_code}")
        print(f"Response content: {response.content}")

# Save the GeoJSON to a file
with open('traffic_data.geojson', 'w') as f:
    json.dump(geojson, f)

print("GeoJSON file created successfully.")
