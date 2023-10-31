import inspect
import json
import os
import re
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime
from functools import wraps
from time import strptime
from typing import Union, Literal, Sequence

import h5py
import numpy as np
import pandas as pd
import psutil
from fuzzywuzzy import process
from pandas import Timestamp
from pathlib import Path
from psutil._common import bytes2human
from tqdm import tqdm

from .Consts import Config
from ..Schema import TimeType, TimeArrays, TimeRaw, TimeReady, NormalArrays


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

    pattern = kwargs.get("pattern", "") or ""
    if isinstance(date_repr, TimeArrays):
        if isinstance(date_repr[0], TimeRaw) and not pattern:
            pattern = is_date(date_repr[0], pattern_return=True, **kwargs)
    elif isinstance(date_repr, TimeType):
        if isinstance(date_repr, TimeRaw) and not pattern:
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
        return Config.trade_date_list[index_begin : index_end + 1]
    elif lag is not None:
        if lag < 0:
            index_end = index_begin
            index_begin -= lag
        else:
            index_end = index_begin + lag
        return Config.trade_date_list[index_begin : index_end + 1]
    else:
        raise AttributeError("参数end与参数lag需要至少有一个不为空")


def format_stock(code: str | int) -> str:
    """
    使得股票代码标准化
    :param code: '000001', '000001.XSHE' etc.
    :return: '000001.SZ'
    """
    if isinstance(code, str):
        if code[-2:] in ["BJ", "SZ", "SH"]:
            return code
        elif "." in code or code.isdigit():
            if code[:6].isdigit():
                num = code[:6]
            elif code[-6:].isdigit():
                num = code[-6:]
            else:
                raise ValueError(f"无效股票代码： {code}")
            code = int(num)
        else:
            return np.nan
    tag = code // 100000
    if tag in [4, 8]:
        tail = "BJ"
    elif code < 500000:
        tail = "SZ"
    else:
        tail = "SH"
    res = "{:06.0f}.{}".format(code, tail)
    return res


def format_future(code: str):
    """
    格式化期货代码
    :param code:
    :return:
    """
    if "qe" in code:
        out = code.split("_")[0].upper()
    else:
        out = code.split(".")[1]
        if "_" in out:
            out = out.split("_")[0].upper()

    if out in Config.futures_list:
        return out
    else:
        raise KeyError("{} 格式化失败，请检查期货代码。".format(code))


def format_code(
    code: Union[NormalArrays, int, str], kind: Literal["stock", "future"] = "stock"
):
    """
    通用的代码格式化函数
    :param code:
    :param kind: Literal["stock", "future"]
    :return:
    """
    if kind == "stock":
        func = format_stock
    elif kind == "future":
        func = format_future
    else:
        raise NotImplementedError(f"Method not implemented for {kind}")

    if isinstance(code, NormalArrays):
        return [func(c) for c in code]
    elif isinstance(code, (int, str)):
        return func(code)


