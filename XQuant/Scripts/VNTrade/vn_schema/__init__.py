import json
from pathlib import Path

from .enums import *
from .structs import *

with open(Path(__file__).parent / "setting.json", encoding="utf-8") as fp:
    setting = json.load(fp)
