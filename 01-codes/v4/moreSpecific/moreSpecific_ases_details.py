import pytricia
import os
import glob


def parse_line(line):
    """Parses a line from the input file."""
    parts = line.strip().split('|')
    if len(parts) < 6 or parts[3] == 'None':
        return None
    return {
        'prefix': parts[0],
        'origin': parts[1],
        'region': parts[3],
        'country': parts[4],
        'as_type': parts[5]
    }

def process_file(input_path, output_path):
    """Processes the input file and generates the output."""
    asn_data = {}
    
    with open(input_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue  # Skip header
            data = parse_line(line)
            if data:
                asn = data['origin']
                prefix = data['prefix']
                region = data['region']
                country = data['country']
                as_type = data['as_type']
                
                if asn not in asn_data:
                    asn_data[asn] = {
                        'region': region,
                        'country': country,
                        'prefixes': [],
                        'pytrie': pytricia.PyTricia(128),
                        'as_type': as_type
                    }
                
                asn_data[asn]['prefixes'].append(prefix)
                asn_data[asn]['pytrie'].insert(prefix, None)
    
    with open(output_path, 'w') as out_file:
        out_file.write('#asn|region|country|as_type|use_moreSpecific(yes;no)|announced_prefixes|moreSpecific_prefixes|moreSpecific_proportion_usage|announced_prefixes(list)\n')
        
        for asn, data in asn_data.items():
            use_more_specific = 'no'
            more_specific_count = 0
            for prefix in data['prefixes']:
                if list(data['pytrie'].children(prefix)):
                    use_more_specific = 'yes'
                    more_specific_count += 1
            
            announced_count = len(data['prefixes'])
            more_specific_proportion = (more_specific_count / announced_count) * 100 if announced_count > 0 else 0
            out_file.write(f"{asn}|{data['region']}|{data['country']}|{data['as_type']}|{use_more_specific}|{announced_count}|{more_specific_count}|{more_specific_proportion:.2f}|{','.join(data['prefixes'])}\n")

def process_all_files(input_dir, output_dir):
    """Processes all files in the input directory and generates corresponding output files."""
    os.makedirs(output_dir, exist_ok=True)
    input_files = glob.glob(os.path.join(input_dir, 'v4_prefixes_policies_*.txt'))
    
    for input_file in input_files:
        date_part = os.path.basename(input_file).split('_')[-1].replace('.txt', '')
        print(f'Analisando {date_part}...')
        output_file = os.path.join(output_dir, f'v4_moreSpecific_ases_details_{date_part}.txt')
        process_file(input_file, output_file)

# Paths
input_dir = f'05-prefixes_policies_regions_and_types_saned/v4_prefixes/'
output_dir = f'08-more_specific_results/v4/ases_details/'

# Process all files in the input directory
process_all_files(input_dir, output_dir)
