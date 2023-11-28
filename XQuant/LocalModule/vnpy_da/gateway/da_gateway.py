import wmi
import requests
from datetime import datetime
from copy import copy
from collections import defaultdict
from typing import Dict, List, Tuple
from csv import DictReader
from io import StringIO
from requests.models import Response

from vnpy.event import EventEngine
from vnpy.trader.constant import (
    Direction,
    Offset,
    Exchange,
    OrderType,
    Product,
    Status,
    OptionType
)
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    OrderRequest,
    CancelRequest,
    HistoryRequest,
    BarData,
    SubscribeRequest,
)
from vnpy.trader.utility import ZoneInfo

from ..api import (
    MarketApi,
    FutureApi,
    DAF_SUB_Append,
    DAF_TYPE_Future
)


# 委托状态映射
STATUS_DA2VT: Dict[str, Status] = {
    "1": Status.SUBMITTING,
    "2": Status.NOTTRADED,
    "3": Status.PARTTRADED,
    "4": Status.ALLTRADED,
    "5": Status.CANCELLED,
    "6": Status.CANCELLED,
    "7": Status.REJECTED,
    "8": Status.SUBMITTING,
    "9": Status.SUBMITTING,
    "A": Status.SUBMITTING,
}

# 多空方向映射
DIRECTION_VT2DA: Dict[Direction, str] = {
    Direction.LONG: "1",
    Direction.SHORT: "2"
}
DIRECTION_DA2VT: Dict[str, Direction] = {v: k for k, v in DIRECTION_VT2DA.items()}


# 委托类型映射
ORDERTYPE_VT2DA: Dict[OrderType, str] = {
    OrderType.LIMIT: "1",
    OrderType.MARKET: "2"
}
ORDERTYPE_DA2VT: Dict[str, OrderType] = {v: k for k, v in ORDERTYPE_VT2DA.items()}

# 开平方向映射
OFFSET_VT2DA: Dict[Offset, str] = {
    Offset.OPEN: "1",
    Offset.CLOSE: "2",
    Offset.CLOSETODAY: "3",
    Offset.CLOSEYESTERDAY: "4",
}
OFFSET_DA2VT: Dict[str, Offset] = {v: k for k, v in OFFSET_VT2DA.items()}

# 交易所映射
EXCHANGE_DA2VT: Dict[str, Exchange] = {
    "CME": Exchange.CME,
    "CME_CBT": Exchange.CBOT,
    "LME": Exchange.LME,
    "SGXQ": Exchange.SGX,
    "HKEX": Exchange.HKFE,
    "APEX": Exchange.APEX,
    "CFFEX": Exchange.CFFEX,
    "SHFE": Exchange.SHFE,
    "DCE": Exchange.DCE,
    "CZCE": Exchange.CZCE,
    "DL-DCE": Exchange.DL_DCE,
}
EXCHANGE_VT2DA: Dict[Exchange, str] = {v: k for k, v in EXCHANGE_DA2VT.items()}

# 产品类型映射
PRODUCT_DA2VT: Dict[str, Product] = {
    "F": Product.FUTURES,
    "O": Product.OPTION,
}

# 期权类型映射
OPTIONTYPE_DA2VT: Dict[str, OptionType] = {
    "R": OptionType.CALL,
    "F": OptionType.PUT
}

# 其他常量
CHINA_TZ = ZoneInfo("Asia/Shanghai")       # 中国时区

# 全局缓存字典
symbol_name_map: Dict[str, str] = {}
symbol_currency_map: Dict[str, str] = {}
currency_account_map: Dict[str, str] = {}
account_currency_map: Dict[str, str] = {}


