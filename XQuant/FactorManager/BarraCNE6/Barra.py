from .Dividend import DividendYield
from .Liquidity import Liquidity
from .Size import Size
from .base_envion import *

class BARRA(Size, Liquidity, DividendYield):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)



