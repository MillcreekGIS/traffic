from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import json
import os

# Authenticate with AGOL
gis = GIS("https://www.arcgis.com", os.getenv('AGOL_USERNAME'), os.getenv('AGOL_PASSWORD'))

# Get the Feature Layer
item = gis.content.get(os.getenv('AGOL_ITEM_ID'))
flc = FeatureLayerCollection.fromitem(item)

# Load the updated GeoJSON data
with open("traffic_data.geojson", "r") as f:
    geojson_data = json.load(f)

# Update the feature layer with new GeoJSON data
flc.manager.overwrite(geojson_data)

print("Feature layer updated successfully.")
