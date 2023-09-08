from .barra_envion import *


class Value(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)
        self.parallel = kwargs.get("parallel", True)

    @cached_property
    def BTOP(self):
        """
        BTOP (Book-to-Price, 账面市值比)
        Computed by dividing the last reported book value of common equity by the current market capitalization.
         The inverse of the price-book ratio 1/PB.
        :return:
        """
        return 1 / self.PB

    @cached_property
    def ETOP(self):
        """
        ETOP (Earnings to Price)
        PE: 滚动市盈率，即市盈率TTM，总市值/归属于母公司所有者的净利润TTM
        Computed by dividing the trailing 12-month earnings by the current market capitailization.
        :return:
        """
        return 1 / self.PETTM

    @cached_property
    def ETOPF(self):
        """
        Analyst-Predicted Earnings-to-Price分析师预测EP比
        :return:
        """
        return 1 / self.PECON

    @cached_property
    def CETOP(self):
        '''
        CETOP
        - Cash earnings earnings to price现金盈利价格比
        - 过去12个月的现金盈利除以当前市值
        - 过去滚动12个月的经营现金流除以当前市值，实际计算中取市现率PCF（经营现金流）的倒数。
        PCF2	Double	市现率(经营TTM)=总市值/经营现金净额TTM
        :return:
        '''
        return 1 / self.PCF

    @cached_property
    def EarningYield(self):
        """
        盈利率（Earning Yield）
        :return:
        """
        ETOP, ETOPF, CETOP = self.align_dataframe([self.ETOP, self.ETOPF, self.CETOP])
        ETOP, ETOPF, CETOP = ETOP.ffill(), ETOPF.ffill(), CETOP.ffill()
        return 0.11 * ETOP + 0.68 * ETOPF + 0.21 * CETOP





