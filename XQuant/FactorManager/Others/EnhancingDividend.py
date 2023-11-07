from datetime import date

import numpy as np
import pandas as pd
from ...Utils import shift_trade_date, transform_index, expand_dataframe

from ..BarraCNE6 import BARRA
from functools import cached_property
from ...Schema import TimeType


class EnhancingDividend(BARRA):

    """
    增强红利因子的设计
    考虑到股息率与市值、盈利性指标的高相关性。我们认为股息率选股的成功之处在于选择大市值中盈利稳健、收入较高的公司，
    因此我们对股息率施以更加严格的市值、盈利能力和分红约束：1）市值和交易活跃度；2）盈利能力和盈利持续性；3）分红能力和持续性。
    为了进一步发挥红利策略的优势，个股权重按照个股分红占全部成份股股票总分红的比例设计（Smart beta的处理方式）。其次，为了
    避免权重向某一些股息率较高或流通市值较高的股票过度倾斜，我们认为还必须对个股和行业的权重进行限制，让组合尽量分散，已达到
    降低组合风险的目的。最后，由于红利策略是一个适合中长期的价值投资策略，我们将调仓期由月频修改至半年调仓，降低因子换手率，避免较高的交易成本。
    通过以上三步增强，我们完成了增强红利因子的构建。我们在股息率因子的基础上引入一个代表其他成份股筛选条件的哑变量D_t，在调仓期t（每半年），
    当股票i满足如下条件时，D_t=1：
    (1)流通市值大于10亿元； negMarketValue
    (2)最近6个月日均成交额大于1,000万元；turnoverValue
    (3)最近两个调整期内至少有一期近三年年均EPS增长率为正；EPS
    (4)最近三年股息年均增长率不低于5%。 perCashDiv
    不满足上述条件时，D_t=0。
    因此，增强红利因子的计算方法为：增强红利因子=D_t×股息率。
    """

    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        begin = shift_trade_date(begin, lag=-252*3)
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def _bool_neg_market_value(self):
        df = self.neg_market_value.ffill()
        df = df.apply(lambda x: x > 1e9)
        df = df.fillna(0)
        return df

    @cached_property
    def _bool_turnover(self):
        df = self.turnover.ffill()
        df = self.pandas_parallelcal(
            df, func=lambda x: np.nanmean(x) >= 1e7, window=6 * 21
        )
        df = df.fillna(0)
        return df

    @cached_property
    def _bool_per_cash_div(self):
        df = self.per_cash_div
        df = df.groupby(pd.Grouper(freq="Y")).mean().ffill()
        df = ((df - df.shift(1)) / df.shift(1)).ffill()
        df = df.rolling(window=3).apply(lambda x: np.nanmean(x) >= 0.05, raw=True).ffill()
        # df = df.rolling(window=3).apply(lambda x: np.nanmean(x) >= 0.05, raw=True).ffill()
        # df.index = list(map(lambda x: TradeDate.shift_trade_date(x, -1), df.index))
        transform_index(df)
        df = expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def _bool_EPS(self):
        df = self.EPS
        df = df.resample("Q").mean().ffill()
        # 计算最近一年的增长率
        df = (df - df.shift(4)) / df.shift(4)
        # 取三年增长率平均
        df = (
            df.rolling(window=9)
            .apply(lambda x: np.nanmean(x[[-1, -5, 0]]), raw=True).ffill()
        )
        df = df.rolling(window=2).apply(lambda x: any(x > 0)).ffill()
        # df.index = list(map(lambda x: TradeDate.shift_trade_date(x, -1), df.index))
        transform_index(df)
        df = expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def EnhancingDividend(self):
        (
            DTOP,
            _bool_neg_market_value,
            _bool_turnover,
            _bool_per_cash_div,
            _bool_EPS,
        ) = self.align_dataframe(
            [
                self.DTOP,
                self._bool_neg_market_value,
                self._bool_turnover,
                self._bool_per_cash_div,
                self._bool_EPS,
            ]
        )
        D_t = _bool_neg_market_value & _bool_turnover & _bool_per_cash_div & _bool_EPS
        DTOP = DTOP.ffill()
        res = (DTOP * D_t).ffill()
        half_year_res = res.resample("6M").last()
        half_year_res.index = list(map(lambda x: shift_trade_date(x, -1), half_year_res.index))
        expand_res = expand_dataframe(half_year_res, begin=self.begin, end=self.end)
        return expand_res
