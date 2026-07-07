import math
import subprocess
import random
import time
from datetime import datetime
from pathlib import Path


import cv2
import numpy as np
import yaml


class ADB:
    """
    Android Debug Bridge interface.

    Responsibilities:
        - Execute shell commands
        - Capture screenshots
        - Tap
        - Swipe (later)
        - Key events (later)
    """

    def __init__(self, config_path="config/config.yaml"):

        # self.adb = ADB()
        # self.adb.logger = logger

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.config = config

        self.serial = config["device"]["serial"]
        self.adb = config["device"]["adb_path"]

        self.capture_dir = Path("captures")
        self.capture_dir.mkdir(exist_ok=True)

        self.logger = None
        

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def log(self, message):

        if self.logger:
            self.logger(message)

    # ---------------------------------------------------------
    # Internal command runner
    # ---------------------------------------------------------

    def _run(self, command):

        return subprocess.run(
            command,
            capture_output=True,
            text=False,
        )

    # ---------------------------------------------------------
    # Shell
    # ---------------------------------------------------------

    # def shell(self, *command):

    #     result = self._run(
    #         [
    #             self.adb,
    #             "-s",
    #             self.serial,
    #             "shell",
    #             *command,
    #         ]
    #     )

    #     return result

    def shell(self, *args):
        """
        Execute an ADB shell command.

        Example:
            self.shell("input", "keyevent", "3")
            self.shell("input", "tap", "500", "300")
        """

        command = [
            self.adb,
            "-s",
            self.serial,
            "shell",
        ]

        command.extend(map(str, args))

        return self._run(command)

    # ---------------------------------------------------------
    # Screenshot
    # ---------------------------------------------------------

    def screenshot(self, save=False):

        self.log("Capturing screenshot...")

        result = self._run(
            [
                self.adb,
                "-s",
                self.serial,
                "exec-out",
                "screencap",
                "-p",
            ]
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Failed to capture screenshot."
            )

        image = cv2.imdecode(
            np.frombuffer(result.stdout, np.uint8),
            cv2.IMREAD_COLOR,
        )

        if image is None:
            raise RuntimeError(
                "OpenCV failed to decode screenshot."
            )

        if save:

            filename = (
                datetime.now()
                .strftime("%Y%m%d_%H%M%S")
                + ".png"
            )

            path = self.capture_dir / filename

            cv2.imwrite(str(path), image)

            self.log(f"Screenshot saved: {path}")

        return image

    # ---------------------------------------------------------
    # Tap
    # ---------------------------------------------------------

    def tap(
        self,
        x,
        y,
        radius=6,
        delay_before=(0.05, 0.20),
        delay_after=(0.10, 0.25),
    ):
        """
        Perform a human-like tap.

        Parameters
        ----------
        x, y : int
            Target coordinates.

        radius : int
            Maximum distance (pixels) from the target.

        delay_before : tuple
            Random delay before the tap.

        delay_after : tuple
            Random delay after the tap.
        """

        # Human reaction time before tapping
        time.sleep(random.uniform(*delay_before))

        # -------------------------------------------------
        # Random point inside a circle
        # -------------------------------------------------

        angle = random.uniform(0, 2 * math.pi)

        # sqrt() gives a uniform distribution over the area
        distance = radius * math.sqrt(random.random())

        tx = int(round(x + distance * math.cos(angle)))
        ty = int(round(y + distance * math.sin(angle)))

        self.log(f"Tap ({tx}, {ty})")

        result = self.shell(
            "input",
            "tap",
            str(tx),
            str(ty),
        )

        if result.returncode != 0:
            raise RuntimeError("Tap failed.")

        # Small delay after the tap
        time.sleep(random.uniform(*delay_after))

    # ---------------------------------------------------------
    # Swipe
    # ---------------------------------------------------------


    def swipe(self, x1, y1, x2, y2, duration=300):
        """
        Perform a swipe gesture.
        """

        if self.logger:
            self.logger(
                f"Swipe ({x1}, {y1}) -> ({x2}, {y2})"
            )

        self.shell(
            "input",
            "swipe",
            x1,
            y1,
            x2,
            y2,
            duration,
        )

