"""
logger.py

Small logging setup: writes to console and to a rotating-by-run log file
under logs/. Also optionally saves the current screenshot alongside a log
line for debugging why the bot made a given decision.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

import cv2
import numpy as np


def build_logger(log_dir: str, level: str = "INFO") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"run_{run_stamp}.log")

    logger = logging.getLogger("autoclash")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    return logger


def save_debug_screenshot(log_dir: str, screenshot: np.ndarray, tag: str) -> str:
    debug_dir = os.path.join(log_dir, "screenshots")
    os.makedirs(debug_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(debug_dir, f"{stamp}_{tag}.png")
    cv2.imwrite(path, screenshot)
    return path
