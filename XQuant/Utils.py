import inspect
import json
import os
import re
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime, date
from functools import wraps
from pathlib import Path
from time import strptime
from typing import Sequence, Iterator
from typing import Union, Literal, Tuple, Any

import h5py
import numpy as np
import pandas as pd
import psutil
from fuzzywuzzy import process
from psutil._common import bytes2human
from tqdm import tqdm
from loguru import logger
from .Consts import datatables
from .Schema import TimeType


__all__ = ["Formatter", "TradeDate", "Config", "Tools"]




class Config:
    database_dir = {
        "info": r"E:\Share\Stk_Data\dataFile",
        "dataYes": r"E:\Share\Stk_Data\dataFile",
        "gm_future": r"E:\Share\Fut_Data",
        "gm_factor": r"E:\Share\Stk_Data\gm",
        "gm_stock": r"E:\Share\Stk_Data\gm",
        "em": r"E:\Share\EM_Data",
        "jq_factor": r"E:\Share\JointQuant_Factor",
        "jq_prepare": r"E:\Share\JointQuant_prepare",
    }

    datasets_name = list(database_dir.keys())
    datatables = datatables

    stock_table: pd.DataFrame = pd.read_hdf(
        "{}/stock_info.h5".format(database_dir["info"])
    )
    stock_list = stock_table["symbol"].tolist()
    stock_num_list = stock_table["sec_id"].unique().tolist()

    futures_list: list[str | Any] = (
        "AG",
        "AL",
        "AU",
        "A",
        "BB",
        "BU",
        "B",
        "CF",
        "CS",
        "CU",
        "C",
        "FB",
        "FG",
        "HC",
        "IC",
        "IF",
        "IH",
        "I",
        "JD",
        "JM",
        "JR",
        "J",
        "LR",
        "L",
        "MA",
        "M",
        "NI",
        "OI",
        "PB",
        "PM",
        "PP",
        "P",
        "RB",
        "RI",
        "RM",
        "RS",
        "RU",
        "SF",
        "SM",
        "SN",
        "SR",
        "TA",
        "TF",
        "T",
        "V",
        "WH",
        "Y",
        "ZC",
        "ZN",
        "PG",
        "EB",
        "AP",
        "LU",
        "SA",
        "TS",
        "CY",
        "IM",
        "PF",
        "PK",
        "CJ",
        "UR",
        "NR",
        "SS",
        "FU",
        "EG",
        "LH",
        "SP",
        "RR",
        "SC",
        "WR",
        "BC",
    )

    trade_date_table: pd.DataFrame = pd.read_hdf(
        "{}/tradeDate_info.h5".format(database_dir["info"])
    )
    trade_date_list = trade_date_table["tradeDate"].dropna().to_list()

    quarter_begin = ["0101", "0401", "0701", "1001"]
    quarter_end = ["0331", "0630", "0930", "1231"]


