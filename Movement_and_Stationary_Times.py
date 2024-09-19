import pandas as pd
from geopy.distance import geodesic

# Define movement threshold in meters
MOVEMENT_THRESHOLD = 10  # Adjust as needed
chunk.columns = chunk.columns.str.strip()


# Define the function to calculate distance
def calculate_distance(row1, row2):
    coords_1 = (row1['lat'], row1['lon'])
    coords_2 = (row2['lat'], row2['lon'])
    if pd.notna(coords_1[0]) and pd.notna(coords_2[0]):
        return geodesic(coords_1, coords_2).meters
    else:
        return 0

# Define the function to calculate distances, time_diff, and movement_status
def calc_distances(group):
    group = group.copy()
    group = group.sort_values(by='parsed_times')  # Ensure sorting by time
    
    # Calculate previous lat and lon
    group['prev_lat'] = group['lat'].shift()
    group['prev_lon'] = group['lon'].shift()
    
    # Calculate distance moved
    group['distance_moved'] = group.apply(
        lambda row: calculate_distance(row[['lat', 'lon']], row[['prev_lat', 'prev_lon']]) 
        if pd.notna(row['prev_lat']) and pd.notna(row['prev_lon']) else 0, axis=1)
    
    # Calculate time_diff in seconds
    group['time_diff'] = group['parsed_times'].diff().dt.total_seconds().fillna(0)
    
    # Classify movement_status
    group['movement_status'] = group['distance_moved'].apply(
        lambda x: 'moving' if x > MOVEMENT_THRESHOLD else 'stationary'
    )
    
    return group

# Load the dataset in chunks
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data.csv'
chunk_size = 500000  # Adjust based on your system's performance
chunks = pd.read_csv(file_path, chunksize=chunk_size)

output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_with_distance_movement_chunked.csv'
summary_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\movement_summary.csv'

# Initialize a summary dictionary
summary = {}

# To handle chunk boundaries, keep track of the last row of each tag
last_rows = {}

# Process each chunk
with open(output_file, 'w') as f_out:
    for chunk_num, chunk in enumerate(chunks):
        print(f"Processing chunk {chunk_num + 1}...")
        
        # Ensure the 'times' column is correctly parsed
        chunk['parsed_times'] = pd.to_datetime(chunk['times'], errors='coerce')
        
        # Sort by 'tag' and 'parsed_times'
        chunk = chunk.sort_values(by=['tag', 'parsed_times'])
        
        # If there are last rows from the previous chunk, prepend them to the current chunk
        if last_rows:
            # Convert the last_rows dictionary to a DataFrame
            last_rows_df = pd.DataFrame.from_dict(last_rows, orient='index').reset_index(drop=True)
            # Prepend the last row to the current chunk
            chunk = pd.concat([last_rows_df, chunk], ignore_index=True)
            # Reset last_rows
            last_rows = {}
        
        # Group by 'tag' and apply the distance and time calculations
        chunk = chunk.groupby('tag', group_keys=False).apply(calc_distances)
        
        # After processing, save the last row for each tag to handle chunk boundaries
        # Get the last row per tag
        last_chunk_rows = chunk.groupby('tag').tail(1)
        for _, row in last_chunk_rows.iterrows():
            tag = row['tag']
            last_rows[tag] = row
        
        # Remove the last row of each tag from the current chunk to avoid duplication in the next chunk
        chunk = chunk[~chunk.index.isin(last_chunk_rows.index)]
        
        # Calculate per tag summary for this chunk
        chunk_summary = chunk.groupby(['tag', 'movement_status'])['time_diff'].sum().reset_index()
        
        # Accumulate the summary
        for _, row in chunk_summary.iterrows():
            tag = row['tag']
            status = row['movement_status']
            time = row['time_diff']
            if tag not in summary:
                summary[tag] = {'moving_time_seconds': 0, 'stationary_time_seconds': 0}
            if status == 'moving':
                summary[tag]['moving_time_seconds'] += time
            elif status == 'stationary':
                summary[tag]['stationary_time_seconds'] += time
        
        # Write the chunk to the output file
        if chunk_num == 0:
            chunk.to_csv(f_out, index=False)  # Write header in the first chunk
        else:
            chunk.to_csv(f_out, index=False, header=False)  # Append without header
        
        print(f"Chunk {chunk_num + 1} processed and saved.")
        
# After all chunks are processed, save the summary
summary_df = pd.DataFrame([
    {'tag': tag, 'moving_time_seconds': data['moving_time_seconds'], 'stationary_time_seconds': data['stationary_time_seconds']}
    for tag, data in summary.items()
])

summary_df.to_csv(summary_file, index=False)
print(f"Movement summary saved to {summary_file}")
