from src.extract_fuctions.extract_data import (
    load_json,
    request_wanted_fbi,
    extract_data_wanted,
    iteration_data_wanted,
)
from src.transform_fuctions.transform_data import (
    transform_data_for_columns,
    columns_with_values,
    create_dataframe,
    separete_values,
    transform_values_for_nan,
    transform_values_str_with_replace,
    change_type_values,
)
from src.load_fuctions.env_functions import user_auth_interaction, create_env_file
from src.load_fuctions.mysql_database import (
    get_credentials,
    connect_to_mysql,
    connect_to_database,
    disconnect_database
)
from src.load_fuctions.query_fuctions import create_database, show_databases
import logging
from colorama import Fore, Style
import os

JSON_PATH = "src/extract_fuctions/request_data.json"
ENV_PATH = "src/load_fuctions/.env"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Extract Data
logging.info(
    Fore.YELLOW
    + f"Iniciando etapa de coleta de dados da FBI Wanted:\n"
    + Style.RESET_ALL
)

url, headers = load_json(
    json_path=JSON_PATH
)
response = request_wanted_fbi(
    url=url, headers=headers, max_pages=50, max_pages_per_session=10, max_attempts=5
)
response_json = extract_data_wanted(informatios_response=response)
extract_data = iteration_data_wanted(data=response_json)

# Transform Data
extract_data = transform_data_for_columns(extracted_data=extract_data)
data_dict = columns_with_values(extracted_data=extract_data)
df = create_dataframe(data_dict=data_dict)
df = separete_values(df=df)
df = transform_values_for_nan(df=df)
df = transform_values_str_with_replace(df=df)
df = change_type_values(df=df)

logging.info(
    Fore.GREEN + f"Dados coletados e tratados com sucesso:\n" + Style.RESET_ALL
)
print(df.head())

# Load Data
try:
    if os.path.exists(ENV_PATH):
        logging.info(Fore.GREEN + "Dot env já criado anteriormente." + Style.RESET_ALL)
        pass
    
    elif not os.path.exists(ENV_PATH):
        db_username, db_password, db_host, db_name = user_auth_interaction()
        create_env_file(
            db_username=db_username,
            db_password=db_password,
            db_host=db_host,
            db_name=db_name,
        )
    username, password, host, database = get_credentials()
    connection, cursor = connect_to_mysql(
        username=username, password=password, host=host
    )
    create_database(cursor=cursor, database=database)
    show_databases(cursor=cursor)
    connect_to_database(user=username, password=password, host=host, database=database, connection=connection)
    
    ## TODO:
    # 1 - Criar database para inserção dos dados; OK
    # 2 - Criar tabela dentro do database;
    # 3 - Especificar o nome das colunas baseando nos nomes presentes no dataframe;
    # 4 - Inserir os dados em suas respectivas colunas.

finally:
    disconnect_database(connection=connection, cursor=cursor)
