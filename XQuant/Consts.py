from pathlib import Path
import json

__all__ = ["datatables"]

file_abspath = Path(__file__)
table_record_folder = file_abspath.parent / "TABLES"

assert table_record_folder.is_dir(), "Table record folder does not exist"

table_record_files = table_record_folder.glob("*.json")

datatables = {}

for file in table_record_files:
    with open(file, "r", encoding="utf-8") as fp:
        tmp = json.load(fp)
        if file.stem == "gm_factor":
            another = {}
            for key in tmp:
                another[key + "_gm"] = tmp[key]
            datatables.update(another)
            del another
        else:
            datatables.update(tmp)
del tmp
