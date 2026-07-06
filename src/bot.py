"""
bot.py

Top-level orchestrator: loads config, builds the ADB connection, template
library and OCR reader, then runs the perceive -> decide -> act loop defined
by `behavior.loop` in config.yaml.
"""

from __future__ import annotations

import time
from typing import Any

import yaml

from .actions import attack as attack_action
from .actions import collect as collect_action
from .actions import donate as donate_action
from .actions import train as train_action
from .adb_controller import ADBController
from .logger import build_logger, save_debug_screenshot
from .ocr import OCRReader
from .vision import TemplateLibrary


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class AutoClashBot:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)

        self.logger = build_logger(
            self.config["logging"]["log_dir"],
            self.config["logging"].get("level", "INFO"),
        )

        self.adb = ADBController(
            serial=self.config["device"]["serial"],
            adb_path=self.config["device"].get("adb_path", "adb"),
        )
        self.adb.connect()

        self.templates = TemplateLibrary(self.config["vision"]["template_dir"])
        self.logger.info("Loaded %d templates", len(self.templates.names()))

        ocr_cfg = self.config["ocr"]
        self.ocr = OCRReader(
            tesseract_cmd=ocr_cfg.get("tesseract_cmd"),
            digits_whitelist=ocr_cfg.get("digits_only_whitelist", "0123456789"),
        )

        self.threshold = self.config["vision"]["match_threshold"]
        self.action_delay = (
            self.config["timing"]["min_action_delay"],
            self.config["timing"]["max_action_delay"],
        )

    def run(self) -> None:
        cycle = 0
        max_cycles = self.config["behavior"].get("max_cycles")
        loop_steps = self.config["behavior"]["loop"]

        self.logger.info("Starting AutoClash-Edu bot. Steps per cycle: %s", loop_steps)

        while max_cycles is None or cycle < max_cycles:
            cycle += 1
            self.logger.info("--- Cycle %d ---", cycle)
            try:
                self._run_cycle(loop_steps)
            except Exception:
                self.logger.exception("Unhandled error during cycle %d", cycle)

            time.sleep(self.config["timing"]["loop_delay_seconds"])

    def _run_cycle(self, steps: list[str]) -> None:
        screenshot = self.adb.screenshot()

        if self.config["logging"].get("save_debug_screenshots"):
            save_debug_screenshot(self.config["logging"]["log_dir"], screenshot, "cycle_start")

        for step in steps:
            if step == "collect":
                collect_action.run(
                    self.adb, self.templates, screenshot, self.threshold,
                    self.logger, self.action_delay,
                )
            elif step == "donate":
                donate_action.run(
                    self.adb, self.templates, self.ocr, screenshot, self.threshold,
                    self.logger, self.action_delay,
                )
            elif step == "train":
                train_action.run(
                    self.adb, self.templates, self.ocr, screenshot, self.threshold,
                    self.logger, self.action_delay,
                )
            elif step == "attack":
                attack_action.run(
                    self.adb, self.templates, screenshot, self.threshold,
                    self.logger, self.action_delay,
                    self.config["timing"]["attack_search_timeout"],
                )
            else:
                self.logger.warning("Unknown behavior step '%s', skipping", step)

            # Re-screenshot between steps since each action changes the screen.
            screenshot = self.adb.screenshot()
