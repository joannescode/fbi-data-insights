import logging
from colorama import Fore, Style
from mysql.connector import Error


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_database(cursor, database):
    """
    Cria um banco de dados MySQL se ele não existir.

    Args:
        cursor: O cursor MySQL usado para executar comandos SQL.
        database (str): Nome do banco de dados a ser criado.

    Raises:
        Error: Caso ocorra um erro ao tentar criar o banco de dados.
    """
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")        
        logging.info(Fore.GREEN + f"\nDatabase {database} criado com sucesso!" + Style.RESET_ALL)
    except Error as e:
        logging.error(
            Fore.RED + f"Erro ao tentar criar o database: {e}" + Style.RESET_ALL
        )  
        
def show_databases(cursor):
    """
    Exibe os bancos de dados disponíveis no servidor MySQL.

    Args:
        cursor: O cursor MySQL usado para executar comandos SQL.

    Raises:
        Error: Caso ocorra um erro ao tentar listar os bancos de dados.
    """
    try:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        if databases:
            logging.info(Fore.GREEN + "Bancos de dados disponíveis:" + Style.RESET_ALL)
            for db in databases:
                logging.info(Fore.BLUE + f" - {db[0]}" + Style.RESET_ALL)
        else:
            logging.info(Fore.YELLOW + "Nenhum banco de dados encontrado." + Style.RESET_ALL)
            
    except Error as e:
        logging.error(
            Fore.RED + f"ERRO: {e}" + Style.RESET_ALL
        )    
    