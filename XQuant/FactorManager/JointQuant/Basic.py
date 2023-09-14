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

    @cached_property
    def sale_expense_ttm(self):
        """
        销售费用TTM
        :return:
        """
        exp_sell = self.exp_sell.ffill()
        df = exp_sell.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def gross_profit_ttm(self):
        """
        毛利润=营业收入 inc_oper-营业成本 cost_oper
        毛利TTM
        :return:
        """
        inc_oper = self.inc_oper.ffill()
        cost_oper = self.cost_oper.ffill()
        inc_oper, cost_oper = self.align_dataframe([inc_oper, cost_oper], clean=False)
        gross = inc_oper - cost_oper
        df = gross.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def retained_earnings(self):
        """
        留存收益=盈余公积金(sur_rsv)+未分配利润(ret_prof)
        :return:
        """
        sur_rsv = self.sur_rsv
        ret_prof = self.ret_prof
        sur_rsv, ret_prof = self.align_dataframe([sur_rsv, ret_prof])
        df = sur_rsv.ffill() + ret_prof.ffill()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def total_operating_cost_ttm(self):
        """
        营业总成本TTM
        :return:
        """
        ttl_inc_oper = self.ttl_inc_oper.ffill()
        df = ttl_inc_oper.rolling(window=4, axis=0).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def non_operating_net_profit_ttm(self):
        """
        营业外收支净额TTM = 营业外收入（TTM） (inc_noper)- 营业外支出（TTM）(exp_noper)
        :return:
        """
        inc_noper = self.inc_noper.ffill()
        exp_noper = self.exp_noper.ffill()
        inc_noper, exp_noper = self.align_dataframe([inc_noper, exp_noper], clean=False)
        inc_noper_ttm = inc_noper.rolling(window=4).sum()
        exp_noper_ttm = exp_noper.rolling(window=4).sum()
        df = inc_noper_ttm - exp_noper_ttm
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df


    @cached_property
    def net_invest_cash_flow_ttm(self):
        """
        投资活动现金流量净额TTM
        :return:
        """
        net_cf_inv = self.net_cf_inv.ffill()
        df = net_cf_inv.rolling(window=4).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def financial_expense_ttm(self):
        """
        财务费用TTM
        :return:
        """
        fin_exp = self.fin_exp.ffill()
        df = fin_exp.rolling(window=4).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df


