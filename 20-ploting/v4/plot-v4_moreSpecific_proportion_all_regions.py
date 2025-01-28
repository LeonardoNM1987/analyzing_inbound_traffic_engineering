############################# Bloco de Configuração do Gráfico ##########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import matplotlib.gridspec as gridspec
from _plot_compact_config import (SUBTITLE, FIGSIZE, FONTSIZE_LABEL, FONTSIZE_TITLE, FONTSIZE_SUBTITLE, FONTSIZE_LEGEND, FONTSIZE_TICKS, DATE_FORMAT, GRID_MAJOR, GRID_MINOR)

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 80001, 20000)
# Limites do eixo Y
Y_LIM = (0, 80000)

def configurar_subplot(ax):
    """Configura o layout e estilo de um subplot."""
    #ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax.set_ylabel('ASes (%)', fontsize=FONTSIZE_LABEL)
    ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS)
    ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)   
    ax.grid(True, **GRID_MAJOR)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 50))
    ax.xaxis.set_major_formatter(DATE_FORMAT)
    

########################################### Bloco de Dados e Plotagem ###################################


# Carregar dados do arquivo
arquivo = '19-preparing_data_for_plot/v4/moreSpecific_proportion_regions.txt'
df = pd.read_csv(arquivo, sep='|')

# Converter a coluna 'date' para datetime
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Regiões para plotagem
regioes = ['apnic', 'lacnic', 'arin', 'afrinic', 'ripencc']

# Função para gerar dados normalizados
def gerar_proporcoes(df):
    categorias = {
        '0.1% a 24.9%': df['from1to24'].values,
        '25% a 49.9%': df['from25to49'].values,
        '50% a 74.9%': df['from50to74'].values,
        '75% a 99.9%': df['from75to99'].values
    }
    totais = np.sum(list(categorias.values()), axis=0)
    proporcoes = {key: (value / totais) * 100 for key, value in categorias.items()}
    return proporcoes

# Criar a figura com subplots
fig, axes = plt.subplots(3, 2, figsize=(8, 6))
axes = axes.flatten()

# Iterar pelas regiões e criar subplots
cores_global = ['#1f77b4', '#ff7f0e', '#2ca02c', '#b82caa']


for i, regiao in enumerate(regioes):
    ax = axes[i]
    df_regiao = df[df['region'] == regiao]
    proporcoes = gerar_proporcoes(df_regiao)
    
    # Plotar linhas para cada categoria
    for (categoria, proporcao), cor in zip(proporcoes.items(), cores_global):
        ax.plot(df_regiao['date'], proporcao, label=categoria, color=cor, linewidth=1)
        ax.margins(x=0.01)
        ax.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='24ME'))
        axes[-1].axis('off')  # Desativa o último subplot (à direita na linha inferior)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    ax.set_title(f'{regiao.upper()}', fontsize=FONTSIZE_SUBTITLE, fontweight='bold')
    #ax.set_title(f'Região: {regiao.upper()}', fontsize=FONTSIZE_SUBTITLE)
    configurar_subplot(ax)


handles, labels = ax.get_legend_handles_labels()  # Obter os rótulos das linhas do último subplot
fig.legend(
    handles=handles,
    labels=labels,
    loc='upper center',
    title='Fração de prefixos que os ASes anunciam de forma mais específica',
    title_fontsize=FONTSIZE_LEGEND,
    ncol=4,  # Número de colunas para distribuir os itens da legenda
    fontsize=FONTSIZE_LEGEND,
    bbox_to_anchor=(0.52, 0.95)  # Centralizado no topo, ajustando a posição
)


# Ajustar o layout da figura
fig.tight_layout()
fig.subplots_adjust(top=0.80, hspace=0.90)
#fig.suptitle('Nível Máximo de Desagregação por Região', fontsize=FONTSIZE_TITLE, fontweight='bold')


# Salvar o gráfico
output_folder = '20-ploting/v4/plot_dissertacao/moreSpecific'
output_path = os.path.join(output_folder, 'v4_moreSpecific_proportion_all_regions.png')
plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()

