import os
import pandas as pd
import glob



# Defina o diretório onde os arquivos estão localizados
dir_path = f'07-aspp_results/v6/proportion/'
output_file = f'19-preparing_data_for_plot/v6/aspp/aspp_proportion_regions.txt'

# Definir as categorias
categories = {
    'from1to24': (0.1, 24.9),
    'from25to49': (25.0, 49.9),
    'from50to74': (50.0, 74.9),
    'from75to100': (75.0, 100.0)
}

# Inicializar um DataFrame para armazenar os resultados
results = pd.DataFrame(columns=['region', 'data', 'from1to24', 'from25to49', 'from50to74', 'from75to100'])

# Função para determinar a categoria de um percentual
def get_category(percent):
    for category, (lower, upper) in categories.items():
        if lower <= percent <= upper:
            return category
    return None

# Verificar se o diretório existe
if not os.path.exists(dir_path):
    print(f"O diretório {dir_path} não existe.")
else:
    # Obter todos os arquivos de texto no diretório
    files = glob.glob(os.path.join(dir_path, 'v6_aspp_proportion_*.txt'))
    
    if not files:
        print("Nenhum arquivo foi encontrado no diretório especificado.")
    else:
        print(f"Total de arquivos encontrados: {len(files)}")

        # Iterar sobre todos os arquivos de texto no diretório
        for file_path in files:
            # Extrair a data do nome do arquivo
            file_name = os.path.basename(file_path)
            date_str = file_name.replace('v6_aspp_proportion_', '').replace('.txt', '')
            
            print(f"Lendo arquivo: {file_name}")
            
            # Ler o arquivo em um DataFrame
            df = pd.read_csv(file_path, sep='|', comment='#', header=None, names=['asn', 'announced_prefixes', 'prepended_prefixes', 'region', 'country','as_type', 'prepend_percentage'])
            
            # Filtrar apenas as regiões especificadas
            df = df[df['region'].isin(['apnic', 'afrinic', 'arin', 'lacnic', 'ripencc'])]

            # Adicionar resultados globais
            internet_category_counts = { 'from1to24': 0, 'from25to49': 0, 'from50to74': 0, 'from75to100': 0 }
            for percent in df['prepend_percentage']:
                category = get_category(percent)
                if category:
                    internet_category_counts[category] += 1

            new_row = pd.DataFrame([{'region': 'internet', 'data': date_str, **internet_category_counts}])
            results = pd.concat([results, new_row], ignore_index=True)

            # Adicionar resultados regionais
            for region in df['region'].unique():
                regional_df = df[df['region'] == region]
                regional_category_counts = { 'from1to24': 0, 'from25to49': 0, 'from50to74': 0, 'from75to100': 0 }
                for percent in regional_df['prepend_percentage']:
                    category = get_category(percent)
                    if category:
                        regional_category_counts[category] += 1

                new_row = pd.DataFrame([{'region': region, 'data': date_str, **regional_category_counts}])
                results = pd.concat([results, new_row], ignore_index=True)

# Ordenar os resultados por data e região
results = results.sort_values(by=['region', 'data'])

# Salvar os resultados em um arquivo de saída TXT
with open(output_file, 'w') as f:
    f.write('region|date|from1to24|from25to49|from50to74|from75to100\n')
    for index, row in results.iterrows():
        f.write(f"{row['region']}|{row['data']}|{row['from1to24']}|{row['from25to49']}|{row['from50to74']}|{row['from75to100']}\n")

print(f"Resultados salvos em {output_file}")
