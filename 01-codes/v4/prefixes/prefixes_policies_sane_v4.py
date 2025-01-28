import os
import csv
import ipaddress
from datetime import datetime, timedelta
from collections import defaultdict

# Caminhos das pastas e arquivos
input_folder = '09-selective_announcement_database/v4/'
delegatedPath = '03-delegated/'
typesFile = '02-resources/as_types.csv'
output_folder = '10-selective_announcement_regions_and_types_saned/v4/'
summary_file = os.path.join(output_folder, 'summary_report.txt')

# Certificar que a pasta de saída existe
os.makedirs(output_folder, exist_ok=True)

# Função para validar se é IPv4 e obter o comprimento do prefixo
def is_ipv4(prefix):
    try:
        ip = ipaddress.IPv4Network(prefix, strict=False)
        return True, ip.prefixlen
    except ValueError:
        return False, None

# Carregar os tipos de ASN no formato atualizado
asn_types = {}
with open(typesFile, 'r', encoding='utf-8') as types_file:
    csv_reader = csv.reader(types_file, delimiter=',', quotechar='"')
    next(csv_reader)  # Ignorar o cabeçalho
    for columns in csv_reader:
        if len(columns) < 7:
            continue
        asn = columns[3].replace('AS', '')
        as_type = columns[6]
        asn_types[asn] = as_type

# Função principal para processar os arquivos
def processar_arquivo(input_file, output_file, date):
    #nome_arquivo = input_file[2].split('/')
    
    print(f"Processando: {input_file}....")

    # Carregar dados das regiões
    delegatedFolder = f'{delegatedPath}{date}'
    region_dicts = {
        region: defaultdict(dict) for region in ['afrinic', 'apnic', 'arin', 'lacnic', 'ripencc']
    }

    for delegatedFile in os.listdir(delegatedFolder):
        filePath = os.path.join(delegatedFolder, delegatedFile)
        regionName = delegatedFile.split('-')[1]
        with open(filePath, 'r') as readDelegated:
            for linha in readDelegated:
                coluna = linha.strip().split('|')
                if len(coluna) < 7 or coluna[2] != 'asn' or coluna[3] == '*' or coluna[6] not in ['allocated', 'assigned']:
                    continue
                if coluna[4] == '1':
                    region_dicts[regionName][coluna[3]] = {'country': coluna[1]}
                else:
                    startAsn = int(coluna[3])
                    endAsn = startAsn + int(coluna[4])
                    for item in range(startAsn, endAsn):
                        region_dicts[regionName][str(item)] = {'country': coluna[1]}

    # Processar o arquivo de entrada e salvar o resultado final
    finalResults = []
    total_prefixes = 0
    removed_invalid_prefix = 0

    with open(input_file, 'r') as entrada:
        for linha in entrada:
            if linha.startswith('#') or not linha.strip():
                continue

            coluna = linha.strip().split('|')
            if len(coluna) < 2:
                continue

            as_origin = coluna[0]
            prefix_data = coluna[1]

            total_prefixes += 1

            # Verificar se o prefixo é válido e está entre /8 e /24
            is_valid_ipv4, prefix_len = is_ipv4(prefix_data)
            if not is_valid_ipv4 or prefix_len < 8 or prefix_len > 24:
                removed_invalid_prefix += 1
                continue

            # Determinar a região e o país
            region, country = None, None
            for reg, data in region_dicts.items():
                if as_origin in data:
                    region = reg
                    country = data[as_origin]['country']
                    break

            if region not in ['afrinic', 'apnic', 'arin', 'lacnic', 'ripencc']:
                continue

            as_type = asn_types.get(as_origin, 'none')
            finalResults.append(f"{as_origin}|{region}|{country}|{as_type}|{prefix_data}")

    # Salvar os resultados no arquivo de saída
    with open(output_file, 'w') as saida:
        saida.write("#as_origin|region|country|as_type|prefix01(neighbors_announced);prefix02(neighbors_announced);...\n")
        for result in finalResults:
            saida.write(f"{result}\n")

    #print(f"Finalizado processamento do arquivo: {output_file}")
    return total_prefixes, removed_invalid_prefix

# Processar arquivos no intervalo de datas e gerar resumo
def processar_por_intervalo(input_folder, output_folder, start_year, end_year, start_month, end_month):
    dia_fixo = 15
    data_atual = datetime(year=start_year, month=start_month, day=dia_fixo)
    data_final = datetime(year=end_year, month=end_month, day=dia_fixo)

    with open(summary_file, 'w') as resumo:
        resumo.write("#date|total_prefixes|removed_invalid_prefix\n")

        while data_atual <= data_final:
            date_str = data_atual.strftime('%Y%m%d')
            input_file = os.path.join(input_folder, f'v4_prefix_origin_{date_str}.txt')
            output_file = os.path.join(output_folder, f'v4_prefix_origin_complete_{date_str}.txt')

            if os.path.exists(input_file):
                total_prefixes, removed_invalid_prefix = processar_arquivo(input_file, output_file, date_str)
                resumo.write(f"{date_str}|{total_prefixes}|{removed_invalid_prefix}\n")
            else:
                print(f"Arquivo de entrada não encontrado: {input_file}")

            data_atual += timedelta(days=31)
            data_atual = data_atual.replace(day=dia_fixo)

if __name__ == "__main__":
    inicio_total = datetime.now()

    # Configurar intervalo de datas
    start_month = 6    # Mês inicial
    start_year = 2014  # Ano inicial
    end_month = 6      # Mês final
    end_year = 2024    # Ano final

    # Processar os arquivos no intervalo definido
    processar_por_intervalo(input_folder, output_folder, start_year, end_year, start_month, end_month)

    fim_total = datetime.now()
    tempo_execucao_total = fim_total - inicio_total
    print(f"Tempo de execução total das análises: {str(tempo_execucao_total).split('.')[0]}")
