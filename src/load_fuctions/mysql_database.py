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
        tuple: Uma tupla contendo os valores de DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME.
    """
    load_dotenv()
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")

    return DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


def connect_to_mysql(username, password, host, database=None):
    """
    Estabelece uma conexão com o banco de dados MySQL.

    Args:
        username (str): Nome de usuário do banco de dados.
        password (str): Senha do banco de dados.
        host (str): Host do banco de dados (ex: localhost).
        database (str, optional): Nome do banco de dados. Padrão é None.

    Returns:
        tuple: Uma tupla contendo a conexão e o cursor do banco de dados.
               Retorna (None, None) em caso de falha na conexão.

    Raises:
        Error: Caso ocorra um erro ao tentar conectar ao banco de dados.
    """
    try:
        connection = mysql.connector.connect(
            user=username, password=password, host=host, database=database
        )
        if connection.is_connected():
            logging.info(
                Fore.GREEN
                + "Conexão ao MySQL realizada com sucesso!"
                + Style.RESET_ALL
            )
            cursor = connection.cursor(buffered=True)
            return connection, cursor

    except Error as e:
        logging.error(
            Fore.RED + f"Erro ao conectar ao MySQL: {e}" + Style.RESET_ALL
        )
        return None, None

def connect_to_database(user, password, host, database, connection):
    try:
        connect_to_mysql(username=user, password=password, host=host, database=database)
        if connection.is_connected():
            logging.info(
                Fore.GREEN
                + f"Conexão ao MySQL realizada com sucesso! Conectado ao banco de dados: {database}."
                + Style.RESET_ALL
            )
            cursor = connection.cursor(buffered=True)
            return connection, cursor
    except Error as e:
        logging.error(
            Fore.RED + f"Erro ao conectar ao banco de dados {database}: {e}" + Style.RESET_ALL
        )
        return None, None
    
def disconnect_database(connection, cursor):
    """
    Encerra a conexão com o banco de dados MySQL e fecha o cursor.

    Args:
        connection: A conexão com o banco de dados que deve ser encerrada.
        cursor: O cursor MySQL que deve ser fechado.

    Raises:
        Error: Caso ocorra um erro ao tentar encerrar a conexão ou fechar o cursor.
    """
    try:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logging.info(
                Fore.YELLOW
                + "Conexão ao banco de dados encerrada com sucesso."
                + Style.RESET_ALL
            )
        else:
            logging.info(Fore.YELLOW + "Não foi encontrada conexão com o banco de dados.")
    except Error as e:
        logging.error(
            Fore.RED + f"Erro ao tentar realizar a desconexão com o MySQL: {e}" + Style.RESET_ALL
        ) 
