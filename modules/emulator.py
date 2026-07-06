import subprocess
import time
from pathlib import Path

import yaml


class LDPlayer:
    """
    LDPlayer controller.

    Responsibilities:
        - Start LDPlayer
        - Wait for Android boot
        - Resolve launcher activities
        - Launch Android apps
    """

    def __init__(self, config_path="config/config.yaml"):

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.config = config

        # Device
        self.serial = config["device"]["serial"]
        self.adb = config["device"]["adb_path"]

        # Emulator
        emulator = config["emulator"]

        if emulator["type"].lower() != "ldplayer":
            raise ValueError("Only LDPlayer is currently supported.")

        self.instance_index = emulator["instance_index"]

        self.ldplayer_path = Path(emulator["install_path"])

        self.ldconsole = self.ldplayer_path / "ldconsole.exe"

        if not self.ldconsole.exists():
            raise FileNotFoundError(
                f"Cannot find LDConsole:\n{self.ldconsole}"
            )

    def _run(self, command):
        """
        Execute a subprocess command.
        """

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

    def list_devices(self):
        """
        Return all connected ADB devices.
        """

        result = self._run([self.adb, "devices"])

        devices = []

        for line in result.stdout.splitlines():

            if "\tdevice" in line:
                devices.append(line.split()[0])

        return devices

    def is_running(self):
        """
        Check whether the configured emulator is connected.
        """

        return self.serial in self.list_devices()

    def start(self):
        """
        Launch the configured LDPlayer instance.
        """

        if self.is_running():
            print(f"Emulator already running ({self.serial})")
            return

        print(f"Starting LDPlayer instance {self.instance_index}...")

        self._run(
            [
                str(self.ldconsole),
                "launch",
                "--index",
                str(self.instance_index),
            ]
        )

    def wait_for_device(self, timeout=120):
        """
        Wait until ADB detects the emulator.
        """

        print("Waiting for emulator...")

        start = time.time()

        while time.time() - start < timeout:

            if self.serial in self.list_devices():

                subprocess.run(
                    [
                        self.adb,
                        "-s",
                        self.serial,
                        "wait-for-device",
                    ]
                )

                print(f"Connected to {self.serial}")

                return self.serial

            time.sleep(2)

        raise TimeoutError(
            f"Timed out waiting for {self.serial}"
        )

    def wait_for_boot(self, serial=None):
        """
        Wait until Android has finished booting.
        """

        if serial is None:
            serial = self.serial

        print("Waiting for Android boot...")

        while True:

            result = self._run(
                [
                    self.adb,
                    "-s",
                    serial,
                    "shell",
                    "getprop",
                    "sys.boot_completed",
                ]
            )

            if result.stdout.strip() == "1":
                break

            time.sleep(2)

        print("Android boot completed.")

    def resolve_activity(self, package_name, serial=None):
        """
        Resolve the launcher activity for an installed package.
        """

        if serial is None:
            serial = self.serial

        result = self._run(
            [
                self.adb,
                "-s",
                serial,
                "shell",
                "cmd",
                "package",
                "resolve-activity",
                "--brief",
                package_name,
            ]
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        lines = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if not lines:
            raise RuntimeError(
                f"Could not resolve launcher activity for {package_name}"
            )

        activity = lines[-1]

        if "/" not in activity:
            raise RuntimeError(
                f"Unexpected resolve-activity output:\n{result.stdout}"
            )

        return activity

    def launch_app(self, package_name, serial=None):
        """
        Launch any installed Android app.
        """

        if serial is None:
            serial = self.serial

        activity = self.resolve_activity(package_name, serial)

        print(f"Launching {package_name}...")
        print(f"Resolved activity: {activity}")

        result = self._run(
            [
                self.adb,
                "-s",
                serial,
                "shell",
                "am",
                "start",
                "-n",
                activity,
            ]
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to launch app:\n{result.stderr}"
            )

        print("App launched successfully.")