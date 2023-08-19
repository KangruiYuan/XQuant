from pathlib import Path

import pandas as pd
from shutil import rmtree
from ..FactorManager.DataReady import DataReady
from ..Schema import BackTestOptions
from ..Utils import Formatter, TradeDate
from .SignalUtils import *

class BackTestRunner:
    def __init__(self, signals: pd.DataFrame, options: BackTestOptions):
        self.signals = signals
        self.options: BackTestOptions = options

        self.data_manager: DataReady = None

        self.global_folder: Path = None
        self.resource_folder = None
        self.work_folder: Path = None
        self.date_range_str: str = None
        self.cache: dict[str, pd.DataFrame] = {}

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

    def adjust_signal(self):
        if self.options.standardize:
            self.signal = standardize(self.signal)

        if self.options.demean:
            self.signal = demean(self.signal)

        self.signal.to_csv(self.work_folder / "signal.csv", index_label="date")

    def run(self):
        self.prepare()
        pass
