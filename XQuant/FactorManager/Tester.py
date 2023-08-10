from typing import Union

import pandas as pd
from .Processer import Processer
from .DataReady import DataReady
from ..Utils import Formatter
from loguru import logger
import scipy.stats as st
import numpy as np


class Tester:

    @staticmethod
    def cure_data(df: pd.DataFrame | pd.Series, ticker: str):
        if len(df.shape) != 1:
            try:
                df = df.T
                assert len(df.shape) == 1
                return df
            except AssertionError:
                if ticker is not None:
                    df = df[Formatter.stock(ticker)]
                    return df
                else:
                    raise ValueError("df can contain only one column of data or you should specify a ticker")

    @classmethod
    def ICIR(
            cls,
            score: Union[pd.DataFrame, pd.Series],
            returns: Union[pd.DataFrame, pd.Series] = None,
            ticker: str = None,
    ):
        score = cls.cure_data(score, ticker)
        min_date = score.index.min()
        max_date = score.index.max()
        if returns is None:
            logger.info("自动获取回报率信息")
            dr = DataReady(begin=min_date, end=max_date)
            returns_total = dr.returns
            returns = cls.cure_data(returns_total, ticker)
        else:
            returns = cls.cure_data(returns)

        score, returns = Processer.align_dataframe(dfs=[score, returns])
        IC = pd.DataFrame(
            data=0, index=score.index, columns=['IC']
        )
        for idx_s, value_s, idx_r, value_r in zip(score.iterrows(), returns.iterrows()):
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
