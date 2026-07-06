"""
adb_controller.py

Thin wrapper around the Android Debug Bridge (ADB) that gives the rest of the
bot two capabilities:
  1. capture the current screen as an image (numpy array)
  2. inject synthetic taps / swipes

This intentionally uses the `adb` binary via subprocess rather than a raw
socket protocol implementation -- it's slower, but far easier to read and
debug for a college project, and it's the same approach the original
closed-source tool uses.
"""

from __future__ import annotations

import random
import subprocess
import time
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class ADBController:
    serial: str
    adb_path: str = "adb"  # assumes adb is on PATH; override with a full path if not

    def _run(self, *args: str, capture: bool = False) -> bytes:
        cmd = [self.adb_path, "-s", self.serial, *args]
        result = subprocess.run(cmd, capture_output=capture, check=True)
        return result.stdout if capture else b""

    def connect(self) -> None:
        """Make sure adb server knows about this device (for network emulators)."""
        subprocess.run([self.adb_path, "connect", self.serial], capture_output=True)

    def screenshot(self) -> np.ndarray:
        """Return the current screen as a BGR numpy array (OpenCV format)."""
        raw = self._run("exec-out", "screencap", "-p", capture=True)
        arr = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError(
                "Failed to decode screenshot from adb. Check that the device "
                f"'{self.serial}' is connected and unlocked."
            )
        return img

    def tap(self, x: int, y: int, jitter_px: int = 3) -> None:
        """
        Tap at (x, y). A small random jitter is added so repeated taps on the
        same button don't land on the exact same pixel every time -- this is
        both more human-like and more robust against slightly-off template
        matches.
        """
        jx = x + random.randint(-jitter_px, jitter_px)
        jy = y + random.randint(-jitter_px, jitter_px)
        self._run("shell", "input", "tap", str(jx), str(jy))

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self._run(
            "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration_ms),
        )

    def human_delay(self, low: float, high: float) -> None:
        """Sleep a randomized amount to avoid perfectly periodic bot timing."""
        time.sleep(random.uniform(low, high))
