import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Nome do arquivo com os dados
input_file = "19-preparing_data_for_plot/v6/all_techs_asn_proportion_average_v6.txt"

# Configuração de filtro para valores nulos
filter_null_values = True  # Alterar para False para desabilitar o filtro

# Ler o arquivo em um DataFrame
df = pd.read_csv(input_file, sep="|")

# Filtrar apenas os ASNs com valores nas três colunas, se habilitado
if filter_null_values:
    filtered_df = df.dropna(subset=["aspp_average", "moreSpecific_average", "selective_average"])
else:
    filtered_df = df


# Análises de quantidade
all_asns = df["asn"].nunique()
asns_all_techs = filtered_df["asn"].nunique()

asns_aspp_only = df[df["aspp_average"].notna() & df["moreSpecific_average"].isna() & df["selective_average"].isna()]["asn"].nunique()
asns_moreSpecific_only = df[df["aspp_average"].isna() & df["moreSpecific_average"].notna() & df["selective_average"].isna()]["asn"].nunique()
asns_selective_only = df[df["aspp_average"].isna() & df["moreSpecific_average"].isna() & df["selective_average"].notna()]["asn"].nunique()

# Exibir resultados no console
print("Quantidade de ASNs diferentes analisados:", all_asns)
print("Quantidade de ASNs que fazem as 3 técnicas:", asns_all_techs)
print("Quantidade de ASNs que fazem apenas ASPP:", asns_aspp_only)
print("Quantidade de ASNs que fazem apenas Prefixo Mais Específico:", asns_moreSpecific_only)
print("Quantidade de ASNs que fazem apenas Anúncio Seletivo:", asns_selective_only)








# Configurar figura
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Configuração de atributos de marcação
# Tamanhos e cores fixos para os pontos (customizáveis pelo usuário)
tamanho_bolinhas = 1  # Tamanho fixo das bolinhas
cores = "red"  # Cor fixa para os pontos

# Plotar os dados
scatter = ax.scatter(
    filtered_df["aspp_average"],
    filtered_df["moreSpecific_average"],
    filtered_df["selective_average"],
    c=cores,
    s=tamanho_bolinhas,
    alpha=1  # Transparência total (sem efeito de transparência)
)

# Configurar os limites dos eixos
ax.set_xlim(0, 100)  # Limites do eixo X (ASPP Average)
ax.set_ylim(0, 100)  # Limites do eixo Y (More Specific Average)
ax.set_zlim(0, 100)  # Limites do eixo Z (Selective Average)

# Adicionar rótulos
ax.set_xlabel("\nASPP (%)", fontsize=12)
ax.set_ylabel("\nPrefixo mais Específico (%)", fontsize=12)
ax.set_zlabel("\nAnuncio Seletivo (%)", fontsize=12)
ax.set_title("Proporçao de Uso das técnicas em IPv6\nASPP x Prefixo Mais Específico x Anúncio Seletivo", fontsize=14)

# Mostrar gráfico
plt.show()
