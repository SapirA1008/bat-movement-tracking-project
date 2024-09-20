Instructions for Running the Project
Prerequisites
Python 3.x installed on your system.

Install the required libraries by running the following command:
pip install -r requirements.txt
The requirements.txt file includes necessary dependencies such as pandas, scikit-learn, folium, matplotlib, numpy, joblib, and dask.

Running the Project
Data Preprocessing and Filtering:

The script separate_file.py processes the raw bat data and filters it into valid and invalid data based on speed and distance thresholds.
To run the script, use:
python separate_file.py
Detect Roosting and Foraging Locations:

Run the Identifying_Roosting_Locations.py script to cluster bat locations and detect potential roosting or foraging sites:
python Identifying_Roosting_Locations.py
The resulting clusters are saved, and frequent roosting locations are highlighted.
Social Interaction Detection:

To detect possible social interactions between bats, run the Social_Interaction_Analysis.py script:
python Social_Interaction_Analysis.py
This will identify instances where bats were in close proximity at the same time, indicating potential social interactions.
Visualize Roosting Locations:

To visualize the roosting locations on a map, run:
python Roosting_Locations_on_a_Map.py
Statistical Validation of Social Interactions:

Statistical tests can be applied to validate the social interactions. The Statistical_Tests.py script analyzes whether the detected groupings occur more frequently than expected by chance:
python Statistical_Tests.py

In this fulder (main branch) you can find all the cods that I needed for solving memory computer issue, marge data and trial codes.

In the script branch you will fing the scripts:
  # All scripts for data analysis
1. separate_file.py
2. Identifying_Roosting_Locations.py
3. Social_Interaction_Analysis.py
4. Roosting_Locations_on_a_Map.py
5. Statistical_Tests.py
