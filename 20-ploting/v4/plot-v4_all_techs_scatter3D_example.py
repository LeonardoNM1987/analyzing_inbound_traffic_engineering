import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Dados fornecidos
data = {
    "asn": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27],
    "aspp_average": [15.65, 16.73, 23.66, 16.67, None, 4.0, 7.69, 74.71, 74.0, 79.17, None, 79.92, 25.0, 95.28, None, 50.0, 28.0, 15.02, 85.0, 92.68, 84.73, 53.57, 100.0, None, 77.12, 78.02],
    "moreSpecific_average": [7.34, 12.72, 5.25, 8.81, 12.86, 9.35, 9.08, 27.14, 18.94, 26.53, 25.0, 14.63, 13.67, 27.18, 50.0, 46.97, 25.16, 36.36, 16.85, 24.01, None, 28.21, None, 17.49, 32.95, 22.69],
    "selective_average": [100.0, 100.0, 100.0, 99.19, 100.0, 100.0, 100.0, 93.11, 100.0, 100.0, 100.0, 67.82, 100.0, 31.7, None, 100.0, 95.13, 42.39, 75.12, 34.95, 95.6, 100.0, 100.0, 3.04, 77.78, 100.0]
}

# Carregar dados em DataFrame
df = pd.DataFrame(data)

# Remover linhas com valores nulos
df = df.dropna()

# Configurar figura
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotar os dados
scatter = ax.scatter(
    df["aspp_average"],
    df["moreSpecific_average"],
    df["selective_average"],
    c=df["selective_average"],
    cmap="viridis",
    s=50
)

# Adicionar rótulos
ax.set_xlabel("ASPP Average")
ax.set_ylabel("More Specific Average")
ax.set_zlabel("Selective Average")
ax.set_title("3D Scatter Plot: ASN Proportions by Technique")

# Adicionar barra de cores
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
cbar.set_label("Selective Average (%)")

# Mostrar gráfico
plt.show()
