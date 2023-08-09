

from .Utils import *
from .Collector import *
from .SQLAgent import *

Config.stock_list = list(map(Formatter.stock, Config.stock_list))