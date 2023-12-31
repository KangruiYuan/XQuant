import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Union, Literal, Callable, Sequence

import numpy as np
import pandas as pd
from pandas.errors import ParserError
from sqlalchemy import text

from .Utils import (
    Config,
    is_date,
    format_future,
    format_code,
    format_date,
    extend_date_span,
)
from .SQLAgent import SQLAgent
from .Schema import TimeType

__all__ = ["thread_load_file", "DataAPI"]


def run_thread_pool_sub(target: Callable, args: Sequence, max_work_count: int):
    with ThreadPoolExecutor(max_workers=max_work_count) as t:
        res = [t.submit(target, i) for i in args]
        return res


def read_from_h5(filepath: str | Path, key: str = "a"):
    """
    :param filepath:
    :param key:
    :return:
    """
    return pd.read_hdf(filepath, key=key)


def thread_load_file(load_list: list[str, Path], **kwargs):
    load_data = pd.DataFrame()
    res = run_thread_pool_sub(
        read_from_h5, load_list, max_work_count=kwargs.get("workers", 20)
    )
    for future in as_completed(res):
        res = future.result()
        if len(res) > 0:
            # 拼接数据
            try:
                if isinstance(res.index[0], datetime) or is_date(res.index[0]):
                    res = res.reset_index()
            except ParserError:
                res = res.reset_index(drop=True)
            load_data = pd.concat((load_data, res), axis=0, ignore_index=True)
    return load_data


