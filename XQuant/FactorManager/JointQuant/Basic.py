from ...Collector import DataAPI

from .joint_quant_envion import *


class Basic(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def net_working_capital(self):
        """
        净运营资本
        :return:
        """
        ast, lia = self.align_dataframe([self.current_asset, self.current_liability])
        return ast - lia

    @cached_property
    def total_operating_revenue_ttm(self):
        """
        营业总收入TTM
        :return:
        """
        ttl_inc_oper = self.ttl_inc_oper.ffill()
        df = ttl_inc_oper.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def operating_profit_ttm(self):
        """
        营业利润TTM
        :return:
        """
        oper_prof = self.oper_prof.ffill()
        df = oper_prof.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def operating_revenue_ttm(self):
        """
        营业收入TTM
        :return:
        """
        inc_oper = self.inc_oper.ffill()
        df = inc_oper.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def interest_free_current_liability(self):
        """
        无息流动负债
        :return:
        """
        feas = [
            "note_pay",
            "acct_pay",
            "adv_acct",
            "tax_pay",
            "int_pay",
            "oth_pay",
            "oth_cur_liab",
        ]
        df = DataAPI.get_data("fundamentals_balance", begin=self.begin, end=self.end)
        df["interest_free_current_liability"] = df[feas].sum(axis=1)
        df = df.pivot(index='pub_date', columns='symbol', values='interest_free_current_liability')
        return Formatter.dataframe(df).ffill()

    @cached_property
    def interest_carry_current_liability(self):
        """
        带息流动负债
        :return:
        """
        interest_free_current_liability = self.interest_free_current_liability
        current_liability = self.current_liability
        interest_free_current_liability, current_liability = self.align_dataframe([
            interest_free_current_liability, current_liability
        ])
        return current_liability - interest_free_current_liability

