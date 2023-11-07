from datetime import datetime, date
from typing import Union, Sequence, List, Tuple

from numpy import ndarray
from pandas import Series, Timestamp, DatetimeIndex, Index

TimeRaw = Union[str, int]
TimeReady = Union[datetime, date, Timestamp]
TimeType = Union[TimeRaw, TimeReady]
TimeArrays = Union[Series, DatetimeIndex, List, Tuple, ndarray, Index]

NormalArrays = Union[Series, Sequence, ndarray]