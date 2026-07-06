# AutoClash-Edu

A small, readable, from-scratch educational recreation of the "vision +
input-injection" architecture used by Clash of Clans automation tools. Built
as a college project to demonstrate:

- Screen automation via ADB (screenshot capture + synthetic input)
- Computer vision (OpenCV template matching) for UI element detection
- OCR (Tesseract via pytesseract) for reading in-game numbers/text
- A simple perceive -> decide -> act state machine

## Architecture

```
main.py                     entry point / CLI
config/config.yaml          all tunables (device serial, thresholds, timing, loop order)
src/
  adb_controller.py         screenshot + tap/swipe via ADB
  vision.py                 template loading + matching (OpenCV)
  ocr.py                    text/number reading (Tesseract)
  state_detector.py         maps screen -> GameState via anchor templates
  logger.py                 run logs + debug screenshots
  bot.py                    orchestrator: builds everything, runs the loop
  actions/
    collect.py               tap full resource collectors
    donate.py                fill clan-castle troop requests
    train.py                 queue troops when under army capacity
    attack.py                find match -> deploy -> end battle -> return home
templates/                  YOUR OWN cropped icon images go here (see templates/README.md)
logs/                       run logs + optional debug screenshots (created at runtime)
```

## Setup

```bash
python -m venv venv
source venv/bin/activate         # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

You also need:
- **ADB** installed and on your PATH (part of Android SDK Platform Tools).
- **Tesseract OCR** installed natively (pytesseract calls the system binary).
  On Windows, install it and either add it to PATH or set
  `ocr.tesseract_cmd` in config.yaml to the full path of `tesseract.exe`.
- An Android emulator (MEmu / LDPlayer / Nox / BlueStacks) with ADB debugging
  enabled, running Clash of Clans, logged into a **test account** — not your
  main account (see "Important caveats" below).

## Calibration steps (required before it will actually work)

1. Run `adb devices` and confirm your emulator's serial, then set it in
   `config/config.yaml` under `device.serial`.
2. Populate `templates/` with your own cropped icons — see
   `templates/README.md`. This is the single most important step; the bot is
   only as good as its templates.
3. Update any hardcoded pixel coordinates for your resolution:
   - `src/actions/train.py` -> `ARMY_CAPACITY_ROI`
   - `src/actions/attack.py` -> `DEPLOY_POINTS`
4. Do a short supervised test run before letting it loop unattended:
   ```bash
   python main.py --cycles 1
   ```
   Check `logs/` for what it detected and did, and `logs/screenshots/` (if
   `save_debug_screenshots: true`) to see what it was looking at.

## Extending this for a bigger project

Good directions to take this further, depending on what your coursework wants
to emphasize:
- Swap simple edge-deployment in `attack.py` for a heuristic or learned model
  that picks deployment points based on detected defensive buildings.
- Replace template matching with a trained object detector (e.g. a small
  YOLO model) for a more robust CV component.
- Add a proper finite-state machine or behavior tree instead of the fixed
  `behavior.loop` list, so the bot can react to unexpected screens.
- Log structured data per cycle (resources collected, troops trained,
  win/loss) to a CSV/SQLite file and produce plots — turns this into a nice
  data-analysis angle too.

## Important caveats

- **Terms of Service**: Supercell's ToS prohibits third-party automation
  tools. Using this against a real account risks a ban. Use a disposable
  test account, and treat this as a local automation/CV exercise rather than
  something to run against an account you care about.
- **No game assets included**: as noted in `templates/README.md`, you must
  capture your own icon crops. Nothing under `templates/` ships with actual
  Supercell artwork.
- **Brittleness by design of the approach**: template matching and fixed
  pixel coordinates break whenever the game UI, resolution, or your
  emulator's zoom level changes. This is expected and is itself worth
  discussing in a write-up — it's a good illustration of why vision-based
  automation is fragile compared to, say, an official API.
