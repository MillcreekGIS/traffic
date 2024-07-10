import json
import requests

# URL of the incidents JSON data
url = "https://www.udottraffic.utah.gov/map/mapIcons/Incidents"

# Fetch the JSON data
response = requests.get(url)
data = response.json()

# Extract the incidents data from item2
incidents = data['item2']

# Initialize GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Loop through each incident and convert it to a GeoJSON feature
for incident in incidents:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": incident["location"]
        },
        "properties": {
            "itemId": incident["itemId"],
            "icon": incident["icon"],
            "title": incident["title"]
        }
    }
    geojson["features"].append(feature)

# Save the GeoJSON to a file
output_file = 'incidents.geojson'
with open(output_file, 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"GeoJSON file created successfully: {output_file}")
