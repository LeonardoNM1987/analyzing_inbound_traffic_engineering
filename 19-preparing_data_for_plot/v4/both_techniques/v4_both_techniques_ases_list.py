import os
import pandas as pd

#local = '(original)'
#local = '(novos-04)'
local = '(novos-06)'

# Função para realizar a análise para uma data específica
def analyze_for_date(date):
    file1 = f'3-full_results/aspp/v4_prepended_proportion/v4_prepended_proportion_{date}.txt'
    file2 = f'3-full_results/more_specific/v4_moreSpecific_deploy_and_proportion/v4_moreSpecific_deploy_and_proportion_{date}.txt'

    # Verificar se os arquivos existem
    if not (os.path.exists(file1) and os.path.exists(file2)):
        print(f"Arquivos faltando para a data {date}")
        return None

    # Ler os arquivos
    try:
        df1 = pd.read_csv(file1, sep='|', comment='#', header=None, names=['ASN', 'ANNOUNCED_PREFIXES', 'PREPENDED_PREFIXES', 'REGION', 'COUNTRY', 'PREPEND_PERCENTAGE'])
        df2 = pd.read_csv(file2, sep='|', comment='#', header=None, names=['ASN', 'REGION', 'COUNTRY', 'USE_MORE_SPECIFIC', 'ANNOUNCED_PREFIXES', 'MORE_SPECIFIC_PREFIXES', 'MORE_SPECIFIC_PROPORTION_USAGE', 'ANNOUNCED_PREFIXES_LIST'])
    except Exception as e:
        print(f"Erro ao ler arquivos para a data {date}: {e}")
        return None

    # Validar apenas os que possuem arin, apnic, lacnic, afrinic ou ripencc na região
    valid_regions = ['apnic', 'arin', 'lacnic', 'afrinic', 'ripencc']
    df1_filtered = df1[df1['REGION'].isin(valid_regions)]
    df2_filtered = df2[(df2['REGION'].isin(valid_regions)) & (df2['USE_MORE_SPECIFIC'] == 'yes')]

    # Identificar os conjuntos de ASNs
    ases_aspp = set(df1_filtered['ASN'])
    ases_more_specific = set(df2_filtered['ASN'])

    # Realizar a interseção para encontrar os ASNs que utilizam ambas as técnicas
    aspp_and_moreSpecific_ases = ases_aspp & ases_more_specific

    # Resultados
    total_aspp_and_moreSpecific = len(aspp_and_moreSpecific_ases)
    result = f"{date}|{total_aspp_and_moreSpecific}|{','.join(map(str, aspp_and_moreSpecific_ases))}"
    
    #print(f"Análise para a data {date} concluída: {result}")
    return result

# Função para listar todas as datas disponíveis nos arquivos
def list_dates(directory, prefix):
    dates = set()
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith('.txt'):
            date = filename[len(prefix):-4]  # Extrair a data do nome do arquivo
            dates.add(date)
    return sorted(dates)

# Listar todas as datas disponíveis
dates1 = list_dates('3-full_results/aspp/v4_prepended_proportion', 'v4_prepended_proportion_')
dates2 = list_dates('3-full_results/more_specific/v4_moreSpecific_deploy_and_proportion', 'v4_moreSpecific_deploy_and_proportion_')

# Interseção das datas disponíveis nos dois diretórios
dates = sorted(set(dates1) & set(dates2))

# Realizar a análise para todas as datas disponíveis
results = ["#date|total_ases_list|aspp_and_moreSpecific_ases_list"]
for date in dates:
    print(f'Analisando {date}...')
    result = analyze_for_date(date)
    if result:
        results.append(result)

# Salvar os resultados em um arquivo de texto
output_path = '9-ready_results/both_techniques/v4_both_techniques_ases_list.txt'
with open(output_path, 'w') as f:
    for line in results:
        f.write(line + '\n')

print("Análise concluída e resultados salvos.")
