import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.cluster import DBSCAN

# Load data in chunks
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\cleaned_bat_data.csv'
print("Loading data in chunks...")

chunk_size = 100000  # Process 100,000 rows at a time
chunks = pd.read_csv(file_path, chunksize=chunk_size, low_memory=False)

filtered_chunks = []

for chunk in chunks:
    print(f"Processing chunk with {len(chunk)} rows...")
    
    # Apply moving average
    chunk['lat_smoothed'] = chunk['lat'].rolling(window=5).mean()
    chunk['lon_smoothed'] = chunk['lon'].rolling(window=5).mean()
    
    # Drop rows with NaN values
    chunk = chunk.dropna(subset=['lat_smoothed', 'lon_smoothed'])
    
    # Vectorized distance calculation
    coords = list(zip(chunk['lat_smoothed'], chunk['lon_smoothed']))
    chunk['distance_moved'] = [geodesic(coords[i], coords[i-1]).meters if i > 0 else np.nan for i in range(len(coords))]
    
    # Movement classification
    movement_threshold = 5  # meters
    chunk['is_moving'] = chunk['distance_moved'] > movement_threshold
    
    # Append processed chunk to list
    filtered_chunks.append(chunk)
    print(f"Chunk processed. Total processed rows: {sum([len(c) for c in filtered_chunks])}")

# Concatenate all processed chunks
filtered_data = pd.concat(filtered_chunks)

# Save filtered data
output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\filtered_bat_data_chunked.csv'
filtered_data.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
