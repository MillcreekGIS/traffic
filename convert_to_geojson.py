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

for segment in traffic_data['flowSegmentData']:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [segment["start"]["longitude"], segment["start"]["latitude"]],
                [segment["end"]["longitude"], segment["end"]["latitude"]]
            ]
        },
        "properties": {
            "currentSpeed": segment["currentSpeed"],
            "freeFlowSpeed": segment["freeFlowSpeed"],
            "confidence": segment["confidence"],
            "roadClosure": segment["roadClosure"]
        }
    }
    geojson["features"].append(feature)

# Save the GeoJSON to a file
with open('traffic_data.geojson', 'w') as f:
    json.dump(geojson, f)
