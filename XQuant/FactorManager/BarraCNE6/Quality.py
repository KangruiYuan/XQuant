from .barra_envion import *


class Quality(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def MLEV(self):
        """
        - MLEV: market leverage. $MLEV = \frac{ME+PE+LD}{ME}=\frac{总市值+非流动负债}{总市值}$
        - ME: the market value of common equity on the last trading day
        - PE: PE and LD are the preferred equity and long-term debt, respectively, from the last fiscal year.
        :return:
        """
        market_value = self.market_value
        ttl_ncur_liab = self.ttl_ncur_liab
        market_value, ttl_ncur_liab = self.align_dataframe(
            [market_value, ttl_ncur_liab]
        )
        return ((market_value + ttl_ncur_liab) / market_value).ffill()

    @cached_property
    def BLEV(self):
        """
        BLEV: book leverage. $BLEV=\frac{BE+PE+LD}{BE}=\frac{账面价值+非流动负债}{账面价值}$
        - BE, PE, and LD are the book value of common equity, preferred equity, and long-term debt, respectively,
         from the last fiscal year.
        :return:
        """

        ttl_ncur_liab = self.ttl_ncur_liab
        ttl_eqy = self.ttl_eqy
        ttl_ncur_liab, ttl_eqy = self.align_dataframe([ttl_ncur_liab, ttl_eqy])
        return ((ttl_eqy + ttl_ncur_liab) / ttl_eqy).ffill()

    @cached_property
    def DTOA(self):
        """
        DTOA: debt-to-assets. $DTOA(资产负债比)=\frac{TL}{TA}$.
        -  TL and TA are the total liabilities and total assets, respectively from the last fiscal year.
        :return:
        """
        ttl_ast = self.ttl_ast
        ttl_liab = self.ttl_liab
        ttl_liab, ttl_ast = self.align_dataframe([ttl_liab, ttl_ast])
        return (ttl_liab/ttl_ast).ffill()

    @cached_property
    def Leverage(self):
        """
        Leverage = 0.38*MLEV + 0.35*DTOA + 0.27*BLEV
        :return:
        """
        MLEV, DTOA, BLEV = self.align_dataframe([self.MLEV, self.DTOA, self.BLEV])
        return (0.38 * MLEV + 0.35 * DTOA + 0.27 * BLEV).ffill()


