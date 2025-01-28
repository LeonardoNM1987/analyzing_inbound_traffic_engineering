import os
import pandas as pd

# Função para realizar a análise para uma data específica
def analyze_for_date(date):
    file1 = f'07-aspp_results/v6/proportion/v6_aspp_proportion_{date}.txt'
    file2 = f'08-more_specific_results/v6/ases_details/v6_moreSpecific_ases_details_{date}.txt'
    file3 = f'11-selective_announcement_results/v6/selective_announc_result_{date}.txt'  # Novo arquivo

    # Verificar se os arquivos existem
    if not (os.path.exists(file1) and os.path.exists(file2) and os.path.exists(file3)):
        print(f"Arquivos faltando para a data {date}")
        return None

    # Ler os arquivos
    try:
        df1 = pd.read_csv(file1, sep='|', comment='#', header=None, names=["asn", "announced_prefixes", "prepended_prefixes", "region", "country", "as_type", "prepend_percentage"])
        df2 = pd.read_csv(file2, sep='|', comment='#', header=None, names=["asn", "region", "country", "as_type", "use_moreSpecific(yes;no)", "announced_prefixes", "moreSpecific_prefixes", "moreSpecific_proportion_usage", "announced_prefixes(list)"])
        df3 = pd.read_csv(file3, sep='|', comment='#', header=None, names=["asn", "region", "country", "as_type", "use_selective", "selective_prefixes", "selective_neighbors", "selective_proportion", "median_intensity"])
    except Exception as e:
        print(f"Erro ao ler arquivos para a data {date}: {e}")
        return None

    # Filtrar df2 para considerar apenas os que têm 'yes' na coluna 'use_moreSpecific(yes;no)'
    df2_filtered = df2[df2['use_moreSpecific(yes;no)'] == 'yes']

    # Filtrar df3 para considerar apenas os que têm 'True' na coluna 'use_selective'
    df3_filtered = df3[df3['use_selective'] == True]

    # Identificar os conjuntos de ASNs
    ases_aspp = set(df1['asn'])
    ases_more_specific = set(df2_filtered['asn'])
    ases_selective = set(df3_filtered['asn'])

    # Realizar as comparações
    aspp_and_more_specific = ases_aspp & ases_more_specific
    aspp_and_selective = ases_aspp & ases_selective
    more_specific_and_selective = ases_more_specific & ases_selective
    all_three = ases_aspp & ases_more_specific & ases_selective

    # Ajustar o cálculo de just_*
    just_aspp = ases_aspp - (ases_more_specific | ases_selective)
    just_more_specific = ases_more_specific - (ases_aspp | ases_selective)
    just_selective = ases_selective - (ases_aspp | ases_more_specific)

    # Calcular os totais
    total_ases = len(ases_aspp | ases_more_specific | ases_selective)
    total_aspp_and_more_specific = len(aspp_and_more_specific)
    total_aspp_and_selective = len(aspp_and_selective)
    total_more_specific_and_selective = len(more_specific_and_selective)
    total_all_three = len(all_three)
    total_just_aspp = len(just_aspp)
    total_just_more_specific = len(just_more_specific)
    total_just_selective = len(just_selective)
    #total_all_three_modified = total_all_three - total_just_more_specific       # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Resultados
    result = f"{date}|{total_ases}|{total_aspp_and_more_specific}|{total_aspp_and_selective}|{total_more_specific_and_selective}|{total_all_three}|{total_just_aspp}|{total_just_more_specific}|{total_just_selective}"
    
    print(f"Análise para a data {date} concluída: {result}")
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
dates1 = list_dates(f'07-aspp_results/v6/proportion', 'v6_aspp_proportion_')
dates2 = list_dates(f'08-more_specific_results/v6/ases_details', 'v6_moreSpecific_ases_details_')
dates3 = list_dates(f'11-selective_announcement_results/v6', 'selective_announc_result_')

# Interseção das datas disponíveis nos três diretórios
dates = sorted(set(dates1) & set(dates2) & set(dates3))

# Realizar a análise para todas as datas disponíveis
results = ["#date|total_ases|aspp_and_moreSpecific|aspp_and_selective|more_specific_and_selective|all_three|just_aspp|just_more_specific|just_selective"]
for date in dates:
    result = analyze_for_date(date)
    if result:
        results.append(result)

# Salvar os resultados em um arquivo de texto
output_path = f'19-preparing_data_for_plot/v6/all_techniques/all_techniques_deploy.txt'

with open(output_path, 'w') as f:
    for line in results:
        f.write(line + '\n')

print("Análise concluída e resultados salvos.")

