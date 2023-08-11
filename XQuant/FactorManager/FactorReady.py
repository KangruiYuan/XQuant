
from functools import cached_property
import numpy as np
import pandas as pd
from datetime import date
from .DataReady import DataReady
from ..Utils import TimeType

class Size(DataReady):

    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def LNCAP(self):
        """
        :return: 非线性市值因子
        """
        return np.log(self.market_value)