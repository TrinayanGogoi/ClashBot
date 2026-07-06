"""
vision.py

Loads template images (small cropped icons) and finds them inside a full
screenshot using OpenCV's normalized cross-correlation template matching.

Template naming convention (mirrors the folder layout you should build in
templates/):
    templates/
        buttons/attack.png
        buttons/train.png
        buttons/donate.png
        buttons/return_home.png
        resources/gold_mine.png
        resources/elixir_collector.png
        troops/barbarian.png
        ...

NOTE ON GAME ASSETS: this repo does not ship any Clash of Clans artwork.
You need to capture your own template crops from your own game client
(see templates/README.md). That keeps this project free of third-party
copyrighted assets and is also just good practice, since icon art changes
between game versions/resolutions anyway.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np


@dataclass
class Match:
    name: str
    confidence: float
    x: int          # center x in screenshot coordinates
    y: int          # center y in screenshot coordinates
    width: int
    height: int


class TemplateLibrary:
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self._templates: dict[str, np.ndarray] = {}
        self._load_all()

    def _load_all(self) -> None:
        for root, _dirs, files in os.walk(self.template_dir):
            for f in files:
                if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                path = os.path.join(root, f)
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                if img is None:
                    continue
                # key = path relative to template_dir, without extension
                rel = os.path.relpath(path, self.template_dir)
                key = os.path.splitext(rel)[0].replace(os.sep, "/")
                self._templates[key] = img

    def names(self) -> list[str]:
        return list(self._templates.keys())

    def find(
        self,
        screenshot: np.ndarray,
        template_name: str,
        threshold: float = 0.82,
        roi: Optional[tuple[int, int, int, int]] = None,  # (x, y, w, h)
    ) -> Optional[Match]:
        """Find a single best match of `template_name` inside screenshot."""
        template = self._templates.get(template_name)
        if template is None:
            raise KeyError(f"No template loaded for '{template_name}'")

        search_img = screenshot
        offset_x = offset_y = 0
        if roi is not None:
            x, y, w, h = roi
            search_img = screenshot[y:y + h, x:x + w]
            offset_x, offset_y = x, y

        if search_img.shape[0] < template.shape[0] or search_img.shape[1] < template.shape[1]:
            return None

        result = cv2.matchTemplate(search_img, template, cv2.TM_CCOEFF_NORMED)
        _min_val, max_val, _min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val < threshold:
            return None

        th, tw = template.shape[:2]
        top_left_x = max_loc[0] + offset_x
        top_left_y = max_loc[1] + offset_y
        return Match(
            name=template_name,
            confidence=float(max_val),
            x=top_left_x + tw // 2,
            y=top_left_y + th // 2,
            width=tw,
            height=th,
        )

    def find_any(
        self,
        screenshot: np.ndarray,
        template_names: list[str],
        threshold: float = 0.82,
    ) -> Optional[Match]:
        """Return the highest-confidence match among several candidate templates."""
        best: Optional[Match] = None
        for name in template_names:
            m = self.find(screenshot, name, threshold=threshold)
            if m and (best is None or m.confidence > best.confidence):
                best = m
        return best
