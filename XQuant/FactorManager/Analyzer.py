from pathlib import Path
from typing import Union, Sequence

import numpy as np
import pandas as pd
import scipy.stats as st
from bokeh.io import output_file
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show
from loguru import logger

from .DataReady import DataReady
from .Processer import Processer
from ..Schema import RtnResult


class Analyzer:
    @classmethod
    def cleanup(
        cls,
        arr: Union[list, np.ndarray],
        inplace: bool = False,
        fill_value: float = 0.0,
    ):
        if inplace:
            res = arr
        else:
            res = arr.copy()
        res[~np.isfinite(res)] = fill_value
        return res

    @classmethod
    def rtns_analysis(cls, rtn: Union[list, np.ndarray]) -> RtnResult:
        rtn = cls.cleanup(rtn)
        nav = np.cumprod(rtn + 1) - 1
        number_of_years = len(rtn) / 250
        RtnTotal = nav[-1] / nav[0]
        RtnAnnual = RtnTotal / number_of_years
        StdTotal = float(np.nanstd(rtn))
        Vol = StdTotal * np.sqrt(250)
        Sharpe = RtnAnnual / Vol
        MaxDown = cls.maximum_draw_down(rtn)
        return RtnResult(
            RtnTotal=RtnTotal,
            RtnAnnual=RtnAnnual,
            StdTotal=StdTotal,
            Vol=Vol,
            Sharpe=Sharpe,
            MaxDown=MaxDown,
        )

    @classmethod
    def maximum_draw_down(cls, rtn: np.ndarray):
        min_all = 0
        sum_here = 0
        for x in rtn:
            sum_here += x
            if sum_here < min_all:
                min_all = sum_here
            elif sum_here >= 0:
                sum_here = 0
        return -min_all

    @classmethod
    def ICIR(
        cls,
        score: pd.DataFrame,
        returns: pd.DataFrame = None,
    ):
        min_date = score.index.min()
        max_date = score.index.max()
        if returns is None:
            logger.info("自动获取回报率信息")
            dr = DataReady(begin=min_date, end=max_date)
            returns = dr.returns

        score, returns = Processer.align_dataframe(dfs=[score, returns], clean=True)

        IC = pd.DataFrame(data=0, index=score.index, columns=["IC"])
        for (idx_s, value_s), (idx_r, value_r) in zip(
            score.iterrows(), returns.iterrows()
        ):
            matrix = np.stack([value_s.values, value_r.values], axis=1)
            nan_indices = np.isnan(matrix).any(axis=1)
            filtered_matrix = matrix[~nan_indices]
            res = st.spearmanr(filtered_matrix)
            if res.pvalue <= 0.05:
                IC.loc[idx_s] = res.statistic
        IC = IC.dropna(axis=0)
        IR = (IC.mean()) / IC.std()
        return IC, IR

    @classmethod
    def plotter(
        cls,
        datas: pd.DataFrame | pd.Series,
        key: str = "IC",
        output: Union[str, Path, bool] = None,
        **kwargs
    ):
        if output is not None:
            # 设置输出文件
            if isinstance(output, (str, Path)):
                output_file(output)
            elif isinstance(output, bool):
                output = Path(__file__).parents[1] / "Temp/ICIR.html"
                output_file(output)
            logger.info("Output to file: %s" % Path(output))
        if isinstance(datas, (pd.DataFrame, pd.Series)):
            x = datas.index
            if isinstance(datas, pd.Series):
                y = datas.values
            else:
                y = datas[key].values

            p = figure(
                height=500,
                width=1000,
                title=kwargs.get("title", "IC"),
                x_axis_label=kwargs.get("xlabel", "Date"),
                y_axis_label=kwargs.get("ylabel", key),
            )

            # 创建柱状图
            p.vbar(
                x=x,
                top=y,
                width=1.5,
                bottom=0,
                color="red",
                alpha=0.6,
            )

            # 设置图表属性
            p.xgrid.grid_line_color = None
            p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
            # 展示图表
            if kwargs.get("verbose", True):
                show(p)
            else:
                return p

