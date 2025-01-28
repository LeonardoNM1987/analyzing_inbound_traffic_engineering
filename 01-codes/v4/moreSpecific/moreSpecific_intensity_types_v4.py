import os
import pytricia
from collections import defaultdict
import ipaddress

def prefix_length_difference(parent_prefix, child_prefix):
    """Calcula a diferença de nível entre um prefixo pai e um prefixo filho."""
    return ipaddress.ip_network(child_prefix).prefixlen - ipaddress.ip_network(parent_prefix).prefixlen

def analyze_prefix_disaggregation(input_directory, output_filepath):
    results = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))  # {region: {date: [disagg_1, disagg_2, disagg_3, disagg_4plus]}}

    for filename in os.listdir(input_directory):
        if filename.startswith("v4_moreSpecific_ases_details_") and filename.endswith(".txt"):
            date = filename.split('_')[-1].split('.')[0]
            filepath = os.path.join(input_directory, filename)
            print(f'Analisando {date}..')
            with open(filepath, 'r') as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    parts = line.strip().split('|')
                    asn, region, country, as_type, use_moreSpecific, announced_prefixes, moreSpecific_prefixes, moreSpecific_proportion_usage, announced_prefixes_list = parts
                    if as_type in {"NA", "inactive"} or use_moreSpecific != 'yes':
                        continue

                    prefixes = announced_prefixes_list.split(',')
                    trie = pytricia.PyTricia()
                    for prefix in prefixes:
                        trie.insert(prefix, prefix)

                    max_disagg_level = 0
                    for prefix in prefixes:
                        subprefixes = list(trie.children(prefix))
                        for subprefix in subprefixes:
                            diff = prefix_length_difference(prefix, subprefix)
                            if diff > max_disagg_level:
                                max_disagg_level = diff

                    if max_disagg_level == 0:
                        results[as_type][date][0] += 1
                    elif max_disagg_level == 1:
                        results[as_type][date][0] += 1
                    elif max_disagg_level == 2:
                        results[as_type][date][1] += 1
                    elif max_disagg_level == 3:
                        results[as_type][date][2] += 1
                    else:
                        results[as_type][date][3] += 1

    with open(output_filepath, 'w') as output_file:
        output_file.write("#as_type|date|disagg_1|disagg_2|disagg_3|disagg_4plus\n")
        for as_type, dates in sorted(results.items()):
            for date, counts in sorted(dates.items()):
                output_file.write(f"{as_type}|{date}|{counts[0]}|{counts[1]}|{counts[2]}|{counts[3]}\n")

    print(f"Resultados salvos em {output_filepath}")

    # Calculating "internet" totals
    internet_totals = defaultdict(lambda: [0, 0, 0, 0])
    for as_type, dates in results.items():
        for date, counts in dates.items():
            internet_totals[date][0] += counts[0]
            internet_totals[date][1] += counts[1]
            internet_totals[date][2] += counts[2]
            internet_totals[date][3] += counts[3]

    with open(output_filepath, 'a') as output_file:
        for date, counts in sorted(internet_totals.items()):
            output_file.write(f"internet|{date}|{counts[0]}|{counts[1]}|{counts[2]}|{counts[3]}\n")

# Directory containing the input files
input_directory = '08-more_specific_results/v4/ases_details/'

# Output file path
output_filepath = '19-preparing_data_for_plot/v4/moreSpecific_intensity_types.txt'

analyze_prefix_disaggregation(input_directory, output_filepath)
