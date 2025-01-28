import os
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta

def process_asn_data_folder(input_folder, output_file):
    # Registrar o início do processamento
    start_time = datetime.now()

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
                    
                    as_type = fields[1]
                    prepend_percentage = fields[6]   
                    
                    # Ignorar linhas onde as_type é "NA"
                    if as_type == "NA":
                        continue
                    
                    # Filtrar prepend data, ignorar prepends não numéricos e valores '0'
                    prepend_values = [int(p) for p in prepend_percentage.split(';') if p.strip().isdigit() and int(p) > 0]
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

                    # Incrementar os resultados por tipo e categoria
                    if as_type not in results:
                        results[as_type] = {'tam_1': 0, 'tam_2': 0, 'tam_3': 0, 'tam_4plus': 0}

                    results[as_type][category] += 1

            # Calcular os totais para o tipo "total"
            total_type = {'tam_1': 0, 'tam_2': 0, 'tam_3': 0, 'tam_4plus': 0}
            for as_type, categories in results.items():
                for category in total_type.keys():
                    total_type[category] += categories[category]

            results["internet"] = total_type

            # Adicionar os resultados ao conjunto geral
            for as_type, categories in results.items():
                all_results.append({
                    'as_type': as_type,
                    'date': date,
                    'tam_1': categories['tam_1'],
                    'tam_2': categories['tam_2'],
                    'tam_3': categories['tam_3'],
                    'tam_4plus': categories['tam_4plus']
                })

    # Criar o DataFrame
    df = pd.DataFrame(all_results)

    # Converter a coluna 'date' para datetime para ordenação
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

    # Ordenar pelo 'as_type' e 'date'
    df.sort_values(by=['as_type', 'date'], inplace=True)

    # Salvar no arquivo de saída
    df.to_csv(output_file, sep='|', index=False, header=True, date_format='%Y%m%d')
    print(f"Resultados salvos em {output_file}")

    # Registrar o fim do processamento
    end_time = datetime.now()

    # Calcular o tempo total de processamento
    elapsed_time = end_time - start_time
    elapsed_formatted = str(timedelta(seconds=elapsed_time.total_seconds()))
    print(f"Tempo total de processamento: {elapsed_formatted}")

# Exemplo de uso
process_asn_data_folder(
    input_folder='06-ases_policies/v4_ases/',
    output_file='19-preparing_data_for_plot/v4/aspp_intensity_types.txt'
)
