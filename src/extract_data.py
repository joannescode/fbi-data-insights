import requests
from json import load
import pandas as pd

def load_json(json_path):
    """Carrega um arquivo JSON com os requisitos para uma sessão de requisição.

    Args:
        json_path (str): Caminho para o arquivo JSON contendo a URL e os headers da requisição.

    Returns:
        tuple: Uma tupla contendo a URL para a página do FBI Wanted (str) e os headers da requisição (dict).
    """
    with open(json_path, "r") as file:
        request_data_json = load(file)

    fbi_wanted = request_data_json["url"]
    request_headers = request_data_json["headers"]

    return fbi_wanted, request_headers


def request_wanted_fbi(url, headers):
    """Faz uma requisição GET para a página do FBI Wanted.

    Args:
        url (str): URL da página do FBI Wanted.
        headers (dict): Dicionário contendo os headers para a requisição.

    Returns:
        requests.models.Response: Resposta da página requisitada.
    """
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    response.raise_for_status()

    return response


def extract_data_wanted(response):
    """Extrai dados da resposta da requisição.

    Args:
        response (requests.models.Response): Resposta obtida pela função request_wanted_fbi.

    Returns:
        dict: Dados extraídos da resposta em formato de dicionário.
    """
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Erro ao decodificar a resposta JSON.")

    return data


def iteration_data_wanted(data, info_data):
    """Itera sobre os dados extraídos e retorna uma lista de informações específicas.

    Args:
        data (dict): Dados extraídos da resposta em formato de dicionário.
        info_data (list): Lista de chaves específicas a serem extraídas de cada item nos dados.

    Returns:
        list: Lista de dicionários com os valores extraídos das chaves especificadas em cada item dos dados.
    """
    if "items" not in data:
        raise KeyError(f"Chave 'items' não encontrada nos dados. Chaves disponíveis: {list(data.keys())}")

    extracted_data = []
    for item in data["items"]:
        extracted_item = {key: item.get(key, None) for key in info_data}
        extracted_data.append(extracted_item)

    return extracted_data


def append_data(data_wanted):
    """Adiciona dados à lista de dados desejados.

    Args:
        data_wanted (list): Lista de dados extraídos.

    Returns:
        list: Lista com os dados adicionados.
    """
    data_wanted_list = []
    for data in data_wanted:
        if data:
            data_wanted_list.append(data)

    return data_wanted_list


def insert_values_in_csv_file(columns, values, filename):
    """Insere valores em um arquivo CSV.

    Args:
        columns (list): Lista de nomes das colunas.
        values (list): Lista de dicionários com os valores a serem inseridos.
        filename (str): Nome do arquivo CSV.

    Returns:
        None
    """
    df = pd.DataFrame(values, columns=columns)
    df.to_csv(filename, index=False)

# Exemplo de uso das funções
# if __name__ == "__main__":
#     json_path = "path/to/json_file.json"
#     info_data = ["field_name1", "field_name2"]  # Substitua pelos campos desejados
#     csv_filename = "output.csv"
#
#     url, headers = load_json(json_path)
#     response = request_wanted_fbi(url, headers)
#     data = extract_data_wanted(response)
#     extracted_data = iteration_data_wanted(data, info_data)
#     data_to_append = append_data(extracted_data)
#     insert_values_in_csv_file(info_data, data_to_append, csv_filename)
