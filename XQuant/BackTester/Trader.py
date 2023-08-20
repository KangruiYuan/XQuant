from pathlib import Path
from typing import Any

import pandas as pd
from shutil import rmtree
from ..FactorManager import DataReady, Analyzer
from ..Schema import BackTestOptions, Strategy
from ..Utils import Formatter, TradeDate
from .SignalUtils import *
import plotly.graph_objects as go
import plotly.express as px


class BackTestRunner:
    def __init__(self, signals: pd.DataFrame, options: BackTestOptions):
        self.signals = signals
        self.options: BackTestOptions = options

        self.data_manager: DataReady = None

        self.global_folder: Path = None
        self.resource_folder = None
        self.work_folder: Path = None
        self.date_range_str: str = None
        self.cache: dict[str, Any] = {}

    def prepare(self):
        self.prepare_signals()
        self.data_manager = DataReady(
            begin=self.options.begin,
            end=self.options.end,
            sql=True,
            adj=True,
            bench_code=self.options.bench_code,
        )
        self.prepare_path()
        self.prepare_resource()

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
        self.date_range_str = f"{self.options.begin.strftime('%Y%m%d')}-{self.options.end.strftime('%Y%m%d')}"

        self.global_folder = self.options.cache / self.date_range_str
        self.resource_folder = self.global_folder / "resource"
        self.work_folder = self.global_folder / self.options.surname

        if self.options.clean_cache and self.global_folder.exists():
            rmtree(self.global_folder)

        for p in [
            self.global_folder,
            self.resource_folder,
            self.work_folder,
        ]:
            p.mkdir(parents=True, exist_ok=True)

    def prepare_resource(self):
        for fea in ["close", "preclose", "bench"]:
            price_file = self.resource_folder / f"{fea}.csv"
            if price_file.exists():
                df = pd.read_csv(price_file, index_col=["date"], parse_dates=True)
            else:
                df = getattr(self.data_manager, fea)
            df.to_csv(price_file, index_label="date")
            self.cache[fea] = df

        returns = np.divide(
            self.cache["close"] - self.cache["preclose"], self.cache["preclose"]
        )
        self.cache["returns"] = returns
        returns.to_csv(self.resource_folder / "returns.csv")

    def adjust_signal(self):
        if self.options.standardize:
            self.signals = standardize(self.signals)

        if self.options.demean:
            self.signals = demean(self.signals)

        self.signals.to_csv(self.work_folder / "signals.csv", index_label="date")

    def run(self):
        self.prepare()
        self.adjust_signal()
        if self.options.method == Strategy.LONG_ONlY:
            assert np.all(
                clean(self.signals.values) >= 0
            ), f"In mode {Strategy.LONG_ONlY}, ensure that all values are greater than zero"
            weights = signal_to_weight(self.signals)
            rtn = pd.DataFrame(
                data=clean(self.cache["returns"].values) * weights.values,
                index=weights.index,
                columns=weights.columns,
            )
            weights.to_csv(
                self.work_folder / "long_only_weight.csv", index_label="date"
            )
            rtn.to_csv(self.work_folder / "long_only_rtn.csv", index_label="date")
            self.cache["long_only"] = {"weights": weights, "rtn": rtn}
        elif self.options.method == Strategy.TOP_BOTTOM:
            weights = signal_to_top_bottom_weight(
                signal=self.signals, quantile=self.options.quantile
            )
            rtn = pd.DataFrame(
                data=clean(self.cache["returns"].values) * weights.values,
                index=weights.index,
                columns=weights.columns,
            )
            weights.to_csv(
                self.work_folder / "top_bottom_weight.csv", index_label="date"
            )
            rtn.to_csv(self.work_folder / "top_bottom_rtn.csv", index_label="date")
            self.cache["top_bottom"] = {"weights": weights, "rtn": rtn}
        elif self.options.method == Strategy.GROUP:
            self.cache["group"] = {}
            group_categorize = categorize_signal_by_quantiles(
                self.signals, group_nums=self.options.group_nums
            )
            for group in range(self.options.group_nums):
                weights = signal_to_weight((group_categorize == group).astype(int))
                rtn = pd.DataFrame(
                    data=clean(self.cache["returns"].values) * weights.values,
                    index=weights.index,
                    columns=weights.columns,
                )
                weights.to_csv(
                    self.work_folder / f"group_{group}_weight.csv", index_label="date"
                )
                rtn.to_csv(
                    self.work_folder / f"group_{group}_rtn.csv", index_label="date"
                )
                self.cache["group"][group] = {"weights": weights, "rtn": rtn}
        elif self.options.method == "weight":
            assert np.all(
                clean(self.signals.values) >= 0
            ), f"In mode {Strategy.WEIGHT}, ensure that all values are greater than zero"
            weights = self.signals.copy()
            rtn = pd.DataFrame(
                    data=clean(self.cache["returns"].values) * weights.values,
                    index=weights.index,
                    columns=weights.columns,
                )
            weights.to_csv(
                self.work_folder / "weight.csv", index_label="date"
            )
            rtn.to_csv(self.work_folder / "weight_rtn.csv", index_label="date")
            self.cache["weight"] = {"weights": weights, "rtn": rtn}

    def plot(self):
        fig = go.Figure()

        fig.update_layout(
            title=f"累计回报率（{self.options.method.value}）",
            xaxis_title="日期",
            yaxis_title="累计回报率",
        )

        bench = self.cache["bench"]

        self.cache['bench_result'] = Analyzer.rtns_analysis(bench.values)

        fig.add_trace(
            go.Scatter(
                x=bench.index,
                y=bench.cumsum().values.flatten(),
                name=f"指数{self.options.bench_code}累计回报率",
            )
        )

        if self.options.method == Strategy.GROUP:
            for group in range(self.options.group_nums):
                daily_rtn = self.cache["group"][group]["rtn"].sum(axis=1)
                self.cache["group"][group]["result"] = Analyzer.rtns_analysis(daily_rtn)
                fig.add_trace(
                    go.Scatter(
                        x=daily_rtn.index,
                        y=daily_rtn.values.flatten().cumsum(),
                        name=f"Group {group} 累计回报率",
                    )
                )
        else:
            daily_rtn = self.cache[self.options.method.value]["rtn"].sum(axis=1)
            daily_rtn = daily_rtn.sort_index()
            self.cache[self.options.method.value]["result"] = Analyzer.rtns_analysis(
                daily_rtn
            )

            fig.add_trace(
                go.Scatter(
                    x=daily_rtn.index,
                    y=daily_rtn.values.flatten().cumsum(),
                    name=f"{self.options.method.value}累计回报率",
                )
            )

        if self.options.verbose:
            fig.show()
        else:
            return fig
