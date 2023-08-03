

from .Utils import *
from .Collector import get_data

Config.stock_list = list(map(Formatter.stock, Config.stock_list))