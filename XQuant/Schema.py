from datetime import datetime, date
from enum import Enum
from pathlib import Path
from typing import NamedTuple, Union, Optional, Callable, Sequence

import pandas as pd
from numpy import ndarray
from pandas import Series, Timestamp, DatetimeIndex

from pydantic import BaseModel, Field

TimeType = Union[str, int, datetime, date, Timestamp, DatetimeIndex]
TimeArrays = Union[Series, Timestamp, DatetimeIndex, Sequence[TimeType]]
ArrayType = Union[Series, ndarray, list, pd.DataFrame]

class ModifiedModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class OptimizeResult(ModifiedModel):
    weight: ndarray = Field(alias='x')
    target: float = Field(alias='fun')
    message: str
    success: bool
    status: int
    njev: int
    nfev: int
    nit: int
    jac: ndarray
    name: Sequence

    @property
    def portfolio(self):
        return dict(zip(self.name, self.weight))


class Strategy(str, Enum):

    LONG_ONlY = 'long_only'
    GROUP = "group"
    TOP_BOTTOM = "top_bottom"
    WEIGHT = "weight"
    SELF_DEFINED = "self_defined"


class BackTestOptions(ModifiedModel):
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




class RtnResult(NamedTuple):
    RtnTotal: float
    RtnAnnual: float
    StdTotal: float
    Vol: float
    Sharpe: float
    MaxDown: float
