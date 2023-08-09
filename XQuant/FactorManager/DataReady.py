from .Processer import Processer
from ..Utils import TimeType, Config, Formatter
from ..Collector import DataAPI
from datetime import date
from functools import cached_property


class DataReady(Processer, DataAPI):
    def __init__(self, begin: TimeType = None, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def returns(self):
        df = self.get_data(
            name="MktEqud",
            ticker=Config.stock_list,
            begin=self.begin,
            end=self.end,
            fields=["ticker", "tradeDate", "chgPct"],
        )
        df = df.rename(columns={'chgPct':'returns', 'tradeDate':'date'})
        df = df.pivot(index='date', values='returns', columns='ticker')
        df = Formatter.dataframe(df)
        return df

