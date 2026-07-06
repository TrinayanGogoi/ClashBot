"""
state_detector.py

Figures out which screen the game is currently showing (home village,
attack-search / matchmaking, in-battle, clan-castle donation popup, shop,
etc.) by looking for a small set of distinctive "anchor" template images
that only appear on that screen.

Add more states here as you build your own template set -- this is meant
as a starting skeleton, not an exhaustive list.
"""

from __future__ import annotations

from enum import Enum, auto

import numpy as np

from .vision import TemplateLibrary


class GameState(Enum):
    HOME_VILLAGE = auto()
    ATTACK_SEARCH = auto()
    IN_BATTLE = auto()
    DONATION_POPUP = auto()
    UNKNOWN = auto()


# Map each state to the anchor template(s) that uniquely identify it.
# These filenames are just suggestions -- populate templates/ to match.
STATE_ANCHORS: dict[GameState, list[str]] = {
    GameState.HOME_VILLAGE: ["buttons/attack"],
    GameState.ATTACK_SEARCH: ["buttons/find_match", "buttons/next"],
    GameState.IN_BATTLE: ["buttons/end_battle", "buttons/surrender"],
    GameState.DONATION_POPUP: ["buttons/donate"],
}


def detect_state(
    screenshot: np.ndarray,
    templates: TemplateLibrary,
    threshold: float = 0.82,
) -> GameState:
    for state, anchor_names in STATE_ANCHORS.items():
        match = templates.find_any(screenshot, anchor_names, threshold=threshold)
        if match is not None:
            return state
    return GameState.UNKNOWN
