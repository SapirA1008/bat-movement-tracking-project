import pandas as pd
from sklearn.cluster import DBSCAN

# Load the stationary bouts data
stationary_bouts = pd.read_csv('stationary_bouts.csv')

# Use DBSCAN clustering to identify habitual locations (clusters of stationary points)
coords = stationary_bouts[['lat', 'lon']].values
clustering = DBSCAN(eps=0.001, min_samples=3).fit(coords)

# Add cluster labels to the data
stationary_bouts['location_cluster'] = clustering.labels_

# Filter out noise (label -1 means it's considered noise by DBSCAN)
stationary_clusters = stationary_bouts[stationary_bouts['location_cluster'] != -1]

# Analyze frequent locations (clusters with multiple visits)
frequent_clusters = stationary_clusters.groupby('location_cluster').agg({
    'lat': 'mean', 
    'lon': 'mean', 
    'location_cluster': 'size'
}).reset_index().rename(columns={'location_cluster': 'visits'})

# Save the frequent clusters with latitude and longitude
frequent_clusters.to_csv('frequent_roosting_locations.csv', index=False)

# Summary
print(f"Frequent roosting/foraging locations: {len(frequent_clusters)}")
