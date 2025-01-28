import os
import glob

# Diretórios e arquivos
dir_path = '11-selective_announcement_results/v4/'
output_file = '19-preparing_data_for_plot/v4/selective_median_intensity_types.txt'

# Definir as categorias (em escala decimal)
categories = {
    'baixa': (0.01, 0.33),
    'media': (0.34, 0.66),
    'alta': (0.67, 1.00)
}

# Função para determinar a categoria de intensidade
def get_category(intensity):
    for category, (lower, upper) in categories.items():
        if lower <= intensity <= upper:
            return category
    return None

# Verificar se o diretório existe
if not os.path.exists(dir_path):
    print(f"O diretório {dir_path} não existe.")
else:
    # Obter todos os arquivos de texto no diretório
    files = glob.glob(os.path.join(dir_path, 'selective_announc_result_*.txt'))

    if not files:
        print("Nenhum arquivo foi encontrado no diretório especificado.")
    else:
        print(f"Total de arquivos encontrados: {len(files)}")

        # Inicializar lista para armazenar resultados
        results = []

        # Iterar sobre todos os arquivos de texto no diretório
        for file_path in files:
            # Extrair a data do nome do arquivo
            file_name = os.path.basename(file_path)
            date_str = file_name.replace('selective_announc_result_', '').replace('.txt', '')

            print(f"Lendo arquivo: {file_name}")

            # Inicializar listas para armazenar os dados
            rows = []

            # Ler o arquivo manualmente
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    parts = line.strip().split('|')
                    if len(parts) < 8:
                        continue
                    # Considerar apenas linhas onde 'use_selective' é 'True'
                    if parts[4] != 'True':
                        continue
                    # Converter 'median_intensity' para valor decimal
                    median_intensity = float(parts[8])
                    rows.append({
                        'origin_as': parts[0],
                        'region': parts[1],
                        'country': parts[2],
                        'as_type': parts[3],
                        'use_selective': parts[4],
                        'selective_prefixes': parts[5],
                        'selective_neighbors': parts[6],
                        'median_intensity': median_intensity
                    })

            # Filtrar apenas tipos especificados
            rows = [row for row in rows if row['as_type'] in ["business", "education", "government", "hosting", "isp", "none"]]

            # Adicionar resultados globais
            internet_category_counts = { 'baixa': 0, 'media': 0, 'alta': 0 }
            for row in rows:
                category = get_category(row['median_intensity'])
                if category:
                    internet_category_counts[category] += 1

            results.append({
                'as_type': 'internet',
                'data': date_str,
                **internet_category_counts
            })

            # Adicionar resultados por tipos
            types = set(row['as_type'] for row in rows)
            for as_type in types:
                type_rows = [row for row in rows if row['as_type'] == as_type]
                type_category_counts = { 'baixa': 0, 'media': 0, 'alta': 0 }
                for row in type_rows:
                    category = get_category(row['median_intensity'])
                    if category:
                        type_category_counts[category] += 1

                results.append({
                    'as_type': as_type,
                    'data': date_str,
                    **type_category_counts
                })

        # Ordenar os resultados por tipo e data
        results.sort(key=lambda x: (x['as_type'], x['data']))

        # Salvar os resultados em um arquivo de saída TXT
        with open(output_file, 'w') as f:
            f.write('#as_type|date|baixa|media|alta\n')
            for result in results:
                f.write(f"{result['as_type']}|{result['data']}|{result['baixa']}|{result['media']}|{result['alta']}\n")

        print(f"Resultados salvos em {output_file}")
