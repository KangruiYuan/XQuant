from .base_envion import *


class Basic(DataReady):
    def __init__(self, begin: TimeType, end: TimeType = None, **kwargs):
        end = end if end else date.today().strftime("%Y%m%d")
        super().__init__(begin, end, **kwargs)

    @cached_property
    def net_working_capital(self):
        ast, lia = self.align_dataframe([self.current_asset, self.current_liability])
        return ast - lia