from typing import Union, Optional

import numpy as np
import pandas as pd

from .Processer import Processer
from ..Utils import TimeType, Config, Formatter, TradeDate
from ..Collector import DataAPI
from datetime import date
from functools import cached_property


class DataReady(Processer, DataAPI):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        self.sql: bool = kwargs.get("sql", False)
        self.adj: bool = kwargs.get("adj", False)
        self.bench_code: str = kwargs.get("bench_code", "000300")
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @classmethod
    def get_pivot_df(
        cls,
        key_value: str,
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        ticker: Optional[Union[str, int, list]] = None,
        index: str = "",
        column: str = "",
        drop: bool = True,
        **kwargs,
    ):
        column = Config.datatables[name]["ticker_column"] or column
        index = Config.datatables[name]["date_column"] or index
        assert column and index
        df = cls.get_data(
            name=name,
            ticker=ticker,
            begin=begin,
            end=end,
            fields=[column, index, key_value],
        )
        if drop:
            df = df.drop_duplicates(subset=[index, column], keep="last")
        index_rename = kwargs.get("index_rename", "date")
        column_rename = kwargs.get("column_rename", "ticker")

        df = df.rename(columns={index: index_rename, column: column_rename})
        df = df.pivot(index=index_rename, values=key_value, columns=column_rename)

        df = Formatter.dataframe(df, **kwargs)
        df = df.sort_index()
        return df

    @cached_property
    def market_value(self):
        """
        市值
        :return:
        """
        return self.get_pivot_df(
            key_value="marketValue", name="MktEqud", begin=self.begin, end=self.end
        )

    @cached_property
    def industry(self):
        """
        申万行业分类
        :return:
        """
        return self.get_pivot_df(
            key_value="industryName1",
            name="IndustryID_Sw21",
            begin=self.begin,
            end=self.end,
        )

    @cached_property
    def returns(self):
        """
        回报率
        :return:
        """
        if self.sql:
            name = "uqer_MktEqud"
            # name = "uqer_mkt_equd_adj"
        else:
            name = "MktEqud"
        value = "chgPct"
        return self.get_pivot_df(
            key_value=value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def turnover(self):
        """
        换手率
        :return:
        """
        if self.sql:
            # name = "uqer_MktEqud"
            name = "uqer_mkt_equd_adj"
            value = "turnovervalue"
        else:
            name = "MktEqud"
            value ="turnoverValue"

        return self.get_pivot_df(
            key_value=value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def close(self):
        """
        收盘价
        :return:
        """
        if self.sql:
            key_value = "close"
            if self.adj:
                name = "gmData_history_adj"
            else:
                name = "gmData_history"
        else:
            key_value = "closePrice"
            name = "MktEqud"

        return self.get_pivot_df(
            key_value=key_value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def preclose(self):
        """
        收盘价
        :return:
        """
        if self.sql:
            key_value = "pre_close"
            if self.adj:
                name = "gmData_history_adj"
            else:
                name = "gmData_history"
        else:
            key_value = "preClosePrice"
            name = "MktEqud"

        return self.get_pivot_df(
            key_value=key_value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def PB(self):
        """
        市净率=总市值/归属于母公司所有者权益合计
        :return:
        """
        if self.sql:
            name = "uqer_MktEqud"
        else:
            name = "MktEqud"

        return self.get_pivot_df(
            key_value="PB", name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def PETTM(self):
        """
        滚动市盈率，即市盈率TTM
        :return:
        """
        if self.sql:
            name = "uqer_MktEqud"
        else:
            name = "MktEqud"

        return self.get_pivot_df(
            key_value="PE", name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def PECON(self):
        """
        一致预期PE: 当前预测日期总市值 / 当前预测日期一致预期归母净利润。
        :return:
        """
        if self.sql:
            name = "uqer_ResConSecCorederi"
        else:
            name = "ResConSecCorederi"

        return self.get_pivot_df(
            key_value="conPe", name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def per_cash_div(self):
        """
        每股派现(税前)
        :return:
        """
        if self.sql:
            name = "uqer_EquDiv"
            key_value = "percashdiv"
        else:
            name = "EquDiv"
            key_value = "perCashDiv"

        return self.get_pivot_df(
            key_value=key_value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def neg_market_value(self):
        """
        流通市值
        :return:
        """
        if self.sql:
            # name = "uqer_MktEqud"
            name = "uqer_mkt_equd_adj"
            value = "negmarketvalue"
        else:
            name = "MktEqud"
            value = "negMarketValue"

        return self.get_pivot_df(
            key_value=value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def EPS(self):
        """
        每股盈余
        :return:
        """
        if self.sql:
            name = "uqer_FdmtIndiPSPit"
            value = "eps"
        else:
            name = "FdmtIndiPSPit"
            value = "EPS"
        return self.get_pivot_df(
            key_value=value, name=name, begin=self.begin, end=self.end
        )

    @cached_property
    def EPSCON(self):
        """
        一致预期EPS
        :return:
        """
        return self.get_pivot_df(
            key_value="conEps", name="ResConSecCoredata", begin=self.begin, end=self.end
        )

    @cached_property
    def PCF(self):
        """
        市现率(经营TTM)=总市值/经营现金净额TTM
        :return:
        """
        return self.get_pivot_df(
            key_value="PCF2", name="MktEqudEval", begin=self.begin, end=self.end
        )

    @cached_property
    def current_asset(self):
        """
        流动资产
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_cur_ast",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def current_liability(self):
        """
        流动负债
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_cur_liab",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()


    @cached_property
    def ttl_ncur_liab(self):
        """
        非流动负债(day)
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_ncur_liab",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def ttl_eqy(self):
        """
        账面价值(day)
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_eqy",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()


    @cached_property
    def ttl_liab(self):
        """
        总负债
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_liab",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def ttl_ast(self):
        """
        总资产
        :return:
        """
        return self.get_pivot_df(
            key_value="ttl_ast",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()



    @cached_property
    def mny_cptl(self):
        """
        货币资金
        :return:
        """
        return self.get_pivot_df(
            key_value="mny_cptl",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def trd_fin_ast(self):
        """
        交易性金融资产
        :return:
        """
        return self.get_pivot_df(
            key_value="trd_fin_ast",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def note_rcv(self):
        """
        应收票据
        :return:
        """
        return self.get_pivot_df(
            key_value="note_rcv",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def int_rcv(self):
        """
        应收利息
        :return:
        """
        return self.get_pivot_df(
            key_value="int_rcv",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def dvd_rcv(self):
        """
        应收股利
        :return:
        """
        return self.get_pivot_df(
            key_value="dvd_rcv",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def aval_sale_fin(self):
        """
        可供出售金融资产
        :return:
        """
        return self.get_pivot_df(
            key_value="aval_sale_fin",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def htm_inv(self):
        """
        持有至到期投资
        :return:
        """
        return self.get_pivot_df(
            key_value="htm_inv",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def ttl_inc_oper(self):
        """
        营业总收入
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="ttl_inc_oper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def ttl_cost_oper(self):
        """
        营业总收入
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="ttl_cost_oper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_fee_comm(self):
        """
        手续费及佣金支出
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_fee_comm",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_rd(self):
        """
        研发费用
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_rd",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def ast_impr_loss(self):
        """
        资产减值损失
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="ast_impr_loss",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def net_prof_pcom(self):
        """
        归属于母公司股东的净利润
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="net_prof_pcom",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def depr_oga_cba(self):
        """
        资产减值损失
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="depr_oga_cba",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def amort_intg_ast(self):
        """
        无形资产摊销
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="amort_intg_ast",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def amort_lt_exp_ppay(self):
        """
        长期待摊费用摊销
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="amort_lt_exp_ppay",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def biz_tax_sur(self):
        """
        营业税金及附加
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="biz_tax_sur",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def net_cf_inv(self):
        """
        投资活动现金流量净额
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="net_cf_inv",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def fin_exp(self):
        """
        财务费用
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="fin_exp",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def net_prof(self):
        """
        净利润
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="net_prof",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def inc_noper(self):
        """
        营业外收入
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="inc_noper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def inc_tax(self):
        """
        所得税
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="inc_tax",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_noper(self):
        """
        营业外支出
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_noper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_adm(self):
        """
        管理费用
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_adm",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_int(self):
        """
        利息支出
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_int",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def inc_int(self):
        """
        利息收入
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="inc_int",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def ttl_prof(self):
        """
        利润总额
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="ttl_prof",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def net_cf_fin(self):
        """
        筹资活动现金流量净额
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="net_cf_fin",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def cash_cash_eq_end(self):
        """
        期末现金及现金等价物余额
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="cash_cash_eq_end",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def cash_rcv_sale(self):
        """
        销售商品提供劳务收到的现金
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="cash_rcv_sale",
                name="fundamentals_cashflow",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def NVALCHGIT(self):
        """
        价值变动净收益(NVALCHGIT)
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="NVALCHGIT",
                name="deriv_finance_indicator",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def PCTTM(self):
        """
        pcf_ratio (ttm)=PCTTM
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="PCTTM",
                name="deriv_finance_indicator",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def PSTTM(self):
        """
        ps_ratio (ttm)=PSTTM
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="PSTTM",
                name="deriv_finance_indicator",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def NPCUT(self):
        """
        扣除非经常损益后的净利润
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="NPCUT",
                name="deriv_finance_indicator",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def oper_prof(self):
        """
        营业利润
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="oper_prof",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def inc_oper(self):
        """
        营业收入
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="inc_oper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def cost_oper(self):
        """
        营业成本
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="cost_oper",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def TDEBT(self):
        """
        总债务
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="TDEBT",
                name="deriv_finance_indicator",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def exp_sell(self):
        """
        销售费用
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="exp_sell",
                name="fundamentals_income",
                begin=self.begin,
                end=self.end,
            )
            .groupby(pd.Grouper(freq="Q"))
            .mean()
        )

    @cached_property
    def sur_rsv(self):
        """
        盈余公积金
        :return:
        """
        return self.get_pivot_df(
            key_value="sur_rsv",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def ret_prof(self):
        """
        未分配利润
        :return:
        """
        return self.get_pivot_df(
            key_value="ret_prof",
            name="fundamentals_balance",
            begin=self.begin,
            end=self.end,
        ).ffill()

    @cached_property
    def bench(self):
        assert self.bench_code is not None
        # df = self.get_data(
        #     name="uqer_MktIdx",
        #     ticker=self.bench_code,
        #     begin=self.begin,
        #     end=self.end,
        #     fields=["tradedate", "chgpct"],
        # )
        # df = df.rename(columns={"chgpct": "returns", "tradedate": "date"})
        # df = df.set_index("date")
        # df.index = pd.to_datetime(df.index)
        # df = df.sort_index()
        # return df
        df = self.get_data(
            name="gmData_bench_price",
            ticker=self.bench_code,
            begin=TradeDate.shift_trade_date(self.begin, -1),
            end=TradeDate.shift_trade_date(self.end, 1),
            fields=["trade_date", "pre_close"],
        )
        df = df.rename(columns={"trade_date": "date"})
        df = df.set_index("date")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = Formatter.expand_dataframe(df, self.begin, self.end)
        pre_close = df['pre_close']
        df["returns"] = (pre_close.shift(-1) - pre_close) / pre_close
        df = df.drop("pre_close", axis=1)
        df = df.ffill()
        return df