class TradeDate:
    trade_date_table = Config.trade_date_table
    trade_date_list = Config.trade_date_list

    @classmethod
    def is_date(
        cls, date_repr: TimeType, pattern_return: bool = False, **kwargs
    ) -> bool | str:
        return Formatter.is_date(date_repr, pattern_return, **kwargs)

    @classmethod
    def format_date(
        cls,
        date_repr: Union[TimeType, pd.Series, list, tuple],
        **kwargs,
    ) -> pd.Series | pd.Timestamp:
        return Formatter.date(date_repr, **kwargs)

    @classmethod
    def extend_date_span(
        cls, begin: TimeType, end: TimeType, freq: Literal["Q", "q", "Y", "y", "M", "m"]
    ) -> tuple[datetime, datetime]:
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
        begin = cls.format_date(begin)
        end = cls.format_date(end)
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
            raise AttributeError("frq should be M, Q or Y!")

    @classmethod
    def is_trade_date(cls, date_repr: TimeType) -> bool:
        res, _ = cls.binary_search(cls.trade_date_list, date_repr)
        return res

    @classmethod
    def binary_search(
        cls, arr: Union[pd.Series, list, tuple, np.ndarray], target: TimeType
    ) -> Tuple[bool, int]:
        """
        :param arr:
        :param target:
        :return:
        """
        if isinstance(arr[0], (pd.Timestamp, datetime, date)):
            target = cls.format_date(target)

        low: int = 0
        high: int = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return True, mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return False, low

    @classmethod
    def shift_trade_date(
        cls,
        date_repr: TimeType,
        lag: int,
    ) -> pd.Timestamp:
        """
        :param date_repr:
        :param lag:
        :return:
        """
        date_repr = cls.format_date(date_repr)
        res, index = cls.binary_search(cls.trade_date_list, date_repr)
        return cls.trade_date_list[index + lag]

    @classmethod
    def range_trade_date(cls, begin: TimeType, end: TimeType = None, lag: int = None):
        """
        :param begin:
        :param end:
        :param lag:
        :return:
        """
        begin = cls.format_date(begin)
        _, index_begin = cls.binary_search(cls.trade_date_list, begin)
        if end is not None:
            end = cls.format_date(end)
            res, index_end = cls.binary_search(cls.trade_date_list, end)
            if not res:
                index_end += 1
            return cls.trade_date_list[index_begin : index_end + 1]
        elif lag is not None:
            if lag < 0:
                index_end = index_begin
                index_begin -= lag
            else:
                index_end = index_begin + lag
            return cls.trade_date_list[index_begin : index_end + 1]
        else:
            raise AttributeError("Pass attribute end or lag to the function!")


