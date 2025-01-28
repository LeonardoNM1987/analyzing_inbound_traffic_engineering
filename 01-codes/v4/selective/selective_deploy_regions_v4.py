import os
from collections import defaultdict



def process_file(file_path, region):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    total_asns = 0
    selective_count = 0
    
    for line in lines:
        if line.startswith("#"):
            continue        
        #fields = line.strip().split('|')
        fields = line.split('|') 
        if len(fields) > 4 and fields[1] == region:
            use_selective = fields[4]
            total_asns += 1
            if use_selective == "True":
                selective_count += 1
    
    return total_asns, selective_count

def main():
    input_directory = f'11-selective_announcement_results/v4'
    output_directory = f'19-preparing_data_for_plot/v4'
    regions = ['afrinic', 'arin', 'apnic', 'lacnic', 'ripencc']
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Dicionário para acumular os dados de cada região e da região 'internet'
    region_data = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    internet_data = defaultdict(lambda: [0, 0])
    
    output_file = os.path.join(output_directory, f'selective_deploy_regions.txt')
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            date_str = filename.split('_')[-1].split('.')[0]
            print(f'Calculando {date_str}...')
            
            for region in regions:
                file_path = os.path.join(input_directory, filename)
                total_asns, selective_count = process_file(file_path, region)
                
                region_data[region][date_str][0] += total_asns
                region_data[region][date_str][1] += selective_count
                
                # Atualizando os valores para a região 'internet'
                internet_data[date_str][0] += total_asns
                internet_data[date_str][1] += selective_count
    
    # Escrevendo os dados no arquivo de saída
    with open(output_file, 'w') as outfile:
        outfile.write("#region|date|total_ases|use_selective\n")
        
        for region in regions:
            for date_str, (total_asns, selective_count) in sorted(region_data[region].items()):
                outfile.write(f"{region}|{date_str}|{total_asns}|{selective_count}\n")
        
        # Escrevendo os dados da região 'internet'
        for date_str, (total_asns, selective_count) in sorted(internet_data.items()):
            outfile.write(f"internet|{date_str}|{total_asns}|{selective_count}\n")

if __name__ == "__main__":
    main()
