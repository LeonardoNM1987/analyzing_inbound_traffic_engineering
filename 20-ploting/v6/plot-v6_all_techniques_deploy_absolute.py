import pandas as pd
import matplotlib.pyplot as plt

# Configuração do gráfico (importar as mesmas configurações do seu projeto)
from _plot_default_config import (SUBTITLE, FIGSIZE, FONTSIZE_LABEL, FONTSIZE_TITLE, FONTSIZE_SUBTITLE,
                                   FONTSIZE_LEGEND, FONTSIZE_TICKS, DATE_FORMAT)
GRID_MAJOR = {'which': 'major', 'linestyle': '-', 'linewidth': 0.3}
GRID_MINOR = {'which': 'both', 'linestyle': '-', 'linewidth': 0.3}

# Intervalos para ticks no eixo Y
Y_TICKS = range(0, 5001, 1500)
# Limites do eixo Y
Y_LIM = (0, 5000)

# Caminho do arquivo
arquivo = '19-preparing_data_for_plot/v6/all_techniques/all_techniques_deploy.txt'

# Ler o arquivo
df = pd.read_csv(arquivo, sep='|')

# Converter a coluna 'date' para o formato de data
df['date'] = pd.to_datetime(df['#date'], format='%Y%m%d')

# Configurar o gráfico
fig, ax = plt.subplots(figsize=FIGSIZE)


# Plotar as linhas com cores personalizadas
ax.plot(df['date'], df['all_three'], label="ASPP + Anúncio de Prefixo Mais Específico + Anúncio Seletivo", linestyle='-', linewidth=2, zorder=3, color='red')
ax.plot(df['date'], df['aspp_and_moreSpecific'], label="ASPP + Anúncio de Prefixo Mais Específico", linestyle='-', linewidth=2, color='blue')
ax.plot(df['date'], df['aspp_and_selective'], label="ASPP + Anúncio Seletivo", linestyle='-', linewidth=2, color='green')
ax.plot(df['date'], df['more_specific_and_selective'], label="Anúncio de Prefixo Mais Específico + Anúncio Seletivo", linestyle='-', linewidth=2, color='purple')
ax.plot(df['date'], df['just_aspp'], label="Somente ASPP", linestyle='-', linewidth=2, color='magenta')
ax.plot(df['date'], df['just_more_specific'], label="Somente Anúncio de Prefixo Mais Específico", linestyle='-', linewidth=2, color='orange')
ax.plot(df['date'], df['just_selective'], label="Somente Anúncio Seletivo", linestyle='-', linewidth=2, color='gray')

# Configurar eixos e legenda
ax.set_xlabel('Data', fontsize=FONTSIZE_LABEL)
ax.set_ylabel('Sistemas Autônomos', fontsize=FONTSIZE_LABEL)
#ax.set_title("Distribuição de Técnicas Utilizadas pelos ASes", fontsize=FONTSIZE_TITLE)
ax.xaxis.set_major_formatter(DATE_FORMAT)
ax.set_xticks(pd.date_range(start='2014-06-15', end='2024-07-15', freq='12ME'))
ax.tick_params(axis='x', labelsize=FONTSIZE_TICKS, rotation=45)
ax.tick_params(axis='y', labelsize=FONTSIZE_TICKS)
ax.grid(True, **GRID_MAJOR)
ax.margins(x=0.005)
ax.set_ylim(Y_LIM)
ax.set_yticks(Y_TICKS)
# Adicionar legenda
ax.legend(
    loc='upper left',
    title='Técnicas utilizadas',
    title_fontsize=FONTSIZE_LEGEND,
    #bbox_to_anchor=(0.5, 1.28),
    framealpha=1,
    ncol=1,
    fontsize=FONTSIZE_LEGEND
)



# Ajustar layout
fig.tight_layout()
plt.subplots_adjust(bottom=0.20)

# Salvar o gráfico
output_path = '20-ploting/v6/plot/all_techs/v6_all_techniques_deploy_absolute.png'
plt.savefig(output_path)

# Mostrar o gráfico
plt.show()
