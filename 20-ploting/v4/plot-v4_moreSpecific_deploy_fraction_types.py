############################# Bloco de Configuração do Gráfico ##########################################
import matplotlib.pyplot as plt
from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR,CORES_TYPES)

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 80001, 20000)
# Limites do eixo Y
Y_LIM = (0, 80000)

def configurar_grafico(fig, ax1):
    """Configura o layout e estilo do gráfico."""
    from matplotlib.ticker import FuncFormatter

    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    ax1.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax1.set_ylabel('Fração de ASes (%)', fontsize=FONTSIZE_LABEL)
    ax1.set_ylim(0, 50)
    ax1.set_yticks(range(0, 51, 10))
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
    plt.subplots_adjust(bottom=0.20)

##############################################################################################################################

########################################### Bloco de Dados e Plotagem ##########################################
import pandas as pd
import os
import datetime

# Caminho para o arquivo consolidado
arquivo = '19-preparing_data_for_plot/v4/more_specific_deploy_types.txt'

# Ler o arquivo em um DataFrame
df = pd.read_csv(arquivo, sep='|', comment='#', header=0)

# Renomear as colunas para facilitar a manipulação
df.columns = ["tipo", "data", "observed_ases", "using_moreSpecific","moreSpecific_fraction"]

# Converter a coluna 'data' para o formato de data
df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')


tipos = ["internet", "business", "education", "government", "hosting", "isp", "none"]
dfs = {tipo: df[df['tipo'] == tipo][['data', 'observed_ases', 'using_moreSpecific']].reset_index(drop=True) for tipo in tipos}

# Criar um DataFrame para armazenar os dados de todas as regiões
df_final = pd.DataFrame()

for tipo in tipos:
    
    total_internet = dfs['internet'].set_index('data')['observed_ases']

    # Calcular a porcentagem baseada no total global
    dfs[tipo]['Porcentagem'] = (dfs[tipo]['using_moreSpecific'] / dfs[tipo]['data'].map(total_internet)) * 100


    
    
    # # Calcular a porcentagem de ASNs com prepends observados
    # dfs[tipo]['Porcentagem'] = (dfs[tipo]['using_moreSpecific'] / dfs[tipo]['observed_ases']) * 100

    # Adicionar uma coluna para a região
    dfs[tipo]['tipo'] = tipo

    # Concatenar ao DataFrame final
    df_final = pd.concat([df_final, dfs[tipo]])

# Criar o gráfico
fig, ax1 = plt.subplots(figsize=FIGSIZE)

# Adicionar título e subtítulo
#fig.suptitle('Fração de ASes usando ASPP de acordo com o tipo de AS', fontsize=FONTSIZE_TITLE, fontweight='bold', y=0.95)
#ax1.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)

# Plotar cada região
for tipo in tipos:
    df_tipo = df_final[df_final['tipo'] == tipo]
    label = 'internet' if tipo == 'internet' else tipo
    linestyle = '-' if tipo == 'internet' else '-'
    linewidth = 3 if tipo == 'internet' else 2
    ax1.plot(df_tipo['data'], df_tipo['Porcentagem'], label=label, color=CORES_TYPES[tipo], linestyle=linestyle, linewidth=linewidth)

# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax1)

# Obter handles e labels das legendas
handles, labels = ax1.get_legend_handles_labels()
order = ["internet", "business", "education", "government", "hosting", "isp", "none"]
# Reordenar handles e labels
handles = [handles[labels.index(label)] for label in order]
translated_labels = {
    'internet': 'Internet',
    'business': 'Negócios',
    'education': 'Educação',
    'government': 'Governo',
    'hosting': 'Hospedagem',
    'isp': 'Provedor de Serviços de Internet (ISP)',
    'none': 'Não Identificado'
}
labels = [translated_labels[label] for label in order]
# Adicionar a legenda com a ordem ajustada
ax1.legend(handles, labels, loc='upper left', ncol=3, fontsize=FONTSIZE_LEGEND, framealpha=1)

# Salvar o gráfico na pasta especificada
output_folder = '20-ploting/v4/plot_dissertacao/moreSpecific'  # Substitua pelo caminho da pasta de saída desejada
current_time = datetime.datetime.now().strftime('%d%m%y.%H%M')
output_path = os.path.join(output_folder, f'v4_moreSpecific_deploy_fraction_types.png')
plt.savefig(output_path)

# Mostrar o gráfico
plt.show()

