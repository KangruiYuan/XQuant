

from .Barra import *

class IMPLEMENTED:
    raw: dict[str, str] = {
        "市值": "market_value",
        "行业分类": "industry",
        "涨跌幅": "returns",
        "换手率": "turnover",
        "收盘价": "close",
        "基准": "bench",
    }
    factor: dict[str, str] = {
        "非线性市值": "LNCAP",
        "中市值": "MIDCAP",
        "股息率": "DTOP",
        "股票月流动性": "STOM",
        "股票季流动性": "STOQ",
        "股票年流动性": "STOA",
        "流动性": "Liquidity"
    }