import unittest
from XQuant import DataAPI


class MyTestCase(unittest.TestCase):

    def test_get_data_sql(self):
        df = DataAPI.get_data('gmData_history', begin='20230601',)
        self.assertEqual(True, len(df) > 0)

    def test_get_data_uqer_MktIdx(self):
        df = DataAPI.get_data('uqer_MktIdx', fields=['tradedate', 'chgpct'], begin='20230101')
        self.assertEqual(True, len(df) > 0)
        self.assertEqual(2, df.shape[1])

    def test_get_data_gm_factor(self):
        df = DataAPI.get_data(name="ACCA_gm", begin='20230101')
        self.assertEqual(True, len(df) > 0)

    def test_get_data_future(self):
        df = DataAPI.get_data(name="Price_Volume_Data/main", begin='20230101')
        self.assertEqual(True, len(df) > 0)

    def test_get_data_general(self):
        df = DataAPI.get_data(
            "ResConSecTarpriScore", begin="20210501", ticker="000400", fields="secCode"
        )
        self.assertEqual(True, len(df) > 0)  # add assertion here


if __name__ == "__main__":
    unittest.main()
