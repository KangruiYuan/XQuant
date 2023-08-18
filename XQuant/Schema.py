from typing import NamedTuple, Union
from datetime import datetime, date
from pandas import Timestamp
from pydantic import BaseModel
from pathlib import Path

TimeType = Union[str, int, datetime, date, Timestamp]


class Options(BaseModel):
    begin: TimeType = None
    end: TimeType = None
    cache: Path = Path(__file__).parent / "Temp" / "BackTestCache"
    surname: str = "Default"
    bench_code: str = "000300"


class RtnResult(NamedTuple):
    RtnTotal: float
    RtnAnnual: float
    StdTotal: float
    Vol: float
    Sharpe: float
    MaxDown: float
