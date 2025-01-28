import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Carregar o arquivo consolidado
#data = pd.read_csv("19-preparing_data_for_plot/v4/all_techniques/all_tech_proportion_consolidated_data.txt")
data = pd.read_csv("19-preparing_data_for_plot/v4/all_techniques/all_tech_proportion_consolidated_data.txt")

# Substituir valores ausentes por 0
# Calcular a matriz de correlação
correlation_matrix = data[["AS-Path Prepend", "Anúncio de Prefixo mais Específico", "Anúncio Seletivo"]].corr()

# Exibir a matriz
print("Matriz de Correlação Original:")
print(correlation_matrix)

# Criar um dicionário para renomear as técnicas
rename_mapping = {
    "AS-Path Prepend": "ASPP",
    "Anúncio de Prefixo mais Específico": "Anúncio de Prefixo\nMais Específico",
    "Anúncio Seletivo": "Anúncio\nSeletivo"
}

# Renomear as colunas e índices da matriz de correlação
correlation_matrix.rename(index=rename_mapping, columns=rename_mapping, inplace=True)

# Exibir a matriz renomeada
print("Matriz de Correlação Renomeada:")
print(correlation_matrix)
# Criar o mapa de calor
sns.heatmap(
    correlation_matrix,
    annot=True,  # Exibe os números dentro do mapa
    annot_kws={"size": 15},  # Tamanho dos números no plot
    cmap="coolwarm",  # Paleta de cores
    cbar=True,  # Exibir barra de cores
    #xticklabels={"fontsize": 14},  # Tamanho das legendas no eixo X
    #yticklabels={"fontsize": 14}   # Tamanho das legendas no eixo Y
)

plt.xticks(rotation=0)
# Ajustar a posição do título (opcional)
#plt.title("Correlação entre Técnicas de Engenharia de Tráfego", fontsize=14, pad=20)

# Salvar o gráfico
output_folder = '20-ploting/v4/plot_dissertacao'
output_path = os.path.join(output_folder, f'v4_all_techniques_proportion_correlation.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
