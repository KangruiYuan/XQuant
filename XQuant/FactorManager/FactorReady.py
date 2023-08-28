from functools import cached_property
import numpy as np
import pandas as pd
from datetime import date
from .DataReady import DataReady
from ..Utils import TimeType


class IMPLEMENTED:
    raw: dict[str, str] = {
        "市值": "market_value",
        "行业分类": "industry",
        "涨跌幅": "returns",
        "换手率": "turnover",
        "收盘价": "close",
        "基准": "bench",
    }
    factor: dict[str, str] = {
        "非线性市值": "LNCAP",
        "中市值": "MIDCAP",
        "股息率": "DTOP",
        "股票月流动性": "STOM",
        "股票季流动性": "STOQ",
        "股票年流动性": "STOA",
        "流动性": "Liquidity"
    }


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

    @classmethod
    def _calc_MIDCAP(cls, x: np.ndarray) -> np.ndarray:
        y = x**3
        beta, alpha = cls.regress(y, x, verbose=False)
        y_hat = alpha + beta * x
        resid = y - y_hat
        resid = cls.winsorize(resid, scale=3)
        resid = cls.standardlize(resid)
        return resid

    @cached_property
    def MIDCAP(self):
        df = self.LNCAP
        df = df.apply(self._calc_MIDCAP, axis=1, raw=True)
        return df


class Liquidity(DataReady):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)
        self.parallel = kwargs.get('parallel', True)

    @staticmethod
    def _calc_Liquidity(series: np.ndarray, days: int):
        freq = len(series) // days
        res = np.log(np.nansum(series) / freq)
        return -1e10 if np.isfinite(res) else res

    @cached_property
    def STOM(self):
        """
        STOM: share turnover, one month, $STOM = ln(\sum_{t=1}^{21} \frac{V_t}{S_t})$
            - $V_t$: the trading volume on day t
            - $S_t$: the number of shares outstanding
            - 1）采用流通股本值，而非自由流通股本值；2）剔除未上市、停牌日期的数据。
        :return:
        """
        df = self.turnover
        if self.parallel:
            df = self.pandas_parallelcal(df, self._calc_Liquidity, args=(21,), window=21)
        else:
            df = df.rolling(axis=0, window=21).apply(func=self._calc_Liquidity, args=(21, ), raw=True)
        return df

    @cached_property
    def STOQ(self):
        """
        STOQ: average share turnover, trailing 3 months. Let $STOM_\tau$ be
         the share turnover for month $\tau$, with each month consisting of
          21 trading days. The quarterly share turnover is defined by,
          $STOQ=ln(\frac{1}{T}\sum^T_{\tau=1} exp(STOM_{\tau}))$, where T=3.
        :return:
        """
        df = self.turnover
        if self.parallel:
            df = self.pandas_parallelcal(df, self._calc_Liquidity, args=(21,), window=63)
        else:
            df = df.rolling(axis=0, window=63).apply(func=self._calc_Liquidity, args=(21, ), raw=True)
        return df

    @cached_property
    def STOA(self):
        """
        STOA: average share turnover, trailing 12 months. $STOA = ln(\frac{
        1}{T}\sum^T_{\tau=1} exp(STOM_{\tau}))$, where T = 12.
        :return:
        """
        df = self.turnover
        if self.parallel:
            df = self.pandas_parallelcal(df, self._calc_Liquidity, args=(21,), window=252)
        else:
            df = df.rolling(axis=0, window=21).apply(func=self._calc_Liquidity, args=(21, ), raw=True)
        return df

    @cached_property
    def Liquidity(self):
        df = 0.35 * self.STOM + 0.35 * self.STOQ + 0.3 * self.STOA
        df = df.ffill()
        return df


class DividendYield(DataReady):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def DTOP(self):
        """
        Dividend Yield = \frac{Annual Dividends Per Share}{Market Value Per Share}
        :return:
        """
        df = self.per_cash_div
        df = df.groupby(pd.Grouper(freq="Q")).sum()
        df = df.rolling(window=4).sum()
        annual_div_per_share = df.resample("D").asfreq().fillna(method="ffill")

        close_price = self.close

        annual_div_per_share, close_price = self.align_dataframe(
            [annual_div_per_share, close_price]
        )

        dtop = annual_div_per_share / close_price
        return dtop


class BARRA(Size, Liquidity, DividendYield):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)