class DaGateway(BaseGateway):
    """
    VeighNa用于对接直达期货的接口。
    """

    default_name: str = "DA"

    default_setting: Dict[str, str] = {
        "用户名": "",
        "密码": "",
        "交易服务器": "",
        "行情服务器": "",
        "授权码": ""
    }

    exchanges: List[str] = list(EXCHANGE_DA2VT.values())

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        """构造函数"""
        super().__init__(event_engine, gateway_name)

        self.future_api: "DaFutureApi" = DaFutureApi(self)
        self.market_api: "DaMarketApi" = DaMarketApi(self)

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        userid: str = setting["用户名"]
        password: str = setting["密码"]
        future_address: str = setting["交易服务器"]
        market_address: str = setting["行情服务器"]
        auth_code: str = setting["授权码"]

        if not future_address.startswith("tcp://"):
            future_address: str = "tcp://" + future_address
        if not market_address.startswith("tcp://"):
            market_address: str = "tcp://" + market_address

        self.future_api.connect(future_address, userid, password, auth_code)
        self.market_api.connect(market_address, userid, password, auth_code)

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        self.market_api.subscribe(req)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        return self.future_api.send_order(req)

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        self.future_api.cancel_order(req)

    def query_account(self) -> None:
        """查询资金"""
        pass

    def query_position(self) -> None:
        """查询持仓"""
        pass

    def query_history(self, req: HistoryRequest) -> List[BarData]:
        """查询历史数据"""
        path: str = "http://222.73.120.40:8609/api/HistoryQuote"

        params: dict = {
            "type": "M1",
            "exchangeNo": EXCHANGE_VT2DA[req.exchange],
            "symbol": req.symbol,
            "startTime": req.start.strftime("%Y-%m-%d"),
            "count": ""
        }

        if req.end:
            params["endTime"] = req.end.strftime("%Y-%m-%d")

        headers: dict = {"Accept-Encoding": "gzip"}

        r: Response = requests.get(path, headers=headers, params=params)

        bars: List[BarData] = []
        reader: List[dict] = DictReader(StringIO(r.json()))
        for d in reader:
            dt: datetime = datetime.strptime(d["时间"], "%Y-%m-%d %H:%M")
            dt: datetime = dt.replace(tzinfo=CHINA_TZ)

            bar: BarData = BarData(
                symbol=req.symbol,
                exchange=req.exchange,
                interval=req.interval,
                datetime=dt,
                open_price=float(d["开盘价"]),
                high_price=float(d["最高价"]),
                low_price=float(d["最低价"]),
                close_price=float(d["收盘价"]),
                volume=int(d["成交量"]),
                gateway_name=self.gateway_name
            )
            bars.append(bar)

        return bars

    def close(self) -> None:
        """关闭接口"""
        self.future_api.close()
        self.market_api.close()

    def write_error(self, msg: str, error: dict) -> None:
        """输出错误信息日志"""
        error_id: str = error["ErrorID"]
        error_msg: str = error["ErrorMsg"]
        msg: str = f"{msg}，代码：{error_id}，信息：{error_msg}"
        self.write_log(msg)


