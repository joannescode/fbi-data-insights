# extract_data.py
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

    fbi_wanted_url = request_data_json["url"]
    request_headers = request_data_json["headers"]

    return fbi_wanted_url, request_headers


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
    session.close()

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


def iteration_data_wanted(data):
    """Itera sobre os dados extraídos e retorna uma lista de informações específicas.

    Args:
        data (dict): Dados extraídos da resposta em formato de dicionário.

    Returns:
        list: Lista de dicionários com os valores extraídos das chaves especificadas em cada item dos dados.
    """
    if "items" not in data:
        raise KeyError(f"Chave 'items' não encontrada nos dados. Chaves disponíveis: {list(data.keys())}")

    extracted_data = []
    for item in data.get("items", []):
        person = {
            "name": item.get("title"),
            "age_max": item.get("age_max"),
            "age_min": item.get("age_min"),
            "sex": item.get("sex"),
            "warning_message": item.get("warning_message"),
            "race": item.get("race_raw"),
            "place_of_birth": item.get("place_of_birth"),
            "details": item.get("details"),
            "occupations": item.get("occupations") or [],
            "locations": item.get("locations") or [],
            "subjects": item.get("subjects") or [],
            "aliases": item.get("aliases") or [],
            "reward_text": item.get("reward_text"),
            "scars_and_marks": item.get("scars_and_marks"),
            "caution": item.get("caution")
        }
        extracted_data.append(person)

    return extracted_data
