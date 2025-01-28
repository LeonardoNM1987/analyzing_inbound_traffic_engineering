############################# Bloco de Configuração do Gráfico ##########################################
import matplotlib.pyplot as plt
from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR,CORES)

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 90001, 10000)
# Limites do eixo Y
Y_LIM = (0, 90000)


def configurar_grafico(fig, ax1):
    """Configura o layout e estilo do gráfico."""
    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    ax1.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax1.set_ylabel('Sistemas Autônomos', fontsize=FONTSIZE_LABEL)
    ax1.set_ylim(Y_LIM)
    ax1.set_yticks(Y_TICKS)
    ax1.tick_params(axis='y', labelsize=FONTSIZE_TICKS)
    ax1.tick_params(axis='x', labelsize=FONTSIZE_TICKS)

    # Ajustar formato da data e marcações no eixo x
    ax1.xaxis.set_major_formatter(DATE_FORMAT)
    ax1.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='12ME'))
    plt.xticks(rotation=45)

    # Adicionar grade
    ax1.grid(True, **GRID_MAJOR)
    ax1.margins(x=0.01) # margem lateral entre resultados e borda do gráfico
    # Ajustar o layout para garantir que não haja espaços extras
    fig.tight_layout()
    # Ajustar espaço para o título
    #plt.subplots_adjust(top=0.85)




##############################################################################################################################



########################################### Bloco de Dados e Plotagem ##########################################
import pandas as pd
import os

# Caminho para o arquivo consolidado
arquivo = '19-preparing_data_for_plot/v4/ases_per_region.txt'

# Ler o arquivo em um DataFrame
df = pd.read_csv(arquivo, sep='|', comment='#', header=0, names=["data", "total_valid_ases", "afrinic", "arin", "apnic", "lacnic", "ripencc"])

# Converter a coluna 'data' para o formato de data
df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')

# Selecionar apenas as colunas de interesse
regioes = ['afrinic', 'arin', 'apnic', 'lacnic', 'ripencc']
df = df[['data'] + regioes]

# Calcular a soma de todas as regiões para representar a Internet
df['internet'] = df[regioes].sum(axis=1)

# Criar o gráfico
fig, ax1 = plt.subplots(figsize=FIGSIZE)

# Adicionar título e subtítulo
#fig.suptitle('ASes anunciando prefixos IPv4 ao longo do tempo', fontsize=FONTSIZE_TITLE, fontweight='bold',  y=0.95, x=0.53)
#ax1.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)

# Adicionar as linhas das regiões
for regiao in regioes:
    ax1.plot(df['data'], df[regiao], linestyle='-', label=regiao.upper(), color=CORES[regiao], linewidth=2)

# Adicionar a linha para a Internet
ax1.plot(df['data'], df['internet'], linestyle='-', label='Internet', color=CORES['internet'], linewidth=3)

# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax1)

# Adicionar a legenda
handles, labels = ax1.get_legend_handles_labels()
order = ['Internet', 'ARIN', 'LACNIC', 'APNIC', 'AFRINIC', 'RIPENCC']
handles = [handles[labels.index(label)] for label in order]
labels = [labels[labels.index(label)] for label in order]
ax1.legend(handles, labels, loc='upper left', bbox_to_anchor=(0, 1), ncol=3, fontsize=FONTSIZE_LEGEND, framealpha=1)

output_folder = '20-ploting/v4/plot_dissertacao'
output_path = os.path.join(output_folder, f'v4_ases_announcing_prefixes_regions.png')
plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()

##############################################################################################################################