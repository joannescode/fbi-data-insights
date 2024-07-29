import csv
from src.extract_data import (load_json, request_wanted_fbi,
    extract_data_wanted, iteration_data_wanted)
from src.transform_data import (transform_data_for_columns, columns_with_values,
    create_dataframe, separete_values,
    transform_values_for_nan, transform_values_str_with_replace, change_type_values)

# Extract Data
url, headers = load_json(json_path="request_data.json")
response = request_wanted_fbi(url=url, headers=headers)
data = extract_data_wanted(response=response)
extract_data = iteration_data_wanted(data=data)

# Transform Data
extract_data = transform_data_for_columns(extracted_data=extract_data)
data_dict = columns_with_values(extract_data)
df = create_dataframe(data_dict)
df = separete_values(df)
df = transform_values_for_nan(df)
df = transform_values_str_with_replace(df)
df = change_type_values(df)

df.to_csv('fbi_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
