from vnpy_scripttrader import init_cli_trading
from vnpy_da import DaGateway
from vn_schema import setting
from time import sleep
from vnpy.trader.object import OrderRequest
from orders import orders
from tqdm import tqdm
from copy import deepcopy

da_engine = init_cli_trading([DaGateway])
da_engine.connect_gateway(setting, gateway_name="DA")
# da_engine.write_log("成功连接直达，正在初始化")

waiting_time = 3
with tqdm(range(waiting_time)) as pbar:
    pbar.set_description_str("正在初始化, 阻塞程序")
    for _ in pbar:
        sleep(1)


def to_standard_order(order: dict):
    res = deepcopy(order)
    res["vt_symbol"] = f"{order['symbol']}.{order['exchange'].value}"
    del res["symbol"]
    del res["exchange"]
    return res


for order in orders:
    standard_order = to_standard_order(order)
    print(f"order: {standard_order}")
    order_id = da_engine.send_order(**standard_order)
    sleep(1)
    print(f"order id: {order_id}")
