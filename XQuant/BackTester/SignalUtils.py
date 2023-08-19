import numpy as np
import pandas as pd

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