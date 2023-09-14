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
        "Relative Strength 12-month": "RSTR",
        "STREV":"STREV",
        "SEASON":"SEASON"

    }

    others: dict[str, str] = {"增强红利因子": "EnhancingDividend"}

    joint_quant: dict[str, str] = {
        "净运营资本": "net_working_capital",
        "营业总收入TTM": "total_operating_revenue_ttm",
        "营业利润TTM": "operating_profit_ttm",
        "无息流动负债": "interest_free_current_liability",
        "带息流动负债": "interest_carry_current_liability",
        "留存收益": "retained_earnings",
        "毛利TTM": "gross_profit_ttm",
        "销售费用TTM": "sale_expense_ttm",
        "营业总成本TTM": "total_operating_cost_ttm",
        "营业外收支净额TTM": "non_operating_net_profit_ttm"
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
        "每股派现(税前)": "per_cash_div",
        "市净率": "PB",
        "市盈率TTM": "PETTM",
        "一致预期PE": "PECON",
        "市现率(经营TTM)": "PCF",
        "营业总收入": "ttl_inc_oper",
        "营业利润": "oper_prof",
        "营业收入": "inc_oper",
        "销售费用": "exp_sell",
        "营业成本": "cost_oper",
        "营业外支出": "exp_noper",
        "营业外收入": "inc_noper"
    }
