import inspect
import json
import os
import re
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime, date
from functools import wraps
from pathlib import Path

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

__all__ = ["Formatter", "Tools"]




class Formatter:


    @classmethod
    def expand_dataframe(cls, data: pd.DataFrame,
                         begin: TimeType = None,
                         end: TimeType = None,
                         fill: Union[str, int, float] = 'ffill',
                         **kwargs):
        fill_args = {"method": fill} if isinstance(fill, str) else {'value': fill}
        if begin is None:
            begin = data.index.min()
        if end is None:
            end = data.index.max()
        res = pd.DataFrame(
            data=np.nan,
            columns=data.columns,
            index=TradeDate.range_trade_date(begin, end)
        )
        inter_index = data.index.intersection(res.index)
        res.loc[inter_index] = data.loc[inter_index]
        res = res.fillna(**fill_args)
        return res

    @classmethod
    def dataframe(
            cls, data: pd.DataFrame, index: bool = True, columns: bool = True, **kwargs
    ):
        res = data.copy()
        if not isinstance(res, pd.DataFrame):
            raise TypeError("data must be a DataFrame")

        if index:
            new_index, full_index = cls.format_index(res, **kwargs)
        else:
            new_index, full_index = res.index, res.index

        # if len(set(new_index)) < len(new_index):
        #     res = res.reset_index(names="index")
        #     res = res.groupby("index").apply(lambda x: x[~np.isfinite(x)])

        if columns:
            new_columns = cls.format_columns(res, **kwargs)
        else:
            new_columns = res.columns

        fill_value = kwargs.get("fill", np.nan)
        res = res.reindex(index=full_index, columns=new_columns, fill_value=fill_value).ffill()
        res = res.loc[new_index]
        return res

    @classmethod
    def format_index(cls, res: pd.DataFrame, **kwargs):
        try:
            index = TradeDate.format_date(res.index).strftime("%Y-%m-%d")
            # index = list(index)
        except ValueError as ve:
            raise ve

        # print(res.index.min(), res.index.max())
        # index = list(index)
        # for i in range(len(index)):
        #     index[i] = index[i] if TradeDate.is_trade_date(index[i]) else TradeDate.shift_trade_date(index[i], -1)
        # print(res.index.min(), res.index.max())

        res.index = pd.to_datetime(index)
        begin = kwargs.get("begin", res.index.min())
        end = kwargs.get("end", res.index.max())

        new_index = pd.date_range(begin, end, freq="D").intersection(
            TradeDate.trade_date_list
        )
        full_index = new_index.union(res.index)
        # print(len(new_index))
        return new_index, full_index

    @classmethod
    def transform_index(cls, df: pd.DataFrame):
        index = list(df.index)
        for i in range(len(index)):
            index[i] = index[i] if TradeDate.is_trade_date(index[i]) else TradeDate.shift_trade_date(index[i], -1)
        df.index = pd.to_datetime(index)

    @classmethod
    def format_columns(cls, res: pd.DataFrame, kind: str = "stock", **kwargs):
        if kind == "stock":
            res.rename(columns=cls.stock, inplace=True)
            if np.nan in res.columns:
                res.drop(columns=np.nan, inplace=True)
            new_columns = list(map(cls.stock, Config.stock_list))
            return new_columns

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
            cls,
            series: Sequence,
            pat: int,
    ) -> Sequence[Sequence] | Iterator:
        """
        :param series:
        :param pat:
        :return:
        """
        assert pat > 0
        return [series[i: i + pat] for i in range(0, len(series), pat)]

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
            res = list(filter(lambda x: keyword.lower() in x.lower() or keyword.lower() == x.lower(), attrs_map.keys()))
            count = 0
            for candidate in res:
                dic[candidate] = attrs_map[candidate]
                count += 1
                if limit is not None and count >= limit:
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