from src.extract_data import *
from src.transform_data import *

# Extract Data
url, headers = load_json("request_data.json")
response = request_wanted_fbi(url, headers)
data = extract_data_wanted(response)
info_data = ["title", "age_max", "age_min", "age_range", "location", "details", "subjects"]
extracted_data = iteration_data_wanted(data, info_data)

# Transform Data
columns_name = ["title", "age_max", "age_min", "age_range", "location", "details", "subjects"]
transformed_data = transform_data_for_columns(extracted_data, columns_name)
data_dict = columns_with_values(columns_name, transformed_data)
df = create_dataframe(data_dict)
df = transform_values_for_nan(df, "Null")
df = transform_values_str_with_replace(df, "details", ["<p>", "</p>"], "")
df = change_type_values(df, "age_max")
df = change_type_values(df, "age_min")

print(df.head())
