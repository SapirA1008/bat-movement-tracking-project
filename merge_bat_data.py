import pandas as pd
import os

# Define the folder where your CSV files are located
folder_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable'

# Get all CSV file names in the folder
file_names = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Check if the script found any CSV files
if len(file_names) == 0:
    print("No CSV files found in the directory.")
else:
    print(f"Found {len(file_names)} CSV files: {file_names}")

# Initialize an empty list to store dataframes
dataframes = []

# Loop through all files and read them into pandas dataframes
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path)  # Read CSV file
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
if len(dataframes) > 0:
    merged_data = pd.concat(dataframes, ignore_index=True)
    output_file = 'merged_bat_data.csv'  # Save as CSV file
    merged_data.to_csv(output_file, index=False)
    print(f"Data merged successfully! Output file saved as {output_file}")
else:
    print("No data to merge.")
