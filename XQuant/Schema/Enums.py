from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def values(cls):
        return [c.value for c in cls]

    @classmethod
    def keys(cls):
        return [c.name for c in cls]

    @classmethod
    def items(cls):
        return [(c.name, c.value) for c in cls]

class StrBaseEnum(str, BaseEnum):
    pass

class IntBaseEnum(int, BaseEnum):
    pass


class Strategy(StrBaseEnum):
    LONG_ONlY = "long_only"
    GROUP = "group"
    TOP_BOTTOM = "top_bottom"
    WEIGHT = "weight"
    SELF_DEFINED = "self_defined"


class RiskMethod(IntBaseEnum):
    HIST = 0  # 历史模拟
    COV = 1  # 协方差矩阵法
    EXPECTED = 2  # 期望亏空
    MAXDOWN = 4  # 最大回撤
