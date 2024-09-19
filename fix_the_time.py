import pandas as pd

# Load the dataset
file_path = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data.csv'
data = pd.read_csv(file_path)

# Custom function to parse both MM/DD/YYYY and DD/MM/YYYY formats
def parse_mixed_date(date_str):
    try:
        # Try parsing the date as MM/DD/YYYY first
        return pd.to_datetime(date_str, format='%m/%d/%Y %H:%M', errors='coerce')
    except:
        # If it fails, try parsing as DD/MM/YYYY
        return pd.to_datetime(date_str, format='%d/%m/%Y %H:%M', errors='coerce')

# Apply the custom date parsing function in one pass
print("Starting unified date parsing...")
data['times'] = data['times'].apply(parse_mixed_date)

# Check progress for large datasets
for index in range(len(data)):
    if index % 500000 == 0:
        print(f"Processed {index} rows...")

# Check for any unparsed dates (NaT values)
missing_dates = data[data['times'].isna()]

# Save rows with missing dates (if any) for further inspection
if not missing_dates.empty:
    missing_output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\missing_times.csv'
    missing_dates.to_csv(missing_output_file, index=False)
    print(f"Missing dates saved to {missing_output_file}")
else:
    print("All dates successfully converted.")

# Save the cleaned data with corrected times
output_file = r'C:\Users\sapir\OneDrive\Desktop\Project\132_rawtable\merged_bat_data_cleaned.csv'
data.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
