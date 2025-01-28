# ESSE CÓDIGO GERA UMA LISTA DE ASES ANUNCIANDO PREFIXOS IPV4 SEGMENTADOS POR REGIÃO EM NUMERO ABSOLUTO

import os

# Caminho para os arquivos de entrada e saída
input_folder = '06-ases_policies/v6_ases/' 
output_file = '19-preparing_data_for_plot/v6/ases/ases_per_region.txt'  

# Certificar que a pasta de saída existe
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Função para processar o arquivo e contar os ASes por região
def contar_ases_por_regiao(input_file):
    # Extrair a data do nome do arquivo
    data = input_file.split('_')[-1].replace('.txt', '')

    # Inicializar contadores de regiões
    regioes = ['afrinic', 'arin', 'apnic', 'lacnic', 'ripencc']
    contagem = {regiao: 0 for regiao in regioes}

    # Ler o arquivo
    with open(input_file, 'r') as f:
        # Ignorar a linha de cabeçalho
        next(f)
        for linha in f:
            partes = linha.strip().split('|')
            if len(partes) < 3:
                continue  # Ignorar linhas malformadas
            region = partes[2].lower()
            if region in contagem:
                contagem[region] += 1

    # Somar o total de ASes (campo 'internet')
    total_as = sum(contagem.values())

    # Criar a linha de saída
    output = f"{data}|{total_as}|"
    output += "|".join(str(contagem[regiao]) for regiao in regioes)
    return output

# Processar todos os arquivos e salvar no arquivo de saída
with open(output_file, 'w') as out:
    # Escrever o cabeçalho
    out.write("#data|internet|afrinic|arin|apnic|lacnic|ripencc\n")
    # Processar cada arquivo no diretório de entrada
    for file in sorted(os.listdir(input_folder)):
        if file.startswith('v6_ases_policies_') and file.endswith('.txt'):
            print(f'Processando {file}')
            input_path = os.path.join(input_folder, file)
            resultado = contar_ases_por_regiao(input_path)
            out.write(resultado + '\n')

print(f"Processamento completo! Resultado salvo em: {output_file}")
