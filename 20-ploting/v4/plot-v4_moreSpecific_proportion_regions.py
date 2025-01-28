############################# Bloco de Configuração do Gráfico ##########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from _plot_compact_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR)


# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 80001, 20000)
# Limites do eixo Y
Y_LIM = (0, 80000)


def configurar_grafico(fig, ax):
    """Configura o layout e estilo do gráfico."""
    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    #ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax.set_ylabel('ASes (%)', fontsize=FONTSIZE_LABEL)

    # Ajustar formato da data e marcações no eixo x
    ax.xaxis.set_major_formatter(DATE_FORMAT)
    ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS)
    ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)

    # Adicionar grid
    ax.grid(True, axis='y')
    ax.grid(True, axis='x', **GRID_MAJOR)
    ax.set_axisbelow(True)

    # Ajustar os limites do eixo y
    ax.set_ylim(0, 70)
    ax.set_yticks(np.arange(0, 71, 20))

    # Ajustar o layout para garantir que não haja espaços extras
    fig.tight_layout()
    # Ajustar espaço para o título
    plt.subplots_adjust(bottom=0.25)

########################################### Bloco de Dados e Plotagem ###################################
import os


regiao = 'ripencc'

# Carregar dados do arquivo
arquivo = '19-preparing_data_for_plot/v4/moreSpecific_proportion_regions.txt'
df = pd.read_csv(arquivo, sep='|')

# Filtrar dados para a região 'internet'
df_global = df[df['region'] == regiao]

# Convertendo a coluna 'date' para datetime
df_global['date'] = pd.to_datetime(df_global['date'], format='%Y%m%d')

# Função para gerar dados normalizados
def gerar_proporcoes(df):
    categorias = {
        '0.1% a 24.9%': df['from1to24'].values,
        '25% a 49.9%': df['from25to49'].values,
        '50% a 74.9%': df['from50to74'].values,
        '75% a 99%': df['from75to99'].values
    }
    totais = np.sum(list(categorias.values()), axis=0)
    proporcoes = {key: (value / totais) * 100 for key, value in categorias.items()}
    return proporcoes

# Gerar proporções para "internet"
proporcoes_global = gerar_proporcoes(df_global)

# Definindo cores contrastantes suaves para "internet"
cores_global = ['#1f77b4', '#ff7f0e', '#2ca02c', '#b82caa']

categorias = ['0.1% a 24.9% dos anúncios', '25% a 49.9% dos anúncios', '50% a 74.9% dos anúncios', '75% a 99.9% dos anúncios']

# Criar o gráfico
fig, ax = plt.subplots(figsize=FIGSIZE)
# Adicionar título e subtítulo
#fig.suptitle(f'Proporção de uso de Prefixo mais Específico \npor cada AS em seus anúncios - {regiao} ', fontsize=FONTSIZE_TITLE, fontweight='bold',y=0.95, x=0.53)
#ax.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)
# Plotar linhas para cada categoria
for (categoria, proporcao), cor in zip(proporcoes_global.items(), cores_global):
    ax.plot(df_global['date'], proporcao, label=categoria, color=cor, linewidth=3)

# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax)

# Adicionar a legenda

ax.title
# ax.legend(
#     loc='upper center',
#     title='Proporção de prefixos que são mais específicos, de cada AS',
#     title_fontsize=12,
#     bbox_to_anchor=(0.5, 1.28),
#     framealpha=1,
#     ncol=4,
#     fontsize=FONTSIZE_LEGEND
# )

# Ajustar os limites do eixo x para exibir todas as datas
#ax.set_xlim(df_global['date'].min() - pd.DateOffset(days=30), df_global['date'].max() + pd.DateOffset(days=30))
ax.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='24ME'))
ax.margins(x=0.01)

#plt.xticks(rotation=45)

output_folder = '20-ploting/v4/plot_dissertacao/moreSpecific'
output_path = os.path.join(output_folder, f'v4_moreSpecific_proportion_regions_{regiao}.png')
plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()
