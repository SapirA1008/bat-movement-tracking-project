import os
import pandas as pd
import matplotlib.pyplot as plt

# Correct file path to the processed data
file_path = 'C:/Users/sapir/OneDrive/Desktop/Project/132_rawtable/filtered_bat_data_with_distance_chunked.csv'

# 1. Check if the file exists and is not empty
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print("Loading data...")
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")
    except pd.errors.EmptyDataError:
        print("Error: No data found in the file.")
else:
    print("File does not exist or is empty.")
    exit()

# 2. Check for Missing Values in Key Columns
print("\nChecking for missing values in key columns (lat, lon, parsed_times, distance_moved):")
missing_values = data[['lat', 'lon', 'parsed_times', 'distance_moved']].isnull().sum()
print(missing_values)

# 3. Check Data Types
print("\nChecking data types of columns:")
print(data.dtypes)

# 4. Describe the 'distance_moved' Column to Check Reasonable Values
print("\nChecking summary statistics of 'distance_moved':")
print(data['distance_moved'].describe())

# 5. Check the Time Differences and Compare with Movement
print("\nCalculating 'time_diff' in minutes between consecutive points:")
data['parsed_times'] = pd.to_datetime(data['parsed_times'], errors='coerce')
data['time_diff'] = data.groupby('tag')['parsed_times'].diff().dt.total_seconds() / 60  # Time difference in minutes
print(data[['tag', 'time_diff', 'distance_moved']].head(10))

# 6. Check Specific Tags for Manual Validation
print("\nChecking data for a specific tag (e.g., tag 119):")
tag_data = data[data['tag'] == 119]  # Example tag number
print(tag_data.head(10))

# 7. Outlier Analysis: Plot the Distribution of 'distance_moved'
print("\nPlotting distribution of 'distance_moved':")
data['distance_moved'].hist(bins=50)
plt.xlabel('Distance Moved (meters)')
plt.ylabel('Frequency')
plt.title('Distribution of Distance Moved')
plt.show()

# 8. Check for Negative Values in 'time_diff' and 'distance_moved'
print("\nChecking for negative 'time_diff' values:")
negative_time_diff = data[data['time_diff'] < 0]
print(negative_time_diff)

print("\nChecking for negative 'distance_moved' values:")
negative_distance_moved = data[data['distance_moved'] < 0]
print(negative_distance_moved)

# 9. Check if Stationary Periods (is_moving == False) Have Close to Zero Distance
print("\nChecking if stationary periods (is_moving == False) have close to zero 'distance_moved':")
stationary_data = data[data['is_moving'] == False]['distance_moved'].describe()
print(stationary_data)

# 10. Randomly Sample Rows for Manual Validation
print("\nRandomly sampling 5 rows for manual validation:")
sample_data = data.sample(5)
print(sample_data)

# 11. Saving Any Issues Found to a File for Further Inspection
print("\nSaving negative time and distance rows to 'negative_values.csv' for review:")
negative_values = pd.concat([negative_time_diff, negative_distance_moved])
negative_values.to_csv('C:/Users/sapir/OneDrive/Desktop/Project/132_rawtable/negative_values.csv', index=False)

print("\nVerification complete.")
