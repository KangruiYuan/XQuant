from .barra_envion import *


class Momentum(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)
        self.version = kwargs.get("version", 6)

    @cached_property
    def RSTR(self):
        """
        The non-lagged Relative Strength is first computed as the
        exponentially-weighted sum of the log excess returns of
        the stock relative to the market over a trailing 252-day window,
         with a 126-day half-life, The final RSTR descriptor is then
         computed as the equal-weighted average of the RS over an
         11-day window lagged by 11 days.

        $$
        RSTR = \sum^{T+L}_{t=L} w_t(ln(1+r_t) - ln(1+r_{ft})) \\
        w_t = (0.5^{1/126})^t,t \in [0,251] \\
        r_t = \frac{P_t}{P_{t-1}} -1 \\
        T=504,L=21(T=252,L=11)
        $$
        :return:
        """
        bench = self.bench
        returns = self.returns
        bench, returns = self.align_dataframe([bench, returns])
        excess_ret = np.log((1 + returns).divide((1 + bench.values), axis=0))
        if self.version == 6:
            rstr = self.rolling(
                excess_ret, window=252, half_life=126, func_name="nansum"
            )
            rstr = rstr.rolling(window=11, min_periods=1).mean()
        elif self.version == 5:
            exp_wt = self.get_exp_weight(504 + 21, 126)[:504]
            rstr = self.rolling(excess_ret.shift(21), window=504, weights=exp_wt,
                                func_name='nansum')
        else:
            raise NotImplementedError(f"Version: {self.version}")
        return rstr

    @cached_property
    def STREV(self):
        strev = self.rolling(self.returns, window=21,
                             half_life=5, func_name='nansum')
        return strev

    @cached_property
    def SEASON(self):
        years = 5
        pct_chg_m_d = self.returns
        pct_chgs_shift = [pct_chg_m_d.shift(i * 21 * 12 - 21) for i in range(1, years + 1)]
        seasonality = sum(pct_chgs_shift) / years
        return seasonality
