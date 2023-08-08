import unittest
from XQuant import DataAPI


class MyTestCase(unittest.TestCase):


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
