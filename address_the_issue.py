import pandas as pd
import numpy as np

# Load the data
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_with_distance_chunked.csv'
data = pd.read_csv(file_path)

# Step 1: Set thresholds (for example, max distance is 5000 meters)
MAX_DISTANCE = 5000  # meters

# Step 2: Filter out rows with distances larger than the threshold
data['distance_moved'] = pd.to_numeric(data['distance_moved'], errors='coerce')  # Ensure numeric values
filtered_data = data[data['distance_moved'] <= MAX_DISTANCE]

# Step 3: Handle any rows with NaN distance values (optional)
filtered_data = filtered_data.dropna(subset=['distance_moved'])

# Step 4: Filter out rows where the time difference is too small, but the distance is large
filtered_data['parsed_times'] = pd.to_datetime(filtered_data['parsed_times'], errors='coerce')
filtered_data['time_diff'] = filtered_data.groupby('tag')['parsed_times'].diff().dt.total_seconds() / 60  # time_diff in minutes

# Set a time difference threshold (e.g., at least 1 minute must have passed)
MIN_TIME_DIFF = 1  # minutes

# If the distance is large but the time difference is very small, flag these rows
filtered_data = filtered_data[(filtered_data['time_diff'] >= MIN_TIME_DIFF) | (filtered_data['distance_moved'] <= MAX_DISTANCE)]

# Step 5: Save the cleaned data
filtered_data.to_csv(r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_cleaned.csv', index=False)

print("Data has been cleaned and saved to filtered_bat_data_cleaned.csv")
