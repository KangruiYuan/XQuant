from .base_envion import *
from ...Utils import TradeDate

class Growth(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        begin = TradeDate.shift_trade_date(begin, -252)
        super().__init__(begin, end, **kwargs)
        self.parallel = kwargs.get("parallel", True)

