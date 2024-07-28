import pandas as pd
import numpy as np
from pandas.core.interchange.dataframe_protocol import Column

def transform_data_for_columns(extracted_data, columns_name):
    """Transforma a lista de dicionários em uma lista de listas para corresponder aos nomes das colunas.

    Args:
        extracted_data (list): Lista de dicionários com os dados extraídos.
        columns_name (list): Lista de nomes das colunas.

    Returns:
        list of lists: Lista de listas de dados para cada coluna.
    """
    column_data = {col: [] for col in columns_name}
    for item in extracted_data:
        for col in columns_name:
            column_data[col].append(item.get(col, None))
    return [column_data[col] for col in columns_name]

def columns_with_values(name_columns, extracted_data):
    """
    Cria um dicionário com várias chaves e os dados extraídos correspondentes.

    Args:
        name_columns (list): Uma lista de nomes de colunas.
        extracted_data (list of lists): Uma lista de listas de dados a serem associadas aos nomes das colunas.

    Returns:
        dict: Um dicionário com as chaves sendo os nomes das colunas e os valores sendo as listas de dados correspondentes.
    """
    if len(name_columns) != len(extracted_data):
        raise ValueError("O número de nomes de colunas deve ser igual ao número de listas de dados.")

    return {name_columns[i]: extracted_data[i] for i in range(len(name_columns))}

def create_dataframe(data_dict):
    """
    Cria um DataFrame a partir de um dicionário de dados.

    Args:
        data_dict (dict): Um dicionário onde as chaves são os nomes das colunas e os valores são listas de dados.

    Returns:
        pd.DataFrame: Um DataFrame criado a partir do dicionário de dados.
    """
    return pd.DataFrame(data_dict)

def transform_values_for_nan(df, value_for_transform):
    """
    Substitui valores específicos por NaN em um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.
        value_for_transform (object): O valor a ser substituído por NaN.

    Returns:
        pd.DataFrame: O DataFrame transformado com os valores especificados substituídos por NaN.
    """
    return df.replace(value_for_transform, np.nan)

def transform_values_str_with_replace(df, column_name, values, value_to_replace):
    """
    Substitui uma substring por outra em uma coluna específica de um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.
        column_name (str): O nome da coluna em que a substituição será feita.
        value (list): A lista contendo substring a ser substituída.
        value_to_replace (str): A substring substituta.

    Returns:
        pd.DataFrame: O DataFrame com a coluna transformada.
    """
    for value in values:
        df[column_name] = df[column_name].str.replace(value, value_to_replace)
    return df

def change_type_values(df, column_name):
    """
    Altera o tipo de dados de uma coluna específica em um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.
        column_name (str): O nome da coluna cujo tipo de dados será alterado.
        type_data (type): O novo tipo de dados para a coluna.

    Returns:
        pd.DataFrame: O DataFrame com a coluna de tipo de dados alterado.
    """
    print("Deseja alterar o valor final da coluna para Int64? Digite 1 para sim, do contrário digite 0 para não.")
    resposta = input()

    try:
        resposta = int(resposta)
    except ValueError:
        print("Entrada inválida. Por favor, digite 1 para sim ou 0 para não.")
        return df

    if resposta == 0:
        print("Defina o type data para a coluna selecionada na função.")
        type_data = input()
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(type_data)

    elif resposta == 1:
        print("Passe o tipo de dado que deseja que seja alterado inicialmente, exemplo: float")
        type_data = input()

        try:
            df[column_name] = df[column_name].astype(type_data)
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype("Int64")
            print(f"Valor da {column_name} alterado primeiramente para {type_data} e finalizado como Int64.")
        except ValueError:
            print(f"Tipo de dado '{type_data}' inválido.")
            return df
    else:
        print("Opção inválida. Por favor, digite 1 para sim ou 0 para não.")

    return df
