# # plot_config.py
import matplotlib.pyplot as plt
import numpy as np

# Configurações de tamanho de figura
FIGSIZE = (12, 4)
# Configurações de tamanho de fonte
FONTSIZE_LABEL = 9
FONTSIZE_TITLE = 18
FONTSIZE_SUBTITLE = 12
FONTSIZE_LEGEND = 11
FONTSIZE_TICKS = 8
# Configurações de formatação de data
DATE_FORMAT = plt.matplotlib.dates.DateFormatter('jun/%y')
# Configurações de grid
GRID_MAJOR = {'which': 'major', 'linestyle': '-', 'linewidth': 0.4}
GRID_MINOR = {'which': 'both', 'linestyle': '-', 'linewidth': 0.4}
SUBTITLE = "Protocolo IPv4 | Coletores: RipeRIS, RouteViews e PCH | Período: 15/06/14 à 15/06/24"
CORES = {
    'internet': '#fa0202',
    'afrinic': '#D55E00',
    'arin': '#009E73',
    'apnic': '#0072B2',
    'lacnic': '#595959',
    'ripencc': '#E69F00'
}
CORES_TYPES = {
    'internet': '#fa0202',
    'business': '#D55E00',
    'education': '#009E73',
    'government': '#0072B2',
    'hosting': '#595959',
    'isp': '#E69F00',
    'none': '#CC00CC'
}

CORES_TYPES_2 = {
    'total': '#fa0202',
    'business': '#D55E00',
    'education': '#009E73',
    'government': '#0072B2',
    'hosting': '#595959',
    'isp': '#E69F00',
    'none': '#CC00CC'
}
