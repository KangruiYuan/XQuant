from datetime import datetime
from typing import Sequence, Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sco

from ..Collector import DataAPI
from ..Consts import datatables
from ..Utils import Formatter
from ..Schema import TimeType, OptimizeResult


class Portfolio:
    def __init__(
        self, ticker: Sequence[str], begin: TimeType, end: Optional[TimeType] = None
    ):
        self.ticker = ticker
        self.begin = begin
        self.end = end if end is not None else datetime.today()
        self.closes = None
        self.returns = None

    def get_close_and_returns(
        self, name: str = "MktEqud", value: str = "closePrice", **kwargs
    ):
        df = DataAPI.get_data(
            name=name, ticker=self.ticker, begin=self.begin, end=self.end, **kwargs
        )
        ticker_column = datatables[name]["ticker_column"]
        date_column = datatables[name]["date_column"]
        df = df.pivot(columns=ticker_column, index=date_column, values=value)
        closes = Formatter.dataframe(df, columns=False)
        returns = np.log(closes / closes.shift(1))
        self.closes = closes
        self.returns = returns
        return closes, returns

    def optimize_weights(
        self,
        montecarlo_trys: int = 4000,
        risk_free: float = 0.04,
        method: str = "SLSQP",
        **kwargs,
    ):
        if self.closes is None or self.returns is None:
            self.get_close_and_returns(**kwargs)

        returns = self.returns
        returns_mean = returns.mean().values * 252
        returns_cov = returns.cov().values * 252
        noa = len(self.ticker)
        weights_random = np.random.random(size=(montecarlo_trys, noa))
        weights_random = np.divide(
            weights_random, np.sum(weights_random, axis=1)[:, np.newaxis]
        )
        port_variance = np.sqrt(
            np.diagonal(np.dot(weights_random, (np.dot(returns_cov, weights_random.T))))
        )
        port_returns = np.sum(returns_mean * weights_random, axis=1)

        target_returns = np.linspace(0, max(0.3, max(port_returns) + 0.05), 50)
        target_variance = []
        bounds = tuple((0, 1) for _ in range(noa))
        x0 = np.ones(noa) / noa
        for tar in target_returns:
            cons = (
                {"type": "eq", "fun": lambda x: self.statistics(x)[0] - tar},
                {"type": "eq", "fun": lambda x: np.sum(x) - 1},
            )
            res = sco.minimize(
                self._min_variance,
                x0=x0,
                method=method,
                bounds=bounds,
                constraints=cons,
            )
            target_variance.append(res["fun"])
        target_variance = np.array(target_variance)

        cons = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        opts = sco.minimize(
            self._max_sharpe, x0=x0, method=method, bounds=bounds, constraints=cons
        )
        optv = sco.minimize(
            self._min_variance, x0=x0, method=method, bounds=bounds, constraints=cons
        )

        plt.figure(figsize=kwargs.get("figsize", (8, 6)))

        plt.scatter(
            port_variance,
            port_returns,
            c=(port_returns - risk_free) / port_variance,
            marker="o",
        )
        plt.scatter(
            target_variance,
            target_returns,
            c=target_returns / target_variance,
            marker="x",
            label="Efficient Frontier",
        )

        max_sharpe_stats = self.statistics(opts["x"])
        # 红星：标记最高sharpe组合
        plt.plot(
            max_sharpe_stats[1],
            max_sharpe_stats[0],
            "*",
            color="r",
            markersize=15.0,
            # markeredgecolor="white",
            label=f"Max Sharpe({max_sharpe_stats[1]:.3f}, {max_sharpe_stats[0]:.3f})",
        )

        min_var_stats = self.statistics(optv["x"])
        # 黄星：标记最小方差组合
        plt.plot(
            min_var_stats[1],
            min_var_stats[0],
            "X",
            color="deeppink",
            markersize=13.0,
            # markeredgecolor="white",
            label=f"Min Variance({min_var_stats[1]:.3f}, {min_var_stats[0]:.3f})",
        )

        plt.grid(True)
        plt.legend()
        plt.xlabel("excepted volatility")
        plt.ylabel("expected return")
        plt.colorbar(label="Sharpe ratio")
        plt.show()

        return {
            "optv": OptimizeResult(name=self.ticker, **optv),
            "opts": OptimizeResult(name=self.ticker, **opts),
        }

    def statistics(self, weights: Sequence[float]):
        weights = np.array(weights)
        port_returns = np.sum(self.returns.mean() * weights) * 252
        port_variance = np.sqrt(
            np.dot(weights.T, np.dot(self.returns.cov() * 252, weights))
        )
        return np.array([port_returns, port_variance, port_returns / port_variance])

    def _max_sharpe(self, weights: Sequence[float]):
        """
        最小化夏普指数的负值
        :param weights:
        :return:
        """
        return -self.statistics(weights)[2]

    def _min_variance(self, weights: Sequence[float]):
        return self.statistics(weights)[1]


if __name__ == "__main__":
    p = Portfolio(
        ticker=["000001", "000063", "000413", "002007"],
        begin="20160101",
        end="20170101",
    )
    p.optimize_weights()
