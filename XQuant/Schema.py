from typing import NamedTuple, Union, Literal
from datetime import datetime, date
from pandas import Timestamp
from pydantic import BaseModel
from pathlib import Path

TimeType = Union[str, int, datetime, date, Timestamp]


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
    method: Literal[
        "线性仓位", "多空对冲", "分组回测", "权重持仓", "自定义"
    ] = "分组回测"

    # 其他属性
    verbose: bool = False


class RtnResult(NamedTuple):
    RtnTotal: float
    RtnAnnual: float
    StdTotal: float
    Vol: float
    Sharpe: float
    MaxDown: float
