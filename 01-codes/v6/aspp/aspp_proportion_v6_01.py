import os
from collections import defaultdict

def process_file(file_path, output_path):
    asn_data = defaultdict(lambda: {'total_prefixes': 0, 'prepended_prefixes': 0, 'region': None, 'country': None, 'as_type': None})
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.strip() and not line.startswith("#"):
            fields = line.strip().split('|')
            if len(fields) == 8:
                prefix = fields[0]
                asn = fields[1]
                num_monitors = fields[2]
                region = fields[3]
                country = fields[4]
                as_type = fields[5]
                aspp_policy = fields[6]
                observed_prepends = fields[7]
                
                
                asn_data[asn]['total_prefixes'] += 1
                if any(int(prepend) != 0 for prepend in observed_prepends.split(';')):
                    asn_data[asn]['prepended_prefixes'] += 1
                if not asn_data[asn]['region']:
                    asn_data[asn]['region'] = region
                if not asn_data[asn]['country']:
                    asn_data[asn]['country'] = country
                if not asn_data[asn]['as_type']:
                    asn_data[asn]['as_type'] = as_type
    
    with open(output_path, 'w') as output_file:
        output_file.write('#asn|announced_prefixes|prepended_prefixes|region|country|as_type|prepend_percentage\n')
        for asn, data in asn_data.items():
            if data['prepended_prefixes'] > 0:
                prepend_percentage = (data['prepended_prefixes'] / data['total_prefixes']) * 100
                output_file.write(f"{asn}|{data['total_prefixes']}|{data['prepended_prefixes']}|{data['region']}|{data['country']}|{data['as_type']}|{prepend_percentage:.2f}\n")

def main():
    input_directory = '05-prefixes_policies_regions_and_types_saned/v6_prefixes/'
    output_directory = '07-aspp_results/v6/proportion/'
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.startswith('v6_prefixes_policies_complete_') and filename.endswith('.txt'):
            input_file = os.path.join(input_directory, filename)
            date = filename.split('_')[-1].split('.')[0]
            output_file = os.path.join(output_directory, f'v6_aspp_proportion_{date}.txt')
            
            print(f'Processing {input_file}...')
            process_file(input_file, output_file)

if __name__ == "__main__":
    main()
