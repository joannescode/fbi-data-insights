# Projeto ETL: Extração, Transformação e Carregamento de Dados

Este projeto tem como objetivo extrair dados da página do FBI Wanted, transformar essas informações e prepará-las para análise ou armazenamento. As etapas envolvidas são Extração, Transformação e Carregamento (a etapa de carregamento ainda está em desenvolvimento).

## Estrutura do Projeto

O projeto está estruturado em três principais módulos:

1. **Extração (extract_data.py)**
2. **Transformação (transform_data.py)**
3. **Carregamento (a ser desenvolvido)**

## Etapas do Projeto

### 1. Extração

A etapa de extração é responsável por obter dados da página do FBI Wanted. As funções envolvidas são:

- `load_json(json_path)`: Carrega a URL e os headers da requisição a partir de um arquivo JSON.
- `request_wanted_fbi(url, headers)`: Realiza uma requisição HTTP GET para obter os dados da página do FBI Wanted.
- `extract_data_wanted(response)`: Extrai dados JSON da resposta da requisição.
- `iteration_data_wanted(data)`: Itera sobre os dados extraídos e organiza as informações em uma lista de dicionários.

### 2. Transformação

Na etapa de transformação, os dados extraídos são preparados para análise. As funções envolvidas são:

- `transform_data_for_columns(extracted_data)`: Transforma a lista de dicionários em uma lista de listas para cada coluna.
- `columns_with_values(extracted_data)`: Cria um dicionário com chaves correspondentes aos nomes das colunas e valores correspondentes aos dados.
- `create_dataframe(data_dict)`: Cria um DataFrame a partir do dicionário de dados.
- `separete_values(df)`: Concatena listas de valores em strings separadas por vírgulas para as colunas `details`, `occupations`, `locations`, `subjects` e `aliases`.
- `transform_values_for_nan(df)`: Substitui valores específicos (neste caso, "Null") por NaN no DataFrame.
- `transform_values_str_with_replace(df)`: Remove tags HTML da coluna `details`.
- `change_type_values(df)`: Converte os tipos de dados das colunas `age_max` e `age_min` para o tipo `Int64`.

### 3. Carregamento

A etapa de carregamento (Load) ainda está em desenvolvimento. Normalmente, esta etapa envolve salvar o DataFrame transformado em um arquivo ou banco de dados para uso futuro. Detalhes adicionais serão incluídos quando esta etapa for desenvolvida.

## Como Executar

Para executar o projeto, siga estas etapas:

1. **Prepare o arquivo JSON**: Certifique-se de que o arquivo JSON contém a URL e os headers corretos para a requisição.

2. **Execute o script**: Utilize o script principal para executar as funções de extração e transformação. 

3. **Verifique o DataFrame**: Após a execução, o DataFrame transformado estará disponível para análise.

## Exemplo de Uso

Aqui está um exemplo de como o código pode ser usado:

```python
from src.extract_data import *
from src.transform_data import *

# Extração de Dados
url, headers = load_json("request_data.json")
response = request_wanted_fbi(url, headers)
data = extract_data_wanted(response)
extracted_data = iteration_data_wanted(data)

# Transformação de Dados
transformed_data = transform_data_for_columns(extracted_data)
data_dict = columns_with_values(transformed_data)
df = create_dataframe(data_dict)
df = separete_values(df)
df = transform_values_for_nan(df)
df = transform_values_str_with_replace(df)
df = change_type_values(df)

print(df.head())
