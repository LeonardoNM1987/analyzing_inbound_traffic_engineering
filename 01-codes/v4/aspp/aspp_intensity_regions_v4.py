import os
import pandas as pd
from collections import Counter

def process_asn_data_folder(input_folder, output_file):
    # Estrutura para armazenar os resultados
    all_results = []

    # Iterar sobre todos os arquivos no diretório de entrada
    for filename in os.listdir(input_folder):
        if filename.startswith('v4_ases_policies_') and filename.endswith('.txt'):
            # Extrair a data do nome do arquivo
            
            date = filename.split('_')[-1].split('.')[0]
            input_file = os.path.join(input_folder, filename)
            print(f'Processando {date}...')
            # Processar cada arquivo
            results = {}
            with open(input_file, 'r') as file:
                for line in file:
                    fields = line.strip().split('|')
                    if len(fields) < 6:
                        continue  # Ignorar linhas mal formatadas

                    asn, region, observed_policies, prepend_data = fields[0], fields[2], fields[4], fields[-1]

                    # Ignorar linhas onde observed_policies é apenas '0'
                    if observed_policies.strip() == '0':
                        continue

                    # Filtrar prepend data, ignorar prepends não numéricos e valores '0'
                    prepend_values = [int(p) for p in prepend_data.split(';') if p.strip().isdigit() and int(p) > 0]
                    if not prepend_values:
                        continue  # Ignorar se não há valores significativos

                    # Encontrar o prepend mais frequente
                    prepend_counts = Counter(prepend_values)
                    dominant_prepend = max(prepend_counts, key=prepend_counts.get)

                    # Determinar a categoria
                    if dominant_prepend == 1:
                        category = 'tam_1'
                    elif dominant_prepend == 2:
                        category = 'tam_2'
                    elif dominant_prepend == 3:
                        category = 'tam_3'
                    else:
                        category = 'tam_4plus'

                    # Incrementar os resultados por região e categoria
                    if region not in results:
                        results[region] = {'tam_1': 0, 'tam_2': 0, 'tam_3': 0, 'tam_4plus': 0}

                    results[region][category] += 1

            # Calcular os totais para a região "internet"
            internet_totals = {'tam_1': 0, 'tam_2': 0, 'tam_3': 0, 'tam_4plus': 0}
            for region, categories in results.items():
                for category in internet_totals.keys():
                    internet_totals[category] += categories[category]

            results["internet"] = internet_totals

            # Adicionar os resultados ao conjunto geral
            for region, categories in results.items():
                all_results.append({
                    'region': region,
                    'date': date,
                    'tam_1': categories['tam_1'],
                    'tam_2': categories['tam_2'],
                    'tam_3': categories['tam_3'],
                    'tam_4plus': categories['tam_4plus']
                })

    # Criar o DataFrame e salvar em arquivo no formato especificado
    df = pd.DataFrame(all_results)
    df.to_csv(output_file, sep='|', index=False, header=True)
    print(f"Resultados salvos em {output_file}")

# Exemplo de uso
process_asn_data_folder(
    input_folder='06-ases_policies/v4_ases/',
    output_file='19-preparing_data_for_plot/v4/aspp_intensity_regions.txt'
)
