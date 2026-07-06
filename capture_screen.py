"""
capture_screen.py

Quick helper for grabbing timestamped screenshots from the emulator via ADB.
Use this while navigating different game screens (main village, attack screen,
shop, training menu, etc.) so you build up a library of raw captures to crop
template icons from later.

Usage:
    python capture_screen.py
    python capture_screen.py --label attack_screen
    python capture_screen.py --serial emulator-5554 --out captures

Each run saves to:
    captures/<label>_<YYYYMMDD_HHMMSS>.png

Run it multiple times as you move around the game -- every capture gets its
own file, so you never lose a previous screenshot.
"""

import argparse
import os
from datetime import datetime

# Adjust this import path if your project layout differs
from src.adb_controller import ADBController

import cv2


def parse_args():
    parser = argparse.ArgumentParser(description="Capture a timestamped screenshot from the emulator.")
    parser.add_argument(
        "--serial",
        default="emulator-5554",
        help="ADB device serial (check with `tools/adb/adb.exe devices`). Default: emulator-5554",
    )
    parser.add_argument(
        "--adb-path",
        default="tools/adb/adb.exe",
        help="Path to adb executable bundled with the project. Default: tools/adb/adb.exe",
    )
    parser.add_argument(
        "--out",
        default="captures",
        help="Subfolder to save screenshots into. Default: captures",
    )
    parser.add_argument(
        "--label",
        default="screen",
        help="Optional label prefix for the filename, e.g. 'attack_screen'. Default: screen",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Make sure the output subfolder exists
    os.makedirs(args.out, exist_ok=True)

    # Connect to the device
    adb = ADBController(serial=args.serial, adb_path=args.adb_path)

    # Grab the screenshot (should return a numpy/OpenCV-compatible image)
    frame = adb.screenshot()

    # Build a timestamped filename so repeated runs never overwrite each other
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{args.label}_{timestamp}.png"
    filepath = os.path.join(args.out, filename)

    cv2.imwrite(filepath, frame)

    print(f"Saved screenshot to: {filepath}")


if __name__ == "__main__":
    main()