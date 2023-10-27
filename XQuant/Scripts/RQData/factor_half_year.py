from XQuant import Formatter, categorize_signal_by_quantiles, signal_to_weight
from utils import *
import numpy as np
import pandas as pd

factor = pd.read_csv(data_dir / "EnhancingDividend.csv", index_col=0, parse_dates=True)
# 半年换仓
factor = factor.ffill().resample("6M").last()
Formatter.transform_index(factor)
# 去除无效行列
factor = factor.replace({0: np.nan}).dropna(axis=0, how="all").dropna(axis=1, how="all")

print(factor.tail())