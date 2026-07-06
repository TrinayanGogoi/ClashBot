#!/usr/bin/env python3
"""
AutoClash-Edu - educational Clash of Clans automation bot.

Usage:
    python main.py [--config config/config.yaml] [--cycles N]

Before running:
  1. Start your Android emulator and enable ADB (e.g. `adb connect 127.0.0.1:5555`).
  2. Open Clash of Clans in the emulator and log into the account you intend
     to test with (use a throwaway/test account -- see README.md).
  3. Populate templates/ with your own cropped icons (see templates/README.md).
  4. Calibrate any pixel coordinates / ROIs in config.yaml and src/actions/*.py
     to match your emulator's resolution.
"""

from __future__ import annotations

import argparse

from src.bot import AutoClashBot


def main() -> None:
    parser = argparse.ArgumentParser(description="AutoClash-Edu")
    parser.add_argument("--config", default="config/config.yaml", help="Path to config.yaml")
    parser.add_argument("--cycles", type=int, default=None, help="Override max_cycles for a quick test run")
    args = parser.parse_args()

    bot = AutoClashBot(config_path=args.config)
    if args.cycles is not None:
        bot.config["behavior"]["max_cycles"] = args.cycles

    bot.run()


if __name__ == "__main__":
    main()
