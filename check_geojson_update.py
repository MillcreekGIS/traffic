# check when the traffic geojson was last updated
# if it's been more than xx minutes
import os
import datetime
import pytz

file_path = 'traffic_data.geojson'

# Define the time threshold
time_threshold = datetime.timedelta(minutes=20)
current_time = datetime.datetime.now(pytz.UTC)

if os.path.exists(file_path):
    modification_time = os.path.getmtime(file_path)
    modification_time = datetime.datetime.fromtimestamp(modification_time, tz=pytz.UTC)

    time_difference = current_time - modification_time

    if time_difference > time_threshold:
        # File not updated within the threshold, replace with a blank file
        with open(file_path, 'w') as f:
            f.write('{}')  # Writing an empty GeoJSON object
        print(f"GeoJSON file was not updated within the last {time_threshold}. Replaced with a blank file.")
    else:
        print(f"GeoJSON file was updated within the last {time_threshold}. No action needed.")
else:
    print("GeoJSON file does not exist.")
