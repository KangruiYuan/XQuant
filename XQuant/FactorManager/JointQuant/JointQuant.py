from .Basic import Basic
from .joint_quant_envion import *

class JointQuant(Basic):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)