def watcher(func: callable):
    """
    监控函数的运行时间
    :param func:
    :return:
    """

    @wraps(func)
    def timer(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print(f"“{func.__name__}” run time: {end - start}.")
        return result

    return timer


def packaging(
    series: Sequence,
    pat: int,
) -> Sequence[Sequence]:
    """
    :param series:
    :param pat:
    :return:
    """
    assert pat > 0
    return [series[i : i + pat] for i in range(0, len(series), pat)]


def get_config(
    filename: Union[str, os.PathLike],
    section: str = None,
    **kwargs,
) -> dict[str, str | dict[str, str]]:
    """

    :param filename:
    :param section:
    :return:
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if section is None:
        res = dict()
        for sec in parser.sections():
            params = parser.items(sec)
            tmp = dict(params)
            res[sec] = tmp
    else:
        if parser.has_section(section):
            res = dict(parser.items(section))
        else:
            raise KeyError(f"Section {section} not found")

    return res


def get_newest_file(name: str, **kwargs):
    assets = Config.datatables[name]["assets"]
    if assets == "gm_factor":
        name = name[:-3]
    elif assets == "sql":
        return None
    base_folder = Config.database_dir[assets]
    table_folder = Path(base_folder) / name
    today = datetime.today()
    newest_file = ""
    if assets in [
        "dataYes",
        "info",
        "em",
        "gm_stock",
        "jq_prepare",
        "jq_factor",
    ]:
        files = [str(i) for i in table_folder.glob("*.h5")]
        if not files:
            file = table_folder.with_suffix(".h5")
            if file.exists():
                return file
            else:
                raise NotImplementedError(table_folder)

        newest_date = 0
        Q_Y_pattern = r"Y(\d+)_Q(\d+)"
        Y_pattern = r"Y(\d+)"
        if re.search(Q_Y_pattern, files[0]):
            today_num = today.year * 10 + np.ceil(today.month / 3)
            for file in files:
                match = re.search(Q_Y_pattern, file)
                if match:
                    year, month = match.groups()
                    date_num = int(year) * 10 + int(month)
                    if newest_date < date_num <= today_num:
                        newest_file = file
                        newest_date = date_num
        elif re.search(Y_pattern, files[0]):
            today_num = today.year
            for file in files:
                match = re.search(Y_pattern, file)
                if match:
                    year = match.groups()[0]
                    date_num = int(year)
                    if newest_date < date_num <= today_num:
                        newest_file = file
                        newest_date = date_num
        else:
            # TODO: 考虑其他文件格式的h5文件
            raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(base_folder, name))
    elif assets in ["gm_future"]:
        subfolders = [
            subfolder for subfolder in table_folder.iterdir() if subfolder.is_dir()
        ]
        if subfolders:
            max_year = max([int(i.stem) for i in subfolders])
            newest_folder = table_folder / str(max_year) / kwargs.get("sources", "gm")
            newest_file = list(newest_folder.glob("*.h5"))
    elif assets in ["gm_factor"]:
        subfolders = [
            subfolder for subfolder in table_folder.iterdir() if subfolder.is_dir()
        ]
        if subfolders:
            max_year = max([int(i.stem) for i in subfolders])
            newest_file = table_folder / str(max_year) / (name + ".h5")
    if newest_file:
        return newest_file
    else:
        raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(base_folder, name))


def search_keyword(
    keyword: str,
    fuzzy: bool = True,
    limit: int = 5,
    update: bool = False,
    initial_path: str = Path(__file__).parent[1] / "Temp/attrs.json",
    **kwargs,
):
    """
    :param initial_path: The initialization path of the log file
    :param keyword: the content you want to search for
    :param fuzzy: fuzzy matching or not
    :param limit: number of the results
    :param update: forced updating
    :return:
    """
    initial_path = Path(initial_path)
    print(f"缓存文件被保存至{initial_path}")
    if not initial_path.exists() or update:
        attrs_map = defaultdict(list)
        with tqdm(Config.datatables.keys()) as t:
            t.set_description("正在初始化...")
            for name in t:
                try:
                    path = get_newest_file(name)
                    if path is None:
                        continue
                except (IndexError, KeyError, NotImplementedError) as e:
                    if kwargs.get("verbose", True):
                        print(f"Name: {name}, Message: {e.message}")
                        continue
                # TODO: 该方法无法正常使用时选用get_data
                if isinstance(path, list):
                    path = path[0]
                data = h5py.File(path)
                try:
                    if "S" in str(data["a"]["axis0"].dtype):
                        columns = data["a"]["axis0"][:]
                    elif "S" in str(data["a"]["axis1"].dtype):
                        columns = data["a"]["axis1"][:]
                except KeyError as e:
                    if kwargs.get("verbose", True):
                        print(f"Path: {path}, Message: {e.message}")
                    continue
                for c in columns:
                    attrs_map[c.decode("utf-8")].append(name)
                t.set_postfix({"状态": "{} 写入成功".format(name)})
            with initial_path.open("w") as write_file:
                json.dump(attrs_map, write_file, indent=4)
    else:
        with initial_path.open() as read_file:
            attrs_map = json.load(read_file)

    dic = {}
    if fuzzy:
        res = process.extract(keyword, attrs_map.keys(), limit=limit)
        for candidate, score in res:
            dic[candidate] = attrs_map[candidate]
    else:
        res = list(
            filter(
                lambda x: keyword.lower() in x.lower() or keyword.lower() == x.lower(),
                attrs_map.keys(),
            )
        )
        count = 0
        for candidate in res:
            dic[candidate] = attrs_map[candidate]
            count += 1
            if limit is not None and count >= limit:
                break
    return dic


def varname(p):
    """
    将变量转化为变量名（字符串）
    :param p: 想要搜寻的变量
    :return: 变量的名字
    """
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r"\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)", line)
        if m:
            return m.group(1)


def memory_analysis():
    pid = os.getpid()
    # 创建psutil的Process对象
    _process = psutil.Process(pid)
    # 获取脚本当前的内存使用量（以字节为单位）
    memory_info = _process.memory_info()
    memory_usage = memory_info.rss
    # 将内存使用量转换为更友好的格式
    memory_usage_readable = bytes2human(memory_usage)

    print("Memory Usage:", memory_usage_readable)
