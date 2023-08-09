
from XQuant import DataAPI, Tools
from XQuant import SQLAgent

print(len(DataAPI.get_data('gmData_history', begin='20230601')))

print(len(DataAPI.get_data('gmData_history_adj', begin='20230601')))

# postgres_connection()

# print(Tools.get_newest_file("Price_Volume_Data/main"))

# print(Tools.search_keyword("PE", update=True, verbose=False, limit=5))

# print(get_data("Price_Volume_Data/main", begin='20220101').info())

# print(
#     get_data(
#         'ResConSecTarpriScore',
#         begin='20210501',
#         ticker='000400',
#         fields='secCode'
#     ).info())