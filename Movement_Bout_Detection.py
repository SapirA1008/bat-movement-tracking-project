import pandas as pd

# Load the validated data (after outliers are filtered)
file_path = 'valid_data.csv'  # Replace with your actual file path
valid_data = pd.read_csv(file_path)

# Parameters for movement and stationary detection
MOVEMENT_THRESHOLD = 0.5  # Speed above this is considered movement
STATIONARY_THRESHOLD = 0.1  # Speed below this is considered stationary
MIN_BOUT_LENGTH = 5  # Minimum number of consecutive points to be considered a bout

# Step 1: Classify movement and stationary points
valid_data['movement_status'] = valid_data['speed'].apply(
    lambda x: 'movement' if x > MOVEMENT_THRESHOLD else 'stationary')

# Step 2: Group consecutive movement or stationary points into bouts
valid_data['bout_id'] = (valid_data['movement_status'] != valid_data['movement_status'].shift()).cumsum()

# Step 3: Filter out short bouts (e.g., less than MIN_BOUT_LENGTH points)
valid_bouts = valid_data.groupby('bout_id').filter(lambda x: len(x) >= MIN_BOUT_LENGTH)

# Step 4: Analyze the bouts (you can explore foraging patterns, roosting, etc.)
movement_bouts = valid_bouts[valid_bouts['movement_status'] == 'movement']
stationary_bouts = valid_bouts[valid_bouts['movement_status'] == 'stationary']

# Save the bouts to CSV
movement_bouts.to_csv('movement_bouts.csv', index=False)
stationary_bouts.to_csv('stationary_bouts.csv', index=False)

# Summary
print(f"Movement bouts: {len(movement_bouts)}")
print(f"Stationary bouts: {len(stationary_bouts)}")
