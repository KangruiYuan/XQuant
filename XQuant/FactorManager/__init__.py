from .DataReady import *
from .Processer import *
from .Analyzer import *
from .BarraCNE6 import *
from .Others import *
from .JointQuant import *


class IMPLEMENTED:
    barra: dict[str, str] = {
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
        "ResidualVolatility": "ResidualVolatility",
        "账面市值比": "BTOP",
        "EP比": "ETOP",
        "分析师预测EP比": "ETOPF",
        "盈利率": "EarningYield",
    }

    others: dict[str, str] = {"增强红利因子": "EnhancingDividend"}

    joint_quant: dict[str, str] = {"净运营资本": "net_working_capital"}

    raw: dict[str, str] = {
        "市值": "market_value",
        "流通市值": "neg_market_value",
        "每股盈余": "EPS",
        "行业分类": "industry",
        "涨跌幅": "returns",
        "换手率": "turnover",
        "收盘价": "close",
        "基准": "bench",
        "每股派现(税前)": "per_cash_div",
        "市净率": "PB",
        "市盈率TTM": "PETTM",
        "一致预期PE": "PECON",
        "市现率(经营TTM)": "PCF",
    }
