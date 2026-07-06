"""
actions/donate.py

If a clan-castle troop request popup is visible, taps the requested troop
icon repeatedly until the request is filled (or a max-donation safety cap
is hit).
"""

from __future__ import annotations

import logging

from ..adb_controller import ADBController
from ..ocr import OCRReader
from ..vision import TemplateLibrary

MAX_DONATIONS_PER_REQUEST = 5  # safety cap so a bad OCR read can't spam-tap forever


def run(
    adb: ADBController,
    templates: TemplateLibrary,
    ocr: OCRReader,
    screenshot,
    threshold: float,
    logger: logging.Logger,
    action_delay: tuple[float, float],
) -> int:
    donate_button = templates.find(screenshot, "buttons/donate", threshold=threshold)
    if donate_button is None:
        return 0

    logger.info("Donation popup detected, opening it")
    adb.tap(donate_button.x, donate_button.y)
    adb.human_delay(*action_delay)

    # After opening the popup, re-screenshot to find the requested troop icon.
    screenshot = adb.screenshot()
    troop_match = templates.find_any(
        screenshot,
        [name for name in templates.names() if name.startswith("troops/")],
        threshold=threshold,
    )
    if troop_match is None:
        logger.info("Could not identify requested troop icon; skipping donation")
        return 0

    donations = 0
    for _ in range(MAX_DONATIONS_PER_REQUEST):
        adb.tap(troop_match.x, troop_match.y)
        adb.human_delay(*action_delay)
        donations += 1

    logger.info("Donated %s x%d", troop_match.name, donations)
    return donations
