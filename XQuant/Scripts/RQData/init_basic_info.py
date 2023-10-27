import pandas as pd
import rqdatac
import yaml

from utils import *

rqdatac.init(use_pool=True)


def hum_convert(value: int):
    """
    :param value: bytes
    :return:
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return value, units[i]
        value /= size


def rest_bytes():
    data_quota = rqdatac.user.get_quota()
    value, unit = hum_convert(data_quota["bytes_limit"] - data_quota["bytes_used"])
    logger.info(f"剩余流量：{value:.2f} {unit}")
    return value


rest_bytes()

stocks = data_dir / "stocks.csv"
if stocks.exists():
    cn_CS = pd.read_csv(stocks)
    order_book_id = cn_CS.get("order_book_id").values.tolist()
    logger.info(f"从本地加载股票信息，共{len(cn_CS)}项")
else:
    cn_CS = rqdatac.all_instruments(type="CS", market="cn", date=None)
    cn_CS.to_csv(stocks, index=False)
    order_book_id = cn_CS.get("order_book_id").values.tolist()
    logger.info(f"从网络加载股票信息，共{len(cn_CS)}项")

factors = data_dir / "factors.yaml"
if factors.exists():
    factor_names = yaml.load(factors.open("r"), yaml.BaseLoader)
    logger.info(f"从本地加载因子信息，共{len(factor_names)}项")
else:
    factor_names = rqdatac.get_all_factor_names()
    with factors.open("w") as fp:
        yaml.dump(factor_names, fp)
    logger.info(f"从网络加载因子信息，共{len(factor_names)}项")


def download_factor(file: Path):
    if file.exists():
        factor = pd.read_csv(file)
        value, unit = hum_convert(factor.memory_usage().sum())
        logger.info(f"从本地加载{file.stem}成功，大小为{value:.2f} {unit}")
    else:
        factor = rqdatac.get_factor(
            order_book_ids=order_book_id,
            factor=file.stem,
            start_date=begin_date,
            end_date=end_date,
        )
        value, unit = hum_convert(factor.memory_usage().sum())
        logger.info(f"从网络下载{file.stem}成功，大小为{value:.2f} {unit}")
        factor.reset_index()
        factor.to_csv(file)
    return factor


# EPS_TTM
epsTTM_file = data_dir / "epsTTM.csv"
epsTTM = download_factor(epsTTM_file)

# negMarketValue
market_cap_2_file = data_dir / "market_cap_2.csv"
market_cap_2 = download_factor(market_cap_2_file)

# turnover
price_file = data_dir / "price.csv"
if price_file.exists():
    price = pd.read_csv(price_file, parse_dates=["date"])
    value, unit = hum_convert(price.memory_usage().sum())
    logger.info(f"从本地加载{price_file.stem}成功，大小为{value:.2f} {unit}")
else:
    price = rqdatac.get_price(
        order_book_ids=order_book_id,
        start_date=begin_date,
        end_date=end_date,
        fields=["close", "total_turnover"],
    )
    value, unit = hum_convert(price.memory_usage().sum())
    logger.info(f"从网络下载price成功，大小为{value:.2f} {unit}")
    price.reset_index()
    price.to_csv(price_file)


dividend_file = data_dir / "dividend.csv"
if dividend_file.exists():
    dividend = pd.read_csv(dividend_file)
    value, unit = hum_convert(dividend.memory_usage().sum())
    logger.info(f"从本地加载dividend成功，大小为{value:.2f} {unit}")
else:
    dividend = rqdatac.get_dividend(
        order_book_ids=order_book_id,
        start_date=begin_date,
        end_date=end_date,
        market="cn",
    )
    value, unit = hum_convert(dividend.memory_usage().sum())
    logger.info(f"从网络下载dividend成功，大小为{value:.2f} {unit}")
    dividend.reset_index()
    dividend.to_csv(dividend_file)


rest_bytes()
