# transform_data.py
import pandas as pd
import numpy as np
import re


def transform_data_for_columns(extracted_data):
    """Transforma a lista de dicionários em uma lista de listas para corresponder aos nomes das colunas.

    Args:
        extracted_data (list): Lista de dicionários com os dados extraídos.

    Returns:
        list of lists: Lista de listas de dados para cada coluna.
    """
    columns_name = [
        "name",
        "age_max",
        "age_min",
        "sex",
        "warning_message",
        "race",
        "place_of_birth",
        "details",
        "occupations",
        "locations",
        "subjects",
        "aliases",
        "reward_text",
        "scars_and_marks",
        "caution",
    ]
    column_data = {col: [] for col in columns_name}
    for item in extracted_data:
        for col in columns_name:
            column_data[col].append(item.get(col, None))

    return [column_data[col] for col in columns_name]


def columns_with_values(extracted_data):
    """
    Cria um dicionário com várias chaves e os dados extraídos correspondentes.

    Args:
        extracted_data (list of lists): Uma lista de listas de dados a serem associadas aos nomes das colunas.

    Returns:
        dict: Um dicionário com as chaves sendo os nomes das colunas e os valores sendo as listas de dados correspondentes.
    """
    columns_name = [
        "name",
        "age_max",
        "age_min",
        "sex",
        "warning_message",
        "race",
        "place_of_birth",
        "details",
        "occupations",
        "locations",
        "subjects",
        "aliases",
        "reward_text",
        "scars_and_marks",
        "caution",
    ]
    if len(columns_name) != len(extracted_data):
        raise ValueError(
            "O número de nomes de colunas deve ser igual ao número de listas de dados."
        )

    return {columns_name[i]: extracted_data[i] for i in range(len(columns_name))}


def create_dataframe(data_dict):
    """
    Cria um DataFrame a partir de um dicionário de dados.

    Args:
        data_dict (dict): Um dicionário onde as chaves são os nomes das colunas e os valores são listas de dados.

    Returns:
        pd.DataFrame: Um DataFrame criado a partir do dicionário de dados.
    """
    return pd.DataFrame(data_dict)


def separete_values(df):
    """
    Concatena os valores das colunas de listas em uma string separada por vírgulas.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.

    Returns:
        pd.DataFrame: O DataFrame transformado com as listas concatenadas em strings.
    """
    for column in ["details", "occupations", "locations", "subjects", "aliases"]:
        df[column] = df[column].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else x
        )
    return df


def transform_values_for_nan(df):
    """
    Substitui valores específicos por NaN em um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.

    Returns:
        pd.DataFrame: O DataFrame transformado com os valores especificados substituídos por NaN.
    """
    return df.replace("Null", np.nan)


def transform_values_str_with_replace(df):
    """
    Substitui substrings específicas na coluna 'details' de um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.

    Returns:
        pd.DataFrame: O DataFrame com a coluna 'details' transformada.
    """
    strings_for_replace = [
        "<p>",
        "</p>",
        "<ul>",
        "</ul>",
        "\r",
        "\n",
        "<li>",
        "</li>",
        "<a>",
        "</a>",
    ]

    for string in strings_for_replace:
        df["details"] = df["details"].str.replace(re.escape(string), "", regex=True)
        df["reward_text"] = df["reward_text"].str.replace(
            re.escape(string), "", regex=True
        )
        df["caution"] = df["caution"].str.replace(re.escape(string), "", regex=True)

    return df


def change_type_values(df):
    """
    Altera o tipo de dados das colunas 'age_max' e 'age_min' em um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser transformado.

    Returns:
        pd.DataFrame: O DataFrame com as colunas 'age_max' e 'age_min' com o tipo de dados alterado.
    """
    for col in ["age_max", "age_min"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df
