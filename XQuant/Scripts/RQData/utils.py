from pathlib import Path
from datetime import date
import warnings
from loguru import logger

warnings.filterwarnings("ignore", category=UserWarning)

cur_dir = Path(__file__).parent
data_dir = cur_dir / "data_files"
log_dir = cur_dir / "log_files"
begin_date = "20160101"
end_date = date.today().strftime("%Y%m%d")


logger.add(
    log_dir / f"interface_log_{date.today()}.log",
    encoding="utf-8",
    enqueue=True,
    rotation="12:00",
    compression="zip",
    retention="5 days",
)
