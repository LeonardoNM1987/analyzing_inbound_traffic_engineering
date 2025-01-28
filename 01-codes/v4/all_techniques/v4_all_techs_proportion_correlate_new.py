import os
import pandas as pd

# Caminho para os arquivos
directory_path_aspp = "07-aspp_results/v4/proportion"
directory_path_moreSpecific = "08-more_specific_results/v4/ases_details"
directory_path_selective = "11-selective_announcement_results/v4"
output_file = "19-preparing_data_for_plot/v4/all_techs_asn_proportion_average_v4.txt"

# Lista para armazenar os dados
asn_data_aspp = []
asn_data_moreSpecific = []
asn_data_selective = []

print('Processando ASPP....')
# Loop para ler todos os arquivos da técnica ASPP
for file_name in os.listdir(directory_path_aspp):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory_path_aspp, file_name)
        # Lê o arquivo ignorando a linha de cabeçalho
        data = pd.read_csv(file_path, sep="|", skiprows=1, names=[
            "asn", "announced_prefixes", "prepended_prefixes", "region", "country", "as_type", "prepend_percentage"]
        )
        asn_data_aspp.append(data)

# Combina todos os dados da técnica ASPP em um único DataFrame
combined_data_aspp = pd.concat(asn_data_aspp, ignore_index=True)

# Calcula a média da proporção para cada ASN da técnica ASPP
average_proportion_aspp = combined_data_aspp.groupby("asn")["prepend_percentage"].mean().reset_index()

# Limita a média a 2 casas decimais
average_proportion_aspp["prepend_percentage"] = average_proportion_aspp["prepend_percentage"].round(2)

# Renomeia a coluna para o formato de saída
average_proportion_aspp.columns = ["asn", "aspp_average"]
print('Processando Mais Específico....')
# Loop para ler todos os arquivos da técnica More Specific
for file_name in os.listdir(directory_path_moreSpecific):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory_path_moreSpecific, file_name)
        # Lê o arquivo ignorando a linha de cabeçalho
        data = pd.read_csv(file_path, sep="|", skiprows=1, names=[
            "asn", "region", "country", "as_type", "use_moreSpecific", "announced_prefixes", "moreSpecific_prefixes", "moreSpecific_proportion_usage", "announced_prefixes_list"]
        )
        # Filtra apenas os registros com use_moreSpecific = 'yes'
        data = data[data["use_moreSpecific"] == "yes"]
        asn_data_moreSpecific.append(data)

# Combina todos os dados da técnica More Specific em um único DataFrame
combined_data_moreSpecific = pd.concat(asn_data_moreSpecific, ignore_index=True)

# Calcula a média da proporção para cada ASN da técnica More Specific
average_proportion_moreSpecific = combined_data_moreSpecific.groupby("asn")["moreSpecific_proportion_usage"].mean().reset_index()

# Limita a média a 2 casas decimais
average_proportion_moreSpecific["moreSpecific_proportion_usage"] = average_proportion_moreSpecific["moreSpecific_proportion_usage"].round(2)

# Renomeia a coluna para o formato de saída
average_proportion_moreSpecific.columns = ["asn", "moreSpecific_average"]

print('Processando Seletivos....')
# Loop para ler todos os arquivos da técnica Selective
for file_name in os.listdir(directory_path_selective):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory_path_selective, file_name)
        # Lê o arquivo ignorando a linha de cabeçalho
        data = pd.read_csv(file_path, sep="|", skiprows=1, names=[
            "origin_as", "region", "country", "as_type", "use_selective", "selective_prefixes", "selective_neighbors", "selective_proportion", "median_intensity"]
        )
        # Filtra apenas os registros com use_selective = True
        data = data[data["use_selective"] == True]
        # Converte os valores de proporção para porcentagem (multiplica por 100)
        data["selective_proportion"] = data["selective_proportion"] * 100
        asn_data_selective.append(data)

# Combina todos os dados da técnica Selective em um único DataFrame
combined_data_selective = pd.concat(asn_data_selective, ignore_index=True)

# Calcula a média da proporção para cada ASN da técnica Selective
average_proportion_selective = combined_data_selective.groupby("origin_as")["selective_proportion"].mean().reset_index()

# Limita a média a 2 casas decimais
average_proportion_selective["selective_proportion"] = average_proportion_selective["selective_proportion"].round(2)

# Renomeia a coluna para o formato de saída
average_proportion_selective.columns = ["asn", "selective_average"]

# Combina os resultados das três técnicas
final_average = pd.merge(average_proportion_aspp, average_proportion_moreSpecific, on="asn", how="outer")
final_average = pd.merge(final_average, average_proportion_selective, on="asn", how="outer")

# Salva o resultado no arquivo de saída
final_average.to_csv(output_file, sep="|", index=False, header=True)

print(f"A média das proporções foi salva no arquivo: {output_file}")
