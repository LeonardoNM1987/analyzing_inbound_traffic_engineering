# ESSE CODIGO DEPENDE DA EXECUÇÃO ANTERIOR DO 'MORESPECIFIC_ASES_DETAILS.PY'

import os
import glob


def compile_results(input_dir, output_path):
    """Compiles results from individual files into a single summary file."""
    compiled_data = {}
    
    input_files = glob.glob(os.path.join(input_dir, 'v4_moreSpecific_ases_details_*.txt'))
    
    for input_file in input_files:
        date_part = os.path.basename(input_file).split('_')[-1].replace('.txt', '')
        print(f'Processando {date_part}...')
        with open(input_file, 'r') as file:
            next(file)  # Skip header
            for line in file:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                region = parts[1]
                use_more_specific = parts[4]
                #as_type = parts[3]
                if region not in compiled_data:
                    compiled_data[region] = {}
                
                if date_part not in compiled_data[region]:
                    compiled_data[region][date_part] = {'observed_ases': 0, 'use_moreSpecific': 0}
                
                compiled_data[region][date_part]['observed_ases'] += 1
                if use_more_specific == 'yes':
                    compiled_data[region][date_part]['use_moreSpecific'] += 1

                # Atualizar dados para a região 'internet'
                if 'internet' not in compiled_data:
                    compiled_data['internet'] = {}
                if date_part not in compiled_data['internet']:
                    compiled_data['internet'][date_part] = {'observed_ases': 0, 'use_moreSpecific': 0}
                
                compiled_data['internet'][date_part]['observed_ases'] += 1
                if use_more_specific == 'yes':
                    compiled_data['internet'][date_part]['use_moreSpecific'] += 1
    
    with open(output_path, 'w') as out_file:
        out_file.write('region|date|observed_ases|use_moreSpecific|moreSpecific_fraction\n')
        for region, dates in compiled_data.items():
            for date, counts in dates.items():
                more_specific_fraction = (counts['use_moreSpecific'] / counts['observed_ases'] * 100) if counts['observed_ases'] > 0 else 0
                out_file.write(f"{region}|{date}|{counts['observed_ases']}|{counts['use_moreSpecific']}|{more_specific_fraction:.2f}\n")


# Paths

output_dir_deploy = '08-more_specific_results/v4/ases_details/'
output_path_compile = '19-preparing_data_for_plot/v4/more_specific_deploy_regions.txt'

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path_compile), exist_ok=True)

# Process all files in the input directory
compile_results(output_dir_deploy, output_path_compile)
