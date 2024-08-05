import logging
from colorama import Fore, Style

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def user_auth_interaction():
    """
    Solicita ao usuário as informações do banco de dados e as retorna.

    Returns:
        tuple: Uma tupla contendo db_username, db_password, db_host, db_name.
    """
    logging.info(
        "Por favor, digite as informações do banco de dados: username, password, host e name."
    )

    db_username = input("Digite o username: ")
    db_password = input("Digite o password: ")
    db_host = input("Digite o host: ")
    db_name = input("Digite o nome do banco de dados: ")

    return db_username, db_password, db_host, db_name


def create_env_file(db_username, db_password, db_host, db_name, file_path="src/load_fuctions/.env"):
    """
    Cria um arquivo .env com as credenciais fornecidas para o banco de dados.

    Args:
        db_username (str): Nome de usuário do banco de dados.
        db_password (str): Senha do banco de dados.
        db_host (str): Host do banco de dados.
        db_name (str): Nome do banco de dados.
        file_path (str): Caminho para o arquivo .env (default: ".env").

    Raises:
        Exception: Se ocorrer um erro ao escrever o arquivo .env.
    """
    env_content = (
        f"DB_USERNAME={db_username}\n"
        f"DB_PASSWORD={db_password}\n"
        f"DB_HOST={db_host}\n"
        f"DB_NAME={db_name}\n"
    )

    try:
        with open(file_path, "w") as env_file:
            env_file.write(env_content)
        logging.info(
            Fore.GREEN + f".env escrito com sucesso em: {file_path}." + Style.RESET_ALL
        )
    except Exception as e:
        logging.error(
            Fore.RED + f"Erro ao tentar escrever o .env: {e}." + Style.RESET_ALL
        )
