


"""

import os
from ipaddress import ip_network
import datetime

def disaggregate_to_48(prefix):
    #Disaggregate a given prefix into /48s.
    network = ip_network(prefix)
    if network.prefixlen >= 48:
        return [str(network)]
    return [str(subnet) for subnet in network.subnets(new_prefix=48)]

def analyze_selective_announcement(input_line):
    # Split the line into the AS origin and the prefix details
    origin_as, region, country, as_type, prefixes = input_line.split('|')
    # Parse the prefixes and their respective neighbors
    prefix_neighbors = {}
    for prefix_info in prefixes.split(';'):
        if '(' not in prefix_info or ')' not in prefix_info:
            continue  # Skip invalid entries
        prefix, neighbors = prefix_info.split('(')
        neighbors = neighbors.rstrip(')').split(',')
        prefix_neighbors[prefix] = set(neighbors)

    # Collect all unique neighbors
    all_neighbors = set()
    for neighbors in prefix_neighbors.values():
        all_neighbors.update(neighbors)

    # Check for selective announcements
    selective_prefixes = 0
    selective_neighbors = set()
    visibility_48 = {}

    for prefix, neighbors in prefix_neighbors.items():
        if neighbors != all_neighbors:
            selective_prefixes += 1
            selective_neighbors.update(all_neighbors - neighbors)

        # Disaggregate prefix into /48 and track their visibility
        disaggregated_prefixes = disaggregate_to_48(prefix)
        for subprefix in disaggregated_prefixes:
            if subprefix not in visibility_48:
                visibility_48[subprefix] = set()
            visibility_48[subprefix].update(neighbors)

    use_selective = selective_prefixes > 0

    # Metrics for AS-level proportionality and intensity
    total_48s = len(visibility_48)
    selective_48s = sum(1 for neighbors in visibility_48.values() if len(neighbors) < len(all_neighbors))
    as_proportionality = selective_48s / total_48s if total_48s > 0 else 0

    # Metrics for per-/48 intensity
    intensities = [len(neighbors) / len(all_neighbors) for neighbors in visibility_48.values()]
    median_intensity = sorted(intensities)[len(intensities) // 2] if intensities else 0

    # Construct the output
    output = f"{origin_as}|{region}|{country}|{as_type}|{use_selective}|{selective_prefixes}|{len(selective_neighbors)}|{as_proportionality:.2f}|{median_intensity:.2f}"
    return output

def process_input_files(input_dir, output_dir, start_year, end_year, start_month=1, end_month=12):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    fixed_day = "15"  # Dia fixo para os arquivos
    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            date = f"{year}{month:02}{fixed_day}"
            input_file = f"v6_prefix_origin_complete_{date}.txt"
            input_path = os.path.join(input_dir, input_file)
            output_file = f"v6_selective_announc_result_{date}.txt"
            output_path = os.path.join(output_dir, output_file)

            if not os.path.exists(input_path):
                print(f"Input file not found: {input_path}. Skipping.")
                continue

            print(f"Processing file: {input_file} -> {output_file}")
            inicioArquivo = datetime.datetime.now()

            try:
                with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
                    # Write header to output file
                    outfile.write('#origin_as|region|country|as_type|use_selective|selective_prefixes|selective_neighbors|selective_proportion|median_intensity\n')
                    for line in infile:
                        line = line.strip()
                        if line and line[0] != '#':  # Skip empty lines and comments
                            try:
                                result = analyze_selective_announcement(line)
                                outfile.write(result + '\n')
                            except Exception as e:
                                print(f"Error processing line: {line[0].strip('|')}. Error: {e}")
            except Exception as e:
                print(f"Error processing file: {input_path}. Error: {e}")

            fimArquivo = datetime.datetime.now()
            tempo_execucao_parcial = fimArquivo - inicioArquivo
            print(f"Arquivo concluído: {str(tempo_execucao_parcial).split('.')[0]}")
            print("---------------------------------------------------")

# Main
if __name__ == "__main__":
    inicioTotal = datetime.datetime.now()

    # Configurar intervalo de datas
    start_month = 1    # Mês inicial
    start_year = 2014  # Ano inicial
    end_month = 12      # Mês final
    end_year = 2024    # Ano final

    # Diretórios de entrada e saída
    input_directory = '10-selective_announcement_regions_and_types_saned/v6'  # Diretório de entrada
    output_directory = '11-selective_announcement_results/v6'  # Diretório de saída

    # Processar os arquivos no intervalo definido
    process_input_files(input_directory, output_directory, start_year, end_year, start_month, end_month)

    fimTotal = datetime.datetime.now()
    tempo_execucao_total = fimTotal - inicioTotal
    print(f"Tempo de execução total das análises: {str(tempo_execucao_total).split('.')[0]}")
"""