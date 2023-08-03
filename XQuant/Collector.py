import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .Utils import Config, TradeDate, TimeType, Formatter
from typing import Union, Literal, Callable, Sequence
from .Consts import datatables
from datetime import datetime
from pathlib import Path
from pandas.errors import ParserError
import re


def run_thread_pool_sub(target: Callable, args: Sequence, max_work_count: int):
    with ThreadPoolExecutor(max_workers=max_work_count) as t:
        res = [t.submit(target, i) for i in args]
        return res


def read_from_h5(filepath: str | Path, key="a"):
    return pd.read_hdf(filepath, key=key)


def thread_load_file(load_list: list[str], **kwargs):
    load_data = pd.DataFrame()
    res = run_thread_pool_sub(
        read_from_h5, load_list, max_work_count=kwargs.get("workers", 20)
    )
    for future in as_completed(res):
        res = future.result()
        if len(res) > 0:
            # 拼接数据
            try:
                if isinstance(res.index[0], datetime) or TradeDate.is_date(res.index[0]):
                    res = res.reset_index()
            except ParserError:
                res = res.reset_index(drop=True)
            load_data = pd.concat((load_data, res), axis=0, ignore_index=True)
    return load_data


def get_data(
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, list] = None,
        ticker: Union[str, int, list] = None,
        engine: Literal["py", "sql"] = "py",
        **kwargs,
):
    if name not in datatables:
        raise KeyError("{} is not ready for use!".format(name))
    if end is None:
        end = datetime.today().strftime("%Y%m%d")
    end = TradeDate.format_date(end)

    if begin:
        begin = TradeDate.format_date(begin)

    if isinstance(fields, str):
        fields = [fields]

    if isinstance(ticker, (int, str)):
        ticker = [ticker]

    assets = datatables[name]["assets"]

    if engine == "py":
        if assets in ["dataYes", "info", "em", "gm_stock", "jq_prepare", "jq_factor"]:
            return get_data_general(
                name=name,
                path=Config.database_dir[assets],
                begin=begin,
                end=end,
                fields=fields,
                ticker=ticker,
                **kwargs,
            )
        elif assets in ["gm_future"]:
            pass
        elif assets in ["gm_factor"]:
            pass

    elif engine == "sql":
        pass


def get_data_general(
        name: str,
        path: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, list] = None,
        ticker: Union[str, int, list] = None,
        **kwargs,
):
    table_folder = Path(path) / name
    if not table_folder.exists():
        try:
            data: pd.DataFrame = read_from_h5(str(table_folder) + ".h5")
        except FileNotFoundError:
            raise FileNotFoundError(f"{name} do not exits!")
    else:
        load_list = []
        h5_file_name_list = [str(i) for i in table_folder.glob("*.h5")]
        if begin:
            if "Q" in h5_file_name_list[0]:
                load_begin, load_end = TradeDate.extend_date_span(begin, end, "Q")
                begin_num = load_begin.year * 10 + load_begin.month // 3
                end_num = load_end.year * 10 + load_end.month // 3
                pattern = r"(\w+)_Y(\d+)_Q(\d+).h5"
                for filename in h5_file_name_list:
                    match = re.search(pattern, filename)
                    if match:
                        _, year, month = match.groups()
                        filename_int = int(year) * 10 + int(month)
                        if begin_num <= filename_int <= end_num:
                            load_list.append(filename)
            elif "Y" in h5_file_name_list[0]:
                load_begin, load_end = TradeDate.extend_date_span(begin, end, "Y")
                begin_num = load_begin.year
                end_num = load_end.year
                pattern = r"(\w+)_Y(\d+).h5"
                for filename in h5_file_name_list:
                    match = re.search(pattern, filename)
                    if match:
                        _, year = match.groups()
                        filename_int = int(year)
                        if begin_num <= filename_int <= end_num:
                            load_list.append(filename)
            else:
                raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(path, name))
        else:
            if "Q" in h5_file_name_list[0]:
                end_num = end.year * 10 + np.ceil(end.month / 3)
                pattern = r"(\w+)_Y(\d+)_Q(\d+).h5"
                for filename in h5_file_name_list:
                    match = re.search(pattern, filename)
                    if match:
                        _, year, month = match.groups()
                        filename_int = int(year) * 10 + int(month)
                        if filename_int <= end_num:
                            load_list.append(filename)
            elif "Y" in h5_file_name_list[0]:
                end_num = end.year
                pattern = r"(\w+)_Y(\d+).h5"
                for filename in h5_file_name_list:
                    match = re.search(pattern, filename)
                    if match:
                        _, year = match.groups()
                        filename_int = int(year)
                        if filename_int <= end_num:
                            load_list.append(filename)
            else:
                raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(path, name))
        data = thread_load_file(load_list)

    return select(
        name=name,
        data=data,
        begin=begin,
        end=end,
        fields=fields,
        ticker=ticker,
        **kwargs,
    )


def select(
        name: str,
        data: pd.DataFrame,
        begin: TimeType = None,
        end: TimeType = None,
        fields: list[str] = None,
        ticker: list[str, int] = None,
        **kwargs,
):

    if begin is not None or end is not None:
        try:
            date_column = datatables[name]["date_column"]
            data = select_date(data, begin, end, date_column)
        except KeyError:
            print("{} 不支持ticker筛选".format(name))

    if ticker is not None:
        try:
            ticker_column = datatables[name]["ticker_column"]
            data = select_ticker(data, ticker, ticker_column)
        except KeyError:
            print("{} 不支持ticker筛选".format(name))

    if fields is not None:
        data = select_fields(data, fields)

    return data


def select_date(data: pd.DataFrame, begin: TimeType, end: TimeType, date_column: str):
    data[date_column] = TradeDate.format_date(data[date_column])
    if begin is not None:
        data = data[data[date_column] >= begin]
    if end is not None:
        data = data[data[date_column] <= end]
    return data.reset_index()


def select_ticker(data: pd.DataFrame, ticker: list[str, int], ticker_column: str):
    ticker_formatted = pd.Series(Formatter.format_code(data[ticker_column]))
    return data[ticker_formatted.isin(Formatter.format_code(ticker))].reset_index()


def select_fields(data: pd.DataFrame, fields: list[str]):
    return data[data.columns.intersection(fields)]
