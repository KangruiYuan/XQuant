from pathlib import Path
from typing import Any

import pandas as pd
from shutil import rmtree
from ..FactorManager import DataReady, Analyzer
from ..Schema import BackTestOptions, Strategy
from ..Utils import Formatter, TradeDate
from .SignalUtils import *
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px


class BackTestRunner:
    def __init__(self, signals: pd.DataFrame, options: BackTestOptions):
        self._hash_mark = None
        self.signals = signals
        self.options: BackTestOptions = options

        self.data_manager: DataReady = None

        self.global_folder: Path = None
        self.resource_folder = None
        self.work_folder: Path = None
        self.date_range_str: str = None
        self.cache: dict[str, Any] = {}

        if self.options.end is None:
            self.options.end = datetime.today()

    def prepare(self, **kwargs):
        self.prepare_signals()
        self.data_manager = DataReady(
            begin=self.options.begin,
            end=self.options.end,
            sql=True,
            adj=True,
            bench_code=self.options.bench_code,
        )
        self.prepare_path()
        self.prepare_resource(**kwargs)

    def prepare_signals(self):
        signals = Formatter.dataframe(self.signals)
        signal_date_min = signals.index.min()
        signal_date_max = signals.index.max()

        options_date_min = TradeDate.shift_trade_date(self.options.begin, -1)
        options_date_max = TradeDate.shift_trade_date(self.options.end, 1)

        global_date_min = max(options_date_min, signal_date_min)
        global_date_max = min(options_date_max, signal_date_max)

        self.signals = signals[
            (signals.index >= global_date_min) & (signals.index <= global_date_max)
        ]

        self.options.begin = global_date_min
        self.options.end = global_date_max

    def prepare_path(self):
        self._hash_mark = hash(tuple(self.signals.values.tostring()))
        self.date_range_str = f"{self.options.begin.strftime('%Y%m%d')}-{self.options.end.strftime('%Y%m%d')}-{self._hash_mark}"

        self.global_folder = self.options.cache / self.date_range_str
        print("Cache: {}".format(self.global_folder))
        self.resource_folder = self.global_folder / "resource"
        self.work_folder = self.global_folder / self.options.surname

        if self.options.clean_cache and self.global_folder.exists():
            rmtree(self.global_folder)
            self.cache = {}

        for p in [
            self.global_folder,
            self.resource_folder,
            self.work_folder,
        ]:
            p.mkdir(parents=True, exist_ok=True)

        self.cache[self.date_range_str] = {}

    def prepare_resource(self, **kwargs):
        for fea in ["close", "preclose", "bench"]:
            price_file = self.resource_folder / f"{fea}.csv"
            if fea not in self.cache[self.date_range_str]:
                if price_file.exists():
                    print(f"Loading {fea} from cache ...")
                    df = pd.read_csv(price_file, index_col=["date"], parse_dates=True)
                    df = df.sort_index()
                else:
                    print(f"Loading {fea} from database ...")
                    # print(self.data_manager.begin, self.data_manager.end)
                    df = kwargs.get(fea, getattr(self.data_manager, fea))
                    df.to_csv(price_file, index_label="date")
                self.cache[self.date_range_str][fea] = df

        if "returns" not in self.cache[self.date_range_str]:
            returns = np.divide(
                self.cache[self.date_range_str]["close"]
                - self.cache[self.date_range_str]["preclose"],
                self.cache[self.date_range_str]["preclose"],
            )
            self.cache[self.date_range_str]["returns"] = returns
            if not (self.resource_folder / "returns.csv").exists():
                returns.to_csv(self.resource_folder / "returns.csv", index_label="date")

    def adjust_signal(self):
        if self.options.shift != 0:
            self.signals = self.signals.shift(self.options.shift)

        if self.options.standardize:
            self.signals = standardize(self.signals)

        if self.options.demean:
            self.signals = demean(self.signals)

        for key in self.cache[self.date_range_str]:
            df = self.cache[self.date_range_str][key]
            df = df[(df.index >= self.options.begin) & (df.index < self.options.end)]
            self.cache[self.date_range_str][key] = df

        self.signals.to_csv(self.work_folder / "signals.csv", index_label="date")

    def run(self):
        if self.options.method in [
            Strategy.LONG_ONlY,
            Strategy.WEIGHT,
            Strategy.TOP_BOTTOM,
            Strategy.SELF_DEFINED,
        ]:
            if self.options.method in [Strategy.LONG_ONlY, Strategy.TOP_BOTTOM]:
                assert np.all(
                    clean(self.signals.values) >= 0
                ), f"In mode {self.options.method.value}, ensure that all values are greater than zero"

            weights_csv = self.work_folder / f"{self.options.method.value}_weight.csv"
            rtn_csv = self.work_folder / f"{self.options.method.value}_rtn.csv"
            if (
                self.options.method.value not in self.cache[self.date_range_str]
                or "weights"
                not in self.cache[self.date_range_str][self.options.method.value]
                or "rtn"
                not in self.cache[self.date_range_str][self.options.method.value]
            ):
                if not weights_csv.exists():
                    if self.options.method == Strategy.LONG_ONlY:
                        weights = signal_to_weight(self.signals)
                    elif self.options.method == Strategy.TOP_BOTTOM:
                        weights = signal_to_top_bottom_weight(
                            signal=self.signals, quantile=self.options.quantile
                        )
                    elif self.options.method == Strategy.WEIGHT:
                        weights = self.signals.copy()
                    elif self.options.method == Strategy.SELF_DEFINED:
                        assert self.options.function is not None
                        weights = self.options.function(self.signals)
                    else:
                        raise NotImplemented(f"Method {self.options.method.value}")
                    save_weight_flag = True
                else:
                    print(f"Loading weight from existing file ...")
                    weights = pd.read_csv(
                        weights_csv, index_col=["date"], parse_dates=True
                    )
                    save_weight_flag = False

                if not rtn_csv.exists():
                    raw_returns = self.cache[self.date_range_str]["returns"]
                    raw_returns, weights = self.data_manager.align_dataframe(
                        [raw_returns, weights]
                    )
                    rtn = pd.DataFrame(
                        data=clean(raw_returns.values) * weights.values,
                        index=weights.index,
                        columns=weights.columns,
                    )
                    save_rtn_flag = True
                    save_weight_flag = True
                else:
                    print(f"Loading rtn from existing file ...")
                    rtn = pd.read_csv(rtn_csv, index_col=["date"], parse_dates=True)
                    save_rtn_flag = False

                if save_rtn_flag:
                    rtn.to_csv(rtn_csv, index_label="date")
                if save_weight_flag:
                    weights.to_csv(weights_csv, index_label="date")

                self.cache[self.date_range_str][self.options.method.value] = {
                    "weights": weights,
                    "rtn": rtn,
                }

        elif self.options.method == Strategy.GROUP:
            group_categorize = categorize_signal_by_quantiles(
                self.signals, group_nums=self.options.group_nums
            )
            if self.options.method.value not in self.cache[self.date_range_str]:
                self.cache[self.date_range_str][self.options.method.value] = {}
                for group in range(self.options.group_nums):
                    weights_csv = self.work_folder / f"group_{group}_weight.csv"
                    rtn_csv = self.work_folder / f"group_{group}_rtn.csv"
                    save_weight_flag = True
                    save_rtn_flag = True
                    if (
                        group in self.cache[self.date_range_str]
                        and "weights"
                        in self.cache[self.date_range_str][self.options.method.value][
                            group
                        ]
                    ):
                        weights = self.cache[self.date_range_str][
                            self.options.method.value
                        ][group]["weights"]
                    elif weights_csv.exists():
                        weights = pd.read_csv(
                            weights_csv, index_col=["date"], parse_dates=True
                        )
                        save_weight_flag = False
                    else:
                        weights = signal_to_weight(
                            (group_categorize == group).astype(int)
                        )
                        save_weight_flag = True

                    if (
                        group in self.cache[self.date_range_str]
                        and "rtn"
                        in self.cache[self.date_range_str][self.options.method.value][
                            group
                        ]
                    ):
                        rtn = self.cache[self.date_range_str][
                            self.options.method.value
                        ][group]["rtn"]
                    elif rtn_csv.exists():
                        rtn = pd.read_csv(rtn_csv, index_col=["date"], parse_dates=True)
                        save_rtn_flag = False
                    else:
                        raw_returns = self.cache[self.date_range_str]["returns"]
                        raw_returns, weights = self.data_manager.align_dataframe(
                            [raw_returns, weights]
                        )
                        rtn = pd.DataFrame(
                            data=clean(raw_returns.values) * weights.values,
                            index=weights.index,
                            columns=weights.columns,
                        )
                        save_rtn_flag = True
                        save_weight_flag = True

                    if save_rtn_flag:
                        rtn.to_csv(rtn_csv, index_label="date")
                    if save_weight_flag:
                        weights.to_csv(weights_csv, index_label="date")

                    self.cache[self.date_range_str][self.options.method.value][
                        group
                    ] = {
                        "weights": weights,
                        "rtn": rtn,
                    }

    def plot(self):
        if "fig" in self.cache[self.date_range_str][self.options.method.value]:
            fig = self.cache[self.date_range_str][self.options.method.value]["fig"]
        else:
            fig = go.Figure()

            fig.update_layout(
                title=f"累计回报率（{self.options.method.value}）",
                xaxis_title="日期",
                yaxis_title="累计回报率",
            )

            bench = self.cache[self.date_range_str]["bench"]

            self.cache[self.date_range_str]["bench_result"] = Analyzer.rtns_analysis(
                bench.values
            )

            fig.add_trace(
                go.Scatter(
                    x=bench.index,
                    y=bench.cumsum().values.flatten(),
                    name=f"指数{self.options.bench_code}累计回报率",
                )
            )

            if self.options.method == Strategy.GROUP:
                for group in range(self.options.group_nums):
                    daily_rtn = self.cache[self.date_range_str]["group"][group][
                        "rtn"
                    ].sum(axis=1)
                    self.cache[self.date_range_str]["group"][group][
                        "result"
                    ] = Analyzer.rtns_analysis(daily_rtn)
                    fig.add_trace(
                        go.Scatter(
                            x=daily_rtn.index,
                            y=daily_rtn.values.flatten().cumsum(),
                            name=f"Group {group} 累计回报率",
                        )
                    )
            else:
                daily_rtn = self.cache[self.date_range_str][self.options.method.value][
                    "rtn"
                ].sum(axis=1)
                daily_rtn = daily_rtn.sort_index()
                self.cache[self.date_range_str][self.options.method.value][
                    "result"
                ] = Analyzer.rtns_analysis(daily_rtn)

                fig.add_trace(
                    go.Scatter(
                        x=daily_rtn.index,
                        y=daily_rtn.values.flatten().cumsum(),
                        name=f"{self.options.method.value}累计回报率",
                    )
                )
            self.cache[self.date_range_str][self.options.method.value]["fig"] = fig

        if self.options.verbose:
            fig.show()
        else:
            return fig
