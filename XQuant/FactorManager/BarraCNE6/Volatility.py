import numpy as np

from .base_envion import *


class Volatility(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def HBETA(self):
        if "HBETA" in self.__dict__:
            return self.__dict__["HBETA"]
        else:
            beta, alpha, hsigma = self.capm_regress(self.returns, self.bench)
            setattr(self, "HSIGMA", hsigma)
            setattr(self, "HALPHA", alpha)
            return beta

    @cached_property
    def HSIGMA(self):
        if "HSIGMA" in self.__dict__:
            return self.__dict__["HSIGMA"]
        else:
            beta, alpha, hsigma = self.capm_regress(self.returns, self.bench)
            setattr(self, "HBETA", beta)
            setattr(self, "HALPHA", alpha)
            return hsigma

    @cached_property
    def HALPHA(self):
        if "HALPHA" in self.__dict__:
            return self.__dict__["HALPHA"]
        else:
            beta, alpha, hsigma = self.capm_regress(self.returns, self.bench)
            setattr(self, "HBETA", beta)
            setattr(self, "HSIGMA", alpha)
            return alpha

    @cached_property
    def CMRA(self):
        version = getattr(self, "version", 6)
        log_rtn = np.log(1 + self.returns)
        cmra = self.rolling_apply(log_rtn, self._cal_cmra, args=(12, 21, version), window=252).T
        return cmra
    @staticmethod
    def _cal_cmra(
        series: np.ndarray, months: int = 12, days_per_month: int = 21, version: int = 6
    ):
        z = sorted(
            np.nansum(series[-i * days_per_month :]) for i in range(1, months + 1)
        )
        if version == 6:
            return z[-1] - z[0]
        elif version == 5:
            return np.log(1 + z[-1]) - np.log(1 + z[0])

    @cached_property
    def DASTD(self):
        dastd = self.rolling(self.returns, window=252, half_life=42, func_name="nanstd")
        return dastd


    @cached_property
    def ResidualVolatility(self):
        HSIGMA, CMRA, DASTD = self.align_dataframe([self.HSIGMA, self.CMRA, self.DASTD])
        return 0.1 * HSIGMA + 0.16 * CMRA + 0.74 * DASTD