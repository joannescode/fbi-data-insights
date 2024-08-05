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
from src.load_fuctions.database import (
    get_credentials,
    connect_to_database,
    disconnect_database,
)
import logging
from colorama import Fore, Style

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
    json_path="/home/joannes/Documents/dev/fbi-data-insights/src/extract_fuctions/request_data.json"
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
    db_username, db_password, db_host, db_name = user_auth_interaction()
    create_env_file(
        db_username=db_username,
        db_password=db_password,
        db_host=db_host,
        db_name=db_name,
    )
    username, password, host, database = get_credentials()
    connection, cursor = connect_to_database(
        username=username, password=password, host=host, database=database
    )

    ## TODO:
    # 1 - Criar database para inserção dos dados;
    # 2 - Criar tabela dentro do database;
    # 3 - Especificar o nome das colunas baseando nos nomes presentes no dataframe;
    # 4 - Inserir os dados em suas respectivas colunas.

finally:
    disconnect_database(connection=connection, cursor=cursor)
