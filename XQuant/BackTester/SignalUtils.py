import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def clean(arr: np.ndarray, inplace=False, fill_value=0.0) -> np.ndarray:
    """
    将array中的Inf, NaN转为 fill_value
    - fill_value默认值为0
    - inplace会同时改变传入的arr
    """
    assert arr.dtype == int or arr.dtype == float
    if inplace:
        res = arr
    else:
        res = arr.copy()
    res[~np.isfinite(res)] = fill_value
    return res


def signal_to_weight(signal: pd.DataFrame) -> pd.DataFrame:
    """
    将信号转为weight
    - 输入为NaN, Inf, 0的部分, 输出的weight均为0
    - 直接按照因子值大小进行赋权
        - 线性赋权 [5, 3, 2] => [0.5, 0.3, 0.2]
        -
    """
    weight_arr = signal.values.copy()
    weight_arr = clean(weight_arr)
    weight_arr = np.divide(weight_arr, weight_arr.sum(axis=1)[:, None])
    return pd.DataFrame(
        data=clean(weight_arr), index=signal.index, columns=signal.columns
    )


def categorize_signal_by_quantiles(
    signal: pd.DataFrame, group_nums: int = 5
) -> pd.DataFrame:
    """
    对信号逐行(即对每天的个股因子)进行因子分组, 默认signal越大值越大
    - 输入为NaN,Inf 输出为NaN
    - 一行全为NaN或者相同, 返回一行NaN
    - 由于使用的是sort逻辑, 会有误差
    """
    signal_arr = signal.values.copy()
    flag_all_nan_rows = ((np.abs(signal_arr) < 1e-7) | np.isnan(signal_arr)).all(axis=1)
    signal_arr[flag_all_nan_rows] = np.nan
    ranks = (signal_arr.argsort().argsort() + 1).astype(float)
    # avoid Inf, NaN
    ranks[~np.isfinite(signal_arr)] = np.nan
    # count the number of non-nan signals at any given time
    count = (~np.isnan(ranks)).sum(1)[:, None]

    result_mtx = np.full_like(signal_arr, np.nan)
    # bin_thresholds is a num_bins-1 dimensional vector, denoting the numbers separating the quantiles
    bin_thresholds = count / group_nums * np.arange(0, group_nums + 1)

    for i in range(0, group_nums):
        idx = (ranks > bin_thresholds[:, i].reshape(-1, 1)) & (
            ranks <= bin_thresholds[:, i + 1].reshape(-1, 1)
        )
        result_mtx[idx] = i
    return pd.DataFrame(data=result_mtx, index=signal.index, columns=signal.columns)


def signal_to_top_bottom_weight(signal: pd.DataFrame, quantile: float = 0.1, direction: int = 0):
    """
    对信号逐行(即对每天的个股因子)进行多空对冲的权重计算
    - quantile为top和bottom的比例, 默认为10%
    - 输入为NaN和Inf, 返回权重为0
    - top和bottom内进行等权重划分
    - direction:
        0: for both
        1: top only
        2: bottom only
    """
    signal_arr = signal.values.copy()
    ranks = (signal_arr.argsort().argsort() + 1).astype(float)
    ranks[~np.isfinite(signal)] = np.nan
    count = (~np.isnan(ranks)).sum(1)[:, None]
    weights = 1 / np.floor(count * quantile)
    # Get the floor of the top quantile and ceiling of the bottom quantile
    floor_top_quantile = count * (1 - quantile)
    ceil_bottom_quantile = count * quantile

    # equal size for both top group and bottom group (ceil for top,floor for bottom)
    if direction == 0:
        weight_arr = weights * (
            (ranks > np.ceil(floor_top_quantile)).astype(float)
            - (ranks <= np.floor(ceil_bottom_quantile)).astype(float)
        )
    elif direction == 1:
        weight_arr = weights * (ranks > np.ceil(floor_top_quantile)).astype(float)
    elif direction == 2:
        weight_arr = - weights * (ranks <= np.floor(ceil_bottom_quantile)).astype(float)
    else:
        raise NotImplementedError("direction must be one of [0,1,2]")

    weight_arr[~np.isfinite(weight_arr)] = 0.0
    return pd.DataFrame(data=weight_arr, index=signal.index, columns=signal.columns)


def standardize(signal: pd.DataFrame) -> pd.DataFrame:
    """
    对信号逐行(即对每天的个股因子)进行标准化
    - out_signal = (signal - mean) / std
    - 计算 mean和std时 skip na
    - 输入为NaN的部分, 输出仍为NaN
    """
    signal_arr = signal.values.copy()
    signal_arr = (
        signal_arr - np.mean(signal_arr, axis=1, where=np.isfinite(signal_arr))[:, None]
    ) / np.std(signal_arr, axis=1, ddof=1, where=np.isfinite(signal_arr))[:, None]
    return pd.DataFrame(
        data=clean(signal_arr), index=signal.index, columns=signal.columns
    )


def demean(signal: pd.DataFrame) -> pd.DataFrame:
    """
    对信号逐行(即对每天的个股因子)进行中心化
    - out_signal = signal - mean
    - 计算 mean时 skip na
    - 输入为NaN的部分, 输出仍为NaN
    """
    signal_arr = signal.values.copy()
    signal_arr = signal_arr - np.mean(signal_arr, axis=1, where=np.isfinite(signal_arr))
    return pd.DataFrame(
        data=clean(signal_arr), index=signal.index, columns=signal.columns
    )
