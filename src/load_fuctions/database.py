from dotenv import load_dotenv
from os import getenv
import mysql.connector
from mysql.connector import Error
import logging
from colorama import Fore, Style

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_credentials():
    """
    Carrega as credenciais do banco de dados a partir do arquivo .env.

    Returns:
        tuple: Um tupla contendo DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME.
    """
    load_dotenv()
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")

    return DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


def connect_to_database(username, password, host, database):
    """
    Conecta-se ao banco de dados MySQL utilizando as credenciais fornecidas.

    Args:
        username (str): Nome de usuário do banco de dados.
        password (str): Senha do banco de dados.
        host (str): Host do banco de dados.
        database (str): Nome do banco de dados.

    Returns:
        tuple: Uma tupla contendo a conexão e o cursor do banco de dados.

    Raises:
        Error: Se ocorrer um erro ao conectar ao banco de dados.
    """
    try:
        connection = mysql.connector.connect(
            user=username, password=password, host=host
        )
        if connection.is_connected():
            logging.info(
                Fore.GREEN
                + "Conexão ao banco de dados realizada com sucesso!"
                + Style.RESET_ALL
            )
            cursor = connection.cursor()
            return connection, cursor

    except Error as e:
        logging.error(
            Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET_ALL
        )
        return None, None


def disconnect_database(connection, cursor):
    """
    Encerra a conexão com o banco de dados e fecha o cursor.

    Args:
        connection: Conexão ao banco de dados.
        cursor: Cursor do banco de dados.
    """
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        logging.info(
            Fore.YELLOW
            + "Conexão ao banco de dados encerrada com sucesso."
            + Style.RESET_ALL
        )
