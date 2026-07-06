"""
check_setup.py

Run this before your first full bot run (or any time something feels broken)
to verify that all the pieces are wired up correctly:

    1. Bundled ADB binary is present and runs
    2. An emulator/device is connected and authorized
    3. A screenshot can actually be pulled from it
    4. Tesseract OCR is present and runs
    5. OCR can read text from a real screenshot (sanity check, not accuracy check)
    6. config/config.yaml exists and has the expected keys

Usage:
    python check_setup.py

Exits with code 0 if everything passes, 1 if anything fails -- useful if you
want to call this from a batch/shell script before main.py.
"""

import os
import subprocess
import sys

try:
    import yaml
except ImportError:
    yaml = None

try:
    import cv2
except ImportError:
    cv2 = None


PASS = "[OK]  "
FAIL = "[FAIL]"
WARN = "[WARN]"


def check(label, ok, detail=""):
    tag = PASS if ok else FAIL
    print(f"{tag} {label}" + (f" -- {detail}" if detail else ""))
    return ok


def check_adb_binary(adb_path):
    if not os.path.isfile(adb_path):
        return check("ADB binary found", False, f"not found at {adb_path}")
    try:
        result = subprocess.run(
            [adb_path, "version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        return check("ADB binary found", True, version_line)
    except Exception as e:
        return check("ADB binary found", False, str(e))


def check_device_connected(adb_path, serial):
    try:
        result = subprocess.run(
            [adb_path, "devices"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = [l.strip() for l in result.stdout.splitlines()[1:] if l.strip()]
        devices = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                devices[parts[0]] = parts[1]

        if serial not in devices:
            return check(
                "Emulator connected",
                False,
                f"'{serial}' not in device list: {devices or 'none found'}. "
                f"Try `adb connect 127.0.0.1:5555` (port varies by emulator).",
            )

        status = devices[serial]
        if status != "device":
            return check(
                "Emulator connected",
                False,
                f"'{serial}' is present but status is '{status}' (expected 'device'). "
                f"If 'unauthorized', accept the USB debugging prompt inside the emulator.",
            )

        return check("Emulator connected", True, f"{serial} ({status})")
    except Exception as e:
        return check("Emulator connected", False, str(e))


def check_screenshot(adb_path, serial):
    if cv2 is None:
        return check("Screenshot capture", False, "opencv-python (cv2) not installed")
    try:
        sys.path.insert(0, os.getcwd())
        from src.adb_controller import ADBController

        adb = ADBController(serial=serial, adb_path=adb_path)
        frame = adb.screenshot()

        if frame is None or frame.size == 0:
            return check("Screenshot capture", False, "screenshot() returned empty frame")

        h, w = frame.shape[:2]

        os.makedirs("captures", exist_ok=True)
        test_path = os.path.join("captures", "_setup_check.png")
        cv2.imwrite(test_path, frame)

        return check("Screenshot capture", True, f"{w}x{h}, saved to {test_path}"), frame
    except Exception as e:
        return check("Screenshot capture", False, str(e)), None


def check_tesseract(tesseract_cmd, tessdata_dir):
    # tesseract_cmd is None -> config says "use system PATH"
    exe = tesseract_cmd if tesseract_cmd else "tesseract"
    try:
        env = os.environ.copy()
        if tessdata_dir and os.path.isdir(tessdata_dir):
            env["TESSDATA_PREFIX"] = tessdata_dir

        result = subprocess.run(
            [exe, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        out = result.stdout or result.stderr
        version_line = out.splitlines()[0] if out else "unknown"
        source = f"config ocr.tesseract_cmd -> {exe}" if tesseract_cmd else "system PATH"
        return check("Tesseract binary found", True, f"{version_line} ({source})")
    except FileNotFoundError:
        return check(
            "Tesseract binary found",
            False,
            f"'{exe}' not runnable. Check ocr.tesseract_cmd in config.yaml or your system PATH.",
        )
    except Exception as e:
        return check("Tesseract binary found", False, str(e))


def check_ocr_on_frame(frame, tesseract_cmd, tessdata_dir):
    if frame is None:
        return check("OCR sanity check", False, "skipped, no screenshot available")
    try:
        import pytesseract

        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        if tessdata_dir and os.path.isdir(tessdata_dir):
            os.environ["TESSDATA_PREFIX"] = tessdata_dir

        text = pytesseract.image_to_string(frame)
        stripped = text.strip()
        detail = f"read {len(stripped)} chars" if stripped else "read 0 chars (may be fine if screen has no text)"
        return check("OCR sanity check", True, detail)
    except ImportError:
        return check("OCR sanity check", False, "pytesseract not installed (pip install pytesseract)")
    except Exception as e:
        return check("OCR sanity check", False, str(e))


def check_config():
    config_path = os.path.join("config", "config.yaml")
    if not os.path.isfile(config_path):
        return check("config/config.yaml found", False, "file missing"), {}

    if yaml is None:
        return check("config/config.yaml found", True, "found (install pyyaml to validate contents)"), {}

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}

        # Real schema: nested under device: / ocr: rather than flat keys
        missing = []
        if "device" not in data:
            missing.append("device")
        else:
            for key in ("serial", "adb_path"):
                if key not in data["device"]:
                    missing.append(f"device.{key}")

        if "ocr" not in data:
            missing.append("ocr")

        if missing:
            ok = check("config/config.yaml valid", False, f"missing keys: {missing}")
        else:
            ok = check("config/config.yaml valid", True)

        return ok, data
    except Exception as e:
        return check("config/config.yaml valid", False, str(e)), {}


def main():
    print("Running setup checks for ClashBot...\n")

    # Defaults, overridden by config.yaml if present
    adb_path = os.path.join("tools", "adb", "adb.exe")
    serial = "emulator-5554"
    tesseract_cmd = os.path.join("tools", "tesseract", "tesseract.exe")
    tessdata_dir = os.path.join("tools", "tesseract", "tessdata")

    config_result, config_data = check_config()

    device = config_data.get("device", {})
    serial = device.get("serial", serial)
    adb_path = device.get("adb_path", adb_path)

    ocr_cfg = config_data.get("ocr", {})
    if "ocr" in config_data:
        configured_cmd = ocr_cfg.get("tesseract_cmd")
        # explicit null in config.yaml means "use system PATH"
        tesseract_cmd = configured_cmd if configured_cmd else None
        # fall back to the bundled path if system PATH tesseract isn't there
        if tesseract_cmd is None and not os.path.isfile(os.path.join("tools", "tesseract", "tesseract.exe")):
            tesseract_cmd = None
        elif tesseract_cmd is None:
            tesseract_cmd = os.path.join("tools", "tesseract", "tesseract.exe")

    results = []

    results.append(check_adb_binary(adb_path))
    results.append(check_device_connected(adb_path, serial))

    screenshot_result, frame = check_screenshot(adb_path, serial)
    results.append(screenshot_result)

    results.append(check_tesseract(tesseract_cmd, tessdata_dir))
    results.append(check_ocr_on_frame(frame, tesseract_cmd, tessdata_dir))
    results.append(config_result)

    print()
    if all(results):
        print("All checks passed. You're good to run: python main.py --cycles 1")
        sys.exit(0)
    else:
        print("One or more checks failed -- fix the issues above before running main.py.")
        sys.exit(1)


if __name__ == "__main__":
    main()
