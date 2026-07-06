"""
actions/attack.py

Handles the attack loop:
  1. Tap "Attack" -> "Find a Match"
  2. Once matched, deploy the configured troop composition across a few
     spread-out drop points along the map edge
  3. Wait for the battle to resolve (or hit a timeout) and return home

This is intentionally simple (edge-spread deployment, no base analysis or
pathing logic) -- a great place to extend the project, e.g. adding a CNN
or heuristic to pick deployment points based on where defenses are weakest.
"""

from __future__ import annotations

import logging
import time

from ..adb_controller import ADBController
from ..vision import TemplateLibrary

DEPLOY_POINTS = [
    (100, 360), (150, 300), (150, 420), (1180, 360), (1130, 300), (1130, 420),
]

DEFAULT_ARMY = ["troops/barbarian", "troops/archer"]


def run(
    adb: ADBController,
    templates: TemplateLibrary,
    screenshot,
    threshold: float,
    logger: logging.Logger,
    action_delay: tuple[float, float],
    search_timeout: float,
) -> bool:
    attack_button = templates.find(screenshot, "buttons/attack", threshold=threshold)
    if attack_button is None:
        logger.debug("Attack button not visible; skipping attack this cycle")
        return False

    logger.info("Starting attack search")
    adb.tap(attack_button.x, attack_button.y)
    adb.human_delay(*action_delay)

    screenshot = adb.screenshot()
    find_match = templates.find_any(screenshot, ["buttons/find_match", "buttons/next"], threshold=threshold)
    if find_match:
        adb.tap(find_match.x, find_match.y)
        adb.human_delay(*action_delay)

    # Poll until we see something that indicates we've landed in a battle
    deadline = time.time() + search_timeout
    in_battle = False
    while time.time() < deadline:
        screenshot = adb.screenshot()
        end_battle = templates.find(screenshot, "buttons/end_battle", threshold=threshold)
        if end_battle is not None:
            in_battle = True
            break
        adb.human_delay(1.0, 2.0)

    if not in_battle:
        logger.info("No match found within timeout; backing out")
        return False

    logger.info("Match found, deploying troops")
    for troop_name in DEFAULT_ARMY:
        screenshot = adb.screenshot()
        troop_match = templates.find(screenshot, troop_name, threshold=threshold)
        if troop_match is None:
            continue
        adb.tap(troop_match.x, troop_match.y)  # select troop in the deploy bar
        adb.human_delay(0.2, 0.5)
        for dx, dy in DEPLOY_POINTS:
            adb.tap(dx, dy)
            adb.human_delay(0.15, 0.4)

    # Let the attack play out, then end it.
    adb.human_delay(20, 30)
    screenshot = adb.screenshot()
    end_battle = templates.find(screenshot, "buttons/end_battle", threshold=threshold)
    if end_battle is not None:
        adb.tap(end_battle.x, end_battle.y)
        adb.human_delay(*action_delay)

    return_home = templates.find(adb.screenshot(), "buttons/return_home", threshold=threshold)
    if return_home is not None:
        adb.tap(return_home.x, return_home.y)

    logger.info("Attack cycle complete")
    return True
