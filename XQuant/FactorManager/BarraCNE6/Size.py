from .base_envion import *

class Size(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
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