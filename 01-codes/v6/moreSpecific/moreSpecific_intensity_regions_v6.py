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
        if filename.startswith("v6_moreSpecific_ases_details_") and filename.endswith(".txt"):
            date = filename.split('_')[-1].split('.')[0]
            filepath = os.path.join(input_directory, filename)
            print(f'Analisando {date}...')
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    parts = line.strip().split('|')
                    asn, region, country, as_type, use_moreSpecific, announced_prefixes, moreSpecific_prefixes, moreSpecific_proportion_usage, announced_prefixes_list = parts
                    if region == 'None' or use_moreSpecific != 'yes':
                        continue

                    prefixes = [p.strip() for p in announced_prefixes_list.split(',') if p.strip()]
                    trie = pytricia.PyTricia(128)
                    for prefix in prefixes:
                        try:
                            ipaddress.IPv6Network(prefix)  # Validate IPv6 prefix
                            trie.insert(prefix, prefix)
                        except ValueError:
                            continue

                    max_disagg_level = 0
                    for prefix in prefixes:
                        subprefixes = list(trie.children(prefix))
                        for subprefix in subprefixes:
                            diff = prefix_length_difference(prefix, subprefix)
                            if diff > max_disagg_level:
                                max_disagg_level = diff

                    if max_disagg_level == 0:
                        results[region][date][0] += 1
                    elif max_disagg_level == 1:
                        results[region][date][0] += 1
                    elif max_disagg_level == 2:
                        results[region][date][1] += 1
                    elif max_disagg_level == 3:
                        results[region][date][2] += 1
                    else:
                        results[region][date][3] += 1

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write("#region|date|disagg_1|disagg_2|disagg_3|disagg_4plus\n")
        for region, dates in sorted(results.items()):
            for date, counts in sorted(dates.items()):
                output_file.write(f"{region}|{date}|{counts[0]}|{counts[1]}|{counts[2]}|{counts[3]}\n")

    print(f"Resultados salvos em {output_filepath}")

    # Calculating "internet" totals
    internet_totals = defaultdict(lambda: [0, 0, 0, 0])
    for region, dates in results.items():
        for date, counts in dates.items():
            internet_totals[date][0] += counts[0]
            internet_totals[date][1] += counts[1]
            internet_totals[date][2] += counts[2]
            internet_totals[date][3] += counts[3]

    with open(output_filepath, 'a', encoding='utf-8') as output_file:
        for date, counts in sorted(internet_totals.items()):
            output_file.write(f"internet|{date}|{counts[0]}|{counts[1]}|{counts[2]}|{counts[3]}\n")

# Directory containing the input files
input_directory = '08-more_specific_results/v6/ases_details/'

# Output file path
output_filepath = '19-preparing_data_for_plot/v6/moreSpecific/moreSpecific_intensity_regions.txt'

analyze_prefix_disaggregation(input_directory, output_filepath)
