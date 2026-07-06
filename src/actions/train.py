"""
actions/train.py

Reads current army camp capacity via OCR (e.g. "142/200") and, if under
capacity, opens the barracks and queues a configured troop composition.
"""

from __future__ import annotations

import logging

from ..adb_controller import ADBController
from ..ocr import OCRReader
from ..vision import TemplateLibrary

# ROI for the army camp counter text, in reference-resolution coordinates.
# You must calibrate this to where the "current/max" troop text appears on
# your emulator -- see templates/README.md for how to find coordinates.
ARMY_CAPACITY_ROI = (1000, 20, 140, 40)  # (x, y, w, h) -- placeholder, calibrate this

# Desired troop composition: template_name -> count to queue per cycle.
DEFAULT_COMPOSITION = {
    "troops/barbarian": 10,
    "troops/archer": 10,
}


def _parse_capacity(text: str) -> tuple[int, int] | None:
    if "/" not in text:
        return None
    try:
        current_str, max_str = text.split("/", 1)
        return int("".join(filter(str.isdigit, current_str))), int("".join(filter(str.isdigit, max_str)))
    except ValueError:
        return None


def run(
    adb: ADBController,
    templates: TemplateLibrary,
    ocr: OCRReader,
    screenshot,
    threshold: float,
    logger: logging.Logger,
    action_delay: tuple[float, float],
) -> int:
    capacity_text = ocr.read_text(screenshot, ARMY_CAPACITY_ROI)
    parsed = _parse_capacity(capacity_text)
    if parsed is None:
        logger.debug("Could not parse army capacity from '%s'; skipping train step", capacity_text)
        return 0

    current, maximum = parsed
    if current >= maximum:
        logger.info("Army full (%d/%d), skipping training", current, maximum)
        return 0

    barracks_button = templates.find(screenshot, "buttons/barracks", threshold=threshold)
    if barracks_button is None:
        logger.debug("Barracks button not visible, skipping training this cycle")
        return 0

    adb.tap(barracks_button.x, barracks_button.y)
    adb.human_delay(*action_delay)

    queued = 0
    screenshot = adb.screenshot()
    for troop_name, count in DEFAULT_COMPOSITION.items():
        match = templates.find(screenshot, troop_name, threshold=threshold)
        if match is None:
            continue
        for _ in range(count):
            adb.tap(match.x, match.y)
            adb.human_delay(*action_delay)
            queued += 1

    logger.info("Queued %d troops (army was %d/%d)", queued, current, maximum)
    return queued
