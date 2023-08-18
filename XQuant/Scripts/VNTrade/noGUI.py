from time import sleep
from loguru import logger
import pandas as pd
from vnpy_da import DaGateway
from vnpy_scripttrader import ScriptTraderApp, ScriptEngine, init_cli_trading

# 导入下单需要的常量
from vnpy.trader.constant import *
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import SubscribeRequest, Exchange


if __name__ == "__main__":
    # 设置登录账号，默认用的simnow模拟账号，可以在simnow网站申请
    setting = {
        "用户名": "AF20230451",
        "密码": "888888",
        "经纪商代码": "DAHK",
        "交易服务器": "222.73.119.230:7003",
        "行情服务器": "222.73.105.170:9430",
        "授权码": "0000000000000000",
    }

    engine = init_cli_trading([DaGateway])
    engine.connect_gateway(setting, gateway_name="DA")
    # req = SubscribeRequest(symbol="6A2309", exchange=Exchange.CME)
    engine.strategy_active = True

    sleep(35)

    vt_symbols = ["6A2309.CME"]
    engine.subscribe(vt_symbols=vt_symbols)
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        logger.info(contract)
        # pd.DataFrame(contract).to_csv(f"{vt_symbol}_contract.csv")

    # res = pd.DataFrame()
    # 持续运行，使用strategy_active来判断是否要退出程序
    while engine.strategy_active:
        # 轮询获取行情
        ticks = engine.get_ticks(vt_symbols)
        logger.info(ticks)

        positions = engine.get_all_positions(use_df=True)
        logger.info(positions)
        # res = pd.concat([res, ticks])
        # res.to_csv(f"./ticks.csv")

        # 等待3秒进入下一轮
        sleep(3)