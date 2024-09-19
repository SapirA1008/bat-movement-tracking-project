import pandas as pd

# Load the CSV file
frequent_clusters = pd.read_csv('frequent_roosting_locations.csv')

# Print the column names
print(frequent_clusters.columns)
