from vnpy.trader.constant import Direction, Exchange, Offset, OrderType

orders = [
    {
        "symbol": "6A2312",
        "exchange": Exchange.CME,
        "price": 0.0,
        "volume": 1,
        "direction": Direction.LONG,
        "offset": Offset.OPEN,
        "order_type": OrderType.MARKET,
    },
    {
        "symbol": "6A2312",
        "exchange": Exchange.CME,
        "price": 0.0,
        "volume": 1,
        "direction": Direction.LONG,
        "offset": Offset.CLOSETODAY,
        "order_type": OrderType.MARKET,
    },
]
