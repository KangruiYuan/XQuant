from time import strptime
from typing import Union, Literal

import pandas as pd
from pandas import Timestamp

from ..Schema import TimeType, TimeArrays, TimeRaw, TimeReady, NormalArrays
from .Consts import Config


def binary_search(arr: NormalArrays, target: TimeType) -> tuple[bool, int]:
    """
    二分法搜索目标
    :param arr:
    :param target:
    :return: 元组，（是否位于序列中，索引）
    """
    if isinstance(arr[0], TimeReady):
        target = format_date(target)

    low: int = 0
    high: int = len(arr) - 1
    while low <= high:
        mid = (low + high) >> 1
        if arr[mid] == target:
            return True, mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return False, low


def is_date(date_repr: TimeType, pattern_return: bool = False, **kwargs) -> bool | str:
    """
    判断对象是否为表示时间的格式
    int: 20230101
    str: '20230101'
    Timestamp: Timestamp('2023-01-01 00:00:00')
    datetime: datetime.datetime(2023, 1, 1, 0, 0)
    date: datetime.date(2023, 1, 1)
    :param date_repr:
    :param pattern_return:
    :param kwargs:
    :return:
    """
    if not isinstance(date_repr, str):
        date_repr = str(date_repr)

    chinese_to_num = {
        "一": "1",
        "二": "2",
        "三": "3",
        "四": "4",
        "五": "5",
        "六": "6",
        "七": "7",
        "八": "8",
        "九": "9",
        "零": "0",
        "十": "10",
    }
    date_str_res = ""
    for i in range(len(date_repr)):
        temp = date_repr[i]
        if temp in chinese_to_num:
            if temp == "十":
                if date_repr[i + 1] not in chinese_to_num:
                    date_str_res += chinese_to_num[temp]
                elif date_repr[i - 1] in chinese_to_num:
                    continue
                else:
                    date_str_res += "1"
            else:
                date_str_res += chinese_to_num[temp]
        else:
            date_str_res += temp

    pattern = (
        "%Y年%m月%d日",
        "%Y-%m-%d",
        "%y年%m月%d日",
        "%y-%m-%d",
        "%Y/%m/%d",
        "%Y%m%d",
    ) + kwargs.get("pattern", ())
    for i in pattern:
        try:
            ret = strptime(date_str_res, i)
            if ret:
                return True if not pattern_return else i
        except ValueError as _:
            continue
    return False if not pattern_return else None


def is_trade_date(date_repr: TimeType) -> bool:
    res, _ = binary_search(Config.trade_date_list, date_repr)
    return res


def format_date(
    date_repr: Union[TimeType, TimeArrays],
    **kwargs,
) -> pd.Timestamp | pd.DatetimeIndex:
    """
    将对象转化为pandas内的Timestamp或DatetimeIndex格式
    :param date_repr:
    :param kwargs:
    :return:
    """

    pattern = ""
    if isinstance(date_repr, TimeArrays):
        if isinstance(date_repr[0], TimeRaw):
            pattern = is_date(date_repr[0], pattern_return=True, **kwargs)
    elif isinstance(date_repr, TimeType):
        if isinstance(date_repr, TimeRaw):
            pattern = is_date(date_repr, pattern_return=True, **kwargs)
    else:
        raise TypeError(f"date_repr {type(date_repr)} is not supported")

    return (
        pd.to_datetime(date_repr, format=pattern)
        if pattern
        else pd.to_datetime(date_repr)
    )

def shift_trade_date(
        date_repr: TimeType,
        lag: int,
) -> pd.Timestamp:
    """
    对当前日期进行偏移，偏移到指定lag数量的交易日
    :param date_repr:
    :param lag:
    :return:
    """
    res, index = binary_search(Config.trade_date_list, date_repr)
    res_index = index + lag
    if res_index < 0:
        res_index = 0
    elif res_index >= len(Config.trade_date_list):
        res_index = -1
    return Config.trade_date_list[res_index]


def extend_date_span(
    begin: TimeType, end: TimeType, freq: Literal["Q", "q", "Y", "y", "M", "m"]
) -> tuple[Timestamp, Timestamp]:
    """
    将区间[begin, end] 进行拓宽, 依据freq将拓展至指定位置, 详见下
    freq = M :
        [2018-01-04, 2018-04-20] -> [2018-01-01, 2018-04-30]
        [2018-01-01, 2018-04-20] -> [2018-01-01, 2018-04-30]
        [2018-01-04, 2018-04-30] -> [2018-01-01, 2018-04-30]
    freq = Q :
        [2018-01-04, 2018-04-20] -> [2018-01-01, 2018-06-30]
        [2018-01-01, 2018-04-20] -> [2018-01-01, 2018-06-30]
        [2018-01-04, 2018-06-30] -> [2018-01-01, 2018-06-30]
    freq = Y :
        [2018-01-04, 2018-04-20] -> [2018-01-01, 2018-12-31]
        [2018-01-01, 2018-04-20] -> [2018-01-01, 2018-12-31]
        [2018-01-04, 2018-12-31] -> [2018-01-01, 2018-12-31]
    """
    begin = format_date(begin)
    end = format_date(end)
    if freq in ["Q", "q"]:
        if not pd.DateOffset().is_quarter_start(begin):
            begin = begin - pd.offsets.QuarterBegin(n=1, startingMonth=1)
        if not pd.offsets.DateOffset().is_quarter_end(end):
            end = end + pd.offsets.QuarterEnd(n=1)
        return begin, end
    elif freq in ["Y", "y"]:
        if not pd.offsets.DateOffset().is_year_start(begin):
            begin = begin - pd.offsets.YearBegin(n=1)
        if not pd.offsets.DateOffset().is_year_end(end):
            end = end + pd.offsets.YearEnd(n=1)
        return begin, end
    elif freq in ["M", "m"]:
        if not pd.DateOffset().is_month_start(begin):
            begin = begin - pd.offsets.MonthBegin(n=1)
        if not pd.offsets.DateOffset().is_month_end(end):
            end = end + pd.offsets.MonthEnd(n=1)
        return begin, end
    else:
        raise AttributeError(f"freq (参数：频率) 只能为M,Q或者Y之一，当前为{freq}")


def range_trade_date(begin: TimeType, end: TimeType = None, lag: int = None):
    """
    返回指定起始日期之间的所有交易日或者根据开始日期进行偏移，获得区间内所有的交易日
    :param begin:
    :param end:
    :param lag:
    :return:
    """
    _, index_begin = binary_search(Config.trade_date_list, begin)
    if end is not None:
        res, index_end = binary_search(Config.trade_date_list, end)
        if not res:
            index_end += 1
        return Config.trade_date_list[index_begin: index_end + 1]
    elif lag is not None:
        if lag < 0:
            index_end = index_begin
            index_begin -= lag
        else:
            index_end = index_begin + lag
        return Config.trade_date_list[index_begin: index_end + 1]
    else:
        raise AttributeError("参数end与参数lag需要至少有一个不为空")
