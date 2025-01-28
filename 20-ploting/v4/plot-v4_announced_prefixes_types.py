############################# Bloco de Configuração do Gráfico ##########################################
import matplotlib.pyplot as plt
from _plot_default_config import (SUBTITLE,FIGSIZE,FONTSIZE_LABEL,FONTSIZE_TITLE,FONTSIZE_SUBTITLE,FONTSIZE_LEGEND,FONTSIZE_TICKS,DATE_FORMAT,GRID_MAJOR,GRID_MINOR,CORES_TYPES)


# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 1200001, 200000)
# Limites do eixo Y
Y_LIM = (0, 1200000)

def configurar_grafico(fig, ax1):
    """Configura o layout e estilo do gráfico."""
    from matplotlib.ticker import FuncFormatter
    
    # Ajustar os rótulos dos eixos com tamanho de fonte personalizado
    ax1.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
    ax1.set_ylabel('Prefixos IPv4', fontsize=FONTSIZE_LABEL)
    ax1.set_ylim(Y_LIM)
    ax1.set_yticks(Y_TICKS)
    ax1.tick_params(axis='y', labelsize=FONTSIZE_TICKS)
    ax1.tick_params(axis='x', labelsize=FONTSIZE_TICKS)

    # Formatação dos valores do eixo Y para exibir números inteiros completos
    def formatar_y(val, pos):
        return f'{int(val):,}'.replace(',', '.')
    ax1.yaxis.set_major_formatter(FuncFormatter(formatar_y))

    # Ajustar formato da data e marcações no eixo x
    ax1.xaxis.set_major_formatter(DATE_FORMAT)
    ax1.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='12ME'))
    plt.xticks(rotation=45)

    # Adicionar grade
    ax1.grid(True, **GRID_MAJOR)
    ax1.margins(x=0.01)  # margem lateral entre resultados e borda do gráfico
    # Ajustar o layout para garantir que não haja espaços extras
    fig.tight_layout()
    # Ajustar espaço para o título
    #plt.subplots_adjust(top=0.85)




##############################################################################################################################



########################################### Bloco de Dados e Plotagem ##########################################
import pandas as pd
import os

# Caminho para o arquivo consolidado
arquivo = '19-preparing_data_for_plot/v4/prefixes_announced_types.txt'

# Ler o arquivo em um DataFrame
df = pd.read_csv(arquivo, sep='|', comment='#', header=0, names=["data", "internet","business","education","government","hosting","isp","none"])

# Converter a coluna 'data' para o formato de data
df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')

# Selecionar apenas as colunas de interesse
tipos = ["internet","business", "education", "government", "hosting", "isp", "none"]
df = df[['data'] + tipos]

# Calcular a soma de todas as regiões para representar a Internet
#df['internet'] = df[tipos].sum(axis=1)

# Criar o gráfico
fig, ax1 = plt.subplots(figsize=FIGSIZE)

# Adicionar título e subtítulo
#fig.suptitle('Prefixos IPv4 anunciados ao longo do tempo por tipo de AS', fontsize=FONTSIZE_TITLE, fontweight='bold',y=0.95, x=0.53)
#ax1.set_title(SUBTITLE, fontsize=FONTSIZE_SUBTITLE, pad=15)

# Adicionar as linhas das regiões
for tipo in tipos:
    ax1.plot(df['data'], df[tipo], linestyle='-', label=tipo, color=CORES_TYPES[tipo], linewidth=2)

# Adicionar a linha para a Internet
ax1.plot(df['data'], df['internet'], linestyle='-', label='internet', color=CORES_TYPES['internet'], linewidth=3)



# Configurar o gráfico com o bloco reutilizável
configurar_grafico(fig, ax1)

# Adicionar a legenda
handles, labels = ax1.get_legend_handles_labels()
order = ['internet', 'business', 'education', 'government', 'hosting', 'isp', 'none']
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
ax1.legend(handles, labels, loc='upper left', bbox_to_anchor=(0, 1), ncol=3, fontsize=12, framealpha=1)

output_folder = '20-ploting/v4/plot_dissertacao'
output_path = os.path.join(output_folder, f'v4_announced_prefixes_types.png')

plt.savefig(output_path, bbox_inches='tight')

# Mostrar o gráfico
plt.show()

##############################################################################################################################