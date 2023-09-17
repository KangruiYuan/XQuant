from typing import NamedTuple, Union, Literal, Optional, Callable
from datetime import datetime, date

import pandas as pd
from pandas import Timestamp, DatetimeIndex, Series
from pydantic import BaseModel
from pathlib import Path
from enum import Enum
from pandas import Series
from numpy import ndarray

TimeArrays = Union[Series, Timestamp, DatetimeIndex, list, tuple, ndarray]
TimeType = Union[str, int, datetime, date, Timestamp, DatetimeIndex]


ArrayType = Union[Series, ndarray, list, pd.DataFrame]

class Strategy(str, Enum):

    LONG_ONlY = 'long_only'
    GROUP = "group"
    TOP_BOTTOM = "top_bottom"
    WEIGHT = "weight"
    SELF_DEFINED = "self_defined"


class BackTestOptions(BaseModel):
    # 基本属性
    begin: TimeType = None
    end: TimeType = None
    cache: Path = Path(__file__).parent / "Temp" / "BackTestCache"
    surname: str = "Default"
    bench_code: str = "000300"
    clean_cache: bool = False

    # 因子处理
    standardize: bool = False
    demean: bool = False
    quantile: float = 0.1

    # 回测属性
    group_nums: int = 5
    method: Strategy = Strategy.GROUP
    function: Optional[Callable] = None

    # 其他属性
    verbose: bool = False

    class Config:
        arbitrary_types_allowed = True


class RtnResult(NamedTuple):
    RtnTotal: float
    RtnAnnual: float
    StdTotal: float
    Vol: float
    Sharpe: float
    MaxDown: float