class DataAPI:
    @classmethod
    def get_data(
        cls,
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, Sequence] = None,
        ticker: Union[str, int, Sequence] = None,
        engine: Literal["py", "sql"] = "py",
        **kwargs,
    ):
        if name not in Config.datatables:
            raise KeyError("{} is not ready for use with .h5 file!".format(name))

        assets = Config.datatables[name]["assets"]
        if assets == "sql":
            engine = "sql"

        if end is None:
            end = datetime.today().strftime("%Y%m%d")
        end = format_date(end)

        if begin:
            begin = format_date(begin)

        if isinstance(fields, str):
            fields = [fields]

        if isinstance(ticker, (int, str)):
            ticker = [ticker]

        if engine == "py":
            if assets in [
                "dataYes",
                "info",
                "em",
                "gm_stock",
                "jq_prepare",
                "jq_factor",
            ]:
                return cls.get_data_general(
                    name=name,
                    path=Config.database_dir[assets],
                    begin=begin,
                    end=end,
                    fields=fields,
                    ticker=ticker,
                    **kwargs,
                )
            elif assets in ["gm_future"]:
                return cls.get_data_gm_future(
                    name=name,
                    path=Config.database_dir[assets],
                    begin=begin,
                    end=end,
                    fields=fields,
                    ticker=ticker,
                    **kwargs,
                )
            elif assets in ["gm_factor"]:
                return cls.get_data_gm_factor(
                    name=name[:-3],
                    path=Config.database_dir[assets],
                    begin=begin,
                    end=end,
                    fields=fields,
                    ticker=ticker,
                    **kwargs,
                )
            elif assets in ["IB"]:
                return cls.get_data_from_IB(
                    name=name, begin=begin, end=end, fields=fields
                )

        elif engine == "sql":
            assert Config.datatables[name]["assets"] == "sql"
            return cls.get_data_from_sql(
                name=name,
                begin=begin,
                end=end,
                ticker=ticker,
                fields=fields,
            )

    @classmethod
    def get_data_from_IB(
        cls,
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: list[str] = None,
        **kwargs,
    ):
        table_folder = Path(Config.database_dir["IB"]) / name
        years_folder = list(table_folder.iterdir())
        begin_year = begin.year
        end_year = end.year
        years_folder = list(
            filter(lambda x: begin_year <= int(x.stem) <= end_year, years_folder)
        )
        load_list = []
        for folder in years_folder:
            load_list.extend(folder.iterdir())

        load_list = list(
            filter(lambda x: begin <= format_date(x.stem) <= end, load_list)
        )
        if load_list:
            data = thread_load_file(load_list)
            if fields is not None:
                return cls.select_fields(data=data, fields=fields)
            else:
                return data

    @classmethod
    def get_data_from_sql(
        cls,
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        ticker: list[str] = None,
        fields: list[str] = None,
        conn=None,
        **kwargs,
    ):
        if conn is None:
            # conn = SQLAgent.postgres_connection(**kwargs)
            conn = SQLAgent.postgres_engine()
        if fields is None:
            fields = "*"
        else:
            fields = ",".join([f.lower() for f in fields])
        SQL_QUERY = [f'SELECT {fields} FROM "{name}"']
        # params = {}
        condition = "WHERE"
        ticker_column = Config.datatables[name]["ticker_column"].lower()
        date_column = Config.datatables[name]["date_column"].lower()

        if ticker is not None and ticker_column:
            _tmp = ",".join(["'" + t + "'" for t in ticker])
            SQL_QUERY.append(f'{condition} "{ticker_column}" IN ({_tmp})')
            # params["ticker"] = tuple(ticker)
            condition = "AND"

        if begin is not None and date_column:
            SQL_QUERY.append(
                f'{condition} "{date_column}" >= \'{begin.strftime("%Y-%m-%d")}\''
            )
            # params["begin"] = begin
            condition = "AND"

        if end is not None and date_column:
            SQL_QUERY.append(
                f'{condition} "{date_column}" <= \'{end.strftime("%Y-%m-%d")}\''
            )
            # params["end"] = end
            condition = "AND"
        SQL_QUERY = " ".join(SQL_QUERY) + ";"
        if kwargs.get("verbose", False):
            print(SQL_QUERY)
        df = pd.read_sql_query(text(SQL_QUERY), conn.connect())
        return df

    @classmethod
    def get_data_gm_future(
        cls,
        name: str,
        path: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, list] = None,
        ticker: Union[str, int, list] = None,
        **kwargs,
    ):
        table_folder = Path(path) / name
        load_list = []
        if begin is not None:
            begin_year = begin.year
        else:
            begin_year = 2010
        end_year = end.year
        for i in range(begin_year, end_year + 1):
            tmp_folder = table_folder / str(i) / kwargs.get("sources", "gm")
            if not tmp_folder.exists():
                continue
            tmp_file_list = [str(j) for j in tmp_folder.glob("*.h5")]
            if ticker is not None:
                target_ticker = [j for j in tmp_file_list if format_future(j) in ticker]
            else:
                target_ticker = tmp_file_list
            if target_ticker:
                load_list.extend(target_ticker)
        if load_list:
            data = thread_load_file(load_list)
            return cls.select(
                name=name,
                data=data,
                begin=begin,
                end=end,
                fields=fields,
                ticker=None,
                **kwargs,
            )
        else:
            raise KeyError(f"File {name} does not exist")

    @classmethod
    def get_data_gm_factor(
        cls,
        name: str,
        path: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, list] = None,
        ticker: Union[str, int, list] = None,
        **kwargs,
    ):
        table_folder = Path(path) / name
        load_list = []
        if begin is not None:
            begin_year = begin.year
        else:
            begin_year = 2010
        end_year = end.year
        for i in range(begin_year, end_year + 1):
            tmp_folder = table_folder / str(i)
            if not tmp_folder.exists():
                continue
            tmp_file_list = [str(j) for j in tmp_folder.glob("*.h5")]
            if tmp_file_list:
                load_list.extend(tmp_file_list)
        if load_list:
            data = thread_load_file(load_list)
            return cls.select(
                name=name,
                data=data,
                begin=begin,
                end=end,
                fields=fields,
                ticker=ticker,
                gm_factor=True,
                **kwargs,
            )
        else:
            raise KeyError(f"File {name} does not exist")

    @classmethod
    def get_data_general(
        cls,
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
            Q_Y_pattern = r"Y(\d+)_Q(\d+)"
            Y_pattern = r"Y(\d+)"
            if begin:
                if re.search(Q_Y_pattern, h5_file_name_list[0]):
                    load_begin, load_end = extend_date_span(begin, end, "Q")
                    begin_num = load_begin.year * 10 + load_begin.month // 3
                    end_num = load_end.year * 10 + load_end.month // 3
                    pattern = r"Y(\d+)_Q(\d+).h5"
                    for filename in h5_file_name_list:
                        match = re.search(pattern, filename)
                        if match:
                            year, month = match.groups()
                            filename_int = int(year) * 10 + int(month)
                            if begin_num <= filename_int <= end_num:
                                load_list.append(filename)
                elif re.search(Y_pattern, h5_file_name_list[0]):
                    load_begin, load_end = extend_date_span(begin, end, "Y")
                    begin_num = load_begin.year
                    end_num = load_end.year
                    pattern = r"Y(\d+).h5"
                    for filename in h5_file_name_list:
                        match = re.search(pattern, filename)
                        if match:
                            year = match.groups()[0]
                            filename_int = int(year)
                            if begin_num <= filename_int <= end_num:
                                load_list.append(filename)
                else:
                    raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(path, name))
            else:
                if re.search(Q_Y_pattern, h5_file_name_list[0]):
                    end_num = end.year * 10 + np.ceil(end.month / 3)
                    for filename in h5_file_name_list:
                        match = re.search(Q_Y_pattern, filename)
                        if match:
                            year, month = match.groups()
                            filename_int = int(year) * 10 + int(month)
                            if filename_int <= end_num:
                                load_list.append(filename)
                elif re.search(Y_pattern, h5_file_name_list[0]):
                    end_num = end.year
                    for filename in h5_file_name_list:
                        match = re.search(Y_pattern, filename)
                        if match:
                            year = match.groups()[0]
                            filename_int = int(year)
                            if filename_int <= end_num:
                                load_list.append(filename)
                else:
                    raise KeyError("请检查{}, 文件不符合{}_Y*_Q*组织形式".format(path, name))
            data = thread_load_file(load_list)

        return cls.select(
            name=name,
            data=data,
            begin=begin,
            end=end,
            fields=fields,
            ticker=ticker,
            **kwargs,
        )

    @classmethod
    def select(
        cls,
        name: str,
        data: pd.DataFrame,
        begin: TimeType = None,
        end: TimeType = None,
        fields: list[str] = None,
        ticker: list[str, int] = None,
        **kwargs,
    ):
        if kwargs.get("gm_factor", False):
            name += "_gm"
        try:
            date_column = Config.datatables[name]["date_column"]
            if not date_column:
                date_column = None
        except KeyError:
            date_column = None
            print("{} 不支持ticker筛选".format(name))

        try:
            ticker_column = Config.datatables[name]["ticker_column"]
            if not ticker_column:
                ticker_column = None
        except KeyError:
            ticker_column = None
            print("{} 不支持ticker筛选".format(name))

        if (begin is not None or end is not None) and date_column is not None:
            data = cls.select_date(data, begin, end, date_column)
        if ticker is not None and ticker_column is not None:
            data = cls.select_ticker(data, ticker, ticker_column)

        if ticker_column is not None and date_column is not None:
            data = data.drop_duplicates(subset=[ticker_column, date_column])
        else:
            data = data.drop_duplicates()

        if fields is not None:
            data = cls.select_fields(data, fields)

        return data.reset_index(drop=True)

    @staticmethod
    def select_date(
        data: pd.DataFrame, begin: TimeType, end: TimeType, date_column: str
    ):
        data = data.reset_index(drop=True)
        data[date_column] = format_date(data[date_column])

        try:
            if begin is not None:
                data = data[data[date_column] >= begin]
            if end is not None:
                data = data[data[date_column] <= end]
        except TypeError:
            if begin is not None:
                data = data[data[date_column].dt.date >= begin.date()]
            if end is not None:
                data = data[data[date_column].dt.date <= end.date()]
        return data

    @staticmethod
    def select_ticker(data: pd.DataFrame, ticker: list[str, int], ticker_column: str):
        data = data.reset_index(drop=True)
        ticker_formatted = pd.Series(format_code(data[ticker_column]))
        return data[ticker_formatted.isin(format_code(ticker))]

    @staticmethod
    def select_fields(data: pd.DataFrame, fields: list[str]):
        return data[data.columns.intersection(fields)]
