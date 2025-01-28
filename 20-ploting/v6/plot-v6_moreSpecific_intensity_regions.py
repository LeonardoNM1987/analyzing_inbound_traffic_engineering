############################# Bloco de Configuração do Gráfico ##########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from _plot_compact_config import (SUBTITLE, FIGSIZE, FONTSIZE_LABEL, FONTSIZE_TITLE, FONTSIZE_SUBTITLE, FONTSIZE_LEGEND, FONTSIZE_TICKS, DATE_FORMAT, GRID_MAJOR, GRID_MINOR)

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 80001, 20000)
# Limites do eixo Y
Y_LIM = (0, 80000)

def configurar_subplot(ax):
    """Configura o layout e estilo de um subplot."""
    ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax.set_ylabel('Fração de ASes (%)', fontsize=FONTSIZE_LABEL)
    ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS)
    ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)   
    ax.grid(True, **GRID_MAJOR)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 25))
    ax.xaxis.set_major_formatter(DATE_FORMAT)
    #plt.xticks(rotation=45)

########################################### Bloco de Dados e Plotagem ###################################
# Caminho para o arquivo consolidado
arquivo = '19-preparing_data_for_plot/v6/moreSpecific/moreSpecific_intensity_regions.txt'
df = pd.read_csv(arquivo, sep='|')

# Converter a coluna 'date' para datetime
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Regiões para plotagem
regioes = ['apnic', 'lacnic', 'arin', 'afrinic', 'ripencc']

# Função para gerar dados normalizados
def gerar_proporcoes(df):
    categorias = {
        'Nível 1': df['disagg_1'].values,
        'Nível 2': df['disagg_2'].values,
        'Nível 3': df['disagg_3'].values,
        'Nível 4+': df['disagg_4plus'].values
    }
    totais = np.sum(list(categorias.values()), axis=0)
    proporcoes = {key: (value / totais) * 100 for key, value in categorias.items()}
    return proporcoes

# Criar a figura com subplots
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()

# Iterar pelas regiões e criar subplots
cores_global = ['#1f77b4', '#ff7f0e', '#2ca02c', '#b82caa']

for i, regiao in enumerate(regioes):
    ax = axes[i]
    df_regiao = df[df['#region'] == regiao]
    proporcoes = gerar_proporcoes(df_regiao)
    
    # Plotar linhas para cada categoria
    for (categoria, proporcao), cor in zip(proporcoes.items(), cores_global):
        ax.plot(df_regiao['date'], proporcao, label=categoria, color=cor, linewidth=2)

    ax.set_title(f'Região: {regiao.upper()}', fontsize=FONTSIZE_SUBTITLE)
    #ax.set_title(f'Região: {regiao.upper()}', fontsize=FONTSIZE_SUBTITLE)
    configurar_subplot(ax)
    #ax.legend(loc='upper left', fontsize=FONTSIZE_LEGEND)

# Ajustar o layout da figura
fig.tight_layout()
fig.subplots_adjust(top=0.93)
#fig.suptitle('Nível Máximo de Desagregação por Região', fontsize=FONTSIZE_TITLE, fontweight='bold')

# Salvar o gráfico
output_folder = '20-ploting/v6/plot/moreSpecific'
output_path = os.path.join(output_folder, 'v6_moreSpecific_intensity_regions_summary.png')
plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()


# ############################# Bloco de Configuração do Gráfico ##########################################

# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR)


# # Intervalos para ticks no eixo Y
# Y_TICKS = range(0, 80001, 20000)
# # Limites do eixo Y
# Y_LIM = (0, 80000)


# def configurar_grafico(fig, ax):
#     """Configura o layout e estilo do gráfico."""
#     # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
#     ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
#     ax.set_ylabel('Fração de ASes (%)', fontsize=FONTSIZE_LABEL)

#     # Ajustar formato da data e marcações no eixo x
#     ax.xaxis.set_major_formatter(DATE_FORMAT)
#     ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS)
#     ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)

#     # Adicionar grid
#     ax.grid(True, axis='y')
#     ax.grid(True, axis='x', **GRID_MAJOR)
#     ax.set_axisbelow(True)

#     # Ajustar os limites do eixo y
#     ax.set_ylim(0, 100)
#     ax.set_yticks(np.arange(0, 101, 20))

#     # Ajustar o layout para garantir que não haja espaços extras
#     fig.tight_layout()
#     # Ajustar espaço para o título
#     #plt.subplots_adjust(bottom=0.25)

# ########################################### Bloco de Dados e Plotagem ###################################
# import os


# regiao = 'internet'

# # Carregar dados do arquivo
# arquivo = '19-preparing_data_for_plot/v6/moreSpecific/moreSpecific_intensity_regions.txt'
# df = pd.read_csv(arquivo, sep='|')

# # Filtrar dados para a região 'internet'
# df_global = df[df['#region'] == regiao]

# # Convertendo a coluna 'date' para datetime
# df_global['date'] = pd.to_datetime(df_global['date'], format='%Y%m%d')

# # Função para gerar dados normalizados
# def gerar_proporcoes(df):
#     categorias = {
#         'Nível 1': df['disagg_1'].values,
#         'Nível 2': df['disagg_2'].values,
#         'Nível 3': df['disagg_3'].values,
#         'Nível 4+': df['disagg_4plus'].values
#     }
#     totais = np.sum(list(categorias.values()), axis=0)
#     proporcoes = {key: (value / totais) * 100 for key, value in categorias.items()}
#     return proporcoes

# # Gerar proporções para "internet"
# proporcoes_global = gerar_proporcoes(df_global)

# # Definindo cores contrastantes suaves para "internet"
# cores_global = ['#1f77b4', '#ff7f0e', '#2ca02c', '#b82caa']

# categorias = ['1', '2', '3', '4+']

# # Criar o gráfico
# fig, ax = plt.subplots(figsize=FIGSIZE)
# # Adicionar título e subtítulo
# #fig.suptitle(f'Nível máximo de desagregação que cada AS executa\n em seus prefixos mais específicos - {regiao} ', fontsize=FONTSIZE_TITLE, fontweight='bold',y=0.95, x=0.53)
# #ax.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)
# # Plotar linhas para cada categoria
# for (categoria, proporcao), cor in zip(proporcoes_global.items(), cores_global):
#     ax.plot(df_global['date'], proporcao, label=categoria, color=cor, linewidth=3)

# # Configurar o gráfico com o bloco reutilizável
# configurar_grafico(fig, ax)

# # Adicionar a legenda

# ax.title
# ax.legend(
#     loc='upper center',
#     title='Nível de Desagregação Máxima dos prefixos de cada AS',
#     title_fontsize=12,
#     #bbox_to_anchor=(0.5, 1.28),
#     framealpha=1,
#     ncol=4,
#     fontsize=FONTSIZE_LEGEND
# )

# # Ajustar os limites do eixo x para exibir todas as datas
# #ax.set_xlim(df_global['date'].min() - pd.DateOffset(days=30), df_global['date'].max() + pd.DateOffset(days=30))
# ax.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='12ME'))
# ax.margins(x=0.01)

# plt.xticks(rotation=45)

# output_folder = '20-ploting/v6/plot/moreSpecific'
# output_path = os.path.join(output_folder, f'v6_moreSpecific_intensity_regions_{regiao}.png')
# plt.savefig(output_path, bbox_inches='tight')

# # Mostrar o gráfico
# plt.show()


