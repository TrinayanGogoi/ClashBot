"""
ocr.py

Thin wrapper around pytesseract for reading the small bits of text/numbers
that template matching can't handle on its own: resource counts, troop
donation requests, timers, trophy counts, etc.
"""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np
import pytesseract


class OCRReader:
    def __init__(self, tesseract_cmd: Optional[str] = None, digits_whitelist: str = "0123456789/,"):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.digits_whitelist = digits_whitelist

    @staticmethod
    def _preprocess(crop: np.ndarray) -> np.ndarray:
        """
        Game fonts are usually bold with a colored outline on a busy
        background, which trips up default OCR. Upscaling + binarizing
        generally improves accuracy a lot for this kind of stylized text.
        """
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        _thresh, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def read_digits(self, screenshot: np.ndarray, roi: tuple[int, int, int, int]) -> Optional[int]:
        """Read an integer from a region of interest (x, y, w, h). Returns None if unparseable."""
        x, y, w, h = roi
        crop = screenshot[y:y + h, x:x + w]
        processed = self._preprocess(crop)
        config = f'--psm 7 -c tessedit_char_whitelist={self.digits_whitelist}'
        text = pytesseract.image_to_string(processed, config=config).strip()
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else None

    def read_text(self, screenshot: np.ndarray, roi: tuple[int, int, int, int]) -> str:
        x, y, w, h = roi
        crop = screenshot[y:y + h, x:x + w]
        processed = self._preprocess(crop)
        return pytesseract.image_to_string(processed, config="--psm 7").strip()