class DaMarketApi(MarketApi):
    """直达行情API"""

    def __init__(self, gateway: DaGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: DaGateway = gateway
        self.gateway_name: str = gateway.gateway_name

        self.reqid: int = 0

        self.connect_status: bool = False
        self.login_status: bool = False
        self.subscribed: Dict[str, SubscribeRequest] = {}
        self.mac_address: str = get_mac_address()

        self.userid: str = ""
        self.password: str = ""
        self.auth_code: str = ""

    def onFrontConnected(self) -> None:
        """服务器连接成功回报"""
        self.gateway.write_log("行情服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        self.login_status: bool = False
        self.gateway.write_log(f"行情服务器连接断开，原因{reason}")

    def onRspUserLogin(self, error: dict, reqid: int, last: bool) -> None:
        """用户登录请求回报"""
        if not error["ErrorID"]:
            self.login_status: bool = True
            self.gateway.write_log("行情服务器登录成功")

            for req in self.subscribed.values():
                self.subscribe(req)
        else:
            self.gateway.write_error("行情服务器登录失败", error)

    def onRspMarketData(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """行情数据更新回报"""
        symbol: str = data["TreatyCode"]
        exchange: Exchange = EXCHANGE_DA2VT.get(data["ExchangeCode"], None)
        if not exchange:
            return

        dt: datetime = datetime.strptime(data['Time'], "%Y-%m-%d %H:%M:%S")
        dt: datetime = dt.replace(tzinfo=CHINA_TZ)

        tick: TickData = TickData(
            symbol=symbol,
            exchange=exchange,
            datetime=dt,
            volume=to_int(data["FilledNum"]),
            open_interest=to_int(data["HoldNum"]),
            limit_up=to_float(data["LimitUpPrice"]),
            limit_down=to_float(data["LimitDownPrice"]),
            last_price=to_float(data["CurrPrice"]),
            open_price=to_float(data["Open"]),
            high_price=to_float(data["High"]),
            low_price=to_float(data["Low"]),
            pre_close=to_float(data["PreSettlementPrice"]),
            bid_price_1=to_float(data["BuyPrice"]),
            bid_price_2=to_float(data["BuyPrice2"]),
            bid_price_3=to_float(data["BuyPrice3"]),
            bid_price_4=to_float(data["BuyPrice4"]),
            bid_price_5=to_float(data["BuyPrice5"]),
            ask_price_1=to_float(data["SalePrice"]),
            ask_price_2=to_float(data["SalePrice2"]),
            ask_price_3=to_float(data["SalePrice3"]),
            ask_price_4=to_float(data["SalePrice4"]),
            ask_price_5=to_float(data["SalePrice5"]),
            bid_volume_1=to_int(data["BuyNumber"]),
            bid_volume_2=to_int(data["BuyNumber2"]),
            bid_volume_3=to_int(data["BuyNumber3"]),
            bid_volume_4=to_int(data["BuyNumber4"]),
            bid_volume_5=to_int(data["BuyNumber5"]),
            ask_volume_1=to_int(data["SaleNumber"]),
            ask_volume_2=to_int(data["SaleNumber2"]),
            ask_volume_3=to_int(data["SaleNumber3"]),
            ask_volume_4=to_int(data["SaleNumber4"]),
            ask_volume_5=to_int(data["SaleNumber5"]),
            gateway_name=self.gateway_name
        )
        tick.name = symbol_name_map[tick.vt_symbol]
        self.gateway.on_tick(tick)

    def connect(self, address: str, userid: str, password: str, auth_code: str) -> None:
        """连接服务器"""
        self.userid = userid
        self.password = password
        self.auth_code = auth_code

        # 连接
        if not self.connect_status:
            self.createMarketApi(False, "market_log.txt")

            self.registerNameServer(address)
            self.init()

            self.connect_status = True
        # 登录
        elif not self.login_status:
            self.login()

    def login(self) -> None:
        """用户登录"""
        req: dict = {
            "UserId": self.userid,
            "UserPwd": self.password,
            "AuthorCode": self.auth_code,
            "MacAddress": self.mac_address,
            "ComputerName": "Dev Server",
            "SoftwareName": "VeighNa",
            "SoftwareVersion": "3.7",
        }

        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        if self.login_status:
            da_exchange: Exchange = EXCHANGE_VT2DA.get(req.exchange, "")
            if not da_exchange:
                self.gateway.write_log(f"不支持的交易所{req.exchange.value}")
                return

            da_code: str = f"{da_exchange},{req.symbol}"

            da_req: dict = {
                "MarketType": DAF_TYPE_Future,
                "SubscMode": DAF_SUB_Append,
                "MarketCount": 1,
                "MarketTrcode": da_code,
            }
            self.reqid += 1
            self.reqMarketData(da_req, self.reqid)

        self.subscribed[req.symbol] = req

    def close(self) -> None:
        """关闭连接"""
        pass


class DaFutureApi(FutureApi):
    """直达期货交易API"""

    def __init__(self, gateway: DaGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: DaGateway = gateway
        self.gateway_name: str = gateway.gateway_name

        self.reqid: int = 0
        self.local_no: int = int(datetime.now().strftime("%Y%m%d") + "000000")

        self.connect_status: bool = False
        self.login_status: bool = False
        self.auth_staus: bool = False
        self.login_failed: bool = False

        self.userid: str = ""
        self.password: str = ""
        self.auth_code: str = ""
        self.mac_address: str = get_mac_address()

        self.exchange_page = defaultdict(int)

        self.orders: Dict[str, OrderData] = {}
        self.order_info: Dict[str, Tuple] = {}

    def onFrontConnected(self) -> None:
        """服务器连接成功回报"""
        self.gateway.write_log("交易服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        self.login_status: bool = False
        self.gateway.write_log(f"交易服务器连接断开，原因{reason}")

    def onRspUserLogin(self, error: dict, reqid: int, last: bool) -> None:
        """用户登录请求回报"""
        if not error["ErrorID"]:
            self.login_status: bool = True
            self.gateway.write_log("交易服务器登录成功")

            # 查询可交易合约
            for exchange in EXCHANGE_DA2VT.values():
                self.query_contract(exchange)

            # 查询账户信息
            self.query_account()
            self.query_position()
            self.query_order()
            self.query_trade()
        else:
            self.login_failed: bool = True
            self.gateway.write_error("交易服务器登录失败", error)

    def onRspNeedVerify(self, firstLogin: bool, hasSetQA: bool) -> None:
        """请求需要验证回报"""
        print("on rsp need verify", firstLogin, hasSetQA)

    def onRspOrderInsert(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """委托下单回报"""
        if not data["OrderNo"]:
            return

        errorid: str = error["ErrorID"]
        orderid: str = data["LocalNo"]
        order: OrderData = self.orders[orderid]

        if errorid:
            order.status = Status.REJECTED
            self.gateway.write_error("交易委托失败", error)
        else:
            timestamp: str = f"{data['OrderDate']} {data['OrderTime']}"
            dt: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            order.datetime = dt.replace(tzinfo=CHINA_TZ)

            self.order_info[order.orderid] = (data["OrderNo"], data["SystemNo"])

        self.gateway.on_order(copy(order))

    def onRspOrderCancel(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """委托撤单回报"""
        errorid: str = error["ErrorID"]
        if errorid:
            self.gateway.write_error("交易撤单失败", error)

    def onRspSettlementInfoConfirm(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """结算信息确认回报"""
        self.gateway.write_log("结算信息确认成功")

        self.reqid += 1
        self.reqQryInstrument({}, self.reqid)

    def onRspQryInstrument(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """机构查询回报"""
        if error["ErrorID"]:
            return

        product: Product = PRODUCT_DA2VT.get(data["CommodityType"], None)

        if product:
            contract: ContractData = ContractData(
                symbol=data["CommodityCode"],
                exchange=EXCHANGE_DA2VT[data["ExchangeNo"]],
                name=data["ContractFName"],
                product=product,
                size=data["ProductDot"] / data["UpperTick"],
                pricetick=data["UpperTick"],
                history_data=True,
                gateway_name=self.gateway_name
            )

            if product == Product.OPTION:
                contract.option_type = OPTIONTYPE_DA2VT[data["OptionType"]]
                contract.option_strike = to_float(data["OptionStrikePrice"])
                contract.option_expiry = datetime.strptime(data["LastTradeDay"], "%Y%m%d")

            symbol_name_map[contract.vt_symbol] = contract.name
            symbol_currency_map[contract.symbol] = data["CommodityFCurrencyNo"]

            self.gateway.on_contract(contract)

        if last:
            current_page: int = self.exchange_page[contract.exchange] + 1
            self.gateway.write_log(f"{contract.exchange.value}第{current_page}页合约信息查询成功")

            self.exchange_page[contract.exchange] += 1
            self.query_contract(contract.exchange, self.exchange_page[contract.exchange])

    def onRspQryOrder(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """委托查询回报"""
        if data["TreatyCode"]:
            timestamp: str = f"{data['OrderDate']} {data['OrderTime']}"
            dt: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            dt: datetime = dt.replace(tzinfo=CHINA_TZ)

            order: OrderData = OrderData(
                symbol=data["TreatyCode"],
                exchange=EXCHANGE_DA2VT[data["ExchangeCode"]],
                orderid=data["LocalNo"],
                type=ORDERTYPE_DA2VT[data["PriceType"]],
                direction=DIRECTION_DA2VT[data["BuySale"]],
                offset=OFFSET_DA2VT[data["AddReduce"]],
                price=float(data["OrderPrice"]),
                volume=int(data["OrderNumber"]),
                traded=int(data["FilledNumber"]),
                status=STATUS_DA2VT[data["OrderState"]],
                datetime=dt,
                gateway_name=self.gateway_name
            )

            self.local_no: int = max(self.local_no, int(data["LocalNo"]))
            self.orders[order.orderid] = order
            self.order_info[order.orderid] = (data["OrderNo"], data["SystemNo"])

            self.gateway.on_order(copy(order))

        if last:
            self.gateway.write_log("委托信息查询成功")

    def onRspQryTrade(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """成交查询回报"""
        if data["TreatyCode"]:
            self.update_trade(data)

        if last:
            self.gateway.write_log("成交信息查询成功")

    def update_trade(self, data: dict) -> None:
        """成交更新推送"""
        timestamp: str = f"{data['FilledDate']} {data['FilledTime']}"
        dt: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        dt: datetime = dt.replace(tzinfo=CHINA_TZ)

        trade: TradeData = TradeData(
            symbol=data["TreatyCode"],
            exchange=EXCHANGE_DA2VT[data["ExchangeCode"]],
            orderid=data["LocalNo"],
            tradeid=data["FilledNo"],
            direction=DIRECTION_DA2VT[data["BuySale"]],
            offset=OFFSET_DA2VT[data["AddReduce"]],
            price=float(data["FilledPrice"]),
            volume=int(data["FilledNumber"]),
            datetime=dt,
            gateway_name=self.gateway_name
        )
        self.gateway.on_trade(trade)

    def onRspQryCapital(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """资金查询回报"""
        account: AccountData = AccountData(
            accountid=data["CurrencyNo"],
            balance=float(data["TodayBalance"]),
            frozen=float(data["FreezenMoney"]),
            gateway_name=self.gateway_name
        )

        currency_account_map[data["CurrencyNo"]] = data["AccountNo"]
        account_currency_map[data["AccountNo"]] = data["CurrencyNo"]
        self.gateway.on_account(account)

        if last:
            self.gateway.write_log("资金信息查询成功")

    def onRspQryTotalPosition(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """持仓查询回报"""
        if data["TreatyCode"]:
            long_position: PositionData = PositionData(
                symbol=data["TreatyCode"],
                exchange=EXCHANGE_DA2VT[data["ExchangeNo"]],
                direction=Direction.LONG,
                volume=data["BuyHoldNumber"],
                price=data["BuyHoldOpenPrice"],
                gateway_name=self.gateway_name
            )
            self.gateway.on_position(long_position)

            short_position: PositionData = PositionData(
                symbol=data["TreatyCode"],
                exchange=EXCHANGE_DA2VT[data["ExchangeNo"]],
                direction=Direction.SHORT,
                volume=data["SaleHoldNumber"],
                price=data["SaleHoldOpenPrice"],
                gateway_name=self.gateway_name
            )
            self.gateway.on_position(short_position)

        if last:
            self.gateway.write_log("持仓信息查询成功")

    def onRtnOrder(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """委托更新推送"""
        orderid: str = data["LocalOrderNo"]
        self.local_no: int = max(self.local_no, int(orderid))

        order: OrderData = self.orders.get(orderid, None)
        if not order:
            return

        # 过滤重复委托
        if not order.is_active():
            return

        order.traded = data["FilledNumber"]

        if data["IsCanceled"] == "1":
            order.status = Status.CANCELLED
        elif order.traded == order.volume:
            order.status = Status.ALLTRADED
        elif order.traded > 0:
            order.status = Status.PARTTRADED
        else:
            order.status = Status.NOTTRADED

        self.gateway.on_order(copy(order))

    def onRtnTrade(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """成交更新推送"""
        self.update_trade(data)

    def onRtnCapital(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """资金更新推送"""
        currency: str = account_currency_map[data["AccountNo"]]

        account: AccountData = AccountData(
            accountid=currency,
            balance=data["TodayTotal"],
            frozen=data["FrozenDeposit"],
            gateway_name=self.gateway_name
        )

        self.gateway.on_account(account)

    def onRtnPosition(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """持仓更新推送"""
        long_position: PositionData = PositionData(
            symbol=data["TreatyCode"],
            exchange=EXCHANGE_DA2VT[data["ExchangeNo"]],
            direction=Direction.LONG,
            volume=data["BuyHoldNumber"],
            price=data["BuyHoldOpenPrice"],
            gateway_name=self.gateway_name
        )
        self.gateway.on_position(long_position)

        short_position: PositionData = PositionData(
            symbol=data["TreatyCode"],
            exchange=EXCHANGE_DA2VT[data["ExchangeNo"]],
            direction=Direction.SHORT,
            volume=data["SaleHoldNumber"],
            price=data["SaleHoldOpenPrice"],
            gateway_name=self.gateway_name
        )
        self.gateway.on_position(short_position)

    def connect(
        self,
        address: str,
        userid: str,
        password: str,
        auth_code: str
    ) -> None:
        """连接服务器"""
        self.userid = userid
        self.password = password
        self.auth_code = auth_code

        if not self.connect_status:
            self.createFutureApi(False, "future_log.txt")

            self.registerNameServer(address)
            self.init()

            self.connect_status = True
        else:
            self.login()

    def authenticate(self) -> None:
        """发起授权验证"""
        req: dict = {
            "UserID": self.userid,
            "BrokerID": self.brokerid,
            "AuthCode": self.auth_code,
            "AppID": self.appid
        }

        if self.product_info:
            req["UserProductInfo"] = self.product_info

        self.reqid += 1
        self.reqAuthenticate(req, self.reqid)

    def login(self) -> None:
        """用户登录"""
        req: dict = {
            "UserId": self.userid,
            "UserPwd": self.password,
            "AuthorCode": self.auth_code,
            "MacAddress": self.mac_address,
            "ComputerName": "Dev Server",
            "SoftwareName": "VeighNa",
            "SoftwareVersion": "3.7",
        }

        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        self.local_no += 1

        if req.exchange != Exchange.DL_DCE:
            currency: str = symbol_currency_map[req.symbol]
            account_no: str = currency_account_map[currency]
        else:
            currency = "NY-USD"
            account_no = currency_account_map[currency]
        # print(currency, account_no)
        print("req", req)

        da_req: dict = {
            "UserId": self.userid,
            "AccountNo": account_no,
            "LocalNo": str(self.local_no),
            "TradePwd": self.password,
            "ExchangeCode": EXCHANGE_VT2DA[req.exchange],
            "TreatyCode": req.symbol,
            "BuySale": DIRECTION_VT2DA[req.direction],
            "OrderPrice": str(req.price),
            "OrderNumber": str(int(req.volume)),
            "PriceType": ORDERTYPE_VT2DA[req.type],
            "ValidDate": "1"
        }

        print(da_req)
        self.reqid += 1
        self.reqOrderInsert(da_req, self.reqid)

        order: OrderData = req.create_order_data(str(self.local_no), self.gateway_name)

        self.orders[order.orderid] = order
        self.gateway.on_order(order)

        return order.vt_orderid

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        order: OrderData = self.orders[req.orderid]

        if order.orderid not in self.order_info:
            msg = f"撤单失败，尚未收到服务端返回的委托信息{order.orderid}"
            self.gateway.write_log(msg)
            return

        currency: str = symbol_currency_map[req.symbol]
        account_no: str = currency_account_map[currency]
        order_no, system_no = self.order_info[order.orderid]

        da_req: dict = {
            "UserId": self.userid,
            "LocalNo": req.orderid,
            "AccountNo": account_no,
            "TradePwd": self.password,
            "ExchangeCode": EXCHANGE_VT2DA[req.exchange],
            "TreatyCode": req.symbol,
            "BuySale": DIRECTION_VT2DA[order.direction],
            "OrderNo": order_no,
            "SystemNo": system_no
        }

        self.reqid += 1
        self.reqOrderCancel(da_req, self.reqid)

    def query_account(self) -> None:
        """查询资金"""
        self.reqid += 1
        self.reqQryCapital({}, self.reqid)

    def query_order(self) -> None:
        """查询委托"""
        self.reqid += 1
        self.reqQryOrder({}, self.reqid)

    def query_trade(self) -> None:
        """查询成交"""
        da_req: dict = {"UserId": self.userid}

        self.reqid += 1
        self.reqQryTrade(da_req, self.reqid)

    def query_position(self) -> None:
        """查询持仓"""
        da_req: dict = {"AccountNo": self.userid}

        self.reqid += 1
        self.reqQryTotalPosition(da_req, self.reqid)

    def query_contract(self, exchange: Exchange, page=0) -> None:
        """查询合约"""
        da_exchange: str = EXCHANGE_VT2DA[exchange]

        req: dict = {
            "PageIndex": page * 1000,
            "ExchangeNo": da_exchange
        }

        self.reqid += 1
        self.reqQryInstrument(req, self.reqid)

    def close(self) -> None:
        """断开连接"""
        pass


def get_network_interface() -> str:
    """获取网络接口"""
    c = wmi.WMI()
    interfaces = c.Win32_NetworkAdapterConfiguration(IPEnabled=1)
    if not interfaces:
        return None

    # 使用默认ip接入
    for interface in interfaces:
        if interface.DefaultIPGateway:
            return interface

    # 否则使用最新的
    return interface


def get_mac_address() -> str:
    """获取mac地址"""
    interface: str = get_network_interface()
    if not interface:
        return ""

    return interface.MACAddress


def to_int(data: str) -> int:
    """字符串转换成整数"""
    if not data:
        return 0
    else:
        return int(data)


def to_float(data: str) -> float:
    """字符串转换成浮点数"""
    if not data:
        return 0.0
    else:
        return float(data)
