import pandas as pd
from sklearn.cluster import DBSCAN

# Load the stationary bouts data
bat_data = pd.read_csv('stationary_bouts.csv')  # Replace with your actual file path

# Perform DBSCAN clustering to generate 'location_cluster' based on 'lat' and 'lon'
coords = bat_data[['lat', 'lon']].values
dbscan = DBSCAN(eps=0.0005, min_samples=3).fit(coords)
bat_data['location_cluster'] = dbscan.labels_

# Now group by 'location_cluster' and 'parsed_times'
grouped = bat_data.groupby(['location_cluster', 'parsed_times'])

# Filter groups with more than one unique bat tag to detect social interactions
social_interactions = grouped.filter(lambda x: x['tag'].nunique() > 1)

# Save the social interactions to a CSV file
social_interactions.to_csv('social_interactions.csv', index=False)

# Print the number of detected social interactions
print(f"Detected social interactions between bats. Total interactions: {len(social_interactions)}")
