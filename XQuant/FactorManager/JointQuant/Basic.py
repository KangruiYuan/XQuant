from typing import Optional

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
        df = df.pivot(
            index="pub_date", columns="symbol", values="interest_free_current_liability"
        )
        return Formatter.dataframe(df).ffill()

    @cached_property
    def interest_carry_current_liability(self):
        """
        带息流动负债
        :return:
        """
        interest_free_current_liability = self.interest_free_current_liability
        current_liability = self.current_liability
        interest_free_current_liability, current_liability = self.align_dataframe(
            [interest_free_current_liability, current_liability]
        )
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
        return self.roll_and_expand_dataframe("ttl_cost_oper")

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

    @cached_property
    def administration_expense_ttm(self):
        """
        管理费用TTM
        :return:
        """
        exp_adm = self.exp_adm.ffill()
        df = exp_adm.rolling(window=4).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def net_interest_expense(self):
        """
        净利息费用=利息支出(exp_int)-利息收入(inc_int)
        :return:
        """
        exp_int, inc_int = self.exp_int, self.inc_int
        exp_int, inc_int = self.align_dataframe([exp_int, inc_int], clean=False)
        df = exp_int - inc_int
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def value_change_profit_ttm(self):
        """
        价值变动净收益TTM
        :return:
        """
        NVALCHGIT = self.NVALCHGIT.ffill()
        df = NVALCHGIT.rolling(window=4).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    def roll_and_expand_dataframe(
        self,
        name: Optional[str] = None,
        df: Optional[pd.DataFrame] = None,
        window: int = 4,
    ):
        if df is None:
            assert name is not None
            df = getattr(self, name)
        df = df.ffill()
        df = df.rolling(window=4).sum()
        df = Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
        return df

    @cached_property
    def total_profit_ttm(self):
        """
        利润总额TTM
        :return:
        """
        return self.roll_and_expand_dataframe(name="ttl_prof")

    @cached_property
    def net_finance_cash_flow_ttm(self):
        """
        筹资活动现金流量净额TTM
        :return:
        """
        return self.roll_and_expand_dataframe(name="net_cf_fin")

    @cached_property
    def EBIT(self):
        """
        息税前利润=净利润(net_prof)+所得税(inc_tax)+财务费用(fin_exp)
        :return:
        """
        fin_exp, net_prof, inc_tax = self.align_dataframe(
            [self.fin_exp, self.net_prof, self.inc_tax]
        )
        df = sum([fin_exp.ffill(), net_prof.ffill(), inc_tax.ffill()])
        return Formatter.expand_dataframe(df, begin=self.begin, end=self.end)

    @cached_property
    def net_profit_ttm(self):
        """
        净利润TTM
        :return:
        """
        return self.roll_and_expand_dataframe("net_prof")

    @cached_property
    def OperateNetIncome(self):
        """
        经营活动净收益=ttl_inc_oper营业总收入-ttl_cost_oper营业总成本
        :return:
        """
        ttl_cost_oper, ttl_inc_oper = (
            self.ttl_cost_oper.ffill(),
            self.ttl_inc_oper.ffill(),
        )
        ttl_cost_oper, ttl_inc_oper = self.align_dataframe(
            [ttl_cost_oper, ttl_inc_oper], clean=False
        )
        return Formatter.expand_dataframe(
            ttl_inc_oper - ttl_cost_oper, begin=self.begin, end=self.end
        )

    @cached_property
    def EBITDA(self):
        """
        息税折旧摊销前利润 = （营业总收入ttl_inc_oper-营业税金及附加biz_tax_sur）
            -（营业成本cost_oper+利息支出exp_int+手续费及佣金支出exp_fee_comm+销售费用exp_sell+管理费用exp_adm+研发费用exp_rd+资产减值损失ast_impr_loss）
            +（固定资产折旧、油气资产折耗、生产性生物资产折旧depr_oga_cba）+无形资产摊销amort_intg_ast+长期待摊费用摊销amort_lt_exp_ppay
        :return:
        """
        ttl_inc_oper = self.ttl_inc_oper.ffill()
        biz_tax_sur = self.biz_tax_sur.ffill()
        cost_oper = self.cost_oper.ffill()
        exp_int = self.exp_int.ffill()
        exp_fee_comm = self.exp_fee_comm.ffill()
        exp_sell = self.exp_sell.ffill()
        exp_adm = self.exp_adm.ffill()
        exp_rd = self.exp_rd.ffill()
        ast_impr_loss = self.ast_impr_loss.ffill()
        depr_oga_cba = self.depr_oga_cba.ffill()
        amort_intg_ast = self.amort_intg_ast.ffill()
        amort_lt_exp_ppay = self.amort_lt_exp_ppay.ffill()

        (
            ttl_inc_oper,
            biz_tax_sur,
            cost_oper,
            exp_int,
            exp_fee_comm,
            exp_sell,
            exp_adm,
            exp_rd,
            ast_impr_loss,
            depr_oga_cba,
            amort_intg_ast,
            amort_lt_exp_ppay,
        ) = self.align_dataframe(
            [
                ttl_inc_oper,
                biz_tax_sur,
                cost_oper,
                exp_int,
                exp_fee_comm,
                exp_sell,
                exp_adm,
                exp_rd,
                ast_impr_loss,
                depr_oga_cba,
                amort_intg_ast,
                amort_lt_exp_ppay,
            ],
            clean=False,
        )
        df = (
            ttl_inc_oper
            - biz_tax_sur
            - cost_oper
            - exp_int
            - exp_fee_comm
            - exp_sell
            - exp_adm
            - exp_rd
            - ast_impr_loss
            + depr_oga_cba
            + amort_intg_ast
            + amort_lt_exp_ppay
        )

        return Formatter.expand_dataframe(df, begin=self.begin, end=self.end)
