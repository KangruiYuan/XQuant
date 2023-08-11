from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import scipy.stats as st
from bokeh.io import output_file
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show
from loguru import logger

from .DataReady import DataReady
from .Processer import Processer
from ..Utils import Formatter


class Tester:
    @staticmethod
    def cure_data(df: pd.DataFrame | pd.Series, ticker: str = None):
        if len(df.shape) != 1:
            if ticker is not None:
                df = pd.DataFrame(df[Formatter.stock(ticker)])
                return df
            elif 1 in df.shape:
                df = df.T
                return df
            else:
                raise ValueError(
                    "Data should be one dimensional or you should specify a ticker"
                )

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
            if res.pvalue > 0.05:
                IC.loc[idx_s] = 0
            else:
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
                color='red',
                alpha=0.6,
            )

            # 设置图表属性
            p.xgrid.grid_line_color = None
            p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
            # 展示图表
            show(p)
