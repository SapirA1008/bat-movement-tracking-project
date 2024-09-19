import pandas as pd

# Constants
MIN_SPEED = 0.0  # Minimum speed (bats are stationary when speed is close to 0)
MAX_SPEED = 15.0  # Lowered maximum speed limit based on bat movement
MAX_DISTANCE_MOVED = 500.0  # Maximum distance a bat can reasonably move between points
STATIONARY_THRESHOLD = 0.1  # Threshold for considering a bat as stationary (speed < 0.1 m/s)
MIN_TIME_DIFF = 0.01  # Minimum time difference to avoid dividing by very small values
VARX_THRESHOLD = 30  # Lowered varx threshold to filter out noisy data
COVXY_THRESHOLD = 50  # Lowered covxy threshold to filter out noisy data

# Load the dataset
file_path = 'filtered_bat_data_cleaned.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure lat_diff, lon_diff, and time_diff are calculated
data['lat_diff'] = data['lat'].diff()
data['lon_diff'] = data['lon'].diff()
data['time_diff'] = data['time'].diff()

# Calculate speed as distance/time
def calculate_speed(row):
    time_diff = row['time_diff']
    if pd.isna(time_diff) or time_diff == 0:
        return 0
    distance = ((row['lat_diff'] ** 2) + (row['lon_diff'] ** 2)) ** 0.5
    return distance / time_diff

data['speed'] = data.apply(calculate_speed, axis=1)

# Step 1: Apply additional distance threshold
def is_outlier(row):
    return (row['varx'] > VARX_THRESHOLD) or (row['covxy'] > COVXY_THRESHOLD) or (row['speed'] > MAX_SPEED) or (row['distance_moved'] > MAX_DISTANCE_MOVED)

data['is_outlier'] = data.apply(is_outlier, axis=1)

# Step 2: Segment data into movement patterns
def classify_movement(row):
    if row['speed'] < STATIONARY_THRESHOLD:
        return "stationary"
    elif row['is_outlier']:
        return "outlier"
    else:
        return "valid_movement"

# Apply the classification
data['movement_type'] = data.apply(classify_movement, axis=1)

# Step 3: Analyze movement patterns for valid rows
valid_data = data[data['movement_type'] == "valid_movement"]
outlier_data = data[data['movement_type'] == "outlier"]
stationary_data = data[data['movement_type'] == "stationary"]

# Save the results to CSV
valid_data.to_csv('valid_data.csv', index=False)
outlier_data.to_csv('outlier_data.csv', index=False)
stationary_data.to_csv('stationary_data.csv', index=False)

# Summary
print(f"Valid movement rows: {len(valid_data)}")
print(f"Outlier rows: {len(outlier_data)}")
print(f"Stationary rows: {len(stationary_data)}")
