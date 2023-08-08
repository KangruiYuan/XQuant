
from XQuant import DataAPI, Tools

print(Tools.search_keyword("PE", update=True, verbose=False, limit=5))

# print(get_data("Price_Volume_Data/main", begin='20220101').info())

# print(
#     get_data(
#         'ResConSecTarpriScore',
#         begin='20210501',
#         ticker='000400',
#         fields='secCode'
#     ).info())