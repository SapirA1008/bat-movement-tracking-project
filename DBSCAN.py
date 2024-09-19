import pandas as pd
from sklearn.cluster import DBSCAN

# Load the stationary bouts data
stationary_bouts = pd.read_csv('stationary_bouts.csv')

# Downsample the data to 10% to reduce memory usage (you can adjust this)
downsampled_stationary_bouts = stationary_bouts.sample(frac=0.1)

# Use DBSCAN clustering on the downsampled data
coords = downsampled_stationary_bouts[['lat', 'lon']].values
clustering = DBSCAN(eps=0.001, min_samples=3).fit(coords)

# Add cluster labels to the data
downsampled_stationary_bouts['location_cluster'] = clustering.labels_

# Filter out noise (label -1 means it's considered noise by DBSCAN)
stationary_clusters = downsampled_stationary_bouts[downsampled_stationary_bouts['location_cluster'] != -1]

# Group by location clusters and calculate mean lat/lon for each cluster
frequent_clusters = stationary_clusters.groupby('location_cluster').agg({
    'lat': 'mean', 
    'lon': 'mean', 
    'location_cluster': 'size'
})

# Reset the index without introducing the 'location_cluster' column again
frequent_clusters = frequent_clusters.rename(columns={'location_cluster': 'visits'}).reset_index()

# Save the frequent clusters with latitude and longitude
frequent_clusters.to_csv('frequent_roosting_locations.csv', index=False)

# Summary
print(f"Frequent roosting/foraging locations: {len(frequent_clusters)}")
