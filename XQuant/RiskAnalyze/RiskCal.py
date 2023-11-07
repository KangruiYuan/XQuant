from ..Utils import Config, format_dataframe
from ..Schema import TimeType, RiskMethod
from ..Collector import DataAPI
from typing import Sequence, Union, Optional
from datetime import datetime
from scipy.stats import norm


class Risk:
    def __init__(
        self,
        ticker: Union[str, Sequence[str]],
        begin: TimeType,
        end: Optional[TimeType] = None,
    ):
        self.cumsum_returns = None
        self.ticker = ticker if isinstance(ticker, Sequence) else [ticker]
        self.begin = begin
        self.end = end if end is not None else datetime.today()

    def get_returns(self, name: str = "MktEqud", **kwargs):
        if name in ["MktEqud", "uqer_MktEqud"]:
            return_value = "chgPct"
        else:
            raise ValueError(f"Unknown Tablename: %s" % name)
        ticker_column = Config.datatables[name]["ticker_column"]
        date_column = Config.datatables[name]["date_column"]
        df = DataAPI.get_data(
            name=name,
            ticker=self.ticker,
            begin=self.begin,
            end=self.end,
            fields=[ticker_column, date_column, return_value],
            **kwargs,
        )
        returns = df.pivot(
            columns=ticker_column, index=date_column, values=return_value
        )
        returns = format_dataframe(returns, columns=False)
        cumsum_returns = returns.cumsum() + 1
        self.returns = returns
        self.cumsum_returns = cumsum_returns

    def hist_risk(self, quantile: float = 0.05, **kwargs):
        hist_risk = self.returns.quantile(quantile)
        print("=" * 30)
        for ticker, var in hist_risk.items():
            print(f"HIST RISK - {ticker} (per day): {var: .3f}")

    def cov_risk(self, quantile: float = 0.05, **kwargs):
        cov_risk = norm.ppf(quantile, self.returns.mean(), self.returns.std())
        print("=" * 30)
        for ticker, var in zip(self.ticker, cov_risk):
            print(f"COV RISK - {ticker} (per day): {var: .3f}")

    def expected_risk(self, quantile: float = 0.05, **kwargs):
        VaR = self.returns.quantile(quantile)
        ES = self.returns[self.returns <= VaR].mean()
        print("=" * 30)
        for ticker, var in ES.items():
            print(f"EXPECTED RISK - {ticker} (per day): {var: .3f}")

    def maxdown_risk(self, **kwargs):
        MDD = (self.cumsum_returns.cummax() - self.cumsum_returns).max()
        print("=" * 30)
        for ticker, var in MDD.items():
            print(f"MAXDOWN RISK - {ticker}: {var: .3f}")

    def summary(self, method: Optional[RiskMethod] = None, **kwargs):
        if self.returns is None or self.cumsum_returns is None:
            self.get_returns(**kwargs)
        if method is None:
            self.hist_risk(**kwargs)
            self.cov_risk(**kwargs)
            self.expected_risk(**kwargs)
            self.maxdown_risk(**kwargs)
        elif method == RiskMethod.HIST:
            self.hist_risk(**kwargs)
        elif method == RiskMethod.COV:
            self.cov_risk(**kwargs)
        elif method == RiskMethod.EXPECTED:
            self.expected_risk(**kwargs)
        elif method == RiskMethod.MAXDOWN:
            self.maxdown_risk(**kwargs)
        else:
            raise NotImplementedError(method)


if __name__ == "__main__":
    r = Risk(
        ticker=["000001", "000063", "000413", "002007"],
        begin="20160101",
        end="20170101",
    )
    r.get_returns()
    # r.hist_risk()
    # r.cov_risk()
    # r.expected_risk()
    # r.maxdown_risk()
    r.summary()
