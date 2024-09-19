import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import random

# Load the interaction data
interaction_data = pd.read_csv("social_interactions_filtered.csv")

# Step 1: Calculate the observed number of interactions
observed_interactions = len(interaction_data)

# Step 2: Function to shuffle the data and calculate random interactions
def shuffle_interactions(data, n_iterations=1000):
    random_interactions = []
    
    for _ in range(n_iterations):
        shuffled_data = data.copy()
        # Shuffle lat, lon, and times to simulate random movement
        shuffled_data['lat'] = np.random.permutation(shuffled_data['lat'].values)
        shuffled_data['lon'] = np.random.permutation(shuffled_data['lon'].values)
        shuffled_data['parsed_times'] = np.random.permutation(shuffled_data['parsed_times'].values)
        
        # Calculate the random interactions in the shuffled data
        random_interactions.append(detect_social_interactions(shuffled_data).shape[0])
    
    return random_interactions

# Step 3: Run the shuffle to get the distribution of random interactions
random_interactions_distribution = shuffle_interactions(interaction_data, n_iterations=1000)

# Step 4: Calculate the p-value from the permutation test
p_value = (np.sum(np.array(random_interactions_distribution) >= observed_interactions) / 1000)
print(f"P-value from permutation test: {p_value}")

# Step 5: Perform chi-square goodness-of-fit test
# Observed: number of real interactions
# Expected: mean of random interactions
expected_interactions = np.mean(random_interactions_distribution)
observed_vs_expected = np.array([observed_interactions, expected_interactions])

chi2, p_chi, dof, expected = chi2_contingency([observed_vs_expected])
print(f"Chi-square statistic: {chi2}, P-value: {p_chi}")

# Step 6: Conclusion based on p-value
if p_value < 0.05:
    print("The observed groupings are significantly more frequent than random, indicating social behavior.")
else:
    print("The observed groupings are not significantly different from random, suggesting no social behavior.")
