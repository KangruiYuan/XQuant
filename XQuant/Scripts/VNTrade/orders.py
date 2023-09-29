from vnpy.trader.constant import Direction, Exchange, Offset, OrderType

long_market_orders = [
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
        "offset": Offset.CLOSE,
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
    {
        "symbol": "6A2312",
        "exchange": Exchange.CME,
        "price": 0.0,
        "volume": 1,
        "direction": Direction.LONG,
        "offset": Offset.CLOSEYESTERDAY,
        "order_type": OrderType.MARKET,
    },
]

short_market_orders = [
    {
        "symbol": "6A2312",
        "exchange": Exchange.CME,
        "price": 0.0,
        "volume": 1,
        "direction": Direction.SHORT,
        "offset": Offset.CLOSETODAY,
        "order_type": OrderType.MARKET,
    },
]
