import pandas as pd
import numpy as np

# Load the data with explicit data types
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_with_distance_chunked.csv'

# Specify dtypes for columns to prevent mixed types
dtype_spec = {
    'lat': 'float64',
    'lon': 'float64',
    'alt': 'float64',
    'time': 'float64',   # Assuming 'time' is a float; change this if it's not
    'tag': 'int64',
    'num_of_det': 'int64',
    'num_of_const': 'int64',
    'gradnrm': 'float64',
    'varx': 'float64',
    'covxy': 'float64',
    'covxz': 'float64',
    'vary': 'float64',
    'times': 'object',  # 'times' is probably an object because of date strings
    'distance_moved': 'float64'  # Ensure the distance_moved is treated as numeric
}

# Load the data
data = pd.read_csv(file_path, dtype=dtype_spec, parse_dates=['parsed_times'])

# Step 1: Set thresholds (for example, max distance is 5000 meters)
MAX_DISTANCE = 5000  # meters

# Step 2: Filter out rows with distances larger than the threshold
filtered_data = data[data['distance_moved'] <= MAX_DISTANCE]

# Step 3: Handle any rows with NaN distance values (optional)
filtered_data 
