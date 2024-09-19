import pandas as pd
from datetime import datetime

# Load the bat interaction data
interaction_data = pd.read_csv("your_interaction_data_file.csv")

# Convert times to datetime
interaction_data['bat_1_time'] = pd.to_datetime(interaction_data['bat_1_time'], format="%d/%m/%Y %H:%M")
interaction_data['bat_2_time'] = pd.to_datetime(interaction_data['bat_2_time'], format="%d/%m/%Y %H:%M")

# Filter for night hours (between 6:00 PM and 6:00 AM)
def is_nighttime(time):
    return time.hour >= 18 or time.hour < 6

interaction_data['night_interaction'] = interaction_data['bat_1_time'].apply(is_nighttime) & interaction_data['bat_2_time'].apply(is_nighttime)

# Assuming 'movement_type' indicates if the bats are stationary
# Add a placeholder column 'stationary' if it doesn't exist
interaction_data['stationary'] = (interaction_data['movement_type'] == 'stationary')

# Filter for nighttime stationary interactions
filtered_data = interaction_data[(interaction_data['night_interaction']) & (interaction_data['stationary'])]

# Set a distance threshold (e.g., 50 meters)
def haversine(lat1, lon1, lat2, lon2):
    # This function calculates the great-circle distance between two points
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Radius of the Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # Convert to meters

filtered_data['distance_between_bats'] = filtered_data.apply(lambda row: haversine(row['bat_1_lat'], row['bat_1_lon'], row['bat_2_lat'], row['bat_2_lon']), axis=1)

# Filter interactions where bats are within a reasonable distance (e.g., 50 meters)
distance_threshold = 50
close_interactions = filtered_data[filtered_data['distance_between_bats'] <= distance_threshold]

# Save the result to a CSV file
close_interactions.to_csv("nighttime_social_interactions.csv", index=False)

print("Nighttime stationary interactions saved to 'nighttime_social_interactions.csv'.")
