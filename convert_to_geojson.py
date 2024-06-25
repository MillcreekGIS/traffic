import requests
import json

# URL to fetch traffic flow data
url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point=40.68593,-111.84545&unit=MPH&openLr=false&key=LtTnJJ7ZG1kboQESdpCfgb2THXMsoU8i"

response = requests.get(url)
traffic_data = response.json()

# Convert JSON to GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Ensure the correct path to the data
if "flowSegmentData" in traffic_data:
    segment = traffic_data["flowSegmentData"]
    coordinates = segment["coordinates"]["coordinate"]
    
    # Create a list of coordinate pairs for the LineString
    line_coordinates = [[coord["longitude"], coord["latitude"]] for coord in coordinates]

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
            "roadClosure": segment["roadClosure"]
        }
    }
    geojson["features"].append(feature)
else:
    print("No flowSegmentData found in the response.")

# Save the GeoJSON to a file
with open('traffic_data.geojson', 'w') as f:
    json.dump(geojson, f)
