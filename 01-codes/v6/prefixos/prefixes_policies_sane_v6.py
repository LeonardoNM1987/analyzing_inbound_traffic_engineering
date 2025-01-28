# ESSE CODIGO REMOVE BOGONS, ALÉM DE ADICIONAR TIPO E REGIAO, NOS PREFIXOS ANUNCIADOS. TUDO DE ACORDO COM O AS QUE O ANUNCIA
import csv
import os
import pytricia
import ipaddress
import datetime
from collections import defaultdict

# Caminhos das pastas e arquivos
input_folder = '04-prefixes_policies_base/v6_prefixes/'
bogon_file_path = '02-resources/full_bogons-v6.txt'
delegatedPath = '03-delegated/'
typesFile = '02-resources/as_types.csv'
output_folder = '05-prefixes_policies_regions_and_types_saned/v6_prefixes/'

# Certificar que a pasta de saída existe
os.makedirs(output_folder, exist_ok=True)

# Função para carregar os prefixos bogons
def carregar_prefixos_bogon(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    return [linha.strip() for linha in linhas if not linha.startswith('#') and linha.strip()]

# Carregar os prefixos bogons em uma estrutura Patricia Trie
bogon_prefixes = carregar_prefixos_bogon(bogon_file_path)
trie = pytricia.PyTricia()
for prefix in bogon_prefixes:
    trie.insert(prefix, "bogon")

# Funções para processamento dos prefixos
def is_bogon(prefix):
    return trie.has_key(prefix)

def is_ipv6(prefix):
    try:
        network = ipaddress.IPv6Network(prefix, strict=False)
        return True, network.prefixlen  # Retorna o tamanho do prefixo
    except ValueError:
        return False, None


# Carregar os tipos de ASN
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
    print(f"Iniciando processamento do arquivo: {input_file}")

    # Carregar dados das regiões
    delegatedFolder = f'{delegatedPath}{date}'
    region_dicts = {
        region: defaultdict(lambda: {'country': None}) for region in ['afrinic', 'apnic', 'arin', 'lacnic', 'ripencc']
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

    total_prefixes = 0
    removed_invalid_prefix = 0

    # Processar o arquivo de entrada e salvar o resultado final
    finalResults = []
    with open(input_file, 'r') as entrada:
        header = entrada.readline()  # Preserva o cabeçalho
        for linha in entrada:
            if linha.startswith('#') or not linha.strip():
                continue

            coluna = linha.strip().split('|')
            if len(coluna) < 5:
                continue

            prefix = coluna[0]
            asn = coluna[1]
            num_monitors = coluna[2]
            aspp_policy = coluna[3]
            annoucement_aspp = coluna[4]
            total_prefixes += 1

            try:
                network = ipaddress.IPv6Network(prefix, strict=False)
                prefix_len = network.prefixlen
                if prefix_len < 16 or prefix_len > 48 or is_bogon(prefix):
                    removed_invalid_prefix += 1
                    continue
            except ValueError:
                print(f"Prefixo inválido ignorado: {prefix}")
                removed_invalid_prefix += 1
                continue

            region, country = None, None
            for reg, data in region_dicts.items():
                if asn in data:
                    region = reg
                    country = data[asn]['country']
                    break

            as_type = asn_types.get(asn, 'none')
            finalResults.append(f"{prefix}|{asn}|{num_monitors}|{region}|{country}|{as_type}|{aspp_policy}|{annoucement_aspp}")

    with open(output_file, 'w') as saida:
        saida.write(f'#prefix|originator|observed_monitors|region|country|as_type|aspp_Policy|announcement_with_aspp(length)\n')
        for result in finalResults:
            saida.write(f"{result}\n")

    print(f"Finalizado processamento do arquivo: {output_file}")


# Processar todos os arquivos
def processar_todos_arquivos():
    arquivos = sorted([f for f in os.listdir(input_folder) if f.endswith('.txt')])
    for arquivo in arquivos:
        input_path = os.path.join(input_folder, arquivo)
        date = arquivo.split('_')[-1].replace('.txt', '')
        output_path = os.path.join(output_folder, f"v6_prefixes_policies_complete_{date}.txt")
        processar_arquivo(input_path, output_path, date)

# Executar o processamento
processar_todos_arquivos()
print("Processamento completo!")

