
from datetime import date
from functools import reduce
from itertools import chain

import pandas as pd
import numpy as np
import statsmodels.api as sm
from typing import Union, Callable, Any, Literal
from dask import dataframe as dd
from pyfinance.utils import rolling_windows
from statsmodels.regression.linear_model import WLS

from ..Utils import Formatter, Tools

ArrayType = Union[pd.Series, np.ndarray, list]


class Processer:
    def __init__(self, begin: str = None, end: str = None, **kwargs) -> None:
        self.begin = begin
        self.end = end if end else date.today().strftime("%Y%m%d")
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def regress(
        y: ArrayType,
        X: ArrayType,
        intercept: bool = True,
        weight: int = 1,
        verbose: bool = True,
    ):
        """
        :param y: 因变量
        :param X: 自变量
        :param intercept: 是否有截距
        :param weight: 权重
        :param verbose: 是否返回残差
        :return:
        """
        if isinstance(y, (pd.Series, list)):
            y = np.array(y)
        if isinstance(X, (pd.Series, list)):
            X = np.array(X)

        if X.ndim == 1:
            X = X.reshape((-1, 1))

        if intercept:
            const = np.ones(len(X))
            X = np.insert(X, 0, const, axis=1)

        model: WLS = sm.WLS(y, X, weights=weight, missing="drop")
        result = model.fit()
        params = result.params
        if verbose:
            resid = y - np.dot(X, params)
            if intercept:
                return params[1:], params[0], resid
            else:
                return params, None, resid
        else:
            if intercept:
                return params[1:], params[0]
            else:
                return params

    @staticmethod
    def align_dataframe(dfs: list[pd.DataFrame] = None, clean: bool = True, *args):
        """
        基于index和columns进行表格的对齐
        :param dfs:
        :param clean:
        :param args: 可以传入单个表格
        :return:
        """
        if dfs is None:
            dfs = []
        dfs = list(chain(dfs, args))

        if clean:
            dfs = [Formatter.dataframe(df) for df in dfs]

        dims = 1 if any(len(df.shape) == 1 or 1 in df.shape for df in dfs) else 2
        res = []
        if len(dfs) > 2:
            mut_date_range = sorted(
                reduce(lambda x, y: x.intersection(y), (df.index for df in dfs))
            )
            if dims == 2:
                mut_codes = sorted(
                    reduce(lambda x, y: x.intersection(y), (df.columns for df in dfs))
                )
                res = [df.loc[mut_date_range, mut_codes] for df in dfs]
            elif dims == 1:
                res = [df.loc[mut_date_range, :] for df in dfs]
        else:
            mut_date_range = sorted(dfs[0].index.intersection(dfs[1].index))
            if dims == 2:
                mut_codes = sorted(dfs[0].columns.intersection(dfs[1].columns))
                res = [df.loc[mut_date_range, mut_codes] for df in dfs]
            elif dims == 1:
                res = [df.loc[mut_date_range, :] for df in dfs]
        return res

    @classmethod
    def capm_regress(
        cls, X: pd.DataFrame, Y: pd.DataFrame, window: int = 504, half_life: int = 252
    ):
        X, Y = cls.align_dataframe([X, Y])
        beta, alpha, sigma = cls.rolling_regress(
            Y, X, window=window, half_life=half_life
        )
        return beta, alpha, sigma

    @classmethod
    def rolling(
        cls,
        df: pd.DataFrame,
        window: int,
        half_life: int = None,
        func_name: str = "nansum",
        weights: ArrayType = None,
    ):
        func = getattr(np, func_name)
        if func is None:
            msg = f"""Search func:{func_name} from numpy failed,
                   only numpy ufunc is supported currently, please retry."""
            raise AttributeError(msg)

        if half_life is not None or (weights is not None):
            exp_wt = cls.get_exp_weight(window, half_life) if half_life else weights
            args = func, exp_wt
        else:
            args = func
        res = cls.pandas_parallelcal(df, cls.nan_func, args=args, window=window)
        return res

    @staticmethod
    def rolling_apply(
        df: pd.DataFrame,
        func: Callable,
        args: Any = None,
        axis: Literal[0, 1] = 0,
        window: int = None,
    ):
        if window is not None:
            res = df.rolling(window=window).apply(func, args=args, raw=True)
        else:
            res = df.apply(func, args=args, axis=axis, raw=True)
        return res

    @staticmethod
    def round_up_to_hundred(num):
        return int(np.ceil(num / 100) * 100)

    @staticmethod
    @Tools.watcher
    def pandas_parallelcal(
        df: pd.DataFrame, func: Callable, args: Any = None, window: int = None, **kwargs
    ):
        """
        :param df:
        :param func:
        :param args:
        :param window:
        :param kwargs:
                scheduler:
                    distributed, multiprocessing, processes,
                    single-threaded, sync, synchronous,
                    threading, threads
        :return:
        """
        if window is not None:
            cores = len(df) // window
        else:
            cores = 6
        print(f"Try with npartitions={cores}")
        res = dd.from_pandas(df, npartitions=cores)
        if window:
            res = res.rolling(window=window, axis=0)
            if args is None:
                res = res.apply(func, raw=True)
            else:
                res = res.apply(func, args=args, raw=True)
        else:
            res = res.apply(func, args=args, axis=1)
        return res.compute(scheduler=kwargs.get("scheduler", "processes"))

    @classmethod
    def nan_func(cls, series: ArrayType, func: Callable, weights: ArrayType = None):
        if weights is not None:
            return cls.weighted_func(func, series, weights=weights)
        else:
            return func(series)

    @classmethod
    def weighted_func(cls, func: Callable, series: ArrayType, weights: ArrayType):
        weights /= np.nansum(weights)
        if "std" in func.__name__:
            return cls.weighted_std(series, weights)
        else:
            return func(series * weights)

    @staticmethod
    def weighted_std(series, weights):
        return np.sqrt(np.nansum((series - np.nanmean(series)) ** 2 * weights))

    @classmethod
    def rolling_regress(
        cls,
        y: ArrayType,
        x: ArrayType,
        window=5,
        half_life=None,
        fill_na: str or (int, float) = 0,
    ):
        fill_args = (
            {"method": fill_na} if isinstance(fill_na, str) else {"value": fill_na}
        )

        stocks = y.columns
        if half_life:
            weight = cls.get_exp_weight(window, half_life)
        else:
            weight = 1

        start_idx = x.index[0]
        x, y = x.loc[start_idx:], y.loc[start_idx:, :]
        rolling_ys = rolling_windows(y, window)
        rolling_xs = rolling_windows(x, window)

        beta = pd.DataFrame(columns=stocks)
        alpha = pd.DataFrame(columns=stocks)
        sigma = pd.DataFrame(columns=stocks)
        for i, (rolling_x, rolling_y) in enumerate(zip(rolling_xs, rolling_ys)):
            rolling_y = pd.DataFrame(
                rolling_y, columns=y.columns, index=y.index[i : i + window]
            )
            window_sdate, window_edate = rolling_y.index[0], rolling_y.index[-1]
            rolling_y = rolling_y.fillna(**fill_args)

            rolling_y_val = rolling_y.values
            b, a, resid = cls.regress(
                rolling_y_val, rolling_x, intercept=True, weight=weight, verbose=True
            )
            vol = np.std(resid, axis=0)

            vol = pd.DataFrame(
                vol.reshape((1, -1)), columns=stocks, index=[window_edate]
            )
            a = pd.DataFrame(a.reshape((1, -1)), columns=stocks, index=[window_edate])
            b = pd.DataFrame(b, columns=stocks, index=[window_edate])

            beta = pd.concat([beta, b], axis=0)
            alpha = pd.concat([alpha, a], axis=0)
            sigma = pd.concat([sigma, vol], axis=0)

        return beta, alpha, sigma

    @staticmethod
    def get_exp_weight(window: int, half_life: int):
        exp_wt = np.asarray([0.5 ** (1 / half_life)] * window) ** np.arange(window)
        return exp_wt[::-1] / np.sum(exp_wt)