class Formatter:
    @classmethod
    def is_date(
        cls, date_repr: TimeType, pattern_return: bool = False, **kwargs
    ) -> bool | str:
        if not isinstance(date_repr, str):
            date_repr = str(date_repr)

        chinesenum = {
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
            if temp in chinesenum:
                if temp == "十":
                    if date_repr[i + 1] not in chinesenum:
                        date_str_res += chinesenum[temp]
                    elif date_repr[i - 1] in chinesenum:
                        continue
                    else:
                        date_str_res += "1"
                else:
                    date_str_res += chinesenum[temp]
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

    @classmethod
    def date(
        cls,
        date_repr: Union[TimeType, pd.Series, list, tuple],
        **kwargs,
    ) -> pd.Series | pd.Timestamp:
        if isinstance(date_repr, (list, tuple, pd.Series)):
            if isinstance(date_repr[0], (datetime, date)):
                return pd.to_datetime(date_repr)
            elif isinstance(date_repr[0], (int, str)):
                pattern = cls.is_date(date_repr[0], pattern_return=True, **kwargs)
                return pd.to_datetime(date_repr, format=pattern)
        elif isinstance(date_repr, TimeType):
            if isinstance(date_repr, (datetime, date, pd.Timestamp)):
                return pd.to_datetime(date_repr)
            elif isinstance(date_repr, (int, str)):
                pattern = cls.is_date(date_repr, pattern_return=True, **kwargs)
                return pd.to_datetime(date_repr, format=pattern)
        else:
            raise TypeError(f"date_repr {type(date_repr)} is not supported")

    @classmethod
    def dataframe(cls, data: pd.DataFrame, **kwargs):
        res = data.copy()
        if not isinstance(res, pd.DataFrame):
            raise TypeError("data must be a DataFrame")
        try:
            res.index = pd.to_datetime(res.index)
        except ValueError:
            try:
                res.index = list(map(TradeDate.format_date, res.index))
            except TypeError as te:
                raise te

        res = res.rename(columns=cls.stock)
        if np.nan in res.columns:
            res = res.drop(columns=np.nan)

        begin = kwargs.get("begin", res.index.min())
        end = kwargs.get("end", res.index.max())

        new_index = pd.date_range(begin, end, freq="D").intersection(
            TradeDate.trade_date_list
        )
        new_columns = list(map(cls.stock, Config.stock_list))

        fill_value = kwargs.get("fill", np.nan)
        return res.reindex(index=new_index, columns=new_columns, fill_value=fill_value)

    @classmethod
    def stock(cls, code: str | int) -> str:
        """
        Standardize the stock code to wind format
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
                    raise ValueError(f"Invalid stock code {code}")
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
        format_code = "{:06.0f}.{}".format(code, tail)
        return format_code

    @classmethod
    def future(cls, code: str):
        if "qe" in code:
            out = code.split("_")[0].upper()
        else:
            out = code.split(".")[1]
            if "_" in out:
                out = out.split("_")[0].upper()

        if out in Config.futures_list:
            return out
        else:
            raise KeyError("{} is not format futures!".format(code))

    @classmethod
    def format_code(cls, code: Union[Sequence, int, str], kind="stock"):
        if kind == "stock":
            func = cls.stock
        elif kind == "future":
            func = cls.future
        else:
            raise NotImplementedError(f"Method not implemented for {kind}")

        if isinstance(code, (list, tuple, pd.Series)):
            return [func(c) for c in code]
        elif isinstance(code, (int, str)):
            return func(code)


class Tools:
    @classmethod
    def info_lag(cls, data: pd.DataFrame, n_lag: int, clean: bool = False):
        """
        Delay the time corresponding to the data by n trading days
        :param clean:
        :param data:
        :param n_lag:
        :return:
        """
        res = data.copy()
        res = res.sort_index()
        if clean:
            res = Formatter.dataframe(res)
        res = res.shift(n_lag)
        res = res.dropna(axis=0, how="all")
        return res

    @classmethod
    def watcher(cls, func: callable):
        """
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
            logger.info(f"“{func.__name__}” run time: {end - start}.")
            return result

        return timer

    @classmethod
    def packaging(
        cls, series: Sequence, pat: int,
    ) -> Sequence[Sequence] | Iterator:
        """
        :param series:
        :param pat:
        :return:
        """
        assert pat > 0
        return [series[i : i + pat] for i in range(0, len(series), pat)]

    @classmethod
    def get_config(
        cls,
        filename: Union[str, os.PathLike] = Path(__file__).parent
        / "Tokens"
        / "quant.const.ini",
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

    @classmethod
    def get_newest_file(cls, name: str, **kwargs):
        assets = datatables[name]["assets"]
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
                newest_folder = (
                    table_folder / str(max_year) / kwargs.get("sources", "gm")
                )
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

    @classmethod
    def search_keyword(
        cls,
        keyword: str,
        fuzzy: bool = True,
        limit: int = 5,
        update: bool = False,
        initial_path: str = Path(__file__).parent / "Temp/attrs.json",
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
        logger.info(f"缓存文件被保存至{initial_path}")
        if not initial_path.exists() or update:
            attrs_map = defaultdict(list)
            with tqdm(datatables.keys()) as t:
                t.set_description("正在初始化...")
                for name in t:
                    try:
                        path = cls.get_newest_file(name)
                        if path is None:
                            continue
                    except (IndexError, KeyError, NotImplementedError) as e:
                        if kwargs.get("verbose", True):
                            logger.error(f"Name: {name}")
                            logger.error(e)
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
                            logger.error(e)
                            logger.error(path)
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
            res = list(filter(lambda x: keyword in x or keyword == x, attrs_map.keys()))
            count = 0
            for candidate in res:
                dic[candidate] = attrs_map[candidate]
                count += 1
                if count >= limit:
                    break
        return dic

    @classmethod
    def varname(cls, p):
        """
        将变量转化为变量名（字符串）
        :param p: 想要搜寻的变量
        :return: 变量的名字
        """
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(r"\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)", line)
            if m:
                return m.group(1)

    @staticmethod
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
