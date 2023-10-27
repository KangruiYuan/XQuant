# from rqalpha_plus.apis import *
from rqalpha.apis import *
from rqalpha_plus import run_func

from XQuant import Formatter, categorize_signal_by_quantiles, signal_to_weight
from utils import *

factor = pd.read_csv(data_dir / "EnhancingDividend.csv", index_col=0, parse_dates=True)
# 半年换仓
factor = factor.ffill().resample("6M").last()
Formatter.transform_index(factor)
# 去除无效行列
factor = factor.replace({0: np.nan}).dropna(axis=0, how="all").dropna(axis=1, how="all")


config = {
    "base": {
        "start_date": factor.index.min().strftime("%Y-%m-%d"),  # 回测开始日期
        "end_date": factor.index.max().strftime("%Y-%m-%d"),  # 回测结束日期
        "frequency": "1d",  # 回测频率, 分钟: '1m'
        "accounts": {"stock": int(1e8)},  # 股票初始资金  期货："future":100000
        "data_bundle_path": "H:/rqsdk_data/bundle",
    },
    "extra": {
        "log_level": "info",
        "log_file": "backtest.log",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        },
        "sys_analyser": {
            "enabled": True,
            "benchmark": "000300.XSHG",  # 基准合约
            "plot": True,
        },
        "sys_simulation": {
            "matching_type": "current_bar",
        },
    },
}


def init(context):
    context.group_nums = 5

    # 目标分组
    context.target = 1

    # 转换信号
    signals = categorize_signal_by_quantiles(factor, group_nums=context.group_nums)
    signals_weights = signal_to_weight((signals == context.target).astype(int))

    order_book_id = signals_weights.columns.tolist()
    logger.info(f"最终股池大小：{len(order_book_id)}")

    context.order_book_id = order_book_id
    context.signals = signals_weights
    context.buy_and_sell = False
    context.signal_date = signals_weights.index.tolist()
    context.ind = 0
    # 缩放比例
    context.scale = 1.0

    context.orders = []
    # update_universe(context.order_book_id)


def handle_bar(context, bar_dict):
    now_time = context.now

    if now_time < context.signal_date[context.ind]:
        if context.orders:
            temp = []
            for stock, percent in context.orders:
                stock_bar = bar_dict[stock]
                if stock_bar.close == stock_bar.limit_up or stock_bar.close == stock_bar.limit_down:
                    temp.append((stock, percent))
                    continue
                order_target_percent(stock, percent * context.scale)
            context.orders = temp
    else:
        series = context.signals.iloc[context.ind, :]
        for stock, percent in series.items():

            stock_bar = bar_dict[stock]
            # print(stock_bar)
            # 无需进行买卖操作
            if percent == 0 and get_position(stock).quantity == 0:
                continue
            # 停牌跳过
            if bar_dict[stock].suspended:
                continue
            # 涨跌停下一日再交易
            if stock_bar.close == stock_bar.limit_up or stock_bar.close == stock_bar.limit_down:
                context.orders.append((stock, percent))
                continue
            order_target_percent(stock, percent * context.scale)
        context.ind += 1


results = run_func(init=init, config=config, handle_bar=handle_bar)
