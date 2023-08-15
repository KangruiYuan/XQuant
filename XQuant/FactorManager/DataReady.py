import pandas as pd

from .Processer import Processer
from ..Utils import TimeType, Config, Formatter
from ..Collector import DataAPI
from datetime import date
from functools import cached_property


class DataReady(Processer, DataAPI):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        self.sql: bool = kwargs.get('sql', False)
        self.adj: bool = kwargs.get('adj', False)
        self.bench_code: str = kwargs.get('bench_code', None)
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def market_value(self):
        """
        市值
        :return:
        """
        df = self.get_data(
            name="MktEqud",
            ticker=Config.stock_list,
            begin=self.begin,
            end=self.end,
            fields=["ticker", "tradeDate", "marketValue"],
        )
        df = df.rename(columns={"marketValue": "market_value", "tradeDate": "date"})
        df = df.pivot(index="date", values="market_value", columns="ticker")
        df = Formatter.dataframe(df)
        return df

    @cached_property
    def industry(self):
        """
        申万行业分类
        :return:
        """
        df = self.get_data(
            "IndustryID_Sw21",
            begin=self.begin,
            end=self.end,
            fields=["date", "winCode", "industryName1"],
        )
        df = df.rename(columns={"industryName1": "industry_name", "winCode": "ticker"})
        df = df.pivot(index="date", values="industry_name", columns="ticker")
        df = Formatter.dataframe(df)
        return df

    @cached_property
    def returns(self):
        """
        回报率
        :return:
        """
        df = self.get_data(
            name="MktEqud",
            ticker=Config.stock_list,
            begin=self.begin,
            end=self.end,
            fields=["ticker", "tradeDate", "chgPct"],
        )
        df = df.rename(columns={"chgPct": "returns", "tradeDate": "date"})
        df = df.pivot(index="date", values="returns", columns="ticker")
        df = Formatter.dataframe(df)
        return df

    @cached_property
    def turnover(self):
        """
        换手率
        :return:
        """
        df = self.get_data(
            name="MktEqud",
            ticker=Config.stock_list,
            begin=self.begin,
            end=self.end,
            fields=["ticker", "tradeDate", "turnoverValue"],
        )
        df = df.rename(columns={"turnoverValue": "turnover", "tradeDate": "date"})
        df = df.pivot(index="date", values="turnover", columns="ticker")
        df = Formatter.dataframe(df)
        return df

    @cached_property
    def close(self):
        """
        收盘价
        :return:
        """
        if self.sql:
            if self.adj:
                name = "gmData_history_adj"
            else:
                name = "gmData_history"
            df = self.get_data(
                name=name,
                begin=self.begin,
                end=self.end,
                fields=["bob", "symbol", "close"],
            )
            df = df.rename(columns={"bob": "date", "symbol": "ticker"})
        else:
            df = self.get_data(
                name="MktEqud",
                ticker=Config.stock_list,
                begin=self.begin,
                end=self.end,
                fields=["ticker", "tradeDate", "closePrice"],
            )
            df = df.rename(columns={"closePrice": "close", "tradeDate": "date"})
        df = df.pivot(index="date", columns="ticker", values="close")
        df = Formatter.dataframe(df)
        return df

    @cached_property
    def bench(self):
        assert self.bench_code is not None
        df = self.get_data(
            name="uqer_MktIdx",
            ticker=self.bench_code,
            begin=self.begin,
            end=self.end,
            fields=['tradedate', 'chgpct']
        )
        df = df.rename(columns={"chgpct": "returns", "tradedate": "date"})
        df = df.set_index("date")
        df.index = pd.to_datetime(df.index)
        return df


