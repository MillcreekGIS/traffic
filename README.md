# Traffic Data Monitoring and Update System

This repository contains scripts and workflows for monitoring and updating traffic data. The system uses GitHub Actions to run Python scripts at regular intervals to check and update traffic data stored in a GeoJSON file.

## Files and Directories

- **check-geojson-update.yml**: GitHub Actions workflow to check when the GeoJSON file was last updated.
- **update_geojson.yml**: GitHub Actions workflow to update the GeoJSON file with the latest traffic data.
- **check_geojson_update.py**: Python script to check the last update time of the GeoJSON file and replace it with a blank file if it hasn't been updated within the specified time.
- **convert_to_geojson.py**: Python script to fetch the latest traffic data and convert it into a GeoJSON file.
- **requirements.txt**: List of Python dependencies required for the scripts.
- **road_midpoints1.csv**: CSV file containing the coordinates of road midpoints used to fetch traffic data.
- **traffic_data.geojson**: GeoJSON file where the traffic data is stored. The "Traffic Web Map" in ArcGIS online has a layer that is directly linked to this GeoJSON.

## Workflows

### Check GeoJSON Update Workflow

This workflow checks the last update time of the `traffic_data.geojson` file. If the file hasn't been updated within the specified time (e.g., 20 minutes), it replaces the file with a blank GeoJSON file.

**Workflow File:** `.github/workflows/check-geojson-update.yml`

**Schedule:**
- Runs every 5 minutes
- Can be triggered manually

### Update GeoJSON Workflow

This workflow fetches the latest traffic data from the TomTom API and updates the `traffic_data.geojson` file.

**Workflow File:** `.github/workflows/update_geojson.yml`

**Schedule:**
- Runs every 10 minutes from 6 AM to 9 PM Mountain Time (based on UTC, must be adjusted for daylight saving time)
- Can be triggered manually

## Scripts

### check_geojson_update.py

This script checks when the `traffic_data.geojson` file was last updated. If it has not been updated within the past 20 minutes, it replaces the file with a blank GeoJSON file.

**How it works:**
1. Checks the last modification time of the `traffic_data.geojson` file.
2. If the file hasn't been updated within the last 20 minutes, it replaces the file with a blank GeoJSON object.
3. Prints the result of the check to the console.

### convert_to_geojson.py

This script fetches the latest traffic data from the TomTom API and converts it into a GeoJSON file.

**How it works:**
1. Reads coordinates from the `road_midpoints1.csv` file.
2. Fetches traffic data from the TomTom API for each coordinate.
3. Converts the traffic data into a GeoJSON format.
4. Saves the GeoJSON data to the `traffic_data.geojson` file.

## Installation

To run the scripts locally, you need to install the required Python packages. Use the following command to install the dependencies:

```sh
pip install -r requirements.txt
```
## Environment Variables

The `convert_to_geojson.py` script requires a TomTom API key to fetch traffic data. Set the `tomtom_key` environment variable with your TomTom API key.

## Usage

### Running the Workflows

The workflows are set up to run automatically based on the defined schedule. You can also trigger them manually from the GitHub Actions tab in the repository.

### Running the Scripts Locally

To run the scripts locally, use the following commands:

```sh
python check_geojson_update.py
python convert_to_geojson.py
```

Ensure you have set the necessary environment variables before running the scripts.
