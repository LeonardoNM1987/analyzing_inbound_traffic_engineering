import pandas as pd
import os

# Função para carregar e processar os dados de cada técnica
def load_as_path_prepend(file_path):
    print(f'Processando {file_path}...')
    """Carrega os dados de AS Path Prepend com cabeçalhos definidos manualmente."""
    # Defina os nomes das colunas esperadas
    columns = ["ASN", "announced_prefixes", "prepended_prefixes", "region", "country", "as_type", "AS_Path_Prepend_Percentage"]

    # Carregar os dados, ignorando a primeira linha (que é interpretada como cabeçalho incorreto)
    df = pd.read_csv(file_path, sep="|", header=None, names=columns, skiprows=1)
    
    # Selecionar apenas as colunas relevantes
    df = df[["ASN", "AS_Path_Prepend_Percentage"]]
    return df

def load_more_specific(file_path):
    print(f'Processando {file_path}...')
    """Carrega os dados de Anúncio de Prefixo mais Específico com cabeçalhos definidos manualmente."""
    columns = ["ASN", "region", "country", "as_type", "use_moreSpecific", "announced_prefixes", 
               "moreSpecific_prefixes", "More_Specific_Percentage", "announced_prefixes_list"]
    df = pd.read_csv(file_path, sep="|", header=None, names=columns, skiprows=1)
    df = df[["ASN", "More_Specific_Percentage"]]
    return df

def load_selective_announcement(file_path):
    print(f'Processando {file_path}...')
    """Carrega os dados de Anúncio Seletivo com cabeçalhos definidos manualmente."""
    columns = ["ASN", "region", "country", "as_type", "use_selective", "selective_prefixes", 
               "selective_neighbors", "Selective_Proportion", "median_intensity"]
    df = pd.read_csv(file_path, sep="|", header=None, names=columns, skiprows=1)
    df = df[["ASN", "Selective_Proportion"]]
    return df



# Caminho para os diretórios com os arquivos
as_path_prepend_dir = "07-aspp_results/v6/proportion/"
more_specific_dir = "08-more_specific_results/v6/ases_details/"
selective_announcement_dir = "11-selective_announcement_results/v6/"

# Inicializa um DataFrame vazio para consolidar os dados
all_data = pd.DataFrame()

# Processa os arquivos de cada técnica com base no padrão de nomes
for file_name in os.listdir(as_path_prepend_dir):
    if not file_name.startswith("v6_aspp_proportion_"):
        print('Pulando arquivo fora do padrão...')
        continue  # Ignora arquivos que não seguem o padrão esperado

    # Extrai a data do arquivo
    date = file_name.replace("v6_aspp_proportion_", "").replace(".txt", "")

    # Constroi os caminhos completos dos arquivos
    as_path_prepend_file = os.path.join(as_path_prepend_dir, file_name)
    more_specific_file = os.path.join(more_specific_dir, f"v6_moreSpecific_ases_details_{date}.txt")
    selective_announcement_file = os.path.join(selective_announcement_dir, f"selective_announc_result_{date}.txt")

    # Verifica se os arquivos correspondentes existem
    if not (os.path.exists(more_specific_file) and os.path.exists(selective_announcement_file)):
        print(f"Arquivos ausentes para {date}, pulando...")
        continue

    try:
        # Carregar os dados
        #print(as_path_prepend_file)
        prepend_data = load_as_path_prepend(as_path_prepend_file)
        more_specific_data = load_more_specific(more_specific_file)
        selective_data = load_selective_announcement(selective_announcement_file)

        # Mesclar os dados
        merged = prepend_data.merge(more_specific_data, on="ASN", how="outer")
        merged = merged.merge(selective_data, on="ASN", how="outer")

        # Adicionar a data
        merged["Date"] = date

        # Consolidar no DataFrame final
        all_data = pd.concat([all_data, merged], ignore_index=True)

    except Exception as e:
        print(f"Erro ao processar {date}: {e}")

# Salvar os dados consolidados
output_path = "19-preparing_data_for_plot/v6/all_techniques/all_tech_proportion_consolidated_data.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Garante que o diretório existe
all_data.to_csv(output_path, index=False)

print(f"Dados consolidados salvos em {output_path}")


