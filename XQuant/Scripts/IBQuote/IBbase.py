import datetime
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

import threading


class TestApp(EWrapper, EClient):
    def __init__(self, ipaddress, port_id, client_id):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        self.connect(ipaddress, port_id, client_id)

        # thread = threading.Thread(target=self.run)
        # thread.start()
        # setattr(self, "_thread", thread)


def websocket_connect():
    app.run()


if __name__ == "__main__":
    print("Launching IB API application...")
    host = "127.0.0.1"
    port = 7496
    client_id = 1234
    app = TestApp(host, port, client_id)

    print("Successfully launched IB API application...")

    con_thread = threading.Thread(target=websocket_connect, daemon=True)
    con_thread.start()
    time.sleep(1)

    # contract = Contract()
    # contract.symbol = "SPX"
    # contract.secType = "IND"
    # contract.exchange = "CBOE"
    # contract.currency = "USD"

    # contract = Contract()
    # contract.symbol = "GCQ4"
    # contract.secType = "FUT"
    # contract.exchange = "COMEX"
    # contract.currency = "USD"
    # contract.includeExpired = True
    # contract.tradingClass = "GC"
    # contract.lastTradeDateOrContractMonth = "20220127"

    # contract = Contract()
    # contract.localSymbol = "GCU1"
    # contract.secType = "FUT"
    # contract.exchange = "COMEX"
    # contract.currency = "USD"
    # contract.includeExpired = True
    # contract.lastTradeDateOrContractMonth = "20210928"

    # contract.primaryExchange = "CME"
    # contract.lastTradeDateOrContractMonth = "20220127"
    # contract.includeExpired = True

    # contract = Contract()
    # contract.symbol = "FISV"
    # contract.secType = "OPT"
    # contract.exchange = "SMART"
    # contract.currency = "USD"

    # contract = Contract()
    # contract.symbol = "INFY"
    # contract.secType = "FUT"
    # contract.exchange = "INR"
    # contract.currency = "NSE"
    # contract.lastTradeDateOrContractMonth = "20220127"
    # contract.includeExpired = True

    queryTime = (datetime.datetime.today() - datetime.timedelta(days=3 * 365)).strftime(
        "%Y%m%d-%H:%M:%S"
    )
    # data = app.reqHistoricalData(
    #     reqId=923, endDateTime=queryTime, contract=contract, durationStr="1 M", barSizeSetting='1 day', whatToShow="MIDPOINT",
    #     useRTH=1, formatDate=1, keepUpToDate=False, chartOptions=[]
    #     )
    # app.reqHistoricalData(
    #     reqId=0,
    #     contract=contract,
    #     endDateTime="",
    #     durationStr="100 D",
    #     barSizeSetting="30 mins",
    #     whatToShow="TRADES",
    #     useRTH=1,
    #     formatDate=1,
    #     keepUpToDate=False,
    #     chartOptions=[],
    # )

    contract = Contract()
    contract.localSymbol = "GCQ4"
    contract.secType = "FUT"
    contract.exchange = "COMEX"

    res = app.reqContractDetails(277, contract)
    print(res)

    # print(DATA)

    # app.disconnect()
