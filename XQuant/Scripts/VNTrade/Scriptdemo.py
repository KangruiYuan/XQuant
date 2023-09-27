from time import sleep
from vnpy_scripttrader import ScriptEngine
from vnpy_scripttrader import init_cli_trading
from vnpy_da import DaGateway


def run(engine: ScriptEngine):
    """"""
    vt_symbols = ["L-ZS3M.LME", "PB3M.LME"]

    # 订阅行情
    engine.subscribe(vt_symbols)

    # 获取合约信息
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f"合约信息，{contract}"
        engine.write_log(msg)

    # 持续运行，使用strategy_active来判断是否要退出程序
    while engine.strategy_active:
        # 轮询获取行情
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f"最新行情, {tick}"
            engine.write_log(msg)

            order = engine.get_order(vt_symbol)
            msg = f"最新order, {order}"
            engine.write_log(msg)

            order = engine.get_trades(vt_symbol)
            msg = f"最新trade, {order}"
            engine.write_log(msg)

        # 等待3秒进入下一轮
        sleep(3)

setting = {
        "用户名": "AF20230451",
        "密码": "888888",
        "经纪商代码": "DAHK",
        "交易服务器": "222.73.119.230:7003",
        "行情服务器": "222.73.105.170:9430",
        "授权码": "porl99bbo/jrfib5xxgagza5giggzr/u",
    }

engine = init_cli_trading([DaGateway])
engine.connect_gateway(setting, gateway_name="DA")

sleep(35)

run(engine)