import pandas as pd
import numpy as np

# Step 1: Load all columns as strings (object) first
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_with_distance_chunked.csv'

# Load with all columns as strings to avoid mixed dtype issues
data = pd.read_csv(file_path, dtype=str)

# Step 2: Convert columns to appropriate types
# Convert numeric columns to floats or integers
numeric_columns = ['lat', 'lon', 'alt', 'time', 'tag', 'num_of_det', 'num_of_const', 
                   'gradnrm', 'varx', 'covxy', 'covxz', 'vary', 'distance_moved']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')  # 'coerce' will turn errors into NaN

# Convert date-related columns to datetime
data['parsed_times'] = pd.to_datetime(data['parsed_times'], errors='coerce')  # 'coerce' will handle invalid dates

# Step 3: Filter out rows with invalid numeric or datetime values
# Drop rows where any of the necessary numeric columns contain NaN values
cleaned_data = data.dropna(subset=numeric_columns + ['parsed_times'])

# Step 4: Filter out rows based on business rules (distance threshold, etc.)
MAX_DISTANCE = 5000  # meters, for example
MIN_TIME_DIFF = 1  # minutes

# Calculate time difference in minutes
cleaned_data['time_diff'] = cleaned_data.groupby('tag')['parsed_times'].diff().dt.total_seconds() / 60

# Filter based on distance and time diff criteria
final_filtered_data = cleaned_data[(cleaned_data['distance_moved'] <= MAX_DISTANCE) | 
                                   (cleaned_data['time_diff'] >= MIN_TIME_DIFF)]

# Step 5: Save the cleaned and filtered dataset
output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_cleaned.csv'
final_filtered_data.to_csv(output_file, index=False)

print("Data cleaning and filtering completed. Saved to filtered_bat_data_cleaned.csv")
