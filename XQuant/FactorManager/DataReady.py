from typing import Union, Optional

import numpy as np
import pandas as pd

from .Processer import Processer
from ..Utils import TimeType, Config, Formatter
from ..Collector import DataAPI
from datetime import date
from functools import cached_property


class DataReady(Processer, DataAPI):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        self.sql: bool = kwargs.get("sql", False)
        self.adj: bool = kwargs.get("adj", False)
        self.bench_code: str = kwargs.get("bench_code", '000300')
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
        df = Formatter.dataframe(df)
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
        return self.get_pivot_df(
            key_value="chgPct", name="MktEqud", begin=self.begin, end=self.end
        )

    @cached_property
    def turnover(self):
        """
        换手率
        :return:
        """
        return self.get_pivot_df(
            key_value="turnoverValue", name="MktEqud", begin=self.begin, end=self.end
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
        return self.get_pivot_df(
            key_value="negMarketValue", name="MktEqud", begin=self.begin, end=self.end
        )

    @cached_property
    def EPS(self):
        """
        每股盈余
        :return:
        """
        return self.get_pivot_df(
            key_value="EPS", name="FdmtIndiPSPit", begin=self.begin, end=self.end
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
    def ttl_inc_oper(self):
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
        return (
            self.get_pivot_df(
                key_value="sur_rsv",
                name="fundamentals_balance",
                begin=self.begin,
                end=self.end,
            ).ffill()
        )

    @cached_property
    def ret_prof(self):
        """
        未分配利润
        :return:
        """
        return (
            self.get_pivot_df(
                key_value="ret_prof",
                name="fundamentals_balance",
                begin=self.begin,
                end=self.end,
            ).ffill()
        )

    @cached_property
    def bench(self):
        assert self.bench_code is not None
        df = self.get_data(
            name="uqer_MktIdx",
            ticker=self.bench_code,
            begin=self.begin,
            end=self.end,
            fields=["tradedate", "chgpct"],
        )
        df = df.rename(columns={"chgpct": "returns", "tradedate": "date"})
        df = df.set_index("date")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df
