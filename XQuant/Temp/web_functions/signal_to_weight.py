import pandas as pd
import numpy as np

def clean(arr: np.ndarray, inplace=False, fill_value=0.0) -> np.ndarray:
    assert arr.dtype == int or arr.dtype == float
    if inplace:
        res = arr
    else:
        res = arr.copy()
    res[~np.isfinite(res)] = fill_value
    return res


def signal_to_weight(signal: pd.DataFrame) -> pd.DataFrame:
    weight_arr = signal.values.copy()
    weight_arr = clean(weight_arr)
    weight_arr = np.divide(weight_arr, weight_arr.sum(axis=1)[:, None])
    return pd.DataFrame(
        data=clean(weight_arr), index=signal.index, columns=signal.columns
    )