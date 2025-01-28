import os
import glob
import pandas as pd

# Define the categories
categories = {
    'from1to24': (0.1, 24.9),
    'from25to49': (25.0, 49.9),
    'from50to74': (50.0, 74.9),
    'from75to99': (75.0, 99.9)
}

# Initialize the result dictionary
results = {}

# Path to the folder containing the text files
input_folder_path = '08-more_specific_results/v4/ases_details/'
output_file_path = '19-preparing_data_for_plot/v4/moreSpecific_proportion_types.txt'

# Process each file
for file_path in glob.glob(os.path.join(input_folder_path, 'v4_moreSpecific_ases_details_*.txt')):
    date = os.path.basename(file_path).split('_')[-1].split('.')[0]
    print(f'Analisando {date}....')
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('|')
            asn, region, country, as_type, use_moreSpecific, announced_prefixes, moreSpecific_prefixes, moreSpecific_proportion_usage, announced_prefixes_list = parts
            if as_type in {"NA", "inactive"}:
                continue
            if use_moreSpecific == 'yes' and as_type in {"business", "education", "government", "hosting", "isp", "none"}:
                moreSpecific_proportion_usage = float(moreSpecific_proportion_usage)
                for categ, (lower, upper) in categories.items():
                    if lower <= moreSpecific_proportion_usage <= upper:
                        if as_type not in results:
                            results[as_type] = {}
                        if date not in results[as_type]:
                            results[as_type][date] = {c: 0 for c in categories.keys()}
                        results[as_type][date][categ] += 1

# Prepare the final output
output_data = []

# Add individual types
for as_type, dates in results.items():
    for date, counts in dates.items():
        output_data.append([as_type, date] + [counts[c] for c in categories.keys()])

# Calculate the 'internet' as_type
internet_totals = {}
for date in {date for dates in results.values() for date in dates}:
    internet_totals[date] = {c: 0 for c in categories.keys()}
    for as_type, dates in results.items():
        if date in dates:
            for categ in categories.keys():
                internet_totals[date][categ] += dates[date][categ]
for date, counts in internet_totals.items():
    output_data.append(['internet', date] + [counts[c] for c in categories.keys()])

# Sort the output data by date
output_data.sort(key=lambda x: (x[0], x[1]))

# Convert to TXT format and save the result
with open(output_file_path, 'w') as f_out:
    f_out.write('#as_type|date|' + '|'.join(categories.keys()) + '\n')
    for row in output_data:
        f_out.write('|'.join(map(str, row)) + '\n')

print("Process completed successfully.")
