############################# Bloco de Configuração do Gráfico ##########################################
import matplotlib.pyplot as plt
from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR,CORES)

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 30001, 5000)
# Limites do eixo Y
Y_LIM = (0, 30000)

def configurar_grafico(fig, ax1):
    """Configura o layout e estilo do gráfico."""
    from matplotlib.ticker import FuncFormatter

    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    ax1.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax1.set_ylabel('Sistemas Autônomos', fontsize=FONTSIZE_LABEL)
    ax1.set_ylim(Y_LIM)
    ax1.set_yticks(Y_TICKS)
    ax1.tick_params(axis='y', labelsize=FONTSIZE_TICKS)
    ax1.tick_params(axis='x', labelsize=FONTSIZE_TICKS)

    # Ajustar formato da data e marcações no eixo x
    ax1.xaxis.set_major_formatter(DATE_FORMAT)
    ax1.set_xticks(pd.date_range(start='2014-06-01', end='2024-07-01', freq='12ME'))
    plt.xticks(rotation=45)

    # Adicionar grid
    ax1.grid(True, **GRID_MAJOR)
    ax1.margins(x=0.01)  # margem lateral entre resultados e borda do gráfico

    # Ajustar o layout para garantir que não haja espaços extras
    fig.tight_layout()
    # Ajustar espaço para o título
    #plt.subplots_adjust(top=0.85)
    #plt.subplots_adjust(bottom=0.20)

##############################################################################################################################

########################################### Bloco de Dados e Plotagem ##########################################
import pandas as pd
import os
import datetime

# Caminho para o arquivo consolidado
arquivo = '19-preparing_data_for_plot/v4/aspp_deploy_regions.txt'

# Ler o arquivo em um DataFrame
df = pd.read_csv(arquivo, sep='|', comment='#', header=0)

# Renomear as colunas para facilitar a manipulação
df.columns = ["regiao", "data", "total_asns", "quantidade_prepends"]

# Converter a coluna 'data' para o formato de data
df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')

# Filtrar apenas as regiões de interesse (excluindo 'global')
regioes = ['arin', 'lacnic', 'apnic', 'afrinic', 'ripencc', 'internet']
dfs = {regiao: df[df['regiao'] == regiao][['data', 'quantidade_prepends']].reset_index(drop=True) for regiao in regioes}

# Criar um DataFrame para armazenar os dados de todas as regiões
df_final = pd.DataFrame()

for regiao in regioes:
    # Adicionar uma coluna para a região
    dfs[regiao]['Regiao'] = regiao

    # Concatenar ao DataFrame final
    df_final = pd.concat([df_final, dfs[regiao]])

# Criar o gráfico
fig, ax1 = plt.subplots(figsize=FIGSIZE)

# Adicionar título e subtítulo
#fig.suptitle('Quantidade de ASes usando ASPP regionalmente', fontsize=FONTSIZE_TITLE, fontweight='bold', y=0.95, x=0.53)
#ax1.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)

# Plotar cada região
for regiao in regioes:
    df_regiao = df_final[df_final['Regiao'] == regiao]
    label = 'Internet' if regiao == 'internet' else regiao.upper()
    linestyle = '-' if regiao == 'internet' else '-'
    linewidth = 4 if regiao == 'internet' else 2
    ax1.plot(df_regiao['data'], df_regiao['quantidade_prepends'], label=label, color=CORES[regiao], linestyle=linestyle, linewidth=linewidth)

# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax1)

# Obter handles e labels das legendas
handles, labels = ax1.get_legend_handles_labels()
order = ['Internet', 'ARIN', 'LACNIC', 'APNIC', 'AFRINIC', 'RIPENCC']
# Reordenar handles e labels
handles = [handles[labels.index(label)] for label in order]
labels = [labels[labels.index(label)] for label in order]
# Adicionar a legenda com a ordem ajustada
ax1.legend(handles, labels, loc='upper left', ncol=3, fontsize=FONTSIZE_LEGEND, framealpha=1)

# Salvar o gráfico na pasta especificada
output_folder = '20-ploting/v4/plot_dissertacao'
current_time = datetime.datetime.now().strftime('%d%m%y.%H%M')
output_path = os.path.join(output_folder, f'v4_aspp_deploy_absolute_regions.png')
plt.savefig(output_path)

# Mostrar o gráfico
plt.show()
##############################################################################################################################
