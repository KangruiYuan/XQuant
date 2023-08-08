

from .Utils import *
from .Collector import *

Config.stock_list = list(map(Formatter.stock, Config.stock_list))