from .base_envion import *

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