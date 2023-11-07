import warnings
from typing import Optional, Union

import numpy as np
import pandas as pd

from .Consts import Config
from .Toolkit import is_trade_date, shift_trade_date, format_date, format_stock, range_trade_date
from ..Schema import TimeType


def transform_index(df: pd.DataFrame, column: Optional[str] = None):
    """
    将指定日期列的日期转换到最近的交易日上，默认对index进行转换
    :param column:
    :param df:
    :return:
    """
    if column:
        seq = df[column].tolist()
    else:
        seq = list(df.index)
    for i in range(len(seq)):
        if not is_trade_date(seq[i]):
            seq[i] = shift_trade_date(seq[i], -1)
    if column:
        df[column] = pd.to_datetime(seq)
    else:
        df.index = pd.to_datetime(seq)
    return seq


def format_index(df: pd.DataFrame, pattern: str = "%Y-%m-%d", **kwargs):
    """
    格式化当前表格index，返回时间范围内所有日期及其与index的交集
    :param pattern:
    :param df:
    :param kwargs:
    :return:
    """
    # TODO:目前只适应日度扩展，对其他频率进行扩展
    try:
        index = format_date(df.index).strftime(pattern)
    except ValueError as ve:
        raise ve

    index = pd.to_datetime(index)
    df.index = index
    begin = kwargs.get("begin", index.min())
    end = kwargs.get("end", index.max())

    full_index = pd.date_range(begin, end, freq="D")
    intersection_index = full_index.intersection(Config.trade_date_list)
    return intersection_index, full_index


def format_columns(df: pd.DataFrame, kind: str = "stock", **kwargs):
    """
    将表的列名标准化
    :param df:
    :param kind:
    :param kwargs:
    :return:
    """
    # TODO:目前只正向简化，还需实现逆向
    if kind == "stock":
        df.rename(columns=format_stock, inplace=True)
        if np.nan in df.columns:
            df.drop(columns=np.nan, inplace=True)
        full_A_stock = list(map(format_stock, Config.stock_list))
        return full_A_stock


def format_dataframe(
    data: pd.DataFrame, index: bool = True, columns: bool = True, fill: Union[str, int, float] = "ffill", **kwargs
):
    """
    将宽表数据的index和column标准化
    :param data:
    :param index:
    :param columns:
    :param kwargs:
    :return:
    """

    res = data.copy()
    if not isinstance(res, pd.DataFrame):
        raise TypeError("data must be a DataFrame")

    if index:
        intersection_index, full_index = format_index(res, **kwargs)
    else:
        intersection_index, full_index = res.index, res.index
    if columns:
        new_columns = format_columns(res, **kwargs)
    else:
        new_columns = res.columns

    fill_value = kwargs.get("fill_value", np.nan)
    fill_args = {"method": fill} if isinstance(fill, str) else {"value": fill}
    res = res.reindex(
        index=full_index, columns=new_columns, fill_value=fill_value
    ).fillna(**fill_args)
    res = res.loc[intersection_index]
    return res


def expand_dataframe(
    data: pd.DataFrame,
    begin: TimeType = None,
    end: TimeType = None,
    fill: Union[str, int, float] = "ffill",
    **kwargs
):
    """
    将表格扩展到指定的起始日期（计划退役中）
    :param data:
    :param begin:
    :param end:
    :param fill:
    :param kwargs:
    :return:
    """
    warnings.warn("该函数计划退役中，请留意版本更迭。", DeprecationWarning)
    fill_args = {"method": fill} if isinstance(fill, str) else {"value": fill}
    if begin is None:
        begin = data.index.min()
    if end is None:
        end = data.index.max()
    res = pd.DataFrame(
        data=np.nan, columns=data.columns, index=range_trade_date(begin, end)
    )
    inter_index = data.index.intersection(res.index)
    res.loc[inter_index] = data.loc[inter_index]
    res = res.fillna(**fill_args)
    return res
