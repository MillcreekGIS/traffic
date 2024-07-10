import json
import requests

# URL of the incidents JSON data
incidents_url = "https://www.udottraffic.utah.gov/map/mapIcons/Incidents"
incident_details_base_url = "https://www.udottraffic.utah.gov/map/data/Incidents/"

# Bounding box coordinates
nw_point = (40.90012110976349, -112.18707379615758)
se_point = (40.46627775757053, -111.5244192742487)

# Function to check if a point is within the bounding box
def is_within_bounding_box(lat, lon, nw_point, se_point):
    return nw_point[0] >= lat >= se_point[0] and nw_point[1] <= lon <= se_point[1]

# Fetch the JSON data
response = requests.get(incidents_url)
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
    # Extract the latitude and longitude
    lat, lon = incident["location"]
    
    # Check if the incident is within the bounding box
    if not is_within_bounding_box(lat, lon, nw_point, se_point):
        continue
    
    # Flip the coordinates to (longitude, latitude)
    coordinates = [lon, lat]
    
    # Fetch additional details for each incident
    item_id = incident["itemId"]
    details_url = f"{incident_details_base_url}{item_id}"
    details_response = requests.get(details_url)
    
    if details_response.status_code == 200:
        details = details_response.json()
    else:
        details = {}

    # Extract sub-details and add them as separate fields
    sub_details = {}
    if details:
        sub_details.update({
            "organizationCenterId": details.get("id", {}).get("organizationCenterId", ""),
            "organizationId": details.get("id", {}).get("organizationId", ""),
            "operatorComment": details.get("operatorComment", ""),
            "areaName": details.get("areas", {}).get("areaName", ""),
            "lanesAffected": details.get("lanes", {}).get("lanesAffected", ""),
            "roadwayName": details.get("location", {}).get("roadwayName", ""),
            "linkDesignator": details.get("location", {}).get("linkDesignator", ""),
            "linkDirection": details.get("location", {}).get("linkDirection", ""),
            "startTime": details.get("dates", {}).get("startTime", ""),
            "endTime": details.get("dates", {}).get("endTime", ""),
            "lastUpdated": details.get("dates", {}).get("lastUpdated", ""),
            "headlineEventType": details.get("headline", {}).get("headlineEventType", ""),
            "headlineEventSubType": details.get("headlineEventSubType", ""),
            "isActive": details.get("isActive", ""),
            "isFullClosure": details.get("isFullClosure", "")
        })

        # Extract details from the 'details' field if present
        if "details" in details:
            sub_details.update({
                "typeCode": details["details"].get("typeCode", ""),
                "eventDescription": details["details"].get("detailLang1", {}).get("eventDescription", ""),
                "eventTypeName": details["details"].get("detailLang1", {}).get("eventTypeName", ""),
                "eventTypeLongName": details["details"].get("detailLang1", {}).get("eventTypeLongName", ""),
                "eventSubTypeName": details["details"].get("detailLang1", {}).get("eventSubTypeName", ""),
                "eventSubTypeLongName": details["details"].get("detailLang1", {}).get("eventSubTypeLongName", "")
            })

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coordinates
        },
        "properties": {
            "itemId": item_id,
            "icon": incident["icon"],
            "title": incident["title"],
            **sub_details
        }
    }
    geojson["features"].append(feature)

# Save the GeoJSON to a file
output_file = 'incidents.geojson'
with open(output_file, 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"GeoJSON file created successfully: {output_file}")
