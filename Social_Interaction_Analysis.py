import pandas as pd
from datetime import timedelta

# Load data in smaller chunks
filename = 'bat_data_with_dbscan_clusters.csv'
chunk_size = 10000  # Adjust the chunk size to balance memory and speed

# Set a time threshold for social interactions (e.g., 5 minutes)
time_threshold = timedelta(minutes=5)

# Initialize an empty DataFrame to store interactions
all_interactions = pd.DataFrame()

# Function to detect social interactions within a chunk
def detect_social_interactions(chunk):
    chunk['parsed_times'] = pd.to_datetime(chunk['parsed_times'], format="%Y-%m-%d %H:%M:%S")
    
    # Filter out noise (cluster = -1)
    valid_data = chunk[chunk['cluster'] != -1]

    # Initialize a list to store interactions
    interactions = []

    # Group the data by cluster
    for cluster_id, cluster_data in valid_data.groupby('cluster'):
        cluster_data = cluster_data.sort_values(by='parsed_times')
        
        # Compare each bat with the next one in the sorted list
        for i in range(len(cluster_data) - 1):
            row1 = cluster_data.iloc[i]
            row2 = cluster_data.iloc[i + 1]
            
            # Only consider interactions between different bats
            if row1['tag'] != row2['tag']:
                # Check if time difference is within the threshold
                if abs(row1['parsed_times'] - row2['parsed_times']) <= time_threshold:
                    interaction = {
                        'bat_1': row1['tag'],
                        'bat_2': row2['tag'],
                        'cluster': cluster_id,
                        'time_diff': abs(row1['parsed_times'] - row2['parsed_times']),
                        'bat_1_time': row1['parsed_times'],
                        'bat_2_time': row2['parsed_times'],
                        'bat_1_lat': row1['lat'],
                        'bat_1_lon': row1['lon'],
                        'bat_2_lat': row2['lat'],
                        'bat_2_lon': row2['lon']
                    }
                    interactions.append(interaction)

    return pd.DataFrame(interactions)

# Read the dataset in chunks and process each one
for chunk in pd.read_csv(filename, chunksize=chunk_size):
    chunk_interactions = detect_social_interactions(chunk)
    all_interactions = pd.concat([all_interactions, chunk_interactions], ignore_index=True)

# Removing duplicate interactions (bat_1, bat_2) and vice versa
all_interactions['pair'] = all_interactions.apply(lambda row: tuple(sorted([row['bat_1'], row['bat_2']])), axis=1)
all_interactions = all_interactions.drop_duplicates(subset=['pair', 'cluster'], keep='first')
all_interactions = all_interactions.drop(columns=['pair'])

# Save the detected interactions to a CSV file
all_interactions.to_csv('social_interactions_filtered.csv', index=False)

print("Social interaction analysis completed. Results saved to 'social_interactions_filtered.csv'")
