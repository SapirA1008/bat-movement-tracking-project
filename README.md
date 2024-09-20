Bat Movement Tracking Project
Project Description
The Bat Movement Tracking Project analyzes GPS tracking data collected from bats using the ATLAS system. The primary objective is to explore the movement patterns, foraging habits, roosting locations, and potential social interactions of bats. The project aims to develop algorithms that can differentiate between movement and stationary bouts, identify frequent roosting and foraging locations, and detect possible social interactions between bats based on proximity.

This project is crucial for understanding the ecological behavior of bats, including how they use their environment and interact with each other. These insights can aid conservation efforts and further the scientific study of bat species and their habitat usage.

Key Features:
GPS Data Analysis: Processing high-resolution GPS tracking data to study bat movement.
Roosting and Foraging Identification: Identifying habitual locations for roosting and foraging.
Social Interaction Detection: Detecting proximity-based social interactions between bats.
Data Clustering: Using DBSCAN and KMeans algorithms to cluster bat movement data and identify patterns.
Installation and Setup Instructions
Prerequisites:
Python 3.8 or above
A terminal or command line interface (CLI)
Git for cloning the repository
Required Libraries:
Ensure that the following Python libraries are installed:

pandas
numpy
scikit-learn
folium
matplotlib
You can install these dependencies by running the following command:
pip install -r requirements.txt

Setup and Run Instructions:
Clone the repository: First, clone the project repository to your local machine using Git:

git clone https://github.com/SapirA1008/bat-movement-tracking-project.git
Navigate to the project folder: Once the repository is cloned, move into the project directory:
cd bat-movement-tracking-project

Install the dependencies: To install all the required libraries, run:
pip install -r requirements.txt

Preprocess the Bat Data: Before running any analysis, clean and preprocess the raw bat GPS data using the following script:
python data_cleaning.py

Running the Analysis Scripts:
1. Roosting and Foraging Location Identification:
To identify frequent roosting and foraging locations based on the GPS data, run the following script:


python Identifying_Roosting_Locations.py
The results, including visual maps, will be saved to the results/maps/ directory.

2. Social Interaction Detection:
To detect social interactions between bats based on GPS data proximity, use:

python Social_Interaction_Analysis.py
This will output interaction logs, indicating when and where bats were near each other, suggesting possible social behavior.

3. Statistical Validation of Social Groupings:
To apply statistical tests and determine whether the social groupings detected are significant or random, run:

python Statistical_Tests.py
Output Files:
results/roosting_locations.csv: Contains the identified roosting and foraging clusters.
results/social_interactions.csv: Logs detailing detected social interactions between bats.
results/maps/: Contains maps showing roosting and foraging clusters.
