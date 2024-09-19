import pandas as pd

# Load the dataset
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data.csv'
data = pd.read_csv(file_path)

# Step 1: Try parsing with dayfirst=True (DD/MM/YYYY)
print("Starting first pass date parsing (dayfirst=True)...")
data['parsed_times'] = pd.to_datetime(data['times'], errors='coerce', dayfirst=True)

# Step 2: For rows that are still missing, try parsing with dayfirst=False (MM/DD/YYYY)
missing_dates = data['parsed_times'].isna().sum()
if missing_dates > 0:
    print(f"Rows with missing 'parsed_times' after first pass: {missing_dates}")
    print("Starting second pass date parsing (dayfirst=False)...")
    unparsed = data['parsed_times'].isna()
    data.loc[unparsed, 'parsed_times'] = pd.to_datetime(data.loc[unparsed, 'times'], errors='coerce', dayfirst=False)

# Step 3: Handle the `DD-MMM-YYYY HH:MM:SS` format (e.g., '06-Sep-2023 00:32:18')
missing_dates_after_second_pass = data['parsed_times'].isna().sum()
if missing_dates_after_second_pass > 0:
    print(f"Rows with missing 'parsed_times' after second pass: {missing_dates_after_second_pass}")
    print("Starting third pass for 'DD-MMM-YYYY HH:MM:SS' format...")
    unparsed = data['parsed_times'].isna()
    data.loc[unparsed, 'parsed_times'] = pd.to_datetime(data.loc[unparsed, 'times'], errors='coerce', format='%d-%b-%Y %H:%M:%S')

# Step 4: Track the remaining missing values
missing_dates_after_third_pass = data['parsed_times'].isna().sum()
print(f"Rows with missing 'parsed_times' after third pass: {missing_dates_after_third_pass}")

# Save the rows with unparsed dates if any still remain
if missing_dates_after_third_pass > 0:
    missing_output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\missing_times_after_third_pass.csv'
    data[data['parsed_times'].isna()].to_csv(missing_output_file, index=False)
    print(f"Unparsed dates saved to {missing_output_file}")
else:
    print("All dates successfully parsed.")

# Step 5: Save the cleaned dataset with parsed times
output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data_cleaned.csv'
data.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
