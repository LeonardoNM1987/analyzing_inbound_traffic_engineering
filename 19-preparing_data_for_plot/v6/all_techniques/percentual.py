import pandas as pd

# Função para converter valores absolutos para percentuais
def convert_to_percent(input_file, output_file):
    # Ler o arquivo de entrada
    df = pd.read_csv(input_file, sep='|')

    # Colunas a serem convertidas para percentuais (excluindo #date e total_ases)
    columns_to_convert = df.columns[2:]

    # Converter valores absolutos para percentuais
    for col in columns_to_convert:
        df[col] = (df[col] / df['total_ases']) * 100

    # Ajustar formato para duas casas decimais
    df[columns_to_convert] = df[columns_to_convert].round(2)

    # Salvar o DataFrame em um novo arquivo
    df.to_csv(output_file, sep='|', index=False)
    print(f"Arquivo com valores percentuais salvo em: {output_file}")

# Caminho do arquivo de entrada e saída
input_file = "19-preparing_data_for_plot/v6/all_techniques/all_techniques_deploy.txt"  # Substitua pelo caminho do arquivo de entrada
output_file = "19-preparing_data_for_plot/v6/all_techniques/all_techniques_deploy_percentual.txt"  # Substitua pelo caminho desejado para o arquivo de saída

# Executar a conversão
convert_to_percent(input_file, output_file)
