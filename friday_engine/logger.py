"""
F.R.I.D.A.Y. Centralized Logging Module
Configures structured console & file loggers with rotation, ISO timestamps,
and colorized console outputs for agent observability.
"""

from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class ANSIColor:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class FridayFormatter(logging.Formatter):
    """Custom colorized formatter for CLI and stdout."""

    FORMAT_STRING = "%(asctime)s | %(levelname)-7s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    COLOR_MAP = {
        logging.DEBUG: ANSIColor.CYAN,
        logging.INFO: ANSIColor.GREEN,
        logging.WARNING: ANSIColor.YELLOW,
        logging.ERROR: ANSIColor.RED,
        logging.CRITICAL: ANSIColor.RED + ANSIColor.BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        orig_msg = super().format(record)
        # Apply color if output is a TTY or on Windows terminal
        color = self.COLOR_MAP.get(record.levelno, ANSIColor.RESET)
        return f"{color}{orig_msg}{ANSIColor.RESET}"


def setup_logger(
    name: str = "friday",
    log_level: str = "INFO",
    log_dir: Optional[str | Path] = None,
) -> logging.Logger:
    """
    Setup and return a configured logger with console and rotating file handlers.
    """
    logger = logging.getLogger(name)
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Avoid duplicate handlers if setup called multiple times
    if logger.handlers:
        return logger

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(FridayFormatter(FridayFormatter.FORMAT_STRING, datefmt=FridayFormatter.DATE_FORMAT))
    logger.addHandler(console_handler)

    # 2. File Handler (Rotating)
    if log_dir is None:
        log_dir = Path("logs")
    else:
        log_dir = Path(log_dir)

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_path = log_dir / f"{name}.log"
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_format = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except Exception as exc:
        print(f"[WARN] Failed to initialize file logger at {log_dir}: {exc}", file=sys.stderr)

    return logger


# Default logger instance
logger = setup_logger("friday_engine")
