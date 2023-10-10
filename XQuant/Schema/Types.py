from datetime import datetime, date
from typing import Union, Sequence

import pandas as pd
from numpy import ndarray
from pandas import Series, Timestamp, DatetimeIndex

TimeType = Union[str, int, datetime, date, Timestamp, DatetimeIndex]
TimeArrays = Union[Series, Timestamp, DatetimeIndex, Sequence[TimeType]]
ArrayType = Union[Series, ndarray, list, pd.DataFrame]