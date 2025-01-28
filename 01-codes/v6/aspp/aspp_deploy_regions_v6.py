import os
from collections import defaultdict



def process_file(file_path, region):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    total_asns = 0
    prepend_count = 0
    
    for line in lines:
        if line.strip() and not line.startswith("#"):
            fields = line.strip().split('|')
            if len(fields) > 4 and fields[2] == region:
                observed_prepends = fields[6].split(';')
                total_asns += 1
                if any(int(prepend) > 0 for prepend in observed_prepends):
                    prepend_count += 1
    
    return total_asns, prepend_count

def main():
    input_directory = f'06-ases_policies/v6_ases'
    output_directory = f'19-preparing_data_for_plot/v6/aspp'
    regions = ['afrinic', 'arin', 'apnic', 'lacnic', 'ripencc']
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Dicionário para acumular os dados de cada região e da região 'internet'
    region_data = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    internet_data = defaultdict(lambda: [0, 0])
    
    output_file = os.path.join(output_directory, f'aspp_deploy_regions.txt')
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            date_str = filename.split('_')[-1].split('.')[0]
            print(f'Calculando {date_str}...')
            
            for region in regions:
                file_path = os.path.join(input_directory, filename)
                total_asns, prepend_count = process_file(file_path, region)
                
                region_data[region][date_str][0] += total_asns
                region_data[region][date_str][1] += prepend_count
                
                # Atualizando os valores para a região 'internet'
                internet_data[date_str][0] += total_asns
                internet_data[date_str][1] += prepend_count
    
    # Escrevendo os dados no arquivo de saída
    with open(output_file, 'w') as outfile:
        outfile.write("#region|date|observed_ases|use_aspp\n")
        
        for region in regions:
            for date_str, (total_asns, prepend_count) in sorted(region_data[region].items()):
                outfile.write(f"{region}|{date_str}|{total_asns}|{prepend_count}\n")
        
        # Escrevendo os dados da região 'internet'
        for date_str, (total_asns, prepend_count) in sorted(internet_data.items()):
            outfile.write(f"internet|{date_str}|{total_asns}|{prepend_count}\n")

if __name__ == "__main__":
    main()
