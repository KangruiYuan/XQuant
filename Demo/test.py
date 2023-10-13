from XQuant import EnhancingDividend
from XQuant import BackTestOptions, BackTestRunner, Strategy, Formatter
from XQuant import TradeDate
import pandas as pd
import numpy as np

begin = "20220101"
bench_code = "000300"
ed  = EnhancingDividend(begin=begin)
ed._bool_per_cash_div.describe()