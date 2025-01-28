import os
import csv
from collections import Counter

def count_unique_cidrs(file_path):
    cidrs = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Ignorar linhas de cabeçalho ou vazias
            if line.startswith("#") or not line.strip():
                continue
            
            # Extrair o campo do prefixo
            prefix = line.split('|')[0]
            
            # Obter o CIDR (parte depois da barra)
            if '/' in prefix:
                cidr = prefix.split('/')[1]
                cidrs.append(cidr)

    # Contar CIDRs únicos
    unique_cidrs = Counter(cidrs)

    # Ordenar os CIDRs numericamente
    sorted_cidrs = sorted(unique_cidrs.items(), key=lambda x: int(x[0]))
    
    return sorted_cidrs

def process_multiple_files(output_csv, base_path):
    # Cabeçalho do CSV
    all_results = {}

    for year in range(2014, 2025):
        for month in range(1, 13):
            # Formatar o caminho do arquivo
            month_str = str(month).zfill(2)
            file_name = f"v6_prefixes_policies_complete_{year}{month_str}15.txt"
            file_path = os.path.join(base_path, file_name)
            print(f'Analisando {file_name}...')
            if not os.path.exists(file_path):
                print(f"Arquivo não encontrado: {file_path}")
                continue

            # Contar os CIDRs no arquivo
            cidr_counts = count_unique_cidrs(file_path)

            # Salvar os resultados na estrutura
            for cidr, count in cidr_counts:
                if cidr not in all_results:
                    all_results[cidr] = {}
                all_results[cidr][f"{year}-{month_str}"] = count

    # Criar o CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Cabeçalho do CSV
        header = ["CIDR"] + [f"{year}-{str(month).zfill(2)}" for year in range(2014, 2025) for month in range(1, 13)]
        writer.writerow(header)

        # Escrever os dados
        for cidr, data in sorted(all_results.items(), key=lambda x: int(x[0])):
            row = [f"/{cidr}"] + [data.get(f"{year}-{str(month).zfill(2)}", 0) for year in range(2014, 2025) for month in range(1, 13)]
            writer.writerow(row)

# Configuração
base_path = "05-prefixes_policies_regions_and_types_saned/v6_prefixes"
output_csv = "cidr_counts_by_date.csv"
process_multiple_files(output_csv, base_path)


#file_path = "05-prefixes_policies_regions_and_types_saned/v6_prefixes/v6_prefixes_policies_complete_20240615.txt"