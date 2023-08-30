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
        self.bench_code: str = kwargs.get("bench_code", None)
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
            df = df.drop_duplicates(subset=[index, column], keep='last')
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
            key_value = 'perCashDiv'

        return self.get_pivot_df(
            key_value=key_value, name=name, begin=self.begin, end=self.end
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


