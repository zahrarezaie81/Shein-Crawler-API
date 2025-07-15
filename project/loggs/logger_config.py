import logging
import os
import sys
from logging.handlers import RotatingFileHandler

log_dir = os.path.join(os.path.dirname(__file__), "loggs_of_project")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")


logger = logging.getLogger("shein_logger")
logger.setLevel(logging.DEBUG)


file_handler = RotatingFileHandler(
    log_file_path,
    maxBytes=12 * 1024 * 1024, 
    backupCount=10,             
    encoding="utf-8"
)

file_format = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_format)


console_handler = logging.StreamHandler(sys.stdout)
console_format = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S"
)
console_handler.setFormatter(console_format)


if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


external_packages = ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "sqlalchemy"]
for pkg_name in external_packages:
    pkg_logger = logging.getLogger(pkg_name)
    pkg_logger.setLevel(logging.DEBUG)
    pkg_logger.addHandler(file_handler)
    pkg_logger.addHandler(console_handler)
    pkg_logger.propagate = False
