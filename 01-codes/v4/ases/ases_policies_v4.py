import os
import datetime

# Caminhos de entrada e saída
input_folder = '05-prefixes_policies_regions_and_types_saned/v4_prefixes'
output_folder = '06-ases_policies/v4_ases'
os.makedirs(output_folder, exist_ok=True)  # Certifica-se de que a pasta de saída exista

# Função para processar o arquivo
def processar_arquivo(arquivo):
    ases_policies = {}
    total_descartados = 0  # Contador de ASNs descartados

    with open(arquivo, 'r') as f:
        # Ignorar a primeira linha (cabeçalho)
        next(f)
        for linha in f:
            # Dividir a linha em partes
            partes = linha.strip().split('|')
            prefix = partes[0]
            asn = partes[1]
            region = partes[3]
            country = partes[4]
            as_type = partes[5]
            aspp_policy = partes[6]
            announcement_with_aspp = partes[7]  # Exemplo: "0;2;4;0"

            # Verificar se o ASN deve ser descartado
            if region.lower() == 'none' or country.lower() == 'none':
                total_descartados += 1
                continue

            # Inicializar ou atualizar o dicionário do ASN
            if asn not in ases_policies:
                ases_policies[asn] = {
                    'type': as_type,
                    'region': region,
                    'country': country,
                    'observed_policies': set(),
                    'prefixes': set(),
                    'announcements': [],
                }

            # Atualizar as informações do ASN
            ases_policies[asn]['observed_policies'].add(aspp_policy)
            ases_policies[asn]['prefixes'].add(prefix)
            ases_policies[asn]['announcements'].extend(map(int, announcement_with_aspp.split(';')))

    return ases_policies, total_descartados

# Função para salvar o resultado em arquivo
def salvar_resultado(output_file, ases_policies, total_descartados):
    with open(output_file, 'w') as f:
        f.write('#asn|type|region|country|observed_policies|prefixes|announcements\n')
        for asn, data in ases_policies.items():
            # Concatenar os valores necessários
            observed_policies = ';'.join(sorted(data['observed_policies']))
            prefixes = ';'.join(sorted(data['prefixes']))
            announcements = ';'.join(map(str, data['announcements']))  # Preserva a ordem e duplicatas

            # Escrever no arquivo
            f.write(f"{asn}|{data['type']}|{data['region']}|{data['country']}|"
                    f"{observed_policies}|{prefixes}|{announcements}\n")
    print(f'Total de ASNs descartados (region=none ou country=none): {total_descartados}')

# Processar todos os arquivos da pasta de entrada
for file in sorted(os.listdir(input_folder)):
    if file.startswith('v4_prefixes_policies_complete_') and file.endswith('.txt'):
        # Caminhos de entrada e saída
        input_file = os.path.join(input_folder, file)
        current_date = file[len('v4_prefixes_policies_complete_'):-len('.txt')]
        output_file = os.path.join(output_folder, f'v4_ases_policies_{current_date}.txt')

        print(f'Processando arquivo: {file}...')

        # Processar o arquivo e gerar o resultado
        ases_policies, total_descartados = processar_arquivo(input_file)
        salvar_resultado(output_file, ases_policies, total_descartados)

        print(f'Arquivo processado e salvo em: {output_file}')

