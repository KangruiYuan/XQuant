from .barra_envion import *

class Liquidity(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
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
