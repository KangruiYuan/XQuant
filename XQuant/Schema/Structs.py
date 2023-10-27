from pathlib import Path
from typing import NamedTuple, Optional, Callable, Sequence
from numpy import ndarray
from pydantic import BaseModel, Field
from .Types import TimeType
from .Enums import Strategy


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

class BackTestOptions(ModifiedModel):
    # 基本属性
    begin: TimeType = None
    end: TimeType = None
    cache: Path = Path(__file__).parents[1] / "Temp" / "BackTestCache"
    surname: str = "Default"
    bench_code: str = "000300"
    clean_cache: bool = False

    # 因子处理
    standardize: bool = False
    demean: bool = False
    quantile: float = 0.1
    direction: int = 0

    # 回测属性
    group_nums: int = 5
    method: Strategy = Strategy.GROUP
    function: Optional[Callable] = None
    shift: int = 1

    # 其他属性
    verbose: bool = False

class RtnResult(NamedTuple):
    RtnTotal: float
    RtnAnnual: float
    StdTotal: float
    Vol: float
    Sharpe: float
    MaxDown: float