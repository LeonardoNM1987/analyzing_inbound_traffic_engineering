############################# Bloco de Configuração do Gráfico ##########################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR)


# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 80001, 20000)
# Limites do eixo Y
Y_LIM = (0, 80000)


def configurar_grafico(fig, ax):
    """Configura o layout e estilo do gráfico."""
    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax.set_ylabel('Fração de ASes (%)', fontsize=FONTSIZE_LABEL)

    # Ajustar formato da data e marcações no eixo x
    ax.xaxis.set_major_formatter(DATE_FORMAT)
    ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS)
    ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)

    # Adicionar grid
    ax.grid(True, axis='y')
    ax.grid(True, axis='x', **GRID_MAJOR)
    ax.set_axisbelow(True)
    #ax.margins(x=0.01)
    # Ajustar os limites do eixo y
    ax.set_ylim(0, 50)
    ax.set_yticks(np.arange(0, 51, 10))
    
    # Ajustar o layout para garantir que não haja espaços extras
    fig.tight_layout()
    # Ajustar espaço para o título
    #plt.subplots_adjust(top=0.82, bottom=0.25)
    #plt.subplots_adjust(bottom=0.15)
########################################### Bloco de Dados e Plotagem ###################################
import os


regiao = 'internet'

# Carregar dados do arquivo
arquivo = '19-preparing_data_for_plot/v6/aspp/aspp_intensity_regions.txt'
df = pd.read_csv(arquivo, sep='|')

# Filtrar dados para a região 'internet'
df_global = df[df['region'] == regiao]

# Convertendo a coluna 'date' para datetime
df_global['date'] = pd.to_datetime(df_global['date'], format='%Y%m%d')

# Função para gerar dados normalizados
def gerar_proporcoes(df):
    categorias = {
        'Tamanho 1': df['tam_1'].values,
        'Tamanho 2': df['tam_2'].values,
        'Tamanho 3': df['tam_3'].values,
        'Tamanho 4+': df['tam_4plus'].values
    }
    totais = np.sum(list(categorias.values()), axis=0)
    proporcoes = {key: (value / totais) * 100 for key, value in categorias.items()}
    return proporcoes

# Gerar proporções para "internet"
proporcoes_global = gerar_proporcoes(df_global)

# Definindo cores contrastantes suaves para "internet"
cores_global = ['#1f77b4', '#ff7f0e', '#2ca02c', '#b82caa']

categorias = ['1', '2', '3', '4+']

# Criar o gráfico
fig, ax = plt.subplots(figsize=FIGSIZE)
# Adicionar título e subtítulo
#fig.suptitle(f'Tamanhos de prepend mais utilizados pelos ASes - {regiao} ', fontsize=FONTSIZE_TITLE, fontweight='bold',y=0.95, x=0.53)
#ax.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=35)
# Plotar linhas para cada categoria
for (categoria, proporcao), cor in zip(proporcoes_global.items(), cores_global):
    ax.plot(df_global['date'], proporcao, label=categoria, color=cor, linewidth=3)

# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax)

# Adicionar a legenda

# ax.title
ax.legend(
    loc='upper center',
    title='Tamanhos de prepend',
    title_fontsize=FONTSIZE_LEGEND,
    #bbox_to_anchor=(0.5, 1.28),
    framealpha=1,
    ncol=4,
    fontsize=FONTSIZE_LEGEND
)
# Ajustar os limites do eixo x para exibir todas as datas
#ax.set_xlim(df_global['date'].min() - pd.DateOffset(days=30), df_global['date'].max() + pd.DateOffset(days=30))
ax.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='12ME'))
ax.margins(x=0.01)

plt.xticks(rotation=45)

output_folder = '20-ploting/v6/plot/aspp'
output_path = os.path.join(output_folder, f'v6_aspp_intensity_regions_{regiao}.png')
plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()


