"""
actions/collect.py

Scans the home-village screenshot for resource collector icons (gold mines,
elixir collectors, dark elixir drills) that have a "full" indicator, and
taps each one to collect.
"""

from __future__ import annotations

import logging

from ..adb_controller import ADBController
from ..vision import TemplateLibrary

# Icon variants that indicate a collector is ready to be tapped.
# You will capture these yourself: e.g. a gold mine template with the
# little resource bubble icon floating above it.
COLLECTIBLE_TEMPLATES = [
    "resources/gold_mine_full",
    "resources/elixir_collector_full",
    "resources/dark_elixir_drill_full",
]


def run(adb: ADBController, templates: TemplateLibrary, screenshot, threshold: float,
        logger: logging.Logger, action_delay: tuple[float, float]) -> int:
    """Tap every visible 'full' collector. Returns number of taps performed."""
    taps = 0
    for name in COLLECTIBLE_TEMPLATES:
        if name not in templates.names():
            continue
        match = templates.find(screenshot, name, threshold=threshold)
        if match is None:
            continue
        logger.info("Collecting from %s at (%d, %d) conf=%.2f", name, match.x, match.y, match.confidence)
        adb.tap(match.x, match.y)
        adb.human_delay(*action_delay)
        taps += 1
    return taps
