from pydantic import BaseModel
from .enums import Exchange, Direction, Offset, OrderType


# class Order(BaseModel):
#     symbol: str
#     exchange: Exchange
#     price: float
#     volume: float
#     direction: Direction
#     offset: Offset
#     order_type: OrderType


class User(BaseModel):
    pass
