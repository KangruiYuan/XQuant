import unittest
from XQuant import get_data


class MyTestCase(unittest.TestCase):


    def test_get_data_gm_factor(self):
        df = get_data(name="ACCA", begin='20230101')
        self.assertEqual(True, len(df) > 0)

    def test_get_data_future(self):
        df = get_data(name="Price_Volume_Data/main", begin='20230101')
        self.assertEqual(True, len(df) > 0)

    def test_get_data_general(self):
        df = get_data(
            "ResConSecTarpriScore", begin="20210501", ticker="000400", fields="secCode"
        )
        self.assertEqual(True, len(df) > 0)  # add assertion here


if __name__ == "__main__":
    unittest.main()
