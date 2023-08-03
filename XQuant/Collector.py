
from .Utils import Config, TradeDate, TimeType, Formatter
from typing import Union, Literal
from .Consts import datatables
from datetime import datetime


def get_data(
        name: str,
        begin: TimeType = None,
        end: TimeType = None,
        fields: Union[str, list] = None,
        ticker: Union[str, int, list] = None,
        engine: Literal["py", "sql"] = "py",
        **kwargs
):
    if name not in datatables:
        raise KeyError("{} is not ready for use!".format(name))
    if end is None:
        end = datetime.today().strftime("%Y%m%d")
    end = TradeDate.format_date(end)

    if begin:
        begin = TradeDate.format_date(begin)

    if isinstance(fields, str):
        fields = [fields]

    if isinstance(ticker, (int, str)):
        ticker = [ticker]

    assets = datatables[name]["assets"]

    if engine == "py":
        if assets in ["dataYes"]:
            pass
        elif assets in []:
            pass
    elif engine == "sql":
        pass

    load_begin, load_end = TradeDate.extend_date_span(begin, end, "Y")


