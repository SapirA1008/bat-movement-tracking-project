import folium
import pandas as pd

# Load the frequent roosting/foraging locations with lat and lon
frequent_clusters = pd.read_csv('frequent_roosting_locations.csv')

# Create a map centered on the average coordinates
bat_map = folium.Map(location=[frequent_clusters['lat'].mean(), frequent_clusters['lon'].mean()], zoom_start=12)

# Add each cluster as a marker on the map
for index, row in frequent_clusters.iterrows():
    folium.Marker([row['lat'], row['lon']], 
                  popup=f"Cluster {row['location_cluster']}, Visits: {row['visits']}").add_to(bat_map)

# Save the map to an HTML file
bat_map.save('bat_roosting_locations.html')

print("Map created and saved as 'bat_roosting_locations.html'")
