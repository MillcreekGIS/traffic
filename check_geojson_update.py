# check when the geojsons were last updated
# if it's been more than xx minutes it replaces them with a blank file
import os
import datetime
import pytz

def check_file_update(file_path, time_threshold):
    current_time = datetime.datetime.now(pytz.UTC)
    
    if os.path.exists(file_path):
        modification_time = os.path.getmtime(file_path)
        modification_time = datetime.datetime.fromtimestamp(modification_time, tz=pytz.UTC)

        time_difference = current_time - modification_time

        if time_difference > time_threshold:
            # File not updated within the threshold, replace with a blank file
            with open(file_path, 'w') as f:
                f.write('{}')  # Writing an empty GeoJSON object
            print(f"{file_path} was not updated within the last {time_threshold}. Replaced with a blank file.")
        else:
            print(f"{file_path} was updated within the last {time_threshold}. No action needed.")
    else:
        print(f"{file_path} does not exist.")

# Check traffic_data.geojson
check_file_update('traffic_data.geojson', datetime.timedelta(minutes=20))

# Check incidents.geojson
check_file_update('incidents.geojson', datetime.timedelta(minutes=30))
