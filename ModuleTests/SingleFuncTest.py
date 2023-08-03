
from XQuant import get_data


print(
    get_data(
        'ResConSecTarpriScore',
        begin='20210501',
        ticker='000400',
        fields='secCode'
    ).info())