import unittest
import pandas as pd
from datetime import datetime
from XQuant import TradeDate, Tools, Config, Formatter


class MyTestCase(unittest.TestCase):
    def test_TradeDate_table(self):
        self.assertEqual(
            isinstance(TradeDate.trade_date_table, pd.DataFrame), True
        )  # add assertion here

    def test_TradeDate_list(self):
        self.assertEqual(isinstance(TradeDate.trade_date_list, list), True)

    def test_TradeDate_format(self):
        date_test = datetime(year=2015, month=1, day=13, hour=2, minute=56)
        self.assertEqual(pd.to_datetime(date_test), TradeDate.format_date(date_test))
        date_test = 20130401
        self.assertEqual(
            pd.to_datetime(date_test, format="%Y%m%d"), TradeDate.format_date(date_test)
        )
        date_test = "2021年3月6日"
        self.assertEqual(
            pd.to_datetime(date_test, format="%Y年%m月%d日"),
            TradeDate.format_date(date_test),
        )
        self.assertEqual(
            pd.to_datetime(date_test, format="%Y年%m月%d日"),
            Formatter.date(date_test),
        )

    def test_in_trade_date(self):
        self.assertEqual(True, TradeDate.is_trade_date("20230721"))

    def test_in_format_stock(self):
        self.assertEqual("000001.SZ", Formatter.stock(1))

    def test_packaging(self):
        my_sequence = [1, 2, 3, 4, 5]
        res = [i for i in Tools.packaging(my_sequence, pat=2, iterator=True)]
        expect_res = [[1, 2], [3, 4], [5]]
        self.assertEqual(res, expect_res)

    def test_datatables(self):
        self.assertEqual(True, "HKshszHold" in Config.datatables)

    def test_get_new_file(self):
        self.assertEqual("2023" in Tools.get_newest_file("ResConSecTarpriScore"), True)


if __name__ == "__main__":
    unittest.main()
