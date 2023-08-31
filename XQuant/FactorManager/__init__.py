
from .DataReady import *
from .Processer import *
from .Analyzer import *
from .BarraCNE6 import *
from .Others import *
from .JointQuant import *

class IMPLEMENTED:
    factor: dict[str, str] = {
        "非线性市值": "LNCAP",
        "中市值": "MIDCAP",
        "股息率": "DTOP",
        "股票月流动性": "STOM",
        "股票季流动性": "STOQ",
        "股票年流动性": "STOA",
        "流动性": "Liquidity",
        "历史BETA": "HBETA",
        "历史ALPHA": "HALPHA",
        "历史SIGMA": "HSIGMA",
        "CMRA": "CMRA",
        "DASTD": "DASTD",
        "ResidualVolatility": "ResidualVolatility"

    }
    raw: dict[str, str] = {
        "市值": "market_value",
        "流通市值": "neg_market_value",
        "每股盈余": "EPS",
        "行业分类": "industry",
        "涨跌幅": "returns",
        "换手率": "turnover",
        "收盘价": "close",
        "基准": "bench",
        "每股派现(税前)": "per_cash_div"
    }
