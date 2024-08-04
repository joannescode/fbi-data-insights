import requests
from json import load
import pandas as pd
from time import sleep
import logging
from colorama import Fore, Style
from requests.exceptions import HTTPError
from src.requests_fuctions import create_session

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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


def request_wanted_fbi(url, headers, max_pages, max_pages_per_session, max_attempts):
    """Faz uma requisição GET para a página do FBI Wanted.

    Args:
        url (str): URL da página do FBI Wanted.
        headers (dict): Dicionário contendo os headers para a requisição.
        max_pages (int): Número máximo de páginas a ser requisitado no total.
        max_pages_per_session (int): Número máximo de páginas por sessão antes de reabrir a sessão.
        max_attempts (int): Número máximo de tentativas para cada conjunto de requisições.

    Returns:
        list: Lista de respostas das páginas requisitadas.
    """
    informations_response = []
    page_num = 1

    for attempt in range(max_attempts):
        session = create_session()

        while page_num <= max_pages:
            try:
                response = session.get(
                    url=url, params={"page": page_num}, headers=headers
                )
                response.raise_for_status()
                informations_response.append(response.json())

                if response.status_code == 200:
                    logging.info(
                        Fore.GREEN
                        + f"Requisição feita com sucesso para a página: {page_num}. Status Code: {response.status_code}"
                        + Style.RESET_ALL
                    )

                page_num += 1

                if (page_num - 1) % max_pages_per_session == 0:
                    logging.info(
                        Fore.YELLOW
                        + f"Reabrindo sessão após {max_pages_per_session} requisições."
                        + Style.RESET_ALL
                    )
                    session.close()
                    break

            except HTTPError as e:
                logging.error(
                    Fore.RED
                    + f"Ocorreu um erro durante a requisição, HTTPError: {e}"
                    + Style.RESET_ALL
                )
                session.close()
                break

        if page_num > max_pages:
            logging.info(
                Fore.GREEN
                + "Número máximo de páginas requisitadas com sucesso!."
                + Style.RESET_ALL
            )
            break

    return informations_response


def extract_data_wanted(informatios_response):
    """Extrai dados da resposta da requisição.

    Args:
        response (requests.models.Response): Resposta obtida pela função request_wanted_fbi.

    Returns:
        dict: Dados extraídos da resposta em formato de dicionário.
    """
    try:
        data = informatios_response
    except ValueError:
        raise ValueError("Erro ao decodificar a resposta JSON.")

    return data


def iteration_data_wanted(data):
    """Itera sobre os dados extraídos e retorna uma lista de informações específicas.

    Args:
        data (list): Lista de listas de dicionários com os dados extraídos da resposta.

    Returns:
        list: Lista de dicionários com os valores extraídos das chaves especificadas em cada item dos dados.
    """
    extracted_data = []

    for page_data in data:
        if "items" not in page_data:
            raise KeyError(
                f"Chave 'items' não encontrada nos dados da página. Chaves disponíveis: {list(page_data.keys())}"
            )

        for item in page_data.get("items", []):
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
                "caution": item.get("caution"),
            }
            extracted_data.append(person)

    return extracted_data
