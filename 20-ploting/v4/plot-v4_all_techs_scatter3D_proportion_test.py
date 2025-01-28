import matplotlib.pyplot as plt
import pandas as pd

# Nome do arquivo com os dados
input_file = "19-preparing_data_for_plot/v4/all_techs_asn_proportion_average_v4.txt"

# Configuração de filtro para valores nulos
filter_null_values = True  # Alterar para False para desabilitar o filtro

# Ler o arquivo em um DataFrame
df = pd.read_csv(input_file, sep="|")

# Filtrar apenas os ASNs com valores nas três colunas, se habilitado
if filter_null_values:
    filtered_df = df.dropna(subset=["aspp_average", "moreSpecific_average", "selective_average"])
else:
    filtered_df = df

# Criar histogramas bidimensionais (heatmaps)
fig, axs = plt.subplots(1, 3, figsize=(18, 6), tight_layout=True)

# ASPP vs More Specific
axs[0].hist2d(
    filtered_df["aspp_average"],
    filtered_df["moreSpecific_average"],
    bins=50, cmap="viridis"
)
axs[0].set_title("ASPP vs More Specific")
axs[0].set_xlabel("ASPP Average")
axs[0].set_ylabel("More Specific Average")

# ASPP vs Selective
axs[1].hist2d(
    filtered_df["aspp_average"],
    filtered_df["selective_average"],
    bins=50, cmap="viridis"
)
axs[1].set_title("ASPP vs Selective")
axs[1].set_xlabel("ASPP Average")
axs[1].set_ylabel("Selective Average")

# More Specific vs Selective
axs[2].hist2d(
    filtered_df["moreSpecific_average"],
    filtered_df["selective_average"],
    bins=50, cmap="viridis"
)
axs[2].set_title("More Specific vs Selective")
axs[2].set_xlabel("More Specific Average")
axs[2].set_ylabel("Selective Average")

# Adicionar barras de cores
for ax in axs:
    cbar = plt.colorbar(ax.collections[0], ax=ax, shrink=0.75)
    cbar.set_label("Densidade")

# Mostrar gráficos
plt.show()
