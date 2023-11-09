from pathlib import Path
import json
import pandas as pd

__all__ = ["Config"]

current_directory = Path(__file__).parent
# parent_directory = current_directory.parent
table_record_directory = current_directory / "TABLES"

assert (
    table_record_directory.is_dir()
), f"内置表格记录文件夹不存在，请联系开发人员。当前路径：{table_record_directory}"

datatables = {}

for file in table_record_directory.glob("*.json"):
    with open(file, "r", encoding="utf-8") as fp:
        tmp = json.load(fp)
        if file.stem == "gm_factor":
            another = {}
            for key in tmp:
                another[key + "_gm"] = tmp[key]
            datatables.update(another)
        else:
            datatables.update(tmp)
del another
del tmp

ib_future = pd.read_csv(table_record_directory / "ib_future.csv")
ib_future = ib_future.dropna(how="any", subset=["exchange"])
for _, row in ib_future.iterrows():
    datatables[row["symbol"]] = {
        "exchange": row["exchange"],
        "timezone": row["timezone"],
        "assets": "IB",
        "description": "",
        "date_column": "date",
        "ticker_column": ""
    }


class Config:
    """
    常量类
    """

    database_dir = {
        "info": r"E:\Share\Stk_Data\dataFile",
        "dataYes": r"E:\Share\Stk_Data\dataFile",
        "gm_future": r"E:\Share\Fut_Data",
        "gm_factor": r"E:\Share\Stk_Data\gm",
        "gm_stock": r"E:\Share\Stk_Data\gm",
        "em": r"E:\Share\EM_Data",
        "jq_factor": r"E:\Share\JointQuant_Factor",
        "jq_prepare": r"E:\Share\JointQuant_prepare",
        "IB": r"H:\global data\IB data"
    }

    datasets_name = list(database_dir.keys())
    datatables = datatables

    stock_table: pd.DataFrame = pd.read_hdf(
        "{}/stock_info.h5".format(database_dir["info"])
    )
    stock_list = stock_table["symbol"].tolist()
    stock_num_list = stock_table["sec_id"].unique().tolist()

    futures_list = (
        "AG",
        "AL",
        "AU",
        "A",
        "BB",
        "BU",
        "B",
        "CF",
        "CS",
        "CU",
        "C",
        "FB",
        "FG",
        "HC",
        "IC",
        "IF",
        "IH",
        "I",
        "JD",
        "JM",
        "JR",
        "J",
        "LR",
        "L",
        "MA",
        "M",
        "NI",
        "OI",
        "PB",
        "PM",
        "PP",
        "P",
        "RB",
        "RI",
        "RM",
        "RS",
        "RU",
        "SF",
        "SM",
        "SN",
        "SR",
        "TA",
        "TF",
        "T",
        "V",
        "WH",
        "Y",
        "ZC",
        "ZN",
        "PG",
        "EB",
        "AP",
        "LU",
        "SA",
        "TS",
        "CY",
        "IM",
        "PF",
        "PK",
        "CJ",
        "UR",
        "NR",
        "SS",
        "FU",
        "EG",
        "LH",
        "SP",
        "RR",
        "SC",
        "WR",
        "BC",
    )

    trade_date_table: pd.DataFrame = pd.read_hdf(
        "{}/tradeDate_info.h5".format(database_dir["info"])
    )
    trade_date_list = trade_date_table["tradeDate"].dropna().to_list()

    quarter_begin = ["0101", "0401", "0701", "1001"]
    quarter_end = ["0331", "0630", "0930", "1231"]
