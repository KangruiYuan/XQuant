from .Dividend import DividendYield
from .Liquidity import Liquidity
from .Size import Size
from .Volatility import Volatility
from .barra_envion import *
from .Value import Value
from .Momentum import Momentum

class BARRA(Size, Liquidity, DividendYield, Volatility, Value, Momentum):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)



