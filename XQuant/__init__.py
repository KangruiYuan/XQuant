

from .Utils import *
from .Collector import *
from .SQLAgent import *
from .FactorManager import *
from .FileManager import *
from .Schema import *

Config.stock_list = list(map(Formatter.stock, Config.stock_list))