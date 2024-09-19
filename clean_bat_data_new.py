import pandas as pd
from geopy.distance import geodesic

# Define the function to calculate distance
def calculate_distance(row1, row2):
    coords_1 = (row1['lat'], row1['lon'])
    coords_2 = (row2['lat'], row2['lon'])
    if pd.notna(coords_1[0]) and pd.notna(coords_2[0]):
        return geodesic(coords_1, coords_2).meters
    else:
        return 0

# Define the function to calculate distances for each group
def calc_distances(group):
    group = group.copy()  # Avoid SettingWithCopyWarning
    group['distance_moved'] = group[['lat', 'lon']].shift().apply(
        lambda row: calculate_distance(row, group.loc[row.name]) if pd.notna(row['lat']) else 0, axis=1)
    return group

# Load the dataset in chunks
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data.csv'
chunk_size = 500000  # Adjust the chunk size based on your system's performance
chunks = pd.read_csv(file_path, chunksize=chunk_size)

output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_with_distance_chunked.csv'

# Process each chunk
with open(output_file, 'w') as f_out:
    for chunk_num, chunk in enumerate(chunks):
        print(f"Processing chunk {chunk_num + 1}...")
        
        # Ensure the 'times' column is correctly parsed
        chunk['parsed_times'] = pd.to_datetime(chunk['times'], errors='coerce')
        
        # Group by 'tag' and apply the distance calculation
        chunk = chunk.groupby('tag', group_keys=False).apply(calc_distances)
        
        # Write the chunk to the output file
        if chunk_num == 0:
            chunk.to_csv(f_out, index=False)  # Write header in the first chunk
        else:
            chunk.to_csv(f_out, index=False, header=False)  # Append without header

        print(f"Chunk {chunk_num + 1} processed and saved.")

print(f"Filtered dataset with distances saved to {output_file}")
